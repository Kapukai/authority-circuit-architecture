# Threat Model

| Risk | Control |
|---|---|
| Packaging unverified work | Required commands must pass |
| Missing artifacts | Manifest-required file gate |
| Silent publication | No publish, merge, tag, or deploy functions |
| Ambiguous ownership | Released status requires release authority |
| Artifact substitution | SHA-256 inventory and detached ZIP checksum |
| Dependency leakage | Common dependency/build directories excluded |
| False conformance claims | Candidate status and limitations preserved |

This version does not provide signing keys, identity proof, secret scanning, or production deployment security.
