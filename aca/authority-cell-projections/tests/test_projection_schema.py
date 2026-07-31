#!/usr/bin/env python3
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT/"projection.schema.json").read_text())
data = json.loads((ROOT/"examples/authority-cell.generated.json").read_text())
assert schema["title"] == "ACA Authority Cell Projection Package"
assert data["schema_version"] == "ACA-121-127-draft-0.1"
assert {"derivation","citation","transition","challenge","timeline"} == set(data["projections"])
print("PASS: test_projection_schema.py")
