# Feeds are replaceable. Your reading is not.

> Superseded. Why every feed reader has the durability of its two data sets backwards: the articles can always be fetched again, and the record of what you read exists in exactly one place.

*Source: <https://myfeeds.sgit.ai/thesis/index.html> · site v0.1.8 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

The argument

# Feeds are replaceable. Your reading is not.

**Superseded.** This page is part of an argument this site made in versions v0.1.0 to v0.1.2 — that the valuable half of a feed reader is the record of what you read, and that it belongs in an encrypted vault. It was written before any MyFeeds source material was available to this site, and it is not what MyFeeds is. The thesis is now [the four-stage pipeline](../index.md), built from the recovered writing.

It stays up, unedited below this line, because deleting a wrong claim destroys the only evidence that the process works. Read it as a record of what was argued, not as a description of this project. The change is recorded in [the release history](../admin/versions.md).

A feed reader holds two data sets with opposite properties, and treats them identically. One of them can be reconstructed from the public internet at any time. The other exists once, nowhere else, and is destroyed by the same event that ends your subscription.

## The two data sets

|  | The items | The reading |
|---|---|---|
| What it is | Titles, bodies, links, dates, fetched from a feed URL | What you read, when you first read it, what you starred, what you noted, what you deliberately skipped |
| Who else has it | The publisher, every other subscriber, the Internet Archive, often Google | Nobody |
| If you lose it | Re-fetch it | It is gone |
| What it says about you | Nothing | What you follow, how closely, at what hours, and what you stopped reading and when |
| Where readers keep it | A local cache, cheerfully disposable | The same database, in a private schema, with the same disposability |

Read the last row twice. The column that cannot be reconstructed is stored with exactly the care given to the column that can.

## What a shutdown actually takes

Google Reader was announced for shutdown on 13 March 2013 and closed on 1 July 2013. It was, by the standards of the time, a well-behaved exit: Takeout produced an OPML file of subscriptions, and JSON for starred, liked, shared and noted items. unverified — the shape of those export files is stated here from memory and is [card 003](../team/board.md#todo), to be checked against the archived documentation rather than left as a confident sentence.

What the export did *not* carry, and what no reader's export has carried since, is the per-item read record: the flags on the hundreds of thousands of items you had worked through. The stars survived because a star is a small, deliberate, countable thing somebody thought to serialise. The reading did not, because it is large, incidental, and looks like cache.

> Everyone who migrated in 2013 has the same memory: the subscriptions came across in a minute, and then every feed was full of unread items going back months, and the only way out was to mark everything read and start again. That is the loss this site is about. It was not treated as a loss at the time; it was treated as an inconvenience, which is how you can tell nobody thought the data was theirs.

## A reading history is a profile

The reason this matters beyond nostalgia: the record a reader accumulates about you is more revealing than the subscription list it is derived from. A subscription list says what you were curious about once. A read record says what you actually consume, at what hours, how quickly you abandoned a source, which topics you open immediately and which you let pile up for three weeks and then bulk-dismiss.

That is a behavioural profile, built continuously, and in the hosted model it is held by a party whose business is often advertising. Even where it is not, it is a plaintext asset in somebody else's breach.

If you would not hand someone a list of everything you read last year, with timestamps, you should not be comfortable that a reader holds one and you do not.

## The three honest objections

### "Self-hosting already solves this"

It moves the database and solves nothing about the format. A self-hosted reader's state is still a private schema in one application; you can back it up, and you still cannot read it without running that application, and you still cannot move it to a different reader. Ownership of the disk is not ownership of the data. argued

### "Nobody uses RSS any more"

Partly true and beside the point. The argument here is about the shape of a personal consumption record, and feeds are simply the cleanest case: an open content format, a well-understood item identity, and an existing portable format for half the problem. If the argument holds for feeds it generalises to every other reading surface, most of which are worse. argued

### "Read state is not worth the engineering"

This is the strongest objection, and the answer is that it is nearly free. Read state is the single easiest distributed data structure there is — a grow-only set, described on the [next page](../read-state/index.md), that needs no conflict resolution, no vector clocks and no server. The engineering that is not free is the reader; the state contract is a weekend and a schema.

[The contract →](../read-state/index.md) [The container →](../vault/index.md) [← Home](../index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/thesis/index.html)*
