"""Strict plan compiler and ACV1 host. Python stdlib only; Linux/POSIX transport.

Device ACK values are commanded DAC codes, never measured voltage or position.
Copyright 2026 Thomas Gfeller. SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import json
import os
from pathlib import Path
import secrets
import select
import stat
import struct
import termios
import time
import tty
import zlib

PROFILE = 0xAC010001
PROFILE_NAME = 'pico-mcp4921-code-v1'
OPEN, BEGIN, POINT, SEAL, START, POLL, STOP = range(1, 8)
STATES = ['IDLE', 'LOADING', 'READY', 'RUNNING', 'DONE', 'ABORTED', 'FAULT']
ERRORS = ['OK', 'FORMAT', 'SESSION', 'ORDER', 'RANGE', 'BAD_STATE', 'PLAN_CRC',
          'LEASE', 'LATE', 'CLOCK', 'REPLAY_CONFLICT', 'PROFILE_ERROR']
WIRE = struct.Struct('<4sBBH9I')
ROOT = Path(__file__).resolve().parents[2]


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    def reject(value):
        raise ValueError('Nonfinite JSON: ' + value)
    data = Path(path).read_bytes()
    if len(data) > 65536:
        raise ValueError('JSON exceeds 64 KiB')
    return json.loads(data, parse_constant=reject, object_pairs_hook=pairs)


def integer(value, low, high, name):
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f'{name}: expected integer {low}..{high}')
    return value


def compile_plan(plan):
    if not isinstance(plan, dict) or set(plan) != {'schema', 'profile', 'duration_ms', 'points'}:
        raise ValueError('Unexpected plan fields')
    if plan['schema'] != 'acvm.channel.plan/1' or plan['profile'] != PROFILE_NAME:
        raise ValueError('Unsupported schema/profile/units')
    duration = integer(plan['duration_ms'], 10, 5000, 'duration_ms')
    points = plan['points']
    if not isinstance(points, list) or not 1 <= len(points) <= 64:
        raise ValueError('Expected 1..64 points')
    payload = struct.pack('<II', duration, len(points))
    previous = -10
    for i, point in enumerate(points):
        if not isinstance(point, dict) or set(point) != {'at_ms', 'dac_code'}:
            raise ValueError('Point fields must be at_ms and dac_code')
        ms = integer(point['at_ms'], 0, duration - 10, 'at_ms')
        code = integer(point['dac_code'], 0, 3276, 'dac_code')
        if (i == 0 and ms != 0) or ms - previous < 10:
            raise ValueError('First point must start at 0; spacing must be >=10 ms')
        previous = ms
        payload += struct.pack('<II', ms, code)
    return payload


def packet(op, session, seq, *args):
    if len(args) > 7:
        raise ValueError('Too many command arguments')
    for value in (op, session, seq, *args):
        integer(value, 0, 0xffffffff, 'wire integer')
    data = WIRE.pack(b'ACV1', op, 0, 0, session, seq, *args, *([0] * (7-len(args))))
    return data + struct.pack('<I', zlib.crc32(data))


def decode(data):
    if len(data) != 48 or zlib.crc32(data[:44]) != struct.unpack('<I', data[44:])[0]:
        raise ValueError('Response length/CRC mismatch')
    magic, op, kind, flags, session, seq, error, state, code, applied, elapsed, runs, profile = WIRE.unpack(data[:44])
    if magic != b'ACV1' or kind != 1 or flags & ~3 or profile != PROFILE:
        raise ValueError('Response header/profile mismatch')
    if op not in range(1, 8) or error >= len(ERRORS) or state >= len(STATES) or code > 3276 or applied > 64 or elapsed > 5000:
        raise ValueError('Response values out of range')
    return {'op': op, 'session': session, 'seq': seq, 'error': ERRORS[error],
            'state': STATES[state], 'commanded_dac_code': code, 'applied_points': applied,
            'elapsed_ms': elapsed, 'run_counter': runs, 'profile': profile,
            'endpoint': 'HARDWARE_DECLARED' if flags & 1 else 'MODEL', 'replayed': bool(flags & 2)}


class Transport:
    """Exclusive explicitly selected serial endpoint. No enumeration or reconnect."""
    def __init__(self, path, log=None):
        self.log = log
        self.buffer = bytearray()
        self.fd = os.open(path, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
        try:
            if not stat.S_ISCHR(os.fstat(self.fd).st_mode) or not os.isatty(self.fd):
                raise ValueError('Expected a serial character device')
            import fcntl
            fcntl.ioctl(self.fd, termios.TIOCEXCL)
            self.original = termios.tcgetattr(self.fd)
            tty.setraw(self.fd)
            settings = termios.tcgetattr(self.fd)
            settings[4] = settings[5] = termios.B115200
            settings[2] |= termios.CLOCAL | termios.CREAD
            termios.tcsetattr(self.fd, termios.TCSANOW, settings)
            termios.tcflush(self.fd, termios.TCIOFLUSH)
        except BaseException:
            os.close(self.fd)
            raise

    def record(self, direction, data):
        if self.log:
            self.log.write(json.dumps({'monotonic_ns': time.monotonic_ns(),
                                       'direction': direction, 'hex': data.hex()}) + '\n')
            self.log.flush()
            os.fsync(self.log.fileno())

    def write(self, data, timeout=0.15):
        self.record('tx', data)
        deadline = time.monotonic() + timeout
        remaining = memoryview(data)
        while remaining:
            left = deadline-time.monotonic()
            if left <= 0 or not select.select([], [self.fd], [], left)[1]:
                raise TimeoutError('Serial write timeout')
            try:
                written = os.write(self.fd, remaining)
            except BlockingIOError:
                continue
            if not written:
                raise OSError('Serial write returned zero')
            remaining = remaining[written:]

    def read(self, timeout=0.15):
        deadline = time.monotonic() + timeout
        while True:
            if len(self.buffer) >= 48:
                data = bytes(self.buffer[:48]); del self.buffer[:48]
                decode(data)  # Fail closed on corruption; retain raw bytes in log.
                return data
            left = deadline-time.monotonic()
            if left <= 0 or not select.select([self.fd], [], [], left)[0]:
                raise TimeoutError('Serial response timeout')
            try:
                data = os.read(self.fd, 4096)
            except BlockingIOError:
                continue
            if not data:
                raise OSError('Serial connection closed')
            self.record('rx', data)
            self.buffer.extend(data)
            if len(self.buffer) > 8192:
                raise ValueError('Serial buffer overflow')

    def close(self):
        try:
            termios.tcsetattr(self.fd, termios.TCSANOW, self.original)
        except (OSError, termios.error):
            pass
        os.close(self.fd)


class Client:
    def __init__(self, transport, expected_endpoint):
        self.transport = transport
        self.session = secrets.randbelow(0xffffffff) + 1
        self.seq = 0
        self.expected_endpoint = expected_endpoint
        self.last = None

    def command(self, op, *args):
        data = packet(op, self.session, self.seq, *args)
        # At most one retry, always byte-identical. Never reconnect/restart a run.
        for attempt in range(2):
            self.transport.write(data)
            try:
                deadline = time.monotonic() + 0.15
                for _ in range(4):
                    response = decode(self.transport.read(max(0, deadline-time.monotonic())))
                    if response['session'] != self.session:
                        raise ValueError('Session mismatch; possible device reset')
                    if response['seq'] < self.seq:
                        continue  # delayed duplicate ACK from a byte-identical retry
                    if response['seq'] != self.seq or response['op'] != op:
                        raise ValueError('Response command identity mismatch')
                    if response['endpoint'] != self.expected_endpoint:
                        raise ValueError('Endpoint class mismatch')
                    self.last = response
                    if response['error'] != 'OK':
                        raise RuntimeError('Device error: ' + response['error'])
                    self.seq += 1
                    return response
                raise ValueError('Too many stale responses')
            except TimeoutError:
                if attempt:
                    raise
        raise RuntimeError('Unreachable transaction state')

    def load(self, plan):
        compiled = compile_plan(plan)
        self.command(OPEN, PROFILE)
        self.command(BEGIN, len(plan['points']), plan['duration_ms'], zlib.crc32(compiled))
        for index, point in enumerate(plan['points']):
            self.command(POINT, index, point['at_ms'], point['dac_code'])
        return self.command(SEAL)

    def stop(self):
        # Valid STOP bypasses sequence gaps on the device; response may carry a fault.
        return self.command(STOP)


def run(plan_path, port, output, expected_endpoint):
    plan = read_json(plan_path)
    compiled = compile_plan(plan)  # validate before opening the serial device
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    (output/'plan.json').write_bytes(json_bytes(plan))
    (output/'compiled.bin').write_bytes(compiled)
    result = {'schema': 'acvm.channel.run/1', 'status': 'INCOMPLETE',
              'endpoint': expected_endpoint, 'electrical_validation': 'NOT_PERFORMED',
              'optical_validation': 'NOT_PERFORMED', 'physical_quantum_claim': 'NOT_ASSESSED',
              'port': str(port), 'plan_sha256': hashlib.sha256(compiled).hexdigest(),
              'responses': [], 'stop_acknowledged': False}
    transport = None; client = None
    try:
        with (output/'transport.jsonl').open('x') as log:
            transport = Transport(port, log)
            client = Client(transport, expected_endpoint)
            result['session'] = client.session
            result['responses'].append(client.load(plan))
            response = client.command(START)
            result['responses'].append(response)
            deadline = time.monotonic() + plan['duration_ms']/1000 + 1
            while response['state'] == 'RUNNING':
                if time.monotonic() >= deadline:
                    raise TimeoutError('Run completion deadline')
                time.sleep(0.05)
                response = client.command(POLL)
                result['responses'].append(response)
            if response['state'] != 'DONE' or response['applied_points'] != len(plan['points']) or response['commanded_dac_code'] != 0:
                raise RuntimeError('Sequence did not complete with zero code')
            result['status'] = 'MODEL_EXECUTION_PASS' if expected_endpoint == 'MODEL' else 'DEVICE_EXECUTION_REPORTED'
    except (Exception, KeyboardInterrupt) as exc:
        result['status'] = 'FAILED'
        result['error'] = f'{type(exc).__name__}: {exc}'
        if client:
            result['last_response'] = client.last
        # The log must remain open for STOP on failure; reopen append-only below.
        if client and transport:
            try:
                with (output/'transport.jsonl').open('a') as log:
                    transport.log = log
                    client.stop()
                    result['stop_acknowledged'] = True
            except Exception as stop_error:
                result['stop_error'] = str(stop_error)
    finally:
        if transport:
            transport.close()
        files = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in output.iterdir() if p.is_file()}
        result['files'] = files
        (output/'result.json').write_bytes(json_bytes(result))
    return result
