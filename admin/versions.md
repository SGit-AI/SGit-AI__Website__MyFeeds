# Release history

> Every release of this site: version, date, and what it did — including what an earlier version got wrong, where one did.

*Source: <https://myfeeds.sgit.ai/admin/versions.html> · site v0.1.1 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Provenance

# Release history

Every release of this site: the version, the date, what it did, and what an earlier version got wrong where one did. A version log that reads as an unbroken sequence of improvements is a version log that is lying.

Each entry is also served as data at `/versions/<version>.json`, indexed by [`/versions/index.json`](../versions/index.json), so a script can check a claim about a release without rendering a page. The version badge in the navigation links to the entry for the version you are looking at, not to this page generally.

`v0.1.1` · 2026-09-14 · [as data](../versions/v0.1.1.json)

### the site gets the deploy workflow every other *.sgit.ai site has, and the four version and provenance practices it was missing

v0.1.0 shipped a build gate and called it done, which was wrong: it never published anything. This release replaces it with the estate's shared deploy-pages pipeline (validate, tag, publish to GitHub Pages) taken from the sibling sites rather than reinvented, moves version ownership to admin/build/version.txt so that workflow can read it, and closes four gaps against sgit.ai/docs/guidance: the version badge is now a link to that version's own details, versions are served as data, app.json denies by default with its reason written down, and every page is one click from the bytes it was rendered from.

**Corrects.** v0.1.0 described a four-step release ending in a live check, and shipped neither a deploy workflow nor anything to check with. The description was accurate about the intent and wrong about the repository.

#### Changes

- .github/workflows/deploy-pages.yml — replaces build.yml; validate -> tag -> deploy, matching SGit-AI__Website__Teams

- admin/build/version.txt — now owns the version; build_pages.py reads it

- admin/build/verify-live.sh — asks the live site what it is serving, because both remotes in sync is not the same as deployed

- versions/index.json + versions/<version>.json — the versions contract

- admin/build/build_pages.py — version badge links to its own entry; every page links its markdown twin; app.json declares permissions {}

- admin/build/validate.js — assertions for each of the above

`v0.1.0` · 2026-09-14 · [as data](../versions/v0.1.0.json)

### the argument, the read-state contract, and the team that runs it

First release. The thesis that feeds are replaceable and reading is not, read-state/v1 published as a contract before any implementation, the vault layout, the build order, and the seven-role dev team the site is run by — generated from the ROLE.md files rather than described beside them. Nothing is served yet: the subdomain does not resolve (board card 004).

#### Changes

- admin/build/build_pages.py — the generator: one shell, 19 pages, twins, llms.txt, llms-full.txt, sitemap.xml, data/team.json

- admin/build/validate.js — the gate

- admin/content/ — the eight authored page bodies and pages.json

- team/roles/*/ROLE.md — seven roles; team/board/*.md — five cards

- assets/site.css, assets/site.js

The log lives in `VERSION_LOG` in `admin/build/build_pages.py` and is owned by the [Historian](../team/roles/historian.md); the version number itself is owned by `admin/build/version.txt`, because that is the file the deploy workflow shared across the [*.sgit.ai sites](../network/index.md) reads. The version in the navigation, the entry here, and the version the live site serves have to agree — [DevOps](../team/roles/devops.md) exists because on two occasions elsewhere in this estate the first two agreed and the third did not.

[← How this site is built](index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/admin/versions.html)*
