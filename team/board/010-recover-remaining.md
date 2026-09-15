---
id: 010
title: Recover what the archive could not reach
status: doing
owner: librarian
kind: task
opened: 2026-09-14
---

`admin/tools/wayback_archive.py` recovered 15 posts and 22 files from `mvp.myfeeds.ai` and
recorded 9 URLs that its own sitemap named and no crawler ever captured. Two of those are
writing rather than an index and are therefore genuinely lost from that source:
`/about/` and `/ceo-news/`.

They may exist elsewhere. Places to look, in order of likelihood:

- the Ghost export or database backup, if one was kept;
- `the-cyber-boardroom/myfeeds-ai`, which generated the persona posts and may hold the
  source of the pages too;
- LinkedIn, where several of these posts were cross-published — the recovered HTML carries
  `?trk=article-ssr-frontend-pulse` parameters, which is evidence they were syndicated
  there;
- a second archive (archive.today, Bing or Google cache) that the Internet Archive's
  index does not cover.

Also outstanding: the run used `--skip-assets`, so the **361 captured images are indexed
in the manifest but not downloaded**. Every recovered post references images on the dead
domain, so those links are currently decorative. Re-run without the flag to pull them, and
decide separately whether to rewrite the posts to point at local copies — which makes them
readable but stops them being verbatim.

**Done when** the two lost pages are either found or declared unrecoverable with the
places checked listed, and the image question is decided either way on this card.

---

**Update, v0.1.7 — images: partially done, and the finish is a re-run.**

The run used `--skip-assets`, so no images had been downloaded at all and every recovered
post rendered a column of markdown source. Both halves are now fixed: the archiver was run
without the flag, and the renderer was taught image syntax (see the release note — it had
never handled `![](url)`, because the inline link rule required non-empty link text).

At the time of this release the Internet Archive is throttling and the download is **partly
complete**. The exact split is printed by the validator on every build — look for the
`recovered images:` note — and shown on each post as an explicit "image not recovered"
marker rather than a broken image, so the gap is visible rather than inferred.

**To finish it:** re-run the same command. The archiver skips files already present, so it
resumes rather than restarting.

```
python3 admin/tools/wayback_archive.py mvp.myfeeds.ai --out back-office/archive --delay 0.25
python3 admin/build/build_pages.py && node admin/build/validate.js
```

**Decided:** the images are served from this repository and the original URL is kept in each
image's `title`. The earlier position — leave references pointing at the dead domain so the
archive stays verbatim — was wrong in practice: it produced an archive nobody could read.
Rewriting a reference and recording it is evidence; rewriting and hiding it is not.
