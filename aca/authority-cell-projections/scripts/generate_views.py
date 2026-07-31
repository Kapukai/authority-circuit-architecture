#!/usr/bin/env python3
import json, sys
from pathlib import Path

KINDS = {
    "derivation":"ACA-122",
    "citation":"ACA-123",
    "transition":"ACA-124",
    "challenge":"ACA-126",
    "timeline":"ACA-127",
}

if len(sys.argv) != 3:
    raise SystemExit("usage: generate_views.py INPUT OUTPUT")

src, dst = map(Path, sys.argv[1:3])
data = json.loads(src.read_text())
cell = data["cell"]
nodes = [n["id"] for n in cell["nodes"]]
edges = [e["id"] for e in cell["edges"]]

data["projections"] = {
    kind: {
        "projection_id": f"{cell['evaluation_id']}:{kind}",
        "kind": kind,
        "standard": standard,
        "cell_id": cell["cell_id"],
        "node_refs": nodes,
        "edge_refs": edges if kind != "citation" else [],
        "findings": []
    }
    for kind, standard in KINDS.items()
}
dst.write_text(json.dumps(data, indent=2) + "\n")
print(f"PASS: generated {len(data['projections'])} projections")
