# Six audiences, and what each converts news into

> The audience side of the join: six roles with a stated appetite rather than a tone of voice — a founder, an allocator, an executive, a practitioner, a risk owner, and a faithful translation that acts as the control. What separates them is what each converts a piece of news into.

*Source: <https://myfeeds.sgit.ai/audiences/index.html> · site v0.1.5 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

The audience side

# Six audiences, and what each converts news into

The same article, read by six roles, should produce six different pieces — not one piece at six lengths. What makes them different is not tone: it is what each role converts a piece of news *into*. A founder turns it into something to do this month; an allocator turns it into evidence about a population; a risk owner turns it into a change in exposure. That is the axis the whole system turns on.

**The first audience is not an audience.** The source material is Portuguese; the first output is a faithful English translation with nothing added, dropped or re-weighted. It is the control: every article reaches it, no selection runs, and it is what the other five are diffed against. Without it there is no way to tell re-framing apart from distortion, because there is nothing to compare against.

## What each one pays in

| Currency | Means | Audience |
|---|---|---|
| **A faithful rendering** | Nothing added, nothing dropped, nothing re-weighted. | EN |
| **Something to act on** | A programme to apply to, an event to attend, a competitor to watch. | Startups |
| **A signal about a population** | What this says about a sector, a cohort or a policy direction. | Investors |
| **A financial or reputational consequence** | What it costs, what it earns, what has to be said about it. | C-level |
| **A technical change** | What to patch, configure, monitor or verify, and by when. | Cyber |
| **A change in exposure or duty** | What became more likely, who is accountable, what obligation was triggered. | Risk |

## The spectrum

Three axes separate them, and the first is the strongest: **how much mechanism the reader wants**. A practitioner and an executive can want the same story and disagree completely about where it should stop. The second — **scope** — is why the founder and the allocator read like inversions of each other: one cares about a named thing, the other about the population it belongs to.

| Audience | Mechanism | Scope | Horizon | Pays in |
|---|---|---|---|---|
| [The faithful translation](#translation-en) | — | — | — | A faithful rendering |
| [The founder](#startups) | 50% | 15% | 20% | Something to act on |
| [The allocator](#investors) | 30% | 90% | 85% | A signal about a population |
| [The executive](#c-level) | 15% | 50% | 50% | A financial or reputational consequence |
| [The practitioner](#cybersecurity) | 100% | 30% | 10% | A technical change |
| [The risk owner](#risk) | 25% | 65% | 60% | A change in exposure or duty |

Mechanism: 0% = the consequence only, 100% = the full mechanism. Scope: 0% = one named thing, 100% = a whole population. Horizon: 0% = this week, 100% = several years. The control audience sits on no axis, deliberately.

## The six

00 · pays in **A faithful rendering** · control

### The faithful translation EN

A reader who wants the Portuguese article in English and nothing else — no re-framing, no selection, no emphasis moved. This is the only audience that is not an audience: it is the control. Every article reaches it, no selection formula runs, and its output is the baseline the other five are diffed against. Without it there is no way to tell re-framing apart from distortion, because there is nothing to compare against.

Mechanism wanted

n/a

the consequence only → the full mechanism

Scope

n/a

one named thing → a whole population

Time horizon

n/a

this week → several years

#### Wants

- Every claim the original made, in the order it made them

- Named entities verbatim, in whatever language the source used

- The source markers carried through unchanged

#### Does not want

- Any judgement about what matters

- Any reordering for emphasis

- Anything the original did not say

01 · pays in **Something to act on**

### The founder Startups

Runs a small company and reads to find things to do this month. Narrow and concrete: their own sector, the companies they compete with or sell to, the programmes they can apply to, the events where the right people will be, and the rules that bite at their size rather than at an incumbent's. A market-level pattern is interesting and not actionable, so it loses to a deadline every time.

Mechanism wanted

the consequence only → the full mechanism

Scope

one named thing → a whole population

Time horizon

this week → several years

#### Wants

- Named programmes, deadlines, eligibility

- Events, who will be there, when

- Competitors and adjacent companies by name

- Rules that apply below a size threshold

#### Does not want

- Portfolio-level analysis

- Anything whose earliest consequence is years away

- Mechanism for its own sake

#### Watches for

| Concern | Satisfied by | Only when |
|---|---|---|
| Funding programmes and calls | `Programme` `Instrument` | — |
| Events worth attending | `Event` | — |
| Companies in the same sector | `Organisation` | — |
| Obligations that bind small companies | `Obligation` | — |

02 · pays in **A signal about a population**

### The allocator Investors

The founder inverted. Cares about populations rather than instances: a single company's news is worth reading only as evidence about a sector, a cohort or a policy direction. Counts things. A story about one firm is noise; the same story as the fourth instance of a pattern is a thesis. Long horizon, low appetite for mechanism, high appetite for a number that can be tracked across quarters.

Mechanism wanted

the consequence only → the full mechanism

Scope

one named thing → a whole population

Time horizon

this week → several years

#### Wants

- Counts, rates and how they moved

- Policy direction and what it will make cheaper or dearer

- Sector-level shifts, not company-level ones

- Anything that says a market is bigger or smaller than believed

#### Does not want

- Single-company operational detail

- This week's deadline

- Technical mechanism

#### Watches for

| Concern | Satisfied by | Only when |
|---|---|---|
| Signals about a sector | `Sector` `Organisation` | — |
| Policy and regulatory direction | `Instrument` | — |
| Counts of a population and how they move | `Measure` | — |
| Money entering or leaving | `Money` | — |

03 · pays in **A financial or reputational consequence**

### The executive C-level

Reads for consequence, in money and reputation, and for what will have to be said to a board next quarter. The lowest appetite for mechanism of any audience here — not because it is beneath them but because it is not the decision they hold. The question behind every item is: does this change what we spend, what we earn, what we owe, or what we will be asked about.

Mechanism wanted

the consequence only → the full mechanism

Scope

one named thing → a whole population

Time horizon

this week → several years

#### Wants

- What it costs or earns, with a number where one exists

- What a board or a regulator will ask

- Competitive position

- What has to be decided, by whom, by when

#### Does not want

- How the technology works

- Implementation detail

- Anything with no consequence to state

#### Watches for

| Concern | Satisfied by | Only when |
|---|---|---|
| Cost, revenue and exposure in money | `Money` | — |
| What a board will ask about | `Discrepancy` `Obligation` | — |
| Where we stand against named others | `Organisation` | — |
| Anything that becomes a public question | `Discrepancy` | — |

04 · pays in **A technical change**

### The practitioner Cyber

The most technical reader on this site and the only one who wants the mechanism for its own sake, because the mechanism is what determines whether the thing is exploitable here. Specific technologies, specific versions, specific controls. Converts news into an action on a system: patch, configure, monitor, verify, or decide that it does not apply. Detail that would lose every other audience is the part this one came for.

Mechanism wanted

the consequence only → the full mechanism

Scope

one named thing → a whole population

Time horizon

this week → several years

#### Wants

- Named technologies and versions

- How something actually works or fails

- What to change and by when

- Whether it applies to this estate at all

#### Does not want

- Consequence framed only in money

- Sector-level abstraction

- A summary that drops the specifics

#### Watches for

| Concern | Satisfied by | Only when |
|---|---|---|
| Named technologies and versions | `Technology` | — |
| Weaknesses and how they are reached | `Weakness` | — |
| Something to change on a system | `Control` | — |
| Whether published information can be trusted | `Discrepancy` | `Technology` `Weakness` `Control` |

05 · pays in **A change in exposure or duty**

### The risk owner Risk

Non-technical and rigorous, which is an unusual pair and the reason this audience is easy to serve badly. Reads for exposure: what became more likely, what became more expensive if it happens, who is accountable, and what duty was triggered. A technical finding matters only as far as it moves one of those. Cares a great deal about one thing nobody else notices — two sources disagreeing with each other — because an organisation that publishes two answers to the same question has a control failure regardless of which answer is right.

Mechanism wanted

the consequence only → the full mechanism

Scope

one named thing → a whole population

Time horizon

this week → several years

#### Wants

- What changed in likelihood or impact

- Who is accountable and under what instrument

- Obligations with dates attached

- Sources that contradict each other

#### Does not want

- Mechanism beyond what changes the exposure

- Opportunity framing

- Anything with no owner

#### Watches for

| Concern | Satisfied by | Only when |
|---|---|---|
| Something more likely or more expensive | `Weakness` | — |
| Duties, and who they bind | `Obligation` `Instrument` | — |
| Who is answerable | `Organisation` `Person` | — |
| Published information that disagrees with itself | `Discrepancy` | — |

[The two ontologies →](../ontology/index.md) [A worked example →](../explain/index.md) [← Home](../index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/audiences/index.html)*
