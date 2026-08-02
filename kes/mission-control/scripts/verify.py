#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "examples" / "program-state.json"
REQUIRED_TOP = {"schema_version", "generated_at", "program", "items", "dependencies", "risks", "critical_path", "next_authorized_work"}
VALID_STATES = {"PROPOSED","AUTHORIZED","IN_PROGRESS","BLOCKED","VERIFIED","ACCEPTED","RELEASED","DEFERRED","SUPERSEDED","WITHDRAWN","INDETERMINATE"}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> None:
    data = json.loads(STATE.read_text(encoding="utf-8"))
    missing = REQUIRED_TOP - data.keys()
    if missing:
        fail(f"missing top-level fields: {sorted(missing)}")
    if data.get("schema_version") != "0.1":
        fail("unsupported schema_version")
    ids = []
    for item in data["items"]:
        for field in ("id", "name", "family", "state", "owner", "verification_state", "publication_state"):
            if field not in item:
                fail(f"item missing {field}: {item}")
        if item["state"] not in VALID_STATES:
            fail(f"invalid state for {item['id']}: {item['state']}")
        ids.append(item["id"])
    if len(ids) != len(set(ids)):
        fail("duplicate item IDs")
    known = set(ids)
    for edge in data["dependencies"]:
        if edge.get("from") not in known or edge.get("to") not in known:
            fail(f"broken dependency: {edge}")
    next_id = data["next_authorized_work"].get("id")
    if next_id not in known:
        fail(f"next authorized work is not a tracked item: {next_id}")
    if next_id not in data["critical_path"]:
        fail("next authorized work is not on the critical path")
    required_files = [
        ROOT / "README.md",
        ROOT / "mission-control.schema.json",
        ROOT / "app" / "index.html",
        ROOT / "docs" / "WORK_ORDER.md",
        ROOT / "docs" / "ADR-0004.md",
        ROOT / "docs" / "THREAT_MODEL.md",
        ROOT / "docs" / "ACCEPTANCE_PLAN.md",
    ]
    absent = [str(p.relative_to(ROOT)) for p in required_files if not p.exists()]
    if absent:
        fail(f"missing required files: {absent}")
    print(f"PASS: {len(ids)} program items, {len(data['dependencies'])} dependencies, {len(data['risks'])} risks verified")


if __name__ == "__main__":
    main()
