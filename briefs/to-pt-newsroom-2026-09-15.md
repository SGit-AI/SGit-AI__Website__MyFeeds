# Brief to the pt.newsroom.sgit.ai team

**From:** myfeeds.sgit.ai · **Date:** 2026-09-15 · **Status:** request, not a complaint

myfeeds.sgit.ai reads your published articles and puts each in front of six audiences with
the reasoning attached. Three of your articles are running through it today. This brief
asks for four things that would make that consumption cheaper and more honest, in the order
we would value them — and says plainly which of them we can work around and which we
cannot.

Everything below is a request from a downstream consumer. None of it is a defect in your
site, and the convention we are following is yours: link, never reproduce.

---

## 1. A machine-readable list of published articles, with what changed

**What we do now.** Clone the repository and walk `artigos/**/artigo.json`. It works and
it is honest — the data is right there — but it means a full clone to answer "what is new
since yesterday", which is the only question a daily routine actually asks.

**What would help.** Either of these, and the first is plenty:

- `api/v1/articles.json` populated with published articles — it exists and is currently
  empty of them (it serves the `historias` shape). Fields we would use: `slug`, `date`,
  `seccao`, `titulo`, `estado`, `url`, and the verification counts.
- An RSS or Atom feed of published articles.

**Would RSS help?** Yes, and less than you might think. A feed is the right shape for
"tell me what is new" and we would use it for exactly that. But a feed that carries only
titles and links still costs us a fetch per article, and a feed that carries full content
duplicates prose you would rather we linked to. **Our preference is the JSON index, not
RSS** — a list of slugs with dates and states, from which we fetch only what changed. If
you are adding one thing, add that.

*Workaround if you do not:* the clone. Cheap enough at six articles, annoying at six
hundred.

## 2. Stable identifiers, and a signal when prose lands

**The problem we have.** `estado` moves from `procurado` to `verificado` to published, and
three of your six articles today are commissioned with no prose yet. We cannot tell from
the data alone when an article has become readable — we look for `artigo.md` existing,
which is an inference about your file layout rather than a fact you published.

**What would help.** A field that says it: `tem_prosa` already exists in
`dados/historias.json` and is exactly right. Carrying it into whatever index you expose
would let us stop guessing.

*Workaround:* we check for the file. It will break the first time you reorganise.

## 3. The claims, as data, next to the article

**This one we would value most and it already exists.** `afirmacoes.json` — each claim,
its frozen source, its verification state, and what was re-found in the bytes — is the
single most useful artefact on your site for what we do, because it is what lets an
audience-specific rewrite keep a path back to the frozen bytes. Without it, a re-framed
article is just an assertion with a nicer tone.

**The request is only:** please keep it beside the article rather than only in an
aggregate, and please keep the `[[fonte:...]]` markers in the prose. We carry both
through into every audience output. An audience-specific piece with no path back to a hash
is precisely the black box our site exists to argue against, so if we ever have to drop
them, we would rather not publish the piece.

## 4. Would article-level ontologies or graphs help?

**Honestly: only if they are yours, not ours.** You asked whether more ontologies,
taxonomies or graphs for articles would help. The answer splits:

- **Your entity extraction, if you publish it — yes, very much.** You already build
  `dados/grafo.json` with typed nodes, named-inverse verbs and a source on every node.
  If a published article carried *which of those nodes it names*, we would stop
  re-extracting entities ourselves. **That is worth more to us than everything else in
  this brief combined**, because extraction is the one step in our pipeline where a model
  can invent something, and everything downstream then explains a connection that does not
  exist, convincingly and with a provenance trail. Consuming your extraction instead of
  making our own removes that failure mode entirely.
- **A generic article taxonomy — no, please do not.** Our audience side needs types shaped
  by what an audience watches for, and that is our problem to get wrong, not yours. A
  taxonomy designed to serve every downstream consumer serves none of them.

**The concrete ask,** if you want one sentence: *for each published article, list the
graph node ids it names.* Nothing new has to be modelled; it is a join you already have
internally.

---

## What we are doing at our end regardless

- Our article ontology, audience ontology and join formula are published at
  `myfeeds.sgit.ai/ontology/`, and every classification is shown with its working out at
  `/explain/`. If our reading of one of your articles is wrong, it is wrong in public with
  the reasoning visible, which is the easiest kind to correct.
- Our extraction is currently AI-generated and unreviewed, and every page says so. We are
  not asking you to trust it.
- We copy nothing. Articles are linked; claims and source markers are carried through;
  your frozen snapshots stay yours.

**One thing we would ask you to correct us on:** your site's own rule is that every claim
walks back to frozen bytes. If you see an audience output of ours that has lost that path,
that is a bug on our side and we would like to hear about it before a reader does.
