#!/usr/bin/env python3
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "examples" / "authority-cell.generated.json"
if not p.exists():
    raise SystemExit("FAIL: run generate_views.py first")

data = json.loads(p.read_text())
cell = data["cell"]
nodes = {n["id"] for n in cell["nodes"]}
edges = {e["id"] for e in cell["edges"]}
sources = {s["id"] for s in cell["sources"]}

if len(nodes) != len(cell["nodes"]): raise SystemExit("FAIL: duplicate node ID")
if len(edges) != len(cell["edges"]): raise SystemExit("FAIL: duplicate edge ID")
if len(sources) != len(cell["sources"]): raise SystemExit("FAIL: duplicate source ID")

for e in cell["edges"]:
    if e["from"] not in nodes or e["to"] not in nodes:
        raise SystemExit(f"FAIL: edge {e['id']} references unknown node")

for s in cell["sources"]:
    if hashlib.sha256(s["exact_quote"].encode()).hexdigest() != s["sha256"]:
        raise SystemExit(f"FAIL: source hash mismatch {s['id']}")
    if s.get("interpretation") == s["exact_quote"]:
        raise SystemExit(f"FAIL: quotation and interpretation collapsed {s['id']}")

required = {"derivation","citation","transition","challenge","timeline"}
if set(data["projections"]) != required:
    raise SystemExit("FAIL: projection set mismatch")

for name, view in data["projections"].items():
    if view["cell_id"] != cell["cell_id"]:
        raise SystemExit(f"FAIL: {name} cell mismatch")
    if set(view["node_refs"]) - nodes or set(view["edge_refs"]) - edges:
        raise SystemExit(f"FAIL: {name} unknown canonical reference")

print("PASS: ACA-121–127 canonical graph and projections verified")
