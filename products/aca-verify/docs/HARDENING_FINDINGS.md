# ACA Verify Hardening Findings

## Controls added in v0.1.1 candidate

- Reject malformed records, profiles, timestamps, remedy states, sources, and
  SHA-256 declarations.
- Reject duplicate predicate identifiers and profile rules.
- Apply the profile's mandatory/advisory distinction.
- Surface predicates not governed by the selected profile and force `WARN`.
- Label reports `DECLARED_PREDICATES` and `DECLARED_DIGESTS_ONLY`.
- Keep `PASS` reliance at `NOT_ESTABLISHED`.
- Make GitHub Action strict mode the default so `WARN` blocks CI.
- Exercise malformed and adversarial fixtures in deterministic tests.

## Residual limitations

- The interpreter does not retrieve artifacts or recompute hashes.
- It does not establish truth, legal validity, legitimacy, credibility, or
  lawful authority.
- It does not authenticate the record author or profile publisher.
- It has no signing, transparency log, replay service, or trusted timestamp.
- It has not been evaluated on real cases and is not authorized for them.
- The public repository licensing and patent boundary still requires human
  review before any release or external adoption claim.

These are product boundaries, not findings that can be erased by changing a
label. Work that closes them requires a separately authorized architecture and
work package.
