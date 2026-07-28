import json
from pathlib import Path
import pytest
from kapu.engine import evaluate,replay
R=Path(__file__).resolve().parents[1]
def load(n): return json.loads((R/"examples"/n).read_text())
@pytest.mark.parametrize("f,s",[("allow.json","ALLOW"),("hold-unknown.json","HOLD"),("conflict.json","CONFLICT"),("revoked.json","REVOKED"),("deny.json","DENY")])
def test_states(f,s): assert evaluate(load(f))["state"]==s
def test_authorization_not_execution():
    d=evaluate(load("allow.json")); assert d["authorization"]["authorized"] and not d["execution"]["executed"]
def test_remedy_attached(): assert evaluate(load("hold-unknown.json"))["remedy"]["route"]=="human-review"
def test_replay():
    p=load("allow.json"); assert replay(p,evaluate(p))
def test_integrity_not_truth(): assert "not factual truth" in evaluate(load("allow.json"))["proof_record"]["integrity_note"]
def test_missing_refused():
    p=load("allow.json"); p["predicates"].pop()
    with pytest.raises(ValueError): evaluate(p)
