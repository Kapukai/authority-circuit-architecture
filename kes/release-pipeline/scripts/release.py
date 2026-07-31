#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ReleaseError(RuntimeError): pass

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''): h.update(chunk)
    return h.hexdigest()

def load(path):
    try: data=json.loads(path.read_text())
    except Exception as exc: raise ReleaseError(f'invalid manifest: {exc}')
    required={'work_order','product','version','status','source_dir','required_files'}
    missing=sorted(required-data.keys())
    if missing: raise ReleaseError('missing fields: '+', '.join(missing))
    if data['status']=='released' and not data.get('release_authority'):
        raise ReleaseError('released status requires release_authority')
    return data

def source_dir(data, manifest):
    raw=Path(data['source_dir']).expanduser()
    candidates=[raw,manifest.parent/raw,Path.cwd()/raw,ROOT.parent.parent/raw]
    for p in candidates:
        if p.resolve().is_dir(): return p.resolve()
    raise ReleaseError('source_dir not found: '+data['source_dir'])

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('manifest',type=Path); ap.add_argument('--dist',type=Path,default=ROOT/'dist'); a=ap.parse_args()
    mp=a.manifest.resolve(); data=load(mp); src=source_dir(data,mp)
    missing=[x for x in data['required_files'] if not (src/x).is_file()]
    if missing: raise ReleaseError('required files missing: '+', '.join(missing))
    verification=[]
    for command in data.get('verification_commands',[]):
        p=subprocess.run(command,cwd=src,text=True,capture_output=True)
        verification.append({'command':command,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        if p.returncode: raise ReleaseError('verification failed: '+' '.join(command)+'\n'+p.stdout+p.stderr)
    slug=data.get('slug') or data['product'].lower().replace(' ','-')
    rid=f"{data['work_order']}-{slug}-v{data['version']}"
    dist=a.dist.resolve(); dist.mkdir(parents=True,exist_ok=True); candidate=dist/rid
    if candidate.exists(): shutil.rmtree(candidate)
    shutil.copytree(src,candidate,ignore=shutil.ignore_patterns('.git','.venv','node_modules','dist','build','__pycache__','*.pyc','.DS_Store'))
    summary=data.get('summary','Verified Kapukai release candidate.')
    (candidate/'GENERATED_RELEASE_NOTES.md').write_text(f"# {data['product']} v{data['version']}\n\n**Work order:** {data['work_order']}  \n**Status:** {data['status']}\n\n{summary}\n\nPrepared by KES-0002. Publication requires explicit human authorization.\n")
    (candidate/'GENERATED_WEBSITE_CARD.md').write_text(f"## {data['product']}\n\n**Version:** {data['version']}  \n**Work order:** {data['work_order']}\n\n{summary}\n")
    (candidate/'GENERATED_ANNOUNCEMENT.md').write_text(f"{data['product']} v{data['version']} is a verified release candidate under {data['work_order']}.\n\n{summary}\n\nHuman release review remains required.\n")
    sums={str(p.relative_to(candidate)):digest(p) for p in sorted(candidate.rglob('*')) if p.is_file()}
    (candidate/'SHA256SUMS.json').write_text(json.dumps(sums,indent=2)+'\n')
    record={'schema':'kapukai.kes.release-record.v0.1','release_id':rid,'generated_at':datetime.now(timezone.utc).isoformat(),'manifest':data,'source':str(src),'verification':verification,'file_count':len(sums),'authorized_for_publication':data['status']=='released' and bool(data.get('release_authority'))}
    (candidate/'RELEASE_RECORD.json').write_text(json.dumps(record,indent=2)+'\n')
    zp=dist/f'{rid}.zip'
    if zp.exists(): zp.unlink()
    with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(candidate.rglob('*')):
            if p.is_file(): z.write(p,Path(rid)/p.relative_to(candidate))
    zh=digest(zp); (dist/f'{rid}.zip.sha256').write_text(f'{zh}  {zp.name}\n')
    print('PASS'); print('release_id='+rid); print('candidate='+str(candidate)); print('zip='+str(zp)); print('publication_authorized='+str(record['authorized_for_publication']).lower())
if __name__=='__main__':
    try: main()
    except ReleaseError as exc: print('FAIL: '+str(exc),file=sys.stderr); raise SystemExit(1)
