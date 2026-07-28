import argparse,json
from pathlib import Path
from .dpr import build_record,verify_record,verify_chain,compare_replay
from .dpr_validation import validate_dpr

def main():
    p=argparse.ArgumentParser(prog="kapu-dpr")
    s=p.add_subparsers(dest="cmd",required=True)
    b=s.add_parser("build"); b.add_argument("decision"); b.add_argument("--created-at")
    v=s.add_parser("verify"); v.add_argument("record")
    c=s.add_parser("verify-chain"); c.add_argument("records")
    r=s.add_parser("compare-replay"); r.add_argument("original"); r.add_argument("replayed")
    a=p.parse_args()
    load=lambda x: json.loads(Path(x).read_text())
    if a.cmd=="build":
        out=build_record(load(a.decision),created_at=a.created_at)
        errors=validate_dpr(out)
        if errors: raise SystemExit("schema failure: "+"; ".join(errors))
        print(json.dumps(out,indent=2,sort_keys=True))
    elif a.cmd=="verify":
        rec=load(a.record); errors=validate_dpr(rec)+verify_record(rec)
        print(json.dumps({"valid":not errors,"errors":errors},indent=2))
        raise SystemExit(0 if not errors else 1)
    elif a.cmd=="verify-chain":
        records=load(a.records); errors=verify_chain(records)
        print(json.dumps({"valid":not errors,"errors":errors},indent=2))
        raise SystemExit(0 if not errors else 1)
    else:
        print(json.dumps(compare_replay(load(a.original),load(a.replayed)),indent=2,sort_keys=True))
if __name__=="__main__": main()
