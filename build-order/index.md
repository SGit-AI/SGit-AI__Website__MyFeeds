# What does not exist yet

> Superseded. Everything this site argues for, in build order, with each item marked shipped, argued or unverified — published before the code so the commitments are checkable against what actually gets built.

*Source: <https://myfeeds.sgit.ai/build-order/index.html> · site v0.1.4 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Honest edges

# What does not exist yet

**Superseded.** This page is part of an argument this site made in versions v0.1.0 to v0.1.2 — that the valuable half of a feed reader is the record of what you read, and that it belongs in an encrypted vault. It was written before any MyFeeds source material was available to this site, and it is not what MyFeeds is. The thesis is now [the four-stage pipeline](../index.md), built from the recovered writing.

It stays up, unedited below this line, because deleting a wrong claim destroys the only evidence that the process works. Read it as a record of what was argued, not as a description of this project. The change is recorded in [the release history](../admin/versions.md).

This site publishes its argument before the thing it argues for. The cost of doing that is this page: every commitment, in the order it has to be built, with what it blocks — so that in six months anyone can check what was claimed against what exists, including the parts that were quietly dropped.

**Status vocabulary.** shipped it is in this repository and you can run it · argued a position, with its reasoning shown, and no code · unverified believed but not checked against a primary source. Nothing on this site is shipped except the site itself.

## The order

| # | Item | Status | Blocks |
|---|---|---|---|
| 0 | **The argument** — these pages and their markdown twins | shipped v0.1.0 | Nothing. It is the thing that lets the rest be criticised before it is written. |
| 1 | **`read-state/v1` as a JSON Schema**, with the worked example validated against it in CI | argued | Everything below. A contract in prose is a conversation; a contract with a validator is a dependency. |
| 2 | **The OPML importer** — an export from any reader becomes `feeds/feeds.json` | not started | The fetcher. Also the first point at which a real user has a vault at all. |
| 3 | **The fetcher** — the only component that touches the network, writing `feeds/<id>/items/` | not started | The reader has nothing to read without it. |
| 4 | **The reader as a vault app** — renders `feeds/`, writes `state/read.json` | not started | Nothing downstream, but it is the first release where the argument is testable by using it. |
| 5 | **Two-device merge, demonstrated** — two branches, a union merge, a published transcript | not started | Nothing. It is the proof obligation for the central claim on [/read-state/](../read-state/index.md#contract). |
| 6 | **A published vault with a read key** — a curated reading list somebody else can open with one string | not started | Nothing. It is the estate's own standard of proof and this site does not meet it yet. |

## The proof obligations

Three claims on this site are the kind that can be shown false. They are written here together so that nobody has to assemble the list themselves.

### 1. Read state merges without conflict

Claimed on [/read-state/](../read-state/index.md#contract). Falsified by a single realistic case where two devices produce a read record that cannot be unioned without losing a fact or requiring a policy decision. Item 5 above is the demonstration that would support it; until then it is arithmetic on a page.

### 2. Item identity is stable enough to be useful

The weakest part of `read-state/v1`, and the one most likely to be wrong. Falsified by measurement: take a few hundred real feeds, fetch them over some weeks, and count how often the derived `item_id` changes for an item that a human would say is the same article. That measurement has not been done. If the churn is high, v1's identity rule is wrong and should be replaced rather than defended.

### 3. No reader exports per-item read state

The claim the whole site rests on, and the one it is least entitled to make right now, because it was written from memory. [Card 003](../team/board.md#todo) is open against it. One counter-example — a mainstream reader whose export carries per-item read flags in a documented format — does not destroy the argument, but it does mean this site has to say so at the top of the page rather than in a footnote.

## Deliberately not doing

- **A hosted service.** There is no server in this design and adding one would undo the reason for it.

- **Cross-feed deduplication.** Tempting, and it turns a rule you can compute into a heuristic you have to tune. Out of scope for v1 and named as such in the contract.

- **Recommendation, ranking, or any read of the history for the user's "benefit".** The entire argument is that this data is sensitive. A feature that mines it, however locally, is a feature that makes the data worth attacking.

- **A Google Reader API compatibility layer.** It would be the fastest route to working with existing clients and it would import the exact model this site is arguing against: read state as a server's business rather than a file's. Reconsider only if item 4 proves too slow to matter.

## What would make this site wrong

Not "incomplete" — wrong. If item 2 above turns out to be true and identity churn makes a portable read record unreliable in practice, then the correct conclusion is that read state is inherently reader-local and the whole argument collapses to "keep better backups". That outcome would be published on this page, above the claim it corrects, with the measurement that produced it. The [Historian role](../team/roles/historian.md) exists to make sure that happens rather than the page quietly changing.

[The board →](../team/board.md) [Honest edges in full →](../about/index.md) [← Home](../index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/build-order/index.html)*
