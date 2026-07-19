# Kapukai Authority Circuit Standards Program

**Status:** Working Draft 0.1  
**Canonical family:** Authority Circuit Architecture (ACA)  
**Field:** Public Decision Systems Engineering (PDSE)

This repository is the version-controlled source for an open standards program that
translates legal, organizational, and policy authority into deterministic,
inspectable, testable decision structures with attached proof and remedy outputs.

## Core pipeline

Natural-language rule -> formal predicates -> truth table -> minimized logic ->
authority circuit -> decision proof record -> operationalized remedy.

## Documents

- ACA-000 - Program Charter and Roadmap
- ACA-100 - Authority Circuit Architecture
- ACA-110 - Core Terminology
- ACA-120 - Verifiable Authority Cell
- ACA-130 - Decision State Machine
- ACA-140 - Decision Proof Record
- ACA-150 - Operationalized Remedy Protocol

## Local build

```bash
./scripts/bootstrap.sh
./scripts/build.sh
```

The compiled PDF will appear at:

```text
docs/build/ACA_Standards_Program_v0.1.pdf
```

## Overleaf

Upload the repository ZIP to Overleaf and set `docs/tex/main.tex` as the main file.

## Website

The static landing-page starter is in:

```text
site/standards/authority-circuit/index.html
```

Publish it only after reviewing it against the existing Kapukai staging design.

## Development rule

The website is the public library. GitHub is the workshop. Published releases are
versioned artifacts. Drafts remain clearly marked as drafts.
