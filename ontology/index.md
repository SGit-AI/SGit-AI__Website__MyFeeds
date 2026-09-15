# Two ontologies and the join between them

> One ontology for what an article contains, one for what a role watches for, and the published formula where they meet. Every verb has a named inverse and reads as a sentence both ways; the verbs that are banned are listed with the reason.

*Source: <https://myfeeds.sgit.ai/ontology/index.html> · site v0.1.5 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

The grammar

# Two ontologies and the join between them

One ontology says what a piece of news contains. Another says what a role watches for. Neither is interesting on its own — the whole value is in the third thing, the join, which is where an article meets an audience and a sentence comes out saying why. The grammar is adapted from the one [pt.newsroom.sgit.ai](https://pt.newsroom.sgit.ai/) uses for the Portuguese graph, and keeps its hardest rule.

## The rules

### Every edge is a verb with a distinct named inverse, and both directions read as sentences.

An edge you cannot read aloud in both directions is usually two different claims wearing one label.

### No symmetric verb. Where a relation genuinely is symmetric, reify it as a node.

A symmetric verb is its own inverse, which means it carries no direction and therefore no information. `contradicts` is the case that matters here: two sources disagreeing is a Discrepancy node, which can then be dated, sourced and pointed at.

### Classification is a published formula or it does not happen.

The entire argument of this site is that a recommendation must be checkable. A selection rule nobody can read is the black box in a different coat.

### An article NOT reaching an audience is recorded with the same structure as one that does.

Any system can explain what it chose. Explaining what it rejected, and why, is the harder half and the one a reader actually doubts.

## The article ontology

What a piece of news contains. Deliberately small: a type earns its place by being something at least one audience watches for, and every type here is named in at least one concern.

| Type | Is |
|---|---|
| `Article` | One published piece, in its original language. |
| `Claim` | A single assertion the article makes, which walks back to a frozen source. |
| `Source` | A frozen, hashed copy of the page a claim rests on. Evidence, not a page of this site. |
| `Organisation` | A named company, institution or body. |
| `Person` | A named individual, in a professional capacity only. |
| `Event` | A dated, located happening: a conference, a deadline, an incident. |
| `Programme` | A funding call, accelerator or scheme somebody can apply to. |
| `Instrument` | A law, regulation, designation or formal decision. |
| `Obligation` | A duty an instrument creates, and who it binds. |
| `Technology` | A named product, protocol, model or version. |
| `Weakness` | A way something fails or can be made to fail. |
| `Control` | A change to a system that reduces a weakness. |
| `Sector` | A population of organisations treated as one. |
| `Measure` | A count or rate, with the thing it counts and the date it was true. |
| `Money` | An amount, with what it was for. |
| `Discrepancy` | Two sources answering the same question differently. A node, not an edge, so it can be dated and pointed at. |

### Its verbs

| Verb | Inverse | Reads | And back |
|---|---|---|---|
| `states` | `is_stated_by` | Article states Claim | Claim is stated by Article |
| `rests_on` | `supports` | Claim rests on Source | Source supports Claim |
| `names` | `is_named_in` | Claim names Organisation | Organisation is named in Claim |
| `organises` | `is_organised_by` | Organisation organises Event | Event is organised by Organisation |
| `runs` | `is_run_by` | Organisation runs Programme | Programme is run by Organisation |
| `imposes` | `is_imposed_by` | Instrument imposes Obligation | Obligation is imposed by Instrument |
| `binds` | `is_bound_by` | Obligation binds Organisation | Organisation is bound by Obligation |
| `affects` | `is_affected_by` | Weakness affects Technology | Technology is affected by Weakness |
| `reduces` | `is_reduced_by` | Control reduces Weakness | Weakness is reduced by Control |
| `belongs_to` | `contains` | Organisation belongs to Sector | Sector contains Organisation |
| `counts` | `is_counted_by` | Measure counts Sector | Sector is counted by Measure |
| `reveals` | `is_revealed_by` | Article reveals Discrepancy | Discrepancy is revealed by Article |
| `involves` | `is_involved_in` | Discrepancy involves Source | Source is involved in Discrepancy |

### Verbs that are not allowed

Naming what is banned, and why, is more useful than naming what is permitted: every one of these is a shortcut somebody will reach for.

| Verb | Why not |
|---|---|
| `contradicts` | Symmetric: A contradicts B is B contradicts A, so it is its own inverse and carries no direction. Use a Discrepancy node, which can also be dated and sourced. |
| `related_to` | Says nothing a reader could check, and absorbs every edge that was too much trouble to name properly. |
| `mentions` | True of almost every pair and therefore useless for selection. If it matters, the specific verb exists. |
| `is_relevant_to` | This is the conclusion, not an edge. Writing it as an edge hides the reasoning the join exists to expose. |

## The audience ontology

What a role watches for. Small on purpose: the audience side is the half a human maintains by hand, and a taxonomy nobody can hold in their head stops being maintained and starts being wrong.

| Type | Is |
|---|---|
| `Audience` | One of the six roles this site publishes for. |
| `Concern` | A thing an audience watches for, declared as the article types that satisfy it. |
| `Currency` | What this audience converts a piece of news into. The reason two audiences given the same article produce different pieces rather than different lengths. |
| `Axis` | A named spectrum audiences sit on: mechanism wanted, scope, horizon. |
| `Qualifier` | A type that must ALSO be present in the article for a concern to fire. The difference between 'this audience cares about source integrity' and 'this audience cares about source integrity in technical material'. |

| Verb | Inverse | Reads | And back |
|---|---|---|---|
| `watches` | `is_watched_by` | Audience watches Concern | Concern is watched by Audience |
| `pays_in` | `is_currency_of` | Audience pays in Currency | Currency is the currency of Audience |
| `satisfied_by` | `satisfies` | Concern is satisfied by Article type | Article type satisfies Concern |
| `sits_on` | `positions` | Audience sits on Axis | Axis positions Audience |

## The join

The two worlds meet here, and this is the only part of the system a reader needs to trust. A Connection is a node rather than an edge so that it can be pointed at, dated, disagreed with and — the case that matters — counted when there are none.

### join/v1

For every article A and every audience U, a Delivery exists. A concern declaring `requires` is skipped unless A also contains a qualifying type. For each remaining concern C and each entity E in A's graph, a match is attempted; every match found becomes a Connection. The Delivery is `reached` if it holds at least one Connection and `withheld` otherwise. Rank counts each ENTITY once, at its strongest match — summing every connection lets one entity score repeatedly through overlapping concerns, which it did the first time this formula ran.

| Match | Weight | When |
|---|---|---|
| `qualified` | 0 | A concern declaring `requires` does not fire at all unless the article also contains one of the qualifying types. Applied before any other match. |
| `exact` | 3 | E's type is named directly in C's satisfied-by list. |
| `narrower` | 2 | E's type is one hop below a type named in C, in the published taxonomy. |
| `broader` | 1 | E's type is one hop above a type named in C. Weakest match, because a broader thing may not carry the specific consequence the audience is watching for. |
| `consequence` | 2 | A path of at most two article edges runs from E to something C names — and the path reads as a sentence. |

**Reached at:** 1 connection. One connection is enough to reach, deliberately. Ranking, not filtering, is what handles a weak connection — a feed that silently drops items cannot be audited, and an item at the bottom of a ranked list can be.

**Withheld:** A withheld Delivery records which concerns were tried and why each failed: either the audience watches for types this article has none of, or the only matches available were below threshold. 'Nothing matched' is not an acceptable reason on its own.

**Where the model fits, stated plainly.** In the running pipeline the matches are PROPOSED by a language model comparing two graphs — that is stage 3 of the MyFeeds architecture. This formula does not replace that; it constrains the shape of what comes back so that every proposed match is recorded with its type, its weight, its two endpoints and a sentence, and can therefore be disagreed with by a human reading the delivery. The model proposes; the formula records and scores; the reader checks. Where the two sides of a match are identical concept ids, no model is needed at all and the match is computed.

The formula is not only described here — it is [`admin/tools/join.py`](../back-office/tools/index.md), and [the worked example](../explain/index.md) is its output rather than a drawing of what its output would look like.

[Watch it run →](../explain/index.md) [← The six audiences](../audiences/index.md) [This page, as JSON](../data/ontology.json)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/ontology/index.html)*
