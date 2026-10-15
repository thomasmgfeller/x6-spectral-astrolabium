"""Offline reference runner. Only code from the trusted checkout is executed."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'REFERENCE_SOURCE_MANIFEST.json'
CASES = ('rational-graphs', 'causal-n6', 'rax-w1', 'wolfram-polarity',
         'current-polarity', 'wolfram-dependence', 'wolfram-causal3', 'lorentz-residuals', 'qe-graphs', 'failure-controls')
FILES = tuple('reports/' + case + '.json' for case in CASES)
LIMIT = 16 * 1024 * 1024
SCOPE = 'FINITE_REFERENCE_CHECKS; NO_NEW_WOLFRAM_CALLS; NO_PHYSICAL_VALIDATION; NO_EXTERNAL_REVIEW'


class Rejected(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise Rejected(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False,
                       allow_nan=False) + '\n').encode('utf-8')


def decode(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def invalid(value):
        raise Rejected('Nonfinite JSON: ' + value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=invalid)


def read(path):
    path = Path(path)
    info = path.lstat()
    require(stat.S_ISREG(info.st_mode) and info.st_size <= LIMIT,
            'Expected bounded regular file: ' + str(path))
    data = path.read_bytes()
    require(len(data) <= LIMIT, 'File grew beyond limit')
    return data


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    p = PurePosixPath(name)
    require(bool(name) and not p.is_absolute() and '..' not in p.parts
            and ':' not in name and '\\' not in name and str(p) == name,
            'Unsafe path: ' + name)
    return p


def sources():
    raw = read(ROOT / MANIFEST)
    doc = decode(raw)
    require(doc['schema'] == 'x6.reference.sources/1', 'Source manifest schema')
    required = {'x6.py', 'tools/workflow/cli.py', 'tools/workflow/backends.py',
                'tools/reference_suite.py', 'tools/reference_cases.py',
                'tools/reference_current.cjs', 'tests/python/independent_audit.py',
                'app/signal-lab-core.js', 'references/causal-order-n6/verify.py',
                'references/causal-order-n6/atlas_n6.json'}
    required.update('research/lorentz_n6_residuals/' + name for name in (
        'core.py', 'verify.py', 'inputs.json', 'contract.json',
        'freeze.json', 'freeze-compact.json', 'freeze-monic.json',
        'wolfram_check.wl', 'wolfram_check_compact.wl', 'wolfram_check_monic.wl',
        'evidence/wolfram-response-attempt1.json', 'evidence/wolfram-response-attempt2.json',
        'evidence/wolfram-response-attempt3.json', 'evidence/wolfram-result-attempt2.json',
        'evidence/wolfram-result.json', 'evidence/local-results.json'))
    from tools.reference_cases import ARCHIVES
    required.update('research/x6_qe/' + name for name in (
        'core.py', 'independent.py', 'verify.py', 'inputs.json', 'contract.json'))
    required.update(value[0] for value in ARCHIVES.values())
    require(required <= set(doc['files']), 'Incomplete source manifest')
    for name, expected in doc['files'].items():
        p = ROOT / safe_name(name)
        require(not any(a.is_symlink() for a in (p, *p.parents)), 'Linked source: ' + name)
        require(sha(read(p)) == expected, 'Source hash mismatch: ' + name)
    return dict(doc['files'], **{MANIFEST: sha(raw)})


def environment():
    # Do not inherit PYTHONOPTIMIZE, PYTHONPATH, NODE_OPTIONS or NODE_PATH.
    return {'PATH': os.environ.get('PATH', ''), 'LANG': 'C.UTF-8', 'LC_ALL': 'C.UTF-8',
            'PYTHONDONTWRITEBYTECODE': '1'}


def execute(args, cwd):
    proc = subprocess.run([str(a) for a in args], cwd=cwd, env=environment(),
                          capture_output=True, timeout=90)
    require(proc.returncode == 0, 'Command failed: ' + str(args[0]) + '\n' +
            (proc.stdout + proc.stderr).decode(errors='replace')[-3000:])
    require(len(proc.stdout) <= LIMIT, 'Command output exceeds limit')
    return decode(proc.stdout)


def python(script, cwd, *args):
    return execute([sys.executable, '-E', '-s', '-B', script, *args], cwd)


def extract(name, target):
    # Called only after the source manifest has checked the immutable archive.
    with zipfile.ZipFile(ROOT / name) as archive:
        entries = archive.infolist()
        require(len(entries) <= 2000 and sum(e.file_size for e in entries) <= 64*1024*1024,
                'Archive size limit')
        seen = set()
        for entry in entries:
            rel = str(safe_name(entry.filename.rstrip('/')))
            require(rel not in seen, 'Duplicate archive member')
            seen.add(rel)
            require(not stat.S_ISLNK(entry.external_attr >> 16), 'Archive symlink')
            require(entry.file_size <= LIMIT, 'Archive member size limit')
            dest = target / rel
            if entry.is_dir():
                dest.mkdir(parents=True, exist_ok=True)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                with dest.open('xb') as stream:
                    stream.write(archive.read(entry))


def assemble(reports, source_files):
    require(set(reports) == set(CASES), 'Case coverage')
    payload = {'reports/' + name + '.json': encode(value) for name, value in reports.items()}
    payload['complete.json'] = encode({
        'schema': 'x6.offline-reference/1', 'status': 'PASS_OFFLINE_REFERENCE',
        'case_ids': list(CASES), 'scope': SCOPE, 'source_files': source_files,
        'files': {name: {'sha256': sha(data), 'bytes': len(data)}
                  for name, data in sorted(payload.items())}})
    return payload


def load_bundle(directory):
    directory = Path(directory)
    require(directory.is_dir() and not directory.is_symlink(), 'Bundle directory required')
    paths = sorted(directory.rglob('*'))
    require(len(paths) <= len(FILES) + 2, 'Unexpected bundle entries')
    payload = {}
    for path in paths:
        name = path.relative_to(directory).as_posix()
        require(not path.is_symlink(), 'Linked bundle entry: ' + name)
        if path.is_dir():
            require(name == 'reports', 'Unexpected directory: ' + name)
        else:
            payload[name] = read(path)
    return payload


def validate(payload, source_files, expected=None):
    require(set(payload) == {*FILES, 'complete.json'}, 'Incomplete or extra bundle files')
    # Canonical encoding also rejects silently ignored duplicates and nonfinite numbers.
    for name, data in payload.items():
        require(encode(decode(data)) == data, 'Noncanonical or invalid JSON: ' + name)
    manifest = decode(payload['complete.json'])
    wanted = {'schema': 'x6.offline-reference/1', 'status': 'PASS_OFFLINE_REFERENCE',
              'case_ids': list(CASES), 'scope': SCOPE, 'source_files': source_files,
              'files': {name: {'sha256': sha(payload[name]), 'bytes': len(payload[name])}
                        for name in FILES}}
    require(encode(manifest) == encode(wanted), 'Completion/source/inventory mismatch')
    if expected is not None:
        for name in [*FILES, 'complete.json']:
            require(payload[name] == expected[name], 'Replay differs: ' + name)


BUNDLE_CONTROLS = ('missing-completion', 'missing-case', 'extra-file', 'truncated-json',
                   'duplicate-json-key', 'nonfinite-json', 'changed-unhashed-result',
                   'rehash-wrong-graph-bound', 'rehash-missing-wolfram-row',
                   'rehash-false-causal-count', 'rehash-false-all-pass',
                   'wrong-source-binding', 'symlink-result', 'rehash-false-qe-motif')


def rejected(action, label):
    try:
        action()
    except (Rejected, ValueError, AssertionError, KeyError, json.JSONDecodeError):
        return {'case': label, 'rejected': True}
    raise Rejected('Negative control accepted: ' + label)


def bundle_controls(good, source_files, work):
    results = []
    for label in BUNDLE_CONTROLS:
        bad = dict(good)
        graph = 'reports/rational-graphs.json'
        rehash = False
        if label == 'missing-completion':
            del bad['complete.json']
        elif label == 'missing-case':
            del bad[graph]
        elif label == 'extra-file':
            bad['unlisted.json'] = b'{}\n'
        elif label == 'truncated-json':
            bad[graph] = bad[graph][:-10]
        elif label == 'duplicate-json-key':
            bad[graph] = b'{"passed":0,' + bad[graph].lstrip()[1:]
        elif label == 'nonfinite-json':
            bad[graph] = b'{"passed":NaN}\n'
        elif label == 'changed-unhashed-result':
            bad[graph] = encode({'passed': 5})
        elif label == 'rehash-wrong-graph-bound':
            doc = decode(bad[graph]); doc['results'][0]['valid_bound'] = '3/5'
            bad[graph] = encode(doc); rehash = True
        elif label == 'rehash-missing-wolfram-row':
            name = 'reports/rax-w1.json'; doc = decode(bad[name])
            doc['verification']['case_results'].pop()
            bad[name] = encode(doc); rehash = True
        elif label == 'rehash-false-causal-count':
            name = 'reports/causal-n6.json'; doc = decode(bad[name])
            doc['representatives_checked'] = 317
            bad[name] = encode(doc); rehash = True
        elif label == 'rehash-false-all-pass':
            bad[graph] = encode({'status': 'PASS', 'passed': 5, 'total': 5}); rehash = True
        elif label == 'rehash-false-qe-motif':
            name = 'reports/qe-graphs.json'; doc = decode(bad[name])
            doc['result']['graphs'][2]['k4_count'] = 0
            doc['result_sha256'] = sha(encode(doc['result']))
            bad[name] = encode(doc); rehash = True
        elif label == 'wrong-source-binding':
            doc = decode(bad['complete.json']); doc['source_files']['x6.py'] = '0'*64
            bad['complete.json'] = encode(doc)
        elif label == 'symlink-result':
            folder = work / 'linked-bundle'
            write_bundle(folder, good)
            path = folder / graph
            path.unlink(); path.symlink_to(ROOT / 'tests/python/independent_audit.py')
            results.append(rejected(lambda: load_bundle(folder), label))
            continue
        if rehash:
            manifest = decode(bad['complete.json'])
            manifest['files'] = {n: {'sha256': sha(bad[n]), 'bytes': len(bad[n])} for n in FILES}
            bad['complete.json'] = encode(manifest)
            # Prove the attacker fixed the envelope: only replay may reject this.
            validate(bad, source_files)
        results.append(rejected(lambda: validate(bad, source_files, good), label))
    return results


def evaluate():
    require(__debug__, 'Python optimization disables legacy assertions; use normal Python')
    require(sys.version_info[:2] == (3, 12), 'Reference runtime requires Python 3.12')
    require(shutil.which('node') is not None, 'Node.js 24 is required')
    version = subprocess.check_output(['node', '--version'], env=environment(), text=True).strip()
    require(version.startswith('v24.'), 'Reference runtime requires Node.js 24')
    before = sources()
    from tools.reference_cases import run_cases
    with tempfile.TemporaryDirectory(prefix='x6-reference-') as tmp:
        work = Path(tmp)
        reports, domain = run_cases(work)
        controls = [{'case': label, 'rejected': True} for label in BUNDLE_CONTROLS]
        reports['failure-controls'] = {'status': 'PASS', 'domain': domain, 'bundle': controls,
                                      'total_rejected': len(domain) + len(controls)}
        payload = assemble(reports, before)
        require(bundle_controls(payload, before, work) == controls, 'Bundle controls incomplete')
    require(sources() == before, 'Sources changed during execution')
    validate(payload, before)
    return payload


def write_bundle(directory, payload):
    directory = Path(directory).absolute()
    # Exclusive creation prevents accidental overwrites. Completion is written last.
    directory.mkdir(parents=True, exist_ok=False)
    for name in [*FILES, 'complete.json']:
        path = directory / name
        path.parent.mkdir(exist_ok=True)
        with path.open('xb') as stream:
            stream.write(payload[name]); stream.flush(); os.fsync(stream.fileno())
        require(read(path) == payload[name], 'Write readback mismatch')
    validate(load_bundle(directory), decode(payload['complete.json'])['source_files'], payload)


def verify(directory):
    observed = load_bundle(directory)
    validate(observed, sources())
    expected = evaluate()
    validate(observed, sources(), expected)
    return expected


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('run', 'qualify'):
        sub.add_parser(name).add_argument('--output', type=Path, required=True)
    sub.add_parser('verify').add_argument('directory', type=Path)
    args = parser.parse_args(argv)
    try:
        require(__debug__, 'Python optimization is not supported')
        if args.command == 'verify':
            payload = verify(args.directory)
        else:
            require(not args.output.exists() and not args.output.is_symlink(), 'Output must be new')
            payload = evaluate()
            write_bundle(args.output, payload)
            if args.command == 'qualify':
                verify(args.output)
        controls = decode(payload['reports/failure-controls.json'])
        print(json.dumps({'status': 'PASS_OFFLINE_REFERENCE_REPLAY' if args.command != 'run'
                          else 'PASS_OFFLINE_REFERENCE', 'cases': len(CASES),
                          'negative_controls': controls['total_rejected'],
                          'scope': SCOPE, 'python': sys.version.split()[0],
                          'node': subprocess.check_output(['node', '--version'], env=environment(), text=True).strip()},
                         indent=2))
        return 0
    except (OSError, ValueError, AssertionError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'FAIL', 'error': str(exc)}, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
