# EDS-0003 Work Order — Decision Replay Explorer

## Purpose

Make replay understandable to a human reviewer by displaying exact equivalence and path-level
divergence between an original Decision Proof Record and a replayed record.

## Scope

Included:

- local JSON loading;
- canonical SHA-256 hashing;
- recursive path comparison;
- added, removed, and changed classifications;
- replay summary;
- comparison export;
- synthetic examples;
- accessibility-conscious responsive interface;
- verification and tests.

Excluded:

- legal conclusions;
- identity verification;
- digital signatures;
- production authentication;
- remote storage;
- automated alteration of source records;
- derived authority.

## Acceptance criteria

1. Equivalent records show `REPLAY EQUIVALENT`.
2. Any changed, added, or removed path shows `REPLAY DIVERGENT`.
3. Original and replay hashes are visible.
4. The interface never silently rewrites either record.
5. A comparison artifact can be exported.
6. The package runs without third-party dependencies.
7. Verification and unit tests pass.

## Definition of done

Source, tests, documentation, synthetic records, verification script, checksums, release notes,
and ZIP package exist. Integration occurs only through review of an isolated branch.
