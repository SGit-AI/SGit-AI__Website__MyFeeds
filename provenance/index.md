# This site is written by an AI, and reviewed afterwards

> Not AI-assisted: the prose, both ontologies, the audience definitions and every classification were produced by a language model and are read by a human after publication rather than before. Who made what, the three places a model can be wrong here in order of damage, and what is not AI-generated.

*Source: <https://myfeeds.sgit.ai/provenance/index.html> · site v0.1.7 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Disclosure

# This site is written by an AI, and reviewed afterwards

Not "AI-assisted". The prose on every page, the two ontologies, the six audience definitions, the extraction of entities from each article and the classifications that follow from them were all produced by a language model — a Claude Code session — and are read by a human **after** publication rather than before. That is an unusual thing to put at the top of a page instead of at the bottom, and it is the only honest place for it on a site whose entire argument is that automated selection should be checkable.

## Who does what

| Part | Made by | Reviewed |
|---|---|---|
| The pages and their argument | Model | After the fact, by Dinis Cruz |
| The article and audience ontologies | Model | After the fact; the open questions are on [the review page](../review/index.md) |
| The six audience role definitions | Model | After the fact. These are the most opinionated thing here and the most worth disagreeing with |
| Entity extraction from each article | Model | Not yet. 3 articles, none reviewed |
| The join formula and its weights | Model | After the fact |
| The source articles themselves | [pt.newsroom.sgit.ai](https://pt.newsroom.sgit.ai/) | By that newsroom's named human editor of record, *before* publication |

Note the asymmetry in the last row. The Portuguese newsroom this site reads from has a named human who reads every page before it goes live. This site does not, yet. That gap is on [the board](../team/board.md) and is the single most important thing to fix before anything here runs on a schedule.

## The status on every page

Every page on this site carries one of these, at the top, under the breadcrumb:

| Status | Means |
|---|---|
| ai-generated, unreviewed | A model wrote it and nobody has checked it. Today this is every page. |
| ai-generated, human-reviewed | A model wrote it and a named person has read it and let it stand. |
| human-written | A person wrote it. |

A page moves off the default when somebody names themselves against it, which is why the generator holds a map of exceptions rather than a field that has to be remembered. An empty map is the honest state and it is currently empty.

## Why this matters more here than elsewhere

This site argues that a recommendation you cannot interrogate is worthless. A site making that argument in prose a model wrote, using an ontology the same model invented, to classify articles the same model extracted, would be an unusually pure example of the problem it describes — unless it says so, in the same place a reader forms their view of whether to trust it.

### The three places a model can be wrong here, in order of damage

1. **Extraction.** A model can name an entity the article does not contain. Everything downstream then explains, correctly and traceably, a connection that should not exist — and the provenance trail makes it *more* convincing, not less. This is the worst failure mode in the whole system and it currently has no automated guard.

2. **The audience definitions.** Six role descriptions written by a model about how real people read. They are plausible, which is exactly the problem: plausible and unchecked is how a stereotype gets encoded as a data structure. These need a practitioner, an investor and a risk owner to read their own entry and say what is wrong.

3. **The prose.** The least dangerous, because a reader can tell. A wrong sentence about how something works is visible in a way that a wrong edge in a graph is not.

## What is not AI-generated

- The [recovered MVP posts](../library/index.md) — written by Dinis Cruz in 2025 and reproduced as published.

- The source articles, which belong to the Portuguese newsroom and are linked rather than reproduced.

- The measurements in this repository: counts of pages, words, articles and connections are computed from files, not written.

[What a human is being asked →](../review/index.md) [About & honest edges →](../about/index.md) [← Home](../index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/provenance/index.html)*
