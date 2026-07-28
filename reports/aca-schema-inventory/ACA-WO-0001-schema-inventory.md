# ACA-WO-0001 — Recovered Schema Contract Inventory

- Generated: 2026-07-28T11:47:04.834653+00:00
- Repository: `/Users/lailaainsley/Kapukai/authority-circuit-architecture`
- Schemas: 10
- Examples: 11
- Direct tests mapped: 3
- Baseline tests passed: **True**

## Executive finding

The recovered v0.1 package is a coherent structural contract family, but it is not yet a complete formal Authority Cell specification or conformance suite.

## Schema inventory

| Schema | Required fields | Properties | References | Conditionals |
|---|---:|---:|---:|---:|
| `authority-derivation.schema.json` | 5 | 8 | 3 | 0 |
| `authority.schema.json` | 10 | 16 | 4 | 0 |
| `change-point.schema.json` | 12 | 18 | 2 | 0 |
| `common-defs.schema.json` | 0 | 0 | 1 | 0 |
| `conformance-report.schema.json` | 11 | 14 | 4 | 0 |
| `decision-proof-record.schema.json` | 12 | 20 | 5 | 2 |
| `evaluation-request.schema.json` | 7 | 9 | 4 | 0 |
| `evidence.schema.json` | 5 | 10 | 3 | 0 |
| `remedy.schema.json` | 7 | 15 | 2 | 1 |
| `rule-profile.schema.json` | 8 | 12 | 2 | 0 |

## Dependency graph

- `authority-derivation.schema.json` → `authority.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`
- `authority.schema.json` → `common-defs.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`
- `change-point.schema.json` → `common-defs.schema.json`, `common-defs.schema.json`
- `common-defs.schema.json` → `#/$defs/predicateValue`
- `conformance-report.schema.json` → `common-defs.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`
- `decision-proof-record.schema.json` → `common-defs.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`
- `evaluation-request.schema.json` → `authority-derivation.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`, `evidence.schema.json`
- `evidence.schema.json` → `common-defs.schema.json`, `common-defs.schema.json`, `common-defs.schema.json`
- `remedy.schema.json` → `common-defs.schema.json`, `common-defs.schema.json`
- `rule-profile.schema.json` → `common-defs.schema.json`, `common-defs.schema.json`

## Existing direct tests

- `test_valid_dpr`: `decision-proof-record.schema.json` with `decision-proof-record.valid.json`
- `test_allow_open_remedy_invalid`: `decision-proof-record.schema.json` with `decision-proof-record.invalid-allow-remedy.json`
- `test_false_remedy_closure_invalid`: `remedy.schema.json` with `remedy.invalid-false-closure.json`

## Baseline pytest result

```text
...                                                                      [100%]
3 passed in 0.04s

```

## Missing coverage

### Schemas without valid examples
- `common-defs.schema.json`

### Schemas without invalid examples
- `authority-derivation.schema.json`
- `authority.schema.json`
- `change-point.schema.json`
- `common-defs.schema.json`
- `conformance-report.schema.json`
- `evaluation-request.schema.json`
- `evidence.schema.json`
- `rule-profile.schema.json`

### Schemas without direct tests
- `authority-derivation.schema.json`
- `authority.schema.json`
- `change-point.schema.json`
- `common-defs.schema.json`
- `conformance-report.schema.json`
- `evaluation-request.schema.json`
- `evidence.schema.json`
- `rule-profile.schema.json`

## Semantic gaps that block ACA-120

- Identity and affected-subject bindings are not uniformly first-class.
- requested_action remains an unconstrained string rather than a taxonomy reference.
- Rule-profile evaluation and state rules remain prose strings, not formal executable semantics.
- Decision authorization and actual execution are not represented as separate mandatory records.
- Replay digests exist, but canonical normalization and equivalence rules require formal specification.
- Schema validation proves structure only; it does not prove factual truth or lawful authority.

## Source-integrity result

- Governed source files unchanged during inventory: **True**
- Runtime caches and bytecode are excluded from source-integrity comparison.

## Human review required

This report is generated evidence. It does not approve ACA-WO-0001, alter ACA semantics, or authorize work on ACA-120.
