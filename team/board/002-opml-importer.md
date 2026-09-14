---
id: 002
title: OPML to vault importer
status: todo
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
