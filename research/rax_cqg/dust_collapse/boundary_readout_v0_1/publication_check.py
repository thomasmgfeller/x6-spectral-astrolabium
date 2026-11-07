"""Verify unchanged boundary-readout artifacts, source identity and isolated replay."""
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
NAME = 'CST_DUST_Kohaerente_Randauslese_Dekohaerenz_v0_1'
PREFIX = 'cst_dust_boundary_readout_v0_1/'
ZIP_HASH = 'f4ae8ff4b00a07eb2fd398d9a45cb421fb9fa121835a92df495258eb6c6183a0'
PDF_HASH = 'a1fdb8fde19e8b744508930689523e0d975ffebdcc6ef7c2fd5e224c7c97e43a'
PLAN_HASH = '01597b51c463b22c0f4302676009d2563966ba2ac7f900c4c9238b413fa82a83'
PARENT = '36afc462dc5a9503616e9b016481e3b441b7c123'
EXACT = {'continuous_gravity.json','tail_bounds.json','boundary_audit.json',
         'event_functionals.json','negative_controls.json','verification.json'}
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
            result['physical_boundary_or_quantum_law_selected'] is False, 'Evidence scope')
    require(result['bounded_readout_and_pullback'] == 'PASS_REFERENCE' and
            result['continuous_gravity_interference'] == 'PASS_REFERENCE_WITH_CERTIFIED_NUMBER_TAIL' and
            result['continuous_matter_phase_integral'] == 'NOT_EVALUATED' and
            result['nonzero_matter_phase_atomic_controls'] == 'PASS_STANDALONE_MEASURE' and
            result['number_channel_decoherence'] == 'PASS_FOR_TERMINAL_NUMBER_PARTITION' and
            result['all_past_event_algebras_decohere'] == 'NOT_CLAIMED', 'Conditional result scope')
    audit = load('results/boundary_audit.json')
    require(audit['terminal_records'] == 921 and audit['pullback_component_checks'] == 6240 and
            audit['fixed_past_functional_cut_checks'] == 72 and len(audit['cases']) == 12,
            'Atomic records and exact pullback checks')
    require(all(0 <= F(x['all_number_success']) <= F(x['number_channel_success']) <= 1 and
                x['terminal_count_medium_decoherence'] is True and
                F(x['action_cotransformed_boundary_success']) == 1 for x in audit['cases']),
            'Nested effects and co-transformed-boundary control')
    events = load('results/event_functionals.json')
    require(len(events['cases']) == 12 and all(
            y['success_audit']['medium_decoherent'] is False and
            F(y['success_audit']['total_mass'])+F(y['complement_audit']['total_mass']) == 1
            for x in events['cases'] for y in x['readouts']), 'Past partition and completeness')
    continuous = load('results/continuous_gravity.json')
    require([sum(h.values()) for h in continuous['gravity_histograms']] == [1,1,2,7,40,357,4824],
            'Independent natural-order census')
    fringe = continuous['two_geometry_fringe']
    require(fringe['pre_readout_count_probabilities'] == ['8/13','4/13','1/13'] and
            [x['complete_success'] for x in fringe['cases']] == ['1','25/26','12/13'] and
            fringe['cases'][2]['accepted_count_probabilities'] == ['2/3','1/3','0'],
            'Exact continuous gravity fringe')
    tails = load('results/tail_bounds.json')
    require(len(tails['cases']) == 8 and all(x['Z_remainder_upper'] == '1/604800' and
            F(x['all_coupling_single_success_lower']) > 0 and
            F(x['all_coupling_block_success_lower']) > 0 for x in tails['cases']),
            'Certified number tail and nonzero-denominator bounds')
    neg = load('results/negative_controls.json')
    require(neg['unequal_preparation']['success']['normalized_atoms'][0][0] == {'re':'4','im':'0'} and
            neg['balanced_dark_control']['normalized_atoms'] is None and
            neg['overscaled_effect']['putative_probability'] == '2' and
            neg['overscaled_effect']['complement_positivity_rejected'] is True and
            neg['rank_one_multiple_positive_decoherent_atoms'] == 'FAIL_ANALYTIC',
            'Interference, dark, overscaled and rank controls')
    contract = load('boundary_contract.json')
    require(contract['source_commit'] == PARENT and
            contract['physical_gates'] == result['physical_gates'] and
            contract['physical_boundary_selected'] is False and
            contract['physical_4d_law_derived'] is False and
            contract['continuous_nonzero_matter_phase_integral'] == 'NOT_EVALUATED' and
            contract['infinite_time_quantum_measure'] == 'NOT_CLAIMED', 'Contract claim boundary')


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
            with tempfile.TemporaryDirectory(prefix='cst-boundary-readout-publication-') as tmp:
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
