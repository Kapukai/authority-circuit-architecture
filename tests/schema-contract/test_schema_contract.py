from pathlib import Path
import importlib.util
ROOT=Path(__file__).resolve().parents[2]; P=ROOT/"tools/schema-validation/validate.py"
spec=importlib.util.spec_from_file_location("aca_validator",P);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
S=ROOT/"schemas/v0.1";E=ROOT/"examples/v0.1"
def test_valid_dpr(): assert m.validate(S,"decision-proof-record",E/"decision-proof-record.valid.json")==[]
def test_allow_open_remedy_invalid(): assert m.validate(S,"decision-proof-record",E/"decision-proof-record.invalid-allow-remedy.json")
def test_false_remedy_closure_invalid(): assert m.validate(S,"remedy",E/"remedy.invalid-false-closure.json")
