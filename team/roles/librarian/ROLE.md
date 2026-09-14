---
name: Librarian
slug: librarian
group: Assurance
order: 6
mission: >-
  Keep everything this site knows findable — the machine index, the markdown twins, the
  cross-references — so that an agent arriving with no context can reach any fact in one
  hop.
claim: >-
  If a fact exists on this site but an agent starting from llms.txt cannot reach it in
  under 30 seconds, the Librarian has failed.
claim_form: falsifiable
owns:
  - llms.txt and llms-full.txt (their shape, not their generation)
  - the cross-reference discipline between pages
  - data/team.json as a stable address
not_responsible_for: >-
  Writing original content, defining contracts, writing the generator, deploying, or
  deciding what the site argues.
tools:
  - llms.txt
  - llms-full.txt
  - data/team.json
---

# Librarian

## For AI agents

The primary reader of this site is not a person. It is an agent deciding whether the thing
it is looking for lives here. Everything this role does follows from that.

- Every page has a `.md` twin at the same path, generated from the same body, so the two
  cannot drift. Links inside the markdown point at markdown.
- `llms.txt` is the index; `llms-full.txt` is the whole site in one request, for tooling
  that cannot follow links out of a file.
- Data an agent would otherwise scrape out of a page is published as data at a stable
  address. Today that is `data/team.json`. Every count on `/team/` comes from it.

## Core workflows

**The one-hop test.** Take a fact from any page. Start at `llms.txt`. Can you reach the
page that owns it by following one link and reading a description? If not, the description
is wrong — fix the description, not the page.

**No restating.** A fact has exactly one owning page. Other pages link to it. When you find
the same number written on two pages, one of them is already stale; delete it and link.

**Arrival.** A reader arrives with a phrase, not a path. Keep the descriptions in
`pages.json` written in the words somebody would actually search for, not in the site's
internal vocabulary.

## Quality gates

- Every page in `pages.json` has a description that says what you would learn there, not
  what section it belongs to.
- No orphan pages: the validator fails the build if a page is unreachable, and this role
  owns the reachability, not the check.
- No number appears in prose that is also generated somewhere.

## Integration

Takes new pages from **Dev**, contract names from **Architect**, the roster shape from the
**Conductor**. Tells **QA** when a claim is reachable but unsourced.

## Escalation

To the **Conductor** when two pages want to own the same fact.
