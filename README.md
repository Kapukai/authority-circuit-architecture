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
- ACA-160 - Predicate Failure Taxonomy

## Local build

```bash
./scripts/bootstrap.sh
./scripts/build.sh
```

The compiled PDF will appear at:

```text
docs/build/ACA_Standards_Program_v0.1.pdf
```

## Validate and package a candidate release

```bash
python3 scripts/validate.py
./scripts/package-release.sh
./scripts/package-site.sh
```

This creates clean, checksummed candidate artifacts under `dist/`. Release,
staging, production, and rollback gates are documented in
`docs/operations/RELEASE_AND_DEPLOYMENT.md`.

## Overleaf

Upload the repository ZIP to Overleaf and set `docs/tex/main.tex` as the main file.

## Website

The static landing-page starter is in:

```text
site/standards/authority-circuit/index.html
```

Canonical public URL:

```text
https://kapukai.org/standards/authority-circuit/
```

Deployment status: not yet promoted to production. The current site is a
Working Draft 0.1 concept demonstrator and does not establish conformance.
Publish only a verified release artifact after staging acceptance.

The July 2026 predecessor website reconciliation is recorded in
`docs/reconciliation/JULY_WEBSITE_MAPPING.md`.

## Development rule

The website is the public library. GitHub is the workshop. Published releases are
versioned artifacts. Drafts remain clearly marked as drafts.
