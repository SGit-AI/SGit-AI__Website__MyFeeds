---
id: 007
title: Record the commit a version was built from, not just its tag
status: held
owner: historian
kind: task
opened: 2026-09-14
---

The estate's versions contract says a version must name the commit it was built from, or it
cannot be verified later. `versions/<version>.json` currently carries `commit: null` and
`commit_ref: refs/tags/<version>` instead.

The reason is real: the commit that *carries* a version cannot be known while that version
is being built — it does not exist yet — and CI tags the release commit at publish time, so
the tag is a durable pointer while a hash written at build time would either be wrong or
change on every rebuild and break the staleness check.

**Held**, not open, because the obvious fixes are worse than the gap: capturing `git
rev-parse HEAD` at build time records the *previous* commit under a field that claims to be
this one, and having CI write the hash back means a CI-authored commit that exists only on
the git side, which breaks the both-remotes-in-sync invariant.

**Reopen when** there is a way to fill `commit` that is true at the moment it is written —
most likely the Historian backfilling the previous release's hash in the entry for the next
one, which is honest and verifiable.
