# The board

> Open work as a kanban of files: needs only the human owner can supply, and tasks an agent can pick up from its starting prompt. Nothing runs — the board versions with the repository it tracks.

*Source: <https://myfeeds.sgit.ai/team/board.html> · site v0.1.0 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Open work

# The board

Every card is a markdown file in `team/board/` with a status line and exactly one owning role. The columns below are those lines rendered at build time. A card with two owners is two cards; a card with no owner does not enter the board.

## Needs 1

Only the human owner can supply these.

`team/board/004-domain.md`

### 004 · myfeeds.sgit.ai does not resolve yet

need owner [devops](roles/devops.md) · opened 2026-09-14

At the time of this release the subdomain has no certificate and no DNS record — a request to `https://myfeeds.sgit.ai/` fails TLS before it reaches anything. The site builds, validates and is committed; it is not served.

Only the human owner can supply this: the DNS record and the Pages configuration that `CNAME` in the repository root expects.

**Done when** `curl -sI https://myfeeds.sgit.ai/` returns 200 and the version in the response matches `VERSION_LOG`.

## Tasks 4

An agent can pick these up from its starting prompt.

`team/board/001-read-state-schema.md`

### 001 · Publish read-state/v1 as a versioned schema with a validator

todo task owner [architect](roles/architect.md) · opened 2026-09-14

`/read-state/` currently describes the shape in prose and one worked example. That is enough to argue with and not enough to build against.

Ship: a JSON Schema at `data/read-state.v1.schema.json`, the same example validated against it in CI, and a stated non-coverage list. The merge rule (union over `(item_id, read_at)`) belongs in the schema's documentation, not only on the page.

**Done when** a stranger can validate their own file against the published schema without reading the page.

`team/board/002-opml-importer.md`

### 002 · OPML to vault importer

todo task owner [dev](roles/dev.md) · opened 2026-09-14

Take an OPML export from any reader and produce the `feeds/feeds.json` described on `/vault/`. Subscriptions only — OPML carries no read state, and the importer must not invent one. Items with no `xmlUrl` are dropped with a line on stderr, not silently.

Blocked by 001 only for the state half; the subscription half can ship first.

**Done when** `myfeeds import subscriptions.xml` produces a `feeds.json` that round-trips back to an OPML a reader will accept.

`team/board/003-verify-reader-exports.md`

### 003 · Check what each named reader actually exports, against its own docs

todo task owner [qa](roles/qa.md) · opened 2026-09-14

Every sentence on this site about what a specific product does or does not export is currently marked `unverified`, because it was written from memory rather than from a primary source. That marker is honest; it is not a resting place.

For each reader this site names: find the vendor's own export documentation, record the URL and the date checked, list the fields the export carries, and move the sentence to sourced — or correct it.

**Done when** no `unverified` marker remains on `/read-state/` without a dated reason beside it.

`team/board/005-network-entry.md`

### 005 · Send the sibling-site entry upstream to sgit.ai

todo task owner [librarian](roles/librarian.md) · opened 2026-09-14

The network directory on sgit.ai carries one file per sibling site, owned by that site's Cartographer. This site does not exist there yet.

Send: the slug, the one-line thesis (*feeds are replaceable, your reading is not*), the description, the version, and the status label. The upstream rule is that a sibling site is described in its own words and corrected upstream when the directory is wrong about it.

**Done when** `myfeeds.sgit.ai` appears in `https://sgit.ai/network/index.md`.

[← The team](index.md)[Starting prompts →](prompts.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/team/board.html)*
