# KAPU-0001 — Authority Cell Engine

First executable reference implementation of ACA-120.

It evaluates A, J, R, E, P, T, N, C, and V; emits an ACA-130 state; separates
authorization from execution; emits an ACA-140-style Decision Proof Record;
attaches remedy metadata; and supports deterministic replay.

Install:

```bash
bash install.sh ~/Kapukai/authority-circuit-architecture
```

Verify:

```bash
~/Kapukai/authority-circuit-architecture/reference-implementation/kapu/scripts/verify.sh
```
