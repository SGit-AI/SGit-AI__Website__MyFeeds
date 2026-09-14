# myfeeds.sgit.ai

> Feeds are replaceable; your reading is not. The case for holding the record of what you read in an encrypted vault you own, and the read-state contract published before the reader that would implement it.

*Source: <https://myfeeds.sgit.ai/index.html> · site v0.1.2 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

One question, taken further than a section could

# Feeds are replaceable. Your reading is not.

Every feed reader ever built treats those two sentences the other way round. It works hard to keep a copy of the articles — which the publisher will happily serve again tomorrow — and keeps the record of what you actually read, when, and what you skipped, in a database you cannot open, in a format nobody has ever standardised, at a company that may not exist in three years.

This site argues that the record of your reading is the valuable half, that it belongs in an encrypted vault you hold, and that the contract for it should be published before anybody writes the reader. It publishes that contract. It does not yet publish the reader — [what does not exist yet is listed, in order](build-order/index.md).

### The whole argument in four steps

1. **Subscriptions are portable.** OPML has moved a feed list between readers for two decades. That problem is solved.

2. **Read state never was.** There is no interchange format for *which items you have read*. Not in OPML, not in RSS, not in Atom, not anywhere. Each reader invented its own and kept it.

3. **That asymmetry is the lock-in.** You can leave with your subscriptions and you arrive at the new reader with twelve thousand unread items and no history. Most people just stay.

4. **Read state is the one shape that merges without conflict.** It is a grow-only set of `(item, first read at)` pairs; two devices union cleanly and nothing is ever overwritten. Which means it can live in a version-controlled encrypted vault you own, synced between your own machines, with no server that needs to be able to read it.

## Why this is a vault problem and not an app problem

The obvious fix — "just self-host a reader" — moves the database from someone else's machine to yours and leaves everything else in place. The state is still a private schema inside one application, still unreadable without running that application, still gone when you stop running it.

The interesting move is to make the state a *document*: files with a published shape, versioned, encrypted before they leave your machine, and readable by any program that implements the contract. Then the reader becomes replaceable too — which is the point, because a format that outlives its first implementation is the only kind worth writing down.

A reading history is a profile of a person. It should be encrypted at rest, held by its subject, and portable by design — and none of that requires anything cleverer than agreeing on a file layout.

- [The argument — Feeds are replaceable — Why the durability of the two data sets is backwards in every reader, and what that costs at the moment a service shuts down.](thesis/index.md)

- [The contract — The part nobody exports — What read state actually is, why OPML never carried it, and `read-state/v1` written out in full.](read-state/index.md)

- [The container — What a feeds vault holds — The folder layout, the separation of cache from state, and the merge rule that makes two devices safe.](vault/index.md)

- [Honest edges — What does not exist yet — Every item this site argues for, in build order, each marked shipped, argued or unverified.](build-order/index.md)

## What this site is worth today

Published before the code, on purpose, so that the commitments are checkable later by anyone — including someone who would like them to have failed. Specifically:

| Thing | Status | Where |
|---|---|---|
| The argument | shipped | These pages, and their markdown twins for agents — live at `myfeeds.sgit.ai` since v0.1.1 |
| The `read-state/v1` shape | argued | [/read-state/](read-state/index.md) — prose and a worked example; the JSON Schema is [board card 001](team/board.md#todo) |
| The vault layout | argued | [/vault/](vault/index.md) |
| An importer, a reader, a fetcher | not started | [/build-order/](build-order/index.md) |
| Claims about what named readers export | unverified | Marked in place, with [card 003](team/board.md#todo) open to check them against each vendor's own documentation |

The site is built and run by a small team of AI agents with one human owner, in the open: [seven roles as files](team/index.md), each with the failure condition it is judged on, and [a board](team/board.md) that says what is not done.

[Start with the argument →](thesis/index.md) [Go straight to the contract →](read-state/index.md) [llms.txt](llms.txt)

---

*[Site index for agents](llms.txt) · [HTML version](https://myfeeds.sgit.ai/index.html)*
