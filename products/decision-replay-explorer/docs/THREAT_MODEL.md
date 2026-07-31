# Threat Model

## Protected properties

- Source records remain unmodified.
- Differences are not hidden.
- Hash inputs use stable key ordering.
- No record is uploaded by the application.
- The result distinguishes equivalence from correctness.

## Threats and controls

| Threat | Current control | Remaining limitation |
|---|---|---|
| Malformed JSON | Parse failure and visible error | No schema validation yet |
| Key-order hash drift | Canonical key sorting | Number normalization is JSON-native |
| Hidden path difference | Recursive comparison | Very large records may affect performance |
| Supply-chain compromise | No third-party dependencies | Browser/runtime remains trusted |
| Sensitive-data disclosure | Local-only operation | User may still screen-share or save exports |
| False legal inference | Explicit disclaimer | Training and governance still required |
| Modified comparison export | Export is not signed | Digital signatures are future work |

## Non-goals

This package does not prove truth, lawful authority, human authorization, or faithful execution.
It proves only the comparison result produced from the supplied JSON records.
