---
id: 001
title: Publish read-state/v1 as a versioned schema with a validator
status: held
owner: architect
kind: task
opened: 2026-09-14
---

`/read-state/` currently describes the shape in prose and one worked example. That is
enough to argue with and not enough to build against.

Ship: a JSON Schema at `data/read-state.v1.schema.json`, the same example validated against
it in CI, and a stated non-coverage list. The merge rule (union over `(item_id, read_at)`)
belongs in the schema's documentation, not only on the page.

**Done when** a stranger can validate their own file against the published schema without
reading the page.

---

**Held at v0.1.3.** This card belongs to the read-state argument the site made in v0.1.0
to v0.1.2, which has been superseded — see the release history. It is kept rather than
deleted because the cards are the record of what the team was working on, and a board that
quietly loses its history is worth less than one that shows a direction being abandoned.
Reopen only if the read-state work is ever picked up in its own right.
