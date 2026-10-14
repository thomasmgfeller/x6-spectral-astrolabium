"""Executable ACVM V01–V08 model qualification plus C1 regression evidence.
SPDX-License-Identifier: Apache-2.0
"""
import cmath
import hashlib
import math
from pathlib import Path
import platform
import re
import subprocess
import sys
from . import archive, engine, feedback

ROOT = Path(__file__).resolve().parents[2]


def demo(output):
    output = Path(output); output.mkdir(parents=True, exist_ok=False)
    plan = {'schema': 'acvm.d01.plan/1', 'run_id': 'D01-reference', 'unit': 'normalized_IQ',
            'tick_ns': 1000000, 'duration_ticks': 512, 'samples': []}
    for n in range(512):
        # Negative-frequency complex tone, real sine, DC and a nonperiodic marker.
        z = .15+.25*cmath.exp(-2j*math.pi*13*n/512)+.1*math.sin(2*math.pi*7*n/512)
        if 173 <= n < 179:
            z += .35
        plan['samples'].append({'tick': n, 'i': z.real, 'q': z.imag})
    image = engine.compile_plan(plan)
    decoded = archive.read_image(image)
    sequencer = engine.Sequencer(plan['run_id'], image, decoded)
    sequencer.start(plan['run_id'], hashlib.sha256(image).hexdigest(), 0)
    for n in range(1, 513):
        sequencer.advance(n)
    archive.write_json(output/'plan.json', plan)
    (output/'samples.bin').write_bytes(image)
    archive.write_json(output/'execution.json', {'evidence_kind': 'SIMULATED', 'run_id': plan['run_id'],
        'events': sequencer.events, 'final_state': sequencer.state, 'runs': sequencer.runs})
    archive.seal(output)
    return archive.verify(output)


def qualify(output):
    output = Path(output); output.mkdir(parents=True, exist_ok=False)
    report = {'schema': 'acvm.qualification/2', 'status': 'FAILED', 'checks': {},
              'environment': {'python': sys.version, 'platform': platform.platform()},
              'V09': 'NOT_PERFORMED_NO_INDEPENDENT_ELECTRICAL_DATA',
              'V10': 'NOT_PERFORMED_NO_HELD_OUT_OPTICAL_DATA',
              'physical_closed_loop': 'NOT_PERFORMED', 'fast_feedforward': 'NOT_PERFORMED',
              'hardware_adapters': 'MODEL_AND_PTY_TESTED_NOT_DEVICE_QUALIFIED'}
    try:
        run = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests/acvm', '-v'],
                             cwd=ROOT, capture_output=True, text=True, timeout=60)
        (output/'tests.log').write_text(run.stdout+run.stderr)
        if run.returncode:
            raise RuntimeError('ACVM tests failed; see tests.log')
        report['checks']['tests'] = int(re.search(r'Ran (\d+) tests', run.stderr).group(1))
        report['checks']['D01'] = demo(output/'D01')
        comparison = feedback.benchmark()
        archive.write_json(output/'feedback-benchmark.json', comparison)
        if comparison['status'] != 'MODEL_PASS':
            raise RuntimeError('Frozen feedback benchmark failed')
        report['checks']['feedback'] = [{
            'run_id': r['run_id'], 'fixed_rmse': r['strategies']['fixed']['rmse'],
            'feedback_rmse': r['strategies']['feedback']['rmse'], 'pass': r['pass']}
            for r in comparison['runs']]
        from experimental.control_channel.qualification import qualify as c1_qualify
        c1 = c1_qualify(output/'C1-regression')
        if c1['status'] != 'SOFTWARE_PASS_HARDWARE_OPEN':
            raise RuntimeError('C1 regression failed')
        report['checks']['C1'] = c1['status']
        report['V01_V08'] = {f'V{i:02d}': 'MODEL_PASS' for i in range(1, 9)}
        report['status'] = 'SOFTWARE_PASS_PHYSICAL_GATES_OPEN'
    except Exception as exc:
        report['error'] = f'{type(exc).__name__}: {exc}'
    report['sources'] = {p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                         for folder in ('experimental/acvm', 'tests/acvm')
                         for p in sorted((ROOT/folder).rglob('*')) if p.is_file() and '__pycache__' not in str(p)}
    archive.write_json(output/'qualification.json', report)
    return report
