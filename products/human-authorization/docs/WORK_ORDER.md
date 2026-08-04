# EDS-0004 Work Order — Human Authorization

## Authorized objective

Design a minimum, inspectable authorization record and interaction contract that preserves accountable human control over consequential actions.

## Required authorization fields

1. `authorization_id`
2. `decision_object`
3. `proposed_action`
4. `authorized_scope`
5. `prohibited_scope`
6. `authorizing_human`
7. `role_and_authority_basis`
8. `evidence_and_result_references`
9. `known_uncertainties`
10. `affected_rights_and_interests`
11. `reason_for_authorization`
12. `alternatives_considered`
13. `effective_at`
14. `expires_at`
15. `rollback_conditions`
16. `remedy_path`
17. `conflict_disclosures`
18. `dissent_or_abstention`
19. `signature_or_attestation`
20. `record_hash`

## Required states

- `DRAFT`
- `PENDING_HUMAN_REVIEW`
- `AUTHORIZED`
- `DENIED`
- `ABSTAINED`
- `EXPIRED`
- `REVOKED`
- `SUPERSEDED`
- `INDETERMINATE`

No state may be inferred from silence, inactivity, model confidence, or successful verification.

## Hard gates

Authorization must not advance to `AUTHORIZED` unless:

- an accountable human is identified;
- the action and scope are explicit;
- material uncertainty is visible;
- affected rights and foreseeable burdens are recorded;
- conflicts are disclosed;
- expiration or review timing is defined;
- rollback or remedy conditions are addressed;
- an affirmative human attestation is recorded.

A failed or indeterminate gate cannot be offset by strengths elsewhere.

## Deliverables

- JSON schema for authorization records;
- canonical examples for authorization, denial, abstention, revocation, and expiry;
- deterministic validator;
- threat model;
- acceptance plan;
- read-only reference interface or renderer;
- Mission Control status update.

## Prohibited behavior

The candidate must not:

- authorize automatically;
- infer approval from a model or verifier;
- hide dissent or uncertainty;
- omit affected-rights analysis;
- create perpetual authorization by default;
- treat a signature alone as sufficient without scope and reasons;
- overwrite prior authorization states.

## Acceptance boundary

Acceptance establishes only the authorization-record architecture. It does not authorize any real-world action.
