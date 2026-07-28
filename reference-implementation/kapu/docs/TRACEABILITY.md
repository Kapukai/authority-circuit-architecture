# Initial ACA-120 Traceability

| ACA-120 behavior | Code | Test |
|---|---|---|
| UNKNOWN blocks ALLOW | `engine.evaluate` | `test_states[hold-unknown]` |
| Conflict blocks authorization | `engine.evaluate` | `test_states[conflict]` |
| Revocation has precedence | `engine.evaluate` | `test_states[revoked]` |
| Authorization is separate from execution | result contract | `test_authorization_not_execution` |
| Adverse states attach remedy | result contract | `test_remedy_attached` |
| Replay is deterministic | `engine.replay` | `test_replay` |
| Integrity is not truth | proof record | `test_integrity_not_truth` |

This is an executable baseline, not a claim of complete ACA-120 conformance.
