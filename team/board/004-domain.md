---
id: 004
title: myfeeds.sgit.ai does not resolve yet
status: done
owner: devops
kind: need
opened: 2026-09-14
closed: 2026-09-14
---

**Closed by v0.1.1, and not in the way this card expected.**

As opened: at v0.1.0 the subdomain had no certificate — a request to
`https://myfeeds.sgit.ai/` failed TLS before reaching anything — and this was filed as a
need only the human owner could supply, on the assumption that a DNS record was missing.

What actually happened: the DNS was already there (`myfeeds.sgit.ai` resolved to the same
GitHub Pages addresses as every sibling site, which is consistent with a wildcard record on
`sgit.ai` — *inferred from the resolution, not confirmed against the zone*). What was
missing was Pages itself being switched on for this repository, so no certificate had ever
been issued for the host. The v0.1.1 deploy job did that: `actions/configure-pages@v5` with
`enablement: true`, plus the `CNAME` file in the repository root, and GitHub provisioned
the certificate.

So the need was not a need. It was the deploy workflow this site did not have.

**Verified:** `admin/build/verify-live.sh` reports `myfeeds.sgit.ai is serving v0.1.1`;
`index.md`, `llms.txt`, `versions/index.json`, `data/team.json` and `app.json` all return
200 with the right content types.
