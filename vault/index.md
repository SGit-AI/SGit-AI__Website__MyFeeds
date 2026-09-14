# What a feeds vault holds

> Superseded. The folder layout of a feeds vault: subscriptions, cached items, and state kept deliberately apart — plus why read state merges cleanly across devices and why that makes an encrypted vault with real branches the right container.

*Source: <https://myfeeds.sgit.ai/vault/index.html> · site v0.1.3 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

The container

# What a feeds vault holds

**Superseded.** This page is part of an argument this site made in versions v0.1.0 to v0.1.2 — that the valuable half of a feed reader is the record of what you read, and that it belongs in an encrypted vault. It was written before any MyFeeds source material was available to this site, and it is not what MyFeeds is. The thesis is now [the four-stage pipeline](../index.md), built from the recovered writing.

It stays up, unedited below this line, because deleting a wrong claim destroys the only evidence that the process works. Read it as a record of what was argued, not as a description of this project. The change is recorded in [the release history](../admin/versions.md).

A layout, not an application. If two programs agree on this folder shape, either can be thrown away without taking the reading history with it — which is the whole point, and the reason the layout is published before either program exists.

## The layout

```
myfeeds-vault/
├── app.json                    # vault app manifest — entry point, no write grant needed to read
├── index.html                  # the reader, if one is present. Replaceable.
├── feeds/
│   ├── feeds.json              # subscriptions: id, xmlUrl, title, folder, added, active
│   └── <feed-id>/
│       ├── meta.json           # title, htmlUrl, last fetch, last etag
│       └── items/2026/09/<item-id>.json
├── state/
│   ├── read.json               # read-state/v1 — the file that cannot be rebuilt
│   ├── devices/<device>.json   # optional per-device shard, merged into read.json
│   └── notes/<item-id>.md      # one note per file, so two devices conflict per note
└── sources/
    └── 2026-09-14-subscriptions.opml   # what you imported, kept verbatim, never rewritten
```

## Why `feeds/` and `state/` are separate trees

This is the only structural decision on the page, and everything else follows from it.

|  | `feeds/` | `state/` |
|---|---|---|
| Origin | Fetched from the public internet | Produced by you, once |
| If deleted | Re-fetch | Unrecoverable |
| Growth | Unbounded; prune freely | Small; never prune |
| Merge | Last fetch wins, nothing is lost | Union, nothing is overwritten |
| Backup priority | Convenience | The reason the vault exists |

Keeping them apart means a user can delete `feeds/` entirely — after a laptop fills up, or to shrink a vault before handing a read key to somebody — and lose nothing that matters. A reader that interleaves read flags into the cached item files makes that impossible, and every reader interleaves them, because when you are writing the code they are obviously the same object.

Store the thing you cannot get back in a different tree from the thing you can. Everything else about this design is a consequence.

## Why an encrypted vault rather than a folder in Dropbox

Three properties, in the order they matter:

1. **The host cannot read it.** A reading history is a behavioural profile; it should be ciphertext everywhere it is at rest and everywhere it is in transit. In an [sgit vault](https://sgit.ai/security/index.md) the client encrypts before anything leaves the machine, and the server holds opaque objects — it does not see file names, contents or commit messages. unverified as stated here: this is a summary of the platform's published security model, not an independent audit of it, and this site has run no such audit.

2. **It has real branches and a real merge.** Two devices are two branches; the union merge from [read-state/v1](../read-state/index.md#contract) is what a merge of `state/` means. File sync gives you last-writer-wins and a folder full of *file (conflicted copy).json*, which for a grow-only set is data loss with extra steps.

3. **It is handed over with one string.** A vault has a read key that is a complete credential — no account, nothing installed for the reader. That matters less for your own reading history and a great deal for the thing one layer up: publishing a curated feed to somebody else is the same mechanism, with a different key.

## The reader is a vault app, and is the replaceable part

A vault can carry its own front end: an `index.html` inside the vault that the host renders, reading the vault's files through a bridge rather than over the network. That makes a reader that ships *with* the data instead of owning it.

The constraint it puts on the design is the useful one. A vault app has no server, so it cannot fetch feeds itself in the general case — cross-origin requests to arbitrary publishers will not survive the browser. So fetching is a separate job on a machine you trust, writing into `feeds/`, and the app is a pure reader over the vault plus a writer of `state/`. That split is a nuisance for one afternoon and correct forever: the component that touches the network never touches your reading record.

None of this is built. The layout above is a contract with no implementation behind it today — see [the build order](../build-order/index.md), where the fetcher, the importer and the reader are listed in the order they have to be written and with what each one blocks.

## The property that falls out for free

Once the reading record is a set of files with a published shape rather than rows in an application, three things stop being features and start being consequences: you can `grep` your own reading history; you can hand a year of it to a program you wrote this morning; and you can give somebody a read key to a curated subset without giving them an account on anything. None of those were design goals. They are what happens when state is a document.

[What does not exist yet →](../build-order/index.md) [← The contract](../read-state/index.md) [sgit.ai ↗](https://sgit.ai/)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/vault/index.html)*
