# KES-0002 — Release Pipeline Work Order

## Objective
Convert a verified work-order output into a durable, checksummed, reviewable release candidate without silently publishing it.

## Acceptance criteria
1. Manifest identifies product, work order, version, source, and required artifacts.
2. Verification commands must pass.
3. Packaging excludes common dependency and build directories.
4. Every packaged file receives a SHA-256 checksum.
5. A versioned ZIP and detached checksum are generated.
6. Release notes, website copy, announcement copy, and a machine-readable release record are generated.
7. `released` status requires an identified release authority.
8. The pipeline never merges, tags, deploys, or publishes automatically.
