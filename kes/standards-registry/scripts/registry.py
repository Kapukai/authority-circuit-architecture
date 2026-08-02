#!/usr/bin/env python3
"""Dependency-free ACA registry verification and advisory proposal tooling."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PACKAGE = Path(__file__).resolve().parents[1]
REGISTRY = PACKAGE / "registry.json"
ID_RE = re.compile(r"^ACA-(\d{3})$")


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load() -> dict:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"invalid registry: {exc}")
    if data.get("schema_version") != "0.1":
        fail("unsupported registry schema version")
    if data.get("authority") != "Human Chief Architect":
        fail("registry authority changed")
    return data


def verify(data: dict) -> None:
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        fail("registry entries must be a non-empty array")
    ids = [entry.get("id") for entry in entries]
    if len(ids) != len(set(ids)):
        fail("duplicate ACA identifier")
    known = set(ids)
    for entry in entries:
        match = ID_RE.fullmatch(str(entry.get("id", "")))
        if not match:
            fail(f"invalid ACA identifier: {entry.get('id')}")
        if entry.get("agents_may_allocate") is not False:
            fail(f"agent allocation enabled for {entry['id']}")
        source = ROOT / str(entry.get("source_path", ""))
        if not source.is_file():
            fail(f"missing source for {entry['id']}: {entry.get('source_path')}")
        number = int(match.group(1))
        parent = entry.get("parent_id")
        if entry.get("kind") == "CHILD_STANDARD":
            expected = f"ACA-{(number // 10) * 10:03d}"
            if parent != expected or parent not in known:
                fail(f"invalid parent for {entry['id']}: expected {expected}")
        elif parent is not None:
            fail(f"non-child {entry['id']} must not declare parent")
    print(f"PASS: {len(entries)} unique ACA identifiers; hierarchy and sources verified")


def next_child(data: dict, parent: str) -> str:
    match = ID_RE.fullmatch(parent)
    if not match or int(match.group(1)) % 10:
        fail("parent must be a decade ACA identifier such as ACA-120")
    if parent not in {entry["id"] for entry in data["entries"]}:
        fail(f"unknown parent: {parent}")
    base = int(match.group(1))
    used = {int(entry["id"].split("-")[1]) for entry in data["entries"]}
    for candidate in range(base + 1, base + 10):
        if candidate not in used:
            return f"ACA-{candidate:03d}"
    fail(f"no unallocated child slot under {parent}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("verify")
    sub.add_parser("list")
    next_parser = sub.add_parser("next")
    next_parser.add_argument("--parent", required=True)
    proposal = sub.add_parser("proposal")
    proposal.add_argument("--parent", required=True)
    proposal.add_argument("--title", required=True)
    args = parser.parse_args()
    data = load()
    verify(data)
    if args.command == "list":
        for entry in sorted(data["entries"], key=lambda item: item["id"]):
            print(f"{entry['id']}\t{entry['allocation_state']}\t{entry['title']}")
    elif args.command == "next":
        print(next_child(data, args.parent))
    elif args.command == "proposal":
        if args.parent not in {entry["id"] for entry in data["entries"]}:
            fail(f"unknown parent: {args.parent}")
        payload = {
            "schema_version": "0.1",
            "proposal_id": "PROPOSAL-UNASSIGNED",
            "parent_id": args.parent,
            "title": args.title,
            "problem": "Define the observable problem before allocation.",
            "dependencies": [],
            "evidence": [],
            "uncertainties": [],
            "requested_human_decision": "ALLOCATE_OR_REJECT",
        }
        print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
