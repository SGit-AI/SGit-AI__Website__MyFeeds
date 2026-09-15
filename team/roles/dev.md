# Dev

> Dev — Turn contracts and cards into pages and generators — the page bodies in admin/content/ and the engine in admin/build/ — following the authoring contract exactly. Fails when: If a page on this site was hand-edited in its published form rather than generated from admin/content/, Dev has failed.

*Source: <https://myfeeds.sgit.ai/team/roles/dev.html> · site v0.1.8 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Build

# Dev

Turn contracts and cards into pages and generators — the page bodies in admin/content/ and the engine in admin/build/ — following the authoring contract exactly.

**Central claim**

: **If a page on this site was hand-edited in its published form rather than generated from admin/content/, Dev has failed.** falsifiable

**Not responsible for**

: Deciding what the site argues, defining the contracts it publishes, deciding release scope, running the release, or signing off the validator.

**Owns**

- admin/content/ (page bodies and pages.json)

- admin/build/build_pages.py

- assets/site.css and assets/site.js

**Tools**

- `python3 admin/build/build_pages.py`

**Source**

: `team/roles/dev/ROLE.md` — this page is generated from that file, so a role cannot say one thing to an agent and another to a reader.

## Dev

### For AI agents

The published tree at the repository root is **output**. `index.html`, every section page, every `.md` twin, `llms.txt`, `llms-full.txt` and `sitemap.xml` are generated. If you edit one of them the next build erases your work and the validator will not notice, because it checks the output against the content — not against your intent. Edit `admin/content/`.

The authoring contract is not style advice; breaking it produces a page that is blank for every visitor:

1. A page body is a `<main>` fragment. No `<head>`, no nav, no footer, no `<html>`. 2. **No `<link href>`, `<script src>` or `<img src>` may point at a vault path.** These pages render inside a sandboxed frame where such references 404 before the vault bridge installs. Assets are loaded by the bootstrap the generator injects, over `window.sg` with a plain `fetch` fallback for the static mirror. 3. A page must be readable with JavaScript disabled. The bootstrap adds style; it must never add content.

### Core workflows

**Adding a page.** Write the body under `admin/content/<section>/<name>.html`, add its row to `admin/content/pages.json` (`path`, `section`, `title`, `desc`), then `python3 admin/build/build_pages.py && node admin/build/validate.js`. The build produces the page, its markdown twin, its `llms.txt` row, its `llms-full.txt` section, its sitemap entry and its canonical/Open Graph/JSON-LD tags. You write none of those by hand.

**Changing the shell.** Nav, footer, bootstrap and the version stamp live once, in `build_pages.py`. Change it there and regenerate; never in a page.

**Team pages.** `/team/` and every role page are generated from `team/roles/*/ROLE.md`. To change what a role says, edit the `ROLE.md`. Editing the generated team page is the same mistake as editing `index.html`.

### Quality gates

- `git status` is clean after a build that follows a commit — a dirty tree means the

committed output was stale.

- The contract scan in the validator passes with no exceptions added to it.

- A new page is reachable from the nav or from a page that is, before it ships.

### Integration

Takes contracts from **Architect**, cards from **Conductor**, findings from **QA**. Hands the built tree to **DevOps**. Tells **Librarian** when a new page exists so the index is true in the same release.

### Escalation

To **Architect** when a page cannot be written without inventing a field. To the **Conductor** when a card needs a decision the page cannot make.

[← All roles](../index.md) [The board →](../board.md)

Other roles: [Conductor](conductor.md) · [Architect](architect.md) · [DevOps](devops.md) · [QA](qa.md) · [Librarian](librarian.md) · [Historian](historian.md)

---

*[Site index for agents](../../llms.txt) · [HTML version](https://myfeeds.sgit.ai/team/roles/dev.html)*
