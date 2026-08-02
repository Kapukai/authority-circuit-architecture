# ACA Verify v0.1 Threat Model

| Risk | Control |
|---|---|
| PASS mistaken for permission | Report says verification is not authorization; reliance remains NOT_ESTABLISHED |
| Full ACA conformance overstated | Every report declares PARTIAL_PROFILE_CONFORMANCE |
| Rules silently change | Profile ID and version must match the record |
| Nondeterministic evaluation | No network, clock, randomness, or model calls |
| Invented ACA identifiers | Profile accepts only identifiers already canonical in v0.1 |
| Missing proof treated as proof | Missing and UNKNOWN mandatory predicates produce INDETERMINATE |
| Unsafe adverse action | Definite mandatory failures produce FAIL and ACTION_BLOCKED |
