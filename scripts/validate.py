#!/usr/bin/env python3
"""Dependency-free release-readiness checks for ACA working drafts."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
VERSION_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[a-z0-9.-]+)?$")
REQUIRED_STATES = {"ALLOW", "DENY", "HOLD", "CONFLICT", "REVOKED", "ESCALATE"}
REQUIRED_DOCS = {
    "aca-000",
    "aca-100",
    "aca-110",
    "aca-120",
    "aca-130",
    "aca-140",
    "aca-150",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)} is not valid JSON: {exc}")


def main() -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not VERSION_RE.fullmatch(version):
        fail(f"VERSION is not a supported semantic version: {version!r}")

    schema = load_json(ROOT / "schemas/decision-proof-record.schema.json")
    example = load_json(ROOT / "examples/minimal-decision.json")
    if not isinstance(schema, dict) or not isinstance(example, dict):
        fail("schema and example must be JSON objects")

    state_values = set(
        schema.get("properties", {}).get("state", {}).get("enum", [])
    )
    if state_values != REQUIRED_STATES:
        fail(f"canonical state set changed: {sorted(state_values)}")

    required = set(schema.get("required", []))
    missing_example = sorted(required - set(example))
    if missing_example:
        fail(f"minimal example is missing required fields: {missing_example}")

    if example.get("state") not in state_values:
        fail("minimal example uses a non-canonical decision state")

    main_tex = (ROOT / "docs/tex/main.tex").read_text(encoding="utf-8")
    included = set(re.findall(r"\\input\{sections/(aca-[0-9]+)\}", main_tex))
    if included != REQUIRED_DOCS:
        fail(
            "standards-family inputs differ from the canonical set: "
            f"{sorted(included)}"
        )

    site = (ROOT / "site/standards/authority-circuit/index.html").read_text(
        encoding="utf-8"
    )
    for marker in (
        "Working Draft 0.1",
        "Authority Circuit Architecture",
        "https://kapukai.org/standards/authority-circuit/",
        'data-demonstrator="synthetic"',
        "Technical working draft. Not legal advice.",
    ):
        if marker not in site:
            fail(f"website is missing required draft marker: {marker}")

    public_site_root = ROOT / "site/standards/authority-circuit"
    required_site_files = {
        public_site_root / "index.html",
        public_site_root / "assets/styles.css",
        public_site_root / "assets/app.js",
    }
    missing_site_files = [
        str(path.relative_to(ROOT)) for path in required_site_files if not path.is_file()
    ]
    if missing_site_files:
        fail(f"website is missing required files: {missing_site_files}")

    privacy_markers = (
        "Hillier Status Integrity Record",
        "Christine Hillier",
        "passport-denial",
        "counsel-role-inconsistency",
    )
    public_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in public_site_root.rglob("*")
        if path.is_file()
    )
    leaked_markers = [marker for marker in privacy_markers if marker in public_text]
    if leaked_markers:
        fail(f"public standards site contains predecessor evidence markers: {leaked_markers}")

    forbidden = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT)
        if path.name == ".DS_Store" or path.name.startswith("._"):
            forbidden.append(str(rel))
        if "node_modules" in path.parts or ".next" in path.parts:
            forbidden.append(str(rel))
    if forbidden:
        fail(f"forbidden generated/private packaging inputs found: {forbidden}")

    registry_verify = ROOT / "kes" / "standards-registry" / "scripts" / "registry.py"
    if registry_verify.is_file():
        subprocess.run(
            [sys.executable, str(registry_verify), "verify"],
            cwd=ROOT,
            check=True,
        )

    aca_verify = ROOT / "products" / "aca-verify" / "scripts" / "verify.py"
    if aca_verify.is_file():
        subprocess.run(
            [sys.executable, str(aca_verify)],
            cwd=ROOT,
            check=True,
        )

    print(f"ACA {version}: release-readiness validation passed")


if __name__ == "__main__":
    main()
