---
id: 011
title: The daily routine that syncs this site with pt.newsroom.sgit.ai
status: todo
owner: devops
kind: task
opened: 2026-09-15
---

The end state, in the author's words: a daily Claude Code routine that synchronises
myfeeds.sgit.ai with `pt.newsroom.sgit.ai`, which itself has agents running on its own
interval. A self-maintaining workflow, where this site's job is to take what that newsroom
published and put it in front of six audiences with the reasoning attached.

**Why this is a task and not a need.** Everything it depends on now exists: the audiences
are defined, the ontology is published, `admin/tools/join.py` runs the formula, and the
newsroom publishes its articles as JSON with claims and frozen sources. What is missing is
the loop and the extraction step, not a decision.

## The shape

```
daily, on a Routine:
  1. pull      pt.newsroom.sgit.ai's published articles (its api/v1 or the repo)
  2. diff      against admin/content/data/articles/ — new and changed only
  3. extract   article -> entities + edges, against the published article ontology
               (stage 1; the only step that needs a model and the only one that can
               invent something, so its output is reviewed before it is used)
  4. translate the faithful EN rendering — the control audience, no selection
  5. join      python3 admin/tools/join.py per article -> data/joins/<slug>.json
  6. write     one output per reached audience, in that audience's currency
  7. build     python3 admin/build/build_pages.py && node admin/build/validate.js
  8. release   bump version.txt, commit "site vX.Y.Z: ...", push dev; CI deploys
```

## What has to be true before it runs unattended

- **Step 3 is the dangerous one.** Extraction is where a model can name an entity the
  article does not contain, and everything downstream will then explain a connection that
  should not exist. The build already refuses an entity whose type is not in the ontology;
  it cannot refuse an entity that is well-typed and wrong. Until there is a check for that,
  a human reads the extraction diff.
- **The newsroom's rule is inherited, not re-implemented.** Every claim there walks back to
  a frozen, hashed source. This site must carry those markers through to the audience
  outputs rather than dropping them in the rewrite — an audience-specific piece with no
  path back to the frozen bytes is exactly the black box this site argues against.
- **Translation is a claim.** The EN control output is a transcription of somebody else's
  words and is checkable as one. Divergences between it and the five re-framed outputs are
  the site's own evidence that re-framing is not distortion, so it has to be right first.
- **The loop needs a stop.** A routine that publishes daily without anyone reading it will
  eventually publish something wrong with full confidence and a provenance trail. The
  newsroom has a named human editor of record as the gate; this site should say who holds
  the equivalent before the routine is armed, not after.

**Done when** a scheduled Routine runs the eight steps end to end on one day's articles,
the release it cuts passes CI, `verify-live.sh` confirms it, and the run record says which
articles were extracted, which audiences each reached, and what a human changed.
