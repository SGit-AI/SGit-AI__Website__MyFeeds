# Release history

> Every release of this site: version, date, and what it did — including what an earlier version got wrong, where one did.

*Source: <https://myfeeds.sgit.ai/admin/versions.html> · site v0.1.2 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Provenance

# Release history

Every release of this site: the version, the date, what it did, and what an earlier version got wrong where one did. A version log that reads as an unbroken sequence of improvements is a version log that is lying.

Each entry is also served as data at `/versions/<version>.json`, indexed by [`/versions/index.json`](../versions/index.json), so a script can check a claim about a release without rendering a page. The version badge in the navigation links to the entry for the version you are looking at, not to this page generally.

`v0.1.2` · 2026-09-14 · [as data](../versions/v0.1.2.json)

### the site went live, so the three pages that said it had not are corrected above the claims rather than instead of them

v0.1.1 shipped the deploy workflow and said, in its own release note, that it made the site deployable rather than deployed. It deployed it. Switching GitHub Pages on for this repository — which is what the new deploy job does with actions/configure-pages and the CNAME file — was the missing step, and the certificate that had never been issued for the host was issued within minutes. verify-live.sh reports myfeeds.sgit.ai serving v0.1.1. This release corrects every page that claimed otherwise, closes board card 004 with what actually blocked it, and records one bookkeeping gap the deploy left behind.

**Corrects.** v0.1.1's release note ends 'this release makes the site deployable; it does not make it deployed', and v0.1.0's says nothing is served yet. The first was wrong within ten minutes of being written — the deploy job it added is precisely what made the site deployed. Both entries stay as written; this is the correction above them.

#### Changes

- team/board/004-domain.md — closed: the subdomain was never the blocker, the missing deploy workflow was. The need was not a need

- team/board/008-v010-tag.md — held: v0.1.0 has no tag on the remote, because its tree carries the workflow file this release replaced and neither GITHUB_TOKEN nor the session credential may push such a ref (HTTP 403)

- admin/content/about/index.html — the honest-edges row for 'live' flips, and says what it used to say

- admin/content/network/index.html — the 'a site that serves nothing' sentence is corrected in place, with the old wording quoted

- admin/content/index.html — the status table records where the site is served

- admin/build/build_pages.py — the version badge anchor no longer breaks across a line mid-tag

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
