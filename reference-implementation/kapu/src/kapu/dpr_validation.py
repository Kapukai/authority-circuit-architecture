import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

def schema_path():
    return Path(__file__).resolve().parents[2]/"schemas"/"decision-proof-record.schema.json"

def validate_dpr(record):
    schema=json.loads(schema_path().read_text())
    validator=Draft202012Validator(schema, format_checker=FormatChecker())
    return [e.message for e in sorted(validator.iter_errors(record), key=lambda x:list(x.path))]
