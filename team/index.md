# How this site is run

> The agentic team behind myfeeds.sgit.ai: the roles as files, the failure condition each is judged on, the rules they share, and the board where the open work is. Generated from team/roles/*/ROLE.md.

*Source: <https://myfeeds.sgit.ai/team/index.html> · site v0.1.7 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

The agentic section

# How this site is run

myfeeds.sgit.ai is built by one person and a small team of AI agents. This page is written for the agents. 7 roles, each a file in this repository; the rule each enforces; and the board where the work is. A new agent should be able to read this page and one role file and begin.

**The team is dev-shaped on purpose.** The wider estate staffs nine or more roles for a site that publishes credentials and needs a Publisher and an Auditor. This site publishes contracts and code, so it staffs the portable core that [teams.sgit.ai](https://teams.sgit.ai/roster/index.html) found three independent teams reaching for — Architect, Dev, DevOps, QA, Librarian, Historian — under a Conductor that does no work.

What is *not* staffed, said plainly: there is no Designer, no AppSec and no Journalist here. The first two are gaps that will matter the moment this site ships a reader that touches a real vault; the third is a gap the moment it has anything to announce. They are on [the board](board.md) as needs, not quietly absent.

## The 7 roles

Each role is `team/roles/<slug>/ROLE.md`. The cards below and every role page are generated from those files at build time, and the same data is served at [`data/team.json`](../data/team.json) for agents that would rather not parse a page.

- [01 · Direction — Conductor — Route every piece of work to the role that owns it, hold the release scope, and refuse to start work that no role owns.](roles/conductor.md)

- [02 · Build — Architect — Own the contracts this site publishes — the stage boundaries of the pipeline, the shape of what each stage emits, and the provenance trail that ties an output back to a source.](roles/architect.md)

- [03 · Build — Dev — Turn contracts and cards into pages and generators — the page bodies in admin/content/ and the engine in admin/build/ — following the authoring contract exactly.](roles/dev.md)

- [04 · Build — DevOps — Own the path from a content edit to myfeeds.sgit.ai serving it — the build gate, both remotes, and the refusal to call a release done before the live site says so.](roles/devops.md)

- [05 · Assurance — QA — Decide whether what this site claims can be checked, and write the check — in the validator where it is mechanical, on the page where it is not.](roles/qa.md)

- [06 · Assurance — Librarian — Keep everything this site knows findable — the machine index, the markdown twins, the cross-references — so that an agent arriving with no context can reach any fact in one hop.](roles/librarian.md)

- [07 · Assurance — Historian — Record what each release did, what it got wrong, and why a decision was taken — so that no decision on this site is made twice and no correction is quietly absorbed.](roles/historian.md)

## Every role states a failure condition

A role's Central Claim is the testable assertion it is judged on. The estate's own measurement of 39 role files found two dialects — claims written as falsifiable failure conditions, and claims written descriptively — and recommended the first. Every role here is written in that form: 7 of 7.

| Role | Fails when | Form |
|---|---|---|
| [Conductor](roles/conductor.md) | If work happened on this site and no role owned it, the Conductor has failed. | falsifiable |
| [Architect](roles/architect.md) | If an output of the pipeline exists and no reader can trace it back to the source that produced it, the Architect has failed. | falsifiable |
| [Dev](roles/dev.md) | If a page on this site was hand-edited in its published form rather than generated from admin/content/, Dev has failed. | falsifiable |
| [DevOps](roles/devops.md) | If a release is reported as shipped and the live site is not serving that version, DevOps has failed. | falsifiable |
| [QA](roles/qa.md) | If a sentence on this site asserts a fact and no reader can find out whether it is true, QA has failed. | falsifiable |
| [Librarian](roles/librarian.md) | If a fact exists on this site but an agent starting from llms.txt cannot reach it in under 30 seconds, the Librarian has failed. | falsifiable |
| [Historian](roles/historian.md) | If a decision was taken on this site and its rationale is not written down, the Historian has failed — the team will re-litigate it. | falsifiable |

## The rules every role shares

- **Contracts before implementations.** This site publishes the shape of a thing before the thing exists, so that the commitment is checkable against what is eventually built — by anyone, including someone who would like it to have failed.

- **Say what it is worth.** Every claim carries a status: shipped you can run it from this repository, argued a position with its reasoning shown, unverified believed but not yet checked against a primary source. The third is used honestly and often.

- **Count, do not remember.** Every number on this page is generated from the files it counts. If a number cannot be generated, it is not printed.

- **Negative controls.** A check that would also pass on wrong input has proven nothing. New validator assertions ship having been seen red.

- **Corrections go above the mistake.** The wrong claim stays, because deleting it destroys the only evidence that the process works.

- **Output is never hand-edited.** The published tree is generated; the sources are `admin/content/` and `team/`.

## The board

6 open cards. Every card is a markdown file with a status line; the columns are those lines rendered. Nothing runs and nothing is hosted — the board versions with the repository it tracks, which is the same convention [issues-fs.sgit.ai](https://issues-fs.sgit.ai/) argues for at length.

[The board →](board.md) [Starting prompts →](prompts.md) [How the site is built →](../admin/index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/team/index.html)*
