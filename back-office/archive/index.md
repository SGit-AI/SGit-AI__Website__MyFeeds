# The mvp.myfeeds.ai archive

> The first MyFeeds MVP recovered from the Internet Archive: the posts that survived, mostly inside a single capture of the RSS feed, and the nine URLs its own sitemap named that no crawler ever caught.

*Source: <https://myfeeds.sgit.ai/back-office/archive/index.html> · site v0.1.5 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Recovered

# The mvp.myfeeds.ai archive

mvp.myfeeds.ai was the first MyFeeds MVP: a Ghost blog publishing machine-generated cybersecurity briefings, one per persona, alongside the long-form posts explaining how they were built. The site is gone. 15 of its posts — 13,527 words — are here, recovered from the Internet Archive and now kept as files rather than as somebody else's cache.

**Most of this survived in the feed, not the pages.** The crawler captured 22 files, of which only eight were post pages. What saved the long-form writing was a single capture of `/rss/` on 31 August 2025: a Ghost feed carries the full body of its recent posts in `content:encoded`, so one 224 KB XML file held articles whose own pages were never archived. If that one request had failed, this page would be mostly a list of what used to exist.

## The posts

Two kinds, and the difference matters. The **How it works** posts are Dinis Cruz explaining the architecture — they are the argument. The persona posts are *output*: briefings the pipeline generated for a CEO, a CISO, a CTO and two kinds of board member, which makes them evidence that the thing ran.

| Tag | Posts | Words |
|---|---|---|
| **How it works** | 4 | 5,728 |
| **CISO** | 3 | 2,224 |
| **CTO** | 3 | 1,729 |
| **CEO** | 3 | 1,995 |
| **Board Member (Public)** | 1 | 870 |
| **Board Member (Private)** | 1 | 981 |

- [15 Apr 2025 · 857 words — for CISOs | 19-26 March 2025 — CISO](for-cisos-19-26-march-2025.md)

- [15 Apr 2025 · 582 words — for CTOs | 19-26 March 2025 — CTO](for-ceos-19-26-march-2025-2.md)

- [15 Apr 2025 · 882 words — for CEOs | 19-26 March 2025 — CEO](for-ceos-19-26-march-2025.md)

- [15 Apr 2025 · 870 words — for Board Member (Public) — Board Member (Public)](for-board-member-public.md)

- [15 Apr 2025 · 981 words — for Board Member (Private) — Board Member (Private)](for-board-member-private.md)

- [26 Mar 2025 · 1,037 words — How I'm Building Personalised News Feeds with Semantic Graphs - Part 1 — How it works](publishing-a-new-personalised-set-of-posts-part-1.md)

- [26 Mar 2025 · 1,551 words — How I'm Building Personalised News Feeds with Semantic Graphs - Part 2 — How it works](how-im-building-personalised-news-feeds-with-semantic-graphs-part-2.md)

- [24 Mar 2025 · 2,019 words — Building Semantic Knowledge Graphs with LLMs: Inside MyFeeds.ai's Multi-Phase Architecture — How it works](building-semantic-knowledge-graphs-with-llms-inside-myfeeds-ais-multi-phase-architecture.md)

- [23 Mar 2025 · 1,121 words — Establishing Provenance and Deterministic Behaviour in an LLM-Powered News Feed (first MyFeeds.ai MVP) — How it works](establishing-provenance-and-deterministic-behaviour-in-an-llm-powered-news-feed-first-myfeeds-mvp.md)

- [20 Mar 2025 · 539 words — CTO (19 Mar) — CTO](cto-19-mar.md)

- [20 Mar 2025 · 706 words — CISO (19 Mar) — CISO](ciso-19-mar-2.md)

- [20 Mar 2025 · 532 words — CEO (19 Mar) — CEO](ceo-19-feb.md)

- [19 Mar 2025 · 608 words — CTO New (Feb 2025) — CTO](cybersecurity-news-for-persona-exec-cto-on-feb-2025.md)

- [19 Mar 2025 · 661 words — CISO News (Feb 2025) — CISO](cybersecurity-news-for-persona-exec-ciso-on-feb-2025.md)

- [19 Mar 2025 · 581 words — CEO (Feb 2025) — CEO](cybersecurity-news-for-persona-exec-ceo-on-feb-2025.md)

## What could not be recovered

9 URLs appear in the site's own sitemap and in no capture anywhere. They are not missing from this page because nobody looked; they are gone.

- `https://mvp.myfeeds.ai/about/`

- `https://mvp.myfeeds.ai/author/athena/`

- `https://mvp.myfeeds.ai/author/dinis/`

- `https://mvp.myfeeds.ai/ceo-news/`

- `https://mvp.myfeeds.ai/tag/board-member-private/`

- `https://mvp.myfeeds.ai/tag/board-member-public/`

- `https://mvp.myfeeds.ai/tag/ceo/`

- `https://mvp.myfeeds.ai/tag/ciso/`

- `https://mvp.myfeeds.ai/tag/cto/`

Two of them are author pages and five are tag listings, which are indexes rather than writing — their contents are largely reconstructable from the posts that survived. `/about/` and `/ceo-news/` are not: whatever they said is lost unless a copy exists somewhere outside the archive.

## How it was recovered

With [`admin/tools/wayback_archive.py`](../tools/index.md), in this repository, which you can run against any domain. The three things that cost content, each of which loses it silently rather than erroring, are written up in that tool's own documentation — the worst is that the Internet Archive's `collapse=urlkey` option merges `http://host/x` with `https://host/x/` and keeps whichever sorts first, which on this domain was a redirect. A collapsed query reports `/tag/how-it-works/` as not existing. It exists, it was captured, and it is [here](../../back-office/archive/index.md).

The manifest — every file, the capture it came from, and its Wayback URL — is at `back-office/archive/mvp.myfeeds.ai__manifest.json`.

[← Back office](../index.md) [The tools →](../tools/index.md)

---

*[Site index for agents](../../llms.txt) · [HTML version](https://myfeeds.sgit.ai/back-office/archive/index.html)*
