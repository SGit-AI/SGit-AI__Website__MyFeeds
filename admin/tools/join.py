#!/usr/bin/env python3
"""join/v1 — decide which audiences an article reaches, and say why it did not reach the rest.

    python3 admin/tools/join.py admin/content/data/articles/<slug>.json

This is the published formula from `admin/content/data/ontology.json`, executed rather
than described. Given an article's extracted entities and the audience definitions, it
emits one Delivery per audience — reached or withheld — each carrying the Connections that
produced it, the match type and weight of each, and a sentence that reads in both
directions.

Two design points worth knowing before changing anything:

**A withheld delivery is a result.** Every audience gets a Delivery whether or not the
article reached it, and a withheld one records which concerns were tried and why each
failed. Any system can explain what it chose; explaining what it rejected is the half a
reader actually doubts.

**This does not replace the model.** In the running pipeline, stage 3 is an LLM comparing
an article graph against a persona graph, and it proposes matches this code could not — a
consequence two hops away, a synonym, an implication. What this formula does is constrain
the SHAPE of what comes back: every match, however proposed, is recorded with its two
endpoints, its type, its weight and its sentence, so a human can disagree with any single
one. Where both sides are the same concept id, no model is needed and the match is simply
computed, which is what happens below.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "admin" / "content" / "data"


def load(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def match_entity(entity: dict, concern: dict, taxonomy: dict) -> dict | None:
    """One entity against one concern. Returns the strongest match or None.

    Only `exact` and the taxonomy hops are computable here. `consequence` matches come
    from the model in the real pipeline; where an article file carries them explicitly
    they are passed through with their stated path, and the path is what a reader checks.
    """
    etype = entity["type"]
    for wanted in concern["match"]:
        if etype == wanted:
            return {"match": "exact", "weight": 3, "wanted": wanted}
        if taxonomy.get(etype) == wanted:
            return {"match": "narrower", "weight": 2, "wanted": wanted}
        if taxonomy.get(wanted) == etype:
            return {"match": "broader", "weight": 1, "wanted": wanted}
    return None


def join(article: dict, audiences: dict, ontology: dict) -> dict:
    taxonomy = ontology["article"].get("taxonomy", {})
    known = {t["id"] for t in ontology["article"]["types"]}
    for e in article["entities"]:
        if e["type"] not in known:
            raise SystemExit(
                f"join: entity {e['id']!r} has type {e['type']!r}, which is not in the "
                f"article ontology. Add the type deliberately or fix the extraction; do "
                f"not let an unknown type through, because it can never match anything "
                f"and the article will look uninteresting rather than unreadable."
            )

    deliveries = []
    for aud in sorted(audiences["audiences"], key=lambda a: a["order"]):
        if aud.get("control"):
            deliveries.append({
                "audience": aud["id"], "audience_name": aud["name"],
                "verdict": "reached", "rank": None, "control": True,
                "connections": [],
                "because": "The control audience. Every article reaches it and no "
                           "selection runs — it is the baseline the other audiences' "
                           "output is compared against.",
            })
            continue

        present = {e["type"] for e in article["entities"]}
        connections, tried = [], []
        for concern in aud["concerns"]:
            need = concern.get("requires")
            if need and not (present & set(need)):
                tried.append({
                    "concern": concern["id"], "label": concern["label"],
                    "wanted": concern["match"], "hits": 0, "qualified_out": True,
                    "why_not": (
                        f"this concern only applies where the article is also about "
                        f"{' or '.join(need)}, and this one is not"
                    ),
                })
                continue
            hits = []
            for entity in article["entities"]:
                m = match_entity(entity, concern, taxonomy)
                if not m:
                    continue
                hits.append({
                    "entity": entity["id"], "entity_label": entity["label"],
                    "entity_type": entity["type"],
                    "concern": concern["id"], "concern_label": concern["label"],
                    "match": m["match"], "weight": m["weight"],
                    "reads": (
                        f"{aud['name']} watches {concern['label'].lower()}; "
                        f"the article names {entity['label']}, which is a "
                        f"{entity['type']}."
                    ),
                    "reads_inverse": (
                        f"{entity['label']} satisfies {concern['label'].lower()}, "
                        f"which {aud['name'].lower()} watches."
                    ),
                })
            connections += hits
            tried.append({
                "concern": concern["id"], "label": concern["label"],
                "wanted": concern["match"], "hits": len(hits),
                "why_not": None if hits else
                f"this article has no {' or '.join(concern['match'])} in it",
            })

        # Explicit consequence connections, proposed by the model in the real pipeline
        # and carried in the article file with the path that justifies them.
        for c in article.get("consequence_connections", []):
            if c["audience"] != aud["id"]:
                continue
            connections.append({**c, "match": "consequence", "weight": 2,
                                "proposed_by": c.get("proposed_by", "model")})

        reached = len(connections) >= 1
        # Rank counts each ENTITY once, at its best match. Summing every connection let
        # one entity score repeatedly through overlapping concerns: on the first article
        # this formula ever ran against, a Discrepancy matched two of the executive's
        # concerns and scored twice, putting an event-logistics story above the audience
        # whose event it was. The connections are all still listed — the double match is
        # real and worth seeing — but it is one entity, so it counts once.
        best: dict[str, int] = {}
        for c in connections:
            key = c.get("entity", c.get("id", ""))
            best[key] = max(best.get(key, 0), c["weight"])
        deliveries.append({
            "audience": aud["id"], "audience_name": aud["name"],
            "verdict": "reached" if reached else "withheld",
            "rank": sum(best.values()) if reached else 0,
            "rank_note": "each entity counted once, at its strongest match",
            "connections": connections,
            "tried": tried,
            "because": (
                f"{len(connections)} connection(s) from "
                f"{len({c['concern'] for c in connections})} concern(s)."
                if reached else
                "None of the concerns this audience watches were satisfied: "
                + "; ".join(t["why_not"] for t in tried if t["why_not"]) + "."
            ),
        })

    return {
        "article": article["slug"],
        "title": article["title"],
        "formula": ontology["join"]["formula"]["id"],
        "entity_types": sorted({e["type"] for e in article["entities"]}),
        "deliveries": deliveries,
        "summary": {
            "reached": [d["audience"] for d in deliveries if d["verdict"] == "reached"],
            "withheld": [d["audience"] for d in deliveries if d["verdict"] == "withheld"],
        },
    }


def findings(result: dict, audiences: dict, articles_seen: int = 1) -> list[dict]:
    """What the run says about the ONTOLOGY rather than about the article.

    The audience side is maintained by hand and starts wrong; this is how it gets better.
    A concern that fires on everything is not a concern, and a concern that never fires
    is not being maintained — both are invisible until something looks for them.
    """
    out = []
    for d in result["deliveries"]:
        if d.get("control"):
            continue
        for t in d.get("tried", []):
            if t["hits"] and "Source" in t["wanted"]:
                out.append({
                    "kind": "concern-too-broad",
                    "audience": d["audience"], "concern": t["concern"],
                    "note": "This concern matches on Source, and every article that "
                            "follows the freeze-before-you-cite rule has Sources. A "
                            "concern satisfied by every article is a tautology: it "
                            "makes the audience look interested in everything and "
                            "carries no information into the ranking.",
                })
    ranks = {d["audience"]: d["rank"] for d in result["deliveries"] if d["rank"]}
    if ranks:
        top = max(ranks, key=lambda k: ranks[k])
        out.append({
            "kind": "ranking-observation",
            "audience": top, "concern": None,
            "note": f"Ranked highest ({ranks[top]}) for this article. Worth a human "
                    f"glance: a rank that surprises you is either a real finding or a "
                    f"concern that is too broad, and only reading the connections tells "
                    f"you which.",
        })
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    article = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    audiences, ontology = load("audiences.json"), load("ontology.json")
    result = join(article, audiences, ontology)
    result["findings"] = findings(result, audiences)

    for d in result["deliveries"]:
        mark = "→" if d["verdict"] == "reached" else "×"
        rank = f"rank {d['rank']}" if d["rank"] else ("control" if d.get("control") else "—")
        print(f"{mark} {d['audience_name']:<24} {rank:<10} {d['because'][:78]}")
        for c in d["connections"]:
            print(f"    [{c['match']}/{c['weight']}] {c['reads']}")
    if result["findings"]:
        print("\nfindings about the ontology:")
        for f in result["findings"]:
            print(f"  · {f['kind']}: {f['audience']}"
                  + (f"/{f['concern']}" if f["concern"] else ""))

    out = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                       encoding="utf-8")
        print(f"\nwrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
