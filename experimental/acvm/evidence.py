"""Conservative bench-data and feed-forward budget assessments.
Input declarations cannot authenticate that an experiment occurred.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import json
from .signals import finite


def decision(value, uncertainty, limit):
    finite(value, 'metric', 0); finite(uncertainty, 'expanded uncertainty', 0)
    finite(limit, 'upper acceptance limit', 0)
    if value+uncertainty < limit:
        return 'PASS'
    if max(0, value-uncertainty) > limit:
        return 'FAIL'
    return 'INCONCLUSIVE'


def assess_electrical(data):
    required = {'schema', 'evidence_kind', 'instrument', 'timebase', 'uncertainty_method',
                'voltage_limit_v', 'timing_limit_s', 'runs'}
    if set(data) != required or data['schema'] != 'acvm.electrical/1':
        raise ValueError('Electrical schema')
    if data['evidence_kind'] not in ('SIMULATED', 'MEASURED'):
        raise ValueError('Electrical evidence class')
    if data['timebase'] not in ('INDEPENDENT_CALIBRATED', 'SHARED'):
        raise ValueError('Timebase identity')
    if not data['instrument'] or not data['uncertainty_method'] or len(data['runs']) < 2:
        raise ValueError('Missing electrical provenance/repeated runs')
    finite(data['voltage_limit_v'], 'voltage limit', 0)
    finite(data['timing_limit_s'], 'timing limit', 0)
    seen, checks, errors = set(), [], []
    for run in data['runs']:
        if set(run) != {'run_id', 'points'} or not run['run_id'] or run['run_id'] in seen or not run['points']:
            raise ValueError('Electrical run identity')
        seen.add(run['run_id'])
        previous = -1
        for p in run['points']:
            if set(p) != {'target_v', 'measured_v', 'target_s', 'measured_s', 'uncertainty_v', 'uncertainty_s'}:
                raise ValueError('Electrical measurement fields')
            for key, value in p.items():
                finite(value, key, 0)
            if p['target_s'] <= previous:
                raise ValueError('Electrical event ordering')
            previous = p['target_s']
            ve, te = abs(p['target_v']-p['measured_v']), abs(p['target_s']-p['measured_s'])
            checks += [decision(ve, p['uncertainty_v'], data['voltage_limit_v']),
                       decision(te, p['uncertainty_s'], data['timing_limit_s'])]
            errors.append({'voltage_error_v': ve, 'timing_error_s': te})
    state = 'FAIL' if 'FAIL' in checks else 'INCONCLUSIVE' if 'INCONCLUSIVE' in checks else 'PASS'
    return {'status': f"{data['evidence_kind']}_DATA_{state}", 'checks': checks, 'errors': errors,
            'absolute_timing_qualified': False,
            'timing_scope': 'RELATIVE_ONLY' if data['timebase'] == 'SHARED' else 'INDEPENDENT_REFERENCE_DECLARED',
            'physical_qualification': 'REQUIRES_RAW_WAVEFORMS_AND_INDEPENDENT_REVIEW'}


def assess_measurements(data):
    required = {'schema', 'evidence_kind', 'bench', 'unit', 'criteria', 'criteria_sha256',
                'calibration_runs', 'test_runs', 'instrument', 'uncertainty_method'}
    if set(data) != required or data['schema'] != 'acvm.measurements/1':
        raise ValueError('Measurement schema/fields')
    if data['evidence_kind'] not in ('SIMULATED', 'MEASURED') or data['bench'] != 'OPTICAL':
        raise ValueError('Measurement class')
    if data['unit'] != ('V' if data['bench'] == 'ELECTRICAL' else 'transmission_fraction'):
        raise ValueError('Measurement unit')
    criteria = data['criteria']
    if set(criteria) != {'max_prediction_error', 'max_drift', 'max_loss_db'}:
        raise ValueError('Frozen criteria fields')
    if hashlib.sha256(json.dumps(criteria, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest() != data['criteria_sha256']:
        raise ValueError('Criteria digest mismatch')
    for limit in criteria.values():
        finite(limit, 'criterion', 0)
    if not data['instrument'] or not data['uncertainty_method']:
        raise ValueError('Missing instrument/uncertainty provenance')
    seen, groups = set(), []
    for group in ('calibration_runs', 'test_runs'):
        runs = data[group]
        if len(runs) < 2:
            raise ValueError('At least two independent acquisition runs per split')
        points = []
        for run in runs:
            if set(run) != {'run_id', 'points'} or not run['run_id'] or run['run_id'] in seen:
                raise ValueError('Repeated run ID / calibration-test leakage')
            seen.add(run['run_id'])
            if len(run['points']) < 3:
                raise ValueError('Insufficient measurement points')
            previous = -1
            for p in run['points']:
                if set(p) != {'time_s', 'input', 'output', 'uncertainty', 'loss_db', 'loss_uncertainty_db'}:
                    raise ValueError('Point fields')
                for name, value in p.items():
                    finite(value, name, 0)
                if p['time_s'] <= previous:
                    raise ValueError('Nonmonotonic measurement times')
                previous = p['time_s']; points.append(p)
        groups.append(points)
    train, test = groups
    # Linear transfer model, only appropriate for a preselected local branch.
    mean_x = sum(p['input'] for p in train)/len(train)
    mean_y = sum(p['output'] for p in train)/len(train)
    denominator = sum((p['input']-mean_x)**2 for p in train)
    if denominator <= 0:
        raise ValueError('Unidentifiable calibration')
    slope = sum((p['input']-mean_x)*(p['output']-mean_y) for p in train)/denominator
    intercept = mean_y-slope*mean_x
    xlow, xhigh = min(p['input'] for p in train), max(p['input'] for p in train)
    if any(not xlow <= p['input'] <= xhigh for p in test):
        raise ValueError('Held-out data outside calibrated range')
    residual = lambda p: p['output']-(intercept+slope*p['input'])
    # Conservative empirical envelope, not a confidence interval or coverage proof.
    envelope = max(abs(residual(p))+p['uncertainty'] for p in train)
    checks = []
    for p in test:
        checks.append(decision(abs(residual(p)), p['uncertainty']+envelope, criteria['max_prediction_error']))
        checks.append(decision(p['loss_db'], p['loss_uncertainty_db'], criteria['max_loss_db']))
    drift_metrics = []
    for run in data['test_runs']:
        r = [residual(p) for p in run['points']]
        uncertainty = 2*max(p['uncertainty'] for p in run['points'])+2*envelope
        drift_metrics.append({'run_id': run['run_id'], 'residual_span': max(r)-min(r), 'uncertainty': uncertainty})
        checks.append(decision(max(r)-min(r), uncertainty, criteria['max_drift']))
    state = 'FAIL' if 'FAIL' in checks else 'INCONCLUSIVE' if 'INCONCLUSIVE' in checks else 'PASS'
    return {'status': f"{data['evidence_kind']}_DATA_{state}", 'fit': {'slope': slope, 'intercept': intercept},
            'calibration_envelope': envelope, 'drift': drift_metrics,
            'max_test_residual': max(abs(residual(p)) for p in test),
            'all_checks': checks, 'run_split_disjoint': True,
            'physical_qualification': 'REQUIRES_RAW_DATA_AND_INDEPENDENT_REVIEW',
            'criteria_preregistration': 'DIGEST_CHECKED_TIMESTAMP_NOT_AUTHENTICATED'}


def feedforward_budget(data):
    if set(data) != {'schema', 'evidence_kind', 'available_ns', 'reserve_ns', 'stages'} or data['schema'] != 'acvm.feedforward.budget/1':
        raise ValueError('Feed-forward schema')
    if data['evidence_kind'] not in ('ASSUMED', 'MEASURED'):
        raise ValueError('Feed-forward evidence class')
    available = finite(data['available_ns'], 'available time', 0)
    reserve = finite(data['reserve_ns'], 'reserve', 0)
    required = {'detector', 'input', 'logic', 'output', 'driver', 'actuator'}
    if set(data['stages']) != required:
        raise ValueError('Incomplete end-to-end latency chain')
    total = reserve
    for stage in data['stages'].values():
        if set(stage) != {'latency_ns', 'jitter_bound_ns', 'evidence'} or not stage['evidence']:
            raise ValueError('Stage timing provenance')
        total += finite(stage['latency_ns'], 'latency', 0)+finite(stage['jitter_bound_ns'], 'jitter bound', 0)
    # Sum bounds; no independence assumption and no RSS shortcut.
    return {'status': ('CONDITIONAL_BUDGET_FITS' if total < available else 'BUDGET_FAIL'),
            'evidence_kind': data['evidence_kind'], 'total_upper_ns': total,
            'margin_ns': available-total, 'fast_feedforward_demonstrated': False}
