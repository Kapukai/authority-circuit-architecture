#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    tmp=Path(tmp); repo=tmp/"repo"; repo.mkdir()
    subprocess.run(["git","init"],cwd=repo,check=True,capture_output=True)
    (repo/"README.md").write_text("# Demo\nACA-120 Authority Cell\n")
    (repo/"products"/"demo").mkdir(parents=True)
    (repo/"products"/"demo"/"app.py").write_text("import json\n")
    (repo/"tests").mkdir()
    (repo/"tests"/"test_demo.py").write_text("assert True\n")
    out=tmp/"out"
    p=subprocess.run([sys.executable,str(ROOT/"scripts/analyze.py"),str(repo),"--output",str(out)],capture_output=True,text=True)
    assert p.returncode==0,p.stdout+p.stderr
    inv=json.loads((out/"repository-inventory.json").read_text())
    assert inv["summary"]["file_count"]==3
    assert inv["summary"]["categories"]["products"]==1
    assert "ACA-120" in inv["references"]
    for name in ["dashboard.html","critical-path.md","SHA256SUMS.json","findings.json","dependency-graph.dot"]:
        assert (out/name).is_file()
print("PASS test_analyze.py")
