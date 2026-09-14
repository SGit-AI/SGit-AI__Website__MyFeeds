---
id: 006
title: Keep deploy-pages.yml in step with the estate's copy
status: todo
owner: devops
kind: task
opened: 2026-09-14
---

`.github/workflows/deploy-pages.yml` is not this site's invention. It is the pipeline every
`*.sgit.ai` site runs, taken from `SGit-AI__Website__Teams`, and it carries fixes this site
has not had to learn: reading `git log` once because piping it into an early-exiting reader
dies of SIGPIPE under `pipefail`; anchoring the release commit to the newest versioned
subject because a merged pull request makes HEAD a merge commit; checking the remote before
pushing backfill tags.

Two adaptations were made here and should be reviewed against upstream rather than
preserved by default: the `validate` job rebuilds and diffs instead of running several
per-generator `--check` steps (this site has one generator), and the release-commit
regexes accept both quote styles for the version, because the main site writes
`SITE_VERSION` with single quotes and this one reads a `version.txt`.

**Done when** a periodic diff against the upstream workflow is part of the release routine,
and any upstream fix since has been ported or its absence noted here.
