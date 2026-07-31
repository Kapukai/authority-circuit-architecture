#!/usr/bin/env python3
from __future__ import annotations
import argparse, ast, hashlib, html, json, re, subprocess, sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

EXCLUDED = {".git",".venv","venv","node_modules","__pycache__","dist","build",".pytest_cache",".mypy_cache",".next","coverage"}
TEXT_EXTS = {".py",".js",".mjs",".cjs",".ts",".tsx",".jsx",".json",".md",".txt",".toml",".yaml",".yml",".html",".css",".scss",".sh",".zsh",".tex",".csv",".ini",".cfg"}
RULES = [
 ("standards",("standards","docs/tex","aca-","specification","charter")),
 ("products",("products/","product/")),
 ("kes",("kes/","work-order","capability")),
 ("reference-implementation",("reference-implementation/","reference_impl")),
 ("tests",("tests/","test_",".github/workflows")),
 ("tools",("tools/","scripts/")),
 ("site",("site/","website","public_html")),
 ("docs",("docs/","readme","changelog","contributing")),
]

def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def git(repo,*args):
    p=subprocess.run(["git",*args],cwd=repo,text=True,capture_output=True)
    return p.stdout.strip() if p.returncode==0 else ""

def classify(rel):
    value=str(rel).lower()
    for category,needles in RULES:
        if any(n in value for n in needles): return category
    return "other"

def imports_for(path,text):
    if path.suffix==".py":
        try: tree=ast.parse(text)
        except Exception: return []
        out=set()
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                out.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node,ast.ImportFrom) and node.module:
                out.add(node.module.split(".")[0])
        return sorted(out)
    if path.suffix in {".js",".mjs",".cjs",".ts",".tsx",".jsx"}:
        found=set()
        patterns = [
            r'(?:from\s+|import\s*\()\s*["\']([^"\']+)["\']',
            r'require\(\s*["\']([^"\']+)["\']\s*\)'
        ]
        for pattern in patterns:
            found.update(re.findall(pattern,text))
        return sorted(found)
    return []

def refs(text):
    found=set()
    patterns = [
        r"\b(?:ACA|KES|EDS|SDK)-\d{3,4}\b",
        r"\bKAPU\b",
        r"\bAuthority Cell\b",
        r"\bDecision Proof Record\b"
    ]
    for pattern in patterns:
        found.update(re.findall(pattern,text,flags=re.I))
    return sorted(found,key=str.lower)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("repository",nargs="?",default=".")
    ap.add_argument("--output")
    args=ap.parse_args()
    repo=Path(args.repository).expanduser().resolve()
    if not repo.is_dir():
        print(f"FAIL: repository not found: {repo}",file=sys.stderr)
        return 1
    output=Path(args.output).expanduser().resolve() if args.output else Path(__file__).resolve().parents[1]/"dist"/"latest"
    output.mkdir(parents=True,exist_ok=True)

    records=[]; edges=[]; ref_index=defaultdict(list)
    for path in repo.rglob("*"):
        if not path.is_file(): continue
        rel=path.relative_to(repo)
        if any(part in EXCLUDED for part in rel.parts): continue
        record={"path":str(rel),"category":classify(rel),"bytes":path.stat().st_size,"sha256":digest(path),"extension":path.suffix.lower() or "[none]"}
        if path.suffix.lower() in TEXT_EXTS:
            text=path.read_text(encoding="utf-8",errors="ignore")
            record["references"]=refs(text)
            record["imports"]=imports_for(path,text)
            for ref in record["references"]: ref_index[ref].append(str(rel))
            for imp in record["imports"]: edges.append({"source":str(rel),"target":imp})
        records.append(record)

    status=git(repo,"status","--short","--untracked-files=all")
    categories=Counter(r["category"] for r in records)
    extensions=Counter(r["extension"] for r in records)
    inventory={
      "schema":"kapukai.kes.repository-intelligence.v0.1",
      "generated_at":datetime.now(timezone.utc).isoformat(),
      "repository":{"path":str(repo),"branch":git(repo,"branch","--show-current"),"head":git(repo,"rev-parse","HEAD"),"origin":git(repo,"remote","get-url","origin"),"worktree_clean":not bool(status)},
      "summary":{"file_count":len(records),"total_bytes":sum(r["bytes"] for r in records),"categories":dict(sorted(categories.items())),"extensions":dict(sorted(extensions.items())),"reference_count":len(ref_index),"dependency_edge_count":len(edges)},
      "files":records,"references":dict(sorted(ref_index.items())),"dependency_edges":edges
    }

    findings=[]
    if status:
        findings.append({"severity":"warning","code":"WORKTREE_NOT_CLEAN","message":"Modified or untracked paths were observed.","evidence":status.splitlines()[:40],"recommendation":"Classify each path before release or reorganization."})
    paths={r["path"] for r in records}
    for required in ("README.md","SECURITY.md","CHANGELOG.md"):
        if required not in paths:
            findings.append({"severity":"warning","code":"MISSING_GOVERNANCE_FILE","message":f"{required} was not found at repository root.","evidence":[required],"recommendation":"Add it or document the canonical equivalent."})
    if not any(r["category"]=="tests" for r in records):
        findings.append({"severity":"warning","code":"NO_TESTS_OBSERVED","message":"No test-classified files were observed.","evidence":[],"recommendation":"Add tests or document external verification."})
    if not any(".github/workflows/" in r["path"] for r in records):
        findings.append({"severity":"info","code":"NO_CI_WORKFLOW_OBSERVED","message":"No GitHub Actions workflow was observed.","evidence":[],"recommendation":"Consider CI after local verification is stable."})

    joined=" ".join(r["path"].lower() for r in records)
    stages=[
      ("ACA standards foundation","aca-" in joined or "standards" in joined,"Maintain"),
      ("Authority Cell formalization","authority" in joined and "cell" in joined,"Maintain"),
      ("KAPU reference implementation","kapu" in joined or "reference-implementation" in joined,"Verify"),
      ("KES capability operating system","kes" in joined,"Maintain"),
      ("KES-0002 release pipeline","release-pipeline" in joined,"Verify"),
      ("EDS-0003 replay explorer","decision-replay-explorer" in joined,"Release candidate"),
      ("KES-0003 repository intelligence",True,"Current"),
      ("EDS-0004 human authorization","human-authorization" in joined,"Next"),
      ("EDS-0005 DPR viewer","dpr-viewer" in joined,"Queued"),
      ("External demonstration",False,"Queued"),
      ("External pilot",False,"Primary milestone"),
    ]
    critical=[{"stage":a,"observed":b,"status":c} for a,b,c in stages]

    (output/"repository-inventory.json").write_text(json.dumps(inventory,indent=2)+"\n")
    (output/"findings.json").write_text(json.dumps(findings,indent=2)+"\n")

    lines=["# Repository Map","",f"- Generated: {inventory['generated_at']}",f"- Repository: `{repo}`",f"- Branch: `{inventory['repository']['branch'] or '[unknown]'}`",f"- HEAD: `{inventory['repository']['head'] or '[unknown]'}`",f"- Worktree clean: **{inventory['repository']['worktree_clean']}**",f"- Files observed: **{len(records)}**","","## Categories","","| Category | Files |","|---|---:|"]
    lines += [f"| {k} | {v} |" for k,v in sorted(categories.items())]
    lines += ["","## Referenced architecture terms",""]
    lines += [f"- **{k}** — {len(v)} file(s)" for k,v in sorted(ref_index.items())]
    (output/"repository-map.md").write_text("\n".join(lines)+"\n")

    cp=["# Critical Path","","Inference from repository evidence; human review determines truth and priority.","","| Observed | Stage | Status |","|---|---|---|"]
    cp += [f"| {'Yes' if s['observed'] else 'No'} | {s['stage']} | {s['status']} |" for s in critical]
    cp += ["","## Governing heuristic","","> Preserve the platform, complete the authority circuit, demonstrate it, and obtain one external pilot before broad expansion."]
    (output/"critical-path.md").write_text("\n".join(cp)+"\n")

    dot=['digraph repository {','  rankdir="LR";','  node [shape=box];']
    for edge in edges:
        src=edge["source"].replace('"','\\"')
        tgt=edge["target"].replace('"','\\"')
        dot.append(f'  "{src}" -> "{tgt}";')
    dot.append('}')
    (output/"dependency-graph.dot").write_text("\n".join(dot)+"\n")

    cards="".join("<article><span>{}</span><strong>{}</strong></article>".format(html.escape(k),v) for k,v in sorted(categories.items()))
    frows="".join("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(html.escape(f["severity"]),html.escape(f["code"]),html.escape(f["message"])) for f in findings) or "<tr><td colspan='3'>No findings</td></tr>"
    prows="".join("<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format("✓" if s["observed"] else "—",html.escape(s["stage"]),html.escape(s["status"])) for s in critical)
    dashboard = (
      '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width">'
      '<title>KES-0003</title><style>body{font-family:system-ui;background:#07111f;color:#edf4ff;margin:0}'
      'main{max-width:1100px;margin:auto;padding:40px 22px}h1{font-size:clamp(2rem,6vw,4.5rem);margin:.2em 0}'
      'p{color:#aab9cc}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}'
      'article,section{background:#0e1c2e;border:1px solid #29405e;border-radius:16px;padding:18px;margin:16px 0}'
      'article span{display:block;color:#aab9cc}article strong{font-size:2rem}table{width:100%;border-collapse:collapse}'
      'td,th{padding:10px;border-bottom:1px solid #29405e;text-align:left}.badge{display:inline-block;padding:7px 10px;'
      'border:1px solid #65d99a;border-radius:999px;color:#65d99a}</style></head><body><main>'
      '<span class="badge">READ-ONLY ANALYSIS</span><h1>Repository Intelligence</h1><p>Generated '
      + html.escape(inventory["generated_at"]) +
      '. Observability report, not authority to modify.</p><div class="grid">' + cards +
      '</div><section><h2>Critical path</h2><table><tr><th>Observed</th><th>Stage</th><th>Status</th></tr>'
      + prows + '</table></section><section><h2>Findings</h2><table><tr><th>Severity</th><th>Code</th>'
      '<th>Observation</th></tr>' + frows + '</table></section></main></body></html>'
    )
    (output/"dashboard.html").write_text(dashboard)

    sums={p.name:digest(p) for p in sorted(output.iterdir()) if p.is_file()}
    (output/"SHA256SUMS.json").write_text(json.dumps(sums,indent=2)+"\n")
    print("PASS")
    print(f"repository={repo}")
    print(f"files={len(records)}")
    print(f"findings={len(findings)}")
    print(f"worktree_clean={not bool(status)}")
    print(f"output={output}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
