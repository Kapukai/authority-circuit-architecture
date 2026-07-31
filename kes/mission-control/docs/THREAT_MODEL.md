# KES-0004 Threat Model

## Protected properties

- separation of verification, acceptance, authorization, release, and publication;
- integrity of the canonical program-state record;
- visibility of unresolved risks and dependencies;
- human control of state transitions;
- preservation of repository and release history.

## Primary threats

1. **False freshness** — stale records presented as current.
2. **False completion** — file or branch presence interpreted as accepted work.
3. **Authorization collapse** — a passing check interpreted as permission to merge, publish, or deploy.
4. **Hidden dependency** — an unrecorded dependency produces a misleading critical path.
5. **Risk suppression** — open findings omitted or marked closed without evidence.
6. **State injection** — untrusted data alters the displayed program state.
7. **Dashboard authority illusion** — users treat Mission Control as the decision-maker.
8. **Silent schema drift** — producers and viewers interpret fields differently.

## Controls

- versioned JSON schema;
- explicit generated timestamp;
- enumerated states;
- separate verification and publication fields;
- read-only browser implementation;
- no repository credentials in the application;
- deterministic validation and findings;
- visible source and update metadata;
- human authorization outside the application;
- fail closed to `INDETERMINATE` when required state is absent.

## Residual limitations

A valid record may still contain incorrect assertions. Mission Control validates structure and exposes declared state; it does not independently establish truth, legal authority, or real-world completion.
