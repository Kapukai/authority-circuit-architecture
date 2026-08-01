# KES-0005 Standards Registry and Work Orchestration

KES-0005 is the control boundary between ACA identifiers, agent-assisted work,
and human acceptance.

The registry is authoritative for identifier ownership. Agents may inspect the
registry, analyze gaps, and submit schema-valid proposals. They may not assign,
reserve, renumber, accept, merge, publish, or retire an ACA identifier.

## Control model

1. KES declares eligible work and validates registry state.
2. A work package defines one bounded, testable delivery.
3. Agents may execute the package and emit proposals and candidate artifacts.
4. Deterministic checks reject collisions, broken parentage, missing sources,
   and unauthorized agent-assigned identifiers.
5. The Human Chief Architect authorizes allocation and acceptance.

## Commands

```bash
python3 kes/standards-registry/scripts/registry.py verify
python3 kes/standards-registry/scripts/registry.py list
python3 kes/standards-registry/scripts/registry.py next --parent ACA-120
python3 kes/standards-registry/scripts/registry.py proposal \
  --parent ACA-120 --title "Candidate projection"
python3 kes/standards-registry/tests/test_registry.py
```

`next` is advisory. It does not reserve an identifier. `proposal` deliberately
emits no ACA identifier.
