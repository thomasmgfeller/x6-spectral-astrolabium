"""Independent analytic expectations, corruptions, PTY and instrument fault cases.
SPDX-License-Identifier: Apache-2.0
"""
import cmath
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import pty
import select
import tempfile
import threading
import time
import unittest
import zipfile

from experimental.acvm import archive, engine, evidence, feedback, optics, qualification, signals
from experimental.acvm.devices import Ell14, EllSerial, PowerMeter


def plan(n=512):
    return {'schema': 'acvm.d01.plan/1', 'run_id': 'run-A', 'unit': 'normalized_IQ',
            'tick_ns': 1000, 'duration_ticks': n,
            'samples': [{'tick': i, 'i': i/(n+1), 'q': 0} for i in range(n)]}


def profile():
    return {'address': '0', 'serial': '12345678', 'pulses_per_degree': 1000,
            'zero_deg': 0, 'min_deg': 0, 'max_deg': 90, 'tolerance_deg': .05,
            'timeout_s': .2, 'scale_evidence': 'TEST_FIXTURE_NOT_HARDWARE'}


def table(kind='SIMULATED'):
    return {'schema': 'acvm.optical.calibration/1', 'calibration_id': 'fixture-1',
            'evidence_kind': kind, 'unit': 'transmission_fraction', 'wavelength_nm': 810,
            'device_serial': '12345678', 'run_ids': ['cal-1', 'cal-2'], 'settle_s': .5,
            'max_power_w': .001, 'points': [
                {'fraction': f, 'motor_deg': d, 'uncertainty_fraction': .001}
                for f, d in ((.05, 40), (.5, 22.5), (.95, 5))]}


class Script:
    def __init__(self, responses):
        self.responses, self.sent = list(responses), []
    def write(self, data):
        self.sent.append(data)
    def read_line(self, timeout):
        if not self.responses:
            raise TimeoutError('Fixture timeout')
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


INFO = '0IN0E1234567820260101016800040000'


class SignalContractTests(unittest.TestCase):
    def test_export_roundtrip_and_zip_traversal_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'run'; qualification.demo(path)
            target = Path(tmp)/'run.zip'; archive.export(path, target)
            self.assertEqual(archive.verify_zip(target)['samples'], 512)
            with self.assertRaises(FileExistsError): archive.export(path, target)
            bad = Path(tmp)/'bad.zip'
            with zipfile.ZipFile(bad, 'w') as z: z.writestr('../escape', 'bad')
            with self.assertRaises(ValueError): archive.verify_zip(bad)

    def test_V01_reject_nonfinite_wrong_units_bool_and_range(self):
        for value in (float('nan'), float('inf'), -float('inf'), True, 1.001):
            p = plan(); p['samples'][8]['i'] = value
            with self.assertRaises(ValueError): engine.compile_plan(p)
        p = plan(); p['unit'] = 'V'
        with self.assertRaises(ValueError): engine.compile_plan(p)

    def test_V02_cyclic_phase_and_zero_amplitude(self):
        result = signals.phase_error([cmath.exp(2j*math.pi), cmath.exp(-1e-8j), 0j], [1, 1, 1])
        self.assertLess(abs(result[0]), 1e-12)
        self.assertAlmostEqual(result[1], -1e-8, delta=1e-12)
        self.assertIsNone(result[2])
        self.assertIsNone(signals.relative_rms([1j], [0j]))

    def test_V03_nonperiodic_symmetric_delay_raw_and_aligned(self):
        r = [complex(math.exp(-((i-40)/7)**2)) for i in range(81)]
        m = [0j]*3+r[:-3]
        report = signals.align_integer_delay(m, r, 8)
        self.assertGreater(report['raw_relative_rms'], .2)
        self.assertEqual(report['delay_samples'], 3)
        self.assertEqual(report['aligned_relative_rms'], 0)

    def test_V04_signed_spectrum_and_parseval(self):
        n, fs = 64, 640
        x = [2*cmath.exp(2j*math.pi*7*i/n)+.5*cmath.exp(-2j*math.pi*11*i/n) for i in range(n)]
        spec = signals.spectrum(x, fs)
        peaks = sorted(range(n), key=lambda k: spec['density'][k], reverse=True)[:2]
        self.assertEqual([spec['frequency_hz'][k] for k in peaks], [70, -110])
        self.assertAlmostEqual(sum(spec['density'])*spec['bin_width_hz'], 4.25, delta=1e-11)
        self.assertAlmostEqual(spec['density'][7]*10, 4, delta=1e-11)
        self.assertAlmostEqual(spec['density'][53]*10, .25, delta=1e-11)

    def test_V05_change_after_sample_256_and_truncate(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'run'; qualification.demo(path)
            original = (path/'samples.bin').read_bytes()
            data = bytearray(original); data[24+300*24+8] ^= 1
            (path/'samples.bin').write_bytes(data)
            with self.assertRaises(ValueError): archive.verify(path)
            archive.seal(path)  # Rehashed tamper must still disagree with the plan.
            with self.assertRaises(ValueError): archive.verify(path)
            for data in (original[:-1], original+b'\0'):
                with self.assertRaises(ValueError): archive.read_image(data)

    def test_V05_hardware_relabelling_and_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'run'; qualification.demo(path)
            record = json.loads((path/'execution.json').read_text())
            record['evidence_kind'] = 'MEASURED'
            archive.write_json(path/'execution.json', record); archive.seal(path)
            with self.assertRaises(ValueError): archive.verify(path)
            (path/'plan.json').unlink()
            with self.assertRaises(ValueError): archive.verify(path)

    def test_V06_counter_order_capacity(self):
        p = plan(); p['duration_ticks'] = 2**53; p['tick_ns'] = 10**9
        with self.assertRaises(ValueError): engine.compile_plan(p)
        p = plan(); p['samples'][4]['tick'] = 3
        with self.assertRaises(ValueError): engine.compile_plan(p)
        self.assertEqual(len(archive.read_image(engine.compile_plan(plan(4096)))['rows']), 4096)
        with self.assertRaises(ValueError): engine.compile_plan(plan(4097))

    def test_V07_duplicate_start_disconnect_clockloss_identity(self):
        for fault in ('disconnect', 'clockloss', 'identity'):
            p = plan(4); image = engine.compile_plan(p)
            s = engine.Sequencer(p['run_id'], image, archive.read_image(image))
            s.start(p['run_id'], s.digest, 0)
            self.assertEqual(s.start(p['run_id'], s.digest, 0), 'DUPLICATE_IGNORED')
            if fault == 'identity':
                with self.assertRaises(ValueError): s.start('other', s.digest, 1)
            else:
                s.advance(1, connected=fault != 'disconnect', clock_valid=fault != 'clockloss')
            self.assertEqual(s.runs, 1); self.assertEqual(s.state, 'FAULT'); self.assertEqual(s.output, (0, 0))
            s.start(p['run_id'], s.digest, 2)
            self.assertEqual(s.state, 'FAULT')

    def test_V07_missed_tick_cannot_burst(self):
        p = plan(4); image = engine.compile_plan(p)
        s = engine.Sequencer(p['run_id'], image, archive.read_image(image))
        s.start(p['run_id'], s.digest, 0); s.advance(2)
        self.assertEqual(s.state, 'FAULT'); self.assertEqual(len(s.events), 1)

    def test_V08_actual_timestamps_define_signal_and_zero_limit(self):
        f = lambda t: complex(math.cos(2*math.pi*31*t), math.sin(2*math.pi*31*t))
        t0, y0 = signals.time_signal(f, 100, .001)
        for i in range(100):
            self.assertEqual(t0[i], i*.001); self.assertEqual(y0[i], f(i*.001))
        for drift in (-300, 0, 300):
            for jitter in (0, .0002):
                t, y = signals.time_signal(f, 100, .001, .003, drift, jitter, 17)
                for at, value in zip(t, y):
                    self.assertAlmostEqual(value.imag, math.sin(2*math.pi*31*at), delta=1e-14)
                self.assertGreater(signals.relative_rms(y, y0), .1)


class OpticalTests(unittest.TestCase):
    def test_hwp_zero_calibration_with_source_drift_and_dark(self):
        rows = []
        for i, theta in enumerate(range(0, 90, 5)):
            reference = .001*(1+i/30)
            response = .02+.9*math.cos(2*math.radians(theta-3.5))**2
            rows.append({'angle_deg': theta, 'reference_w': reference,
                         'power_w': reference*response+.000001, 'dark_w': .000001})
        result = optics.fit_hwp_zero(rows)
        self.assertAlmostEqual(result['zero_deg_modulo_90'], 3.5, delta=1e-10)
        self.assertLess(result['rmse'], 1e-14)
        for row in rows: row['angle_deg'] = 0
        with self.assertRaises(ValueError): optics.fit_hwp_zero(rows)

    def test_phase_calibration_maps_axes_and_rejects_bad_retardance(self):
        c = {'calibration_id': 'fixture', 'evidence_kind': 'MEASURED', 'wavelength_nm': 810,
             'max_phase_error_rad': .02, 'max_crosstalk_amplitude': .01,
             'axes': {k: {'zero_deg': 2, 'direction': 1, 'retardance_rad': math.pi if k == 'h' else math.pi/2}
                      for k in ('q1', 'h', 'q2')}}
        angles = optics.phase_motor_angles(0, c)
        self.assertAlmostEqual(angles['h'], 47)
        c['axes']['h']['retardance_rad'] = 1
        with self.assertRaises(ValueError): optics.phase_motor_angles(0, c)

    def test_qhq_relative_phase_and_no_polarization_mixing(self):
        for phi in (-2.2, 0, .2, math.pi, 2*math.pi):
            j = optics.qhq_phase(phi)['matrix']
            self.assertLess(abs(j[0][1])+abs(j[1][0]), 1e-14)
            self.assertLess(abs(j[1][1]/j[0][0]-cmath.exp(1j*phi)), 1e-14)

    def test_analyzer_axis_is_half_hwp_angle(self):
        self.assertEqual(optics.linear_analyzer_angle(45, 2), 24.5)
        self.assertEqual(optics.linear_analyzer_angle(-22.5, 2, -1), 13.25)

    def test_calibration_monotonic_no_extrapolation(self):
        t = table(); self.assertEqual(optics.fraction_to_angle(t, .5), 22.5)
        self.assertAlmostEqual(optics.fraction_to_angle(t, .275), 31.25)
        with self.assertRaises(ValueError): optics.fraction_to_angle(t, .99)
        t['points'][-1]['motor_deg'] = 30
        with self.assertRaises(ValueError): optics.calibration(t)

    def test_simulated_calibration_cannot_enable_hardware_loop(self):
        with self.assertRaises(ValueError): optics.calibration(table(), 'MEASURED')

    def test_ell_golden_command_and_identity(self):
        io = Script([INFO, '0PO000057E4'])
        motor = Ell14(io, profile()); motor.identify(); r = motor.move(22.5)
        self.assertEqual(io.sent, [b'0in', b'0ma000057E4'])
        self.assertEqual(r['reported_deg'], 22.5); self.assertFalse(r['physical_position_verified'])

    def test_ell_wrong_model_serial_address(self):
        for bad in (INFO.replace('12345678', '87654321'), INFO.replace('IN0E', 'IN06'), '1'+INFO[1:]):
            io = Script([bad]); motor = Ell14(io, profile())
            with self.assertRaises(ValueError): motor.identify()
            self.assertEqual(io.sent, [b'0in'])

    def test_ell_invalid_angle_never_sends_move(self):
        io = Script([INFO]); motor = Ell14(io, profile()); motor.identify()
        for angle in (-1, 91, float('nan'), True):
            with self.assertRaises(ValueError): motor.move(angle)
        self.assertEqual(io.sent, [b'0in'])

    def test_ell_busy_status_is_not_completion(self):
        io = Script([INFO, '0GS09', '0GS00', '0PO000057E4'])
        motor = Ell14(io, profile()); motor.identify(); motor.move(22.5)
        self.assertEqual(io.sent[-2:], [b'0gs', b'0gp'])

    def test_ell_error_timeout_and_wrong_position_latch_fault(self):
        for response in ('0GS08', '0PO00000000', TimeoutError('lost reply'), '0POZZZZZZZZ'):
            io = Script([INFO, response]); motor = Ell14(io, profile()); motor.identify()
            with self.assertRaises((RuntimeError, ValueError, TimeoutError)): motor.move(22.5)
            self.assertEqual(io.sent[-1], b'0st')
            self.assertEqual(io.sent.count(b'0ma000057E4'), 1)
            with self.assertRaises(RuntimeError): motor.move(22.5)

    def test_ell_real_pty_fragmented_protocol(self):
        master, slave = pty.openpty(); path = os.ttyname(slave); errors = []
        with tempfile.TemporaryDirectory() as tmp:
            with open(Path(tmp)/'wire.jsonl', 'w') as log:
                transport = EllSerial(path, log)
                def responder():
                    try:
                        for command, response in ((b'0in', INFO.encode()+b'\r\n'),
                                                  (b'0ma000057E4', b'0PO000057E4\r\n')):
                            data = b''
                            while len(data) < len(command):
                                if not select.select([master], [], [], 1)[0]: raise TimeoutError('PTY request')
                                data += os.read(master, len(command)-len(data))
                            if data != command: raise AssertionError(data)
                            for chunk in (response[:4], response[4:-1], response[-1:]): os.write(master, chunk)
                    except Exception as exc: errors.append(exc)
                thread = threading.Thread(target=responder); thread.start()
                try:
                    motor = Ell14(transport, profile()); motor.identify(); motor.move(22.5)
                finally:
                    transport.close(); thread.join(2); os.close(master); os.close(slave)
                self.assertFalse(errors); self.assertFalse(thread.is_alive())


class MeterIO:
    def __init__(self):
        self.writes = []
        self.values = {'*IDN?': 'THORLABS,PM100D,PM123,1.0', 'SYST:SENS:IDN?': 'S120C,SN123,cal,1,0,0',
                       'SYST:ERR?': '+0,"No error"', 'SENS:CORR:WAV?': '810',
                       'SENS:POW:UNIT?': 'W', 'MEAS:POW?': '0.0005'}
    def query(self, command): return self.values[command]
    def write(self, command): self.writes.append(command)


class FeedbackTests(unittest.TestCase):
    def test_meter_wrong_units_overrange_nonfinite_error(self):
        for key, value in (('SENS:POW:UNIT?', 'DBM'), ('MEAS:POW?', '9.9E37'),
                           ('MEAS:POW?', 'nan'), ('SYST:ERR?', '-113,"Undefined"')):
            io = MeterIO(); meter = PowerMeter(io, 'PM123', 'SN123', 810, .001)
            io.values[key] = value
            with self.assertRaises((ValueError, RuntimeError)): meter.read()

    def test_meter_identity_readback_and_sensor(self):
        for serial, sensor in (('other', 'SN123'), ('PM123', 'other')):
            with self.assertRaises(ValueError): PowerMeter(MeterIO(), serial, sensor, 810, .001)
        io = MeterIO(); io.values['SENS:CORR:WAV?'] = '780'
        with self.assertRaises(ValueError): PowerMeter(io, 'PM123', 'SN123', 810, .001)

    def test_pi_bounded_slew_and_antiwindup_recovery(self):
        pi = feedback.PI(.25, .65, .05, .95, .5, .1)
        old = .5
        for _ in range(100):
            value = pi.step(1, 0, 1)
            self.assertLessEqual(abs(value-old), .100000001); self.assertLessEqual(value, .95); old = value
        values = [pi.step(0, 1, 1) for _ in range(10)]
        self.assertAlmostEqual(values[-1], .05)

    def test_paired_held_out_feedback_benchmark(self):
        report = feedback.benchmark()
        self.assertEqual(report['status'], 'MODEL_PASS')
        self.assertFalse(set(report['calibration_run_ids']) & set(report['test_run_ids']))
        for run in report['runs']:
            a, b = run['strategies']['fixed'], run['strategies']['feedback']
            self.assertEqual(a['measurements'], b['measurements'])
            self.assertEqual([(r['gain'], r['noise']) for r in a['rows']], [(r['gain'], r['noise']) for r in b['rows']])

    def loop_fixture(self, stale=False, fail_move=False):
        class Clock:
            t = 0
            def now(self): return self.t
            def wait(self, seconds): self.t += seconds
        clock = Clock()
        class Motor:
            moves = []
            def move(self, angle):
                if fail_move: raise OSError('Disconnected')
                self.moves.append(angle)
        class Meter:
            def read(self):
                return {'power_w': .0005, 'request_s': clock.t, 'received_s': clock.t-1 if stale else clock.t}
        config = {'target_w': .0005, 'normalization_w': .001, 'steps': 3, 'period_s': .5,
                  'kp': .25, 'ki': .65, 'slew_per_s': .1, 'initial_fraction': .5,
                  'park_fraction': .05, 'max_query_s': .2}
        motor, records = Motor(), []
        r = feedback.run_loop(motor, Meter(), table('MEASURED'), config, records.append, clock.now, clock.wait)
        return r, motor, records

    def test_bounded_live_loop_with_injected_devices(self):
        r, motor, rows = self.loop_fixture()
        self.assertEqual(r['status'], 'DEVICE_REPORTED_LOOP_COMPLETE')
        self.assertEqual(len(rows), 3); self.assertEqual(motor.moves[-1], 40)
        self.assertFalse(r['optical_loop_qualified'])

    def test_stale_feedback_stops_and_attempts_park(self):
        r, motor, rows = self.loop_fixture(stale=True)
        self.assertEqual(r['status'], 'FAILED'); self.assertEqual(rows, [])
        self.assertEqual(motor.moves[-1], 40)

    def test_disconnect_never_claims_park(self):
        r, _, _ = self.loop_fixture(fail_move=True)
        self.assertEqual(r['status'], 'FAILED'); self.assertEqual(r['park'], 'UNKNOWN')


def measurements():
    criteria = {'max_prediction_error': .02, 'max_drift': .03, 'max_loss_db': 3}
    def run(name, drift=0):
        return {'run_id': name, 'points': [{'time_s': i, 'input': x, 'output': .1+.8*x+drift*i,
                  'uncertainty': .001, 'loss_db': 1, 'loss_uncertainty_db': .1} for i, x in enumerate((.1, .5, .9))]}
    return {'schema': 'acvm.measurements/1', 'evidence_kind': 'SIMULATED', 'bench': 'OPTICAL',
            'unit': 'transmission_fraction', 'criteria': criteria,
            'criteria_sha256': hashlib.sha256(json.dumps(criteria, sort_keys=True, separators=(',', ':')).encode()).hexdigest(),
            'calibration_runs': [run('c1'), run('c2')], 'test_runs': [run('t1'), run('t2')],
            'instrument': 'SIMULATED_FIXTURE', 'uncertainty_method': 'Synthetic absolute envelope; no coverage claim'}


class EvidenceTests(unittest.TestCase):
    def test_V09_absolute_errors_not_fitted_away(self):
        data = {'schema': 'acvm.electrical/1', 'evidence_kind': 'SIMULATED', 'instrument': 'fixture',
                'timebase': 'INDEPENDENT_CALIBRATED', 'uncertainty_method': 'test bounds',
                'voltage_limit_v': .01, 'timing_limit_s': .001,
                'runs': [{'run_id': name, 'points': [{'target_v': 1, 'measured_v': 1.1,
                     'target_s': .1, 'measured_s': .1001, 'uncertainty_v': .001, 'uncertainty_s': .0001}]}
                         for name in ('e1', 'e2')]}
        self.assertEqual(evidence.assess_electrical(data)['status'], 'SIMULATED_DATA_FAIL')
        for run in data['runs']: run['points'][0]['measured_v'] = 1.001
        self.assertEqual(evidence.assess_electrical(data)['status'], 'SIMULATED_DATA_PASS')
        self.assertFalse(evidence.assess_electrical(data)['absolute_timing_qualified'])

    def test_guardbands_include_inconclusive(self):
        self.assertEqual(evidence.decision(.01, .002, .02), 'PASS')
        self.assertEqual(evidence.decision(.03, .002, .02), 'FAIL')
        self.assertEqual(evidence.decision(.019, .002, .02), 'INCONCLUSIVE')
        self.assertEqual(evidence.decision(.02, 0, .02), 'INCONCLUSIVE')

    def test_V10_held_out_pass_bad_data_and_split_leak(self):
        data = measurements(); r = evidence.assess_measurements(data)
        self.assertEqual(r['status'], 'SIMULATED_DATA_PASS')
        self.assertAlmostEqual(r['fit']['slope'], .8)
        bad = copy.deepcopy(data); bad['test_runs'][0]['points'][2]['output'] += .1
        r2 = evidence.assess_measurements(bad)
        self.assertEqual(r2['status'], 'SIMULATED_DATA_FAIL')
        self.assertEqual(r['fit'], r2['fit'])
        bad = copy.deepcopy(data); bad['test_runs'][0]['run_id'] = 'c1'
        with self.assertRaises(ValueError): evidence.assess_measurements(bad)

    def test_V10_unidentifiable_extrapolation_criteria_tamper(self):
        data = measurements(); data['criteria']['max_prediction_error'] = 10
        with self.assertRaises(ValueError): evidence.assess_measurements(data)
        data = measurements(); data['test_runs'][0]['points'][2]['input'] = 1
        with self.assertRaises(ValueError): evidence.assess_measurements(data)
        data = measurements()
        for run in data['calibration_runs']:
            for point in run['points']: point['input'] = .5
        with self.assertRaises(ValueError): evidence.assess_measurements(data)

    def test_feedforward_full_budget_never_claims_demonstration(self):
        data = {'schema': 'acvm.feedforward.budget/1', 'evidence_kind': 'ASSUMED',
                'available_ns': 100, 'reserve_ns': 10,
                'stages': {name: {'latency_ns': 10, 'jitter_bound_ns': 2, 'evidence': 'ASSUMPTION'}
                           for name in ('detector', 'input', 'logic', 'output', 'driver', 'actuator')}}
        r = evidence.feedforward_budget(data)
        self.assertEqual(r['total_upper_ns'], 82); self.assertEqual(r['margin_ns'], 18)
        self.assertFalse(r['fast_feedforward_demonstrated'])
        data['available_ns'] = 82
        self.assertEqual(evidence.feedforward_budget(data)['status'], 'BUDGET_FAIL')
        del data['stages']['actuator']
        with self.assertRaises(ValueError): evidence.feedforward_budget(data)


if __name__ == '__main__':
    unittest.main()
