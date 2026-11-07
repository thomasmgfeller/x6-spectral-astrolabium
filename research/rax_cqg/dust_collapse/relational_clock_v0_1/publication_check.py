"""Verify unchanged relational-clock artifacts, source identity and isolated replay."""
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
NAME = 'CST_DUST_Relationale_Uhr_Kandidatenpruefung_v0_1'
PREFIX = 'cst_dust_relational_clock_v0_1/'
ZIP_HASH = 'd7788615b01c9bbb040a8b1834545c981b311b0d19b4c02ecd3bbfe88d9c204d'
PDF_HASH = '4187a735c9357dfc3e1ee1a0cf1e432f5b6493a16904b760986ab6d8089152d1'
PLAN_HASH = '379d6101c9fb29f8faf5847919e44e83b0292ff30a15446f1160ebb43eccfa0e'
PARENT = '5e08cef8dcac5c7d1214dd2beff1b1533427e856'
EXACT = {'clock_ordering.json','domain_measure.json','birth_norms.json',
         'instrument_completion.json','stationarity.json','verification.json'}
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
            result['new_physical_4D_ensemble'] is False and
            result['physical_clock_or_metric_selected'] is False, 'Evidence scope')
    require(result['candidate_closed_fixed_birth_isometry'] ==
            'FAIL_ANALYTIC_FULL_STAGE_CLASS', 'Scoped candidate exclusion')
    ordering = load('results/clock_ordering.json')
    require(ordering['total_natural_marked_representations'] == 88324 and
            ordering['total_chronological_marked_records'] == 14704 and
            ordering['open_and_closed_phase_covariance_checks'] == 88324 and
            ordering['threshold_ideal_checks'] == 29440 and
            ordering['wrong_factor_entries_detected'] == 14020, 'Exact ordering controls')
    require(ordering['nonmonotone_cut_negative_control']['is_ideal'] is False,
            'Nonmonotone cut negative control')
    measure = load('results/domain_measure.json')
    require(measure['sector_restriction_is_gauge'] == 'NO' and
            measure['two_element_type_weights']['ordered_sector'] ==
            {'antichain':'1/2','chain':'1/2'}, 'Sector selection and measure')
    norms = load('results/birth_norms.json')
    require(len(norms['packets']) == 50 and
            [x['output_norm_squared'] for x in norms['packets'][0]['windows']] ==
            ['5/4','3/4'], 'Preparation norm counterexample')
    require([x['output_norm_squared'] for x in norms['packets'][0]['endpoint_packets']] ==
            ['1/4','1/8','1/16','1/32','1/64'], 'Endpoint obstruction controls')
    inst = load('results/instrument_completion.json')
    require(inst['pointwise_checks'] == 250 and len(inst['two_outcome_controls']) == 4 and
            all(F(x['birth_probability'])+F(x['no_birth_probability']) == 1
                for x in inst['two_outcome_controls']), 'Instrument completeness')
    require(inst['overscaled_birth_effect'] == '3/2' and
            inst['overscaled_complement'] == '-1/2' and
            inst['physical_no_birth_law'] == 'NOT_DERIVED' and
            inst['scale_selected'] == 'NO', 'Instrument scope and negative control')
    saddle = load('results/stationarity.json')
    require(saddle['after_gamma'][-1] == '-1' and
            saddle['new_density_derivative'] == '0' and
            saddle['after_clock_gradient'][1] == '7/120' and
            saddle['old_free_clock_equation_preserved'] is False,
            'Full-history stationarity counterexample')
    contract = load('clock_contract.json')
    require(contract['clock_sector']['selection_is_pure_gauge'] is False and
            contract['clock_sector']['chronological_coefficient'] ==
            'one, after the exact natural-label multiplicity cancellation' and
            contract['fixed_birth_continuation']['bounded_coercive_metric_isometry'] ==
            'FAIL_ANALYTIC_ON_FULL_STAGE_SPACES_FOR_M_GE_1' and
            contract['readout']['same_clock_interval_evolution'] == 'NOT_CONSTRUCTED' and
            contract['physical_selection'] == 'OPEN' and
            contract['all_eight_physical_gates'] == 'HOLD', 'Candidate contract scope')


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
            with tempfile.TemporaryDirectory(prefix='cst-relational-clock-publication-') as tmp:
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
