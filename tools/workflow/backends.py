"""Adapters preserve native scientific formats and conclusions. Apache-2.0."""
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
RAX_ARCHIVE = 'docs/research/rax/method-review-v0.1/RAX_M1_Methodenpruefung_v0_1_Paket.zip'
RAX_SHA = '8f74c7b4133d85369178d6f3edf25b46c9c6f6aaf899576d5150fdb6a0c00d7a'
MODULES = ('signal', 'spectral', 'rax')


def source_paths(module):
    common = ['x6.py', 'tools/workflow/cli.py', 'tools/workflow/backends.py', 'tools/workflow/requirements-research.txt']
    if module == 'signal':
        return common + ['tools/workflow/signal_adapter.cjs', 'experimental/edge_reference/runner.cjs', 'app/signal-lab-core.js', 'app/signal-lab-evidence.js', 'app/signal-lab-build.js']
    if module == 'spectral':
        return common + ['tests/python/independent_audit.py']
    if module == 'rax':
        return common + [RAX_ARCHIVE]
    raise ValueError('Unknown module')


def rational_run(output, execute):
    output.mkdir()
    script = output / 'independent_audit.py'
    shutil.copyfile(ROOT / 'tests/python/independent_audit.py', script)
    execute([sys.executable, str(script)], 'spectral-reference')
    return json.loads((output / 'python_results.local.json').read_text())


def rax_run(archive, results, execute, extract, digest):
    if digest(archive.read_bytes()) != RAX_SHA:
        raise ValueError('RAX approved archive digest mismatch')
    with tempfile.TemporaryDirectory(prefix='x6-rax-') as temp:
        temp = Path(temp)
        extract(archive, temp / 'package')
        package = temp / 'package/RAX_M1_Methodenpruefung_v0_1'
        execute([sys.executable, str(package / 'reproduce.py'), '--workdir', str(temp / 'reproduction')], 'rax-reproduction')
        shutil.copytree(temp / 'reproduction/method-results', results)
        shutil.copyfile(temp / 'reproduction/REPRODUCTION.json', results / 'REPRODUCTION.json')
    review = json.loads((results / 'METHOD_REVIEW.json').read_text())
    receipt = json.loads((results / 'REPRODUCTION.json').read_text())
    if receipt['status'] != 'PASS' or review['original_primary_decisions_changed'] is not False:
        raise ValueError('RAX reproduction did not pass')
    return review


def scientific_summary(module, result):
    if module == 'signal':
        return {'native_schema': 'x6.signal-lab.evidence/1', 'result': result['quality_status'], 'scope': 'Synthetic signal screening; same-engine replay is not independent validation.'}
    if module == 'spectral':
        if result['passed'] != result['total'] or result['total'] != 5:
            raise ValueError('Rational fixture audit failed')
        return {'native_schema': result['schema'], 'result': {'passed': result['passed'], 'total': result['total']}, 'scope': 'Five fixed exact rational graph fixtures; not a run of every browser module or physical validation.'}
    return {'native_schema': 'RAX-M1-20261014-001', 'result': {'primary_conclusions': result['checks']['00_original_replay']['primary_decisions'], 'method_findings': {k: v['status'] for k, v in result['checks'].items()}, 'original_files_unchanged': result['original_files_unchanged']}, 'scope': 'Internal post-hoc RAX-B1/M1 replay; not new acquisition, external review, U2 or physical evidence.'}


def run(module, native, job, execute, extract, digest, imported=None):
    if module == 'signal':
        job = job or ROOT / 'experimental/edge_reference/examples/synthetic-signal.json'
        command, input_path = ('import', imported) if imported else ('run', job)
        result = execute(['node', str(ROOT / 'tools/workflow/signal_adapter.cjs'), command, str(native / 'signal'), str(input_path.resolve())], 'signal-' + command, parse=True)
    elif module == 'spectral':
        result = rational_run(native / 'spectral', execute)
    else:
        archive = native / 'RAX_M1_Methodenpruefung_v0_1_Paket.zip'
        shutil.copyfile(ROOT / RAX_ARCHIVE, archive)
        result = rax_run(archive, native / 'results', execute, extract, digest)
    return scientific_summary(module, result)


def same_rax(expected, actual):
    """Compare fixed findings; only declared runtime metadata may vary."""
    from tools.workflow.cli import equivalent
    equivalent(expected['checks'], actual['checks'], ignore={'created_utc', 'wall_seconds', 'unit_log'})
    for key in ['status', 'original_files_unchanged', 'original_primary_decisions_changed', 'audit_script_sha256', 'guard_script_sha256']:
        equivalent(expected[key], actual[key])


def verify(module, native, execute, extract, digest):
    if module == 'signal':
        result = execute(['node', str(ROOT / 'tools/workflow/signal_adapter.cjs'), 'verify', str(native / 'signal')], 'signal-replay', parse=True)
    elif module == 'spectral':
        if (native / 'spectral/independent_audit.py').read_bytes() != (ROOT / 'tests/python/independent_audit.py').read_bytes():
            raise ValueError('Spectral reference source mismatch')
        with tempfile.TemporaryDirectory(prefix='x6-spectral-') as temp:
            result = rational_run(Path(temp) / 'reference', execute)
        if result != json.loads((native / 'spectral/python_results.local.json').read_text()):
            raise ValueError('Spectral result mismatch')
    else:
        with tempfile.TemporaryDirectory(prefix='x6-rax-verify-') as temp:
            fresh = Path(temp) / 'results'
            result = rax_run(native / 'RAX_M1_Methodenpruefung_v0_1_Paket.zip', fresh, execute, extract, digest)
            from tools.workflow.cli import equivalent
            names = {p.name for p in fresh.iterdir()}
            if names != {p.name for p in (native / 'results').iterdir()}:
                raise ValueError('RAX result inventory differs')
            for name in names:
                ignored = {'created_utc', 'wall_seconds', 'unit_log', 'test_log', 'started_utc', 'finished_utc'}
                if name == 'REPRODUCTION.json':
                    ignored.add('runtime')  # Recorded environment is not authenticated.
                equivalent(json.loads((native / 'results' / name).read_text()), json.loads((fresh / name).read_text()), ignore=ignored)
            same_rax(json.loads((native / 'results/METHOD_REVIEW.json').read_text()), result)
    return scientific_summary(module, result)
