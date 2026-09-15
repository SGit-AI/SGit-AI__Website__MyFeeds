# The board

> Open work as a kanban of files: needs only the human owner can supply, and tasks an agent can pick up from its starting prompt. Nothing runs — the board versions with the repository it tracks.

*Source: <https://myfeeds.sgit.ai/team/board.html> · site v0.1.8 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

Open work

# The board

Every card is a markdown file in `team/board/` with a status line and exactly one owning role. The columns below are those lines rendered at build time. A card with two owners is two cards; a card with no owner does not enter the board.

## Needs 1

Only the human owner can supply these.

`team/board/009-audience-views.md`

### 009 · Build the multi-audience demo over a live newsroom

need owner [architect](roles/architect.md) · opened 2026-09-14

From the author's voice memo of 14 September 2026, recorded here so the intent does not live only in a transcript.

The ask: a MyFeeds-published version of an existing news site, cut for several audiences rather than one — **startups, investors, and corporate executives**, with the executive audience splitting further into C-level, cybersecurity, and risk. Roughly five views. Portuguese first, English second, since the pipeline can do both and the source newsroom is Portuguese (`pt.newsroom.sk.ai`, with other sources to follow).

The shape is two sites, not one:

- a **generic** MyFeeds site explaining the concepts and principles — which is what

myfeeds.sgit.ai now is; and

- a **worked example** that runs the argument on real news: the graphs from the source

articles, the ontology of each target audience, and the join between them rendered as the output. "Connect the dots, and that's what you see on the website."

**Why this is a need rather than a task.** It requires a running pipeline against a live source, which is an engineering project in `myfeeds-ai`, not a page in this repository. What this site can do without it is publish the contract the demo would have to meet — the audience ontologies and what a view is — which is item 1 below and *is* a task once the audiences are settled.

**Open questions the author has to settle before anything is built** 1. Are the five audiences final, and is there a written ontology for each, or is deriving them from the existing persona definitions part of the work? 2. Does the demo publish as its own site, a section of this one, or back into the source newsroom? 3. Portuguese first — does this site become bilingual, or does the demo carry the Portuguese and this site stay English?

**Done when** those three are answered and the contract for an audience view is published here, before the demo exists. That is this estate's order of work and the reason the commitments stay checkable.

## Tasks 3

An agent can pick these up from its starting prompt.

`team/board/005-network-entry.md`

### 005 · Send the sibling-site entry upstream to sgit.ai

todo task owner [librarian](roles/librarian.md) · opened 2026-09-14

The network directory on sgit.ai carries one file per sibling site, owned by that site's Cartographer. This site does not exist there yet.

Send: the slug, the one-line thesis (*feeds are replaceable, your reading is not*), the description, the version, and the status label. The upstream rule is that a sibling site is described in its own words and corrected upstream when the directory is wrong about it.

**Done when** `myfeeds.sgit.ai` appears in `https://sgit.ai/network/index.md`.

`team/board/006-workflow-upstream.md`

### 006 · Keep deploy-pages.yml in step with the estate's copy

todo task owner [devops](roles/devops.md) · opened 2026-09-14

`.github/workflows/deploy-pages.yml` is not this site's invention. It is the pipeline every `*.sgit.ai` site runs, taken from `SGit-AI__Website__Teams`, and it carries fixes this site has not had to learn: reading `git log` once because piping it into an early-exiting reader dies of SIGPIPE under `pipefail`; anchoring the release commit to the newest versioned subject because a merged pull request makes HEAD a merge commit; checking the remote before pushing backfill tags.

Two adaptations were made here and should be reviewed against upstream rather than preserved by default: the `validate` job rebuilds and diffs instead of running several per-generator `--check` steps (this site has one generator), and the release-commit regexes accept both quote styles for the version, because the main site writes `SITE_VERSION` with single quotes and this one reads a `version.txt`.

**Done when** a periodic diff against the upstream workflow is part of the release routine, and any upstream fix since has been ported or its absence noted here.

`team/board/011-daily-sync.md`

### 011 · The daily routine that syncs this site with pt.newsroom.sgit.ai

todo task owner [devops](roles/devops.md) · opened 2026-09-15

The end state, in the author's words: a daily Claude Code routine that synchronises myfeeds.sgit.ai with `pt.newsroom.sgit.ai`, which itself has agents running on its own interval. A self-maintaining workflow, where this site's job is to take what that newsroom published and put it in front of six audiences with the reasoning attached.

**Why this is a task and not a need.** Everything it depends on now exists: the audiences are defined, the ontology is published, `admin/tools/join.py` runs the formula, and the newsroom publishes its articles as JSON with claims and frozen sources. What is missing is the loop and the extraction step, not a decision.

### The shape

```
daily, on a Routine:
  1. pull      pt.newsroom.sgit.ai's published articles (its api/v1 or the repo)
  2. diff      against admin/content/data/articles/ — new and changed only
  3. extract   article -> entities + edges, against the published article ontology
               (stage 1; the only step that needs a model and the only one that can
               invent something, so its output is reviewed before it is used)
  4. translate the faithful EN rendering — the control audience, no selection
  5. join      python3 admin/tools/join.py per article -> data/joins/<slug>.json
  6. write     one output per reached audience, in that audience's currency
  7. build     python3 admin/build/build_pages.py && node admin/build/validate.js
  8. release   bump version.txt, commit "site vX.Y.Z: ...", push dev; CI deploys
```

### What has to be true before it runs unattended

- **Step 3 is the dangerous one.** Extraction is where a model can name an entity the

article does not contain, and everything downstream will then explain a connection that should not exist. The build already refuses an entity whose type is not in the ontology; it cannot refuse an entity that is well-typed and wrong. Until there is a check for that, a human reads the extraction diff.

- **The newsroom's rule is inherited, not re-implemented.** Every claim there walks back to

a frozen, hashed source. This site must carry those markers through to the audience outputs rather than dropping them in the rewrite — an audience-specific piece with no path back to the frozen bytes is exactly the black box this site argues against.

- **Translation is a claim.** The EN control output is a transcription of somebody else's

words and is checkable as one. Divergences between it and the five re-framed outputs are the site's own evidence that re-framing is not distortion, so it has to be right first.

- **The loop needs a stop.** A routine that publishes daily without anyone reading it will

eventually publish something wrong with full confidence and a provenance trail. The newsroom has a named human editor of record as the gate; this site should say who holds the equivalent before the routine is armed, not after.

**Done when** a scheduled Routine runs the eight steps end to end on one day's articles, the release it cuts passes CI, `verify-live.sh` confirms it, and the run record says which articles were extracted, which audiences each reached, and what a human changed.

## In progress 1

Claimed, with a role behind it.

`team/board/012-newsroom-brief.md`

### 012 · Brief filed to the pt.newsroom.sgit.ai team — four requests

doing task owner [librarian](roles/librarian.md) · opened 2026-09-15

`briefs/to-pt-newsroom-2026-09-15.md` is filed. Four requests, in value order, each saying whether we can work around it:

1. A JSON index of published articles with what changed. **We asked for the index rather than RSS** and said why: a feed answers "what is new" but still costs a fetch per article, and a full-content feed duplicates prose we would rather link to. 2. Carry `tem_prosa` into whatever index is exposed, so we stop inferring "has prose" from the existence of a file. 3. Keep `afirmacoes.json` beside each article and keep the `[[fonte:...]]` markers in the prose. We carry both into every audience output; without them a re-framed piece is an assertion with a nicer tone. 4. **The one worth more than the other three combined:** for each published article, the graph node ids it names. They already build a typed graph with named-inverse verbs and a source per node. Consuming their extraction instead of making our own removes the single most dangerous failure mode in this pipeline — a model inventing an entity, after which everything downstream explains a connection that does not exist, convincingly, with a provenance trail.

We also told them what we do NOT want: a generic article taxonomy designed to serve every downstream consumer, because the audience side has to be shaped by what an audience watches for and that is ours to get wrong.

**Done when** the brief has been read and each request has an answer — including "no", which is a fine answer and should be recorded here with its reason rather than left open.

## Held 4

Deliberately not shipping, with the reason on the card.

`team/board/001-read-state-schema.md`

### 001 · Publish read-state/v1 as a versioned schema with a validator

held task owner [architect](roles/architect.md) · opened 2026-09-14

`/read-state/` currently describes the shape in prose and one worked example. That is enough to argue with and not enough to build against.

Ship: a JSON Schema at `data/read-state.v1.schema.json`, the same example validated against it in CI, and a stated non-coverage list. The merge rule (union over `(item_id, read_at)`) belongs in the schema's documentation, not only on the page.

**Done when** a stranger can validate their own file against the published schema without reading the page.

---

**Held at v0.1.3.** This card belongs to the read-state argument the site made in v0.1.0 to v0.1.2, which has been superseded — see the release history. It is kept rather than deleted because the cards are the record of what the team was working on, and a board that quietly loses its history is worth less than one that shows a direction being abandoned. Reopen only if the read-state work is ever picked up in its own right.

`team/board/002-opml-importer.md`

### 002 · OPML to vault importer

held task owner [dev](roles/dev.md) · opened 2026-09-14

Take an OPML export from any reader and produce the `feeds/feeds.json` described on `/vault/`. Subscriptions only — OPML carries no read state, and the importer must not invent one. Items with no `xmlUrl` are dropped with a line on stderr, not silently.

Blocked by 001 only for the state half; the subscription half can ship first.

**Done when** `myfeeds import subscriptions.xml` produces a `feeds.json` that round-trips back to an OPML a reader will accept.

---

**Held at v0.1.3.** This card belongs to the read-state argument the site made in v0.1.0 to v0.1.2, which has been superseded — see the release history. It is kept rather than deleted because the cards are the record of what the team was working on, and a board that quietly loses its history is worth less than one that shows a direction being abandoned. Reopen only if the read-state work is ever picked up in its own right.

`team/board/003-verify-reader-exports.md`

### 003 · Check what each named reader actually exports, against its own docs

held task owner [qa](roles/qa.md) · opened 2026-09-14

Every sentence on this site about what a specific product does or does not export is currently marked `unverified`, because it was written from memory rather than from a primary source. That marker is honest; it is not a resting place.

For each reader this site names: find the vendor's own export documentation, record the URL and the date checked, list the fields the export carries, and move the sentence to sourced — or correct it.

**Done when** no `unverified` marker remains on `/read-state/` without a dated reason beside it.

---

**Held at v0.1.3.** This card belongs to the read-state argument the site made in v0.1.0 to v0.1.2, which has been superseded — see the release history. It is kept rather than deleted because the cards are the record of what the team was working on, and a board that quietly loses its history is worth less than one that shows a direction being abandoned. Reopen only if the read-state work is ever picked up in its own right.

`team/board/007-version-commit-hash.md`

### 007 · Record the commit a version was built from, not just its tag

held task owner [historian](roles/historian.md) · opened 2026-09-14

The estate's versions contract says a version must name the commit it was built from, or it cannot be verified later. `versions/<version>.json` currently carries `commit: null` and `commit_ref: refs/tags/<version>` instead.

The reason is real: the commit that *carries* a version cannot be known while that version is being built — it does not exist yet — and CI tags the release commit at publish time, so the tag is a durable pointer while a hash written at build time would either be wrong or change on every rebuild and break the staleness check.

**Held**, not open, because the obvious fixes are worse than the gap: capturing `git rev-parse HEAD` at build time records the *previous* commit under a field that claims to be this one, and having CI write the hash back means a CI-authored commit that exists only on the git side, which breaks the both-remotes-in-sync invariant.

**Reopen when** there is a way to fill `commit` that is true at the moment it is written — most likely the Historian backfilling the previous release's hash in the entry for the next one, which is honest and verifiable.

## Done 3

Closed, with the release that carried it.

`team/board/004-domain.md`

### 004 · myfeeds.sgit.ai does not resolve yet

done need owner [devops](roles/devops.md) · opened 2026-09-14

**Closed by v0.1.1, and not in the way this card expected.**

As opened: at v0.1.0 the subdomain had no certificate — a request to `https://myfeeds.sgit.ai/` failed TLS before reaching anything — and this was filed as a need only the human owner could supply, on the assumption that a DNS record was missing.

What actually happened: the DNS was already there (`myfeeds.sgit.ai` resolved to the same GitHub Pages addresses as every sibling site, which is consistent with a wildcard record on `sgit.ai` — *inferred from the resolution, not confirmed against the zone*). What was missing was Pages itself being switched on for this repository, so no certificate had ever been issued for the host. The v0.1.1 deploy job did that: `actions/configure-pages@v5` with `enablement: true`, plus the `CNAME` file in the repository root, and GitHub provisioned the certificate.

So the need was not a need. It was the deploy workflow this site did not have.

**Verified:** `admin/build/verify-live.sh` reports `myfeeds.sgit.ai is serving v0.1.1`; `index.md`, `llms.txt`, `versions/index.json`, `data/team.json` and `app.json` all return 200 with the right content types.

`team/board/008-v010-tag.md`

### 008 · v0.1.0 has no tag on the remote

done need owner [devops](roles/devops.md) · opened 2026-09-14

The `tag-release` job backfills a tag for every historical release. It created `v0.1.0` locally and could not push it: `GITHUB_TOKEN` cannot push a ref to a commit whose tree carries a different `.github/workflows` blob, and v0.1.0's tree carried the `build.yml` this release replaced.

The workflow names the remedy — `git push origin --tags` from a workflows-scoped human credential. That was attempted from this session and also rejected, with `HTTP 403`, so the session credential carries the same limit. `v0.1.1` is tagged; `v0.1.0` is not.

**Held**, not open, because nothing is broken: the release is identified by its commit subject and by `versions/v0.1.0.json`, and the missing tag is a bookkeeping gap rather than an outage — which is exactly the distinction the workflow is built around. Every future release tags normally, because their trees will carry the current workflow.

**Done when** somebody with a workflows-scoped token runs `git push origin --tags`, or the team decides the gap is permanent and says so here.

---

**Closed 2026-09-15: won't fix, and that is the right answer.**

The author's call: tagging works fine from v0.1.1 onward, and one missing historical tag is not worth a credential rotation. v0.1.0 remains identifiable by its commit subject and by `versions/v0.1.0.json`, which is what the versions contract actually requires — the tag was a convenience, not the record. Every release since has tagged normally because their trees carry the current workflow file.

Recorded rather than deleted, because "we decided not to" is a more useful thing for a future reader to find than silence.

`team/board/010-recover-remaining.md`

### 010 · Recover what the archive could not reach

done task owner [librarian](roles/librarian.md) · opened 2026-09-14

`admin/tools/wayback_archive.py` recovered 15 posts and 22 files from `mvp.myfeeds.ai` and recorded 9 URLs that its own sitemap named and no crawler ever captured. Two of those are writing rather than an index and are therefore genuinely lost from that source: `/about/` and `/ceo-news/`.

They may exist elsewhere. Places to look, in order of likelihood:

- the Ghost export or database backup, if one was kept;

- `the-cyber-boardroom/myfeeds-ai`, which generated the persona posts and may hold the

source of the pages too;

- LinkedIn, where several of these posts were cross-published — the recovered HTML carries

`?trk=article-ssr-frontend-pulse` parameters, which is evidence they were syndicated there;

- a second archive (archive.today, Bing or Google cache) that the Internet Archive's

index does not cover.

Also outstanding: the run used `--skip-assets`, so the **361 captured images are indexed in the manifest but not downloaded**. Every recovered post references images on the dead domain, so those links are currently decorative. Re-run without the flag to pull them, and decide separately whether to rewrite the posts to point at local copies — which makes them readable but stops them being verbatim.

**Done when** the two lost pages are either found or declared unrecoverable with the places checked listed, and the image question is decided either way on this card.

---

**Closed v0.1.8 — and the v0.1.7 update above this line was wrong about the numbers.**

The images are done, and "partly complete, re-run to finish" was a misreading of the count. Three different things were being added together:

|  |  |  |
|---|---|---|
| 92 | served from this repository | recovered, working |
| 16 | on the dead domain, **never captured by the Internet Archive** | re-running finds nothing |
| 51 | embedded from other publishers' CDNs | never part of that site at all |

The last group is the one that made the number look bad. The persona briefings quote Hacker News articles and embed the screenshots from the original publisher's image host — those were never on `mvp.myfeeds.ai`, so no archive of that site could ever have held them. They are not missing. They are somebody else's images, and they are now rendered as a link to the original rather than counted as a loss.

Of the 105 images the posts actually reference from the dead domain, **89 are here and 16 were never archived**. Those 16 are gone unless a copy exists outside the Internet Archive — most are DALL·E header images for the persona posts, which the MyFeeds engine repository may still hold.

**What was actually done**

- Archiver run without `--skip-assets`; 120 files pulled before archive.org's rate limiting

made further progress pointless.

- The archiver now honours `Retry-After` and paces the whole run rather than backing off

per file, because per-file exponential backoff is the wrong shape for a server that is telling you a specific number of seconds to wait.

- Each image renders as one of three honest states rather than one misleading one.

**What is left, and it is not this card:** the 16 never-archived images, if anyone wants to go looking in `the-cyber-boardroom/myfeeds-ai` for the originals. That is a new card if it matters, not an unfinished part of this one.

---

**Superseded update from v0.1.7, kept because it was published:**

**Update, v0.1.7 — images: partially done, and the finish is a re-run.**

The run used `--skip-assets`, so no images had been downloaded at all and every recovered post rendered a column of markdown source. Both halves are now fixed: the archiver was run without the flag, and the renderer was taught image syntax (see the release note — it had never handled `![](url)`, because the inline link rule required non-empty link text).

At the time of this release the Internet Archive is throttling and the download is **partly complete**. The exact split is printed by the validator on every build — look for the `recovered images:` note — and shown on each post as an explicit "image not recovered" marker rather than a broken image, so the gap is visible rather than inferred.

**To finish it:** re-run the same command. The archiver skips files already present, so it resumes rather than restarting.

```
python3 admin/tools/wayback_archive.py mvp.myfeeds.ai --out back-office/archive --delay 0.25
python3 admin/build/build_pages.py && node admin/build/validate.js
```

**Decided:** the images are served from this repository and the original URL is kept in each image's `title`. The earlier position — leave references pointing at the dead domain so the archive stays verbatim — was wrong in practice: it produced an archive nobody could read. Rewriting a reference and recording it is evidence; rewriting and hiding it is not.

[← The team](index.md)[Starting prompts →](prompts.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/team/board.html)*
