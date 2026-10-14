#!/usr/bin/env python3
"""Execute the documented workflow in an initially clean checkout without a venv."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import select
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--wheelhouse', type=Path)
    p.add_argument('--with-browser', action='store_true')
    args = p.parse_args()
    output = args.output.resolve()
    if output.is_relative_to(ROOT):
        raise ValueError('Qualification output must be outside the checkout')
    if (ROOT / '.venv').exists():
        raise ValueError('A fresh checkout without .venv is required')
    def git(*cmd):
        return subprocess.check_output(['git', *cmd], cwd=ROOT, text=True).strip()
    if git('status', '--porcelain'):
        raise ValueError('Checkout must be clean before qualification')
    output.mkdir(parents=True, exist_ok=False)
    report = {'schema': 'x6.integration.qualification/1', 'status': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(), 'source_commit': git('rev-parse', 'HEAD'), 'initial_checkout_clean': True, 'initial_environment_absent': True, 'steps': [], 'browser': 'NOT_EXECUTED', 'physical_validation': 'NOT_PERFORMED', 'research_agents_executed': False}
    tracked = git('ls-files', '-z').strip('\0').split('\0')
    before = {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in tracked}
    def run(name, command, expect=0, timeout=300):
        started = time.monotonic()
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
        entry = {'name': name, 'command': list(map(str, command)), 'exit_code': result.returncode, 'expected_exit_code': expect, 'seconds': time.monotonic() - started, 'passed': result.returncode == expect}
        (output / (name + '.log')).write_text(result.stdout + '\n--- stderr ---\n' + result.stderr)
        report['steps'].append(entry)
        print(json.dumps({'step': name, 'passed': entry['passed']}), flush=True)
        if not entry['passed']:
            raise RuntimeError(name + ' failed; see ' + str(output / (name + '.log')))
        return result.stdout
    try:
        command = [sys.executable, 'x6.py', 'setup', '--profile', 'research']
        if args.wheelhouse:
            command += ['--wheelhouse', str(args.wheelhouse.resolve())]
        run('01-setup', command)
        env = json.loads(run('02-doctor', [sys.executable, 'x6.py', 'doctor', '--profile', 'research']))
        report['environment'] = env['environment']
        cfg = (ROOT / '.venv/pyvenv.cfg').read_text()
        if 'include-system-site-packages = false' not in cfg.lower():
            raise ValueError('Environment inherits global packages')
        report['isolated_environment_config'] = cfg
        run('03-pip-check', [str(ROOT / '.venv/bin/python'), '-m', 'pip', 'check'])
        run('04-regressions', [str(ROOT / '.venv/bin/python'), '-m', 'unittest', 'discover', '-s', 'tests/integration', '-p', 'test_*.py', '-v'])
        for module in ['signal', 'spectral', 'rax']:
            target = output / 'runs' / module
            archive = output / 'exports' / (module + '.zip')
            run(module + '-run', [sys.executable, 'x6.py', 'run', module, '--output', str(target)])
            run(module + '-verify', [sys.executable, 'x6.py', 'verify', str(target)])
            run(module + '-export', [sys.executable, 'x6.py', 'export', str(target), '--output', str(archive)])
            run(module + '-zip-replay', [sys.executable, 'x6.py', 'verify', str(archive)])
        run('no-overwrite', [sys.executable, 'x6.py', 'run', 'signal', '--output', str(output / 'runs/signal')], expect=1)
        run('invalid-job', [sys.executable, 'x6.py', 'run', 'signal', '--job', 'experimental/edge_reference/examples/invalid-job.json', '--output', str(output / 'invalid')], expect=1)
        if (output / 'invalid/run.json').exists():
            raise ValueError('Failed run published a completion record')
        server_log = (output / 'server.log').open('w')
        server = subprocess.Popen([sys.executable, 'x6.py', 'serve', '--port', '0'], cwd=ROOT, stdout=subprocess.PIPE, stderr=server_log, text=True)
        try:
            if not select.select([server.stdout], [], [], 15)[0]:
                raise TimeoutError('Local server did not report readiness')
            url = json.loads(server.stdout.readline())['url']
            if args.with_browser:
                run('browser-workflow', ['node', 'tests/integration/browser_workflow.cjs', url, str(output / 'runs/signal/native/signal/evidence.json'), str(output / 'browser')])
                report['browser'] = json.loads((output / 'browser/browser-report.json').read_text())
                run('browser-native-import', [sys.executable, 'x6.py', 'import-signal', str(output / 'browser/browser-evidence.json'), '--output', str(output / 'runs/browser-import')])
                run('browser-import-export', [sys.executable, 'x6.py', 'export', str(output / 'runs/browser-import'), '--output', str(output / 'exports/browser-import.zip')])
                run('browser-import-replay', [sys.executable, 'x6.py', 'verify', str(output / 'exports/browser-import.zip')])
        finally:
            server.terminate()
            server.wait(timeout=10)
            server_log.close()
        report['final_checkout_clean'] = git('status', '--porcelain') == ''
        report['all_tracked_files_unchanged'] = before == {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in tracked}
        if not report['final_checkout_clean'] or not report['all_tracked_files_unchanged']:
            raise ValueError('Qualification changed source checkout')
        run('source-inventory', [sys.executable, 'tests/python/verify_manifest.py'])
        report['status'] = 'PASS_WITH_BROWSER' if args.with_browser else 'PASS_CORE_WORKFLOW'
    except Exception as exc:
        report['status'] = 'FAIL'
        report['error'] = str(exc)
    report['finished_utc'] = datetime.now(timezone.utc).isoformat()
    (output / 'qualification.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'report': str(output / 'qualification.json')}, indent=2))
    return 1 if report['status'] == 'FAIL' else 0


if __name__ == '__main__':
    raise SystemExit(main())
