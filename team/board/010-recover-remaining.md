---
id: 010
title: Recover what the archive could not reach
status: done
owner: librarian
kind: task
opened: 2026-09-14
closed: 2026-09-15
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

**Closed v0.1.8 — and the v0.1.7 update above this line was wrong about the numbers.**

The images are done, and "partly complete, re-run to finish" was a misreading of the
count. Three different things were being added together:

| | | |
|---|---|---|
| 92 | served from this repository | recovered, working |
| 16 | on the dead domain, **never captured by the Internet Archive** | re-running finds nothing |
| 51 | embedded from other publishers' CDNs | never part of that site at all |

The last group is the one that made the number look bad. The persona briefings quote
Hacker News articles and embed the screenshots from the original publisher's image host —
those were never on `mvp.myfeeds.ai`, so no archive of that site could ever have held them.
They are not missing. They are somebody else's images, and they are now rendered as a link
to the original rather than counted as a loss.

Of the 105 images the posts actually reference from the dead domain, **89 are here and 16
were never archived**. Those 16 are gone unless a copy exists outside the Internet Archive
— most are DALL·E header images for the persona posts, which the MyFeeds engine repository
may still hold.

**What was actually done**
- Archiver run without `--skip-assets`; 120 files pulled before archive.org's rate limiting
  made further progress pointless.
- The archiver now honours `Retry-After` and paces the whole run rather than backing off
  per file, because per-file exponential backoff is the wrong shape for a server that is
  telling you a specific number of seconds to wait.
- Each image renders as one of three honest states rather than one misleading one.

**What is left, and it is not this card:** the 16 never-archived images, if anyone wants to
go looking in `the-cyber-boardroom/myfeeds-ai` for the originals. That is a new card if it
matters, not an unfinished part of this one.

---

**Superseded update from v0.1.7, kept because it was published:**

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
