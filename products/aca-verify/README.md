# ACA Verify v0.1.1 Candidate

> **SAFETY HOLD:** This is a candidate declared-predicate interpreter. It is
> not approved for release, deployment, pilots, marketing claims, real cases,
> or consequential reliance. See [SAFETY_HOLD.md](docs/SAFETY_HOLD.md).

ACA Verify is a dependency-free, deterministic interpreter for the public
Decision Proof Record (DPR) schema. It evaluates one synthetic or supplied DPR
against an explicit partial conformance profile and returns `PASS`, `WARN`,
`FAIL`, or `INDETERMINATE` with canonical ACA references and minimum repairs.

ACA Verify does **not** determine truth, legality, legitimacy, credibility, or
authorization. It does not fetch source artifacts, recompute their digests, or
independently establish the supplied facts. A passing result means only that
the supplied declarations satisfy the selected machine-checkable profile.
Human authorization remains separate.

## Run

```bash
python3 products/aca-verify/src/aca_verify.py \
  products/aca-verify/examples/passing-decision.json

python3 products/aca-verify/src/aca_verify.py \
  products/aca-verify/examples/failing-decision.json --format json

# Treat WARN as a failing workflow result.
python3 products/aca-verify/src/aca_verify.py \
  products/aca-verify/examples/warning-decision.json --strict
```

Without `--strict`, exit codes are `0` for `PASS` and `WARN`, `1` for `FAIL`,
`2` for `INDETERMINATE`, and `3` for invalid input or configuration. With
`--strict`, `WARN` also exits `1`. Strict mode is the GitHub Action default.

## Verify the package

```bash
python3 products/aca-verify/scripts/verify.py
python3 products/aca-verify/tests/test_aca_verify.py
```

## GitHub Action

```yaml
- uses: Kapukai/authority-circuit-architecture/.github/actions/aca-verify@main
  with:
    record: decisions/example.json
    strict: "true"
```

Pin a release tag or commit SHA for consequential workflows. The action fails
for `WARN` and `FAIL` by default and returns a distinct nonzero result for
`INDETERMINATE`. No tag is authorized while the safety hold is active.
