"""Integrity/status checks, intentionally incapable of granting G1."""
from pathlib import Path
import hashlib
import json
HERE=Path(__file__).resolve().parent
def check(ok,message):
    if not ok:raise SystemExit('FAIL: '+message)
def main():
    manifest={}
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        h,name=line.split('  ',1);manifest[name]=h
        check(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,'package hash '+name)
    actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p.name!='SHA256SUMS' and '__pycache__' not in p.parts}
    check(actual==set(manifest),'complete package inventory')
    lock=json.loads((HERE/'FREEZE.json').read_text())
    for group,folder in [('sources',HERE),('dependencies',HERE.parent/'scalar_pilot_v0_1')]:
        for name,h in lock[group].items():check(hashlib.sha256((folder/name).read_bytes()).hexdigest()==h,'source lock '+name)
    runs=json.loads((HERE/'results/RUNS.json').read_text());result=json.loads((HERE/'results/RESULTS.json').read_text())
    check(len(runs)==48 and {(r['density_index'],r['realization_index']) for r in runs}=={(d,i) for d in range(3) for i in range(16)},'all planned identities')
    check(all(r['status']=='COMPUTED_DIAGNOSTIC' for r in runs),'all statuses accounted for')
    check(result['scientific_status']=='HOLD' and result['G1']=='HOLD' and result['G2']=='NOT_RUN' and result['G3']=='NOT_RUN','science gates preserved')
    check(result['confirmation_seed_used'] is False,'confirmation phase unused')
    check(len(result['cells'])==27 and all(c['all_16_finite'] for c in result['cells']),'complete cell matrix')
    check(result['source_reference']['reference_status']=='HOLD_NO_VALIDATED_REMAINDER','source-reference qualification blocked')
    check(json.loads((HERE.parent/'e4_v0_1/contract.json').read_text())['freeze_status']=='NOT_FROZEN','original contract unchanged')
    print(f'PASS: {len(manifest)} hashes, 48 planned runs, 27 cells; scientific HOLD preserved')
if __name__=='__main__':main()
