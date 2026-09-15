# Tools

> The archiver, the generator, the release gate and the live check: one file each, nothing to install, each documented in its own header.

*Source: <https://myfeeds.sgit.ai/back-office/tools/index.html> · site v0.1.4 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Runnable

# Tools

Everything needed to build, check, publish and recover, in this repository, with nothing to install beyond Python 3.11 and Node 22. Each one is a single file and each one is documented in its own header rather than here, so the documentation cannot drift from the thing it documents.

`admin/tools/wayback_archive.py`

### wayback_archive.py

Recovers a site from the Internet Archive into files you own: originals in id_ mode, a markdown rendering, and a manifest that states what the sitemap listed and no crawler ever captured.

```
python3 admin/tools/wayback_archive.py mvp.myfeeds.ai --out back-office/archive
```

`admin/build/build_pages.py`

### build_pages.py

The site generator. Every page, every markdown twin, llms.txt, the team pages from their ROLE.md files, and this back office.

```
python3 admin/build/build_pages.py
```

`admin/build/validate.js`

### validate.js

The release gate. Link resolution, twin presence, the authoring contract, status vocabulary, roster agreement, the deploy pipeline.

```
node admin/build/validate.js
```

`admin/build/verify-live.sh`

### verify-live.sh

Asks the live site what version it is serving. Green CI means GitHub accepted an artifact, not that anyone can read it.

```
./admin/build/verify-live.sh
```

## Why the archiver has a long header

Because three separate things lose content while appearing to work, and each cost a run before it was understood: the Internet Archive's `collapse=urlkey` hides good captures behind redirects; fetching without the `id_` modifier archives the Wayback Machine's rewritten copy rather than the site; and a blog's feed frequently holds writing whose own pages were never captured, so it is a primary source and not a fallback. Those are written into the tool where somebody modifying it will read them.

[← Back office](../index.md) [How this site is built →](../../admin/index.md)

---

*[Site index for agents](../../llms.txt) · [HTML version](https://myfeeds.sgit.ai/back-office/tools/index.html)*
