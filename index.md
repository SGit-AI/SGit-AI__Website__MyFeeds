# myfeeds.sgit.ai

> Ask one LLM to read fifty articles and pick five for a CISO and it will — and you will never be able to say why. How MyFeeds decomposes that single opaque call into four stages with a semantic knowledge graph between them, so every recommendation carries a provenance trail you can inspect.

*Source: <https://myfeeds.sgit.ai/index.html> · site v0.1.8 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Personalised news, without the black box

# The LLM was doing too much.

Take fifty cybersecurity articles, describe a CEO, and ask a language model to pick the five that matter. It will. The output is plausible, often good, and completely unaccountable — you cannot say why those five, you cannot trace a claim back to its source, and you will not get the same answer twice. That is the failure mode every personalised-feed product has shipped into, and it is the one MyFeeds was built to avoid.

If you cannot answer "why am I seeing this?", you have not built a feed. You have built a slot machine with good taste.

## The diagnosis

The first attempt was the obvious one: one prompt containing the whole RSS feed, a description of the persona, and a description of the wanted output. It worked well enough to be tempting, and it failed on four counts at once — recorded at the time, in [the post that worked it out](back-office/archive/building-semantic-knowledge-graphs-with-llms-inside-myfeeds-ais-multi-phase-architecture.md):

| Problem | The question you cannot answer |
|---|---|
| **Explainability** | How were *those* five articles selected, exactly? |
| **Provenance** | Which source does this specific fact come from? |
| **Determinism** | Will the same input produce the same output tomorrow? |
| **Scope** | What did the model actually do in there? It did everything, in one step, where nobody can look. |

The last one is the cause of the other three, and it is the sentence this site is named after: **the LLM is doing too much**. Not wrong — too much, in one step, with no surface to inspect.

## The fix is a graph between the stages

Split the single call into four, each with a typed, structured output, and put a semantic knowledge graph where the reasoning used to be hidden:

Stage 1

### Extract the article

Article text in; a JSON knowledge graph of its entities and their relationships out. What this article is *about*, as data.

Stage 2

### Build the persona

A persona profile in; a graph of what that person cares about out. A CISO and a board member are different graphs, not different prompts.

Stage 3

### Map relevance

Both graphs in; out comes a JSON description of *which* entities overlap. This is the step that replaces "the model picked it".

Stage 4

### Write the summary

The article plus the connections from stage 3 in; a summary written for that persona out, emphasising the points that actually matched.

Every stage emits structured JSON rather than prose, which is what buys back the three properties the single call destroyed. The intermediate files *are* the provenance trail: "the article mentions GraphQL, your persona lists GraphQL as an interest, so it was flagged" is not a generated explanation, it is a row you can point at.

### What this costs, honestly

Four LLM calls where there was one, a graph database in the middle, and a schema to maintain for every stage. You do not do this because it is cheaper. You do it because a security executive asking "why is this in my briefing?" deserves an answer that is not "the model thought so" — and because, in a regulated setting, that answer has to survive somebody checking it.

## Where this stands

MyFeeds ran. The MVP published machine-generated briefings for five personas — CEO, CISO, CTO, and board members of private and public companies — from the Hacker News RSS feed, and wrote up how it did it. Then the site went down. The writing survived mostly inside a single capture of its RSS feed, and it is [recovered here](back-office/archive/index.md).

| Thing | Status | Where |
|---|---|---|
| The argument and the architecture | shipped | [/how-it-works/](how-it-works/index.md), and the recovered posts it is built from |
| The first MVP's output — five personas, real briefings | shipped | [the archive](back-office/archive/index.md) — it ran, and this is what it produced |
| The engine that produced them | shipped | [the-cyber-boardroom/myfeeds-ai](https://github.com/the-cyber-boardroom/myfeeds-ai) — public and open source |
| The business case | shipped | [documents](back-office/documents/index.md), and [investor.myfeeds.ai](https://investor.myfeeds.ai/) |
| A live feed anyone can subscribe to | not yet | The MVP is offline. What exists is the record of it having worked. |

- [The architecture — How it works — The four stages in detail, the structured outputs that make them inspectable, and why a graph rather than a longer prompt.](how-it-works/index.md)

- [Recovered — The first MVP — Fifteen posts, pulled back out of the Internet Archive — the architecture write-ups and the briefings the pipeline actually generated.](back-office/archive/index.md)

- [The working material — Back office — Documents, tools and every previous version — indexed from what is on disk rather than maintained by hand.](back-office/index.md)

- [How this is run — The team — Seven agent roles as files, each with the failure condition it is judged on.](team/index.md)

**This site changed its mind, in public.** Versions v0.1.0 to v0.1.2 argued something else entirely — that the valuable part of a feed reader is the record of what you read, and that it belongs in an encrypted vault. That was written before any of the MyFeeds source material was available, and it is not what MyFeeds is. Those pages are still here, marked, starting at [the superseded thesis](thesis/index.md): the correction goes above the mistake, and the mistake stays.

[How it works →](how-it-works/index.md) [The recovered MVP →](back-office/archive/index.md) [llms.txt](llms.txt)

---

*[Site index for agents](llms.txt) · [HTML version](https://myfeeds.sgit.ai/index.html)*
