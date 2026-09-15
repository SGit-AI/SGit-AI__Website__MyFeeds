#!/usr/bin/env python3
"""myfeeds.sgit.ai — the page generator.

One shared shell (nav, footer, critical style, bridge bootstrap, version stamp) plus one
body file per page under ``admin/content/``. Everything at the repository root is output:
the HTML pages, their markdown twins, ``llms.txt``, ``llms-full.txt``, ``sitemap.xml`` and
``data/team.json``. Edit ``admin/content/`` and the files under ``team/`` — never the
output.

    python3 admin/build/build_pages.py && node admin/build/validate.js

The team pages are generated from ``team/roles/*/ROLE.md`` and the board from
``team/board/*.md``, so the site cannot describe a role the repository does not carry.
"""

from __future__ import annotations

import html
import json
import re
import sys
import urllib.parse
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import backoffice  # noqa: E402  (same folder; the back-office data module)
import feeds  # noqa: E402  (audiences, ontology, joins)

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "admin" / "content"
ROLES_DIR = ROOT / "team" / "roles"
BOARD_DIR = ROOT / "team" / "board"

# The version is owned by admin/build/version.txt — the estate convention, so that the
# deploy workflow every *.sgit.ai site shares can read it without knowing anything about
# this generator. It is bumped exactly once per release and must also appear in that
# release's commit subject ("site vX.Y.Z: ..."); CI fails the release if the two disagree.
VERSION_FILE = Path(__file__).resolve().parent / "version.txt"
try:
    SITE_VERSION = VERSION_FILE.read_text(encoding="utf-8").strip()
except FileNotFoundError:  # pragma: no cover - a checkout without it is broken
    raise SystemExit(f"build: {VERSION_FILE} is missing — it owns the site version")
if not re.fullmatch(r"v\d+\.\d+\.\d+", SITE_VERSION):
    raise SystemExit(f"build: {VERSION_FILE} holds {SITE_VERSION!r}, expected vMAJOR.MINOR.PATCH")

SITE_HOST = "myfeeds.sgit.ai"
SITE_ORIGIN = f"https://{SITE_HOST}"
SITE_NAME = "myfeeds.sgit.ai"
SITE_THESIS = "The LLM was doing too much."
SITE_DESC = (
    "Ask one LLM to read fifty articles and pick five for a CISO and it will — and you "
    "will never be able to say why. MyFeeds decomposes that single opaque call into four "
    "stages with a semantic knowledge graph between them, so every recommendation carries "
    "a provenance trail you can inspect. This site is the argument, the recovered record "
    "of the first MVP, and the back office behind both."
)
LICENCE = "CC BY 4.0 — Dinis Cruz, with AI co-authorship (Claude, Anthropic)."

# One entry per release, appended, never rewritten. The shape is the estate's
# versions/ contract (sgit.ai/docs/guidance): `title` is a SENTENCE, not a label —
# "the settings move into the right-hand column" tells a reader more than "UI
# improvements" ever will — `changes` names files, and a version that corrects an
# earlier one says which and how. Rendered to /admin/versions.html and served as data
# at /versions/index.json + /versions/<version>.json.
VERSION_LOG = [
    {
        "version": "v0.1.0",
        "date": "2026-09-14",
        "title": "the argument, the read-state contract, and the team that runs it",
        "summary": (
            "First release. The thesis that feeds are replaceable and reading is not, "
            "read-state/v1 published as a contract before any implementation, the vault "
            "layout, the build order, and the seven-role dev team the site is run by — "
            "generated from the ROLE.md files rather than described beside them. Nothing "
            "is served yet: the subdomain does not resolve (board card 004)."
        ),
        "changes": [
            "admin/build/build_pages.py — the generator: one shell, 19 pages, twins, "
            "llms.txt, llms-full.txt, sitemap.xml, data/team.json",
            "admin/build/validate.js — the gate",
            "admin/content/ — the eight authored page bodies and pages.json",
            "team/roles/*/ROLE.md — seven roles; team/board/*.md — five cards",
            "assets/site.css, assets/site.js",
        ],
    },
    {
        "version": "v0.1.1",
        "date": "2026-09-14",
        "title": (
            "the site gets the deploy workflow every other *.sgit.ai site has, and the "
            "four version and provenance practices it was missing"
        ),
        "summary": (
            "v0.1.0 shipped a build gate and called it done, which was wrong: it never "
            "published anything. This release replaces it with the estate's shared "
            "deploy-pages pipeline (validate, tag, publish to GitHub Pages) taken from "
            "the sibling sites rather than reinvented, moves version ownership to "
            "admin/build/version.txt so that workflow can read it, and closes four gaps "
            "against sgit.ai/docs/guidance: the version badge is now a link to that "
            "version's own details, versions are served as data, app.json denies by "
            "default with its reason written down, and every page is one click from the "
            "bytes it was rendered from."
        ),
        "changes": [
            ".github/workflows/deploy-pages.yml — replaces build.yml; validate -> tag "
            "-> deploy, matching SGit-AI__Website__Teams",
            "admin/build/version.txt — now owns the version; build_pages.py reads it",
            "admin/build/verify-live.sh — asks the live site what it is serving, "
            "because both remotes in sync is not the same as deployed",
            "versions/index.json + versions/<version>.json — the versions contract",
            "admin/build/build_pages.py — version badge links to its own entry; every "
            "page links its markdown twin; app.json declares permissions {}",
            "admin/build/validate.js — assertions for each of the above",
        ],
        "corrects": (
            "v0.1.0 described a four-step release ending in a live check, and shipped "
            "neither a deploy workflow nor anything to check with. The description was "
            "accurate about the intent and wrong about the repository."
        ),
    },
    {
        "version": "v0.1.2",
        "date": "2026-09-14",
        "title": (
            "the site went live, so the three pages that said it had not are corrected "
            "above the claims rather than instead of them"
        ),
        "summary": (
            "v0.1.1 shipped the deploy workflow and said, in its own release note, that it "
            "made the site deployable rather than deployed. It deployed it. Switching "
            "GitHub Pages on for this repository — which is what the new deploy job does "
            "with actions/configure-pages and the CNAME file — was the missing step, and "
            "the certificate that had never been issued for the host was issued within "
            "minutes. verify-live.sh reports myfeeds.sgit.ai serving v0.1.1. This release "
            "corrects every page that claimed otherwise, closes board card 004 with what "
            "actually blocked it, and records one bookkeeping gap the deploy left behind."
        ),
        "changes": [
            "team/board/004-domain.md — closed: the subdomain was never the blocker, the "
            "missing deploy workflow was. The need was not a need",
            "team/board/008-v010-tag.md — held: v0.1.0 has no tag on the remote, because "
            "its tree carries the workflow file this release replaced and neither "
            "GITHUB_TOKEN nor the session credential may push such a ref (HTTP 403)",
            "admin/content/about/index.html — the honest-edges row for 'live' flips, and "
            "says what it used to say",
            "admin/content/network/index.html — the 'a site that serves nothing' sentence "
            "is corrected in place, with the old wording quoted",
            "admin/content/index.html — the status table records where the site is served",
            "admin/build/build_pages.py — the version badge anchor no longer breaks across "
            "a line mid-tag",
        ],
        "corrects": (
            "v0.1.1's release note ends 'this release makes the site deployable; it does "
            "not make it deployed', and v0.1.0's says nothing is served yet. The first was "
            "wrong within ten minutes of being written — the deploy job it added is "
            "precisely what made the site deployed. Both entries stay as written; this is "
            "the correction above them."
        ),
    },
    {
        "version": "v0.1.3",
        "date": "2026-09-14",
        "title": (
            "the site finds out what MyFeeds actually is, recovers the MVP that proved "
            "it, and gains a back office to keep the evidence in"
        ),
        "summary": (
            "Versions v0.1.0 to v0.1.2 argued that the valuable half of a feed reader is "
            "the record of what you read. That was written with no access to any MyFeeds "
            "source material and it was wrong about the project it claimed to describe. "
            "MyFeeds is a pipeline that decomposes one opaque LLM call — read fifty "
            "articles, pick five for this persona — into four inspectable stages with a "
            "semantic knowledge graph between them, so a recommendation carries a "
            "provenance trail instead of a shrug. The site now argues that, from the "
            "primary sources: fifteen posts recovered out of the Internet Archive, the "
            "open-source engine, and the investor material. The four superseded pages "
            "stay up with a banner rather than being deleted."
        ),
        "changes": [
            "admin/tools/wayback_archive.py — recovers a site from the Internet Archive: "
            "originals in id_ mode, a markdown rendering, and a manifest naming what the "
            "sitemap listed and no crawler caught",
            "back-office/archive/ — 15 posts (13,527 words) and 22 original files from "
            "mvp.myfeeds.ai, plus 9 recorded gaps",
            "back-office/ — the new section: the archive, documents indexed where they "
            "live rather than copied, the tools, and previous versions",
            "admin/content/index.html, admin/content/how-it-works/ — the real argument, "
            "built from the recovered posts",
            "admin/content/{thesis,read-state,vault,build-order}/ — superseded banners; "
            "the pages stay, out of the nav",
            "team/roles/architect/ROLE.md — now owns the pipeline's stage boundaries and "
            "provenance trail, not a read-state schema",
            "team/board/ — cards 001-003 held; 009 (the multi-audience demo) and 010 "
            "(what the archive could not reach) opened",
            "data/site.json — the page inventory as data; validate.js reads it instead of "
            "re-deriving the list",
        ],
        "corrects": (
            "The whole argument of v0.1.0 through v0.1.2. It was a plausible thesis about "
            "feed readers in general and not a description of this project, and it was "
            "asserted on a site named after the project. The pages stay up, marked, "
            "because deleting them would remove the only evidence that this site corrects "
            "itself rather than quietly rewriting. Separately: v0.1.2's validator "
            "reported 19 pages passing while the build produced 38 — it maintained its "
            "own idea of what existed. It now reads the build's published inventory."
        ),
    },
    {
        "version": "v0.1.4",
        "date": "2026-09-15",
        "title": (
            "a committed .pyc broke the staleness check on every push, which is the "
            "gitignore fix from v0.1.0 coming back around"
        ),
        "summary": (
            "v0.1.3 validated clean, committed clean, and failed CI. The cause was a "
            "Python bytecode cache file tracked in the repository: v0.1.0 had to negate "
            "the Python .gitignore's build/ rule to track the generator at all, and the "
            "negation un-ignored __pycache__ along with it. Python rewrites those bytes "
            "on every import, so CI's 'a fresh build must be byte-identical to the "
            "committed tree' check failed regardless of what the release contained. The "
            "gate behaved correctly — deploy is gated on validate, so nothing shipped and "
            "the live site went on serving v0.1.2 rather than half a release."
        ),
        "changes": [
            ".gitignore — re-ignores admin/build/**/__pycache__/ and *.py[cod] after the "
            "negation that un-ignores the generator",
            "admin/build/__pycache__/backoffice.cpython-311.pyc — untracked",
            "admin/build/validate.js — fails on any tracked __pycache__, .pyc, .DS_Store "
            "or node_modules, and asserts the generator and gate ARE tracked, because the "
            "same .gitignore edit could hide them too. Demonstrated red before trusting.",
        ],
        "corrects": (
            "v0.1.3 was announced as shipped. It was committed and pushed; it never "
            "deployed, and the site served v0.1.2 throughout. The failure was in the "
            "repository's own hygiene rather than in anything the release changed, which "
            "is the least interesting kind of outage and the easiest to repeat: the "
            "assertion added here exists so the next one fails at the desk instead of in "
            "CI."
        ),
    },
    {
        "version": "v0.1.5",
        "date": "2026-09-15",
        "title": (
            "the six audiences, the two ontologies and the join between them — and the "
            "first run of the formula finding three defects in its own audience side"
        ),
        "summary": (
            "The machinery the site had been arguing for now exists as data and as a "
            "runnable tool. Six audiences defined as roles with a stated appetite rather "
            "than a tone of voice, each converting news into a different currency; an "
            "article ontology and an audience ontology, every verb carrying a named "
            "inverse that reads as a sentence both ways, with the banned verbs listed and "
            "the reason given; and join/v1, the published formula where the two meet, "
            "executed by admin/tools/join.py rather than described. The worked example is "
            "a real verified article from pt.newsroom.sgit.ai, and the debug view shows "
            "every concern tried, not only the ones that fired."
        ),
        "changes": [
            "admin/content/data/audiences.json — six audiences: the faithful translation "
            "(the control), the founder, the allocator, the executive, the practitioner, "
            "the risk owner. Three axes, six currencies, concerns declared as article types",
            "admin/content/data/ontology.json — the article ontology (16 types, 13 verbs, "
            "4 banned), the audience ontology, and join/v1 with its match weights",
            "admin/tools/join.py — the formula, executed; emits one delivery per audience, "
            "reached or withheld, each with its connections and readings",
            "audiences/, ontology/, explain/, library/ — four new pages; explain/ is the "
            "debug view and library/ makes the recovered MVP readable as sections",
            "api/v1/audiences.json, api/v1/joins.json, data/{audiences,ontology}.json and "
            "data/joins/ — the same facts a reader can fetch",
            "team/board/011 — the daily routine that syncs with pt.newsroom.sgit.ai",
        ],
        "corrects": (
            "Nothing from an earlier release, but the first run of join/v1 corrected "
            "three things in the audience ontology written hours earlier, and the page "
            "shows the before and after rather than the fix alone: a concern matching on "
            "Source fired for every article that freezes its sources and put the security "
            "practitioner at the top of a story about stage names at a startup event; one "
            "entity satisfying two overlapping concerns scored twice and put the executive "
            "above the founder on an event story; and a concern called 'something more "
            "likely or more expensive' fired on any event at all. Concerns can now be "
            "qualified, rank counts each entity once, and the practitioner is correctly "
            "withheld."
        ),
    },
    {
        "version": "v0.1.6",
        "date": "2026-09-15",
        "title": (
            "the site says who wrote it, the corpus grows to three articles and starts "
            "asking questions back, and the ontology's first rule becomes that it does "
            "not have to be right"
        ),
        "summary": (
            "Three changes that belong together. The ontology's first rule is now that it "
            "does not have to be correct — it has to be wrong in ways a human can see and "
            "correct — which outranks every other rule here and changes what the system "
            "is for. Every page now states that it was written by a model and not yet "
            "read by a person, at the top rather than in a footnote, because a site "
            "arguing that automated selection must be checkable cannot itself be an "
            "unmarked pile of model output. And the corpus grew from one article to "
            "three, which was immediately enough for it to start contradicting its own "
            "ontology."
        ),
        "changes": [
            "provenance/ — who made what, the three places a model can be wrong here in "
            "order of damage, and the per-page review status vocabulary",
            "review/ + admin/tools/review.py — the feedback loop: corpus-level findings "
            "as open questions with evidence, a model diagnosis marked as a proposal, and "
            "an answer format. Nothing on the page fixes itself",
            "admin/content/data/articles/ — two more real articles from the newsroom, "
            "extraction marked ai-generated and unreviewed",
            "admin/content/data/ontology.json 0.2.0 — the good-enough-to-be-argued-with "
            "rule, placed first",
            "briefs/to-pt-newsroom-2026-09-15.md — four requests to the newsroom team, "
            "with what we can and cannot work around",
            "admin/build/validate.js — every page must carry a review status and an "
            "AI-generation disclosure",
            "team/board/008 closed won't-fix; 012 opened for the brief",
        ],
        "corrects": (
            "Two things this release found by having more than one article. With one "
            "article the audience ontology looked serviceable; with three, the founder "
            "receives everything and seven concerns have never fired once. Neither is "
            "necessarily a defect — a concern about funding programmes cannot fire on a "
            "newsroom that has not published one — and that ambiguity is exactly why they "
            "are published as questions for a human rather than auto-corrected. "
            "Separately, review.py's first diagnosis named the wrong culprit: a "
            "max-of-counts heuristic pointed at the concern that fires most, which is not "
            "the one that fired on the article that should not have been delivered. It "
            "now reports the whole distribution and lets a reader find it."
        ),
    },
]

NAV = [
    ("how-it-works/index.html", "How it works"),
    ("audiences/index.html", "Audiences"),
    ("explain/index.html", "Explain"),
    ("review/index.html", "Review"),
    ("back-office/archive/index.html", "The MVP archive"),
    ("back-office/index.html", "Back office"),
    ("team/index.html", "Team"),
    ("admin/index.html", "Admin"),
]

FOOTER_COLS = [
    ("The argument", [
        ("how-it-works/index.html", "How it works — the four stages"),
        ("audiences/index.html", "The six audiences"),
        ("ontology/index.html", "The two ontologies"),
        ("explain/index.html", "A worked example"),
        ("library/index.html", "The recovered library"),
        ("back-office/documents/index.html", "The business case"),
        ("about/index.html", "About & honest edges"),
    ]),
    ("Superseded", [
        ("thesis/index.html", "Feeds are replaceable (v0.1.0–v0.1.2)"),
        ("read-state/index.html", "The part nobody exports"),
        ("vault/index.html", "What a feeds vault holds"),
        ("build-order/index.html", "What does not exist yet"),
    ]),
    ("How it is run", [
        ("team/index.html", "The team"),
        ("team/board.html", "The board"),
        ("admin/index.html", "How this site is built"),
        ("admin/versions.html", "Release history"),
    ]),
    ("Back office", [
        ("back-office/index.html", "Everything it is built from"),
        ("back-office/archive/index.html", "The recovered MVP archive"),
        ("back-office/documents/index.html", "Documents"),
        ("back-office/tools/index.html", "Tools"),
    ]),
    ("Elsewhere", [
        ("provenance/index.html", "Who wrote this site"),
        ("review/index.html", "Open questions"),
        ("network/index.html", "The sgit.ai network"),
        ("about/index.html", "About & licence"),
        ("llms.txt", "llms.txt"),
        ("llms-full.txt", "llms-full.txt"),
    ]),
]

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='7' fill='%230f766e'/%3E"
    "%3Cg fill='none' stroke='%23faf9f5' stroke-width='3' stroke-linecap='round'%3E"
    "%3Cpath d='M10 22h.01'/%3E%3Cpath d='M10 16a6 6 0 0 1 6 6'/%3E"
    "%3Cpath d='M10 10a12 12 0 0 1 12 12'/%3E%3C/g%3E%3C/svg%3E"
)

# Every page carries a review status. The default is the true one for this site today:
# written by a model and not yet read by a human. A page moves off the default only when
# somebody names themselves against it, which is why this is a map of exceptions rather
# than a field somebody remembers to set.
REVIEW_DEFAULT = "ai-generated, unreviewed"
REVIEWED: dict[str, str] = {}

CRITICAL_CSS = """
:root{--bg:#faf9f5;--panel:#fff;--panel2:#f2f0e9;--line:#e5e1d5;--fg:#1c1d21;--dim:#5c5f66;
--dim2:#8a8d94;--accent:#0f766e;--accent-dk:#115e59;
--sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--wide:1180px;--measure:74ch}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#14151a;--panel:#1b1d23;
--panel2:#22242b;--line:#2c2f38;--fg:#e8e6e0;--dim:#a3a7b0;--dim2:#767b86;--accent:#2dd4bf;
--accent-dk:#5eead4}}
*,*::before,*::after{box-sizing:border-box}
.skip{position:absolute;left:-9999px;top:0;background:var(--panel);padding:.6rem 1rem;z-index:99}
.skip:focus{left:.5rem;top:.5rem}
body{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:17px;
line-height:1.62}
img{max-width:100%;height:auto}
a{color:var(--accent-dk);text-decoration:none}
main{max-width:var(--wide);margin:0 auto;padding:0 20px 5rem}
main>*{max-width:var(--measure)}
main>.grid,main>.band,main>.tablewrap,main>.wide{max-width:none}
h1{font-size:clamp(1.95rem,1.3rem + 2.4vw,3rem);line-height:1.1;margin:.4rem 0 .6rem}
h2{margin:3rem 0 .8rem;padding-top:1.2rem;border-top:1px solid var(--line)}
.site-head{border-bottom:1px solid var(--line)}
.site-head .bar{max-width:var(--wide);margin:0 auto;padding:.7rem 20px;display:flex;
align-items:baseline;gap:1rem;flex-wrap:wrap}
.site-nav{display:flex;gap:.1rem;flex-wrap:wrap;margin-left:auto;font-size:.88rem}
.site-nav a{color:var(--dim);padding:.22rem .55rem}
.prov{font-size:.78rem;color:var(--dim2);margin:.6rem 0 0}
.site-foot{border-top:1px solid var(--line);background:var(--panel2);color:var(--dim)}
.site-foot .inner{max-width:var(--wide);margin:0 auto;padding:2.2rem 20px 3rem;display:grid;
gap:1.4rem;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));font-size:.86rem}
.site-foot ul{list-style:none;margin:0;padding:0}
pre{overflow-x:auto}
.tablewrap{overflow-x:auto}
table{border-collapse:collapse;width:100%}
""".strip()

# The authoring contract in twenty lines: vault pages render inside a sandboxed frame, so
# a declarative <link>/<script src> would 404 before the bridge installs. Ask the bridge
# first, fall back to fetch on the static mirror, and degrade to unstyled-but-readable.
BOOTSTRAP = """
(function(){var B=%(base)s,n=0,t;
function applied(){try{return getComputedStyle(document.documentElement)
.getPropertyValue('--site-css').trim()==='1'}catch(e){return false}}
function inject(tag,c){if(!c)return;var e=document.createElement(tag);e.textContent=c;
(tag==='style'?document.head:document.body).appendChild(e);}
function viaFetch(){fetch(B+'assets/site.css').then(function(r){return r.ok?r.text():''})
.then(function(c){if(!applied())inject('style',c)}).catch(function(){});
fetch(B+'assets/site.js').then(function(r){return r.ok?r.text():''})
.then(function(c){inject('script',c)}).catch(function(){});}
function viaBridge(sg){if(sg.loadCss&&sg.loadJs){try{sg.loadCss('assets/site.css');
sg.loadJs('assets/site.js');return true}catch(e){}}
if(sg.vfs&&sg.vfs.readText){try{Promise.resolve(sg.vfs.readText('assets/site.css'))
.then(function(c){if(!applied())inject('style',c)});
Promise.resolve(sg.vfs.readText('assets/site.js')).then(function(c){inject('script',c)});
return true}catch(e){}}return false;}
// The two transports are tried concurrently and both are idempotent: fetch starts now so
// the static mirror is never unstyled, and the bridge is used the moment it appears. The
// --site-css sentinel in site.css stops the second arrival applying anything twice.
if(window.sg&&viaBridge(window.sg))return;
viaFetch();
window.addEventListener('sg-ready',function(){if(!applied()&&window.sg)viaBridge(window.sg)},
{once:true});
t=setInterval(function(){if(window.sg){clearInterval(t);if(!applied())viaBridge(window.sg);}
else if(++n>40){clearInterval(t);if(!applied())viaFetch();}},50);})();
""".strip()


# --------------------------------------------------------------------------- utilities


def rel_prefix(path: str) -> str:
    """``thesis/index.html`` -> ``../`` — the depth-aware root for a generated page."""
    return "../" * path.count("/")


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """A deliberately small YAML subset: ``k: v``, ``k: >-`` folded blocks, and ``- ``
    lists. Small enough to have no dependency and to fail loudly on anything else."""
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        raise ValueError("unterminated front matter")
    raw, body = text[4:end], text[end + 4:].lstrip("\n")
    data: dict = {}
    key: str | None = None
    mode: str | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal key, mode, buf
        if key is not None and mode == "folded":
            data[key] = " ".join(x.strip() for x in buf if x.strip())
        key, mode, buf = None, None, []

    for line in raw.split("\n"):
        if not line.strip():
            continue
        if line.startswith("  ") and mode == "folded":
            buf.append(line)
            continue
        if line.startswith("  - ") and mode == "list":
            data[key].append(line[4:].strip())
            continue
        flush()
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            raise ValueError(f"front matter line not understood: {line!r}")
        k, v = m.group(1), m.group(2).strip()
        if v in (">-", ">", "|", "|-"):
            key, mode, buf = k, "folded", []
        elif v == "":
            key, mode, data[k] = k, "list", []
        else:
            data[k] = v.strip("'\"")
    flush()
    return data, body


def md_href(href: str) -> str:
    """Links inside a markdown twin point at markdown, so an agent can traverse the whole
    site without ever parsing HTML."""
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return href
    base, _, frag = href.partition("#")
    if base.endswith(".html"):
        base = base[:-5] + ".md"
    return base + ("#" + frag if frag else "")


class ToMarkdown(HTMLParser):
    """Converts this site's own body HTML — a small, known vocabulary — to markdown.

    It is deliberately not a general converter: an unknown block-level tag is a build
    error rather than silently dropped content, because a silently dropped paragraph is
    exactly the drift the markdown twin exists to prevent.
    """

    BLOCK = {
        "p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "li", "pre", "blockquote",
        "hr",
        "div", "section", "table", "thead", "tbody", "tr", "th", "td", "dl", "dt", "dd",
        "figure", "figcaption", "main", "nav", "header", "footer", "aside",
    }
    INLINE = {"a", "strong", "b", "em", "i", "code", "span", "small", "br", "img", "abbr"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: list[str] = []
        self.buf: list[str] = []
        self.lists: list[list] = []          # [kind, counter]
        self.pre = 0
        self.quote = 0
        self.href: list[str] = []
        self.link = 0            # inside an <a>: block tags become separators, not breaks
        self.card = 0            # inside an <a class="card">: emit as one list item
        self.table: list[list[str]] | None = None
        self.row: list[str] | None = None
        self.header_row = False
        self.unknown: set[str] = set()

    # -- helpers ----------------------------------------------------------------

    def text(self) -> str:
        t = "".join(self.buf).strip()
        self.buf = []
        return re.sub(r"[ \t]*\n[ \t]*", "\n", re.sub(r"[ \t]{2,}", " ", t))

    def emit(self, block: str) -> None:
        if block.strip():
            self.blocks.append(block.rstrip())

    def flush_para(self, prefix: str = "") -> None:
        t = self.text()
        if not t:
            return
        if self.quote:
            t = "\n".join("> " + ln if ln else ">" for ln in t.split("\n"))
        self.emit(prefix + t if prefix else t)

    # -- parser hooks -----------------------------------------------------------

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self.pre += 100
            return
        if tag == "br":
            self.buf.append("\n")
            return
        if tag == "img":
            self.buf.append(f"![{a.get('alt', '')}]({a.get('src', '')})")
            return
        if tag == "a":
            if "card" in a.get("class", ""):
                # A card wraps a heading and a paragraph in one link. Flattened into a
                # list item, it reads as a link; left alone, the twin grows a link whose
                # text spans four blocks and renders as noise.
                self.flush_para()
                self.card += 1
            self.link += 1
            self.href.append(md_href(a.get("href", "")))
            self.buf.append("[")
            return
        if tag in ("strong", "b"):
            self.buf.append("**")
            return
        if tag in ("em", "i"):
            self.buf.append("*")
            return
        if tag == "code" and not self.pre:
            self.buf.append("`")
            return
        if tag in ("span", "small", "abbr", "code"):
            return
        if tag not in self.BLOCK:
            self.unknown.add(tag)
            return
        if self.link and tag not in ("table", "tr", "th", "td", "pre"):
            tail = "".join(self.buf).rstrip()
            if tail and not tail.endswith(("[", "—")):
                self.buf.append(" — ")
            return

        # block-level
        if tag in ("div", "section", "main", "figure", "header", "nav", "footer", "aside"):
            self.flush_para()
            return
        if tag == "pre":
            self.flush_para()
            self.pre += 1
            return
        if tag == "blockquote":
            self.flush_para()
            self.quote += 1
            return
        if tag in ("ul", "ol"):
            self.flush_para()
            self.lists.append([tag, 0])
            return
        if tag == "li":
            self.flush_para()
            return
        if tag == "table":
            self.flush_para()
            self.table, self.row = [], None
            return
        if tag == "tr":
            self.row = []
            return
        if tag in ("th", "td"):
            self.buf = []
            self.header_row = self.header_row or tag == "th"
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "dl", "dt", "dd",
                   "figcaption"):
            self.flush_para()
            return
        if tag == "hr":
            self.flush_para()
            self.emit("---")

    def handle_endtag(self, tag):
        if self.link and tag in self.BLOCK and tag not in ("table", "tr", "th", "td", "pre"):
            return
        if tag in ("script", "style"):
            self.pre -= 100
            self.buf = []
            return
        if tag == "a":
            href = self.href.pop() if self.href else ""
            self.buf.append(f"]({href})")
            self.link = max(0, self.link - 1)
            if self.card:
                self.card -= 1
                t = self.text().replace("\n", " ")
                t = re.sub(r"\[\s+", "[", t)
                t = re.sub(r"\s+\]", "]", t)
                t = re.sub(r"(\s*—\s*)+", " — ", t)
                t = re.sub(r"\s*—\s*\]", "]", t)
                self.emit("- " + re.sub(r"\s{2,}", " ", t).strip())
            return
        if tag in ("strong", "b"):
            self.buf.append("**")
            return
        if tag in ("em", "i"):
            self.buf.append("*")
            return
        if tag == "code" and not self.pre:
            self.buf.append("`")
            return
        if tag == "pre":
            body = "".join(self.buf).strip("\n")
            self.buf = []
            self.pre -= 1
            self.emit("```\n" + body + "\n```")
            return
        if tag == "blockquote":
            self.flush_para()
            self.quote -= 1
            return
        if tag in ("ul", "ol"):
            self.flush_para()
            if self.lists:
                self.lists.pop()
            return
        if tag == "li":
            t = self.text()
            if t:
                kind, n = self.lists[-1] if self.lists else ["ul", 0]
                if self.lists:
                    self.lists[-1][1] = n = n + 1
                marker = f"{n}." if kind == "ol" else "-"
                indent = "  " * max(0, len(self.lists) - 1)
                t = t.replace("\n", "\n" + indent + " " * (len(marker) + 1))
                self.emit(f"{indent}{marker} {t}")
            return
        if tag in ("th", "td"):
            if self.row is not None:
                self.row.append(self.text().replace("\n", " ").replace("|", "\\|"))
            return
        if tag == "tr":
            if self.table is not None and self.row:
                self.table.append(self.row)
            self.row = None
            return
        if tag == "table":
            rows = self.table or []
            self.table = None
            if rows:
                head = rows[0] if self.header_row else [""] * len(rows[0])
                body = rows[1:] if self.header_row else rows
                out = ["| " + " | ".join(head) + " |",
                       "|" + "|".join("---" for _ in head) + "|"]
                out += ["| " + " | ".join(r + [""] * (len(head) - len(r))) + " |" for r in body]
                self.emit("\n".join(out))
            self.header_row = False
            return
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.buf = ["".join(self.buf).replace("\n", " ")]
            self.flush_para("#" * int(tag[1]) + " ")
            return
        if tag == "dt":
            t = self.text()
            if t:
                self.emit(f"**{t}**")
            return
        if tag == "dd":
            self.flush_para(": ")
            return
        if tag in ("p", "figcaption", "div", "section", "main", "dl", "figure"):
            self.flush_para()

    def handle_data(self, data):
        if self.pre >= 100:
            return
        if self.pre:
            self.buf.append(data)
        else:
            self.buf.append(re.sub(r"\s+", " ", data))

    def close(self):  # type: ignore[override]
        super().close()
        self.flush_para()
        return self


def html_to_markdown(fragment: str) -> str:
    p = ToMarkdown()
    p.feed(fragment)
    p.close()
    if p.unknown:
        raise SystemExit(
            "build: markdown twin would drop unknown tag(s): "
            + ", ".join(sorted(p.unknown))
            + " — teach ToMarkdown about them rather than shipping a twin that has"
              " less in it than the page."
        )
    return "\n\n".join(p.blocks)


# ----------------------------------------------------------------------------- shell


def render_page(page: dict, body: str) -> str:
    path, title, desc = page["path"], page["title"], page["desc"]
    base = rel_prefix(path)
    url = f"{SITE_ORIGIN}/{path}"
    full_title = title if path == "index.html" else f"{title} · {SITE_NAME}"
    nav = "".join(
        f'<a href="{base}{href}">{html.escape(label)}</a>' for href, label in NAV
    )
    status = REVIEWED.get(path, REVIEW_DEFAULT)
    badge = (
        f'<p class="prov"><span class="tag unverified">{html.escape(status)}</span> '
        f'<a href="{base}provenance/index.html">what this means</a></p>'
    )
    crumb = ""
    if path != "index.html":
        crumb = (
            f'<p class="crumb"><a href="{base}index.html">{SITE_NAME}</a> '
            f'/ {html.escape(page["section"])}</p>'
        )
    cols = ""
    for heading, links in FOOTER_COLS:
        items = "".join(
            f'<li><a href="{base}{href}">{html.escape(label)}</a></li>'
            for href, label in links
        )
        cols += f"<div><h4>{html.escape(heading)}</h4><ul>{items}</ul></div>"

    ld = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "TechArticle",
            "headline": title,
            "description": desc,
            "url": url,
            "isPartOf": {"@type": "WebSite", "name": SITE_NAME, "url": SITE_ORIGIN + "/"},
            "inLanguage": "en",
            "version": SITE_VERSION,
            "license": "https://creativecommons.org/licenses/by/4.0/",
            "author": {"@type": "Person", "name": "Dinis Cruz"},
        },
        separators=(",", ":"),
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="generator" content="admin/build/build_pages.py {SITE_VERSION}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{FAVICON}">
<meta property="og:type" content="article">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{html.escape(full_title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
<script type="application/ld+json">{ld}</script>
<style>{CRITICAL_CSS}</style>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head"><div class="bar">
<a class="brand" href="{base}index.html"><b>myfeeds</b><span class="tld">.sgit.ai</span></a>
<a class="ver" href="{base}admin/versions.html#{version_anchor(SITE_VERSION)}"
title="What changed in {SITE_VERSION}">{SITE_VERSION}</a>
<nav class="site-nav" aria-label="Sections">{nav}</nav>
</div></header>
<main id="main">
{crumb}
{badge}
{body.strip()}
</main>
<footer class="site-foot"><div class="inner">
{cols}
<div><h4>Written by</h4>
<p>This entire site — its prose, its ontologies and the classifications they produce —
is <strong>generated by an AI system</strong> and reviewed by a human after the fact,
not before. <a href="{base}provenance/index.html">What that means, exactly</a>.</p></div>
<div><h4>This page</h4>
<p><a href="{path.rsplit("/", 1)[-1][:-5]}.md">This page as markdown</a> — the bytes it was rendered
from. Anything rendered here stays one click from its source.</p>
<p>{html.escape(SITE_THESIS)}</p>
<p><small>{html.escape(LICENCE)}<br>Site {SITE_VERSION}. Part of the
<a href="https://sgit.ai/network/index.html">sgit.ai network</a>.</small></p></div>
</div></footer>
<script>{BOOTSTRAP % {"base": json.dumps(base)}}</script>
</body>
</html>
"""


def render_markdown(page: dict, body: str) -> str:
    path, title, desc = page["path"], page["title"], page["desc"]
    url = f"{SITE_ORIGIN}/{path}"
    md = html_to_markdown(body)
    md = re.sub(r"^# .*\n\n", "", md, count=1)  # the H1 is the twin's own title
    return f"""# {title}

> {desc}

*Source: <{url}> · site {SITE_VERSION} · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

{md}

---

*[Site index for agents]({rel_prefix(path)}llms.txt) · [HTML version]({url})*
"""


# ------------------------------------------------------------------- generated bodies


def load_roles() -> list[dict]:
    roles = []
    for f in sorted(ROLES_DIR.glob("*/ROLE.md")):
        meta, body = parse_frontmatter(f.read_text(encoding="utf-8"))
        for required in ("name", "slug", "mission", "claim", "not_responsible_for"):
            if not meta.get(required):
                raise SystemExit(f"build: {f} is missing '{required}'")
        if meta["slug"] != f.parent.name:
            raise SystemExit(f"build: {f} slug '{meta['slug']}' != folder '{f.parent.name}'")
        meta["body"] = body
        meta["order"] = int(meta.get("order", 99))
        meta["file"] = str(f.relative_to(ROOT))
        roles.append(meta)
    roles.sort(key=lambda r: r["order"])
    if not roles:
        raise SystemExit("build: no ROLE.md files found under team/roles/")
    return roles


def load_board() -> list[dict]:
    cards = []
    for f in sorted(BOARD_DIR.glob("*.md")):
        if f.name == "README.md":
            continue
        meta, body = parse_frontmatter(f.read_text(encoding="utf-8"))
        meta["body"] = body
        meta["file"] = str(f.relative_to(ROOT))
        cards.append(meta)
    return cards


def md_inline(text: str) -> str:
    """The small inline markdown used inside ROLE.md bodies and board cards."""
    out = html.escape(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    return out


def md_block(text: str, base: str = "") -> str:
    """A minimal markdown renderer for the role and card bodies. It handles exactly what
    those files use — headings, paragraphs, lists, tables, blockquotes, fenced code — and
    raises on a fence it cannot close, rather than swallowing the rest of the file."""
    lines = text.split("\n")
    out: list[str] = []
    i, n = 0, len(lines)
    para: list[str] = []
    bullets: list[str] = []

    def close() -> None:
        nonlocal para, bullets
        if para:
            out.append("<p>" + md_inline(" ".join(para)) + "</p>")
            para = []
        if bullets:
            out.append("<ul>" + "".join(f"<li>{md_inline(b)}</li>" for b in bullets) + "</ul>")
            bullets = []

    while i < n:
        line = lines[i]
        s = line.strip()
        if s.startswith("```"):
            close()
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            if i >= n:
                raise SystemExit("build: unclosed code fence in a markdown body")
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            i += 1
            continue
        if s.startswith("|") and i + 1 < n and set(lines[i + 1].strip()) <= set("|-: "):
            close()
            head = [c.strip() for c in s.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thead = "".join(f"<th>{md_inline(c)}</th>" for c in head)
            tbody = "".join(
                "<tr>" + "".join(f"<td>{md_inline(c)}</td>" for c in r) + "</tr>"
                for r in rows
            )
            out.append(
                f'<div class="tablewrap"><table><thead><tr>{thead}</tr></thead>'
                f"<tbody>{tbody}</tbody></table></div>"
            )
            continue
        if not s:
            close()
        elif s.startswith("#"):
            close()
            lvl = len(s) - len(s.lstrip("#"))
            txt = s[lvl:].strip()
            out.append(f"<h{lvl + 1} id=\"{slugify(txt)}\">{md_inline(txt)}</h{lvl + 1}>")
        elif s.startswith("> "):
            close()
            quote = []
            while i < n and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>" + md_inline(" ".join(quote)) + "</p></blockquote>")
            continue
        elif s.startswith("- "):
            if para:
                close()
            bullets.append(s[2:])
        elif s == "---":
            close()
            out.append("<hr>")
        else:
            if bullets:
                close()
            para.append(s)
        i += 1
    close()
    return "\n".join(out)


def role_page_body(role: dict, roles: list[dict]) -> str:
    others = [r for r in roles if r["slug"] != role["slug"]]
    nav = " · ".join(f'<a href="{r["slug"]}.html">{html.escape(r["name"])}</a>' for r in others)
    owns = "".join(f"<li>{md_inline(x)}</li>" for x in role.get("owns", []))
    tools = "".join(f"<li><code>{html.escape(x)}</code></li>" for x in role.get("tools", []))
    form = role.get("claim_form", "descriptive")
    return f"""
<p class="kicker">{html.escape(role.get("group", "Role"))}</p>
<h1>{html.escape(role["name"])}</h1>
<p class="lede">{md_inline(role["mission"])}</p>

<dl class="fields">
<dt>Central claim</dt><dd><strong>{md_inline(role["claim"])}</strong>
<span class="tag">{html.escape(form)}</span></dd>
<dt>Not responsible for</dt><dd>{md_inline(role["not_responsible_for"])}</dd>
<dt>Owns</dt><dd><ul>{owns}</ul></dd>
<dt>Tools</dt><dd><ul>{tools}</ul></dd>
<dt>Source</dt><dd><code>{html.escape(role["file"])}</code> — this page is generated from
that file, so a role cannot say one thing to an agent and another to a reader.</dd>
</dl>

{md_block(role["body"])}

<div class="next"><a href="../index.html">← All roles</a>
<a href="../board.html">The board →</a></div>
<p><small>Other roles: {nav}</small></p>
"""


def team_index_body(roles: list[dict], cards: list[dict]) -> str:
    cardsel = ""
    for r in roles:
        cardsel += (
            f'<a class="card" href="roles/{r["slug"]}.html">'
            f'<p class="k">{r["order"]:02d} · {html.escape(r.get("group", ""))}</p>'
            f'<h3>{html.escape(r["name"])}</h3>'
            f'<p>{md_inline(r["mission"])}</p></a>'
        )
    rows = "".join(
        f'<tr><td><a href="roles/{r["slug"]}.html">{html.escape(r["name"])}</a></td>'
        f'<td>{md_inline(r["claim"])}</td>'
        f'<td><span class="tag">{html.escape(r.get("claim_form", ""))}</span></td></tr>'
        for r in roles
    )
    falsifiable = sum(1 for r in roles if r.get("claim_form") == "falsifiable")
    open_cards = sum(1 for c in cards if c.get("status") in ("need", "todo", "doing"))
    return f"""
<p class="kicker">The agentic section</p>
<h1>How this site is run</h1>
<p class="lede">myfeeds.sgit.ai is built by one person and a small team of AI agents.
This page is written for the agents. {len(roles)} roles, each a file in this repository;
the rule each enforces; and the board where the work is. A new agent should be able to
read this page and one role file and begin.</p>

<div class="band">
<p><strong>The team is dev-shaped on purpose.</strong> The wider estate staffs
nine or more roles for a site that publishes credentials and needs a Publisher and an
Auditor. This site publishes contracts and code, so it staffs the portable core that
<a href="https://teams.sgit.ai/roster/index.html">teams.sgit.ai</a> found three
independent teams reaching for — Architect, Dev, DevOps, QA, Librarian, Historian —
under a Conductor that does no work.</p>
<p>What is <em>not</em> staffed, said plainly: there is no Designer, no AppSec and no
Journalist here. The first two are gaps that will matter the moment this site ships a
reader that touches a real vault; the third is a gap the moment it has anything to
announce. They are on <a href="board.html">the board</a> as needs, not quietly absent.</p>
</div>

<h2 id="roles">The {len(roles)} roles</h2>
<p>Each role is <code>team/roles/&lt;slug&gt;/ROLE.md</code>. The cards below and every
role page are generated from those files at build time, and the same data is served at
<a href="../data/team.json"><code>data/team.json</code></a> for agents that would rather
not parse a page.</p>
<div class="grid">{cardsel}</div>

<h2 id="claims">Every role states a failure condition</h2>
<p>A role's Central Claim is the testable assertion it is judged on. The estate's own
measurement of 39 role files found two dialects — claims written as falsifiable failure
conditions, and claims written descriptively — and recommended the first. Every role here
is written in that form: {falsifiable} of {len(roles)}.</p>
<div class="tablewrap"><table>
<thead><tr><th>Role</th><th>Fails when</th><th>Form</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2 id="rules">The rules every role shares</h2>
<ul>
<li><strong>Contracts before implementations.</strong> This site publishes the shape of a
thing before the thing exists, so that the commitment is checkable against what is
eventually built — by anyone, including someone who would like it to have failed.</li>
<li><strong>Say what it is worth.</strong> Every claim carries a status:
<span class="tag shipped">shipped</span> you can run it from this repository,
<span class="tag argued">argued</span> a position with its reasoning shown,
<span class="tag unverified">unverified</span> believed but not yet checked against a
primary source. The third is used honestly and often.</li>
<li><strong>Count, do not remember.</strong> Every number on this page is generated from
the files it counts. If a number cannot be generated, it is not printed.</li>
<li><strong>Negative controls.</strong> A check that would also pass on wrong input has
proven nothing. New validator assertions ship having been seen red.</li>
<li><strong>Corrections go above the mistake.</strong> The wrong claim stays, because
deleting it destroys the only evidence that the process works.</li>
<li><strong>Output is never hand-edited.</strong> The published tree is generated; the
sources are <code>admin/content/</code> and <code>team/</code>.</li>
</ul>

<h2 id="board">The board</h2>
<p>{open_cards} open {"card" if open_cards == 1 else "cards"}. Every card is a markdown
file with a status line; the columns are those lines rendered. Nothing runs and nothing is
hosted — the board versions with the repository it tracks, which is the same convention
<a href="https://issues-fs.sgit.ai/">issues-fs.sgit.ai</a> argues for at length.</p>

<div class="next"><a href="board.html">The board →</a>
<a href="prompts.html">Starting prompts →</a>
<a href="../admin/index.html">How the site is built →</a></div>
"""


BOARD_COLUMNS = [
    ("need", "Needs", "Only the human owner can supply these."),
    ("todo", "Tasks", "An agent can pick these up from its starting prompt."),
    ("doing", "In progress", "Claimed, with a role behind it."),
    ("held", "Held", "Deliberately not shipping, with the reason on the card."),
    ("done", "Done", "Closed, with the release that carried it."),
]


def board_body(cards: list[dict], roles: list[dict]) -> str:
    known = {r["slug"] for r in roles}
    for c in cards:
        if c.get("owner") not in known:
            raise SystemExit(
                f"build: board card {c.get('file')} names owner "
                f"'{c.get('owner')}', which is not a role in team/roles/"
            )
    out = [
        '<p class="kicker">Open work</p>',
        "<h1>The board</h1>",
        '<p class="lede">Every card is a markdown file in <code>team/board/</code> with a '
        "status line and exactly one owning role. The columns below are those lines "
        "rendered at build time. A card with two owners is two cards; a card with no "
        "owner does not enter the board.</p>",
    ]
    for status, heading, blurb in BOARD_COLUMNS:
        col = [c for c in cards if c.get("status") == status]
        if not col:
            continue
        out.append(f'<h2 id="{status}">{heading} <span class="tag {status}">'
                   f"{len(col)}</span></h2>")
        out.append(f"<p>{html.escape(blurb)}</p>")
        for c in col:
            out.append(
                f'<div class="band"><p class="k"><code>{html.escape(c["file"])}</code></p>'
                f'<h3>{html.escape(str(c.get("id", "")))} · {md_inline(c["title"])}</h3>'
                f'<p><span class="tag {status}">{status}</span> '
                + (f'<span class="tag">{html.escape(c.get("kind", "task"))}</span> '
                   if c.get("kind", "task") != status else "")
                + f'owner <a href="roles/{c["owner"]}.html">{html.escape(c["owner"])}</a> '
                + f'· opened {html.escape(str(c.get("opened", "")))}</p>'
                + f'{md_block(c["body"])}</div>'
            )
    out.append('<div class="next"><a href="index.html">← The team</a>'
               '<a href="prompts.html">Starting prompts →</a></div>')
    return "\n".join(out)


def prompts_body() -> str:
    src = (ROOT / "team" / "prompts" / "README.md").read_text(encoding="utf-8")
    _, _, rest = src.partition("\n")
    return (
        '<p class="kicker">The regular work</p>\n'
        "<h1>Starting prompts</h1>\n"
        '<p class="lede">One prompt per recurring task, each naming the role file that '
        "turns a general model into the role that owns the work. Paste one into a fresh "
        "agent with nothing else. Generated from "
        "<code>team/prompts/README.md</code>.</p>\n"
        + md_block(rest.strip())
        + '\n<div class="next"><a href="index.html">← The team</a>'
          '<a href="board.html">The board →</a></div>'
    )


def version_anchor(version: str) -> str:
    return version.replace(".", "-")


def versions_body() -> str:
    blocks = []
    for e in reversed(VERSION_LOG):
        anchor = version_anchor(e["version"])
        changes = "".join(f"<li>{md_inline(c)}</li>" for c in e.get("changes", []))
        corrects = (
            f'<div class="note"><p><strong>Corrects.</strong> '
            f'{md_inline(e["corrects"])}</p></div>'
            if e.get("corrects") else ""
        )
        blocks.append(
            f'<div class="band" id="{anchor}">'
            f'<p class="k"><code>{e["version"]}</code> · {e["date"]} · '
            f'<a href="../versions/{e["version"]}.json">as data</a></p>'
            f'<h3>{md_inline(e["title"])}</h3>'
            f'<p>{md_inline(e["summary"])}</p>'
            f"{corrects}"
            f"<h4>Changes</h4><ul>{changes}</ul></div>"
        )
    return f"""
<p class="kicker">Provenance</p>
<h1>Release history</h1>
<p class="lede">Every release of this site: the version, the date, what it did, and what
an earlier version got wrong where one did. A version log that reads as an unbroken
sequence of improvements is a version log that is lying.</p>

<p>Each entry is also served as data at <code>/versions/&lt;version&gt;.json</code>, indexed
by <a href="../versions/index.json"><code>/versions/index.json</code></a>, so a script can
check a claim about a release without rendering a page. The version badge in the navigation
links to the entry for the version you are looking at, not to this page generally.</p>

{"".join(blocks)}

<p>The log lives in <code>VERSION_LOG</code> in <code>admin/build/build_pages.py</code> and
is owned by the <a href="../team/roles/historian.html">Historian</a>; the version number
itself is owned by <code>admin/build/version.txt</code>, because that is the file the
deploy workflow shared across the <a href="../network/index.html">*.sgit.ai sites</a>
reads. The version in the navigation, the entry here, and the version the live site serves
have to agree — <a href="../team/roles/devops.html">DevOps</a> exists because on two
occasions elsewhere in this estate the first two agreed and the third did not.</p>
<div class="next"><a href="index.html">← How this site is built</a></div>
"""


def backoffice_index_body(arc: dict) -> str:
    site = arc["sites"][0] if arc["sites"] else None
    posts = site["posts"] if site else []
    words = sum(p["words"] for p in posts)
    gaps = len(site["gaps"]) if site else 0
    res = len(site["resources"]) if site else 0
    return f"""
<p class="kicker">Back office</p>
<h1>Everything this site is built from</h1>
<p class="lede">The working material behind myfeeds.sgit.ai: writing recovered from a
site that no longer exists, the documents that live in other repositories, the tools that
did the recovering, and every release this site has cut. Indexed from what is actually on
disk, because a back office maintained by hand becomes a lie on a schedule.</p>

<div class="grid">
<a class="card" href="archive/index.html"><p class="k">Recovered</p>
<h3>The mvp.myfeeds.ai archive</h3>
<p>{len(posts)} posts, {words:,} words, pulled back out of the Internet Archive.
{gaps} things the sitemap named that no crawler ever caught.</p></a>
<a class="card" href="documents/index.html"><p class="k">Indexed, not copied</p>
<h3>Documents</h3>
<p>{len(backoffice.DOCUMENTS)} documents across {len(backoffice.REPOS)} repositories:
the business plan, the pitch decks and their briefs, the engine's architecture notes.</p></a>
<a class="card" href="tools/index.html"><p class="k">Runnable</p>
<h3>Tools</h3>
<p>{len(backoffice.TOOLS)} scripts, no dependencies between them and nothing to install:
the archiver, the generator, the gate, the live check.</p></a>
<a class="card" href="../admin/versions.html"><p class="k">Provenance</p>
<h3>Previous versions</h3>
<p>Every release of this site, as prose and as data at
<code>/versions/index.json</code>.</p></a>
</div>

<h2 id="rules">Two rules this section follows</h2>
<p><strong>A document has one owner.</strong> Where something lives in another
repository it is indexed and linked, never copied — a second copy is a disagreement
waiting to happen. Where something exists <em>only</em> in the Internet Archive, this
repository is now its home, and every item says which of the two it is.</p>
<p><strong>State the gaps.</strong> The archive page lists what could not be recovered as
prominently as what could. A recovery that does not say what it lost is not a recovery,
and the list is the honest measure of how much of the original is gone for good.</p>

<h2 id="counts">What is here</h2>
<div class="tablewrap"><table>
<thead><tr><th>Holding</th><th>Count</th><th>Where it lives</th></tr></thead>
<tbody>
<tr><td>Recovered posts, as markdown with front matter</td><td>{len(posts)}</td>
<td><code>back-office/archive/mvp.myfeeds.ai__posts/</code></td></tr>
<tr><td>Recovered original files, unmodified bytes</td><td>{res}</td>
<td><code>back-office/archive/mvp.myfeeds.ai/</code></td></tr>
<tr><td>Recorded gaps — listed in the sitemap, never captured</td><td>{gaps}</td>
<td><a href="archive/index.html#gaps">the archive page</a></td></tr>
<tr><td>Documents indexed in other repositories</td><td>{len(backoffice.DOCUMENTS)}</td>
<td><a href="documents/index.html">documents</a></td></tr>
<tr><td>Tools</td><td>{len(backoffice.TOOLS)}</td><td><code>admin/tools/</code>,
<code>admin/build/</code></td></tr>
</tbody></table></div>

<div class="next"><a href="archive/index.html">The recovered archive →</a>
<a href="documents/index.html">Documents →</a><a href="tools/index.html">Tools →</a></div>
"""


def archive_index_body(arc: dict) -> str:
    site = arc["sites"][0]
    posts = site["posts"]
    by_tag: dict[str, list] = {}
    for p in posts:
        for t in (p.get("tags") or ["(untagged)"]):
            by_tag.setdefault(t, []).append(p)
    rows = ""
    for t, ps in sorted(by_tag.items(), key=lambda kv: -len(kv[1])):
        rows += (f'<tr><td><strong>{html.escape(t)}</strong></td><td>{len(ps)}</td>'
                 f'<td>{sum(x["words"] for x in ps):,}</td></tr>')
    listing = ""
    for p in posts:
        tags = " ".join(f'<span class="tag">{html.escape(t)}</span>'
                        for t in (p.get("tags") or []))
        listing += (
            f'<a class="card" href="{p["slug"]}.html">'
            f'<p class="k">{html.escape(p.get("published_human", "undated"))} · '
            f'{p["words"]:,} words</p>'
            f'<h3>{html.escape(p["title"])}</h3><p>{tags}</p></a>'
        )
    gaps = "".join(f'<li><code>{html.escape(g["url"])}</code></li>' for g in site["gaps"])
    return f"""
<p class="kicker">Recovered</p>
<h1>The mvp.myfeeds.ai archive</h1>
<p class="lede">mvp.myfeeds.ai was the first MyFeeds MVP: a Ghost blog publishing
machine-generated cybersecurity briefings, one per persona, alongside the long-form posts
explaining how they were built. The site is gone. {len(posts)} of its posts —
{sum(p["words"] for p in posts):,} words — are here, recovered from the Internet Archive
and now kept as files rather than as somebody else's cache.</p>

<div class="note">
<p><strong>Most of this survived in the feed, not the pages.</strong> The crawler
captured {len(site["resources"])} files, of which only eight were post pages. What saved
the long-form writing was a single capture of <code>/rss/</code> on
31 August 2025: a Ghost feed carries the full body of its recent posts in
<code>content:encoded</code>, so one 224&nbsp;KB XML file held articles whose own pages
were never archived. If that one request had failed, this page would be mostly a list of
what used to exist.</p>
</div>

<h2 id="posts">The posts</h2>
<p>Two kinds, and the difference matters. The <strong>How it works</strong> posts are
Dinis Cruz explaining the architecture — they are the argument. The persona posts are
<em>output</em>: briefings the pipeline generated for a CEO, a CISO, a CTO and two kinds
of board member, which makes them evidence that the thing ran.</p>
<div class="tablewrap"><table>
<thead><tr><th>Tag</th><th>Posts</th><th>Words</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<div class="grid">{listing}</div>

<h2 id="gaps">What could not be recovered</h2>
<p>{len(site["gaps"])} URLs appear in the site's own sitemap and in no capture anywhere.
They are not missing from this page because nobody looked; they are gone.</p>
<ul>{gaps}</ul>
<p>Two of them are author pages and five are tag listings, which are indexes rather than
writing — their contents are largely reconstructable from the posts that survived.
<code>/about/</code> and <code>/ceo-news/</code> are not: whatever they said is lost
unless a copy exists somewhere outside the archive.</p>

<h2 id="how">How it was recovered</h2>
<p>With <a href="../tools/index.html"><code>admin/tools/wayback_archive.py</code></a>, in
this repository, which you can run against any domain. The three things that cost
content, each of which loses it silently rather than erroring, are written up in that
tool's own documentation — the worst is that the Internet Archive's
<code>collapse=urlkey</code> option merges <code>http://host/x</code> with
<code>https://host/x/</code> and keeps whichever sorts first, which on this domain was a
redirect. A collapsed query reports <code>/tag/how-it-works/</code> as not existing. It
exists, it was captured, and it is <a href="../../back-office/archive/index.html">here</a>.</p>

<p>The manifest — every file, the capture it came from, and its Wayback URL — is at
<code>{html.escape(site["manifest_file"])}</code>.</p>

<div class="next"><a href="../index.html">← Back office</a>
<a href="../tools/index.html">The tools →</a></div>
"""


def archive_post_body(post: dict, site: dict) -> str:
    tags = " ".join(f'<span class="tag">{html.escape(t)}</span>'
                    for t in (post.get("tags") or []))
    return f"""
<p class="kicker">Recovered from the archive</p>
<h1>{html.escape(post["title"])}</h1>
<dl class="fields">
<dt>Originally</dt><dd><code>{html.escape(post.get("url", ""))}</code> —
the site no longer exists</dd>
<dt>Published</dt><dd>{html.escape(post.get("published_human", "undated"))}</dd>
<dt>Author</dt><dd>{html.escape(post.get("author") or "not recorded")}</dd>
<dt>Tags</dt><dd>{tags or "none"}</dd>
<dt>Recovered</dt><dd>From a capture of the site's RSS feed, which carried the full body.
The markdown is at <code>{html.escape(post["file"])}</code>.</dd>
</dl>

<div class="note"><p>This is recovered content, reproduced as it was published. Links in
it point at pages that in many cases no longer resolve, and images are still served from
the dead domain — both are left exactly as written rather than silently repaired, because
a rewritten archive is no longer evidence of what was said.</p></div>

{md_block(post["body"])}

<div class="next"><a href="index.html">← All recovered posts</a>
<a href="../index.html">Back office →</a></div>
"""


def documents_body() -> str:
    rows = ""
    for d in backoffice.DOCUMENTS:
        repo = backoffice.REPOS[d["where"]]
        href = f'{repo["url"]}/blob/main/{urllib.parse.quote(d["path"])}'
        rows += (
            f'<tr><td><a href="{href}">{html.escape(d["title"])}</a></td>'
            f'<td><span class="tag">{html.escape(d["kind"])}</span></td>'
            f'<td>{html.escape(d["date"])}</td>'
            f'<td><code>{html.escape(d["where"])}</code></td>'
            f'<td>{html.escape(d["note"])}</td></tr>'
        )
    repos = ""
    for name, r in backoffice.REPOS.items():
        repos += (f'<tr><td><a href="{r["url"]}">{html.escape(name)}</a></td>'
                  f'<td>{html.escape(r["what"])}</td></tr>')
    return f"""
<p class="kicker">Indexed, not copied</p>
<h1>Documents</h1>
<p class="lede">The business plan, the pitch decks, the briefs that produced them, and the
engine's own architecture notes. All of these live in other repositories and are indexed
from here rather than duplicated — a document has one owner, and a second copy is a
disagreement waiting to happen.</p>

<div class="tablewrap"><table>
<thead><tr><th>Document</th><th>Kind</th><th>Date</th><th>Repository</th><th>Note</th></tr></thead>
<tbody>{rows}</tbody></table></div>

<h2 id="repos">Where they live</h2>
<div class="tablewrap"><table>
<thead><tr><th>Repository</th><th>What it is</th></tr></thead>
<tbody>{repos}</tbody></table></div>
<p>Both are public and open source. <code>investor.myfeeds.ai</code> is published from
the first; the second is the pipeline that generated every persona briefing in
<a href="../archive/index.html">the recovered archive</a>.</p>

<div class="note"><p><strong>The exception to indexing rather than copying</strong> is
anything that exists only in the Internet Archive. That has no owner left to defer to, so
this repository holds it — see <a href="../archive/index.html">the archive</a>, where
every item records the capture it came from.</p></div>

<div class="next"><a href="../index.html">← Back office</a>
<a href="../archive/index.html">The archive →</a></div>
"""


def tools_body() -> str:
    blocks = ""
    for t in backoffice.TOOLS:
        blocks += (
            f'<div class="band"><p class="k"><code>{html.escape(t["file"])}</code></p>'
            f'<h3>{html.escape(t["title"])}</h3>'
            f'<p>{html.escape(t["what"])}</p>'
            f'<pre><code>{html.escape(t["run"])}</code></pre></div>'
        )
    return f"""
<p class="kicker">Runnable</p>
<h1>Tools</h1>
<p class="lede">Everything needed to build, check, publish and recover, in this
repository, with nothing to install beyond Python 3.11 and Node 22. Each one is a single
file and each one is documented in its own header rather than here, so the documentation
cannot drift from the thing it documents.</p>

{blocks}

<h2 id="archiver">Why the archiver has a long header</h2>
<p>Because three separate things lose content while appearing to work, and each cost a
run before it was understood: the Internet Archive's <code>collapse=urlkey</code> hides
good captures behind redirects; fetching without the <code>id_</code> modifier archives
the Wayback Machine's rewritten copy rather than the site; and a blog's feed frequently
holds writing whose own pages were never captured, so it is a primary source and not a
fallback. Those are written into the tool where somebody modifying it will read them.</p>

<div class="next"><a href="../index.html">← Back office</a>
<a href="../../admin/index.html">How this site is built →</a></div>
"""


AXIS_BAR = (
    '<div style="background:var(--panel2);border:1px solid var(--line);border-radius:999px;'
    'height:8px;position:relative;margin:.3rem 0 .1rem">'
    '<div style="position:absolute;left:calc({pct}% - 6px);top:-3px;width:12px;height:12px;'
    'border-radius:50%;background:var(--accent)"></div></div>'
)


def _pct(audience: dict, axis: str) -> str:
    """An axis value as a percentage, or an em dash for the control audience, which sits
    on no axis on purpose."""
    v = audience["axes"].get(axis)
    return "—" if v is None else f"{v:.0%}"


def audiences_body(fd: dict) -> str:
    au = fd["audiences"]
    cur = {c["id"]: c for c in au["currencies"]}
    axes = {a["id"]: a for a in au["axes"]}

    rows = ""
    for a in sorted(au["audiences"], key=lambda x: x["order"]):
        ax = ""
        for aid, axis in axes.items():
            v = a["axes"].get(aid)
            ax += (f'<div><small>{html.escape(axis["label"])}</small>'
                   + (AXIS_BAR.format(pct=int(v * 100)) if v is not None
                      else '<div style="height:8px;margin:.3rem 0 .1rem;color:var(--dim2)">'
                           '<small>n/a</small></div>')
                   + f'<small style="color:var(--dim2)">{html.escape(axis["low"])} → '
                     f'{html.escape(axis["high"])}</small></div>')
        rows += (
            f'<div class="band" id="{a["id"]}">'
            f'<p class="k">{a["order"]:02d} · pays in <strong>'
            f'{html.escape(cur[a["currency"]]["label"])}</strong>'
            + (' · <span class="tag">control</span>' if a.get("control") else "")
            + f'</p><h3>{html.escape(a["name"])} '
              f'<span class="tag">{html.escape(a["short"])}</span></h3>'
            f'<p>{html.escape(a["role"])}</p>'
            f'<div class="grid" style="gap:.8rem;margin:1rem 0">{ax}</div>'
            f'<h4>Wants</h4><ul>'
            + "".join(f"<li>{html.escape(w)}</li>" for w in a["wants"]) + "</ul>"
            f'<h4>Does not want</h4><ul>'
            + "".join(f"<li>{html.escape(w)}</li>" for w in a["does_not_want"]) + "</ul>"
            + (f'<h4>Watches for</h4><div class="tablewrap"><table><thead><tr>'
               f'<th>Concern</th><th>Satisfied by</th><th>Only when</th></tr></thead><tbody>'
               + "".join(
                   f'<tr><td>{html.escape(c["label"])}</td>'
                   f'<td>{" ".join(f"<code>{html.escape(m)}</code>" for m in c["match"])}</td>'
                   f'<td>{" ".join(f"<code>{html.escape(m)}</code>" for m in c.get("requires", [])) or "—"}</td>'
                   f'</tr>' for c in a["concerns"])
               + "</tbody></table></div>" if a["concerns"] else "")
            + "</div>"
        )

    curr = "".join(
        f'<tr><td><strong>{html.escape(c["label"])}</strong></td>'
        f'<td>{html.escape(c["note"])}</td>'
        f'<td>{", ".join(html.escape(a["short"]) for a in au["audiences"] if a["currency"] == c["id"])}</td></tr>'
        for c in au["currencies"])

    return f"""
<p class="kicker">The audience side</p>
<h1>Six audiences, and what each converts news into</h1>
<p class="lede">The same article, read by six roles, should produce six different pieces —
not one piece at six lengths. What makes them different is not tone: it is what each role
converts a piece of news <em>into</em>. A founder turns it into something to do this month;
an allocator turns it into evidence about a population; a risk owner turns it into a change
in exposure. That is the axis the whole system turns on.</p>

<div class="note">
<p><strong>The first audience is not an audience.</strong> The source material is
Portuguese; the first output is a faithful English translation with nothing added, dropped
or re-weighted. It is the control: every article reaches it, no selection runs, and it is
what the other five are diffed against. Without it there is no way to tell re-framing apart
from distortion, because there is nothing to compare against.</p>
</div>

<h2 id="currencies">What each one pays in</h2>
<div class="tablewrap"><table>
<thead><tr><th>Currency</th><th>Means</th><th>Audience</th></tr></thead>
<tbody>{curr}</tbody></table></div>

<h2 id="spectrum">The spectrum</h2>
<p>Three axes separate them, and the first is the strongest: <strong>how much mechanism
the reader wants</strong>. A practitioner and an executive can want the same story and
disagree completely about where it should stop. The second — <strong>scope</strong> — is
why the founder and the allocator read like inversions of each other: one cares about a
named thing, the other about the population it belongs to.</p>

<div class="tablewrap"><table>
<thead><tr><th>Audience</th><th>Mechanism</th><th>Scope</th><th>Horizon</th><th>Pays in</th></tr></thead>
<tbody>""" + "".join(
        f'<tr><td><a href="#{a["id"]}">{html.escape(a["name"])}</a></td>'
        + "".join(f"<td>{_pct(a, k)}</td>" for k in ("depth", "breadth", "horizon"))
        + f'<td>{html.escape(cur[a["currency"]]["label"])}</td></tr>'
        for a in sorted(au["audiences"], key=lambda x: x["order"])) + f"""</tbody></table></div>
<p><small>Mechanism: 0% = the consequence only, 100% = the full mechanism. Scope: 0% = one
named thing, 100% = a whole population. Horizon: 0% = this week, 100% = several years.
The control audience sits on no axis, deliberately.</small></p>

<h2 id="roles">The six</h2>
{rows}

<div class="next"><a href="../ontology/index.html">The two ontologies →</a>
<a href="../explain/index.html">A worked example →</a>
<a href="../index.html">← Home</a></div>
"""


def ontology_body(fd: dict) -> str:
    o = fd["ontology"]

    def edge_table(edges):
        return ('<div class="tablewrap"><table><thead><tr><th>Verb</th><th>Inverse</th>'
                '<th>Reads</th><th>And back</th></tr></thead><tbody>'
                + "".join(
                    f'<tr><td><code>{html.escape(e["verb"])}</code></td>'
                    f'<td><code>{html.escape(e["inverse"])}</code></td>'
                    f'<td>{html.escape(e["reading"].replace("{s}", e["domain"]).replace("{t}", e["range"]))}</td>'
                    f'<td>{html.escape(e["reading_inverse"].replace("{s}", e["domain"]).replace("{t}", e["range"]))}</td></tr>'
                    for e in edges)
                + "</tbody></table></div>")

    types = "".join(
        f'<tr><td><code>{html.escape(t["id"])}</code></td><td>{html.escape(t["definition"])}</td></tr>'
        for t in o["article"]["types"])
    forbidden = "".join(
        f'<tr><td><code>{html.escape(f["verb"])}</code></td><td>{html.escape(f["why"])}</td></tr>'
        for f in o["article"]["forbidden"])
    rules = "".join(
        f'<div class="band"><h3>{html.escape(r["rule"])}</h3>'
        f'<p>{html.escape(r["why"])}</p></div>' for r in o["rules"])
    f = o["join"]["formula"]
    matches = "".join(
        f'<tr><td><code>{html.escape(m["id"])}</code></td><td>{m["weight"]}</td>'
        f'<td>{html.escape(m["when"])}</td></tr>' for m in f["matches"])
    atypes = "".join(
        f'<tr><td><code>{html.escape(t["id"])}</code></td><td>{html.escape(t["definition"])}</td></tr>'
        for t in o["audience"]["types"])

    return f"""
<p class="kicker">The grammar</p>
<h1>Two ontologies and the join between them</h1>
<p class="lede">One ontology says what a piece of news contains. Another says what a role
watches for. Neither is interesting on its own — the whole value is in the third thing,
the join, which is where an article meets an audience and a sentence comes out saying why.
The grammar is adapted from the one
<a href="https://pt.newsroom.sgit.ai/">pt.newsroom.sgit.ai</a> uses for the Portuguese
graph, and keeps its hardest rule.</p>

<h2 id="rules">The rules</h2>
{rules}

<h2 id="article">The article ontology</h2>
<p>{html.escape(o["article"]["note"])}</p>
<div class="tablewrap"><table><thead><tr><th>Type</th><th>Is</th></tr></thead>
<tbody>{types}</tbody></table></div>
<h3>Its verbs</h3>
{edge_table(o["article"]["edges"])}

<h3 id="forbidden">Verbs that are not allowed</h3>
<p>Naming what is banned, and why, is more useful than naming what is permitted: every one
of these is a shortcut somebody will reach for.</p>
<div class="tablewrap"><table><thead><tr><th>Verb</th><th>Why not</th></tr></thead>
<tbody>{forbidden}</tbody></table></div>

<h2 id="audience">The audience ontology</h2>
<p>{html.escape(o["audience"]["note"])}</p>
<div class="tablewrap"><table><thead><tr><th>Type</th><th>Is</th></tr></thead>
<tbody>{atypes}</tbody></table></div>
{edge_table([e for e in o["audience"]["edges"] if "{{s}}" not in e["range"]])}

<h2 id="join">The join</h2>
<p>{html.escape(o["join"]["note"])}</p>
<div class="band">
<h3>{html.escape(f["id"])}</h3>
<p>{html.escape(f["statement"])}</p>
</div>
<div class="tablewrap"><table>
<thead><tr><th>Match</th><th>Weight</th><th>When</th></tr></thead>
<tbody>{matches}</tbody></table></div>
<p><strong>Reached at:</strong> {f["threshold"]["reached_at"]} connection.
{html.escape(f["threshold"]["note"])}</p>
<p><strong>Withheld:</strong> {html.escape(f["withheld_reason"])}</p>

<div class="note">
<p><strong>Where the model fits, stated plainly.</strong>
{html.escape(f["honest_note"])}</p>
</div>

<p>The formula is not only described here — it is
<a href="../back-office/tools/index.html"><code>admin/tools/join.py</code></a>, and
<a href="../explain/index.html">the worked example</a> is its output rather than a
drawing of what its output would look like.</p>

<div class="next"><a href="../explain/index.html">Watch it run →</a>
<a href="../audiences/index.html">← The six audiences</a>
<a href="../data/ontology.json">This page, as JSON</a></div>
"""

def explain_body(fd: dict) -> str:
    art = fd["articles"][0]
    j = fd["joins"].get(art["slug"], {})
    before = fd["before"]
    au = {a["id"]: a for a in fd["audiences"]["audiences"]}

    ents = "".join(
        f'<tr><td><code>{html.escape(e["id"])}</code></td>'
        f'<td><span class="tag">{html.escape(e["type"])}</span></td>'
        f'<td>{html.escape(e["label"])}</td></tr>' for e in art["entities"])
    edges = "".join(
        f'<tr><td><code>{html.escape(e["from"])}</code></td>'
        f'<td><strong>{html.escape(e["verb"])}</strong></td>'
        f'<td><code>{html.escape(e["to"])}</code></td></tr>' for e in art["edges"])

    blocks = ""
    for d in j.get("deliveries", []):
        a = au[d["audience"]]
        reached = d["verdict"] == "reached"
        head = (f'<span class="tag shipped">reached</span> rank {d["rank"]}'
                if reached and d["rank"] else
                ('<span class="tag">control · always</span>' if d.get("control")
                 else '<span class="tag unverified">withheld</span>'))
        conns = "".join(
            f'<div style="border-left:3px solid var(--line2);padding-left:.9rem;margin:.8rem 0">'
            f'<p class="k">{html.escape(c["match"])} · weight {c["weight"]}'
            + (f' · <em>proposed by the model</em>' if c.get("proposed_by") else "")
            + f'</p><p>{html.escape(c["reads"])}</p>'
            f'<p><small><strong>And back:</strong> {html.escape(c["reads_inverse"])}</small></p>'
            + (f'<p><small><strong>Path:</strong> <code>{html.escape(c["path"])}</code></small></p>'
               if c.get("path") else "")
            + "</div>"
            for c in d["connections"])
        tried = "".join(
            f'<tr><td>{html.escape(t["label"])}</td>'
            f'<td>{" ".join(f"<code>{html.escape(w)}</code>" for w in t["wanted"])}</td>'
            f'<td>{t["hits"] or "—"}</td>'
            f'<td>{html.escape(t["why_not"] or "satisfied")}</td></tr>'
            for t in d.get("tried", []))
        blocks += (
            f'<div class="band" id="to-{d["audience"]}">'
            f'<p class="k">{head}</p>'
            f'<h3>{html.escape(d["audience_name"])}</h3>'
            f'<p>{html.escape(d["because"])}</p>'
            + (conns or "")
            + (f'<h4>Every concern tried</h4><div class="tablewrap"><table><thead><tr>'
               f'<th>Concern</th><th>Wanted</th><th>Hits</th><th>Outcome</th></tr></thead>'
               f'<tbody>{tried}</tbody></table></div>' if tried else "")
            + "</div>")

    before_rows = ""
    if before:
        now = {d["audience"]: d for d in j.get("deliveries", [])}
        for d in before["deliveries"]:
            n = now.get(d["audience"], {})
            before_rows += (
                f'<tr><td>{html.escape(d["audience_name"])}</td>'
                f'<td>{d["verdict"]} · {d["rank"] or "—"}</td>'
                f'<td><strong>{n.get("verdict", "?")} · {n.get("rank") or "—"}</strong></td></tr>')

    return f"""
<p class="kicker">The debug view</p>
<h1>Why this article reached these audiences and not the others</h1>
<p class="lede">One real article, put through the join and shown with its working out. This
is the view that exists to be <em>checked</em> rather than read — the one you open when a
feed shows you something and you want to know who decided that. Every line below is output
from <code>admin/tools/join.py</code>, not a drawing of what the output would look like.</p>

<h2 id="article">The article</h2>
<div class="band">
<p class="k">{html.escape(art["date"])} · {html.escape(art["language"])} ·
<a href="{html.escape(art["source_url"])}">{html.escape(art["source_site"])}</a></p>
<h3>{html.escape(art["title"])}</h3>
<p><em>{html.escape(art["title_en"])}</em></p>
<p>{html.escape(art["what_it_says"])}</p>
<p><small>{art["verification"]["confirmed"]} claims confirmed,
{art["verification"]["disputed"]} disputed, {art["verification"]["not_found"]} not found —
re-checked against the frozen sources by the newsroom that published it.</small></p>
</div>

<div class="note"><p><strong>Extraction status:</strong>
{html.escape(art["extraction"]["note"])}</p></div>

<h2 id="graph">What stage 1 pulled out</h2>
<p>The article as entities and edges. Every type here is defined in
<a href="../ontology/index.html#article">the article ontology</a>, and an entity whose type
is not defined stops the build — an unknown type can never match anything, so the article
would look uninteresting rather than unreadable.</p>
<div class="tablewrap"><table><thead><tr><th>Entity</th><th>Type</th><th>Is</th></tr></thead>
<tbody>{ents}</tbody></table></div>
<h3>And how they connect</h3>
<div class="tablewrap"><table><thead><tr><th>From</th><th>Verb</th><th>To</th></tr></thead>
<tbody>{edges}</tbody></table></div>

<h2 id="deliveries">The six verdicts</h2>
<p>One delivery per audience, whether or not the article reached it. A withheld delivery
carries the same structure as a reached one, because explaining what was rejected is the
half a reader actually doubts.</p>
{blocks}

<h2 id="findings">What the first run found — about the ontology, not the article</h2>
<p>The first time this formula ran, the answer was wrong, and it was wrong in a way that
is worth showing rather than quietly fixing. Here is what it said and what it says now:</p>
<div class="tablewrap"><table>
<thead><tr><th>Audience</th><th>First run</th><th>Now</th></tr></thead>
<tbody>{before_rows}</tbody></table></div>

<p>Three defects, all in the hand-maintained audience side rather than in the article:</p>
<ul>
<li><strong>The practitioner ranked highest</strong> — on a story about stage names at a
startup event. Its <em>integrity</em> concern matched on <code>Source</code>, and every
article that freezes its sources has Sources. A concern satisfied by every article is a
tautology: it makes an audience look interested in everything and carries no information
into the ranking. The concern is now <em>qualified</em> — it only fires where the article
is also about a technology, a weakness or a control — and the practitioner is now correctly
withheld from this story.</li>
<li><strong>The executive outranked the founder</strong>, on an event story, because one
Discrepancy satisfied two of its overlapping concerns and scored twice. Rank now counts
each entity once, at its strongest match. The double match is still listed, because it is
real and worth seeing; it just does not pay twice.</li>
<li><strong>The risk owner matched on any event at all</strong> through a concern called
"something more likely or more expensive". An event existing is not a change in exposure.
That concern now requires a <code>Weakness</code>; the article still reaches the risk owner,
by the route its role predicted — sources disagreeing with each other.</li>
</ul>

<div class="band">
<h3>The part worth keeping</h3>
<p>A ranking model that put a stage-naming story at the top of a security practitioner's
feed is not unusual. What is unusual is being able to see it, in one table, with the
offending concern named — and to fix the concern rather than tune a weight until the
symptom goes away. That is the entire argument of this site, happening on the first
article it was pointed at.</p>
<p>The second thing the run showed is subtler. With exact matches only, four audiences tied
at the same rank: the formula was auditable and useless. The discrimination comes back with
the <em>consequence</em> matches — which are the ones a model proposes, because they need
reading rather than lookup. Neither half works alone. A rules engine is checkable and
blunt; a model is sharp and unaccountable; this is a model proposing inside a shape that
records what it proposed.</p>
</div>

<h2 id="data">The same thing, as data</h2>
<p>Every verdict above is served at
<a href="../data/joins/{html.escape(art["slug"])}.json"><code>/data/joins/{html.escape(art["slug"])}.json</code></a>,
the audiences at <a href="../data/audiences.json"><code>/data/audiences.json</code></a> and
the grammar at <a href="../data/ontology.json"><code>/data/ontology.json</code></a>. Run it
yourself:</p>
<pre><code>python3 admin/tools/join.py \
  admin/content/data/articles/{html.escape(art["slug"])}.json</code></pre>

<div class="next"><a href="../audiences/index.html">← The six audiences</a>
<a href="../ontology/index.html">The grammar →</a>
<a href="../library/index.html">The recovered library →</a></div>
"""


def library_body(arc: dict) -> str:
    site = arc["sites"][0]
    posts = site["posts"]
    groups: dict[str, list] = {}
    for p in posts:
        key = "How it works" if "How it works" in (p.get("tags") or []) else "Generated briefings"
        groups.setdefault(key, []).append(p)
    out = ""
    for key in ("How it works", "Generated briefings"):
        items = groups.get(key, [])
        if not items:
            continue
        cards = "".join(
            f'<a class="card" href="../back-office/archive/{p["slug"]}.html">'
            f'<p class="k">{html.escape(p.get("published_human", "undated"))} · '
            f'{p["words"]:,} words</p><h3>{html.escape(p["title"])}</h3></a>'
            for p in items)
        note = ("Dinis Cruz explaining the architecture as he built it. These are the "
                "argument — the diagnosis, the four stages, the structured outputs, the "
                "graph. Everything on this site's <a href=\"../how-it-works/index.html\">"
                "How it works</a> page is assembled from them."
                if key == "How it works" else
                "Output, not argument: briefings the pipeline generated for a CEO, a CISO, "
                "a CTO and two kinds of board member, from the Hacker News feed. They are "
                "the evidence that the thing ran, and the earliest examples of the "
                "one-article-many-audiences idea this site is now rebuilding.")
        out += (f'<h2 id="{slugify(key)}">{html.escape(key)} '
                f'<span class="tag">{len(items)}</span></h2><p>{note}</p>'
                f'<div class="grid">{cards}</div>')
    return f"""
<p class="kicker">The library</p>
<h1>The first MVP, in full</h1>
<p class="lede">Everything recovered from <code>mvp.myfeeds.ai</code>, readable here
rather than only as an archive listing: {len(posts)} posts,
{sum(p["words"] for p in posts):,} words, from a site that no longer exists. The long-form
posts are where the architecture was worked out; the briefings are what the pipeline
produced when it ran.</p>

<div class="note"><p>These are reproduced as published. Links inside them point at pages
that in most cases no longer resolve and images are still served from the dead domain —
both left as written rather than silently repaired, because a rewritten archive stops
being evidence. How they were recovered, and the nine URLs that could not be, is on
<a href="../back-office/archive/index.html">the archive page</a>.</p></div>

{out}

<div class="next"><a href="../how-it-works/index.html">The architecture they describe →</a>
<a href="../back-office/archive/index.html">How they were recovered →</a>
<a href="../index.html">← Home</a></div>
"""

def provenance_body(fd: dict) -> str:
    n_art = len(fd["articles"])
    return f"""
<p class="kicker">Disclosure</p>
<h1>This site is written by an AI, and reviewed afterwards</h1>
<p class="lede">Not "AI-assisted". The prose on every page, the two ontologies, the six
audience definitions, the extraction of entities from each article and the classifications
that follow from them were all produced by a language model — a Claude Code session — and
are read by a human <strong>after</strong> publication rather than before. That is an
unusual thing to put at the top of a page instead of at the bottom, and it is the only
honest place for it on a site whose entire argument is that automated selection should be
checkable.</p>

<h2 id="who">Who does what</h2>
<div class="tablewrap"><table>
<thead><tr><th>Part</th><th>Made by</th><th>Reviewed</th></tr></thead>
<tbody>
<tr><td>The pages and their argument</td><td>Model</td>
<td>After the fact, by Dinis Cruz</td></tr>
<tr><td>The article and audience ontologies</td><td>Model</td>
<td>After the fact; the open questions are on <a href="../review/index.html">the review
page</a></td></tr>
<tr><td>The six audience role definitions</td><td>Model</td>
<td>After the fact. These are the most opinionated thing here and the most worth
disagreeing with</td></tr>
<tr><td>Entity extraction from each article</td><td>Model</td>
<td>Not yet. {n_art} articles, none reviewed</td></tr>
<tr><td>The join formula and its weights</td><td>Model</td><td>After the fact</td></tr>
<tr><td>The source articles themselves</td>
<td><a href="https://pt.newsroom.sgit.ai/">pt.newsroom.sgit.ai</a></td>
<td>By that newsroom's named human editor of record, <em>before</em> publication</td></tr>
</tbody></table></div>

<p>Note the asymmetry in the last row. The Portuguese newsroom this site reads from has a
named human who reads every page before it goes live. This site does not, yet. That gap is
on <a href="../team/board.html">the board</a> and is the single most important thing to fix
before anything here runs on a schedule.</p>

<h2 id="vocabulary">The status on every page</h2>
<p>Every page on this site carries one of these, at the top, under the breadcrumb:</p>
<div class="tablewrap"><table>
<thead><tr><th>Status</th><th>Means</th></tr></thead>
<tbody>
<tr><td><span class="tag unverified">ai-generated, unreviewed</span></td>
<td>A model wrote it and nobody has checked it. Today this is every page.</td></tr>
<tr><td><span class="tag argued">ai-generated, human-reviewed</span></td>
<td>A model wrote it and a named person has read it and let it stand.</td></tr>
<tr><td><span class="tag shipped">human-written</span></td>
<td>A person wrote it.</td></tr>
</tbody></table></div>
<p>A page moves off the default when somebody names themselves against it, which is why
the generator holds a map of exceptions rather than a field that has to be remembered.
An empty map is the honest state and it is currently empty.</p>

<h2 id="why">Why this matters more here than elsewhere</h2>
<p>This site argues that a recommendation you cannot interrogate is worthless. A site
making that argument in prose a model wrote, using an ontology the same model invented, to
classify articles the same model extracted, would be an unusually pure example of the
problem it describes — unless it says so, in the same place a reader forms their view of
whether to trust it.</p>

<div class="band">
<h3>The three places a model can be wrong here, in order of damage</h3>
<ol>
<li><strong>Extraction.</strong> A model can name an entity the article does not contain.
Everything downstream then explains, correctly and traceably, a connection that should not
exist — and the provenance trail makes it <em>more</em> convincing, not less. This is the
worst failure mode in the whole system and it currently has no automated guard.</li>
<li><strong>The audience definitions.</strong> Six role descriptions written by a model
about how real people read. They are plausible, which is exactly the problem: plausible
and unchecked is how a stereotype gets encoded as a data structure. These need a
practitioner, an investor and a risk owner to read their own entry and say what is
wrong.</li>
<li><strong>The prose.</strong> The least dangerous, because a reader can tell. A wrong
sentence about how something works is visible in a way that a wrong edge in a graph is
not.</li>
</ol>
</div>

<h2 id="not">What is not AI-generated</h2>
<ul>
<li>The <a href="../library/index.html">recovered MVP posts</a> — written by Dinis Cruz in
2025 and reproduced as published.</li>
<li>The source articles, which belong to the Portuguese newsroom and are linked rather
than reproduced.</li>
<li>The measurements in this repository: counts of pages, words, articles and connections
are computed from files, not written.</li>
</ul>

<div class="next"><a href="../review/index.html">What a human is being asked →</a>
<a href="../about/index.html">About &amp; honest edges →</a>
<a href="../index.html">← Home</a></div>
"""


def review_body(fd: dict, review: dict) -> str:
    kinds = {
        "audience-receives-everything": "An audience that receives everything",
        "audience-receives-nothing": "An audience that receives nothing",
        "concern-fires-on-everything": "A concern that fires on everything",
        "concern-never-fires": "A concern that has never fired",
    }
    blocks = ""
    for kind, heading in kinds.items():
        fs = [f for f in review["findings"] if f["kind"] == kind]
        if not fs:
            continue
        blocks += f'<h3>{html.escape(heading)} <span class="tag">{len(fs)}</span></h3>'
        for f in fs:
            d = f.get("diagnosis")
            diag = ""
            if isinstance(d, dict):
                counts = ", ".join(f"<code>{html.escape(k)}</code> {v}"
                                   for k, v in d["fire_counts"].items())
                diag = (f'<p><small><strong>The model\'s own diagnosis, which is a '
                        f'proposal and not a finding:</strong> fired on — {counts} '
                        f'(of {d["of"]} articles). {html.escape(d["note"])}</small></p>')
            blocks += (
                f'<div class="band" id="{html.escape(f["id"])}">'
                f'<p class="k"><span class="tag open">open</span> '
                f'{html.escape(f["audience"])}'
                + (f' · {html.escape(f["concern"])}' if f["concern"] else "")
                + f'</p><p><strong>{html.escape(f["question"])}</strong></p>'
                + diag
                + f'<p><small><strong>Answering it would change:</strong> '
                  f'{html.escape(f["would_change"])}</small></p>'
                + (f'<p><small><strong>Articles:</strong> '
                   + ", ".join(f"<code>{html.escape(a)}</code>" for a in f["articles"])
                   + "</small></p>" if f["articles"] else "")
                + "</div>"
            )

    return f"""
<p class="kicker">The feedback loop</p>
<h1>What a human is being asked to settle</h1>
<p class="lede">The ontologies here do not have to be right. They have to be <strong>wrong
in ways somebody can see and correct</strong> — which is a different and much more
achievable target, and the only one available to a system whose classifications are
written by a model. This page is the output of that principle: not a quality score, but
{review["counts"]["open"]} specific questions, each with the evidence that raised it and
what an answer would change.</p>

<div class="note">
<p><strong>Nothing on this page fixes itself.</strong> The formula does not change in
response to these questions. A model proposing a diagnosis and then acting on it is the
same closed loop this site exists to argue against — so the questions sit here until a
person answers them, and the answer is recorded next to the question.</p>
</div>

<h2 id="corpus">The corpus these came from</h2>
<p>{review["corpus"]["articles"]} articles from
<a href="https://pt.newsroom.sgit.ai/">pt.newsroom.sgit.ai</a>. That is a small corpus and
the questions below reflect it: several concerns have never fired, and with three articles
the honest reading is usually "this newsroom has not published that kind of thing yet"
rather than "the concern is wrong". Both answers are useful and only a human can tell them
apart.</p>
<ul>""" + "".join(
        f'<li><code>{html.escape(s)}</code></li>' for s in review["corpus"]["slugs"]
    ) + f"""</ul>

<h2 id="questions">The {review["counts"]["open"]} open questions</h2>
{blocks}

<h2 id="how">How to answer one</h2>
<p>Every question has an id. An answer is a line in
<code>admin/content/data/review-answers.json</code> naming the question, the person, the
date and what they decided — and, where the answer changes the ontology, the change lands
in the same release as the answer so the two cannot drift. There is no form on this page
and no comment box: the answers version with the repository, like everything else here.</p>
<pre><code>{{
  "question": "aud-everything-startups",
  "answered_by": "&lt;name&gt;",
  "date": "2026-09-__",
  "decision": "keep | narrow | qualify | replace",
  "because": "&lt;one sentence a stranger could check&gt;"
}}</code></pre>

<h2 id="data">As data</h2>
<p><a href="../data/review.json"><code>/data/review.json</code></a> — regenerate with
<code>python3 admin/tools/review.py</code> after any join run.</p>

<div class="next"><a href="../provenance/index.html">← Who wrote this site</a>
<a href="../explain/index.html">The debug view →</a>
<a href="../audiences/index.html">The audiences →</a></div>
"""

# ------------------------------------------------------------------------------- build


def build() -> int:
    pages = json.loads((CONTENT / "pages.json").read_text(encoding="utf-8"))
    roles = load_roles()
    cards = load_board()

    # Pages whose bodies come from the repository itself rather than from a file in
    # admin/content/ — the team from team/roles/, the board from team/board/, the release
    # history from VERSION_LOG. They are registered here rather than in pages.json so that
    # a role added to the repository cannot fail to appear on the site.
    pages += [
        {
            "path": "team/index.html",
            "section": "How this site is run",
            "title": "How this site is run",
            "desc": (
                "The agentic team behind myfeeds.sgit.ai: the roles as files, the failure "
                "condition each is judged on, the rules they share, and the board where "
                "the open work is. Generated from team/roles/*/ROLE.md."
            ),
        },
        {
            "path": "team/board.html",
            "section": "How this site is run",
            "title": "The board",
            "desc": (
                "Open work as a kanban of files: needs only the human owner can supply, "
                "and tasks an agent can pick up from its starting prompt. Nothing runs — "
                "the board versions with the repository it tracks."
            ),
        },
        {
            "path": "team/prompts.html",
            "section": "How this site is run",
            "title": "Starting prompts",
            "desc": (
                "One prompt per recurring task on this site — add a page, publish a "
                "contract, cut a release, sweep the claims — each naming the role file "
                "that turns a general model into the role that owns the work."
            ),
        },
        {
            "path": "admin/versions.html",
            "section": "Provenance",
            "title": "Release history",
            "desc": (
                "Every release of this site: version, date, and what it did — including "
                "what an earlier version got wrong, where one did."
            ),
        },
    ]

    arc = backoffice.load_archive(ROOT)
    fd = feeds.load_all(ROOT)
    review = json.loads((ROOT / "data" / "review.json").read_text(encoding="utf-8")) \
        if (ROOT / "data" / "review.json").exists() else {
            "counts": {"open": 0}, "corpus": {"articles": 0, "slugs": []}, "findings": []}
    site0 = arc["sites"][0] if arc["sites"] else None

    pages += [
        {
            "path": "provenance/index.html",
            "section": "Provenance",
            "title": "This site is written by an AI, and reviewed afterwards",
            "desc": (
                "Not AI-assisted: the prose, both ontologies, the audience definitions and "
                "every classification were produced by a language model and are read by a "
                "human after publication rather than before. Who made what, the three "
                "places a model can be wrong here in order of damage, and what is not "
                "AI-generated."
            ),
        },
        {
            "path": "review/index.html",
            "section": "Provenance",
            "title": "What a human is being asked to settle",
            "desc": (
                "The ontologies do not have to be right; they have to be wrong in ways "
                "somebody can see and correct. The open questions the corpus raised, each "
                "with its evidence and what an answer would change — and nothing on the "
                "page fixes itself."
            ),
        },
        {
            "path": "audiences/index.html",
            "section": "The argument",
            "title": "Six audiences, and what each converts news into",
            "desc": (
                "The audience side of the join: six roles with a stated appetite rather "
                "than a tone of voice — a founder, an allocator, an executive, a "
                "practitioner, a risk owner, and a faithful translation that acts as the "
                "control. What separates them is what each converts a piece of news into."
            ),
        },
        {
            "path": "ontology/index.html",
            "section": "The argument",
            "title": "Two ontologies and the join between them",
            "desc": (
                "One ontology for what an article contains, one for what a role watches "
                "for, and the published formula where they meet. Every verb has a named "
                "inverse and reads as a sentence both ways; the verbs that are banned are "
                "listed with the reason."
            ),
        },
        {
            "path": "explain/index.html",
            "section": "The argument",
            "title": "Why this article reached these audiences and not the others",
            "desc": (
                "One real Portuguese article put through the join, with its working out: "
                "the entities, every concern tried, the connections that fired and the "
                "verdicts that did not — plus the three defects the first run found in "
                "the audience ontology, shown before and after."
            ),
        },
        {
            "path": "library/index.html",
            "section": "The argument",
            "title": "The first MVP, in full",
            "desc": (
                "Everything recovered from mvp.myfeeds.ai, readable: the long-form posts "
                "where the architecture was worked out, and the briefings the pipeline "
                "generated for five personas when it ran."
            ),
        },
        {
            "path": "back-office/index.html",
            "section": "Back office",
            "title": "Everything this site is built from",
            "desc": (
                "The working material behind myfeeds.sgit.ai: writing recovered from a "
                "site that no longer exists, the documents that live in other "
                "repositories, the tools that did the recovering, and every release cut "
                "so far. Indexed from what is on disk."
            ),
        },
        {
            "path": "back-office/archive/index.html",
            "section": "Back office",
            "title": "The mvp.myfeeds.ai archive",
            "desc": (
                "The first MyFeeds MVP recovered from the Internet Archive: the posts "
                "that survived, mostly inside a single capture of the RSS feed, and the "
                "nine URLs its own sitemap named that no crawler ever caught."
            ),
        },
        {
            "path": "back-office/documents/index.html",
            "section": "Back office",
            "title": "Documents",
            "desc": (
                "The business plan, the pitch decks and their briefs, and the engine's "
                "architecture notes — indexed where they live rather than copied, because "
                "a document has one owner."
            ),
        },
        {
            "path": "back-office/tools/index.html",
            "section": "Back office",
            "title": "Tools",
            "desc": (
                "The archiver, the generator, the release gate and the live check: one "
                "file each, nothing to install, each documented in its own header."
            ),
        },
    ]

    generated = {
        "provenance/index.html": lambda: provenance_body(fd),
        "review/index.html": lambda: review_body(fd, review),
        "audiences/index.html": lambda: audiences_body(fd),
        "ontology/index.html": lambda: ontology_body(fd),
        "explain/index.html": lambda: explain_body(fd),
        "library/index.html": lambda: library_body(arc),
        "back-office/index.html": lambda: backoffice_index_body(arc),
        "back-office/archive/index.html": lambda: archive_index_body(arc),
        "back-office/documents/index.html": documents_body,
        "back-office/tools/index.html": tools_body,
        "team/index.html": lambda: team_index_body(roles, cards),
        "team/board.html": lambda: board_body(cards, roles),
        "team/prompts.html": prompts_body,
        "admin/versions.html": versions_body,
    }
    if site0:
        for post in site0["posts"]:
            pages.append({
                "path": f"back-office/archive/{post['slug']}.html",
                "section": "Back office",
                "title": post["title"],
                "desc": (
                    f"Recovered from mvp.myfeeds.ai, published "
                    f"{post.get('published_human', 'undated')}: "
                    + " ".join(post["body"].split()[:28]) + "…"
                ),
                "hidden": True,
            })
            generated[f"back-office/archive/{post['slug']}.html"] = (
                lambda p=post: archive_post_body(p, site0)
            )

    for r in roles:
        pages.append({
            "path": f"team/roles/{r['slug']}.html",
            "section": "Team",
            "title": r["name"],
            "desc": f"{r['name']} — {r['mission']} Fails when: {r['claim']}",
            "hidden": True,
        })
        generated[f"team/roles/{r['slug']}.html"] = (lambda role=r: role_page_body(role, roles))

    # Every file the build reads. A twin written over one of these would destroy its own
    # source on the next run, silently, and the page would keep building from the wreckage
    # — which is exactly what happened to team/prompts.md before this check existed.
    inputs = {(CONTENT / "pages.json").resolve()}
    inputs |= {f.resolve() for f in ROLES_DIR.glob("*/ROLE.md")}
    inputs |= {f.resolve() for f in BOARD_DIR.glob("*.md")}
    inputs |= {f.resolve() for f in CONTENT.rglob("*.html")}
    inputs.add((ROOT / "team" / "prompts" / "README.md").resolve())

    seen: set[str] = set()
    written: list[Path] = []
    for page in pages:
        path = page["path"]
        if path in seen:
            raise SystemExit(f"build: duplicate page path {path}")
        seen.add(path)
        if path in generated:
            body = generated[path]()
        else:
            src = CONTENT / path
            if not src.exists():
                raise SystemExit(f"build: no body for {path} (expected {src})")
            body = src.read_text(encoding="utf-8")

        out_html = ROOT / path
        out_html.parent.mkdir(parents=True, exist_ok=True)
        out_html.write_text(render_page(page, body), encoding="utf-8")
        out_md = ROOT / (path[:-5] + ".md")
        if out_md.resolve() in inputs:
            raise SystemExit(
                f"build: the markdown twin for {path} would overwrite {out_md}, which is "
                f"a build input — move the source or change the page path"
            )
        out_md.write_text(render_markdown(page, body), encoding="utf-8")
        written += [out_html, out_md]

    visible = [p for p in pages if not p.get("hidden")]
    role_pages = [p for p in pages if p.get("hidden")]

    # llms.txt — the index an agent arrives at.
    sections: dict[str, list[dict]] = {}
    for p in visible:
        sections.setdefault(p["section"], []).append(p)
    lines = [
        f"# {SITE_NAME}",
        "",
        f"> {SITE_THESIS} {SITE_DESC}",
        "",
        f"Site version: {SITE_VERSION}. A site in the [sgit.ai](https://sgit.ai) network.",
        "Every page below is markdown, generated from the same source as the HTML page at",
        "the same path (swap `.md` for `.html`). Links inside the markdown point at",
        "markdown, so you can traverse the whole site without parsing HTML.",
        "",
        "Notes for agents:",
        "- Nothing here is a running service. This site publishes contracts and an",
        "  argument; what does not exist yet is listed, in order, at /build-order/index.md",
        "- Claims carry a status: `shipped` (in this repository, runnable), `argued` (a",
        "  position, reasoning shown), `unverified` (believed, not yet checked against a",
        "  primary source). Treat `unverified` as a lead, not a fact.",
        "- The site is run by an agentic team: /team/index.md, with one file per role at",
        "  team/roles/<slug>/ROLE.md in the repository and the roster as data at",
        "  /data/team.json",
        "- To change a page, edit admin/content/ and run admin/build/build_pages.py. The",
        "  tree at the repository root is output.",
        "",
        f"If your tooling cannot follow links out of this file, fetch /llms-full.txt —",
        "every page of this site concatenated into one document.",
        "",
    ]
    for section, items in sections.items():
        lines.append(f"## {section}")
        for p in items:
            lines.append(f"- [{p['title']}](/{p['path'][:-5]}.md): {p['desc']}")
        lines.append("")
    lines.append("## Roles (one page per role, generated from its ROLE.md)")
    for p in role_pages:
        lines.append(f"- [{p['title']}](/{p['path'][:-5]}.md): {p['desc']}")
    lines += ["", "## Licence", "", LICENCE, ""]
    (ROOT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")

    # llms-full.txt — the whole site in one request.
    full = [f"# {SITE_NAME} — every page, {SITE_VERSION}", "",
            f"> {SITE_THESIS}", "",
            f"Generated {date.today().isoformat()} from {SITE_ORIGIN}/. Sections below are",
            "the markdown twins of every page, in navigation order.", ""]
    for p in pages:
        full.append("\n" + "=" * 78)
        full.append(f"# /{p['path']}")
        full.append("=" * 78 + "\n")
        full.append((ROOT / (p["path"][:-5] + ".md")).read_text(encoding="utf-8"))
    (ROOT / "llms-full.txt").write_text("\n".join(full), encoding="utf-8")

    # sitemap + robots
    urls = "".join(
        f"<url><loc>{SITE_ORIGIN}/{p['path']}</loc>"
        f"<lastmod>{date.today().isoformat()}</lastmod></url>"
        for p in pages
    )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>\n",
        encoding="utf-8",
    )
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE_ORIGIN}/sitemap.xml\n", encoding="utf-8"
    )
    (ROOT / "CNAME").write_text(f"{SITE_HOST}\n", encoding="utf-8")
    # Deny by default. The narrowest permission that works, and why each grant exists —
    # here there are no grants at all, which is a real answer and the right one: every
    # page on this site is static content read out of the vault, and reads need no grant.
    # Nothing on this site can modify the vault it is served from.
    (ROOT / "app.json").write_text(
        json.dumps(
            {
                "entry": "index.html",
                "present": True,
                "auto_open": True,
                "title": SITE_NAME,
                "version": SITE_VERSION,
                "permissions": {},
                "permissions_note": (
                    "Deny by default: this app requests nothing. It renders static pages "
                    "read from the vault, and reads require no grant. If a future release "
                    "needs a permission, add it here with the reason it exists."
                ),
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    # versions/ — the estate's versions contract (sgit.ai/docs/guidance): an index plus
    # one file per version, so an app can render it, a script can check it, and an agent
    # can read it without running anything.
    versions_dir = ROOT / "versions"
    versions_dir.mkdir(exist_ok=True)
    for e in VERSION_LOG:
        (versions_dir / f"{e['version']}.json").write_text(
            json.dumps(
                {
                    "version": e["version"],
                    "date": e["date"],
                    # The commit that CARRIES a version cannot be known while building
                    # that version — it does not exist yet. CI tags the release commit
                    # v<version> at publish time, so the tag is the durable pointer and
                    # is recorded here instead of a hash that would be wrong or would
                    # change on every rebuild.
                    "commit": None,
                    "commit_ref": f"refs/tags/{e['version']}",
                    "vault": None,
                    "reconstructed": False,
                    "title": e["title"],
                    "summary": e["summary"],
                    "changes": e.get("changes", []),
                    "corrects": e.get("corrects"),
                    "basis": e.get("basis", []),
                    "site": SITE_NAME,
                    "url": f"{SITE_ORIGIN}/admin/versions.html#{version_anchor(e['version'])}",
                },
                indent=2,
            ) + "\n",
            encoding="utf-8",
        )
    (versions_dir / "index.json").write_text(
        json.dumps(
            {
                "site": SITE_NAME,
                "current": SITE_VERSION,
                "source": "VERSION_LOG in admin/build/build_pages.py",
                "versions": [
                    {
                        "version": e["version"],
                        "date": e["date"],
                        "title": e["title"],
                        "href": f"{e['version']}.json",
                    }
                    for e in reversed(VERSION_LOG)
                ],
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    # The audience/ontology data, published so a reader can fetch the same facts the
    # pages show. A page showing a number nobody can fetch is asking to be trusted.
    for name in ("audiences.json", "ontology.json"):
        (ROOT / "data" / name).write_text(
            json.dumps(json.loads((CONTENT / "data" / name).read_text(encoding="utf-8")),
                       indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "api" / "v1").mkdir(parents=True, exist_ok=True)
    (ROOT / "api" / "v1" / "audiences.json").write_text(
        json.dumps({
            "version": SITE_VERSION,
            "count": len(fd["audiences"]["audiences"]),
            "audiences": [
                {"id": a["id"], "name": a["name"], "order": a["order"],
                 "currency": a["currency"], "control": a.get("control", False),
                 "concerns": [c["id"] for c in a["concerns"]],
                 "href": f"{SITE_ORIGIN}/audiences/index.html#{a['id']}"}
                for a in sorted(fd["audiences"]["audiences"], key=lambda x: x["order"])
            ],
        }, indent=2) + "\n", encoding="utf-8")
    (ROOT / "api" / "v1" / "joins.json").write_text(
        json.dumps({
            "version": SITE_VERSION,
            "formula": fd["ontology"]["join"]["formula"]["id"],
            "joins": [
                {"article": k, "title": v["title"],
                 "reached": v["summary"]["reached"], "withheld": v["summary"]["withheld"],
                 "href": f"{SITE_ORIGIN}/data/joins/{k}.json"}
                for k, v in fd["joins"].items()
            ],
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # data/site.json — the page inventory as data. The validator reads this rather than
    # re-deriving the list from pages.json plus a hardcoded set of generated paths, which
    # is what it used to do: the back office shipped and the validator went on checking
    # 19 pages out of 38 while reporting success.
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "site.json").write_text(
        json.dumps(
            {
                "site": SITE_NAME,
                "version": SITE_VERSION,
                "generated": date.today().isoformat(),
                "source": "admin/build/build_pages.py",
                "counts": {
                    "pages": len(pages),
                    "indexed": len(visible),
                    "hidden": len(pages) - len(visible),
                },
                "pages": [
                    {k: p[k] for k in ("path", "section", "title", "hidden") if k in p}
                    for p in pages
                ],
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    # data/team.json — the roster at a stable address, because the primary reader of a
    # page like /team/ is an agent that would rather have the data.
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "team.json").write_text(
        json.dumps(
            {
                "site": SITE_NAME,
                "version": SITE_VERSION,
                "generated": date.today().isoformat(),
                "source": "team/roles/*/ROLE.md",
                "licence": LICENCE,
                "totals": {
                    "roles": len(roles),
                    "falsifiable_claims": sum(
                        1 for r in roles if r.get("claim_form") == "falsifiable"),
                    "board_cards": len(cards),
                    "open_cards": sum(
                        1 for c in cards if c.get("status") in ("need", "todo", "doing")),
                    "pages": len(pages),
                },
                "roles": [
                    {k: r[k] for k in
                     ("name", "slug", "group", "order", "mission", "claim", "claim_form",
                      "not_responsible_for", "owns", "tools", "file") if k in r}
                    for r in roles
                ],
                "board": [
                    {k: c[k] for k in
                     ("id", "title", "status", "owner", "kind", "opened", "file") if k in c}
                    for c in cards
                ],
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print(f"build: {SITE_VERSION} · {len(pages)} pages "
          f"({len(visible)} in the index, {len(role_pages)} not indexed) · "
          f"{len(roles)} roles · {len(cards)} board cards")
    print(f"build: wrote {len(written)} page files + llms.txt, llms-full.txt, "
          f"sitemap.xml, robots.txt, CNAME, app.json, data/team.json, "
          f"versions/index.json + {len(VERSION_LOG)} version file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(build())
