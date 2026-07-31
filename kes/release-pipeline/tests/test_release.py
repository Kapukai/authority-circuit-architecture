#!/usr/bin/env python3
from pathlib import Path
import json,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as d:
    d=Path(d); src=d/'product'; src.mkdir(); (src/'README.md').write_text('# Demo\n'); (src/'RELEASE_NOTES.md').write_text('# Notes\n')
    m={'work_order':'EDS-9999','product':'Synthetic Product','slug':'synthetic-product','version':'0.1.0','status':'release-candidate','source_dir':str(src),'required_files':['README.md','RELEASE_NOTES.md'],'verification_commands':[],'summary':'Synthetic test.','release_authority':None}
    mp=d/'manifest.json'; mp.write_text(json.dumps(m)); dist=d/'dist'
    p=subprocess.run([sys.executable,str(ROOT/'scripts/release.py'),str(mp),'--dist',str(dist)],capture_output=True,text=True)
    assert p.returncode==0,p.stdout+p.stderr
    c=dist/'EDS-9999-synthetic-product-v0.1.0'; assert (c/'RELEASE_RECORD.json').is_file(); assert (dist/'EDS-9999-synthetic-product-v0.1.0.zip').is_file()
    assert json.loads((c/'RELEASE_RECORD.json').read_text())['authorized_for_publication'] is False
print('PASS test_release.py')
