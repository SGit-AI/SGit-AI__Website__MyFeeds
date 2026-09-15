# About, licence and honest edges

> Whose site this is, how it was written, what it is worth, and the list of things it currently gets to assert without having proven.

*Source: <https://myfeeds.sgit.ai/about/index.html> · site v0.1.7 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Provenance

# About, licence and honest edges

A site arguing that people should be sceptical about who holds their data owes its readers the same scepticism about itself. This page says who wrote it, how, what it is worth, and what it is currently getting away with.

## Whose site this is

**Owner**

: Dinis Cruz

**Written by**

: A team of AI agents under one human owner, in the open. The roles, the rules each enforces and the prompts that start them are published at [/team/](../team/index.md).

**Licence**

: CC BY 4.0. Quote it, fork it, argue with it; attribution is the only condition.

**Source**

: The repository carries both the source and the generated site. Nothing on the published tree was hand-written.

**Part of**

: The [sgit.ai network](../network/index.md).

## Participant disclosure

This site argues for a design that is a natural fit for sgit and SG/Send, which are products of the same estate that publishes this site. That is a conflict of interest and it is disclosed rather than managed: the argument on [/vault/](../vault/index.md#why-vault) for an encrypted vault over a synced folder should be read knowing that the author sells the vault.

The defence offered is that the argument is written so it can be taken elsewhere. The [read-state contract](../read-state/index.md#contract) names no vendor and would work in a git repository, a synced folder, or a proprietary service; the properties it needs — a union merge and encryption at rest — are stated as requirements rather than as a product. If the contract is only useful with one company's software, it is a bad contract and that is a fair criticism to make of it.

## Honest edges

The complete list of things this site currently asserts without having proven:

**This table was replaced wholesale at v0.1.3.** Until then it listed the edges of a different argument — what feed readers export, what a vault guarantees — which was superseded when the MyFeeds source material became available. Those rows are not hidden: they are in [the superseded build order](../build-order/index.md) and in [the release history](../admin/versions.md), which is where a retired claim belongs once it is no longer the site's claim.

| Claim | Status | What would settle it |
|---|---|---|
| The four-stage pipeline is what MyFeeds does | shipped | Settled. It is described in the author's own posts, recovered [here](../back-office/archive/index.md), and the engine is public at [the-cyber-boardroom/myfeeds-ai](https://github.com/the-cyber-boardroom/myfeeds-ai). |
| Decomposing the call buys back explainability and provenance | argued | A worked trace published end to end: one briefing, its four intermediate JSON files, and the source article each claim came from. The archive shows the outputs; it does not show the intermediates. |
| "A measure of determinism" | argued | Deliberately hedged, in the original's own words. An LLM is not deterministic; schema-constrained stages are repeatable enough to check. Settled by running the same inputs repeatedly and publishing the variance — which nobody has done. |
| The single-call approach fails the way this site says it does | argued | It is a first-hand account of building both, not a controlled comparison. A side-by-side on the same fifty articles, with both outputs published, would make it evidence. |
| Competitors have tried this "with limited success" | unverified | Carried over from the recovered post and not independently checked here. `docs/similar-services.md` in the engine repository is the place to start. |
| 9 archived URLs are unrecoverable | argued | Unrecoverable *from the Internet Archive*, which is what the manifest says. [Card 010](../team/board.md#todo) lists the other places to look before that becomes a conclusion. |
| The site is live at myfeeds.sgit.ai | shipped | Serving since v0.1.1, confirmed by `admin/build/verify-live.sh` rather than by a green CI badge. |

## What this site is worth

It is an argument with a contract attached and no implementation. That is worth something — it is cheap to disagree with now and expensive to disagree with after the code exists, which is the entire reason for publishing in this order. It is not worth treating as a description of working software, and the [build order](../build-order/index.md) exists so that nobody has to guess which parts are which.

## Corrections

A correction is published above the claim it corrects, and the claim stays, because deleting a wrong claim destroys the only evidence that the process works. If something here is wrong — particularly one of the unverified rows above — the useful form of that is the primary source, and it will be quoted and dated on the page rather than absorbed.

[What does not exist yet →](../build-order/index.md) [How this site is run →](../team/index.md) [← Home](../index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/about/index.html)*
