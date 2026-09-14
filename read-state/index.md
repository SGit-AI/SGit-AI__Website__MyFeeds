# The part nobody exports

> OPML moves your subscriptions between readers and carries no read state at all. What read state actually is, why it has never had an interchange format, and read-state/v1 — a contract published before anything implements it.

*Source: <https://myfeeds.sgit.ai/read-state/index.html> · site v0.1.2 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

The contract

# The part nobody exports

OPML has moved subscription lists between readers since 2000. Nothing has ever moved read state, because nothing has ever described it. This page describes it — before any implementation exists, so the description can be judged on its own terms rather than as documentation of whatever got built.

## What OPML carries, and what it does not

An OPML subscription list is a tree of `<outline>` elements. A feed is an element with an `xmlUrl`; a folder is an element with children. In practice the fields that survive a move between readers are the feed URL, a title, and the folder it sat in.

```
<outline text="Security" title="Security">
  <outline type="rss" text="Krebs on Security"
           xmlUrl="https://krebsonsecurity.com/feed/"
           htmlUrl="https://krebsonsecurity.com/" />
</outline>
```

That is the whole interchange surface. There is no element for an item, so there is nowhere to put whether you read one. argued — OPML is a subscription format and was never intended to carry per-item state; the complaint is not that OPML is deficient but that the gap it leaves was never filled by anything else.

**Claims about specific products on this page are marked unverified.** They were written from working memory rather than from each vendor's own export documentation. [Card 003](../team/board.md#todo) is open to check every one of them and either source it or correct it. Until that card closes, treat them as leads.

## What read state actually is

Strip away the product features and a reading record is a set of facts of one shape:

This item, first read at this time.

Everything else a reader stores about an item is either derived from that (unread counts, "keep unread", per-feed progress) or is a separate, smaller, deliberate act: a star, a tag, a note. The deliberate acts are already treated as valuable — they are what the exports carry. The reading itself is not, and it is the large one.

### Why the shape matters more than the fields

Because of what it lets you do without a server. A set of `(item, first read at)` pairs is a **grow-only set**: entries are added and never removed or changed. Two copies of it merge by union. There is no conflict to resolve, because if your phone says you read something at 07:14 and your laptop says 07:16, both are true and the earlier one wins by simple comparison — not by a policy, by arithmetic.

That single property is why this belongs in a version-controlled encrypted vault rather than behind a sync API. A sync API exists to arbitrate conflicting writes. Read state has no conflicting writes. All it needs is somewhere to put files and a merge that means union.

## read-state/v1

argued — published as a contract, not as documentation of an implementation. The JSON Schema and its validator are [card 001](../team/board.md#todo); until that ships, this prose and the example below are the whole specification, and any disagreement with it is cheap to act on, which is the reason for publishing it this early.

### The file

```
{
  "schema": "read-state/v1",
  "generated": "2026-09-14T09:12:04Z",
  "device": "laptop",
  "entries": {
    "sha256:9f2a1c…": { "read": "2026-09-13T07:14:22Z" },
    "sha256:4b77e0…": { "read": "2026-09-13T07:16:03Z", "star": "2026-09-13T07:16:19Z" },
    "sha256:0ad913…": { "read": "2026-09-12T22:40:11Z", "note": "notes/0ad913.md" }
  }
}
```

| Field | Rule |
|---|---|
| `schema` | Exact string `read-state/v1`. A reader that does not recognise it must not write to the file. |
| `entries` | Keyed by item identity (below). Add-only: an entry is never deleted and an existing timestamp is never moved later. |
| `read` | RFC 3339, UTC, the *first* time this item was read. Required on every entry — an entry with no `read` is not read state. |
| `star`, `note` | Optional. Present because they are already portable in practice, and cheap to carry in the same place. |
| `device` | A free label, for a human debugging a merge. It carries no semantics and no two devices are required to differ. |

### Item identity

The hard part, and the part most likely to be wrong in v1. An item's identity must be stable across re-fetches, stable across readers, and computable without a server. The rule:

```
item_id = "sha256:" + sha256( feed_url + "\n" + guid )

where guid is, in order of preference:
  RSS   <guid>            if present
  Atom  <id>              if present
  else  <link>            normalised (scheme+host lowercased, fragment dropped)
  else  sha256(<title> + <pubDate>)
```

**What this does not cover, stated plainly:**

- A feed that changes its `guid` scheme orphans every prior entry. The old entries remain and become unreachable; nothing breaks, but the history is silently split. No mitigation is proposed in v1.

- The same article in two feeds is two items. Cross-feed deduplication is out of scope.

- A feed served from two URLs (http/https, with and without `www`) produces two identities. Normalisation of the feed URL itself is deliberately not specified in v1, because guessing it wrong is worse than leaving it.

- There is no "unread" — removing an entry is not permitted, so marking something unread again is a reader-local affair and does not belong in this file.

### The merge rule

```
merge(A, B):
  for each item_id in A ∪ B:
    read  = min(A.read,  B.read)     # first read wins; both were true
    star  = min(A.star,  B.star)     # first star wins
    note  = A.note or B.note         # divergent notes are a vault-level conflict
```

Note the shape of that: it is commutative, associative and idempotent, so it does not matter what order devices sync in, how many times, or whether one was offline for a month. The one case it does not settle — two devices writing different notes for the same item — is pushed up to the vault, where a real merge with a human in the loop already exists. argued

## What existing readers do instead

Every one of the rows below is unverified and is the subject of [card 003](../team/board.md#todo). They are recorded here as the shape of the problem, not as findings.

| Approach | What is claimed, pending verification |
|---|---|
| The Google Reader API, after 2013 | Several self-hosted readers implement a compatible API, which makes it the closest thing to a de-facto read-state protocol — a protocol for a product that no longer exists, never standardised, and defined by whatever its clients happened to need. |
| Per-product export | Typically OPML for subscriptions, and a separate dump of starred or saved items. The per-item read flags are generally not included. |
| Direct database access | Available for self-hosted readers, and the shape is per-product. It is a backup, not an interchange format. |

If any of that is wrong, it is wrong in public with a card open against it, which is the intended behaviour of this site rather than an embarrassment about it.

[Where the file lives →](../vault/index.md) [What is not built yet →](../build-order/index.md) [← The argument](../thesis/index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/read-state/index.html)*
