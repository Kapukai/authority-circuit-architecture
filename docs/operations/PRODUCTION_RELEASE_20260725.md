# Production Release Record — 2026-07-25

## Outcome

Authority Circuit Architecture Working Draft 0.1 was promoted from the tested
Iceland staging path to:

```text
https://kapukai.org/standards/authority-circuit/
```

The existing standards registry was preserved and updated additively with an
ACA entry:

```text
https://kapukai.org/standards/
```

## Integrity

- Release ID: `20260725T015927Z`
- Release archive SHA-256:
  `19ca5aae87d1e07dfd5da711a1b67024fe164c4dbb78a9f71c184d14e1cc6f81`
- Prior registry SHA-256:
  `f4a9b0be71fd6d9f6e44bbb7f89e428ebe8d5ec00696b6b57cfe43aa2c8d657c`
- Deployed registry SHA-256:
  `bf0af3a035564c9b4cc62c073ee065dc04d93fbc5d9d4eae7dbf08999cb226ae`

## Backups

- Complete pre-ACA standards backup:
  `/var/backups/kapukai/aca-release/20260725T014806Z/standards-before-aca.tar.gz`
- Immediate production rollback:
  `/var/backups/kapukai/aca-release/20260725T015927Z`
- Legacy-preview rollback:
  `/var/backups/kapukai/preview-release/20260725T022909Z`

## Verification

- Package and internal manifest checks passed.
- Nginx configuration validation passed.
- ACA HTML, CSS, JavaScript, manifest, social image, and directory card returned
  successful public responses.
- Observable, Interlock, Authority OS, Congress, FMLIS, and MVS registry
  destinations remained reachable.
- Observable, Interlock, Authority OS, and Congress received distinct preview
  metadata and versioned 1200 × 630 images.
- The Congress Gunicorn service restarted and passed its public health check.

## Publication status

The site remains visibly labeled `Working Draft 0.1`. Publication does not
establish ACA conformance and does not determine real-world authority.
