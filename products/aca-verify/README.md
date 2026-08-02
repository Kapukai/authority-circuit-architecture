# ACA Verify v0.1

ACA Verify is a dependency-free, deterministic interpreter for the public
Decision Proof Record (DPR) schema. It evaluates one synthetic or supplied DPR
against an explicit partial conformance profile and returns `PASS`, `WARN`,
`FAIL`, or `INDETERMINATE` with canonical ACA references and minimum repairs.

ACA Verify does **not** determine truth, legality, legitimacy, credibility, or
authorization. A passing result means only that the supplied record satisfies
the declared machine-checkable profile. Human authorization remains separate.

## Run

```bash
python3 products/aca-verify/src/aca_verify.py \
  products/aca-verify/examples/passing-decision.json

python3 products/aca-verify/src/aca_verify.py \
  products/aca-verify/examples/failing-decision.json --format json
```

Exit codes are `0` for `PASS` and `WARN`, `1` for `FAIL`, `2` for
`INDETERMINATE`, and `3` for invalid input or configuration.

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
```

Pin a release tag or commit SHA for consequential workflows. The action fails
for `FAIL`, returns a distinct nonzero result for `INDETERMINATE`, and succeeds
for `PASS` and `WARN`.
