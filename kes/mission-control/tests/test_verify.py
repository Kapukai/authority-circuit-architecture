import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_program_state_has_unique_items_and_valid_dependencies():
    data = json.loads((ROOT / "examples" / "program-state.json").read_text(encoding="utf-8"))
    ids = [item["id"] for item in data["items"]]
    assert len(ids) == len(set(ids))
    known = set(ids)
    assert all(edge["from"] in known and edge["to"] in known for edge in data["dependencies"])
    assert data["next_authorized_work"]["id"] in known


def test_dashboard_preserves_read_only_limitation():
    html = (ROOT / "app" / "index.html").read_text(encoding="utf-8")
    assert "Read-only program control plane" in html
    assert "does not authorize, merge, publish, deploy" in html
