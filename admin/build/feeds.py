"""The audience/ontology/join data, loaded for the site pages.

Source of truth is `admin/content/data/`; the build validates it, renders it, and copies
it to `data/` and `api/v1/` so an agent can fetch the same facts the pages show. The
copy is deliberate: a page that shows a number a reader cannot fetch is asking to be
trusted.
"""

from __future__ import annotations

import json
from pathlib import Path

SRC = "admin/content/data"


def load_all(root: Path) -> dict:
    src = root / SRC
    audiences = json.loads((src / "audiences.json").read_text(encoding="utf-8"))
    ontology = json.loads((src / "ontology.json").read_text(encoding="utf-8"))

    articles = []
    for f in sorted((src / "articles").glob("*.json")):
        articles.append(json.loads(f.read_text(encoding="utf-8")))

    joins = {}
    jdir = root / "data" / "joins"
    if jdir.exists():
        for f in sorted(jdir.glob("*.json")):
            j = json.loads(f.read_text(encoding="utf-8"))
            joins[j["article"]] = j

    before = None
    bf = src / "findings" / "join-v1-before.json"
    if bf.exists():
        before = json.loads(bf.read_text(encoding="utf-8"))

    # Cross-check: every type a concern names must exist in the article ontology, or the
    # concern can never fire and the audience quietly looks uninterested in everything.
    known = {t["id"] for t in ontology["article"]["types"]}
    for a in audiences["audiences"]:
        for c in a["concerns"]:
            for t in c["match"] + c.get("requires", []):
                if t not in known:
                    raise SystemExit(
                        f"build: audience {a['id']} concern {c['id']} names article type "
                        f"{t!r}, which the ontology does not define"
                    )

    return {"audiences": audiences, "ontology": ontology,
            "articles": articles, "joins": joins, "before": before}
