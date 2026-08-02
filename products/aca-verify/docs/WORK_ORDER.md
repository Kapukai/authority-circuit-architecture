# ACA Verify v0.1 Work Order

## Objective

Implement a dependency-free, deterministic interpreter that evaluates one
Decision Proof Record against an explicit partial conformance profile.

## Acceptance criteria

- Identical record and profile bytes produce identical semantic results.
- Every non-passing finding identifies a canonical ACA requirement and repair.
- PASS, WARN, FAIL, and INDETERMINATE have test fixtures.
- Decision state, conformance, reliance, and authorization remain distinct.
- No network, model, clock, or hidden state affects evaluation.

## Out of scope

Truth, legality, legitimacy, credibility, authority inference, evidence
extraction, autonomous authorization, real-case adjudication, signing, and
publication.
