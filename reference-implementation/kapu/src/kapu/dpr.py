from __future__ import annotations
import copy, hashlib, json
from datetime import datetime, timezone
from typing import Any

DPR_VERSION = "0.2.0"
ALLOWED_STATES = {"ALLOW","DENY","HOLD","CONFLICT","REVOKED","ESCALATE"}

class ProofRecordError(ValueError):
    pass

def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",",":"), ensure_ascii=False, allow_nan=False)

def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()

def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def _without_hashes(record: dict[str, Any]) -> dict[str, Any]:
    value = copy.deepcopy(record)
    value.pop("record_sha256", None)
    return value

def build_record(decision: dict[str, Any], *, previous_record_sha256: str | None = None,
                 created_at: str | None = None) -> dict[str, Any]:
    required = ["evaluation_id","cell_id","state","reason_code","proof_record"]
    missing = [k for k in required if k not in decision]
    if missing:
        raise ProofRecordError("decision missing: " + ", ".join(missing))
    if decision["state"] not in ALLOWED_STATES:
        raise ProofRecordError("invalid canonical state")
    source = decision["proof_record"]
    required_source = ["profile_version","rule_version","predicates","input_sha256"]
    missing_source = [k for k in required_source if k not in source]
    if missing_source:
        raise ProofRecordError("proof source missing: " + ", ".join(missing_source))

    record = {
        "dpr_version": DPR_VERSION,
        "record_id": decision["evaluation_id"],
        "cell_id": decision["cell_id"],
        "created_at": created_at or _utc_now(),
        "profile_version": source["profile_version"],
        "rule_version": source["rule_version"],
        "state": decision["state"],
        "reason_code": decision["reason_code"],
        "predicates": copy.deepcopy(source["predicates"]),
        "authorization": copy.deepcopy(decision.get("authorization")),
        "execution": copy.deepcopy(decision.get("execution")),
        "remedy": copy.deepcopy(decision.get("remedy")),
        "input_sha256": source["input_sha256"],
        "previous_record_sha256": previous_record_sha256,
        "assurance": {
            "integrity_is_not_truth": True,
            "human_approval_required": source.get("human_approval_required", True),
            "ai_output_accepted_as_authority": False,
        },
    }
    record["record_sha256"] = digest(_without_hashes(record))
    return record

def verify_record(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if record.get("dpr_version") != DPR_VERSION:
        errors.append("unsupported dpr_version")
    if record.get("state") not in ALLOWED_STATES:
        errors.append("invalid state")
    expected = digest(_without_hashes(record))
    if record.get("record_sha256") != expected:
        errors.append("record hash mismatch")
    assurance = record.get("assurance") or {}
    if assurance.get("integrity_is_not_truth") is not True:
        errors.append("integrity/truth distinction missing")
    if assurance.get("ai_output_accepted_as_authority") is not False:
        errors.append("AI output cannot be accepted as authority")
    execution = record.get("execution") or {}
    if execution.get("executed") is True and not execution.get("execution_record_id"):
        errors.append("executed action lacks execution_record_id")
    return errors

def verify_chain(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    previous = None
    for index, record in enumerate(records):
        for error in verify_record(record):
            errors.append(f"record[{index}]: {error}")
        if record.get("previous_record_sha256") != previous:
            errors.append(f"record[{index}]: previous hash mismatch")
        previous = record.get("record_sha256")
    return errors

def compare_replay(original: dict[str, Any], replayed: dict[str, Any]) -> dict[str, Any]:
    fields = ("cell_id","profile_version","rule_version","state","reason_code","input_sha256")
    differences = {
        field: {"original": original.get(field), "replayed": replayed.get(field)}
        for field in fields if original.get(field) != replayed.get(field)
    }
    return {"equivalent": not differences, "differences": differences}

def quarantine_ai_candidate(candidate: dict[str, Any], *, model: str, prompt_sha256: str,
                            output_sha256: str, reviewer_required: bool = True) -> dict[str, Any]:
    return {
        "status": "QUARANTINED",
        "candidate": copy.deepcopy(candidate),
        "provenance": {
            "producer_type": "AI_MODEL",
            "model": model,
            "prompt_sha256": prompt_sha256,
            "output_sha256": output_sha256,
        },
        "accepted_as_authority": False,
        "human_review_required": reviewer_required,
    }
