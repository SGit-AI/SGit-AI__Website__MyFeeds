---
id: 010
title: Recover what the archive could not reach
status: todo
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
