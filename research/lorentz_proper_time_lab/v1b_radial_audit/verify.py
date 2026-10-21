#!/usr/bin/env python3
"""Verify evidence completeness, frozen source and numeric reanalysis."""
import gzip, hashlib, json, subprocess
import numpy as np
from run_control import HERE, ROOT, digest, analyze, schedule

def main():
    out=HERE/'results/control';q=json.loads((HERE/'protocol.json').read_text())
    old=HERE.parent/'v1b_boundary/results'
    verified=0
    for folder in [old,out]:
        for line in (folder/'SHA256SUMS').read_text().splitlines():
            h,name=line.split(maxsplit=1);assert digest(folder/name)==h,name;verified+=1
    saved=json.loads((out/'control_report.json').read_text())
    assert digest(HERE/'finalize_executed.py')==saved['serialization_recovery']['recovery_script_sha256']
    old_trace=json.loads((HERE/'results/historical_trace.json').read_text())['groups'][0]
    assert digest(HERE/'results'/old_trace['file'])==old_trace['file_sha256']
    assert digest(HERE.parent/'core.js')==q['core_sha256']==saved['provenance']['core_sha256']
    freeze=saved['provenance']['freeze_commit']
    for name,h in saved['provenance']['source_sha256'].items():
        assert digest(HERE/name)==h
        assert subprocess.check_output(['git','show',f'{freeze}:{(HERE/name).relative_to(ROOT)}'],cwd=ROOT)==(HERE/name).read_bytes()
    seeds,skipped=schedule(q);s=json.loads((out/'schedule.json').read_text())
    assert seeds==s['mulberry32'] and skipped==s['skipped_without_generating_outputs']
    for arm in ['mulberry32','philox32']:
        r=json.loads((out/f'{arm}_trace.json').read_text());assert len(r['groups'])==32
        streams=[s for g in r['groups'] for s in g['streams']];assert len(streams)==128
        for i,stream in enumerate(streams):
            if arm=='mulberry32':assert stream['seed']==seeds[i]['seed']
            else:assert stream['key']==s['philox_keys'][i]
        for g in r['groups']:
            data=gzip.decompress((out/g['file']).read_bytes());assert len(data)==65536*12
            assert hashlib.sha256(data).hexdigest()==g['raw_sha256']
    computed=analyze(out,q)
    computed=json.loads(json.dumps(computed,default=lambda x:x.item() if isinstance(x,np.generic) else x))
    for k,v in computed.items():assert saved[k]==v,k
    assert saved['original_V1b']=='NOT_PASSED'
    assert len(list(out.glob('*.bin.gz')))==64
    result=dict(status='PASS_EVIDENCE_AND_NUMERIC_REANALYSIS',verified_hashes=verified+2,new_points=4194304,
        original_archive_unchanged=True,source_unchanged=True,protocol_unchanged=True,
        fresh_followup_status=saved['status'],overall_V1b='NOT_PASSED',
        scope='All raw radial traces and primary statistics reanalyzed; source hashes verified. This is not a second independent scientific replication.')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
