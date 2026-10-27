"""Integrity, amendment and scope guard. This tool cannot grant E4 G1."""
import hashlib
import json
from pathlib import Path
from flint import arb
from balls import HERE, plan, configure, decode
from run import frozen, sha

def check(ok,message):
    if not ok:
        raise SystemExit('FAIL: '+message)

def main():
    configure(); frozen(); p=plan(); manifest={}
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1);manifest[name]=digest
        check(sha(HERE/name)==digest,'hash '+name)
    actual={str(f.relative_to(HERE)) for f in HERE.rglob('*')
            if f.is_file() and f.name!='SHA256SUMS' and '__pycache__' not in f.parts}
    check(actual==set(manifest),'complete inventory')
    old=json.loads((HERE/'amendment_01/FREEZE_original.json').read_text())
    lock=json.loads((HERE/'FREEZE.json').read_text())
    amendment=json.loads((HERE/'amendment_01/RECORD.json').read_text())
    check(lock['amendment_01']['prior_lock_sha256']==sha(HERE/'amendment_01/FREEZE_original.json'),'prior lock')
    check(old['files']['audit.py']==sha(HERE/'amendment_01/audit_original.py')==amendment['original_audit_sha256'],'original audit')
    check(sha(HERE/'audit.py')==amendment['corrected_audit_sha256'],'corrected audit')
    for name,digest in old['files'].items():
        if name!='audit.py':check(sha(HERE/name)==digest==lock['files'][name],'unchanged production source '+name)
    for name,digest in amendment['unchanged_production_results'].items():
        check(sha(HERE/'results'/name)==digest,'unchanged production result '+name)
    b=json.loads((HERE/'results/BUDGET.json').read_text())
    s=json.loads((HERE/'results/SOURCE.json').read_text())
    check((b['G1'],b['G2'],b['G3'])==('HOLD','NOT_RUN','NOT_RUN'),'E4 gates')
    check(b['confirmation_seed_used'] is False and p['new_random_realizations']==0,'no confirmation draws')
    check(len(b['rows'])==7 and [r['ell_k'] for r in b['rows']]==p['gaussian']['ell_k'],'budget matrix')
    for r in b['rows']:
        check(r['scope']=='one Gaussian witness; no E4 or all-field qualification','witness scope')
        check(decode(r['mean_infinite']).is_finite(),'finite mean ball')
        if r['witness_RMS_target_impossible_at_chosen_H']:
            check(decode(r['relative_RMS_lower_at_any_admissible_density']).real>arb(p['gaussian']['relative_total_RMS_goal']),'necessary exclusion inequality')
        if r['single_witness_total_RMS_within_goal']:
            check(decode(r['relative_RMS_upper_at_sufficient_density']).real<=arb(p['gaussian']['relative_total_RMS_goal']),'sufficient witness inequality')
    identities={(r['probe_index'],r['mass']) for r in s['rows']}
    expected={(i,0) for i in range(28)}|{(i,m) for i in [0,7,14] for m in [1,2]}
    check(len(s['rows'])==34 and identities==expected,'exact source coverage')
    for r in s['rows']:
        z=decode(r['value']);goal=arb(p['source']['absolute_component_radius_goal'])
        check(z.is_finite() and z.real.rad()<=goal and z.imag.rad()<=goal,'finite source enclosure/radius')
        check(r['enclosure_status']=='WITHIN_RADIUS_GOAL','source status')
    check(s['full_reference_status']=='HOLD_OFF_CENTER_MASSIVE_AND_DETECTOR_ERROR_OPEN','full reference HOLD')
    check(s['not_a_detector_trace_distance_bound'] is True,'no detector qualification')
    check(json.loads((HERE.parent/'e4_v0_1/contract.json').read_text())['freeze_status']=='NOT_FROZEN','E4 freeze unchanged')
    a=json.loads((HERE/'AUDIT.json').read_text())
    check(a['software_status']=='PASS' and a['replay']['reference_amplitudes']==34 and a['replay']['budget_rows']==7,'complete replay')
    streams=json.loads((HERE/'PORTABILITY_STREAMS.json').read_text())
    check(streams['script_sha256']==sha(HERE/'portability_audit.py'),'portability source lock')
    expected_keys={f'd{d}_r{i:02d}' for d in range(3) for i in range(16)}
    check(len(streams['rows'])==48 and {r['key'] for r in streams['rows']}==expected_keys,'stream inventory')
    for name in ['PORTABILITY_DEFAULT.json','PORTABILITY_BASELINE.json']:
        pp=json.loads((HERE/'results'/name).read_text())
        check(pp['status']=='PASS_NUMERIC_REPLAY_NOT_GENERAL_BITWISE_REPRODUCIBILITY','numeric-only portability status')
        check(len(pp['runs'])==48 and {r['key'] for r in pp['runs']}==expected_keys,'complete portability replay')
        check(all(r['rng_draws_probe_counts_and_region_masks_exact'] for r in pp['runs']),'exact stream/count/mask checks')
        check(all(r['maximum_coordinate_absolute_difference']<=2.0**-48 for r in pp['runs']),'declared coordinate screen')
        check(pp['negative_controls']==5 and pp['G1']=='HOLD','portability guards and scientific HOLD')
    check(json.loads((HERE/'results/PORTABILITY_DEFAULT.json').read_text())['coordinate_bytes_identical_for_all_runs'] is True,'original CPU path matches archive bytes')
    check(json.loads((HERE/'results/PORTABILITY_BASELINE.json').read_text())['coordinate_bytes_identical_for_all_runs'] is False,'cross-CPU byte limitation retained')
    print(f'PASS: {len(manifest)} hashes; 7 witness budgets; 34 reference enclosures; G1/full reference HOLD')

if __name__=='__main__':main()
