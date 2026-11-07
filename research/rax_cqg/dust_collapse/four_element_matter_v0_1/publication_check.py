"""Verify unchanged four-element matter artifacts, source identity and isolated replay."""
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
NAME = 'CST_DUST_Vier_Elemente_Kontinuierliche_Materiephase_v0_1'
PREFIX = 'cst_dust_four_element_matter_v0_1/'
ZIP_HASH = 'd26fdd01ffdb121e3372a8971146366794b99741d6c588e9e70f3c69e68416d2'
PDF_HASH = 'e35a7201a66d7301808acdd6fcce4207e3cde98d5a6822a58c8e82839301c19d'
PLAN_HASH = '89d0a80bc70a25f8cbf06b68b32f391c9f7820b42f3741ec246e002bc89b033f'
PARENT = 'e4787d04c78a1da43825dbbac670a0e3dfacee51'
EXACT = {'geometry_controls.json','quadrature_certificates.json','four_element_amplitudes.json',
         'extended_results.json','tail_reduction.json','verification.json'}
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
            'Pinned source and frozen plan')
    require(set(result['physical_gates']) == GATES and
            set(result['physical_gates'].values()) == {'HOLD'}, 'Eight physical HOLDs')
    require(result['sources_verified'] == 12 and result['formal_proof_checker'] is False and
            result['physical_4D_ensemble'] is False and
            result['physical_boundary_or_detector_selected'] is False, 'Evidence scope')
    require(result['status'] == 'PASS_CERTIFIED_CONTINUOUS_FOUR_ELEMENT_REFERENCE_SECTOR' and
            result['natural_orders'] == 40 and result['action_and_increment_checks'] == 32400 and
            result['exact_four_element_moment_checks'] == 320 and result['previous_method_bridges'] == 28 and
            result['continuous_cases'] == 36 and result['geometry_amplitudes'] == 240 and
            result['count_interval_containment_checks'] == 36 and
            result['field_phases_n_ge_5'] == 'NOT_INTEGRATED', 'Conditional result census')
    require(F(result['max_arithmetic_error']) < F('1.841e-12') and
            F(result['max_quadrature_error']) < F('1.041e-9'), 'Separated certified errors')
    geometry = load('results/geometry_controls.json')
    require(len(geometry['natural_orders']) == 40 and len(geometry['records']) == 80 and
            geometry['action_and_increment_checks'] == 32400 and geometry['exact_moment_checks'] == 320,
            'Complete geometry census')
    neg = geometry['negative_controls']['omitted_entire_jacobian']
    require(neg['cube_integral_of_constant'] == neg['required_normalization'] == 1 and
            neg['wrong_first_moment'] == '-101/162' and neg['required_first_moment'] == '-5/6' and
            neg['normalization_alone_detects_error'] is False and neg['status'] == 'REJECTED_BY_MOMENT',
            'Normalization-preserving Jacobian negative control')
    quad = load('results/quadrature_certificates.json')
    require(quad['native_fraction_bits'] == 60 and quad['node_reference_fraction_bits'] == 160 and len(quad['bridges']) == 28 and
            all(x['status'] == 'PASS' for x in quad['bridges']), 'Certified arithmetic and method bridges')
    arithmetic = quad['arithmetic_controls']
    require(arithmetic['rational_arithmetic_checks'] == 168 and
            arithmetic['pointwise_160_bit_inclusions'] == 52 and
            arithmetic['intentional_overflow'] == 'REJECTED' and
            arithmetic['floating_point_integral'] is False, 'Native arithmetic controls')
    cost = quad['cost_gate']
    require(cost['status'] == 'GO' and cost['paid_compute'] is False and
            cost['node_limit'] == 1200000 and cost['density_call_limit'] == 35000000 and
            cost['runtime_limit_seconds_per_configuration'] == 600 and
            len(cost['configurations']) == 4, 'Frozen cost gate')
    require(sum(x['nodes'] for x in cost['configurations']) == 1305984 and
            sum(x['density_characteristic_calls'] for x in cost['configurations']) ==
            cost['total_density_characteristic_calls'] == 31343616 and
            all(x['nodes'] <= cost['node_limit'] for x in cost['configurations']) and
            cost['total_density_characteristic_calls'] <= cost['density_call_limit'],
            'Actual operation budget')
    for x in quad['rules']:
        require(x['root_sign_brackets'] == x['positive_weights'] == x['order'] and
                x['monomial_checks'] == 2*x['order'], 'Gaussian rule certificates')
    amps = load('results/four_element_amplitudes.json')
    require(len(amps['records']) == 240 and all(F(x['total_error']) <= F('1e-8')
            for x in amps['records']), 'All geometry amplitude tolerances')
    for x in amps['records']:
        require(F(x['total_error']) == F(x['arithmetic_error']) + F(x['quadrature_error']) and
                F(x['arithmetic_error']) <= F('4e-9') and
                F(x['quadrature_error']) <= F('5e-9'), 'Separate error budgets')
    cases = load('results/extended_results.json')
    require(cases['integrated_count_cap'] == 4 and len(cases['cases']) == 36,
            'Continuous four-element cases')
    tails = load('results/tail_reduction.json')
    require(tails['normalization_count_cap'] == 6 and tails['phase_tail_begins_at'] == 5 and
            len(tails['cases']) == tails['count_containment_checks'] == 36 and
            len(tails['weight_reductions']) == 4, 'Separated higher-number tails')
    for x in tails['cases']:
        lo,hi = map(F,x['count_success_infinite_interval'])
        old_lo,old_hi = map(F,x['previous_count_interval'])
        require(0 <= old_lo <= lo <= hi <= old_hi <= 1, 'Count interval inclusion')
        al,au = map(F,x['all_success_infinite_interval'])
        require(0 <= al <= au <= 1 and x['all_interval_intersected_with_previous'] is True,
                'Declared all-number intersection')
        require(F(x['unintegrated_n_ge_5_mass_upper']) == F(x['unintegrated_n5_to_6_mass']) +
                F(x['normalization_tail_n_gt_6_upper']), 'Exact mass and analytic norm tail separated')
        h = F(x['h'])
        require(F(x['normalization_tail_n_gt_6_upper']) == h**7/(factorial(7)*(1-h/8)),
                'Inherited norm tail kept unchanged for direct comparison')
    for x in tails['weight_reductions']:
        removed=1-F(x['new_phase_tail_probability_upper'])/F(x['old_phase_tail_probability_upper'])
        require(removed == F(x['fraction_removed']) and F('0.9358') < removed < F('0.9905'),
                'Certified phase-tail reduction')
    contract = load('four_element_contract.json')
    require(contract['source_commit'] == PARENT and contract['physical_gates'] == result['physical_gates'] and
            contract['physical_boundary_or_detector_selected'] is False and
            contract['physical_4d_dynamics_derived'] is False and
            contract['continuous_integration']['count_cap'] == 4 and
            contract['continuous_integration']['native_fraction_bits'] == 60 and
            contract['external_replication'] is False and contract['formal_proof_checker'] is False and
            contract['infinite_number_enclosures']['n_ge_5_field_phases'] == 'NOT_INTEGRATED',
            'Physical selection and integration contract')

def run(replay=False):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP hash')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 37 and z.testzip() is None, 'Archive inventory')
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
        require(provenance['commit'] == PARENT and len(provenance['files']) == 12, 'Source count')
        for local, record in provenance['files'].items():
            rel = PurePosixPath(record['path'])
            require(not rel.is_absolute() and '..' not in rel.parts, 'Safe source path')
            data = read('inputs/'+local)
            gitsha = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            require(data == (REPO/record['path']).read_bytes() and gitsha == record['sha'],
                    'Byte-identical source: '+local)
        receipt = json.loads(read('results/replay.json'))
        require(receipt['isolated_replay'] == 'PASS' and receipt['result_files'] == 6 and
                {item['name'] for item in receipt['checks']} == EXACT, 'Replay inventory')
        for item in receipt['checks']:
            require(item['byte_identical'] and item['sha256'] == sha(read('results/'+item['name'])),
                    'Replay digest')
        check_scope(read)
        if replay:
            with tempfile.TemporaryDirectory(prefix='cst-four-element-publication-') as tmp:
                z.extractall(tmp)
                work = Path(tmp)/PREFIX
                subprocess.run([sys.executable,'-O','-B','replay.py'],cwd=work,
                               check=True,capture_output=True,text=True)
                require((work/'results/replay.json').read_bytes() == read('results/replay.json'),
                        'Isolated replay receipt')
    print('PASS: original ZIP, 37 members, PDF, twelve byte-identical sources and eight physical HOLDs'+
          ('; six exact result files reproduced byte-for-byte in isolation' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    run(parser.parse_args().replay)
