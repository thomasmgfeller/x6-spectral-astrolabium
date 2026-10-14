"""Independent image reader and full-byte artifact verification. Not authenticity.
Does not import the compiler, its structs, or its parsing helpers.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import json
import math
from pathlib import Path
import struct
import tempfile
import zipfile


def read_image(data):
    if len(data) < 24 or data[:8] != b'ACVMD01\0':
        raise ValueError('D01 header')
    n = int.from_bytes(data[8:12], 'little')
    tick_ns = int.from_bytes(data[12:16], 'little')
    duration = int.from_bytes(data[16:24], 'little')
    if not 1 <= n <= 4096 or len(data) != 24+24*n or not 1 <= tick_ns <= 10**9:
        raise ValueError('D01 length/count/timebase')
    if not 1 <= duration < 2**53 or duration*tick_ns >= 2**64:
        raise ValueError('D01 time overflow')
    rows = []
    for p in range(24, len(data), 24):
        tick = int.from_bytes(data[p:p+8], 'little')
        i, q = struct.unpack('<dd', data[p+8:p+24])
        if (not math.isfinite(i) or not math.isfinite(q) or abs(i) > 1 or abs(q) > 1
                or tick >= duration or (rows and tick <= rows[-1][0]) or (not rows and tick != 0)):
            raise ValueError('D01 sample values/order')
        rows.append((tick, i, q))
    return {'tick_ns': tick_ns, 'duration_ticks': duration, 'rows': rows}


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False)+'\n')


def seal(directory):
    directory = Path(directory)
    files = {p.relative_to(directory).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(directory.rglob('*')) if p.is_file() and p.name != 'manifest.json'}
    write_json(directory/'manifest.json', {'schema': 'acvm.archive/2', 'files': files})


def verify(directory):
    directory = Path(directory)
    manifest = json.loads((directory/'manifest.json').read_text())
    if manifest.get('schema') != 'acvm.archive/2' or not isinstance(manifest.get('files'), dict):
        raise ValueError('Manifest schema')
    actual = {p.relative_to(directory).as_posix() for p in directory.rglob('*') if p.is_file()}
    if actual != set(manifest['files']) | {'manifest.json'}:
        raise ValueError('Missing or unlisted file')
    for name, digest in manifest['files'].items():
        p = directory/name
        if (Path(name).is_absolute() or '..' in Path(name).parts or p.is_symlink()
                or not p.resolve().is_relative_to(directory.resolve())):
            raise ValueError('Unsafe archive path')
        if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
            raise ValueError('Full file hash mismatch: '+name)
    decoded = read_image((directory/'samples.bin').read_bytes())
    plan = json.loads((directory/'plan.json').read_text())
    if set(plan) != {'schema', 'run_id', 'unit', 'tick_ns', 'duration_ticks', 'samples'}:
        raise ValueError('Plan fields')
    if type(plan['tick_ns']) is not int or type(plan['duration_ticks']) is not int:
        raise ValueError('Plan time types')
    for row in plan['samples']:
        if (set(row) != {'tick', 'i', 'q'} or type(row['tick']) is not int
                or type(row['i']) not in (int, float) or type(row['q']) not in (int, float)):
            raise ValueError('Plan sample types')
    expected = [(r['tick'], r['i'], r['q']) for r in plan['samples']]
    if (plan['schema'] != 'acvm.d01.plan/1' or plan['unit'] != 'normalized_IQ'
            or decoded['rows'] != expected or decoded['tick_ns'] != plan['tick_ns']
            or decoded['duration_ticks'] != plan['duration_ticks']):
        raise ValueError('Plan/image disagreement')
    execution = json.loads((directory/'execution.json').read_text())
    if (execution['evidence_kind'] != 'SIMULATED' or execution['run_id'] != plan['run_id']
            or execution['events'] != [list(row) for row in decoded['rows']]
            or execution['final_state'] != 'DONE' or execution['runs'] != 1):
        raise ValueError('Execution/model provenance disagreement')
    return {'status': 'VERIFIED_SIMULATION', 'files': len(manifest['files']),
            'samples': len(decoded['rows']), 'authenticity': 'NOT_ASSESSED'}


def export(directory, target):
    result = verify(directory)
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(Path(directory).rglob('*')):
            if p.is_file():
                z.write(p, p.relative_to(directory).as_posix())
    return {**result, 'archive_sha256': hashlib.sha256(Path(target).read_bytes()).hexdigest()}


def verify_zip(path):
    with zipfile.ZipFile(path) as z, tempfile.TemporaryDirectory(prefix='acvm-import-') as tmp:
        entries = z.infolist()
        if len(entries) > 100 or sum(p.file_size for p in entries) > 10*1024*1024:
            raise ValueError('Archive resource limit')
        names = set()
        for p in entries:
            name = p.filename
            if (name in names or Path(name).is_absolute() or '..' in Path(name).parts
                    or '\\' in name or ':' in name or p.is_dir()
                    or (p.external_attr >> 16) & 0o170000 == 0o120000):
                raise ValueError('Unsafe or duplicate ZIP entry')
            names.add(name)
            target = Path(tmp)/name; target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(p))
        return verify(tmp)
