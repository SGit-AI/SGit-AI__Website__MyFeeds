---
id: 001
title: Publish read-state/v1 as a versioned schema with a validator
status: todo
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
