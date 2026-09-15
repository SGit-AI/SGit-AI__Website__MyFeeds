# What a human is being asked to settle

> The ontologies do not have to be right; they have to be wrong in ways somebody can see and correct. The open questions the corpus raised, each with its evidence and what an answer would change — and nothing on the page fixes itself.

*Source: <https://myfeeds.sgit.ai/review/index.html> · site v0.1.7 · this file is generated from the same content as
the page, so the two cannot drift. Every page on this site has a `.md` twin; internal
links below point at them.*

---

The feedback loop

# What a human is being asked to settle

The ontologies here do not have to be right. They have to be **wrong in ways somebody can see and correct** — which is a different and much more achievable target, and the only one available to a system whose classifications are written by a model. This page is the output of that principle: not a quality score, but 9 specific questions, each with the evidence that raised it and what an answer would change.

**Nothing on this page fixes itself.** The formula does not change in response to these questions. A model proposing a diagnosis and then acting on it is the same closed loop this site exists to argue against — so the questions sit here until a person answers them, and the answer is recorded next to the question.

## The corpus these came from

3 articles from [pt.newsroom.sgit.ai](https://pt.newsroom.sgit.ai/). That is a small corpus and the questions below reflect it: several concerns have never fired, and with three articles the honest reading is usually "this newsroom has not published that kind of thing yet" rather than "the concern is wrong". Both answers are useful and only a human can tell them apart.

- `dois-nomes-para-os-mesmos-palcos`

- `registo-nacional-nao-devolve-texto`

- `uma-captura-nao-mostra-movimento`

## The 9 open questions

### An audience that receives everything 1

open startups

**The founder received all 3 articles. Is that right for this corpus, or is one of its concerns too broad?**

**The model's own diagnosis, which is a proposal and not a finding:** fired on — `funding-programme` 0, `event` 2, `peer-company` 1, `small-company-rule` 0 (of 3 articles). Concerns matching a coarse type fire on things the concern did not mean: Organisation covers a startup and a government department equally, and Event covers a conference and an incident. Where a concern above fired on an article you would not have sent, the coarse type is the first place to look.

**Answering it would change:** Narrowing or qualifying the concern that fires most often.

**Articles:** `dois-nomes-para-os-mesmos-palcos`, `registo-nacional-nao-devolve-texto`, `uma-captura-nao-mostra-movimento`

### A concern that has never fired 8

open startups · funding-programme

**“Funding programmes and calls” has never fired in 3 articles. Is it waiting for material this newsroom has not published yet, or is it looking for types the extraction never produces?**

**Answering it would change:** Either keep it and say what it is waiting for, or replace it.

open startups · small-company-rule

**“Obligations that bind small companies” has never fired in 3 articles. Is it waiting for material this newsroom has not published yet, or is it looking for types the extraction never produces?**

**Answering it would change:** Either keep it and say what it is waiting for, or replace it.

open investors · policy-direction

**“Policy and regulatory direction” has never fired in 3 articles. Is it waiting for material this newsroom has not published yet, or is it looking for types the extraction never produces?**

**Answering it would change:** Either keep it and say what it is waiting for, or replace it.

open investors · capital-flow

**“Money entering or leaving” has never fired in 3 articles. Is it waiting for material this newsroom has not published yet, or is it looking for types the extraction never produces?**

**Answering it would change:** Either keep it and say what it is waiting for, or replace it.

open c-level · financial-consequence

**“Cost, revenue and exposure in money” has never fired in 3 articles. Is it waiting for material this newsroom has not published yet, or is it looking for types the extraction never produces?**

**Answering it would change:** Either keep it and say what it is waiting for, or replace it.

open cybersecurity · control-action

**“Something to change on a system” has never fired in 3 articles. Is it waiting for material this newsroom has not published yet, or is it looking for types the extraction never produces?**

**Answering it would change:** Either keep it and say what it is waiting for, or replace it.

open cybersecurity · integrity

**“Whether published information can be trusted” has never fired in 3 articles. Is it waiting for material this newsroom has not published yet, or is it looking for types the extraction never produces?**

**Answering it would change:** Either keep it and say what it is waiting for, or replace it.

open risk · obligation

**“Duties, and who they bind” has never fired in 3 articles. Is it waiting for material this newsroom has not published yet, or is it looking for types the extraction never produces?**

**Answering it would change:** Either keep it and say what it is waiting for, or replace it.

## How to answer one

Every question has an id. An answer is a line in `admin/content/data/review-answers.json` naming the question, the person, the date and what they decided — and, where the answer changes the ontology, the change lands in the same release as the answer so the two cannot drift. There is no form on this page and no comment box: the answers version with the repository, like everything else here.

```
{
  "question": "aud-everything-startups",
  "answered_by": "<name>",
  "date": "2026-09-__",
  "decision": "keep | narrow | qualify | replace",
  "because": "<one sentence a stranger could check>"
}
```

## As data

[`/data/review.json`](../data/review.json) — regenerate with `python3 admin/tools/review.py` after any join run.

[← Who wrote this site](../provenance/index.md) [The debug view →](../explain/index.md) [The audiences →](../audiences/index.md)

---

*[Site index for agents](../llms.txt) · [HTML version](https://myfeeds.sgit.ai/review/index.html)*
