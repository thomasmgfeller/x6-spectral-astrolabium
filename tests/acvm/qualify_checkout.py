#!/usr/bin/env python3
"""Run the ACVM workflow from a clean checkout without an existing environment.
SPDX-License-Identifier: Apache-2.0
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(ROOT) or (ROOT/'.venv').exists():
        raise ValueError('External new output directory and absent .venv required')
    git = lambda *cmd: subprocess.check_output(['git', *cmd], cwd=ROOT, text=True).strip()
    if git('status', '--porcelain'):
        raise ValueError('Clean committed checkout required')
    output.mkdir(parents=True, exist_ok=False)
    files = git('ls-files', '-z').strip('\0').split('\0')
    hashes = lambda: {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in files}
    before = hashes()
    report = {'schema': 'acvm.fresh-checkout/1', 'status': 'FAILED', 'source_commit': git('rev-parse', 'HEAD'),
              'started_utc': datetime.now(timezone.utc).isoformat(), 'steps': [],
              'initial_checkout_clean': True, 'initial_environment_absent': True,
              'hardware_accessed': False, 'physical_qualification': 'NOT_PERFORMED'}
    def run(name, args, expected=0):
        start = time.monotonic()
        interpreter = ROOT/'.venv/bin/python'
        executable = str(interpreter) if interpreter.exists() else sys.executable
        result = subprocess.run([executable, *map(str, args)], cwd=ROOT,
                                capture_output=True, text=True, timeout=90)
        (output/(name+'.log')).write_text(result.stdout+result.stderr)
        passed = result.returncode == expected
        report['steps'].append({'name': name, 'command': [executable, *map(str, args)],
                                'exit_code': result.returncode, 'expected_exit_code': expected,
                                'passed': passed, 'seconds': time.monotonic()-start})
        print(json.dumps({'step': name, 'passed': passed}), flush=True)
        if not passed:
            raise RuntimeError(name+' failed')
    try:
        run('01-isolated-environment', ['x6.py', 'setup', '--profile', 'core'])
        if 'include-system-site-packages = false' not in (ROOT/'.venv/pyvenv.cfg').read_text().lower():
            raise ValueError('Venv inherits global packages')
        run('02-qualification', ['x6.py', 'acvm', 'qualify', '--output', output/'qualification'])
        d01 = output/'qualification/D01'
        run('03-verify', ['x6.py', 'acvm', 'verify', d01])
        run('04-export', ['x6.py', 'acvm', 'export', d01, '--output', output/'D01.zip'])
        run('05-import-verify', ['x6.py', 'acvm', 'verify', output/'D01.zip'])
        for number, command, example in ((6, 'assess-electrical', 'electrical-simulated.json'),
                                          (7, 'assess-optical', 'optical-measurements-simulated.json'),
                                          (8, 'fit-hwp', 'hwp-scan-simulated.json'),
                                          (9, 'feedforward-budget', 'feedforward-assumptions.json')):
            run(f'{number:02d}-{command}', ['x6.py', 'acvm', command, 'experimental/acvm/examples/'+example,
                                           '--output', output/(command+'.json')])
        run('10-template-refused', ['x6.py', 'acvm', 'move', '--profile', 'experimental/acvm/examples/loop-profile-template.json',
             '--port', '/THIS_PORT_MUST_NOT_BE_OPENED', '--degrees', '22.5', '--output', output/'must-not-exist'], expected=1)
        if (output/'must-not-exist').exists():
            raise ValueError('Template rejection happened too late')
        run('11-integration-regressions', ['-m', 'unittest', 'discover', '-s', 'tests/integration', '-v'])
        run('12-source-inventory', ['tests/python/verify_manifest.py'])
        if git('status', '--porcelain') or before != hashes():
            raise ValueError('Source files changed during qualification')
        report['all_tracked_files_unchanged'] = True
        report['status'] = 'PASS_SOFTWARE_WORKFLOW_PHYSICAL_OPEN'
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (output/'fresh-checkout.json').write_text(json.dumps(report, indent=2)+'\n')
    print(report['status'])
    return 0 if report['status'].startswith('PASS') else 1


if __name__ == '__main__':
    raise SystemExit(main())
