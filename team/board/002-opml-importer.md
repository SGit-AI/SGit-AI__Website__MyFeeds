---
id: 002
title: OPML to vault importer
status: held
owner: dev
kind: task
opened: 2026-09-14
---

Take an OPML export from any reader and produce the `feeds/feeds.json` described on
`/vault/`. Subscriptions only — OPML carries no read state, and the importer must not
invent one. Items with no `xmlUrl` are dropped with a line on stderr, not silently.

Blocked by 001 only for the state half; the subscription half can ship first.

**Done when** `myfeeds import subscriptions.xml` produces a `feeds.json` that round-trips
back to an OPML a reader will accept.

---

**Held at v0.1.3.** This card belongs to the read-state argument the site made in v0.1.0
to v0.1.2, which has been superseded — see the release history. It is kept rather than
deleted because the cards are the record of what the team was working on, and a board that
quietly loses its history is worth less than one that shows a direction being abandoned.
Reopen only if the read-state work is ever picked up in its own right.
