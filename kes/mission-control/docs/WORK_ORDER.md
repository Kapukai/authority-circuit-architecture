# KES-0004 — Mission Control

**Status:** Candidate work order  
**Class:** KES control-plane capability  
**Branch:** `kes/kes-0004-mission-control`

## Mission

Create a read-only program control surface that turns repository, roadmap, work-order, release, research, product, and risk state into one inspectable program view.

Mission Control must answer:

1. What exists?
2. What state is each item in?
3. What depends on what?
4. What is on the critical path?
5. What is blocked, stale, disputed, or unverified?
6. What is the next authorized work order?

## Inputs

- repository inventory;
- branch and pull-request state;
- work-order records;
- release records;
- roadmap and critical-path records;
- verification state;
- risk and finding records;
- human authorization records.

## Outputs

- canonical machine-readable program-state record;
- portfolio dashboard;
- dependency and critical-path view;
- branch and pull-request register;
- risk and finding register;
- next-authorized-work display;
- deterministic validation report.

## Safety boundaries

Mission Control is observational and advisory only.

It must not:

- merge branches;
- publish releases;
- deploy software;
- modify work orders;
- close risks or findings;
- declare legal authority;
- authorize consequential actions;
- infer completion from code presence alone.

## Decision states

Every tracked item must use one explicit state:

- `PROPOSED`
- `AUTHORIZED`
- `IN_PROGRESS`
- `BLOCKED`
- `VERIFIED`
- `ACCEPTED`
- `RELEASED`
- `DEFERRED`
- `SUPERSEDED`
- `WITHDRAWN`
- `INDETERMINATE`

## Acceptance criteria

KES-0004 is acceptable when it can:

- validate a program-state file against a versioned schema;
- render standards, products, KES capabilities, research programs, releases, branches, risks, and dependencies in one browser view;
- distinguish verification from acceptance and acceptance from release;
- display the critical path without claiming authority to alter it;
- surface missing owners, stale items, broken dependencies, and unresolved branch dispositions;
- operate without external runtime dependencies;
- preserve existing ACA, KAPU, EDS, release, and public-site behavior.

## Initial critical path represented by the candidate

`Repository reconciliation → KES-0004 Mission Control → AIM-0000 Program Charter → EDS-0004 Human Authorization → AIM-0001 Measurement Primitives → EDS-0005 DPR Explorer → AIM synthetic corpus → AIM agent prototype → ACA-200 research overview → controlled pilot`

## Human gate

Only the human Chief Architect may approve changes to program state, critical path, work-order authorization, release status, or publication status.
