#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "docs" / "CHARTER.md",
    ROOT / "docs" / "RESEARCH_BOUNDARY.md",
    ROOT / "docs" / "WORK_ORDER.md",
    ROOT / "docs" / "CONSTRUCT_REGISTER.md",
    ROOT / "docs" / "ACCEPTANCE_PLAN.md",
]

REQUIRED_PHRASES = {
    ROOT / "README.md": [
        "non-normative research program",
        "Hard safety gates precede profiles",
    ],
    ROOT / "docs" / "CHARTER.md": [
        "Research candidate. Non-normative.",
        "Hard gates first. Profiles second.",
        "Verification establishes",
    ],
    ROOT / "docs" / "RESEARCH_BOUNDARY.md": [
        "must not output a single aggregate",
        "Only an accountable human may",
    ],
    ROOT / "docs" / "WORK_ORDER.md": [
        "No aggregate legitimacy or lawfulness percentage",
        "no code claims to measure authority at this stage",
    ],
    ROOT / "docs" / "CONSTRUCT_REGISTER.md": [
        "All entries are candidate research constructs",
        "No construct may move to `VALIDATED` through author declaration alone",
    ],
    ROOT / "docs" / "ACCEPTANCE_PLAN.md": [
        "research-only and non-normative",
        "The repository contains no operational AIM scoring engine",
    ],
}

PROHIBITED_OPERATIONAL_PHRASES = [
    "percent lawful",
    "% lawful",
    "automatically authorize",
    "autonomous authorization",
]

OPERATIONAL_SUFFIXES = {".py", ".js", ".mjs", ".ts", ".tsx", ".sh"}


def operational_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or path == Path(__file__).resolve():
            continue
        if "docs" in path.relative_to(ROOT).parts:
            continue
        if path.suffix.lower() in OPERATIONAL_SUFFIXES:
            yield path


def main() -> int:
    failures = []

    for path in REQUIRED_FILES:
        if not path.is_file():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")
            continue

        text = path.read_text(encoding="utf-8")
        for phrase in REQUIRED_PHRASES.get(path, []):
            if phrase not in text:
                failures.append(
                    f"missing required boundary phrase in {path.relative_to(ROOT)}: {phrase!r}"
                )

    # Policy documents may quote forbidden claims in order to prohibit them.
    # Only executable or operational source files are scanned for those claims.
    for path in operational_files():
        lowered = path.read_text(encoding="utf-8", errors="replace").lower()
        for phrase in PROHIBITED_OPERATIONAL_PHRASES:
            if phrase.lower() in lowered:
                failures.append(
                    f"prohibited operational claim in {path.relative_to(ROOT)}: {phrase!r}"
                )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        return 1

    print(f"PASS: {len(REQUIRED_FILES)} AIM-0000 files and research boundaries verified")
    return 0


if __name__ == "__main__":
    sys.exit(main())
