# KES-0003 — Repository Intelligence Work Order

## Purpose

Make the repository observable before further expansion or automated guardianship.

## Acceptance criteria

1. Analysis is read-only except for a designated output directory.
2. Existing source files are never moved, edited, or deleted.
3. Every observed file receives a classification, size, and SHA-256 hash.
4. Modified and untracked paths are surfaced.
5. Observation and inference remain distinguishable.
6. JSON, Markdown, DOT, HTML, and checksums are generated.
7. Synthetic tests pass.
8. No third-party dependency is required.
