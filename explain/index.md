# Why this article reached these audiences and not the others

> One real Portuguese article put through the join, with its working out: the entities, every concern tried, the connections that fired and the verdicts that did not — plus the three defects the first run found in the audience ontology, shown before and after.

*Source: <https://myfeeds.sgit.ai/explain/index.html> · site v0.1.6 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

The debug view

# Why this article reached these audiences and not the others

One real article, put through the join and shown with its working out. This is the view that exists to be *checked* rather than read — the one you open when a feed shows you something and you want to know who decided that. Every line below is output from `admin/tools/join.py`, not a drawing of what the output would look like.

## The article

2026-09-14 · pt-PT · [pt.newsroom.sgit.ai](https://pt.newsroom.sgit.ai/artigos/2026/09/14/dois-nomes-para-os-mesmos-palcos/)

### Dois nomes para os mesmos palcos

*Two names for the same stages*

Three pages of the same event site, frozen on the same day, name the event's stages two different ways. The agenda and the speakers page say Unicorn Stage, Impact Stage and Workshop Rooms. The sponsorship page says Main Stage, Startup Stage and Workshop Rooms. One of the three names matches; two do not. The article does not say which is right, because nothing in the frozen pages says.

3 claims confirmed, 0 disputed, 0 not found — re-checked against the frozen sources by the newsroom that published it.

**Extraction status:** Extracted by hand from the article and its afirmacoes.json, NOT by the pipeline. This is a worked example chosen because the article is real, verified, and carries its claims and frozen sources — so the join can be checked against something that exists. When the pipeline runs against the newsroom, this file is what stage 1 produces and this hand copy is deleted.

## What stage 1 pulled out

The article as entities and edges. Every type here is defined in [the article ontology](../ontology/index.md#article), and an entity whose type is not defined stops the build — an unknown type can never match anything, so the article would look uninteresting rather than unreadable.

| Entity | Type | Is |
|---|---|---|
| `article` | Article | Dois nomes para os mesmos palcos |
| `event:startup-summit-lisbon-2026` | Event | Startup Summit Lisbon 2026 |
| `discrepancy:stage-names` | Discrepancy | the stage names disagree across three pages of one site |
| `source:agenda` | Source | the frozen agenda page (2026-09-14/agenda) |
| `source:oradores` | Source | the frozen speakers page (2026-09-14/oradores) |
| `source:patrocinadores` | Source | the frozen sponsorship page (2026-09-14/patrocinadores) |
| `claim:a1` | Claim | the agenda names Unicorn Stage, Impact Stage and Workshop Rooms |
| `claim:a2` | Claim | the speakers page names the same three |
| `claim:a3` | Claim | the sponsorship page names Main Stage, Startup Stage and Workshop Rooms |

### And how they connect

| From | Verb | To |
|---|---|---|
| `article` | **states** | `claim:a1` |
| `article` | **states** | `claim:a2` |
| `article` | **states** | `claim:a3` |
| `claim:a1` | **rests_on** | `source:agenda` |
| `claim:a2` | **rests_on** | `source:oradores` |
| `claim:a3` | **rests_on** | `source:patrocinadores` |
| `article` | **reveals** | `discrepancy:stage-names` |
| `discrepancy:stage-names` | **involves** | `source:agenda` |
| `discrepancy:stage-names` | **involves** | `source:patrocinadores` |

## The six verdicts

One delivery per audience, whether or not the article reached it. A withheld delivery carries the same structure as a reached one, because explaining what was rejected is the half a reader actually doubts.

control · always

### The faithful translation

The control audience. Every article reaches it and no selection runs — it is the baseline the other audiences' output is compared against.

reached rank 5

### The founder

2 connection(s) from 1 concern(s).

exact · weight 3

The founder watches events worth attending; the article names Startup Summit Lisbon 2026, which is a Event.

**And back:** Startup Summit Lisbon 2026 satisfies events worth attending, which the founder watches.

consequence · weight 2 · *proposed by the model*

The founder watches events worth attending; the stage they were told to expect may not be the stage that exists, which matters to anyone printing a schedule, briefing a speaker or buying a sponsorship.

**And back:** This event's stage naming is unreliable, which the founder attending it needs to know.

**Path:** `discrepancy:stage-names --involves--> source:agenda --describes--> event:startup-summit-lisbon-2026`

#### Every concern tried

| Concern | Wanted | Hits | Outcome |
|---|---|---|---|
| Funding programmes and calls | `Programme` `Instrument` | — | this article has no Programme or Instrument in it |
| Events worth attending | `Event` | 1 | satisfied |
| Companies in the same sector | `Organisation` | — | this article has no Organisation in it |
| Obligations that bind small companies | `Obligation` | — | this article has no Obligation in it |

withheld

### The allocator

None of the concerns this audience watches were satisfied: this article has no Sector or Organisation in it; this article has no Instrument in it; this article has no Measure in it; this article has no Money in it.

#### Every concern tried

| Concern | Wanted | Hits | Outcome |
|---|---|---|---|
| Signals about a sector | `Sector` `Organisation` | — | this article has no Sector or Organisation in it |
| Policy and regulatory direction | `Instrument` | — | this article has no Instrument in it |
| Counts of a population and how they move | `Measure` | — | this article has no Measure in it |
| Money entering or leaving | `Money` | — | this article has no Money in it |

reached rank 3

### The executive

2 connection(s) from 2 concern(s).

exact · weight 3

The executive watches what a board will ask about; the article names the stage names disagree across three pages of one site, which is a Discrepancy.

**And back:** the stage names disagree across three pages of one site satisfies what a board will ask about, which the executive watches.

exact · weight 3

The executive watches anything that becomes a public question; the article names the stage names disagree across three pages of one site, which is a Discrepancy.

**And back:** the stage names disagree across three pages of one site satisfies anything that becomes a public question, which the executive watches.

#### Every concern tried

| Concern | Wanted | Hits | Outcome |
|---|---|---|---|
| Cost, revenue and exposure in money | `Money` | — | this article has no Money in it |
| What a board will ask about | `Discrepancy` `Obligation` | 1 | satisfied |
| Where we stand against named others | `Organisation` | — | this article has no Organisation in it |
| Anything that becomes a public question | `Discrepancy` | 1 | satisfied |

withheld

### The practitioner

None of the concerns this audience watches were satisfied: this article has no Technology in it; this article has no Weakness in it; this article has no Control in it; this concern only applies where the article is also about Technology or Weakness or Control, and this one is not.

#### Every concern tried

| Concern | Wanted | Hits | Outcome |
|---|---|---|---|
| Named technologies and versions | `Technology` | — | this article has no Technology in it |
| Weaknesses and how they are reached | `Weakness` | — | this article has no Weakness in it |
| Something to change on a system | `Control` | — | this article has no Control in it |
| Whether published information can be trusted | `Discrepancy` | — | this concern only applies where the article is also about Technology or Weakness or Control, and this one is not |

reached rank 3

### The risk owner

2 connection(s) from 2 concern(s).

exact · weight 3

The risk owner watches published information that disagrees with itself; the article names the stage names disagree across three pages of one site, which is a Discrepancy.

**And back:** the stage names disagree across three pages of one site satisfies published information that disagrees with itself, which the risk owner watches.

consequence · weight 2 · *proposed by the model*

The risk owner watches who is answerable; one organisation published two answers to the same question on its own site, which is a control failure regardless of which answer is right.

**And back:** This discrepancy makes the event organiser answerable, which the risk owner watches.

**Path:** `discrepancy:stage-names --involves--> source:patrocinadores; source:patrocinadores is a page of the event organiser's own site`

#### Every concern tried

| Concern | Wanted | Hits | Outcome |
|---|---|---|---|
| Something more likely or more expensive | `Weakness` | — | this article has no Weakness in it |
| Duties, and who they bind | `Obligation` `Instrument` | — | this article has no Obligation or Instrument in it |
| Who is answerable | `Organisation` `Person` | — | this article has no Organisation or Person in it |
| Published information that disagrees with itself | `Discrepancy` | 1 | satisfied |

## What the first run found — about the ontology, not the article

The first time this formula ran, the answer was wrong, and it was wrong in a way that is worth showing rather than quietly fixing. Here is what it said and what it says now:

| Audience | First run | Now |
|---|---|---|
| The faithful translation | reached · — | **reached · —** |
| The founder | reached · 3 | **reached · 5** |
| The allocator | withheld · — | **withheld · —** |
| The executive | reached · 9 | **reached · 3** |
| The practitioner | reached · 12 | **withheld · —** |
| The risk owner | reached · 6 | **reached · 3** |

Three defects, all in the hand-maintained audience side rather than in the article:

- **The practitioner ranked highest** — on a story about stage names at a startup event. Its *integrity* concern matched on `Source`, and every article that freezes its sources has Sources. A concern satisfied by every article is a tautology: it makes an audience look interested in everything and carries no information into the ranking. The concern is now *qualified* — it only fires where the article is also about a technology, a weakness or a control — and the practitioner is now correctly withheld from this story.

- **The executive outranked the founder**, on an event story, because one Discrepancy satisfied two of its overlapping concerns and scored twice. Rank now counts each entity once, at its strongest match. The double match is still listed, because it is real and worth seeing; it just does not pay twice.

- **The risk owner matched on any event at all** through a concern called "something more likely or more expensive". An event existing is not a change in exposure. That concern now requires a `Weakness`; the article still reaches the risk owner, by the route its role predicted — sources disagreeing with each other.

### The part worth keeping

A ranking model that put a stage-naming story at the top of a security practitioner's feed is not unusual. What is unusual is being able to see it, in one table, with the offending concern named — and to fix the concern rather than tune a weight until the symptom goes away. That is the entire argument of this site, happening on the first article it was pointed at.

The second thing the run showed is subtler. With exact matches only, four audiences tied at the same rank: the formula was auditable and useless. The discrimination comes back with the *consequence* matches — which are the ones a model proposes, because they need reading rather than lookup. Neither half works alone. A rules engine is checkable and blunt; a model is sharp and unaccountable; this is a model proposing inside a shape that records what it proposed.

## The same thing, as data

Every verdict above is served at [`/data/joins/dois-nomes-para-os-mesmos-palcos.json`](../data/joins/dois-nomes-para-os-mesmos-palcos.json), the audiences at [`/data/audiences.json`](../data/audiences.json) and the grammar at [`/data/ontology.json`](../data/ontology.json). Run it yourself:

```
python3 admin/tools/join.py   admin/content/data/articles/dois-nomes-para-os-mesmos-palcos.json
```

[← The six audiences](../audiences/index.md) [The grammar →](../ontology/index.md) [The recovered library →](../library/index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/explain/index.html)*
