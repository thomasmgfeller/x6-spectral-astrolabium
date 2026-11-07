"""Verify unchanged three-element matter artifacts, source identity and isolated replay."""
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
NAME = 'CST_DUST_Drei_Elemente_Kontinuierliche_Materiephase_v0_1'
PREFIX = 'cst_dust_three_element_matter_v0_1/'
ZIP_HASH = 'e4afc101569a203e335e1286a833fa5ce9c115ce62ae2cb9e6df5598c01b3a5f'
PDF_HASH = 'eade58888523f3640ffc3a8aa70e935a53d7e7f4d0534c513d8bf5dedb654c01'
PLAN_HASH = 'a2fcfbfbcd5c283ceeb4df612caf5e7d1e719617042671373931f8ff3e2225ed'
PARENT = '9869528d008966a88052b65216da14eafce8db6f'
EXACT = {'geometry_controls.json','quadrature_certificates.json','three_element_amplitudes.json',
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
    require(result['sources_verified'] == 8 and result['formal_proof_checker'] is False and
            result['physical_4D_ensemble'] is False and
            result['physical_boundary_or_detector_selected'] is False, 'Evidence scope')
    require(result['status'] == 'PASS_CERTIFIED_CONTINUOUS_THREE_ELEMENT_REFERENCE_SECTOR' and
            result['natural_orders'] == 7 and result['action_and_increment_checks'] == 3780 and
            result['exact_three_element_moment_checks'] == 56 and result['previous_method_bridges'] == 3 and
            result['continuous_cases'] == 36 and result['geometry_amplitudes'] == 42 and
            result['count_interval_containment_checks'] == 36 and
            result['field_phases_n_ge_4'] == 'NOT_INTEGRATED', 'Conditional result census')
    require(F(result['max_arithmetic_error']) < F('1.61e-37') and
            F(result['max_quadrature_error']) < F('6.50e-12'), 'Separated certified errors')
    geometry = load('results/geometry_controls.json')
    require(len(geometry['natural_orders']) == 7 and len(geometry['records']) == 14 and
            geometry['action_and_increment_checks'] == 3780 and geometry['exact_moment_checks'] == 56,
            'Complete geometry census')
    neg = geometry['negative_controls']['omitted_entire_jacobian']
    require(neg['cube_integral_of_constant'] == neg['required_normalization'] == 1 and
            neg['wrong_first_moment'] == '-107/216' and neg['required_first_moment'] == '-5/8' and
            neg['normalization_alone_detects_error'] is False and neg['status'] == 'REJECTED_BY_MOMENT',
            'Normalization-preserving Jacobian negative control')
    quad = load('results/quadrature_certificates.json')
    require(quad['fixed_point_bits'] == 160 and len(quad['bridges']) == 3 and
            all(x['status'] == 'PASS' for x in quad['bridges']), 'Certified arithmetic and method bridges')
    for x in quad['rules']:
        require(x['root_sign_brackets'] == x['positive_weights'] == x['order'] and
                x['monomial_checks'] == 2*x['order'], 'Gaussian rule certificates')
    amps = load('results/three_element_amplitudes.json')
    require(len(amps['records']) == 42 and all(F(x['total_error']) <= F('1e-10')
            for x in amps['records']), 'All geometry amplitude tolerances')
    cases = load('results/extended_results.json')
    require(cases['integrated_count_cap'] == 3 and len(cases['cases']) == 36,
            'Continuous three-element cases')
    tails = load('results/tail_reduction.json')
    require(tails['normalization_count_cap'] == 6 and tails['phase_tail_begins_at'] == 4 and
            len(tails['cases']) == tails['count_containment_checks'] == 36 and
            len(tails['weight_reductions']) == 4, 'Separated higher-number tails')
    for x in tails['cases']:
        lo,hi = map(F,x['count_success_infinite_interval'])
        old_lo,old_hi = map(F,x['previous_count_interval'])
        require(0 <= old_lo <= lo <= hi <= old_hi <= 1, 'Count interval inclusion')
        al,au = map(F,x['all_success_infinite_interval'])
        require(0 <= al <= au <= 1 and x['all_interval_intersected_with_previous'] is True,
                'Declared all-number intersection')
        require(F(x['unintegrated_n_ge_4_mass_upper']) == F(x['unintegrated_n4_to_6_mass']) +
                F(x['normalization_tail_n_gt_6_upper']), 'Exact mass and analytic norm tail separated')
    for x in tails['weight_reductions']:
        removed=1-F(x['new_phase_tail_probability_upper'])/F(x['old_phase_tail_probability_upper'])
        require(removed == F(x['fraction_removed']) and F('0.9136') < removed < F('0.9944'),
                'Certified phase-tail reduction')
    contract = load('three_element_contract.json')
    require(contract['source_commit'] == PARENT and contract['physical_gates'] == result['physical_gates'] and
            contract['physical_boundary_or_detector_selected'] is False and
            contract['physical_4d_dynamics_derived'] is False and
            contract['continuous_integration']['count_cap'] == 3 and
            contract['infinite_number_enclosures']['n_ge_4_field_phases'] == 'NOT_INTEGRATED',
            'Physical selection and integration contract')

def run(replay=False):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP hash')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 35 and z.testzip() is None, 'Archive inventory')
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
        require(receipt['isolated_replay'] == 'PASS' and receipt['result_files'] == 6 and
                {item['name'] for item in receipt['checks']} == EXACT, 'Replay inventory')
        for item in receipt['checks']:
            require(item['byte_identical'] and item['sha256'] == sha(read('results/'+item['name'])),
                    'Replay digest')
        check_scope(read)
        if replay:
            with tempfile.TemporaryDirectory(prefix='cst-three-element-publication-') as tmp:
                z.extractall(tmp)
                work = Path(tmp)/PREFIX
                subprocess.run([sys.executable,'-O','-B','replay.py'],cwd=work,
                               check=True,capture_output=True,text=True)
                require((work/'results/replay.json').read_bytes() == read('results/replay.json'),
                        'Isolated replay receipt')
    print('PASS: original ZIP, 35 members, PDF, eight byte-identical sources and eight physical HOLDs'+
          ('; six exact result files reproduced byte-for-byte in isolation' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    run(parser.parse_args().replay)
