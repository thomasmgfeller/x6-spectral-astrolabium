"""Offline, bearing-grouped feasibility pilot. No industrial performance PASS."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
import zipfile

import numpy as np
from scipy.signal import butter, hilbert, sosfiltfilt, windows

ROOT = Path(__file__).resolve().parent


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    def pairs(items):
        d = {}
        for k, v in items:
            require(k not in d, 'DUPLICATE_JSON_KEY')
            d[k] = v
        return d
    def invalid(_):
        raise ValueError('NONFINITE_JSON')
    p = Path(path)
    require(p.stat().st_size <= 4*1024*1024, 'JSON_SIZE_LIMIT')
    return json.loads(p.read_bytes(), object_pairs_hook=pairs, parse_constant=invalid)


def write_new(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x') as f:
        f.write(json.dumps(value, indent=2, sort_keys=True, allow_nan=False)+'\n')


def validate_manifest(contract, manifest):
    require(manifest['schema'] == 'x6.industrial.pilot-inputs/1', 'INPUT_SCHEMA')
    require(manifest['evidence_class'] == contract['evidence_class'], 'EVIDENCE_CLASS')
    require(manifest['license'] == 'CC-BY-NC-4.0', 'DATA_RIGHTS')
    records = manifest['records']
    ids = [r['bearing_id'] for r in records]
    expected = contract['selection']['bearing_ids']
    require(len(ids) == len(set(ids)) and set(ids) == set(expected), 'MISSING_EXTRA_OR_DUPLICATE_BEARING')
    require(len({r['signal_sha256'] for r in records}) == len(records), 'DUPLICATE_SIGNAL_CONTENT')
    grouped = [x for v in contract['splits'].values() for x in v]
    require(len(grouped) == len(set(grouped)) and set(grouped) == set(expected), 'GROUP_LEAKAGE')
    for r in records:
        b = r['bearing_id']
        require(r['split'] in contract['splits'] and b in contract['splits'][r['split']], 'GROUP_LEAKAGE')
        label = 'healthy' if b in contract['ground_truth']['healthy'] else 'damaged'
        require(r['label'] == label, 'LABEL_MISMATCH')
        audit = r['selection_audit']
        require(isinstance(audit, list) and 1 <= len(audit) <= 20, 'MISSING_SELECTION_ATTEMPT')
        require([a['repeat'] for a in audit] == list(range(1,r['selected_repeat']+1)), 'MISSING_SELECTION_ATTEMPT')
        require(audit[-1]['accepted'] is True and all(a['accepted'] is False for a in audit[:-1]), 'SELECTION_RULE_VIOLATION')
        require(all(a['accepted'] == all(a['gates'].values()) for a in audit), 'SELECTION_GATE_MISMATCH')
        require(audit[-1]['member_sha256'] == r['member_sha256'], 'SELECTED_MEMBER_HASH')
        require(r['record_id'] == 'N15_M07_F10_'+b+'_'+str(r['selected_repeat']), 'RECORD_SUBSTITUTION')
        require(r['path'] == b+'.npz', 'UNSAFE_OR_SUBSTITUTED_PATH')
        require(r['samples'] == 256000 and r['dtype'] == '<f8', 'SAMPLE_METADATA')
        require(r['native_unit'] == '', 'UNVERIFIED_UNIT_CONVERSION')


def context(data):
    contract, freeze, manifest = read(ROOT/'contract.json'), read(ROOT/'freeze.json'), read(data/'manifest.json')
    require(set(freeze['sources']) == {'contract.json','pilot.py','prepare.py','power.py',
            'download_sources.py','requirements.txt','requirements-import.txt'}, 'FREEZE_SOURCE_SET')
    for name, digest in freeze['sources'].items():
        require(sha(ROOT/name) == digest, 'FROZEN_SOURCE_CHANGED: '+name)
    require(sha(ROOT/'contract.json') == manifest['contract_sha256'], 'CONTRACT_BINDING')
    require(sha(data/'manifest.json') == freeze['manifest_sha256'], 'FROZEN_INPUT_MANIFEST_CHANGED')
    validate_manifest(contract, manifest)
    return contract, freeze, manifest


def load_signal(data, record):
    path = data/record['path']
    require(not path.is_symlink() and path.is_file(), 'MISSING_OR_SYMLINK_DATA')
    require(path.stat().st_size == record['bytes'] and sha(path) == record['sha256'], 'RAW_FILE_HASH_OR_LENGTH')
    with zipfile.ZipFile(path) as z:
        require(z.namelist() == ['vibration.npy'], 'ARRAY_ARCHIVE_MEMBERS')
        require(z.infolist()[0].file_size <= 256000*8+1024, 'ARRAY_SIZE_LIMIT')
    with np.load(path, allow_pickle=False) as z:
        x = z['vibration']
    require(x.shape == (256000,) and x.dtype.str == '<f8' and np.isfinite(x).all(), 'ARRAY_SHAPE_DTYPE_FINITE')
    require(hashlib.sha256(x.tobytes()).hexdigest() == record['signal_sha256'], 'SIGNAL_HASH')
    require(float(np.var(x)) > 0, 'CONSTANT_SIGNAL')
    return x


def scores(x, contract):
    a, b = contract['methods']['crop_for_all_methods']
    z = x[a:b] - np.mean(x[a:b])
    variance = np.mean(z*z)
    envelope_cfg = contract['methods']['envelope']
    fs = contract['machine_and_sensor']['sampling_hz']
    sos = butter(envelope_cfg['butterworth_order'], envelope_cfg['bandpass_hz'], btype='bandpass', fs=fs, output='sos')
    envelope = np.abs(hilbert(sosfiltfilt(sos, x)))[a:b]
    spectrum = np.abs(np.fft.rfft((envelope-envelope.mean())*windows.hann(len(envelope), sym=False)))**2
    frequencies = np.fft.rfftfreq(len(envelope), 1/fs)
    lo, hi = envelope_cfg['normalization_band_hz']
    denominator = float(spectrum[(frequencies >= lo) & (frequencies <= hi)].sum())
    require(denominator > 0, 'DEGENERATE_ENVELOPE')
    ratios = []
    for fundamental in envelope_cfg['fault_fundamentals_hz']:
        selected = np.zeros(len(frequencies), dtype=bool)
        for h in envelope_cfg['harmonics']:
            selected |= np.abs(frequencies-h*fundamental) <= envelope_cfg['half_width_hz']
        ratios.append(float(spectrum[selected].sum()/denominator))
    result = {'raw_rms': float(np.sqrt(variance)),
              'raw_kurtosis': float(np.mean(z**4)/variance**2),
              'envelope_harmonic_ratio': max(ratios)}
    require(all(math.isfinite(v) and v >= 0 for v in result.values()), 'INVALID_SCORE')
    return result


def fitted_thresholds(data, contract, manifest):
    rows = [r for r in manifest['records'] if r['split'] == 'validation' and r['label'] == 'healthy']
    require([r['bearing_id'] for r in rows] == ['K003', 'K004'], 'VALIDATION_UNITS')
    values = [scores(load_signal(data, r), contract) for r in rows]
    return {k: float(np.nextafter(max(v[k] for v in values), np.inf)) for k in contract['methods']['ids']}


def fit(data):
    contract, freeze, manifest = context(data)
    return dict(schema='x6.industrial.pilot-fit/1',
        frozen_utc=datetime.now(timezone.utc).isoformat(),
        contract_sha256=sha(ROOT/'contract.json'), manifest_sha256=sha(data/'manifest.json'),
        freeze_sha256=sha(ROOT/'freeze.json'), training_bearings=['K003', 'K004'],
        thresholds=fitted_thresholds(data, contract, manifest),
        selection='All methods fixed; no optimization on evaluation labels or scores.')


def same(actual, expected, path='report'):
    if isinstance(expected, dict):
        require(isinstance(actual, dict) and actual.keys() == expected.keys(), 'OUTPUT_KEYS: '+path)
        for k in expected:
            same(actual[k], expected[k], path+'.'+k)
    elif isinstance(expected, list):
        require(isinstance(actual, list) and len(actual) == len(expected), 'OUTPUT_LENGTH: '+path)
        for i, v in enumerate(expected):
            same(actual[i], v, path+'.'+str(i))
    elif type(expected) is float:
        require(type(actual) in (float, int) and math.isfinite(actual)
                and math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-12), 'OUTPUT_NUMBER: '+path)
    else:
        require(type(actual) is type(expected) and actual == expected, 'OUTPUT_VALUE: '+path)


def run(data, fit_path, started_utc=None):
    contract, freeze, manifest = context(data)
    fitted = read(fit_path)
    require(fitted['schema'] == 'x6.industrial.pilot-fit/1', 'FIT_SCHEMA')
    require(fitted['contract_sha256'] == sha(ROOT/'contract.json')
            and fitted['manifest_sha256'] == sha(data/'manifest.json')
            and fitted['freeze_sha256'] == sha(ROOT/'freeze.json'), 'FIT_BINDING')
    require(fitted['training_bearings'] == ['K003', 'K004'], 'FIT_TRAINING_UNITS')
    require(datetime.fromisoformat(fitted['frozen_utc']) > datetime.fromisoformat(freeze['frozen_utc']), 'FIT_BEFORE_SOURCE_FREEZE')
    same(fitted['thresholds'], fitted_thresholds(data, contract, manifest), 'fit.thresholds')
    thresholds = fitted['thresholds']
    rows = []
    for record in manifest['records']:
        row = {k: record[k] for k in ['bearing_id', 'record_id', 'split', 'label']}
        row['scores'] = scores(load_signal(data, record), contract)
        row['decisions'] = {k: row['scores'][k] >= thresholds[k] for k in thresholds}
        rows.append(row)
    evaluation = [r for r in rows if r['split'] == 'evaluation']
    counts = {}
    for method in thresholds:
        tp = sum(r['label'] == 'damaged' and r['decisions'][method] for r in evaluation)
        fp = sum(r['label'] == 'healthy' and r['decisions'][method] for r in evaluation)
        positives = sum(r['label'] == 'damaged' for r in evaluation)
        negatives = sum(r['label'] == 'healthy' for r in evaluation)
        require((positives, negatives) == (4, 2), 'EVALUATION_COMPLETENESS')
        counts[method] = dict(true_positive=tp, false_negative=positives-tp,
            false_positive=fp, true_negative=negatives-fp,
            positive_bearings=positives, negative_bearings=negatives,
            sensitivity_descriptive=tp/positives, false_positive_rate_descriptive=fp/negatives)
    started = started_utc or datetime.now(timezone.utc).isoformat()
    require(datetime.fromisoformat(started) > datetime.fromisoformat(fitted['frozen_utc']), 'RUN_BEFORE_FIT_FREEZE')
    return dict(schema='x6.industrial.pilot-report/1', status='PILOT_PIPELINE_PASS',
        started_utc=started, evidence_class=contract['evidence_class'],
        contract_sha256=sha(ROOT/'contract.json'), manifest_sha256=sha(data/'manifest.json'),
        freeze_sha256=sha(ROOT/'freeze.json'), fit_sha256=sha(fit_path),
        runner_sha256=sha(Path(__file__)),
        units_total=len(rows), units_by_split={k: len(v) for k, v in contract['splits'].items()},
        thresholds=thresholds, records=rows, evaluation=counts,
        primary_baseline=contract['methods']['primary_baseline'],
        industrial_claim_supported=False, confirmatory_v1_status='NOT_READY',
        commercial_use_authorized=False,
        scope='Only complete and reproducible secondary-data/classical-baseline processing on the 20 registered laboratory bearings. Descriptive counts are not a population performance claim.',
        unavailable=['independent_external_data','calibration_certificates','new_filter_comparison','industrial_FPR_guarantee','causal_streaming_and_resources'])


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('command', choices=['fit', 'run', 'verify'])
    p.add_argument('--data', type=Path, default=ROOT/'data')
    p.add_argument('--fit', type=Path, default=ROOT/'evidence/fit.json')
    p.add_argument('--report', type=Path, default=ROOT/'evidence/pilot-report.json')
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    try:
        if a.command == 'fit':
            require(a.output is not None, 'OUTPUT_REQUIRED')
            value = fit(a.data)
        elif a.command == 'run':
            require(a.output is not None, 'OUTPUT_REQUIRED')
            value = run(a.data, a.fit)
        else:
            saved = read(a.report)
            expected = run(a.data, a.fit, saved['started_utc'])
            same(saved, expected)
            value = dict(status='REPLAY_PASS', units=expected['units_total'], industrial_claim_supported=False)
        if a.output:
            write_new(a.output, value)
        print(json.dumps({'status':value.get('status', 'FIT_FROZEN'), 'industrial_claim_supported':False}))
        return 0
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile) as exc:
        print(json.dumps({'status':'INVALID', 'reason':str(exc), 'industrial_claim_supported':False}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
