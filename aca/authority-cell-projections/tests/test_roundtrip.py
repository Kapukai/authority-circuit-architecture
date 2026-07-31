#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT/"examples/authority-cell.generated.json").read_text())
nodes = {n["id"] for n in data["cell"]["nodes"]}
edges = {e["id"] for e in data["cell"]["edges"]}
rn = set().union(*(set(v["node_refs"]) for v in data["projections"].values()))
re = set().union(*(set(v["edge_refs"]) for v in data["projections"].values()))
assert rn == nodes
assert re == edges
print("PASS: test_roundtrip.py")
