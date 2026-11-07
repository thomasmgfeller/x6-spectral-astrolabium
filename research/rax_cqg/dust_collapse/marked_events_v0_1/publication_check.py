"""Verify unchanged marked-events artifacts, source identity and isolated replay."""
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
NAME = 'CST_DUST_Markierte_Zustaende_Ereignisse_v0_1'
PREFIX = 'cst_dust_marked_events_v0_1/'
ZIP_HASH = '6df972fb1e4b53eec4c693ff61ecc6afe83ef4d755206d103fb6a7c9facc6e1e'
PDF_HASH = '167decf4a0c64b2358d2ca8dfba60669466b4bd169374f95ceff45bb3b2deae3'
PLAN_HASH = '6eea1d379814c77dfe50e02ae6946da030dfea3eb1074ad181447abe27c8a0c2'
PARENT = '57aea796ac1f35c31ca3fabce45e0a27c518a5bf'
EXACT = {'marked_quotient.json','action_covariance.json','metrics_records.json',
         'current_events.json','terminal_readout.json','verification.json'}
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
    require(result['provenance_files_checked'] == 7 and result['formal_proof_checker'] is False,
            'Evidence scope')
    quotient = load('results/marked_quotient.json')
    require(quotient['natural_marked_counts'] == [1,2,8,56,640] and
            quotient['orbit_counts'] == [1,2,7,32,192], 'Marked census')
    require(quotient['representative_columns_checked'] == 67 and
            quotient['independent_deletion_entries'] == 6384, 'Quotient checks')
    actions = load('results/action_covariance.json')
    require(actions['permutations_checked_open_and_closed'] == 15715 and
            actions['increments_checked'] == 706, 'Exact action controls')
    metrics = load('results/metrics_records.json')
    require(len(metrics['metrics']) == len(metrics['records']) == 4 and
            all(F(p) > 0 for record in metrics['metrics'] for p in record['LDL_pivots']),
            'Positive products and records')
    events = load('results/current_events.json')
    require(events['putative_Born_weight'] == '-1/149' and
            events['M_selfadjoint'] == 'FAIL_EXPECTED' and
            events['sum_atom_diagonals'] == '153/149', 'Current-event negative control')
    terminal = load('results/terminal_readout.json')
    require(terminal['cut_pullback'] == ['8/3']*3+['11/6']*4 and
            terminal['original_sum_cut_compatibility'] == 'FAIL_EXPECTED', 'Readout cut defect')
    require(all(x['overscaled_witness_probability'] == '2' for x in terminal['finite_effects']),
            'Readout scaling negative control')
    contract = load('event_contract.json')
    require(contract['continuous_marked_quotient']['physical_constraint_quotient'] == 'NOT_DERIVED' and
            contract['positive_products']['physical_selection'] == 'OPEN' and
            contract['event_options']['physical_event_algebra'] == 'NOT_SELECTED' and
            contract['coherent_endpoint']['actual_physical_boundary_readout'] == 'OPEN',
            'Physical selection remains open')


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
        provenance = json.loads(read('inputs/git_sources.json'))
        require(provenance['commit'] == PARENT and len(provenance['files']) == 7, 'Source count')
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
            with tempfile.TemporaryDirectory(prefix='cst-marked-events-publication-') as tmp:
                z.extractall(tmp)
                work = Path(tmp)/PREFIX
                subprocess.run([sys.executable,'-O','-B','replay.py'],cwd=work,
                               check=True,capture_output=True,text=True)
                require((work/'results/replay.json').read_bytes() == read('results/replay.json'),
                        'Isolated replay receipt')
    print('PASS: original ZIP, 31 members, PDF, seven byte-identical sources and eight physical HOLDs'+
          ('; six exact result files reproduced byte-for-byte in isolation' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay',action='store_true')
    run(parser.parse_args().replay)
