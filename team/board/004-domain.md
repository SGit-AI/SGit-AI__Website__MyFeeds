---
id: 004
title: myfeeds.sgit.ai does not resolve yet
status: need
owner: devops
kind: need
opened: 2026-09-14
---

At the time of this release the subdomain has no certificate and no DNS record — a
request to `https://myfeeds.sgit.ai/` fails TLS before it reaches anything. The site
builds, validates and is committed; it is not served.

Only the human owner can supply this: the DNS record and the Pages configuration that
`CNAME` in the repository root expects.

**Done when** `curl -sI https://myfeeds.sgit.ai/` returns 200 and the version in the
response matches `VERSION_LOG`.
