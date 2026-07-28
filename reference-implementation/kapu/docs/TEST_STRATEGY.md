# KAPU Test Strategy

The release gate includes:

- unit tests for state and record behavior;
- golden deterministic vectors;
- JSON Schema validation;
- negative tests for malformed or incomplete records;
- tamper and chain-order tests;
- replay-equivalence tests;
- hostile-input tests;
- AI-output quarantine tests;
- an end-to-end CLI build and verify test.

Production releases should later add mutation testing, dependency scanning,
static analysis, signed release artifacts, external assessment, load tests, and
domain-specific acceptance tests.
