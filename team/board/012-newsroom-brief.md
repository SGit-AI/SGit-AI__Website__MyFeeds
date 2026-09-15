---
id: 012
title: Brief filed to the pt.newsroom.sgit.ai team — four requests
status: doing
owner: librarian
kind: task
opened: 2026-09-15
---

`briefs/to-pt-newsroom-2026-09-15.md` is filed. Four requests, in value order, each saying
whether we can work around it:

1. A JSON index of published articles with what changed. **We asked for the index rather
   than RSS** and said why: a feed answers "what is new" but still costs a fetch per
   article, and a full-content feed duplicates prose we would rather link to.
2. Carry `tem_prosa` into whatever index is exposed, so we stop inferring "has prose" from
   the existence of a file.
3. Keep `afirmacoes.json` beside each article and keep the `[[fonte:...]]` markers in the
   prose. We carry both into every audience output; without them a re-framed piece is an
   assertion with a nicer tone.
4. **The one worth more than the other three combined:** for each published article, the
   graph node ids it names. They already build a typed graph with named-inverse verbs and a
   source per node. Consuming their extraction instead of making our own removes the single
   most dangerous failure mode in this pipeline — a model inventing an entity, after which
   everything downstream explains a connection that does not exist, convincingly, with a
   provenance trail.

We also told them what we do NOT want: a generic article taxonomy designed to serve every
downstream consumer, because the audience side has to be shaped by what an audience watches
for and that is ours to get wrong.

**Done when** the brief has been read and each request has an answer — including "no",
which is a fine answer and should be recorded here with its reason rather than left open.
