#!/usr/bin/env python3
"""Deterministic KES capability planner. Standard library only."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ALL = {"architecture","engineering","verification","release","research","product","publisher","security","liaison"}

def plan(wo: dict) -> dict:
    required = {"architecture", "verification"}
    typ = wo.get("type", "")
    tags = set(wo.get("tags", []))
    risk = wo.get("risk", "low")

    if typ in {"code","product","integration","release"}:
        required.add("engineering")
    if typ == "product":
        required.add("product")
    if typ in {"research","standard"}:
        required.add("research")
    if typ in {"code","product","integration","release"}:
        required.add("release")
    if typ == "pilot" or tags & {"pilot","partnership","event","standards-engagement"}:
        required.add("liaison")
    if wo.get("public_release") or tags & {"campaign","public-release"}:
        required.add("publisher")
    if wo.get("sensitive_data") or wo.get("external_deployment") or risk in {"high","life-critical"} or tags & {"regulated","authentication","sensitive-data"}:
        required.add("security")
    if risk in {"high","life-critical"}:
        required.add("research")

    ordered = [x for x in ["architecture","product","research","engineering","security","verification","release","publisher","liaison"] if x in required]
    return {
        "work_order_id": wo.get("id"),
        "required_capabilities": ordered,
        "independent_gates": [x for x in ordered if x in {"security","verification","release"}],
        "human_approval_required": bool(wo.get("release", {}).get("human_approval", True)),
    }

def validate_minimal(wo: dict) -> list[str]:
    errors=[]
    for key in ["id","title","type","risk","purpose","acceptance_criteria","deliverables","verification","release"]:
        if key not in wo: errors.append(f"missing required field: {key}")
    if wo.get("type") not in {"documentation","code","product","research","standard","pilot","release","integration"}:
        errors.append("invalid type")
    if wo.get("risk") not in {"low","medium","high","life-critical"}:
        errors.append("invalid risk")
    if not isinstance(wo.get("acceptance_criteria"), list) or not wo.get("acceptance_criteria"):
        errors.append("acceptance_criteria must be a non-empty list")
    return errors

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("work_order", type=Path)
    ap.add_argument("--output", type=Path)
    args=ap.parse_args()
    wo=json.loads(args.work_order.read_text())
    errors=validate_minimal(wo)
    if errors:
        print(json.dumps({"valid":False,"errors":errors},indent=2), file=sys.stderr)
        return 2
    result={"valid":True, **plan(wo)}
    text=json.dumps(result,indent=2)+"\n"
    if args.output: args.output.write_text(text)
    else: print(text,end="")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
