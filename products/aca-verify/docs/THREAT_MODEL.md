# ACA Verify v0.1 Threat Model

| Risk | Control |
|---|---|
| PASS mistaken for permission | Report says verification is not authorization; reliance remains NOT_ESTABLISHED |
| Supplied assertions mistaken for independently verified facts | Every report labels its basis DECLARED_PREDICATES and states that facts are not independently established |
| A digest string mistaken for artifact binding | Evidence assurance is DECLARED_DIGESTS_ONLY; placeholder and malformed SHA-256 strings are rejected; artifact retrieval and recomputation remain out of scope |
| Full ACA conformance overstated | Every report declares PARTIAL_PROFILE_CONFORMANCE |
| Rules silently change | Profile ID and version must match the record |
| Nondeterministic evaluation | No network, clock, randomness, or model calls |
| Invented ACA identifiers | Profile accepts only identifiers already canonical in v0.1 |
| Profile silently ignores supplied predicates | Undeclared predicates are listed and force WARN |
| Advisory and mandatory rules are conflated | The profile's mandatory field is validated and controls FAIL versus WARN behavior |
| Missing proof treated as proof | Missing and UNKNOWN mandatory predicates produce INDETERMINATE |
| Unsafe adverse action | Definite mandatory failures produce FAIL and ACTION_BLOCKED |
| CI permits warning conditions | The reusable action defaults to strict mode, where WARN exits nonzero |
| Candidate mistaken for released software | Safety hold prohibits release, tags, deployment, pilots, marketing, and real-case use pending human reviews |
| Public code creates unintended licensing claims | Release remains blocked on human intellectual-property and licensing review; the repository license grants no patent license |
