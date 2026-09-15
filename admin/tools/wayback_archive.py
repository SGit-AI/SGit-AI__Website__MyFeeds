#!/usr/bin/env python3
"""Recover a site from the Wayback Machine, into files you own.

    python3 admin/tools/wayback_archive.py mvp.myfeeds.ai --out back-office/archive

No dependencies beyond the standard library, so it runs anywhere Python 3.11 does.

WHY THIS IS NOT THREE LINES OF CURL
-----------------------------------
Three things bite, and each one silently loses content rather than erroring:

1. **`collapse=urlkey` hides good captures.** CDX canonicalises
   `http://host/tag/x` and `https://host/tag/x/` to the SAME key, and collapse keeps
   the FIRST row for a key — which sorts as the http 301, not the https 200. On
   mvp.myfeeds.ai that hid `/tag/how-it-works/` entirely: a real, captured, 200 page
   that a collapsed query says does not exist. So: never collapse. Fetch every
   capture, group by canonical URL, and choose deliberately.

2. **Without `id_` you archive the Wayback Machine, not the site.** A plain
   `/web/<ts>/<url>` response is rewritten: a toolbar is injected, every link is
   rewritten to point back at web.archive.org, and the markup no longer matches what
   was served. The `id_` modifier (`/web/<ts>id_/<url>`) returns the original bytes.

3. **The feed often holds what the crawl missed.** A blog's RSS carries the full
   body of its recent posts in `content:encoded`. Where the crawler captured the feed
   but not the post page, the feed is the only surviving copy — on mvp.myfeeds.ai
   that is most of the long-form writing. So the feed is a first-class source here,
   not a fallback.

The archive is written as: the original bytes, a markdown rendering, and a manifest
that says where every file came from and — importantly — what the sitemap listed that
was never captured at all. A recovery that does not state its gaps is not a recovery.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CDX = "https://web.archive.org/cdx/search/cdx"
WEB = "https://web.archive.org/web"
UA = "myfeeds-archive/1.0 (+https://myfeeds.sgit.ai; recovering our own site)"


# The Internet Archive rate-limits hard on a long asset run. Per-file exponential backoff
# is the wrong shape for that: every file independently waits 3s, 6s, 12s… and the run
# crawls while the server is telling you a specific number of seconds to wait. Honour
# Retry-After, and slow the WHOLE run rather than each file separately, so a throttled run
# is slow-and-finishing instead of slow-and-apparently-hung.
_PACE = {"delay": 0.0}


def fetch(url: str, tries: int = 5, timeout: int = 60) -> bytes:
    """GET with backoff that respects the server. The Internet Archive throttles, 429s and
    goes offline for maintenance; all three are transient and none should lose a run."""
    last = None
    for attempt in range(1, tries + 1):
        if _PACE["delay"]:
            time.sleep(_PACE["delay"])
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                body = r.read()
            if b"Internet Archive services are temporarily offline" in body[:4000]:
                raise RuntimeError("archive.org is in maintenance")
            # A clean response earns the run a little speed back.
            _PACE["delay"] = max(0.0, _PACE["delay"] - 0.25)
            return body
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429:
                # The server named a number. Use it, and keep the new pace for the rest
                # of the run rather than forgetting it on the next file.
                retry_after = e.headers.get("Retry-After")
                wait = float(retry_after) if (retry_after or "").isdigit() else 30.0
                _PACE["delay"] = min(10.0, _PACE["delay"] + 1.0)
                print(f"    429 — waiting {wait:.0f}s, run pace now "
                      f"{_PACE['delay']:.2f}s/request", file=sys.stderr)
                time.sleep(wait)
                continue
            wait = min(60, 3 * 2 ** (attempt - 1))
            print(f"    retry {attempt}/{tries} in {wait}s (HTTP {e.code})", file=sys.stderr)
            time.sleep(wait)
        except Exception as e:  # noqa: BLE001 - every other failure is worth retrying too
            last = e
            wait = min(60, 3 * 2 ** (attempt - 1))
            print(f"    retry {attempt}/{tries} in {wait}s ({type(e).__name__}: {e})",
                  file=sys.stderr)
            time.sleep(wait)
    raise SystemExit(f"giving up on {url}: {last}")


def cdx_index(domain: str, limit: int = 20000) -> list[dict]:
    """Every capture of every URL on the domain. Deliberately NOT collapsed."""
    q = urllib.parse.urlencode({
        "url": domain,
        "matchType": "domain",
        "output": "json",
        "fl": "original,timestamp,statuscode,mimetype,digest",
        "limit": limit,
    })
    rows = json.loads(fetch(f"{CDX}?{q}"))
    header, data = rows[0], rows[1:]
    return [dict(zip(header, r)) for r in data]


def canonical(u: str) -> str:
    """One key per resource: scheme-insensitive, www-insensitive, trailing slash and
    tracking query stripped. This is the grouping CDX's own collapse gets wrong for us."""
    p = urllib.parse.urlparse(u)
    host = p.netloc.lower().removeprefix("www.")
    path = re.sub(r"/+$", "", p.path) or "/"
    keep = urllib.parse.urlencode(
        [(k, v) for k, v in urllib.parse.parse_qsl(p.query)
         if not k.startswith(("trk", "utm_", "fbclid", "gclid"))]
    )
    return f"{host}{path}" + (f"?{keep}" if keep else "")


def best_captures(rows: list[dict], prefer: str = "latest") -> dict[str, dict]:
    """Choose one capture per resource: a 200 always beats a redirect or an error, and
    among 200s take the newest (or oldest with --prefer oldest, for the earliest
    surviving version of a page that later changed)."""
    by: dict[str, list[dict]] = {}
    for r in rows:
        by.setdefault(canonical(r["original"]), []).append(r)
    out = {}
    for key, caps in by.items():
        ok = [c for c in caps if c["statuscode"] == "200"] or caps
        ok.sort(key=lambda c: c["timestamp"], reverse=(prefer == "latest"))
        out[key] = ok[0]
    return out


def local_path(out: Path, url: str, mimetype: str) -> Path:
    p = urllib.parse.urlparse(url)
    path = p.path
    if path.endswith("/") or not path:
        # A feed served at /rss/ is XML, not a page; naming it index.html makes the
        # archive lie about what it holds.
        path = path + ("index.xml" if "xml" in mimetype else "index.html")
    if "." not in Path(path).name:
        path += ".html" if "html" in mimetype else ""
    safe = "/".join(
        urllib.parse.unquote(seg).replace("\\", "_")[:120]
        for seg in path.lstrip("/").split("/") if seg not in ("", ".", "..")
    )
    return out / p.netloc.lower() / safe


TAG_RE = re.compile(r"<[^>]+>")


def html_to_markdown(fragment: str) -> str:
    """Enough markdown to make the recovered prose readable and greppable. The original
    bytes are kept beside it, so this never has to be the only copy."""
    s = fragment
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", s, flags=re.S | re.I)
    s = re.sub(r"<figcaption[^>]*>(.*?)</figcaption>", r"\n\n*\1*\n\n", s, flags=re.S | re.I)
    s = re.sub(r'<img[^>]*?alt="([^"]*)"[^>]*?src="([^"]+)"[^>]*>', r"\n\n![\1](\2)\n\n", s, flags=re.I)
    s = re.sub(r'<img[^>]*?src="([^"]+)"[^>]*>', r"\n\n![](\1)\n\n", s, flags=re.I)
    s = re.sub(r"<pre[^>]*>(.*?)</pre>", lambda m: "\n\n```\n" + TAG_RE.sub("", m.group(1)).strip() + "\n```\n\n", s, flags=re.S | re.I)
    s = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", s, flags=re.S | re.I)
    for n in range(1, 7):
        s = re.sub(rf"<h{n}[^>]*>(.*?)</h{n}>", lambda m, n=n: f"\n\n{'#' * n} " + TAG_RE.sub("", m.group(1)).strip() + "\n\n", s, flags=re.S | re.I)
    s = re.sub(r"<li[^>]*>(.*?)</li>", lambda m: "\n- " + TAG_RE.sub("", m.group(1)).strip(), s, flags=re.S | re.I)
    s = re.sub(r"<blockquote[^>]*>(.*?)</blockquote>", lambda m: "\n\n> " + TAG_RE.sub("", m.group(1)).strip().replace("\n", "\n> ") + "\n\n", s, flags=re.S | re.I)
    s = re.sub(r'<a[^>]*?href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f"[{TAG_RE.sub('', m.group(2)).strip()}]({m.group(1)})", s, flags=re.S | re.I)
    s = re.sub(r"<(strong|b)[^>]*>(.*?)</\1>", r"**\2**", s, flags=re.S | re.I)
    s = re.sub(r"<(em|i)[^>]*>(.*?)</\1>", r"*\2*", s, flags=re.S | re.I)
    s = re.sub(r"</p>|<br\s*/?>", "\n\n", s, flags=re.I)
    s = re.sub(r"<hr[^>]*>", "\n\n---\n\n", s, flags=re.I)
    s = TAG_RE.sub("", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t]+", " ", s)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def cdata(x: str) -> str:
    m = re.match(r"\s*<!\[CDATA\[(.*?)\]\]>\s*$", x, re.S)
    return m.group(1) if m else x


def parse_feed(xml: str) -> list[dict]:
    """A blog feed carries the full body of its recent posts. Where the crawler caught
    the feed but not the post page, this is the only surviving copy of that writing."""
    items = []
    for raw in re.findall(r"<item>(.*?)</item>", xml, re.S):
        def field(tag: str) -> str:
            m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", raw, re.S)
            return html.unescape(cdata(m.group(1)).strip()) if m else ""
        items.append({
            "title": field("title"),
            "link": field("link"),
            "published": field("pubDate"),
            "author": field(r"dc:creator"),
            "categories": [html.unescape(cdata(c)) for c in
                           re.findall(r"<category[^>]*>(.*?)</category>", raw, re.S)],
            "html": cdata(re.search(r"<content:encoded>(.*?)</content:encoded>", raw, re.S).group(1))
                    if re.search(r"<content:encoded>(.*?)</content:encoded>", raw, re.S) else "",
        })
    return items


def slug_of(link: str) -> str:
    return (urllib.parse.urlparse(link).path.strip("/") or "index").split("/")[-1]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domain", help="e.g. mvp.myfeeds.ai")
    ap.add_argument("--out", default="back-office/archive", help="output directory")
    ap.add_argument("--prefer", choices=["latest", "oldest"], default="latest",
                    help="which capture to keep when a URL has several (default: latest)")
    ap.add_argument("--delay", type=float, default=1.5,
                    help="seconds between downloads; be kind to a free archive")
    ap.add_argument("--skip-assets", action="store_true",
                    help="text only: no images, css or js")
    ap.add_argument("--limit", type=int, default=0, help="stop after N downloads (testing)")
    args = ap.parse_args()

    out = Path(args.out).resolve()
    site = out / args.domain
    site.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] indexing every capture of {args.domain} …")
    rows = cdx_index(args.domain)
    print(f"      {len(rows)} captures")
    best = best_captures(rows, args.prefer)
    print(f"      {len(best)} distinct resources (no collapse — see the module docstring)")

    wanted = {k: c for k, c in best.items() if c["statuscode"] == "200"}
    if args.skip_assets:
        wanted = {k: c for k, c in wanted.items()
                  if "html" in c["mimetype"] or "xml" in c["mimetype"] or "json" in c["mimetype"]}
    print(f"      {len(wanted)} recoverable (status 200{'' if not args.skip_assets else ', text only'})")

    manifest = {
        "domain": args.domain,
        "recovered_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tool": "admin/tools/wayback_archive.py",
        "captures_indexed": len(rows),
        "resources": [],
        "feed_posts": [],
        "gaps": [],
    }

    print(f"[2/4] downloading originals (id_ mode — the site's bytes, not the archive's) …")
    done = 0
    for key, cap in sorted(wanted.items()):
        if args.limit and done >= args.limit:
            break
        url = cap["original"]
        dest = local_path(out, url, cap["mimetype"])
        rec = {"url": url, "timestamp": cap["timestamp"], "status": cap["statuscode"],
               "mimetype": cap["mimetype"],
               "wayback": f"{WEB}/{cap['timestamp']}/{url}",
               "file": str(dest.relative_to(out))}
        if dest.exists() and dest.stat().st_size:
            rec["note"] = "already present, not re-fetched"
            manifest["resources"].append(rec)
            continue
        try:
            body = fetch(f"{WEB}/{cap['timestamp']}id_/{url}")
        except SystemExit as e:
            rec["error"] = str(e)
            manifest["resources"].append(rec)
            print(f"  !! {url}: {e}", file=sys.stderr)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        rec["bytes"] = len(body)
        manifest["resources"].append(rec)
        done += 1
        print(f"  ok [{done}/{len(wanted)}] {len(body):>8}b  {dest.relative_to(out)}")
        time.sleep(args.delay)

    print("[3/4] extracting posts from the feed …")
    posts_dir = out / f"{args.domain}__posts"
    posts_dir.mkdir(parents=True, exist_ok=True)
    # Find feeds by what the file IS, not what it is called. A feed can be served at
    # /rss/, /feed/, /index.xml or /atom.xml, and naming the saved file after the URL
    # made this step miss the only copy of most of the writing — once, already.
    feed_files = []
    for f in sorted(site.rglob("*")):
        if not f.is_file() or f.stat().st_size < 200:
            continue
        head = f.read_bytes()[:2048].lower()
        if b"<rss" in head or b"<feed" in head or b"<channel" in head:
            feed_files.append(f)
    seen_slugs = set()
    for f in feed_files:
        try:
            items = parse_feed(f.read_text(encoding="utf-8", errors="replace"))
        except Exception as e:  # noqa: BLE001
            print(f"  !! {f}: {e}", file=sys.stderr)
            continue
        for it in items:
            if not it["html"]:
                continue
            slug = slug_of(it["link"]) or re.sub(r"\W+", "-", it["title"].lower())[:60]
            if slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            body = html_to_markdown(it["html"])
            fm = {
                "title": it["title"], "slug": slug, "url": it["link"],
                "published": it["published"], "author": it["author"],
                "tags": it["categories"], "source": f"feed capture {f.name}",
                "recovered_from": "wayback", "words": len(body.split()),
            }
            (posts_dir / f"{slug}.md").write_text(
                "---\n" + "\n".join(
                    f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm.items()
                ) + "\n---\n\n" + body + "\n", encoding="utf-8")
            manifest["feed_posts"].append(fm)
            print(f"  post {fm['words']:>6}w  {slug}.md")

    print("[4/4] checking the sitemap for what was never captured …")
    listed: set[str] = set()
    for sm in site.rglob("sitemap*.xml"):
        listed |= set(re.findall(r"<loc>(.*?)</loc>", sm.read_text(encoding="utf-8", errors="replace")))
    have = {canonical(r["url"]) for r in manifest["resources"]}
    have |= {canonical(p["url"]) for p in manifest["feed_posts"]}
    for loc in sorted(listed):
        if canonical(loc) not in have:
            manifest["gaps"].append({"url": loc, "reason": "listed in sitemap, never captured"})

    (out / f"{args.domain}__manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print()
    print(f"resources saved : {sum(1 for r in manifest['resources'] if 'error' not in r)}")
    print(f"posts recovered : {len(manifest['feed_posts'])}")
    print(f"sitemap gaps    : {len(manifest['gaps'])}"
          + (" — listed but never archived, so unrecoverable from here:" if manifest["gaps"] else ""))
    for g in manifest["gaps"]:
        print(f"  - {g['url']}")
    print(f"\nmanifest        : {out / (args.domain + '__manifest.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
