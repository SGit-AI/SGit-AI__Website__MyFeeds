"""The back office: everything this site is built from, indexed from what is on disk.

The rule that makes it worth having — and the reason it is generated rather than
written — is that a back office maintained by hand becomes a lie on a schedule. Every
page under /back-office/ derives from files in this repository: the recovered archive
from its manifest, the recovered writing from the markdown the archiver produced, the
tools from the scripts themselves, the documents from a small registry that says where
each one actually lives.

Nothing here is a copy of something that has an owner elsewhere. Where a document lives
in another repository, this indexes it and links to it; where a document exists ONLY in
the Internet Archive, this repository is now its home, and that distinction is recorded
per item rather than blurred.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ARCHIVE = "back-office/archive"


def load_archive(root: Path) -> dict:
    """The recovered site: its manifest, its posts, and — the part that matters — the
    list of things the sitemap named that no crawler ever captured."""
    manifests = sorted((root / ARCHIVE).glob("*__manifest.json"))
    sites = []
    for m in manifests:
        data = json.loads(m.read_text(encoding="utf-8"))
        posts_dir = m.parent / f"{data['domain']}__posts"
        posts = []
        for f in sorted(posts_dir.glob("*.md")):
            meta, body = parse_post(f.read_text(encoding="utf-8"))
            meta["file"] = str(f.relative_to(root))
            meta["body"] = body
            meta["words"] = len(body.split())
            posts.append(meta)
        posts.sort(key=lambda p: (p.get("published_sort", ""), p["slug"]), reverse=True)
        data["posts"] = posts
        data["manifest_file"] = str(m.relative_to(root))
        sites.append(data)
    return {"sites": sites}


MONTHS = {m: i for i, m in enumerate(
    "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), 1)}


def parse_post(text: str) -> tuple[dict, str]:
    """The archiver writes JSON-valued front matter, so this needs no YAML."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 3)
    raw, body = text[4:end], text[end + 4:].lstrip("\n")
    meta: dict = {}
    for line in raw.split("\n"):
        if not line.strip():
            continue
        k, _, v = line.partition(":")
        try:
            meta[k.strip()] = json.loads(v.strip())
        except json.JSONDecodeError:
            meta[k.strip()] = v.strip()
    # "Mon, 24 Mar 2025 13:35:32 GMT" -> sortable, without pulling in a date parser
    m = re.search(r"(\d{1,2}) (\w{3}) (\d{4})", meta.get("published", "") or "")
    if m:
        meta["published_sort"] = f"{m.group(3)}-{MONTHS.get(m.group(2), 0):02d}-{int(m.group(1)):02d}"
        meta["published_human"] = f"{int(m.group(1))} {m.group(2)} {m.group(3)}"
    return meta, body


# Documents that exist in other repositories. Indexed, never copied: a document has one
# owner, and a second copy is a disagreement waiting to happen. `bytes` is deliberately
# absent — this file does not claim a size it did not measure.
DOCUMENTS = [
    {
        "title": "MyFeeds-AI — Business Plan",
        "date": "2025-10-24",
        "kind": "Business plan",
        "where": "MyFeeds-AI__Investor_Relations",
        "path": "pdfs/MyFeeds-AI - Business Plan - 24-Oct-2025.pdf",
        "note": "The plan as submitted. PDF.",
    },
    {
        "title": "Pitch Deck — Never Miss Critical Cyber News (v0.1.2)",
        "date": "2025-11-22",
        "kind": "Pitch deck",
        "where": "MyFeeds-AI__Investor_Relations",
        "path": "pdfs/pitch-decks/Pitch Deck - MyFeeds-AI – Never Miss Critical Cyber News (v0.1.2 | 22 Nov 2025).pdf",
        "note": "The current deck. Its predecessor v0.1.0 is beside it in the same folder.",
    },
    {
        "title": "First MVP of Personalised News Publishing",
        "date": "2025",
        "kind": "Report",
        "where": "MyFeeds-AI__Investor_Relations",
        "path": "pdfs/MyFeeds-AI - First MVP of Personalised News Publishing .pdf",
        "note": "The MVP written up as a document, alongside the posts recovered here.",
    },
    {
        "title": "Pitch deck brief — Perplexity research",
        "date": "2025",
        "kind": "Brief",
        "where": "MyFeeds-AI__Investor_Relations",
        "path": "pdfs/Perplexity Research - MyFeeds-AI-LLM-Brief-Pitch-Decks.md",
        "note": "8,900 words, slide by slide. Markdown, so it is readable without a viewer.",
    },
    {
        "title": "Pitch deck brief — Claude Opus 4.1",
        "date": "2025",
        "kind": "Brief",
        "where": "MyFeeds-AI__Investor_Relations",
        "path": "pdfs/Claude Opus 4.1 - myfeeds-ai-llm-pitch-deck-brief.md",
        "note": "A second brief for the same job, from a different model. Worth reading beside the first.",
    },
    {
        "title": "Personalised news feed — architecture",
        "date": "2025",
        "kind": "Architecture",
        "where": "myfeeds-ai",
        "path": "docs/dev/personalised-news-feed-architecture.md",
        "note": "The engine's own account of the pipeline the recovered posts describe.",
    },
    {
        "title": "Similar services",
        "date": "2025",
        "kind": "Market",
        "where": "myfeeds-ai",
        "path": "docs/similar-services.md",
        "note": "What else exists in this space.",
    },
]

REPOS = {
    "MyFeeds-AI__Investor_Relations": {
        "url": "https://github.com/the-cyber-boardroom/MyFeeds-AI__Investor_Relations",
        "what": "The investor pitch, its source, and the documents behind it. Publishes "
                "investor.myfeeds.ai.",
    },
    "myfeeds-ai": {
        "url": "https://github.com/the-cyber-boardroom/myfeeds-ai",
        "what": "The engine: the pipeline that produced the posts recovered here — RSS "
                "ingestion, entity extraction, graph building, persona selection, output.",
    },
}

TOOLS = [
    {
        "file": "admin/tools/wayback_archive.py",
        "title": "wayback_archive.py",
        "what": "Recovers a site from the Internet Archive into files you own: originals "
                "in id_ mode, a markdown rendering, and a manifest that states what the "
                "sitemap listed and no crawler ever captured.",
        "run": "python3 admin/tools/wayback_archive.py mvp.myfeeds.ai --out back-office/archive",
    },
    {
        "file": "admin/build/build_pages.py",
        "title": "build_pages.py",
        "what": "The site generator. Every page, every markdown twin, llms.txt, the team "
                "pages from their ROLE.md files, and this back office.",
        "run": "python3 admin/build/build_pages.py",
    },
    {
        "file": "admin/build/validate.js",
        "title": "validate.js",
        "what": "The release gate. Link resolution, twin presence, the authoring "
                "contract, status vocabulary, roster agreement, the deploy pipeline.",
        "run": "node admin/build/validate.js",
    },
    {
        "file": "admin/build/verify-live.sh",
        "title": "verify-live.sh",
        "what": "Asks the live site what version it is serving. Green CI means GitHub "
                "accepted an artifact, not that anyone can read it.",
        "run": "./admin/build/verify-live.sh",
    },
]
