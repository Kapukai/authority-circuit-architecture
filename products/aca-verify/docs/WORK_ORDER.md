# ACA Verify v0.1.1 Hardening Work Order

## Objective

Implement a dependency-free, deterministic interpreter that evaluates one
Decision Proof Record against an explicit partial conformance profile while
making the boundary between declared inputs and independently proven facts
unmistakable.

## Acceptance criteria

- Identical record and profile bytes produce identical semantic results.
- Every non-passing finding identifies a canonical ACA requirement and repair.
- PASS, WARN, FAIL, and INDETERMINATE have test fixtures.
- Decision state, conformance, reliance, and authorization remain distinct.
- No network, model, clock, or hidden state affects evaluation.
- Placeholder hashes and malformed record/profile structures are rejected.
- Predicates outside the selected profile remain visible and force WARN.
- GitHub Action strict mode treats WARN as a failing workflow result.
- Reports state that artifact binding and factual truth are not established.
- A safety hold and explicit human release gates remain in force.

## Out of scope

Truth, legality, legitimacy, credibility, authority inference, evidence
extraction, autonomous authorization, real-case adjudication, signing, and
publication.
