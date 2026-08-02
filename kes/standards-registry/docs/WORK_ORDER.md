# KES-0005 Work Order

## Objective

Establish the authoritative ACA identifier registry and the execution boundary
for agent-assisted standards derivation.

## In scope

- canonical and proposed ACA identifier inventory;
- hierarchy and collision validation;
- advisory next-child discovery;
- identifier-free agent proposal contract;
- work-package contract;
- deterministic tests and Mission Control integration.

## Out of scope

- autonomous allocation or acceptance;
- legal conclusions;
- autonomous merging, publication, release, or authorization;
- bulk generation of new ACA standards.

## Acceptance criteria

- Existing canonical ACA standards have unique identifiers.
- Every child identifier has the correct decade parent.
- Every registry source path exists.
- Agent proposals cannot contain an ACA identifier or acceptance state.
- Work packages name a human authorizer and bounded verification commands.
- Repository release-readiness invokes the KES-0005 verifier.
