"""Unified local workflow and lossless export envelope. Apache-2.0."""
import argparse
from datetime import datetime, timezone
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import importlib.metadata
import json
import math
import os
from pathlib import Path, PurePosixPath
import platform
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.parse
import venv
import zipfile

from tools.workflow import backends

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = 'x6.integration.run/1'
MAX_FILE = 64 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_FILES = 2000
PINS = {'numpy': '2.3.5', 'scipy': '1.17.0'}
LIMITS = {'authenticity': 'NOT_ASSESSED', 'physical_validation': 'NOT_PERFORMED', 'external_review': 'NOT_PERFORMED', 'hardware_control': 'NOT_PERFORMED'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def encoded(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def read_json(path):
    def invalid(value):
        raise ValueError('Nonfinite JSON value: ' + value)
    return json.loads(read_file(path), parse_constant=invalid)


def read_file(path):
    path = Path(path)
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_FILE:
        raise ValueError('Expected bounded regular file: ' + str(path))
    data = path.read_bytes()
    if len(data) > MAX_FILE:
        raise ValueError('File grew beyond size limit')
    return data


def write_new(path, value):
    data = encoded(value)
    with Path(path).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if Path(path).read_bytes() != data:
        raise OSError('Write readback mismatch')


def relative_name(name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Invalid relative filename')
    posix = PurePosixPath(name)
    if posix.is_absolute() or '..' in posix.parts or ':' in name or posix.as_posix() != name:
        raise ValueError('Unsafe or noncanonical relative filename: ' + name)
    return posix


def inventory(root, omit=()):
    files = {}
    total = 0
    for path in sorted(root.rglob('*')):
        if path.is_symlink():
            raise ValueError('Linked file/directory is not a run payload')
        if not path.is_file():
            continue
        name = path.relative_to(root).as_posix()
        if name in omit:
            continue
        relative_name(name)
        data = read_file(path)
        total += len(data)
        if total > MAX_TOTAL or len(files) >= MAX_FILES:
            raise ValueError('Run inventory exceeds limits')
        files[name] = {'bytes': len(data), 'sha256': digest(data)}
    return files


def extract(archive, target):
    """No absolute paths, traversal, duplicate names, links, or oversized members."""
    target.mkdir(parents=True, exist_ok=False)
    total = 0
    with zipfile.ZipFile(archive) as z:
        infos = z.infolist()
        if len(infos) > MAX_FILES or len({i.filename for i in infos}) != len(infos):
            raise ValueError('ZIP inventory invalid')
        for info in infos:
            name = info.filename.rstrip('/') if info.is_dir() else info.filename
            posix = relative_name(name)
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode) or (stat.S_IFMT(mode) not in (0, stat.S_IFREG, stat.S_IFDIR)):
                raise ValueError('Special ZIP entry rejected')
            total += info.file_size
            if info.file_size > MAX_FILE or total > MAX_TOTAL:
                raise ValueError('ZIP exceeds uncompressed size limits')
            path = target.joinpath(*posix.parts)
            if info.is_dir():
                path.mkdir(parents=True, exist_ok=True)
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            data = z.read(info)
            if len(data) != info.file_size:
                raise ValueError('ZIP byte-count mismatch')
            with path.open('xb') as stream:
                stream.write(data)


def equivalent(expected, actual, ignore=frozenset(), trail='result'):
    if isinstance(expected, dict):
        if not isinstance(actual, dict) or set(expected) != set(actual):
            raise ValueError(trail + ': fields differ')
        for key in expected:
            if key not in ignore:
                equivalent(expected[key], actual[key], ignore, trail + '.' + key)
    elif isinstance(expected, list):
        if not isinstance(actual, list) or len(expected) != len(actual):
            raise ValueError(trail + ': array length differs')
        for i, (a, b) in enumerate(zip(expected, actual)):
            equivalent(a, b, ignore, f'{trail}[{i}]')
    elif isinstance(expected, float):
        if type(actual) not in (int, float) or not math.isfinite(actual) or not math.isclose(expected, actual, rel_tol=1e-12, abs_tol=1e-15):
            raise ValueError(trail + ': numerical value differs')
    elif type(expected) is not type(actual) or expected != actual:
        raise ValueError(trail + ': value differs')


def sources(module):
    return {name: digest(read_file(ROOT / name)) for name in backends.source_paths(module)}


def command_runner(logs=None, timeout=240):
    count = 0
    def execute(command, label, parse=False):
        nonlocal count
        count += 1
        env = dict(os.environ, PYTHONNOUSERSITE='1', PYTHONDONTWRITEBYTECODE='1')
        env.pop('PYTHONPATH', None)
        env.pop('PYTHONHOME', None)
        try:
            p = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired as exc:
            if logs:
                write_new(logs / f'{count:02d}-{label}.json', {'status': 'TIMEOUT', 'timeout_seconds': timeout})
            raise RuntimeError(f'{label}: timed out after {timeout} seconds') from exc
        if logs:
            write_new(logs / f'{count:02d}-{label}.json', {'exit_code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
        if p.returncode:
            raise RuntimeError(f'{label}: exit {p.returncode}: {p.stderr[-1500:]}')
        return json.loads(p.stdout) if parse else p.stdout
    return execute


def environment():
    packages = {}
    for name in PINS:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    node = shutil.which('node')
    node_version = subprocess.check_output([node, '--version'], text=True).strip() if node else None
    return {'python': platform.python_version(), 'platform': platform.platform(), 'machine': platform.machine(), 'node': node_version, 'git': shutil.which('git') is not None, 'packages': packages, 'isolated_environment': Path(sys.prefix).resolve() == (ROOT / '.venv').resolve()}


def doctor(profile):
    env = environment()
    failures = []
    if sys.version_info[:2] != (3, 12):
        failures.append('Use Python 3.12; other minor versions have not been qualified')
    if not env['node'] or int(env['node'].lstrip('v').split('.')[0]) < 22:
        failures.append('Install Node.js 22 or newer for the signal adapter')
    if not env['git']:
        failures.append('Install Git')
    if not env['isolated_environment']:
        failures.append('Run python3 x6.py setup --profile ' + profile)
    if profile == 'research':
        if os.name != 'posix':
            failures.append('The RAX research adapter requires a POSIX environment')
        for name, version in PINS.items():
            if env['packages'][name] != version:
                failures.append(f'{name}=={version} is required')
    return {'status': 'READY' if not failures else 'NOT_READY', 'profile': profile, 'environment': env, 'required_actions': failures, 'scope': 'Local software prerequisites; no hardware or scientific qualification.'}


def setup(profile, wheelhouse):
    if sys.version_info[:2] != (3, 12):
        raise ValueError('Setup requires Python 3.12 for this qualified workflow')
    folder = ROOT / '.venv'
    if folder.exists() and (folder.is_symlink() or not (folder / 'pyvenv.cfg').is_file()):
        raise ValueError('Existing .venv is not a regular environment; no replacement performed')
    if not folder.exists():
        venv.EnvBuilder(with_pip=True, system_site_packages=False).create(folder)
    py = folder / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if profile == 'research':
        command = [str(py), '-m', 'pip', 'install', '--disable-pip-version-check', '--only-binary=:all:', '-r', str(ROOT / 'tools/workflow/requirements-research.txt')]
        if wheelhouse:
            command.extend(['--no-index', '--find-links', str(wheelhouse.resolve())])
        subprocess.run(command, cwd=ROOT, check=True, stdout=sys.stderr)
        subprocess.run([str(py), '-m', 'pip', 'check'], cwd=ROOT, check=True, stdout=sys.stderr)
    result = subprocess.run([str(py), str(ROOT / 'x6.py'), 'doctor', '--profile', profile], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError('Environment created, prerequisites incomplete: ' + result.stdout + result.stderr)
    return json.loads(result.stdout)


def run(module, output, job, timeout, imported=None):
    if job is not None and module != 'signal':
        raise ValueError('--job is supported only for signal')
    ready = doctor('research' if module == 'rax' else 'core')
    if ready['status'] != 'READY':
        raise ValueError('; '.join(ready['required_actions']))
    output = output.resolve()
    if output == ROOT or output in ROOT.parents:
        raise ValueError('Output cannot replace source checkout')
    output.mkdir(parents=True, exist_ok=False)
    started = now()
    original_sources = sources(module)
    try:
        (output / 'logs').mkdir()
        (output / 'native').mkdir()
        result = backends.run(module, output / 'native', job, command_runner(output / 'logs', timeout), extract, digest, imported)
        if sources(module) != original_sources:
            raise ValueError('Sources changed during execution')
        summary = {'schema': 'x6.integration.summary/1', 'module': module, 'execution_status': 'COMPLETED', 'verification_status': 'BACKEND_CHECKS_PASS', 'evidence_class': 'SYNTHETIC_SOFTWARE', 'scientific_result': result, 'limits': LIMITS}
        write_new(output / 'summary.json', summary)
        try:
            commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        except (OSError, subprocess.SubprocessError):
            commit = None
        record = {'schema': SCHEMA, 'module': module, 'operation': 'IMPORT_SIGNAL' if imported else 'RUN', 'execution_status': 'COMPLETED', 'started_utc': started, 'finished_utc': now(), 'source_commit': commit, 'sources': original_sources, 'environment': ready['environment'], 'files': inventory(output), 'limits': LIMITS}
        write_new(output / 'run.json', record)  # Completion record is last, never overwritten.
        check_integrity(output)
        return {'status': 'COMPLETED', 'directory': str(output), 'summary': summary}
    except Exception as exc:
        # A failed attempt remains inspectable but never has an accepted completion record.
        if (output / 'run.json').exists():
            (output / 'run.json').rename(output / 'rejected-run.json')
        write_new(output / 'failure.json', {'status': 'FAILED', 'module': module, 'started_utc': started, 'finished_utc': now(), 'error': str(exc)})
        raise


def check_integrity(directory):
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('Expected regular run directory')
    record = read_json(directory / 'run.json')
    required = {'schema', 'module', 'operation', 'execution_status', 'started_utc', 'finished_utc', 'source_commit', 'sources', 'environment', 'files', 'limits'}
    if set(record) != required or record['schema'] != SCHEMA or record['module'] not in backends.MODULES or record['execution_status'] != 'COMPLETED' or record['limits'] != LIMITS:
        raise ValueError('Unsupported/incomplete run record')
    if record['operation'] not in ('RUN', 'IMPORT_SIGNAL') or (record['operation'] == 'IMPORT_SIGNAL' and record['module'] != 'signal'):
        raise ValueError('Invalid recorded operation')
    if record['sources'] != sources(record['module']):
        raise ValueError('Source revision mismatch; retain the matching source checkout')
    if inventory(directory, omit={'run.json'}) != record['files']:
        raise ValueError('Run payload inventory/hash mismatch')
    summary = read_json(directory / 'summary.json')
    if set(summary) != {'schema', 'module', 'execution_status', 'verification_status', 'evidence_class', 'scientific_result', 'limits'} or summary['schema'] != 'x6.integration.summary/1' or summary['module'] != record['module'] or summary['execution_status'] != 'COMPLETED' or summary['verification_status'] != 'BACKEND_CHECKS_PASS' or summary['evidence_class'] != 'SYNTHETIC_SOFTWARE' or summary['limits'] != LIMITS:
        raise ValueError('Summary contract mismatch')
    return record, summary


def verify_directory(directory, timeout):
    record, summary = check_integrity(directory)
    before = record['sources']
    result = backends.verify(record['module'], directory / 'native', command_runner(timeout=timeout), extract, digest)
    equivalent(summary['scientific_result'], result)
    if sources(record['module']) != before:
        raise ValueError('Sources changed during replay')
    check_integrity(directory)
    return {'status': 'REPLAY_PASS', 'module': record['module'], 'scientific_result': result, 'limits': LIMITS, 'runtime_metadata': 'RECORDED_NOT_AUTHENTICATED'}


def verify(path, timeout):
    if path.is_dir():
        return verify_directory(path, timeout)
    with tempfile.TemporaryDirectory(prefix='x6-export-') as temp:
        directory = Path(temp) / 'payload'
        extract(path, directory)
        return verify_directory(directory, timeout)


def export(directory, output):
    record, summary = check_integrity(directory)
    output = output.resolve()
    if output.is_relative_to(directory.resolve()):
        raise ValueError('Export destination must be outside its run directory')
    if output.exists():
        raise FileExistsError('Export already exists; choose a new path')
    output.parent.mkdir(parents=True, exist_ok=True)
    expected = dict(record['files'])
    run_bytes = read_file(directory / 'run.json')
    expected['run.json'] = {'bytes': len(run_bytes), 'sha256': digest(run_bytes)}
    # A .partial path is never advertised as a completed export.
    fd, tmp_name = tempfile.mkstemp(prefix=output.name + '.', suffix='.partial', dir=output.parent)
    os.close(fd)
    temp = Path(tmp_name)
    try:
        with zipfile.ZipFile(temp, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for name, info in sorted(expected.items()):
                data = read_file(directory / name)
                if len(data) != info['bytes'] or digest(data) != info['sha256']:
                    raise ValueError('Payload changed during export: ' + name)
                z.writestr(name, data)
        with zipfile.ZipFile(temp) as z:
            if z.testzip() is not None:
                raise ValueError('ZIP CRC check failed')
        with temp.open('rb') as stream:
            os.fsync(stream.fileno())
        os.link(temp, output)  # Publish only a completed ZIP; exclusive, never replace.
        exported = read_file(output)
        return {'status': 'EXPORTED', 'archive': str(output), 'bytes': len(exported), 'sha256': digest(exported), 'files': len(expected), 'verification_performed': 'INVENTORY_AND_DIGESTS', 'next_step': 'python3 x6.py verify ' + str(output), 'limits': LIMITS}
    finally:
        temp.unlink(missing_ok=True)


class LocalHandler(SimpleHTTPRequestHandler):
    """Static loopback entry, without directory listing or arbitrary checkout access."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_head(self):
        path = urllib.parse.unquote(urllib.parse.urlsplit(self.path).path)
        if path in ('/', '/index.html'):
            self.path = '/tools/workflow/start.html'
            path = self.path
        parts = PurePosixPath(path).parts
        allowed = path.startswith(('/app/', '/docs/')) or path == '/tools/workflow/start.html'
        target = (ROOT / path.lstrip('/')).resolve()
        if not allowed or any(p.startswith('.') for p in parts if p != '/') or not target.is_relative_to(ROOT):
            self.send_error(404)
            return None
        if target.is_dir():
            if (target / 'index.html').is_file():
                self.path = path.rstrip('/') + '/index.html'
            else:
                self.send_error(404)
                return None
        return super().send_head()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        super().end_headers()


def serve(port):
    server = ThreadingHTTPServer(('127.0.0.1', port), LocalHandler)
    print(json.dumps({'status': 'SERVING', 'url': f'http://127.0.0.1:{server.server_port}/', 'stop': 'Ctrl+C'}), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return {'status': 'STOPPED'}


def main(argv=None):
    parser = argparse.ArgumentParser(description='X6 local workflow: setup, doctor, serve, run, import-signal, verify, export')
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ['setup', 'doctor']:
        p = commands.add_parser(name)
        p.add_argument('--profile', choices=['core', 'research'], default='core')
        if name == 'setup':
            p.add_argument('--wheelhouse', type=Path, help='Optional existing wheel directory for offline installation')
    p = commands.add_parser('serve')
    p.add_argument('--port', type=int, default=8000)
    p = commands.add_parser('run')
    p.add_argument('module', choices=backends.MODULES)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--job', type=Path)
    p.add_argument('--timeout', type=int, default=240)
    p = commands.add_parser('import-signal')
    p.add_argument('evidence', type=Path)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--timeout', type=int, default=240)
    p = commands.add_parser('verify')
    p.add_argument('path', type=Path)
    p.add_argument('--timeout', type=int, default=240)
    p = commands.add_parser('export')
    p.add_argument('directory', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if not __debug__:
            raise ValueError('Run without -O: historical scientific checks use assertions')
        if hasattr(args, 'timeout') and not 1 <= args.timeout <= 3600:
            raise ValueError('Timeout must be 1–3600 seconds per subprocess')
        if args.command == 'setup':
            result = setup(args.profile, args.wheelhouse)
        elif args.command == 'doctor':
            result = doctor(args.profile)
        elif args.command == 'serve':
            if not 0 <= args.port <= 65535:
                raise ValueError('Port outside 0–65535')
            result = serve(args.port)
        elif args.command == 'run':
            result = run(args.module, args.output, args.job, args.timeout)
        elif args.command == 'import-signal':
            result = run('signal', args.output, None, args.timeout, imported=args.evidence)
        elif args.command == 'verify':
            result = verify(args.path, args.timeout)
        else:
            result = export(args.directory, args.output)
        print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), flush=True)
        return 1 if result.get('status') == 'NOT_READY' else 0
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError, zipfile.BadZipFile, KeyError, TypeError, AssertionError) as exc:
        print(json.dumps({'status': 'ERROR', 'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
