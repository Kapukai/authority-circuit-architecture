#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("registry", PACKAGE / "scripts" / "registry.py")
registry = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(registry)

data = registry.load()
registry.verify(data)
assert registry.next_child(data, "ACA-120") == "ACA-121"

duplicate = copy.deepcopy(data)
duplicate["entries"].append(copy.deepcopy(duplicate["entries"][0]))
try:
    registry.verify(duplicate)
    raise AssertionError("duplicate identifier was accepted")
except SystemExit as exc:
    assert "duplicate ACA identifier" in str(exc)

agent_schema = json.loads((PACKAGE / "agent-proposal.schema.json").read_text())
assert "id" not in agent_schema["properties"]
assert "allocation_state" not in agent_schema["properties"]
assert agent_schema["additionalProperties"] is False

work_schema = json.loads((PACKAGE / "work-package.schema.json").read_text())
assert work_schema["properties"]["human_acceptance_required"]["const"] is True
assert work_schema["properties"]["authorized_by"]["const"] == "Human Chief Architect"

print("PASS: registry collision, hierarchy, agent boundary, and work-package tests")
