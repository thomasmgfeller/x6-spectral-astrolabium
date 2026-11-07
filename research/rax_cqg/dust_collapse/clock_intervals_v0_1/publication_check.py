"""Verify unchanged clock-intervals artifacts, source identity and isolated replay."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
NAME = 'CST_DUST_Uhrintervalle_Variable_Elementzahl_v0_1'
PREFIX = 'cst_dust_clock_intervals_v0_1/'
ZIP_HASH = '673007adcbb2e4fd3660a31a366e311f11b4225375b5e7c38695734bec5d5974'
PDF_HASH = '49439bc26b564babbdab6d80d03f4fb9ef1cf628bdf117c09653a42c91adbbba'
PLAN_HASH = '6e9655943c1b715a4de23fbec110061c2e63748002e000f572dcdc38afdf3acc'
PARENT = '3a26651cb1476b5e3b5d89c343e11487a012e432'
EXACT = {'interval_sewing.json','counts_norms.json','entropy_bounds.json',
         'horizon_completion.json','weight_alternatives.json','verification.json'}
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
            result['physical_quantum_definition_selected'] is False, 'Evidence scope')
    require(result['finite_global_cap_composition'] == 'PASS' and
            result['raw_uncapped_L2_candidate'] == 'FAIL_ANALYTIC' and
            result['weighted_common_horizon_completion'] == 'PASS_CONDITIONAL_REFERENCE',
            'Scoped result and conditional completion')
    sewing = load('results/interval_sewing.json')
    require(sewing['marked_records'] == 10853 and sewing['full_action_cut_checks'] == 32559 and
            sewing['count_cocycle_checks'] == 97677 and
            sewing['extra_factorial_negative_controls'] == 27, 'Exact sewing controls')
    past = sewing['missing_past_example']
    require(past['correct_increment'] == ['9','27/4'] and
            past['incorrect_isolated_increment'] == ['0','-33/32'], 'Full-past negative control')
    counts = load('results/counts_norms.json')
    require(counts['natural_order_census'] == [1,1,2,7,40,357,4824] and
            counts['independent_counts'] == 51, 'Independent order and extension counts')
    witness = counts['raw_norm_witness']
    require(F(witness['antichain_norm_squared']) == 2 and
            F(witness['chain_norm_squared']) == F(7,4), 'Raw norm counterexample')
    entropy = load('results/entropy_bounds.json')
    require([x['two_layer_records'] for x in entropy['finite_family_controls']] ==
            [1,1,2,4,16,64,512], 'Two-layer family injection')
    require(entropy['raw_infinite_L2_candidate'].startswith('FAIL:'), 'Unbounded raw norm scope')
    horizon = load('results/horizon_completion.json')
    require(horizon['partition_norm_identities'] == horizon['hazard_identities'] == 198 and
            horizon['horizon_coefficient_cocycles'] == 108441, 'Common-horizon identities')
    demos = horizon['terminal_demos']
    require([x['terminal_birth_count_probabilities'] for x in demos] ==
            [['4/7','2/7','1/7'],['8/13','4/13','1/13'],['16/25','8/25','1/25']],
            'Distinct normalized count predictions')
    require(all(sum(map(F,x['terminal_birth_count_probabilities'])) == 1 and
                F(x['no_birth_first_interval'])*F(x['no_birth_second_given_none']) ==
                F(x['terminal_birth_count_probabilities'][0]) for x in demos),
            'No-birth horizon composition')
    naive = horizon['separate_endpoint_normalization_negative_control']
    require(naive['half_interval_Z_product'] == '441/256' and
            naive['full_interval_Z'] == '7/4', 'Separate normalization failure')
    weights = load('results/weight_alternatives.json')
    require(weights['weighted_extension_bound_checks'] == 102 and
            len(weights['tail_controls']) == 24 and
            weights['physical_weight_or_endpoint_selected'] is False, 'Uniform bounds and scope')
    a,b = weights['distinct_uncapped_predictions']
    require(a['Z_remainder_upper'] == b['Z_remainder_upper'] == '1/604800' and
            F(a['infinite_no_birth_probability_interval'][1]) <
            F(b['infinite_no_birth_probability_interval'][0]), 'Certified uncapped nonuniqueness')
    contract = load('interval_contract.json')
    require(contract['basis_commit'] == PARENT and
            contract['physical_quantum_definition_selected'] is False and
            contract['physical_gates'] == result['physical_gates'] and
            contract['weighted_candidate']['physical_weight_selection'] == 'OPEN' and
            contract['common_horizon_completion']['norm'] == 'ISOMETRY_IN_DECLARED_REFERENCE_PRODUCT' and
            contract['common_horizon_completion']['physical_waiting_law'] == 'NOT_DERIVED' and
            contract['nonuniqueness']['coherent_boundary_or_decoherence_functional'] == 'NOT_SELECTED',
            'Physical selection and conditional norm contract')

def run(replay=False):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP hash')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 30 and z.testzip() is None, 'Archive inventory')
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
            with tempfile.TemporaryDirectory(prefix='cst-clock-intervals-publication-') as tmp:
                z.extractall(tmp)
                work = Path(tmp)/PREFIX
                subprocess.run([sys.executable,'-O','-B','replay.py'],cwd=work,
                               check=True,capture_output=True,text=True)
                require((work/'results/replay.json').read_bytes() == read('results/replay.json'),
                        'Isolated replay receipt')
    print('PASS: original ZIP, 30 members, PDF, six byte-identical sources and eight physical HOLDs'+
          ('; six exact result files reproduced byte-for-byte in isolation' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    run(parser.parse_args().replay)
