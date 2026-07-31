# KES-0004 Mission Control

Mission Control is the read-only program control plane for the Kapukai ecosystem.

It converts a canonical program-state record into an inspectable view of:

- standards;
- products;
- KES capabilities;
- research programs;
- branches and pull requests;
- verification, acceptance, release, and publication states;
- dependencies and critical path;
- risks and findings;
- next authorized work.

## Current candidate contents

- `docs/WORK_ORDER.md` — mission, boundaries, states, and acceptance criteria;
- `docs/ADR-0004.md` — decision to use a read-only, JSON-driven control plane;
- `mission-control.schema.json` — versioned program-state schema;
- `examples/program-state.json` — initial Kapukai portfolio snapshot.

## Candidate implementation sequence

1. Validate the example state against the schema.
2. Add a dependency-free browser dashboard.
3. Add deterministic findings for missing owners, broken dependencies, stale records, and ambiguous branch dispositions.
4. Add tests and checksums.
5. Perform local browser inspection and human acceptance.
6. Open a merge candidate only after verification.

## Architectural limitation

Mission Control observes and validates declared program state. It does not prove that the declared state is true and cannot authorize, merge, publish, deploy, or change any tracked item.
