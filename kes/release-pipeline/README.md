# KES-0002 — Release Pipeline

A governed, local-first pipeline that converts a verified Kapukai work order into a durable release candidate.

## Outputs

- validated release manifest
- required-artifact gate
- verification-command gate
- clean release directory
- SHA-256 file inventory
- versioned ZIP and detached checksum
- release notes, website card, announcement copy
- machine-readable release record

## Authority boundary

The pipeline prepares release evidence. It does not merge, tag, publish, or deploy. A human must explicitly authorize those actions.

## Run

```bash
python3 scripts/release.py examples/eds-0003.release.json
python3 scripts/verify.py
```

Recommended repository location: `kes/release-pipeline/`.
