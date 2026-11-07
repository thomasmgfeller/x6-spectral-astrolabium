"""Verify unchanged alpha-dependent norm-tail artifacts, source identity and isolated replay."""
import argparse
from fractions import Fraction as F
from math import factorial
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
NAME = 'CST_DUST_Alpha_Abhaengige_Normrestschranke_v0_1'
PREFIX = 'cst_dust_alpha_normtail_v0_1/'
ZIP_HASH = '30f519f3db1197933f32ca5cbf5eef908231f7000e08879ddbb9da250c716835'
PDF_HASH = 'b18c24053a8a0eefe7b4f3cd4310c6c89a37360dd276c73296b9b83ac2f5f1ef'
PLAN_HASH = '3e02c09940c35349fbf64374bb22466e2e1189355c0c632c911007b6303eba78'
PARENT = '0067da907da4ea8df5b625ea9f8f99ce1527e9ed'
EXACT = {'combinatorial_certificate.json','tail_bound_certificate.json','refined_results.json',
         'improvement_summary.json','verification.json'}
GATES = {'MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION'}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_scope(read):
    load = lambda name: json.loads(read(name))
    result = load('results/verification.json')
    require(result['source_commit'] == PARENT and result['plan_sha256'] == PLAN_HASH,
            'Pinned source and plan')
    require(set(result['physical_gates']) == GATES and
            set(result['physical_gates'].values()) == {'HOLD'}, 'Eight physical HOLDs')
    require(result['status'] == 'PASS_ALPHA_DEPENDENT_ANCHORED_NORMTAIL_REFERENCE_MODEL' and
            result['sources_verified'] == 8 and result['production_normalization_cap'] == 6 and
            result['field_integration_cap'] == 4 and result['new_field_integrals'] == 0 and
            result['field_phases_n_ge_5'] == 'NOT_INTEGRATED' and
            result['all_amplitude_inputs_unchanged'] is True, 'Conditional scope')
    for field in ['external_replication','formal_proof_checker',
                  'physical_density_boundary_or_detector_selected','physical_4d_dynamics_derived']:
        require(result[field] is False, 'Unclaimed physical selection or certification')
    require(result['natural_order_counts_validation'] == [1,1,2,7,40,357,4824,96428] and
            result['proof_grid_valid_cases'] == 157 and result['proof_grid_rejected_ratio_cases'] == 11 and
            result['majorant_recurrence_checks'] == 7536 and
            result['count_interval_containment_checks'] == result['coherent_interval_containment_checks'] == 36 and
            result['accepted_count_interval_containment_checks'] == 180, 'Control census')
    census = load('results/combinatorial_certificate.json')
    require([x['natural_orders'] for x in census['records']] == result['natural_order_counts_validation'] and
            census['n7_count_is_validation_only'] is True and census['exact_normalization_cap_used'] == 6,
            'Enumeration and production cutoff separated')
    cert = load('results/tail_bound_certificate.json')
    require(len(cert['records']) == 157 and len(cert['invalid_ratio_cases']) == 11 and
            cert['majorant_recurrence_checks'] == 7536 and cert['enumerated_partial_tail_checks'] == 157,
            'Tail certificate census')
    for x in cert['records']:
        require(0 <= F(x['q']) < 1 and
                F(x['enumerated_partial_tail_through_7']) <= F(x['anchored_tail_upper']) <=
                F(x['universal_alpha_tail_upper']), 'Positive finite control below analytic tail')
        if x['inherited_tail_upper'] is not None:
            require(F(x['universal_alpha_tail_upper']) <= F(x['inherited_tail_upper']), 'Inherited bound dominance')
    require(all(F(x['q']) >= 1 and x['status'] == 'REJECTED' for x in cert['invalid_ratio_cases']),
            'Invalid geometric ratios rejected')
    for name in ['wrong_alpha_instead_of_alpha_minus_one','dropped_N6_multiplicity']:
        x=cert['negative_controls'][name]
        require(x['status'] == 'REJECTED' and F(x['wrong_upper']) < F(x['actual_c7']),
                'False tail underbounds exact seventh-sector mass')
    require(len(cert['negative_controls']['invalid_domain']) == 4 and
            all(x['status'] == 'REJECTED' for x in cert['negative_controls']['invalid_domain']),
            'Four invalid-domain controls')
    data=load('results/refined_results.json')
    require(data['integrated_count_cap'] == 4 and data['normalization_count_cap'] == 6 and
            data['phase_tail_begins_at'] == 5 and len(data['cases']) == 36, 'Refined result scope')
    key=lambda x:(x['alpha'],x['h'],x['g_over_pi'],x['mu'])
    prior={key(x):x for x in load('inputs/prior_extended_results.json')['cases']}
    require(len({key(x) for x in data['cases']}) == 36, 'Unique parameter cases')
    for x in data['cases']:
        for current,previous in [('count_success_infinite_interval','previous_count_interval'),
                                 ('all_success_infinite_interval','previous_all_interval'),
                                 ('all_success_infinite_raw_interval','previous_all_raw_interval')]:
            lo,hi=map(F,x[current]);old_lo,old_hi=map(F,x[previous])
            require(0 <= old_lo <= lo <= hi <= old_hi <= 1, 'Probability interval containment')
        fields={name:prior[key(x)][name] for name in
                ['number_amplitude_centers','number_amplitude_errors','number_visibility_intervals']}
        require(sha(json.dumps(fields,sort_keys=True).encode()) == x['inherited_amplitude_data_sha256'],
                'Unchanged inherited amplitude data')
        require(x['new_field_integrals'] == 0 and x['all_interval_intersected_with_previous'] is True and
                F(x['unintegrated_n_ge_5_mass_upper']) == F(x['unintegrated_n5_to_6_mass']) +
                F(x['normalization_tail_n_gt_6_upper']), 'Unknown phases and norm tail separated')
    summary=load('results/improvement_summary.json')['records']
    require(len(summary) == 4, 'Four parameter-pair summaries')
    for x in summary:
        require(x['exact_N6'] == 4824 and F(x['anchor_fraction']) == F(603,4096) and
                F(x['anchored_norm_tail_upper']) == F(x['anchor_fraction'])*F(x['universal_alpha_tail_upper']),
                'Exact count-anchored factor')
        reduction=1-F(x['new_phase_tail_probability_upper'])/F(x['old_phase_tail_probability_upper'])
        require(reduction == F(x['phase_tail_fraction_removed']), 'Actual phase-tail improvement')
        lo,hi=(F('0.8184'),F('0.9491')) if x['alpha'] == 2 else (F('0.0036'),F('0.0148'))
        require(lo < reduction < hi, 'Published improvement range')
    contract=load('alpha_normtail_contract.json')
    require(contract['source_commit'] == PARENT and contract['physical_gates'] == result['physical_gates'] and
            contract['implementation']['new_field_integrals'] == 0 and
            contract['implementation']['n7_count_used_in_production_bound'] is False and
            contract['implementation']['inherited_amplitudes_and_errors_unchanged'] is True and
            contract['physical_4d_dynamics_derived'] is False, 'Contract scope')

def run(replay=False):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP hash')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 31 and z.testzip() is None, 'Archive inventory')
        for name in names:
            rel = PurePosixPath(name)
            require(not rel.is_absolute() and '..' not in rel.parts and name.startswith(PREFIX),
                    'Safe archive member')
            require(z.read(name) == (ROOT/name[len(PREFIX):]).read_bytes(), 'Original bytes: '+name)
        read = lambda name: z.read(PREFIX+name)
        listed = set()
        for line in read('MANIFEST.sha256').decode().splitlines():
            digest, rel = line.split(maxsplit=1)
            require(rel not in listed and sha(read(rel)) == digest, 'Manifest entry: '+rel)
            listed.add(rel)
        require({PREFIX+r for r in listed} == set(names)-{PREFIX+'MANIFEST.sha256'},
                'Complete manifest')
        require(sha(read(NAME+'.pdf')) == PDF_HASH and read(NAME+'.pdf') ==
                (ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(), 'PDF copies')
        require(sha(read('plan.json')) == PLAN_HASH == read('plan.sha256').decode().split()[0],
                'Frozen plan digest')
        provenance = json.loads(read('inputs/provenance.json'))
        require(provenance['commit'] == PARENT and len(provenance['files']) == 8, 'Source count')
        for local, record in provenance['files'].items():
            rel = PurePosixPath(record['path'])
            require(not rel.is_absolute() and '..' not in rel.parts, 'Safe source path')
            data = read('inputs/'+local)
            gitsha = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            require(data == (REPO/record['path']).read_bytes() and gitsha == record['sha'],
                    'Byte-identical source: '+local)
        receipt = json.loads(read('results/replay.json'))
        require(receipt['isolated_replay'] == 'PASS' and receipt['result_files'] == 5 and
                {item['name'] for item in receipt['checks']} == EXACT, 'Replay inventory')
        for item in receipt['checks']:
            require(item['byte_identical'] and item['sha256'] == sha(read('results/'+item['name'])),
                    'Replay digest')
        check_scope(read)
        if replay:
            with tempfile.TemporaryDirectory(prefix='cst-alpha-normtail-publication-') as tmp:
                z.extractall(tmp)
                work = Path(tmp)/PREFIX
                subprocess.run([sys.executable,'-B','replay.py'],cwd=work,
                               check=True,capture_output=True,text=True)
                require((work/'results/replay.json').read_bytes() == read('results/replay.json'),
                        'Isolated replay receipt')
    print('PASS: original ZIP, 31 members, PDF, eight byte-identical sources and eight physical HOLDs'+
          ('; five exact result files reproduced byte-for-byte in isolation' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    run(parser.parse_args().replay)
