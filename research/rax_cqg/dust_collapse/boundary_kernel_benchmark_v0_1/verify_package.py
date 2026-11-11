#!/usr/bin/env python3
"""Offline package verification; physical decisions remain scoped and separate."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from package import ROOT, ARCHIVE, MANIFEST, files, archive_bytes

def require(condition, message):
    if not condition:raise RuntimeError(message)

def read_json(name):
    return json.loads((ROOT/name).read_text(encoding='utf-8'))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--replay',action='store_true')
    args=parser.parse_args()
    manifest=read_json(MANIFEST)
    require(manifest['algorithm']=='sha256','Unsupported digest algorithm')
    actual={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in files()}
    require(actual==manifest['files'],'Package inventory or SHA256 mismatch')
    for name in actual:
        if name.endswith('.json'):read_json(name)
    provenance=read_json('provenance.json')
    originals=0
    for source in provenance['sources']:
        name=source['local_copy']
        if name:
            data=(ROOT/name).read_bytes()
            sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            require(sha==source['git_blob_sha'],'Original source identity mismatch: '+name)
            originals+=1
    require(originals==5,'Expected five original inputs')
    result=read_json('results/verification.json');status=read_json('status.json')
    require(result['control_count']==len(result['controls'])==status['software_controls']['count']==41,'Control count mismatch')
    require(len({x['id'] for x in result['controls']})==41 and all(x['result']=='PASS' for x in result['controls']),'Duplicate or failed controls')
    gates={x:'HOLD' for x in ['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']}
    require(result['physical_gates']==status['physical_gates']==gates,'Physical gate state mismatch')
    require(result['parent_raw_kernel_decision']==status['parent_raw_kernel_decision']==read_json('results/raw_clock_kernel.json')['decision']=='FAIL_EVERY_COMMON_POSITIVE_METRIC','Historical scoped FAIL changed')
    require(result['eight_state_matter_matrix']==status['eight_state_matter_matrix']=='NOT_CONSTRUCTED','Unverified eight-state matrix claim')
    require(result['K_0plus']==status['K_0plus']=='NOT_COMPUTED','Unverified mixed-block claim')
    require(result['external_replication']==status['external_replication']=='NOT_EXECUTED','Unverified external replication')
    require(result['paid_compute'] is False and status['paid_compute'] is False,'Execution scope mismatch')
    pending=read_json('OFFENE_RANDBASIS.json')
    require(pending['state']=='NOT_CONSTRUCTED','Pending boundary basis was promoted')
    for key in ['basis_functions','basis_rank','physical_clock_and_zero_stratum_clock','G_in','G_out','K','K_0plus','K_Schur_0','K_Schur_plus']:
        require(pending[key] is None,'Unknown data replaced: '+key)
    require(pending['single_zero_block_implies_superselection'] is False,'Invalid superselection rule')
    label=read_json('results/label_quotient.json')
    require(label['labeled_support_states']==15 and label['orbits']==10 and label['common_map_to_GEOM']=='NOT_CONSTRUCTED','Label scope mismatch')
    pdf=(ROOT/'CST_DUST_Randkern_Benchmark_v0_1.pdf').read_bytes()
    require(pdf.startswith(b'%PDF-') and pdf.rstrip().endswith(b'%%EOF'),'Malformed PDF envelope')
    links=0
    for md in ROOT.glob('*.md'):
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',md.read_text(encoding='utf-8')):
            if '://' in target or target.startswith(('#','../','mailto:')):continue
            if target==ARCHIVE and not (ROOT/ARCHIVE).is_file():continue
            require((md.parent/target.split('#')[0]).is_file(),'Broken local link: '+target)
            links+=1
    archive_present=(ROOT/ARCHIVE).is_file()
    if archive_present:require((ROOT/ARCHIVE).read_bytes()==archive_bytes(),'ZIP differs from deterministic rebuild')
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='cst-randkern-replay-') as tmp:
            target=Path(tmp)/'results'
            subprocess.run([sys.executable,'-I','-O','-B',str(ROOT/'benchmark.py'),'--output',str(target)],check=True,cwd=tmp)
            names={p.name for p in (ROOT/'results').glob('*.json')}
            require(names=={p.name for p in target.glob('*.json')} and len(names)==5,'Replay result inventory mismatch')
            for name in names:require((target/name).read_bytes()==(ROOT/'results'/name).read_bytes(),'Replay differs: '+name)
    print(f'PASS: {len(actual)} file digests, 5 source identities, {links} local links'
          + (', deterministic ZIP' if archive_present else ', extracted package')
          + (', isolated byte-identical replay of 5 results' if args.replay else ''))
    print('Physical gates: 8 HOLD; proposed matter matrix: NOT_CONSTRUCTED; parent raw-clock FAIL preserved')

if __name__=='__main__':main()
