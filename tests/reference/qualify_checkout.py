#!/usr/bin/env python3
"""Fresh-checkout acceptance through the public CLI, including rehashed attacks."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from tools.reference_suite import decode, encode, read, require, sha


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--require-network-isolation', action='store_true')
    args = parser.parse_args()
    out = args.output.absolute()
    require(not out.exists() and not out.is_relative_to(ROOT), 'Use a new output outside checkout')
    require(not (ROOT / '.venv').exists(), 'Acceptance requires a fresh checkout without .venv')
    dirty = subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT)
    require(not dirty.strip(), 'Acceptance requires a clean checkout')
    try:
        isolated = os.readlink('/proc/self/ns/net') != os.readlink('/proc/1/ns/net')
    except OSError:
        isolated = False
    require(not args.require_network_isolation or isolated, 'A separate network namespace is required')
    out.mkdir(parents=True)
    steps = []

    def command(label, arguments, expected=0, message=None, cwd=ROOT, env=None, optimized=False):
        cmd = [sys.executable, '-S', '-B'] + (['-O'] if optimized else []) + ['x6.py', 'reference', *map(str, arguments)]
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, env=env, timeout=180)
        log = proc.stdout + proc.stderr
        (out / (label + '.log')).write_bytes(log)
        require(proc.returncode == expected, label + ': unexpected exit code; see ' + str(out))
        require(message is None or message.encode() in log, label + ': expected rejection reason missing')
        steps.append({'step': label, 'exit_code': proc.returncode,
                      'expected_exit_code': expected, 'log_sha256': sha(log)})

    command('01-qualify', ['qualify', '--output', out / 'run'], message='PASS_OFFLINE_REFERENCE_REPLAY')
    command('02-no-overwrite', ['run', '--output', out / 'run'], 1, 'Output must be new')
    command('03-no-optimization', ['verify', out / 'run'], 1, 'optimization', optimized=True)
    with tempfile.TemporaryDirectory(prefix='x6-reference-attacks-') as temporary:
        temp = Path(temporary)
        for name in ('graph', 'wolfram', 'missing', 'duplicate', 'symlink'):
            bad = temp / name
            shutil.copytree(out / 'run', bad)
            report_path = bad / 'reports/rational-graphs.json'
            rehash = name in ('graph', 'wolfram', 'missing')
            if name == 'graph':
                report = decode(read(report_path)); report['results'][0]['valid_bound'] = '3/5'
                report_path.write_bytes(encode(report))
            elif name == 'wolfram':
                report_path = bad / 'reports/rax-w1.json'
                report = decode(read(report_path)); report['verification']['case_results'].pop()
                report_path.write_bytes(encode(report))
            elif name == 'missing':
                report_path.unlink()
            elif name == 'duplicate':
                report_path.write_bytes(b'{"passed":5,' + read(report_path).lstrip()[1:])
            else:
                report_path.unlink(); report_path.symlink_to(out / 'run/reports/rational-graphs.json')
            if rehash:
                manifest = decode(read(bad / 'complete.json'))
                manifest['files'] = {p.relative_to(bad).as_posix(): {'sha256': sha(read(p)), 'bytes': p.stat().st_size}
                                     for p in sorted((bad / 'reports').glob('*.json'))}
                (bad / 'complete.json').write_bytes(encode(manifest))
            reason = 'Replay differs' if name in ('graph', 'wolfram') else {
                'missing': 'Incomplete or extra bundle files', 'duplicate': 'Duplicate JSON key',
                'symlink': 'Linked bundle entry'}[name]
            command('04-reject-' + name, ['verify', bad], 1, reason)

        source = temp / 'source'; source.mkdir()
        manifest = decode(read(ROOT / 'REFERENCE_SOURCE_MANIFEST.json'))
        for name in [*manifest['files'], 'REFERENCE_SOURCE_MANIFEST.json']:
            dest = source / name; dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        for label, name in [('05-changed-current-core', 'app/signal-lab-core.js'),
                            ('06-corrupted-wolfram-archive', next(n for n in manifest['files'] if n.endswith('.zip')))]:
            original = read(source / name)
            (source / name).write_bytes(original + b'corrupt')
            target = temp / label
            command(label, ['run', '--output', target], 1, 'Source hash mismatch', cwd=source)
            require(not target.exists(), 'Failed run left an accepted output')
            (source / name).write_bytes(original)
        env = dict(os.environ, PATH='')
        target = temp / 'without-node'
        command('07-missing-runtime', ['run', '--output', target], 1, 'Node.js 24 is required', cwd=source, env=env)
        require(not target.exists(), 'Missing runtime left an accepted output')

    require(not subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT).strip(), 'Checkout changed')
    report = {'schema': 'x6.reference.checkout-acceptance/1', 'status': 'PASS',
              'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'fresh_checkout': True, 'python_site_packages_disabled': True,
              'network_namespace_isolated': isolated, 'steps': steps,
              'suite_negative_controls': 26, 'bundle_manifest_sha256': sha(read(out / 'run/complete.json')),
              'scope': 'CLI acceptance; namespace field records enforcement, not a mathematical claim.'}
    (out / 'acceptance.json').write_bytes(encode(report))
    print(encode(report).decode(), end='')


if __name__ == '__main__':
    main()
