# ACA Schema Contract v0.1

This package is the machine-readable contract between the ACA specifications, reference implementation, conformance vectors, replay system, and independent implementations.

## Canonical locations

```text
schemas/v0.1/
examples/v0.1/
tools/schema-validation/
tests/schema-contract/
```

The earlier root-level `schemas/decision-proof-record.schema.json` is not overwritten.

## Design invariants

1. Every schema has a stable `$id`.
2. Undeclared properties are rejected unless extension is explicit.
3. Authority, evidence, rules, decisions, remedy, and assurance remain separate objects.
4. `UNKNOWN`, `CONFLICT`, `EXPIRED`, and `REVOKED` remain distinct.
5. `ALLOW` cannot carry an open remedy.
6. A completed remedy requires completion evidence and verified closure.
7. Material legal-technical change identifies accountable legal and technical owners.
8. Schema validity proves structure, not factual truth or lawful authority.
