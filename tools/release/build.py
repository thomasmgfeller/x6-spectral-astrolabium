#!/usr/bin/env python3
"""Build deterministic, small source/data handoff from a clean pinned Git checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[2]
TAG='reference-2026.10.15'

def build(output):
    status=subprocess.check_output(['git','status','--porcelain','--untracked-files=normal'],cwd=ROOT)
    if status:raise ValueError('clean checkout required')
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT).decode().strip()
    names=set(json.loads((ROOT/'REFERENCE_SOURCE_MANIFEST.json').read_text())['files'])
    names.update(['REFERENCE_SOURCE_MANIFEST.json','CITATION.cff','LICENSE','LICENSE_SCOPE.md','NOTICE','docs/OFFLINE_REFERENCE.md'])
    for folder in ['experimental/rax_guarded','tests/rax-guarded','docs/validation-v1','docs/agent-archive/2026-10-15','tools/release']:
        names.update(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
    payload={n:(ROOT/n).read_bytes() for n in sorted(names)}
    manifest={'schema':'x6.reference-bundle/1','release_tag':TAG,'source_commit':commit,
      'scope':'Nine finite reference reports, guarded declarative runner, selected original agent evidence. No industrial performance, physical acceptance or external review claim.',
      'files':{n:hashlib.sha256(data).hexdigest() for n,data in payload.items()}}
    payload['RELEASE_BUNDLE.json']=(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()
    output.mkdir(parents=False,exist_ok=False);name='x6-'+TAG+'.zip'
    with zipfile.ZipFile(output/name,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for n,data in sorted(payload.items()):
            info=zipfile.ZipInfo('x6-reference/'+n,(1980,1,1,0,0,0));info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    h=hashlib.sha256((output/name).read_bytes()).hexdigest()
    (output/'SHA256SUMS').write_text(h+'  '+name+'\n')
    (output/'BUILD.json').write_text(json.dumps({'source_commit':commit,'archive_sha256':h,'bytes':(output/name).stat().st_size,'files':len(payload)},indent=2)+'\n')
    print((output/'BUILD.json').read_text())

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();build(a.output)
