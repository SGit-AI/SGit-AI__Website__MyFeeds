# How this site is built

> The pipeline: page bodies in admin/content/, one generator, a validator that fails the build on a broken link or a missing markdown twin, and the authoring contract that keeps a vault-hosted page from rendering blank.

*Source: <https://myfeeds.sgit.ai/admin/index.html> · site v0.1.2 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Provenance

# How this site is built

Not hosted on a web server in the usual sense. The published tree is a static mirror and, equally, a **vault app** — a set of pages that can live inside an encrypted vault and be decrypted and rendered in the reader's browser. That second target is what makes the authoring contract below non-negotiable.

## The tree

```
# output — generated, never hand-edited
├── index.html · index.md            # every page has a markdown twin at the same path
├── thesis/ · read-state/ · vault/ · build-order/
├── team/index.html · team/board.html · team/prompts.html · team/roles/<slug>.html
├── admin/index.html · admin/versions.html
├── llms.txt · llms-full.txt · sitemap.xml · robots.txt · CNAME · app.json
├── data/team.json                   # the roster, as data, at a stable address
└── assets/site.css · assets/site.js

# source — what you edit
├── admin/content/                   # one body per page, plus pages.json
├── admin/build/build_pages.py       # the generator: one shell, all pages
├── admin/build/validate.js          # the gate
└── team/roles/<slug>/ROLE.md        # the roles; the team pages are generated from these
    team/board/*.md · team/prompts.md
```

## Adding a page

```
# 1. write the body — just the <main> fragment: no head, no nav, no footer
$ vim admin/content/case-studies/my-study.html
# 2. register it: { "path", "section", "title", "desc" }
$ vim admin/content/pages.json
# 3. build and check
$ python3 admin/build/build_pages.py && node admin/build/validate.js
```

The build then produces, without further work: the page with its navigation, footer and version stamp; its `.md` twin with every link rewritten to markdown; its row in `llms.txt`; its section in `llms-full.txt`; its entry in `sitemap.xml`; and its canonical, Open Graph and JSON-LD tags.

## The authoring contract

Four rules. The first two are not style preferences — breaking them produces a page that is blank for a visitor rather than one that looks wrong.

1. **No declarative reference to a vault path.** No `<link href>`, `<script src>` or `<img src>` pointing at a file in the vault. Inside a sandboxed vault frame those requests 404 before the bridge installs. The validator scans for this and fails the build.

2. **Assets arrive over the bridge.** Every page carries a small critical style block inline and a twenty-line bootstrap that waits for `window.sg`, tries `sg.loadCss`/`sg.loadJs`, falls back to `sg.vfs.readText` and injection, and falls back again to plain `fetch` for the static mirror. Worst case the page is unstyled and readable.

3. **JavaScript adds style, never content.** Every page must be complete with scripting disabled. `assets/site.js` highlights the current nav item, wraps tables for narrow screens and adds heading anchors — nothing a reader would miss.

4. **Output is never hand-edited.** Editing `index.html` is a change the next build silently erases and the validator cannot catch, because it checks the output against the content rather than against your intention.

## Generated from the repository, not described beside it

The team section is not written prose about the roles. `/team/`, every role page, and `data/team.json` are all generated from `team/roles/<slug>/ROLE.md`; the board is generated from `team/board/*.md`; the release history is generated from `VERSION_LOG` in the generator itself. So the site cannot describe a role the repository does not carry, quote a count that has drifted, or list a card that was closed three releases ago.

Two deliberate divergences from the house pattern elsewhere in the estate, recorded because a reader comparing sites will notice them:

- **Front matter rather than prose fields.** The estate's `ROLE.md` files carry their identity fields as markdown. Here they are YAML front matter, because these files are parsed at build time and a parse failure should be a build error rather than a page with a missing sentence. The markdown body below the front matter follows the house sections.

- **The generated team pages sit under `team/` beside their own sources.** `team/roles/dev.html` is output; `team/roles/dev/ROLE.md` is source. The URL was worth more than the tidiness, and the validator knows which is which.

## Validation before every push

- Every internal link is resolved against the real file tree — a broken link fails the build, not the reader.

- Every page has a markdown twin, and the twin is not empty.

- The contract scan: no `<link href>`, `<script src>` or `<img src>` pointing at a relative path.

- Every page carries a canonical URL, a description and JSON-LD structured data.

- Every page is reachable from the navigation or from a page that is — no orphans.

- Every inline script and `assets/site.js` is parse-checked.

- Every status claim uses one of the three permitted markers and nothing else.

- The roster served at `data/team.json` matches the files on disk.

## Release and deploy

The deploy pipeline is the estate's, shared by every `*.sgit.ai` site and taken from `SGit-AI__Website__Teams` rather than reinvented here. One workflow, three jobs, in this order:

| Job | Does | Gate |
|---|---|---|
| `validate` | Runs the validator, rebuilds on a clean checkout, and fails if the committed tree differs by a byte | Runs on pull requests too, so branch work is gated before it reaches the release branch. A failure means no tag and no publish. |
| `tag-release` | Tags the release commit `v{major}.{minor}.{patch}`, backfilling any historical release that has no tag | Only on a push to `dev`. The version is owned by `admin/build/version.txt` and must also appear in the release commit's *subject* — `site vX.Y.Z: …` — and CI fails if the two disagree, if the version was reused, or if the bump is not the next minor. |
| `deploy` | Assembles the tree (excluding `.git`, `.github` and `.sg_vault`) and publishes it to GitHub Pages | Never from a pull request, and never when validation failed. Publishes even when `tag-release` skipped, because a missing tag is a bookkeeping gap and a blocked deploy is an outage. |

That last distinction is not hypothetical. On the main site an earlier version of `tag-release` tagged unconditionally, so two good commits landing on top of a release failed the job and took the publish down with them — with an error that said the version had not been bumped when the truth was that this was not a release. The estate's current workflow carries that fix and several others this site has not had to learn the hard way; the standing instruction in the [DevOps role](../team/roles/devops.md) is not to diverge from it without a reason on the board.

```
# 1. bump admin/build/version.txt and add its VERSION_LOG entry in build_pages.py
# 2. regenerate and validate
$ python3 admin/build/build_pages.py && node admin/build/validate.js
# 3. commit the whole tree — source and output — with the version in the SUBJECT
$ git commit -m "site vX.Y.Z: what this release did" && git push origin dev
# 4. verify live — the version string has to come back from the site itself
$ ./admin/build/verify-live.sh
```

Step 4 is separate from the workflow on purpose, because it is the one thing CI cannot tell you. A green deploy job means GitHub accepted an artifact; it does not mean the site is serving it. Elsewhere in this estate two releases pushed cleanly, reported success and never reached the site — `actions/configure-pages` got a 429 and the deploy job died before running a step, and a two-release-old page was served for forty minutes with every check green, because the failure was in a job neither remote knows about. So the last act of a release is to ask the live site what version it is serving, and `verify-live.sh` exits non-zero until it answers correctly.

## Versions are data

The version appears in the navigation of every page and **is a link** — to that version's own entry, not to a generic changelog, because a reader who clicks `v0.1.1` wants to know what v0.1.1 was. The same history is served as data at `/versions/index.json` and one file per version, so a script can check a claim about a release without rendering a page. Each entry's `title` is a sentence rather than a label, and a release that corrects an earlier one says which and how.

One honest note on that contract: the estate's shape includes the commit a version was built from, and this site records the tag reference rather than a hash. The commit that carries a version cannot be known while that version is being built — it does not exist yet — and CI tags the release commit at publish time, so `refs/tags/v0.1.1` is the durable pointer and a hash written at build time would either be wrong or change on every rebuild.

[Release history →](versions.md) [The team →](../team/index.md) [← Home](../index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/admin/index.html)*
