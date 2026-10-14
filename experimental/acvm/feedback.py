"""Finite slow optical power loop with anti-windup, slew and freshness limits.
SPDX-License-Identifier: Apache-2.0
"""
import math
import random
import time
from .signals import finite
from .optics import calibration, fraction_to_angle


class PI:
    def __init__(self, kp, ki, low, high, initial, slew_per_s):
        for value in (kp, ki, low, high, initial, slew_per_s):
            finite(value)
        if kp < 0 or ki < 0 or not 0 <= low < high <= 1 or not low <= initial <= high or slew_per_s <= 0:
            raise ValueError('PI configuration')
        self.kp, self.ki, self.low, self.high = kp, ki, low, high
        self.integral = initial
        self.output, self.slew = initial, slew_per_s

    def step(self, target, measured, dt):
        finite(target, 'target', 0, 1); finite(measured, 'measurement', 0, 2)
        finite(dt, 'dt', .001, 60)
        error = target-measured
        candidate_i = self.integral+self.ki*error*dt
        raw = self.kp*error+candidate_i
        lower = max(self.low, self.output-self.slew*dt)
        upper = min(self.high, self.output+self.slew*dt)
        self.output = max(lower, min(upper, raw))
        # Back-calculation handles both amplitude and slew saturation.
        self.integral = self.output-self.kp*error
        return self.output


def run_loop(motor, meter, table, config, emit, clock=time.monotonic, wait=time.sleep):
    calibration(table, 'MEASURED')
    if set(config) != {'target_w', 'normalization_w', 'steps', 'period_s', 'kp', 'ki',
                       'slew_per_s', 'initial_fraction', 'park_fraction', 'max_query_s'}:
        raise ValueError('Loop configuration fields')
    norm = finite(config['normalization_w'], 'normalization W', 1e-12, table['max_power_w'])
    target = finite(config['target_w'], 'target W', 0, norm)/norm
    dt = finite(config['period_s'], 'period', table['settle_s'], 60)
    max_query = finite(config['max_query_s'], 'query latency', .001, dt)
    steps = config['steps']
    if type(steps) is not int or not 1 <= steps <= 10000 or steps*dt > 3600:
        raise ValueError('Finite run limit: 1 hour / 10000 measurements')
    points = table['points']
    controller = PI(config['kp'], config['ki'], points[0]['fraction'], points[-1]['fraction'],
                    config['initial_fraction'], config['slew_per_s'])
    park = fraction_to_angle(table, config['park_fraction'])
    # Preflight all fields before the first move.
    angle = fraction_to_angle(table, controller.output)
    result = {'status': 'FAILED', 'evidence_kind': 'DEVICE_REPORTED', 'measurements': 0,
              'optical_loop_qualified': False, 'park': 'NOT_ATTEMPTED'}
    started = clock()
    try:
        motor.move(angle)
        for index in range(steps):
            # Wait after completion of every move, not merely after issuing it.
            wait(dt)
            requested = clock()
            reading = meter.read()
            now = clock()
            finite(reading['request_s'], 'measurement request time', 0)
            finite(reading['received_s'], 'measurement reception time', 0)
            if (reading['request_s'] < requested or reading['received_s'] < reading['request_s']
                    or not 0 <= now-reading['received_s'] <= max_query
                    or reading['received_s']-reading['request_s'] > max_query):
                raise ValueError('Stale, future, or excessively slow feedback')
            if now-started > 3600:
                raise TimeoutError('Maximum loop wall time')
            actual_dt = dt if index == 0 else now-previous_time
            output = controller.step(target, reading['power_w']/norm, actual_dt)
            emit({'index': index, 'reading': reading, 'fraction_before': previous_output if index else config['initial_fraction'],
                  'fraction_next': output, 'dt_s': actual_dt})
            result['measurements'] += 1
            previous_time, previous_output = now, output
            if index+1 < steps:
                motor.move(fraction_to_angle(table, output))
        result['status'] = 'DEVICE_REPORTED_LOOP_COMPLETE'
    except Exception as exc:
        result['error'] = f'{type(exc).__name__}: {exc}'
    finally:
        try:
            motor.move(park)
            result['park'] = 'POSITION_REPORTED_NOT_OPTICALLY_VERIFIED'
        except Exception as exc:
            result['park'] = 'UNKNOWN'; result['park_error'] = str(exc)
            result['status'] = 'FAILED'
    return result


def benchmark():
    """Frozen gains; paired disturbances and equal 160-reading budgets per run.

    Model: detector measures power, actuator controls normalized transmission.
    Dynamic gain and noise are common between fixed and feedback alternatives.
    No hardware claim, confidence interval, or per-sample independence claim.
    """
    calibration_rng = random.Random(17)
    cal_rows = [{'command': u, 'measured': 1.02*u+calibration_rng.gauss(0, .001)}
                for u in (.05, .15, .3, .5, .7, .85, .95)]
    gain_hat = sum(r['command']*r['measured'] for r in cal_rows)/sum(r['command']**2 for r in cal_rows)
    initial = .5/gain_hat
    report = {'evidence_kind': 'SIMULATED', 'calibration_run_ids': ['cal-17'],
              'calibration': {'run_id': 'cal-17', 'rows': cal_rows, 'gain_fit_through_origin': gain_hat,
                              'calibrated_initial_command': initial},
              'test_run_ids': [f'test-{s}' for s in range(101, 106)],
              'gain_selection': 'FROZEN kp=0.25 ki=0.65; no tuning on test runs',
              'criterion': 'each paired run: feedback tail RMSE < 0.5 * fixed tail RMSE',
              'analysis_window': [40, 160], 'runs': []}
    for seed in range(101, 106):
        rng = random.Random(seed)
        disturbance = [(1.02+.18*math.sin(i/25)+.001*i, rng.gauss(0, .002)) for i in range(160)]
        outcomes = {}
        for strategy in ('fixed', 'feedback'):
            pi = PI(.25, .65, .05, .95, initial, .15)
            u, rows = initial, []
            for index, (gain, noise) in enumerate(disturbance):
                y = gain*u+noise
                next_u = pi.step(.5, y, 1) if strategy == 'feedback' else initial
                rows.append({'index': index, 'command': u, 'gain': gain, 'noise': noise,
                             'measured': y, 'error': y-.5, 'next_command': next_u})
                u = next_u
            rmse = math.sqrt(sum(r['error']**2 for r in rows[40:])/120)
            outcomes[strategy] = {'measurements': len(rows), 'rmse': rmse, 'rows': rows}
        report['runs'].append({'run_id': f'test-{seed}', 'strategies': outcomes,
                               'pass': outcomes['feedback']['rmse'] < .5*outcomes['fixed']['rmse']})
    report['status'] = 'MODEL_PASS' if all(r['pass'] for r in report['runs']) else 'MODEL_FAIL'
    return report
