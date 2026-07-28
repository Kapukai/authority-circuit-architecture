#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
MAP={"authority":"authority.schema.json","authority-derivation":"authority-derivation.schema.json","evidence":"evidence.schema.json","rule-profile":"rule-profile.schema.json","evaluation-request":"evaluation-request.schema.json","decision-proof-record":"decision-proof-record.schema.json","remedy":"remedy.schema.json","change-point":"change-point.schema.json","conformance-report":"conformance-report.schema.json"}
def load(p):
 with p.open(encoding="utf-8") as f:return json.load(f)
def registry(d):
 r=Registry(); ss={}
 for p in sorted(d.glob("*.schema.json")):
  s=load(p); ss[p.name]=s; r=r.with_resource(s["$id"],Resource.from_contents(s))
 return r,ss
def validate(d,name,instance):
 r,ss=registry(d); fn=MAP.get(name,name); v=Draft202012Validator(ss[fn],registry=r,format_checker=FormatChecker()); return sorted(v.iter_errors(load(instance)),key=lambda e:list(e.absolute_path))
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--schema-dir",type=Path,required=True);ap.add_argument("--schema",required=True);ap.add_argument("instance",type=Path);a=ap.parse_args();errs=validate(a.schema_dir,a.schema,a.instance)
 if errs:
  print(f"INVALID {a.instance}")
  for e in errs: print("  - "+("/".join(map(str,e.absolute_path)) or "<root>")+": "+e.message)
  return 1
 print(f"VALID {a.instance}");return 0
if __name__=="__main__":raise SystemExit(main())
