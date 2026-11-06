"""Validate the immutable classical evidence and replay without editing it."""
import argparse
import csv
import hashlib
import importlib.util
import io
import json
from decimal import Decimal
from pathlib import Path, PurePosixPath
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent
NAME = 'CST_DUST_Expansion_Trapping_v0_1'
PREFIX = NAME + '/'
ZIP_HASH = 'd5d8f64665595182d445f9d1dfceebf7021c4004641a23801aa0879b89f4eb70'
PDF_HASH = 'a6be2b5f6e35c147ffb94b65f3b037228907b420704f36f50498a820c3339941'
PLAN_HASH = '19dd9611f324a6d91866c5b71dad495a3391ba497e5e9c87a107cd2e4bfedfbd'
PARENT = 'b4a52636c506288462e21d88e0f6bd152a78b540'
GATES = {'MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE', 'REGULARITY',
         'BOUNDARY', 'TRAPPING', 'EXTENSION'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_records(work):
    spec = importlib.util.spec_from_file_location('expansion_parent_gate',
                                                work/'inputs/parent_gate.py')
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    records = json.loads((work/'results/checkpoint_P4_records.json').read_text())
    audits = json.loads((work/'results/checkpoint_P4_audits.json').read_text())
    require(len(records) == len(audits) == 72, 'P4 record count')
    manifest = work/'results/run_manifest.json'
    data = json.loads(manifest.read_text())
    require(data['physical_execution'] == 'NOT_RUN'
            and data['classical_reference_execution'] == 'RUN'
            and data['new_CST_ensembles'] == data['new_random_draws'] == 0
            and data['parent_main_commit'] == PARENT
            and data['plan_sha256'] == PLAN_HASH, 'Execution scope/provenance')
    require(set(data['source_sha256']) == {'analyze.py', 'intervals.py'}, 'Source inventory')
    for name, digest in data['source_sha256'].items():
        require(sha((work/name).read_bytes()) == digest, 'Executed source: '+name)
    actual, fixed, events = [], set(), set()
    for record in records:
        context = record['checkpoint_context']
        require(record['execution'] == 'NOT_RUN' and record['checkpoint_id'] == 'P4'
                and record['run_manifest_sha256'] == sha(manifest.read_bytes()), 'P4 provenance')
        if context['kind'] == 'FIXED_GRID':
            fixed.add((context['density_ratio'], context['M'], context['x']))
        elif context['kind'] == 'REFERENCE_CROSSING':
            events.add((context['density_ratio'], context['M'], context['chi']))
        else:
            raise ValueError('Unexpected P4 context')
        result = gate.evaluate(record, work/'inputs/parent_contract.json', manifest)
        require(result['record_valid'] and result['decisions'] == {g: 'HOLD' for g in GATES},
                'Invalid P4 record or promoted physical decision')
        actual.append({'context': context, **result})
    require(fixed == {(d, m, t) for d in [1, 2, 4, 8] for m in ['1/4', '1', '4']
                      for t in ['0', '1/4', '1/2', '3/4', '1']}, 'Fixed P4 grid')
    require(events == {(d, '4', c) for d in [1, 2, 4, 8] for c in ['9/10', '19/20', '1']},
            'Event P4 grid')
    require(actual == audits, 'Archived P4 audits disagree with parent gate')


def run(replay):
    archive = ROOT.parent/'packages'/(NAME+'_Pruefpaket.zip')
    require(sha(archive.read_bytes()) == ZIP_HASH, 'Original ZIP changed')
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
        require(len(names) == len(set(names)) == 40 and z.testzip() is None, 'ZIP inventory')
        for name in names:
            p = PurePosixPath(name)
            require(not p.is_absolute() and '..' not in p.parts and name.startswith(PREFIX),
                    'Unsafe archive path')
            require((ROOT/name[len(PREFIX):]).read_bytes() == z.read(name), 'Expanded bytes: '+name)

        def read(relative):
            return z.read(PREFIX+relative)

        listed = set()
        for line in read('SHA256SUMS').decode().splitlines():
            digest, name = line.split(maxsplit=1)
            require(name not in listed and sha(read(name)) == digest, 'Member hash: '+name)
            listed.add(name)
        require({PREFIX+n for n in listed} == set(names)-{PREFIX+'SHA256SUMS'}, 'Incomplete hashes')
        pdf = read(NAME+'.pdf')
        require(sha(pdf) == PDF_HASH and pdf == (ROOT.parent/'reports'/(NAME+'.pdf')).read_bytes(),
                'PDF bytes')
        dependencies = {
            'parent_contract.json': 'model_contract_v0_1/contract.json',
            'parent_gate.py': 'model_contract_v0_1/gate.py',
            'correspondence_plan.json': 'correspondence_v0_1/plan.json',
            'correspondence_verification.json': 'correspondence_v0_1/results/verification.json',
            'reference_comparisons.csv': 'correspondence_v0_1/results/reference_comparisons.csv',
            'P3_summary.json': 'correspondence_v0_1/results/checkpoint_P3_summary.json',
            'reference_regularity.json': 'correspondence_v0_1/results/reference_regularity.json',
        }
        provenance = json.loads(read('inputs/provenance.json'))
        require(provenance['parent_main_commit'] == PARENT, 'Parent publication commit')
        require(set(provenance['input_sha256']) == set(dependencies), 'Input inventory')
        for name, path in dependencies.items():
            data = read('inputs/'+name)
            require(data == (ROOT.parent/path).read_bytes()
                    and sha(data) == provenance['input_sha256'][name], 'Predecessor input: '+name)
        require(read('intervals.py') == (ROOT.parent/'correspondence_v0_1/intervals.py').read_bytes()
                and sha(read('intervals.py')) == provenance['intervals_sha256'], 'Interval library')
        require(sha(read('plan.json')) == PLAN_HASH == read('plan.sha256').decode().split()[0],
                'Frozen plan')
        plan = json.loads(read('plan.json'))
        require(plan['numerical']['normalized_expansion_cap'] == '1/200'
                and plan['numerical']['event_bracket_width_cap_x'] == '1/40'
                and plan['numerical']['physical_density_refinement'] is False
                and plan['area_calibration']['absolute_e_cap'] == '1/200', 'Tolerance scope')
        result = json.loads(read('results/verification.json'))
        require(result['controls'] == 25 and result['new_random_draws'] == 0
                and result['new_CST_ensembles'] == 0 and result['paid_runs'] is False, 'Scope/counts')
        require(result['physical_CST_trapping'] == 'HOLD_NOT_ELIGIBLE'
                and result['physical_CST_execution'] == 'NOT_RUN'
                and result['physical_CST_regularity'] == 'HOLD'
                and result['global_event_horizon'] == 'NOT_DETERMINED', 'Scientific decision promoted')
        levels = result['numerical_levels']
        require([r['N'] for r in levels] == [128, 256, 512, 1024]
                and [r['numerical_cap_pass'] for r in levels] == [False, False, True, True]
                and sum(r['interior_spheres'] for r in levels) == 420, 'Numerical levels')
        require(Decimal(levels[-1]['max_absolute_e_error']) < Decimal('0.005'), 'Finest numerical cap')
        require(result['numerical_event_brackets'] == 12 and result['all_bracket_caps_pass'] is True,
                'Event brackets')
        require(result['finest_round_classifications'] == {
            'FUTURE_TRAPPED_ROUND': 4, 'UNTRAPPED_ROUND': 101}, 'Reference signs')
        require(result['hypothetical_5_percent_box_classifications'] == {
            'FUTURE_TRAPPED_ROUND': 1, 'UNTRAPPED_ROUND': 95, 'HOLD_SIGN_UNRESOLVED': 9},
            'Hypothetical uncertainty diagnostic')
        counts = {'sphere_expansions.csv': 420, 'exterior_expansions.csv': 420,
                  'surface_matching.csv': 15, 'area_derivative_calibration.csv': 216,
                  'analytic_crossings.csv': 21, 'numerical_event_brackets.csv': 12}
        for name, expected in counts.items():
            rows = list(csv.DictReader(io.StringIO(read('results/'+name).decode())))
            require(len(rows) == expected, 'Case inventory: '+name)
        controls = json.loads(read('results/controls.json'))
        require(len(controls) == 25 and all(r['pass'] is True and r['actual'] == r['expected']
                                          for r in controls), 'Controls')
        check_records(ROOT)
        if replay:
            with tempfile.TemporaryDirectory(prefix='x6-dust-expansion-') as temp:
                z.extractall(temp)
                work = Path(temp)/NAME
                subprocess.run([sys.executable, '-O', '-B', str(work/'analyze.py')],
                               check=True, capture_output=True, text=True, cwd=work)
                check_records(work)
                expected_results = {name[len(PREFIX):] for name in names
                                    if name.startswith(PREFIX+'results/')}
                actual_results = {p.relative_to(work).as_posix() for p in (work/'results').rglob('*')
                                  if p.is_file()}
                require(expected_results == actual_results and len(expected_results) == 17,
                        'Replayed result inventory')
                for relative in sorted(expected_results):
                    expected, actual = read(relative), (work/relative).read_bytes()
                    if relative == 'results/run_manifest.json':
                        a, b = json.loads(expected), json.loads(actual)
                        require(isinstance(b['python'], str) and b['python'], 'Runtime version missing')
                        a.pop('python'); b.pop('python')
                        require(a == b, relative)
                    elif relative == 'results/checkpoint_P4_records.json':
                        a, b = json.loads(expected), json.loads(actual)
                        # check_records verified each set against its own complete manifest.
                        for record in a+b:
                            record.pop('run_manifest_sha256')
                        require(a == b, relative)
                    else:
                        require(expected == actual, relative)
    print('PASS: original ZIP, 40 members, complete hashes, PDF, predecessor inputs, frozen plan, '
          'all 72 P4 records and separate physical HOLD decisions'
          + ('; isolated replay of all 17 result files agrees' if replay else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--replay', action='store_true')
    run(parser.parse_args().replay)
