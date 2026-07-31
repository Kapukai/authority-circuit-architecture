# EDS-0004 — Human Authorization

EDS-0004 defines the human authorization layer that sits between verified information and consequential action.

## Purpose

Prevent verification, recommendation, confidence, or system output from being mistaken for permission to act.

## Core invariant

**Verification is not authorization.**

A system may establish that a method ran, that evidence was supplied, or that a result was reproduced. Only an accountable human may authorize a consequential action, and that authorization must be explicit, scoped, attributable, time-bounded, reviewable, and revocable where possible.

## Candidate outputs

- authorization record schema;
- human decision interface contract;
- scope and duration controls;
- dissent, abstention, and refusal states;
- conflict-of-interest disclosure;
- reason and evidence references;
- rollback and remedy conditions;
- audit and replay requirements.

## Non-goals

EDS-0004 does not determine legality, legitimacy, guilt, entitlement, credibility, or truth. It does not automate authorization, infer consent, or convert a passing verification result into permission to act.

## Critical-path role

AIM-0000 establishes the research boundary. EDS-0004 establishes accountable human authorization before AIM-0001 measurement primitives can be used in governed workflows.
