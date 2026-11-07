"""Verify unchanged operational-matter artifacts, source identity and isolated replay."""
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
NAME = 'CST_DUST_Messmodell_Kontinuierliche_Materiephase_v0_1'
PREFIX = 'cst_dust_operational_matter_v0_1/'
ZIP_HASH = 'c5029b9d6dd5d32f0902ae2d57db8e73c2136f22a72b3b61aceb0690bc6fe681'
PDF_HASH = 'd9f0ed39817d7bfc3b11bed29b8b8351122061514cf999e82c4dbb157cc79f31'
PLAN_HASH = '386387f9d0c5db4c037ee6b6a678ed1bfcef83f6a01b47067f6d003b4c31e024'
PARENT = '35a0d886c4a7ca1d639f09b2933ffeb6c255ad9e'
EXACT = {'moments.json','continuous_results.json','certified_bounds.json',
         'instrument.json','negative_controls.json','verification.json'}
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
            'Source and frozen plan')
    require(set(result['physical_gates']) == GATES and
            set(result['physical_gates'].values()) == {'HOLD'}, 'Eight physical HOLDs')
    require(result['sources_verified'] == 6 and result['formal_proof_checker'] is False and
            result['physical_4D_ensemble'] is False and
            result['physical_boundary_or_detector_selected'] is False, 'Evidence scope')
    require(result['operational_pointer_dilation'] == 'EXACT_REFERENCE_PASS' and
            result['count_only_phase_sensitivity'] == 'FAIL_ANALYTIC' and
            result['continuous_nonzero_matter_phase'] == 'CERTIFIED_FOR_N_LE_2' and
            result['higher_number_field_phases'] == 'NOT_EVALUATED' and
            result['normalization_tail'] == 'CERTIFIED_THROUGH_N6' and
            result['continuous_cases'] == 36, 'Conditional result scope')
    ins = load('results/instrument.json')
    require(ins['unitary_dimension'] == 16 and ins['orthogonal_projector_products'] == 16 and
            ins['unitarity'] == ins['kraus_completeness'] == 'EXACT_PASS' and
            ins['count_only_probabilities'] == ['1','1'] and
            ins['coherent_success_probabilities'] == ['1','0'] and
            ins['nonselective_record_disturbance']['after'] == ['0','0','1/2','1/2'] and
            ins['physical_detector_selected'] is False, 'Operational instrument and disturbance')
    moments = load('results/moments.json')
    require(moments['action_polynomial_checks'] == 390 and
            moments['independent_low_order_moment_checks'] == 16 and
            len(moments['records']) == 6 and all(len(x['moments']) == 49 and
            x['moments'][0] == '1' for x in moments['records']), 'Continuous moment census')
    require(F(moments['max_amplitude_remainder']) == F(10**49,factorial(49)) and
            F(moments['max_amplitude_remainder']) < F('1.65e-14'), 'Certified integration error')
    continuous = load('results/continuous_results.json')
    require(continuous['count_cap'] == 2 and continuous['taylor_order'] == 48 and
            len(continuous['cases']) == 36 and continuous['published_gravity_fringe_checks'] == 3,
            'Continuous cases and published gravity controls')
    witness = next(x for x in continuous['cases'] if x['alpha'] == 1 and x['h'] == '1/2'
                   and x['g_over_pi'] == '1/9' and x['mu'] == '1')
    lo,hi = map(F,witness['number_visibility_intervals'][2])
    require(F('0.053484072766766') <= lo <= hi <= F('0.053484072766800'),
            'Certified matter phase lifts the dark two-geometry output')
    bounds = load('results/certified_bounds.json')
    require(bounds['normalization_enumerated_through'] == 6 and len(bounds['cases']) == 36 and
            bounds['physical_couplings_selected'] is False, 'Higher-number bound scope')
    for x in bounds['cases']:
        for key in ['count_success_infinite_interval','all_success_infinite_interval']:
            lo,hi = map(F,x[key]);require(0 <= lo <= hi <= 1, 'Bounded probability interval')
    for h in ['1/4','1/2']:
        intervals = [next(x['count_success_infinite_interval'] for x in bounds['cases'] if
                     x['h'] == h and x['alpha'] == alpha and x['g_over_pi'] == '0' and x['mu'] == '1')
                     for alpha in [1,2]]
        require(F(intervals[0][1]) < F(intervals[1][0]) < F(intervals[1][1]) < 1,
                'Certified preparation dependence below phase-free success')
    neg = load('results/negative_controls.json')
    require(neg['density_atom_omitted']['status'] == 'REJECTED' and
            neg['ordered_clock_factor_two_omitted']['status'] == 'REJECTED' and
            neg['higher_number_phases_integrated'] is False, 'Measure and scope negatives')
    contract = load('operational_contract.json')
    require(contract['source_commit'] == PARENT and contract['physical_gates'] == result['physical_gates'] and
            contract['physical_detector_selected'] is False and
            contract['cosmological_boundary_selected'] is False and
            contract['physical_4d_dynamics_derived'] is False and
            contract['continuous_integration']['count_cap'] == 2 and
            contract['infinite_number_enclosures']['n_ge_3_field_phases'] == 'NOT_EVALUATED',
            'Physical selection and integration contract')


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
        require(provenance['commit'] == PARENT and len(provenance['files']) == 6, 'Source count')
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
            with tempfile.TemporaryDirectory(prefix='cst-operational-matter-publication-') as tmp:
                z.extractall(tmp)
                work = Path(tmp)/PREFIX
                subprocess.run([sys.executable,'-O','-B','replay.py'],cwd=work,
                               check=True,capture_output=True,text=True)
                require((work/'results/replay.json').read_bytes() == read('results/replay.json'),
                        'Isolated replay receipt')
    print('PASS: original ZIP, 31 members, PDF, six byte-identical sources and eight physical HOLDs'+
          ('; six exact result files reproduced byte-for-byte in isolation' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    run(parser.parse_args().replay)
