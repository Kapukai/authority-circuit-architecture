# Authority Cell Evolution Roadmap

Status: proposed architecture roadmap

## Alignment with the existing ACA family

The repository already defines ACA-100 Authority Circuit Architecture, ACA-110 Core Terminology, ACA-120 Verifiable Authority Cell, ACA-130 Decision State Machine, ACA-140 Decision Proof Record, and ACA-150 Operationalized Remedy Protocol.

This roadmap does not replace or renumber those documents. It evolves ACA-120 by defining one canonical Authority Cell record with multiple reproducible projections.

## Canonical-object principle

A Verifiable Authority Cell is the canonical object. Derivation, citation, evidence, timeline, challenge, authorization, audit, remedy, and AIM measurement are views generated from the same versioned record. No projection may maintain an independent substantive source of truth.

## Proposed sequence

1. ACA-121 — Authority Cell Canonical Graph
2. ACA-122 — Sovereign-to-Action Derivation Projection
3. ACA-123 — Verbatim Source and Citation Binding
4. ACA-124 — Transition Proof Obligations
5. ACA-125 — Multi-View Projection and Cross-View Reconciliation
6. ACA-126 — Challenge, Counter-Authority, and Disagreement Records
7. ACA-127 — Temporal and Audit Projection
8. EDS-0004 integration — Human authorization projection
9. AIM-0001 integration — Measurement projection

## Safety invariants

- Exact quotation, interpretation, machine parse, and human determination remain distinct.
- Every material node identifies source, version, effective interval, locator, provenance, and integrity metadata.
- Every material edge states the proposition connecting its source and target nodes.
- Missing, disputed, superseded, temporally invalid, or inaccessible support remains visible.
- A valid projection does not establish legal truth, legitimacy, or permission to act.
- Verification is not authorization.
- Cross-view disagreement is a defect signal and is never hidden or averaged away.
- No aggregate lawfulness score is produced.

## Compatibility rule

These packages extend ACA-120, ACA-140, and ACA-150. They preserve existing identifiers, decision states, proof-record semantics, replay requirements, and remedy obligations unless a separately governed revision explicitly changes them.
