# How it works

> The four-stage pipeline: entity extraction, persona graph, relevance mapping, personalised summary — each emitting typed JSON, with a semantic knowledge graph where the reasoning used to be hidden. Assembled from the posts that described it as it was built.

*Source: <https://myfeeds.sgit.ai/how-it-works/index.html> · site v0.1.5 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

The architecture

# How it works

Four LLM stages with a semantic knowledge graph between them, each stage emitting typed JSON rather than prose. This page is assembled from the posts that described it while it was being built — all of which are [recovered in the back office](../back-office/archive/index.md), because the site they were published on no longer exists.

## What was tried first, and why it failed

The obvious approach: convert the RSS feed into a prompt-friendly block of text, append a description of the persona, append a description of the wanted output, send one call, get a digest back. It works. That is the trap.

> Although this kinda works, when using the 50x RSS articles and asking the LLM to pick the most relevant 5x, I had a large number of very important problems, challenges and concerns — which, by the way, are the same ones faced by the companies and services that have been trying to create personalised news feeds, with limited success.

That is from [Building Semantic Knowledge Graphs with LLMs](../back-office/archive/building-semantic-knowledge-graphs-with-llms-inside-myfeeds-ais-multi-phase-architecture.md), March 2025. The four concerns it lists — explainability, provenance, determinism, and an LLM doing too much in one step — are the design brief for everything below.

## The four stages

Each stage is a module with a defined input and output, which is what keeps the workflow interpretable rather than being one big black box.

| # | Stage | In | Out |
|---|---|---|---|
| 1 | **Entity & relationship extraction** | An article's text or title | A JSON knowledge graph of the article: the key entities and how they connect |
| 2 | **Persona graph construction** | A persona profile | A JSON graph of what matters to that persona |
| 3 | **Relevance mapping** | Both graphs | A JSON description of which entities and concepts intersect — *why* this article is relevant to this person |
| 4 | **Personalised summary** | The original article plus stage 3's connections | A summary written for that persona, emphasising what actually matched |

Stage 3 is the one that earns the whole design. In the single-call version, "the model picked it" is the entire explanation and there is nothing underneath. Here, the selection is a join between two graphs, and the join is a file.

## Structured outputs are what make it inspectable

Every stage returns a populated schema rather than free text — Python classes handed to the model as the shape its response must take, so what comes back is typed objects rather than prose to be parsed. Two things follow, and both are properties the single call does not have:

- **Traceability.** The intermediate JSON is a step-by-step record. Asked "why am I seeing this?", the answer is a row: the article mentions GraphQL, the persona graph lists GraphQL, so it was flagged. That is evidence, not a generated justification — and a generated justification is exactly what a black-box system offers instead.

- **Consistency and control.** A model filling in predefined fields is more predictable than one writing paragraphs, and a malformed or incomplete response is detectable rather than plausible. The pipeline can tell that something went wrong, which a prose-generating pipeline fundamentally cannot.

**Determinism, stated precisely.** The claim is not that an LLM is deterministic — it is not. The claim is that constraining each stage to a schema, and capturing every intermediate, makes the behaviour repeatable enough to be checked and the failures visible enough to be caught. The recovered post's own words are "a measure of determinism", and that is the honest size of it.

## Why a graph, and not just a longer prompt

Because the graph is the thing you can merge, inspect, visualise and reuse. Article graphs are built per article and merged; the persona graph is built once and compared against many. The project used [MGraph-DB](https://github.com/owasp-sbot/MGraph-DB), a memory-first graph database built for exactly this kind of serverless, LLM-adjacent work, and rendered the graphs as DOT/Graphviz — not for decoration, but because, in the author's words, without the visualisation he could not see what the graphs actually looked like.

The subtle part is feeding a graph *back* to a model. Sending raw JSON or an image of a graph is expensive and invites hallucination, so the graph is exported as a compressed tree-shaped text representation that preserves nodes and edges while staying small. How you talk to the model is a design decision in its own right, and this is the one that made stage 3 work.

## The personas are the product

The MVP published for five: a CEO, a CISO, a CTO, and board members of private and public companies. They are not five prompt variations — each is a graph, and the same article reaches each of them with a different summary and a different reason, or does not reach them at all.

The output is in [the archive](../back-office/archive/index.md#posts), so the claim is checkable rather than asserted: those briefings are what the pipeline produced, on real articles, on named dates.

## Where the code is

The engine is public and open source at [the-cyber-boardroom/myfeeds-ai](https://github.com/the-cyber-boardroom/myfeeds-ai) — the RSS ingestion, the persona definitions, the graph building, the prompts for each stage, the pipelines that run them. The recovered posts link directly to individual prompt files and schema classes at the commits they were written against, which is a better artefact than any diagram: the argument and the line of code it describes, side by side.

[The recovered posts →](../back-office/archive/index.md) [Documents →](../back-office/documents/index.md) [← Home](../index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/how-it-works/index.html)*
