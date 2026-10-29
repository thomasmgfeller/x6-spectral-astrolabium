"""Fail-closed integrity and status checks; no science gate is opened by this script."""
from pathlib import Path
import hashlib
import json

HERE=Path(__file__).resolve().parent
def check(ok,message):
    if not ok:raise SystemExit('FAIL: '+message)
def main():
    manifest={}
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        sha,name=line.split('  ',1);manifest[name]=sha
        check(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==sha,'package hash '+name)
    reconstructed=HERE/'results/reference.npz'
    if reconstructed.exists():
        spec=json.loads((HERE/'results/REFERENCE_ARCHIVE.json').read_text())
        check(hashlib.sha256(reconstructed.read_bytes()).hexdigest()==spec['sha256'],'reconstructed reference archive')
    actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS' and p!=reconstructed}
    check(actual==set(manifest),'complete package inventory')
    freeze=json.loads((HERE/'FREEZE.json').read_text())
    for name,sha in freeze['sha256'].items():
        check(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==sha,'pilot source lock '+name)
    plan=json.loads((HERE/'PROTOCOL.json').read_text());runs=json.loads((HERE/'results/RUNS.json').read_text());r=json.loads((HERE/'results/RESULTS.json').read_text())
    check(len(runs)==64 and len({(x['density_index'],x['realization_index']) for x in runs})==64,'complete run identities')
    check(all(x['status']=='COMPUTED_DIAGNOSTIC' for x in runs),'all planned statuses retained')
    check(r['status']=='HOLD' and not r['confirmation_seed_used'] and not r['Dirac_run'] and not r['flavor_run'],'scientific HOLD retained')
    check(len(r['cells'])==12 and {(c['nu'],c['epsilon']) for c in r['cells']}=={(n,e) for n in plan['nu'] for e in plan['epsilon']},'complete cell matrix')
    check(all(c['draft_tolerance_screen']=='FAIL_TOLERANCE' and c['maximum_field_RMSE']>.1 for c in r['cells']),'negative tolerance result retained')
    check(json.loads((HERE/'results/REFERENCE.json').read_text())['reference_status']=='REFERENCE_HOLD_NO_CERTIFIED_REMAINDER','reference HOLD retained')
    check(json.loads((HERE.parent/'e4_v0_1/contract.json').read_text())['freeze_status']=='NOT_FROZEN','parent contract not silently frozen')
    print(f'PASS: {len(manifest)} package hashes; 64 run identities; HOLD and unused confirmation seed preserved')
if __name__=='__main__':main()
