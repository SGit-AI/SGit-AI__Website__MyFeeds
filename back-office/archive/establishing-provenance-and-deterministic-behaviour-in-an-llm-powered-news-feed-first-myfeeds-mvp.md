# Establishing Provenance and Deterministic Behaviour in an LLM-Powered News Feed (first MyFeeds.ai MVP)

> Recovered from mvp.myfeeds.ai, published 23 Mar 2025: The first MVP of the MyFeeds.ai site shows an example of personalised cyber security news feeds based on Semantic Knowledge Graphs, which provide provenance on why each article…

*Source: <https://myfeeds.sgit.ai/back-office/archive/establishing-provenance-and-deterministic-behaviour-in-an-llm-powered-news-feed-first-myfeeds-mvp.html> · site v0.1.8 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Recovered from the archive

# Establishing Provenance and Deterministic Behaviour in an LLM-Powered News Feed (first MyFeeds.ai MVP)

**Originally**

: `https://mvp.myfeeds.ai/establishing-provenance-and-deterministic-behaviour-in-an-llm-powered-news-feed-first-myfeeds-mvp/` — the site no longer exists

**Published**

: 23 Mar 2025

**Author**

: Dinis Cruz

**Tags**

: How it works

**Recovered**

: From a capture of the site's RSS feed, which carried the full body. The markdown is at `back-office/archive/mvp.myfeeds.ai__posts/establishing-provenance-and-deterministic-behaviour-in-an-llm-powered-news-feed-first-myfeeds-mvp.md`.

This is recovered content, reproduced as it was published. Its links point at pages that in many cases no longer resolve and are left exactly as written. Its **images are served from this repository** — the originals were recovered from the same archive as the text, and each one carries the URL it came from in its title attribute, so the reference is rewritten and recorded rather than rewritten and hidden. An image the archive did not capture is marked as missing rather than left broken.

↓ recovered article begins 23 Mar 2025 · Dinis Cruz

[image never archived: `1742165370948-2-1-1.jpeg`]

The first MVP of the [MyFeeds.ai](https://mvp.myfeeds.ai/) site shows an example of personalised cyber security news feeds based on Semantic Knowledge Graphs, which provide provenance on *why* each article was chosen for each targeted persona (CEO, CISO, CTO, Board Member, etc...)

The solution pulls in content from sources like RSS feeds (in this first MVP, from [the Hacker News](https://thehackernews.com/?ref=mvp.myfeeds.ai)) and uses a series of large language model (LLM) powered steps to transform raw articles into tailored briefings for specific personas (such as a CTO or an investor), with every step of this pipeline producing structured and traceable data.

In this post, we'll explore how MyFeeds works under the hood, focusing on how it establishes **provenance** (traceable origins of information) and a degree of **deterministic behaviour** in its LLM-driven workflow.

### From RSS Feeds to Knowledge Graphs

MyFeeds begins by gathering content from RSS feeds. In this first MVP only from [the Hacker News](https://thehackernews.com/?ref=mvp.myfeeds.ai), but many more cyber security news feed will be added very soon.

Each article is then analysed semantically and converted using an LLM into a **knowledge graph** – a structured representation of the article’s key **entities** (people, organisations, technologies, etc.) and the **relationships** between them.

In other words, the system extracts the who, what, and how of the story and encodes those facts into a graph data structure. Each article yields its own graph in JSON format, capturing the essential concepts in machine-readable form.

[image · `1742165370948-2-1.jpeg`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/1742165370948-2-1.jpeg)

*Figure: A visualisation of a semantic knowledge graph generated from 50 Hacker News article titles (553 nodes, 1451 edges)​ Even with just titles and summaries, the graph forms a dense web of interconnected entities, illustrating how much structured information can be derived from raw text.*

### Persona Semantic Graphs: Tailoring to the Reader

Next, MyFeeds considers the **persona** that will read the news. A persona could be a specific individual or a role-based profile like “CTO”, “AI researcher”, or “Tech investor”.

The system uses an LLM to generate a **persona knowledge graph** which represents that persona’s domain of interest – essentially, a graph of topics and entities the persona cares about.

For example, a CTO’s persona graph might include nodes for “cloud infrastructure”, “microservices”, and “cybersecurity” to highlight key interest areas. This persona graph, also represented in JSON, serves as a semantic fingerprint of the user’s interests against which incoming article graphs can be compared.

### Mapping Articles to Personas: Finding Relevance

With an article graph and a persona graph in hand, the next step is to **map the article to the persona** and determine relevance.

An LLM at this stage compares the two graphs to find overlaps or connections. Essentially, it asks: *Which entities or themes in this article align with the persona’s interests?*

Shared topics appearing in both will be flagged as points of relevance. The output of this stage is another JSON structure that lists these connections – linking specific elements of the article to elements of the persona. Articles with significant overlap or strong semantic ties are marked as relevant to that persona, while those with little intersection are filtered out.

### Four LLM-Powered Stages of Processing

Under the hood, MyFeeds’ pipeline consists of four LLM-driven stages, each producing a structured output. These stages break down the transformation from raw text to personalised summary into clear, verifiable steps:

- Entity & Relationship Extraction (Article) – Input: an article’s text (or summary). Task: Identify the important entities and how they relate. Output: A JSON knowledge graph of the article’s content (the key people, terms, and how they connect).

- Persona Graph Construction – Input: persona information (profile or description). Task: Build a semantic graph of the persona’s interests. Output: A JSON graph representing what’s important to that persona.

- Relevance Mapping – Input: the article graph and the persona graph. Task: Find intersections or links between them. Output: A JSON description of which entities or concepts from the article align with the persona's graph (i.e. why the article is relevant).

- Personalised Summary Generation – Input: the original article content plus the relevant connections from stage 3. Task: Produce a brief summary of the article tailored to the persona, emphasising the points that match the persona’s interests. Output: A final summary text (personalised for the reader).Each stage is like a module with a well-defined input and output, keeping the LLM workflow controlled and interpretable rather than one big black box.

### Structured Outputs: Traceability and Determinism

A standout feature of MyFeeds is that every LLM stage outputs a structured JSON file rather than free-form text. This design brings **traceability** and a measure of **determinism** to the workflow that typical LLM pipelines lack:

- Traceability & Explainability: Since intermediate results are captured as JSON, the system keeps a step-by-step record of its reasoning. The chain of outputs forms a provenance trail that shows why a particular article was recommended to a persona. If someone asks “Why am I seeing this?”, we can point to the evidence – e.g., “The article mentions GraphQL, and your persona profile lists GraphQL as an interest, so it was flagged.” Every recommendation can thus be explained by tracing those intermediate entities and links, turning an opaque decision into an open, auditable one.

- Consistency & Control: While LLMs are probabilistic, having them fill out predefined JSON schemas at each step makes their behaviour more predictable. The model isn’t just generating text; it’s populating specific fields. This yields more consistent outputs and reduces variability. Structured outputs let us retrieve information from an LLM in a more deterministic way​. Moreover, the strict format allows automatic validation at each step – if the JSON is malformed or missing expected elements, the system knows something went wrong and can flag or fix it. The end result is a pipeline that behaves reliably given the same inputs, and clearly surfaces any errors.

### Conclusion

MyFeeds MVP showcases a novel approach to AI-driven content personalisation by combining knowledge graphs with multi-stage LLM processing.

By making each step transparent and capturing its output as data, the system makes it possible to understand and trust why a specific article is shown to a given persona. The intermediate entities and relationships form a verifiable provenance trail that engineers and end-users alike can inspect, proving that we don't have to treat AI models as inscrutable black boxes.

In essence, MyFeeds demonstrates that an AI system can be both smart *and* accountable—providing tailored news with a clear explanation of *why* each item was selected.

In an era of black-box AI, MyFeeds’ focus on determinism and provenance, shows that we can have powerful LLM-driven solutions without sacrificing transparency or trust.

And here is what this first MVP looked like:

[image · `Screenshot-2025-03-23-at-01.28.45-4-1.png`](../../back-office/archive/mvp.myfeeds.ai/content/images/2025/03/Screenshot-2025-03-23-at-01.28.45-4-1.png)

---

*by Dinis Cruz and ChatGPT Deep Research*

↑ recovered article ends this site's words resume

[← All recovered posts](index.md) [Back office →](../index.md)

---

*[Site index for agents](../../llms.txt) · [HTML version](https://myfeeds.sgit.ai/back-office/archive/establishing-provenance-and-deterministic-behaviour-in-an-llm-powered-news-feed-first-myfeeds-mvp.html)*
