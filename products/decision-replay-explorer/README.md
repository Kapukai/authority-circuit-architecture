# EDS-0003 — Decision Replay Explorer

A dependency-free browser application for comparing an original Decision Proof Record (DPR)
with a replayed DPR.

## Purpose

The explorer makes replay observable. It distinguishes:

- exact equivalence,
- changed values,
- added paths,
- removed paths,
- verification state,
- record hashes.

It does **not** determine legal authority or guarantee correctness. It visualizes and verifies
the supplied records.

## Run

```bash
python3 -m http.server 8080 --directory .
```

Open:

```text
http://127.0.0.1:8080/
```

You may also open `index.html` directly in a modern browser.

## Verify

```bash
python3 scripts/verify.py
```

## Test

```bash
node tests/replay.test.mjs
```

## Safety boundary

- Local-first and dependency-free.
- No network requests.
- No authentication or multi-user controls.
- Use synthetic or properly authorized records only.
- Not production-ready for sensitive or regulated data.

## Work-order outputs

- Product brief
- Architecture decision record
- Capability plan
- Threat model
- Source code
- Tests
- Verification
- Demo records
- Release notes
