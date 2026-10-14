"""Unified ACVM 0.2 command line. Default qualification never opens devices.
SPDX-License-Identifier: Apache-2.0
"""
import argparse
import json
from pathlib import Path
import sys
from contextlib import ExitStack
from experimental.control_channel.channel import read_json
from . import archive, evidence, qualification
from .devices import Ell14, EllSerial, PowerMeter, LoggedVisa
from .feedback import run_loop
from .optics import calibration, phase_motor_angles, fit_hwp_zero


def hardware(args):
    profile = read_json(args.profile)
    if profile.get('evidence_kind') != 'MEASURED' or not profile.get('commissioning_record'):
        raise ValueError('Measured commissioning profile required; templates cannot operate devices')
    # Compile and range-check all requested motion before opening a serial endpoint.
    if args.command == 'phase':
        mapping = phase_motor_angles(args.radians, profile['phase_calibration'])
        if len({profile['motors'][key]['address'] for key in ('q1', 'h', 'q2')}) != 3:
            raise ValueError('QHQ requires three distinct motor addresses')
        for key in ('q1', 'h', 'q2'):
            m = Ell14(None, profile['motors'][key])
            if not m.p['min_deg'] <= mapping[key] <= m.p['max_deg']:
                raise ValueError('QHQ target outside motor range')
    else:
        Ell14(None, profile['motor'])
        if args.command == 'loop':
            table = read_json(args.calibration); calibration(table, 'MEASURED')
            if table['device_serial'] != profile['motor']['serial']:
                raise ValueError('Calibration/motor identity mismatch')
    output = Path(args.output); output.mkdir(parents=True, exist_ok=False)
    archive.write_json(output/'profile.json', profile)
    result = {'status': 'FAILED', 'physical_qualification': 'NOT_PERFORMED'}
    try:
        with ExitStack() as stack:
            log = stack.enter_context((output/'serial.jsonl').open('w'))
            transport = EllSerial(args.port, log); stack.callback(transport.close)
            if args.command == 'phase':
                # Three separately identified physical rotators on one serial bus.
                results = []
                motors = {key: Ell14(transport, profile['motors'][key]) for key in ('q1', 'h', 'q2')}
                for motor in motors.values():
                    motor.identify()
                for key in ('q1', 'h', 'q2'):
                    results.append(motors[key].move(mapping[key]))
                result = {'status': 'POSITIONS_REPORTED_PHASE_UNVERIFIED', 'positions': results,
                          'ideal_relative_phase_rad': args.radians, 'physical_qualification': 'NOT_PERFORMED'}
            else:
                motor = Ell14(transport, profile['motor']); motor.identify()
                if args.command == 'move':
                    result = {'status': 'POSITION_REPORTED', **motor.move(args.degrees)}
                else:
                    table = read_json(args.calibration); calibration(table, 'MEASURED')
                    if table['device_serial'] != profile['motor']['serial']:
                        raise ValueError('Calibration/motor identity mismatch')
                    archive.write_json(output/'calibration.json', table)
                    import pyvisa  # Optional only for explicitly selected hardware loop.
                    manager = pyvisa.ResourceManager(args.visa_backend); stack.callback(manager.close)
                    io = manager.open_resource(args.meter, timeout=1000, read_termination='\n', write_termination='\n')
                    stack.callback(io.close)
                    meter_log = stack.enter_context((output/'meter.jsonl').open('w'))
                    meter = PowerMeter(LoggedVisa(io, meter_log), profile['meter_serial'], profile['sensor_serial'],
                                       table['wavelength_nm'], table['max_power_w'])
                    events = stack.enter_context((output/'feedback.jsonl').open('w'))
                    def emit(record):
                        events.write(json.dumps(record, allow_nan=False)+'\n'); events.flush()
                    result = run_loop(motor, meter, table, profile['loop'], emit)
    except BaseException as exc:
        result.update(status='FAILED', error=f'{type(exc).__name__}: {exc}')
    archive.write_json(output/'result.json', result)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description='ACVM 0.2 reference/optical workflow')
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ('qualify', 'demo'):
        p = sub.add_parser(name); p.add_argument('--output', required=True)
    p = sub.add_parser('verify'); p.add_argument('directory')
    p = sub.add_parser('export'); p.add_argument('directory'); p.add_argument('--output', required=True)
    for name in ('assess-electrical', 'assess-optical', 'feedforward-budget', 'fit-hwp'):
        p = sub.add_parser(name); p.add_argument('input'); p.add_argument('--output', required=True)
    for name in ('move', 'phase', 'loop'):
        p = sub.add_parser(name)
        p.add_argument('--profile', required=True); p.add_argument('--port', required=True)
        p.add_argument('--output', required=True)
        if name == 'move':
            p.add_argument('--degrees', type=float, required=True)
        elif name == 'phase':
            p.add_argument('--radians', type=float, required=True)
        else:
            p.add_argument('--calibration', required=True); p.add_argument('--meter', required=True)
            p.add_argument('--visa-backend', required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'qualify':
            result = qualification.qualify(args.output)
        elif args.command == 'demo':
            result = qualification.demo(args.output)
        elif args.command == 'verify':
            result = archive.verify_zip(args.directory) if Path(args.directory).is_file() else archive.verify(args.directory)
        elif args.command == 'export':
            result = archive.export(args.directory, args.output)
        elif args.command in ('move', 'phase', 'loop'):
            result = hardware(args)
        else:
            function = {'assess-electrical': evidence.assess_electrical,
                        'assess-optical': evidence.assess_measurements,
                        'fit-hwp': fit_hwp_zero,
                        'feedforward-budget': evidence.feedforward_budget}[args.command]
            result = function(read_json(args.input))
            # No stale report: exclusive creation; never overwrite a prior PASS.
            with open(args.output, 'x') as stream:
                json.dump(result, stream, indent=2, allow_nan=False); stream.write('\n')
        print(json.dumps(result, indent=2, allow_nan=False))
        return 1 if 'FAIL' in result.get('status', '') else 0
    except Exception as exc:
        print(f'ACVM failed: {type(exc).__name__}: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
