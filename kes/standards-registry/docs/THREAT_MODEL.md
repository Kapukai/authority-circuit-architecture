# KES-0005 Threat Model

| Threat | Failure mode | Control |
|---|---|---|
| Identifier collision | Two concepts receive one ACA number | Unique registry IDs and CI failure |
| Namespace drift | Sequential numbering crosses a decade owner | Explicit child parent and decade validation |
| Agent authority escalation | Agent output becomes canonical | Identifier-free proposal schema and human allocation boundary |
| Silent renumbering | Existing citations lose referential integrity | Stable registry entries; changes require reviewed source diff |
| Premature promotion | Draft is described as accepted or released | Separate allocation and lifecycle states |
| Concurrent allocation | Two branches claim the same free slot | Advisory `next`; allocation occurs only through reviewed registry change |
| Source disappearance | Registry points to no specification | Source-path existence validation |

Verification establishes structural consistency only. It does not authorize an
action or prove the underlying substantive claim.
