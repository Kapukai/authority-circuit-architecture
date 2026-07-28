from __future__ import annotations
import hashlib,json
from enum import Enum
from typing import Any

class State(str,Enum):
    ALLOW="ALLOW"; DENY="DENY"; HOLD="HOLD"; CONFLICT="CONFLICT"; REVOKED="REVOKED"; ESCALATE="ESCALATE"

VALUES={"TRUE","FALSE","UNKNOWN","CONFLICTED","NOT-APPLICABLE"}
IDS=("A","J","R","E","P","T","N","C","V")
POS=("A","J","R","E","P","T","N")

def canon(v:Any)->str:
    return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)

def digest(v:Any)->str:
    return hashlib.sha256(canon(v).encode()).hexdigest()

def evaluate(p:dict[str,Any])->dict[str,Any]:
    items=p.get("predicates")
    if not isinstance(items,list): raise ValueError("predicates must be a list")
    m={}
    for x in items:
        if x.get("id") not in IDS or x.get("value") not in VALUES: raise ValueError("invalid predicate")
        if x["id"] in m: raise ValueError("duplicate predicate")
        m[x["id"]]=x["value"]
    missing=[x for x in IDS if x not in m]
    if missing: raise ValueError("missing predicates: "+",".join(missing))

    if m["V"]=="TRUE":
        s,r,e=State.REVOKED,"ACA120.REVOKED","Revocation or prohibition takes precedence."
    elif m["C"]=="TRUE" or "CONFLICTED" in m.values():
        s,r,e=State.CONFLICT,"ACA120.CONFLICT","A material conflict prevents authorization."
    elif any(m[x]=="UNKNOWN" for x in POS):
        s,r,e=State.HOLD,"ACA120.UNKNOWN","A mandatory predicate is unknown."
    elif any(m[x]=="FALSE" for x in POS):
        s,r,e=State.DENY,"ACA120.FALSE","A mandatory authorization predicate is false."
    elif any(m[x]=="NOT-APPLICABLE" for x in POS):
        s,r,e=State.ESCALATE,"ACA120.APPLICABILITY","Applicability requires review."
    elif all(m[x]=="TRUE" for x in POS) and m["C"]=="FALSE" and m["V"]=="FALSE":
        s,r,e=State.ALLOW,"ACA120.ALLOW","All mandatory predicates are satisfied."
    else:
        s,r,e=State.ESCALATE,"ACA120.UNRESOLVED","The cell cannot safely resolve the evaluation."

    proof={
      "record_type":"ACA-140 Decision Proof Record",
      "record_id":p["evaluation_id"],"cell_id":p["cell_id"],
      "profile_version":p["profile_version"],"rule_version":p["rule_version"],
      "predicates":items,"state":s.value,"reason_code":r,
      "input_sha256":digest(p),
      "integrity_note":"A digest proves normalized-input integrity, not factual truth.",
      "human_approval_required":p.get("human_approval_required",True)
    }
    proof["proof_sha256"]=digest(proof)
    return {
      "evaluation_id":p["evaluation_id"],"cell_id":p["cell_id"],
      "state":s.value,"reason_code":r,"explanation":e,
      "authorization":{"authorized":s is State.ALLOW,"state":s.value},
      "execution":{"executed":False,"execution_record_required":s is State.ALLOW},
      "proof_record":proof,
      "remedy":None if s is State.ALLOW else p.get("remedy",{"status":"AVAILABLE","route":"human-review"})
    }

def replay(payload:dict[str,Any],prior:dict[str,Any])->bool:
    cur=evaluate(payload)
    return cur["state"]==prior["state"] and cur["reason_code"]==prior["reason_code"] and cur["proof_record"]["input_sha256"]==prior["proof_record"]["input_sha256"]
