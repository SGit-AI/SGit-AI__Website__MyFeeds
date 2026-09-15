#!/usr/bin/env python3
"""What the corpus says about the ontology — the list a human is asked to settle.

    python3 admin/tools/review.py

The audience side of this system is written by hand (today, by a model) and starts
wrong. It does not have to be right; it has to be **wrong in ways somebody can see and
correct**. That is what this produces: not a quality score, but a list of specific,
evidenced questions, each naming the concern, the articles involved, and what a human
answering it would change.

Three shapes of defect only appear across a corpus, which is why one article was not
enough and three already are:

- **A tautology.** A concern satisfied by every article carries no information into the
  ranking and makes its audience look interested in everything.
- **An unmaintained concern.** A concern that never fires is either wrong about the
  corpus or about the audience, and nobody will notice which.
- **An undiscriminating audience.** An audience that receives everything is not an
  audience; it is a mailing list with extra steps.

Every finding is a question with an owner, not an automatic fix. The formula stays as it
is until a human says otherwise, and the answer is recorded next to the question.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    audiences = json.loads((ROOT / "admin/content/data/audiences.json").read_text(encoding="utf-8"))
    joins = [json.loads(f.read_text(encoding="utf-8"))
             for f in sorted((ROOT / "data" / "joins").glob("*.json"))]
    n = len(joins)
    if not n:
        raise SystemExit("review: no joins in data/joins/ — run join.py first")

    fired: dict[tuple[str, str], list[str]] = defaultdict(list)
    reached: dict[str, list[str]] = defaultdict(list)
    for j in joins:
        for d in j["deliveries"]:
            if d["verdict"] == "reached":
                reached[d["audience"]].append(j["article"])
            for c in d.get("connections", []):
                fired[(d["audience"], c["concern"])].append(j["article"])

    findings = []
    for a in audiences["audiences"]:
        if a.get("control"):
            continue
        got = reached.get(a["id"], [])
        if len(got) == n and n >= 3:
            # Report the whole distribution rather than guessing a single culprit. A
            # max-of-counts heuristic was tried first and named the wrong concern: the one
            # that fires most is not the one that fired on the article that should not
            # have been delivered. Three numbers let a human find it instantly; one wrong
            # answer sends them looking in the wrong place.
            counts = {c["id"]: len(set(fired.get((a["id"], c["id"]), [])))
                      for c in a["concerns"]}
            coarse = [c["id"] for c in a["concerns"] if counts[c["id"]]
                      and set(c["match"]) & {"Organisation", "Event", "Source", "Claim"}]
            findings.append({
                "diagnosis": {
                    "fire_counts": counts, "of": n, "coarse_types": coarse,
                    "note": (
                        "Concerns matching a coarse type fire on things the concern did "
                        "not mean: Organisation covers a startup and a government "
                        "department equally, and Event covers a conference and an "
                        "incident. Where a concern above fired on an article you would "
                        "not have sent, the coarse type is the first place to look."
                        if coarse else
                        "No obviously coarse type is involved; the concerns may simply "
                        "all be right for this corpus."
                    ),
                },
                "proposed_by": "model",
                "id": f"aud-everything-{a['id']}",
                "kind": "audience-receives-everything",
                "audience": a["id"], "concern": None,
                "articles": got,
                "question": (
                    f"{a['name']} received all {n} articles. Is that right for this "
                    f"corpus, or is one of its concerns too broad?"
                ),
                "would_change": "Narrowing or qualifying the concern that fires most often.",
                "status": "open",
            })
        if not got and n >= 3:
            findings.append({
                "id": f"aud-nothing-{a['id']}",
                "kind": "audience-receives-nothing",
                "audience": a["id"], "concern": None, "articles": [],
                "question": (
                    f"{a['name']} received none of the {n} articles. Is this corpus simply "
                    f"not for them, or are its concerns written for material this newsroom "
                    f"does not publish?"
                ),
                "would_change": "Either accept it, or rewrite the concerns against real articles.",
                "status": "open",
            })
        for c in a["concerns"]:
            hits = fired.get((a["id"], c["id"]), [])
            if len(set(hits)) == n and n >= 3:
                findings.append({
                    "id": f"tautology-{a['id']}-{c['id']}",
                    "kind": "concern-fires-on-everything",
                    "audience": a["id"], "concern": c["id"],
                    "articles": sorted(set(hits)),
                    "question": (
                        f"“{c['label']}” fired on all {n} articles. A concern satisfied by "
                        f"everything carries no information. Is it too broad, or is this "
                        f"corpus unusually uniform?"
                    ),
                    "would_change": f"Qualifying it, or narrowing {c['match']}.",
                    "status": "open",
                })
            if not hits and n >= 3:
                findings.append({
                    "id": f"silent-{a['id']}-{c['id']}",
                    "kind": "concern-never-fires",
                    "audience": a["id"], "concern": c["id"], "articles": [],
                    "question": (
                        f"“{c['label']}” has never fired in {n} articles. Is it waiting for "
                        f"material this newsroom has not published yet, or is it looking for "
                        f"types the extraction never produces?"
                    ),
                    "would_change": "Either keep it and say what it is waiting for, or replace it.",
                    "status": "open",
                })

    out = {
        "id": "myfeeds-review",
        "note": ("Open questions about the ontology, computed from the corpus. Not a "
                 "quality score: a list of things a human is being asked to settle. The "
                 "system does not change itself in response to these."),
        "corpus": {"articles": n, "slugs": [j["article"] for j in joins]},
        "counts": {
            "open": sum(1 for f in findings if f["status"] == "open"),
            "by_kind": {k: sum(1 for f in findings if f["kind"] == k)
                        for k in {f["kind"] for f in findings}},
        },
        "findings": findings,
    }
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data" / "review.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"corpus: {n} articles")
    for f in findings:
        print(f"  [{f['kind']}] {f['audience']}"
              + (f"/{f['concern']}" if f["concern"] else ""))
        print(f"      {f['question']}")
    print(f"\n{len(findings)} open question(s) -> data/review.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
