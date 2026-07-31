# Local Run

From the repository root:

```bash
python3 kes/mission-control/scripts/verify.py
python3 -m http.server 8000 --directory kes/mission-control
```

Then open:

```text
http://localhost:8000/app/
```

Optional tests:

```bash
python3 -m pytest kes/mission-control/tests/test_verify.py
```
