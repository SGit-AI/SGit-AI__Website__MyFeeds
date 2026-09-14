---
id: 009
title: Build the multi-audience demo over a live newsroom
status: need
owner: architect
kind: need
opened: 2026-09-14
---

From the author's voice memo of 14 September 2026, recorded here so the intent does not
live only in a transcript.

The ask: a MyFeeds-published version of an existing news site, cut for several audiences
rather than one — **startups, investors, and corporate executives**, with the executive
audience splitting further into C-level, cybersecurity, and risk. Roughly five views.
Portuguese first, English second, since the pipeline can do both and the source newsroom
is Portuguese (`pt.newsroom.sk.ai`, with other sources to follow).

The shape is two sites, not one:

- a **generic** MyFeeds site explaining the concepts and principles — which is what
  myfeeds.sgit.ai now is; and
- a **worked example** that runs the argument on real news: the graphs from the source
  articles, the ontology of each target audience, and the join between them rendered as
  the output. "Connect the dots, and that's what you see on the website."

**Why this is a need rather than a task.** It requires a running pipeline against a live
source, which is an engineering project in `myfeeds-ai`, not a page in this repository.
What this site can do without it is publish the contract the demo would have to meet — the
audience ontologies and what a view is — which is item 1 below and *is* a task once the
audiences are settled.

**Open questions the author has to settle before anything is built**
1. Are the five audiences final, and is there a written ontology for each, or is deriving
   them from the existing persona definitions part of the work?
2. Does the demo publish as its own site, a section of this one, or back into the source
   newsroom?
3. Portuguese first — does this site become bilingual, or does the demo carry the
   Portuguese and this site stay English?

**Done when** those three are answered and the contract for an audience view is published
here, before the demo exists. That is this estate's order of work and the reason the
commitments stay checkable.
