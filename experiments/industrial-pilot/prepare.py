"""Extract only the predeclared vibration records from official KAt RAR archives.

Requires libarchive-c and system libarchive. No network or archive path extraction.
All source archives must already be in --archives. Never overwrite a data bundle.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sys

import libarchive
import numpy as np
from scipy.io import loadmat

ROOT = Path(__file__).resolve().parent


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def extract(archives, output):
    if output.exists():
        raise ValueError('OUTPUT_EXISTS')
    raw = (ROOT/'contract.json').read_bytes()
    contract = json.loads(raw)
    output.mkdir(parents=True)
    records = []
    for bearing in contract['selection']['bearing_ids']:
        archive_path = archives/(bearing+'.rar')
        prefix = 'N15_M07_F10_'+bearing+'_'
        candidates = {}
        with libarchive.file_reader(str(archive_path)) as archive:
            for entry in archive:
                if entry.pathname.startswith(bearing+'/'+prefix) and entry.pathname.endswith('.mat'):
                    repeat = int(entry.pathname.rsplit('_',1)[1].removesuffix('.mat'))
                    if repeat in candidates or entry.size > 32*1024*1024:
                        raise ValueError('DUPLICATE_OR_OVERSIZED_MEMBER')
                    candidates[repeat] = b''.join(entry.get_blocks())
        if set(candidates) != set(contract['selection']['candidate_repeats']):
            raise ValueError('MISSING_OR_EXTRA_CANDIDATE_REPEAT: '+bearing)
        audit = []
        for repeat in contract['selection']['candidate_repeats']:
            name = prefix+str(repeat)
            payload = candidates[repeat]
            m = loadmat(io.BytesIO(payload), simplify_cells=True)
            if [k for k in m if not k.startswith('__')] != [name]:
                raise ValueError('MAT_RECORD_NAME_MISMATCH')
            v = m[name]
            channels = [y for y in v['Y'] if y.get('Name') == 'vibration_1']
            if len(channels) != 1:
                raise ValueError('VIBRATION_CHANNEL_AMBIGUOUS')
            channel = channels[0]
            original = np.asarray(channel['Data'])
            x = np.asarray(original, dtype='<f8')
            t = np.asarray(v['X'][int(channel['XIndex'])-1]['Data'], dtype=float)
            dt = np.diff(t)
            fs = contract['machine_and_sensor']['sampling_hz']
            grid_error = float(np.max(np.abs((t-t[0])*fs-np.arange(len(t)))))
            unit = channel.get('Unit')
            unit = str(unit) if isinstance(unit, str) else '' if np.size(unit) == 0 else str(unit)
            gates = dict(shape=x.ndim == 1 and len(x) in contract['selection']['native_samples_allowed'],
                finite_lossless=bool(np.isfinite(x).all() and np.array_equal(x, original)),
                timebase=bool(t.shape == x.shape and np.isfinite(t).all() and np.all(dt > 0)
                    and grid_error <= contract['selection']['max_timestamp_grid_error_samples']),
                native_unit_unchanged=unit == '')
            audit.append(dict(repeat=repeat, member_sha256=hashlib.sha256(payload).hexdigest(),
                native_samples=int(x.size), max_grid_error_samples=grid_error, gates=gates,
                accepted=all(gates.values())))
            if all(gates.values()):
                break
        else:
            (output/(bearing+'-failed-selection.json')).write_text(json.dumps(audit,indent=2)+'\n')
            raise ValueError('NO_ELIGIBLE_REPEAT: '+bearing)
        signal = np.ascontiguousarray(x[:contract['selection']['samples']], dtype='<f8')
        path = output/(bearing+'.npz')
        np.savez_compressed(path, vibration=signal)
        split = next(k for k, values in contract['splits'].items() if bearing in values)
        records.append(dict(bearing_id=bearing, record_id=name, selected_repeat=repeat, selection_audit=audit, split=split,
            label='healthy' if bearing in contract['ground_truth']['healthy'] else 'damaged',
            archive_url=contract['source']['download_base']+bearing+'.rar',
            archive_bytes=archive_path.stat().st_size, archive_sha256=sha(archive_path),
            member=bearing+'/'+name+'.mat', member_bytes=len(payload),
            member_sha256=hashlib.sha256(payload).hexdigest(),
            path=bearing+'.npz', bytes=path.stat().st_size, sha256=sha(path),
            samples=signal.size, dtype='<f8', native_unit=unit,
            signal_sha256=hashlib.sha256(signal.tobytes()).hexdigest(),
            timebase=dict(first=float(t[0]), last=float(t[-1]),
                median_dt=float(np.median(dt)), max_deviation_ppm=float(np.max(np.abs(dt*fs-1))*1e6),
                max_grid_error_samples=grid_error)))
        print('EXTRACTED', bearing, path.stat().st_size, flush=True)
    manifest = dict(schema='x6.industrial.pilot-inputs/1',
        contract_sha256=hashlib.sha256(raw).hexdigest(),
        importer_sha256=sha(Path(__file__)),
        created_utc=datetime.now(timezone.utc).isoformat(),
        evidence_class=contract['evidence_class'], license=contract['source']['license'],
        transformation='First metadata-qualified repeat per bearing, named vibration_1, first 256000 samples unchanged as float64; omitted extra endpoint if present and other channels; no filtering or resampling.',
        records=records)
    (output/'manifest.json').write_text(json.dumps(manifest, indent=2, allow_nan=False)+'\n')
    return manifest


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--archives', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    try:
        extract(a.archives, a.output)
    except Exception as exc:
        print('INVALID:', str(exc), file=sys.stderr)
        raise SystemExit(2)
