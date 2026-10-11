#!/usr/bin/env python3
"""Loopback-only, read-only Sagnac v0.7 bridge. No FPGA/optical commands.

Default: immutable synthetic replay. Explicit --device: finite Linux serial
capture, saved in full (including failed/partial captures). Uses stdlib only.
"""
import argparse
import base64
import hashlib
import json
import math
import os
import select
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VENDOR = Path(__file__).parent / 'vendor' / 'sagnac_v0_7'
sys.path.insert(0, str(VENDOR))
from frame_codec import decode_stream, FRAME_BYTES
from analyze import validate


class CaptureState:
    def __init__(self, origin, first_sequence, mode):
        if origin not in ('synthetic', 'hardware'):
            raise ValueError('Explicit origin required')
        if isinstance(first_sequence, bool) or not isinstance(first_sequence, int) or not 0 <= first_sequence < 2**64:
            raise ValueError('first_sequence must be uint64')
        self.origin, self.first_sequence, self.mode = origin, first_sequence, mode
        self.lock = threading.Lock()
        self.data = b''
        self.status = 'WAITING'
        self.reason = None
        self.recorded_at = None

    def complete(self, data, reason=None):
        data = bytes(data)
        try:
            if reason:
                raise ValueError(reason)
            if len(data) > 4096 * FRAME_BYTES:
                raise ValueError('Capture too large')
            decoded = decode_stream(data, origin=self.origin, expected_first_sequence=self.first_sequence)
            for record in decoded['records']:
                validate(record)
            status = 'COMPLETE'
        except (ValueError, TypeError) as exc:
            status, reason = 'INVALID', str(exc)
        with self.lock:
            self.data, self.status, self.reason = data, status, reason
            self.recorded_at = datetime.now(timezone.utc).isoformat()

    def report(self):
        with self.lock:
            return {'schema': 'x6.sagnac.bridge/1', 'mode': self.mode,
                    'status': self.status, 'reason': self.reason,
                    'origin': self.origin, 'first_sequence': str(self.first_sequence),
                    'recorded_at_utc': self.recorded_at, 'bytes_received': len(self.data),
                    'raw_base64': base64.b64encode(self.data).decode('ascii'),
                    'raw_sha256': hashlib.sha256(self.data).hexdigest(),
                    'physical_quantum_claim': 'NOT_ASSESSED',
                    'capabilities': {'read_snapshot': True, 'start_measurement': False,
                                     'set_analyzer': False, 'closed_loop': False}}


def acquire_serial(state, device, frames, baud, timeout, raw_path, stop=None):
    """Finite receive with incremental raw persistence; tested with a Linux PTY.

    Termios setup adapted from the MIT-licensed Sagnac v0.7 receiver retained
    under device/vendor/sagnac_v0_7. No UART output is written.
    """
    data, reason, fd, old = bytearray(), None, None, None
    stop = stop or threading.Event()
    try:
        import termios
        import tty
        if not 1 <= frames <= 4096 or not math.isfinite(timeout) or timeout <= 0:
            raise ValueError('Invalid frame count or timeout')
        speed = getattr(termios, 'B' + str(baud), None)
        if speed is None:
            raise ValueError('Unsupported Linux UART baud rate')
        with Path(raw_path).open('xb') as raw:
            fd = os.open(device, os.O_RDONLY | os.O_NOCTTY | os.O_NONBLOCK)
            old = termios.tcgetattr(fd)
            tty.setraw(fd, when=termios.TCSANOW)
            attrs = termios.tcgetattr(fd)
            attrs[4] = attrs[5] = speed
            attrs[2] |= termios.CLOCAL | termios.CREAD
            attrs[2] &= ~(termios.CSTOPB | getattr(termios, 'CRTSCTS', 0))
            termios.tcsetattr(fd, termios.TCSANOW, attrs)
            deadline, target = time.monotonic() + timeout, frames * FRAME_BYTES
            while len(data) < target:
                if stop.is_set():
                    reason = 'Capture cancelled; partial raw bytes retained'
                    break
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    reason = 'Capture deadline exceeded; partial raw bytes retained'
                    break
                if not select.select([fd], [], [], min(remaining, 0.1))[0]:
                    continue
                try:
                    chunk = os.read(fd, target - len(data))
                except BlockingIOError:
                    continue
                if not chunk:
                    reason = 'UART closed before prescribed frame count'
                    break
                data.extend(chunk)
                raw.write(chunk)
                raw.flush()
    except (OSError, ValueError, ImportError) as exc:
        reason = str(exc)
    finally:
        if fd is not None:
            if old is not None:
                try:
                    termios.tcsetattr(fd, termios.TCSANOW, old)
                except OSError:
                    pass
            os.close(fd)
        state.complete(data, reason)


def make_server(state, port=8766):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

        def reply(self, status, body, content_type='application/json'):
            if isinstance(body, dict):
                body = json.dumps(body, allow_nan=False).encode()
            self.send_response(status)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            actual_port = self.server.server_port
            allowed = {f'127.0.0.1:{actual_port}', f'localhost:{actual_port}'}
            if self.headers.get('Host') not in allowed:
                return self.reply(403, {'error': 'Loopback Host required'})
            origin = self.headers.get('Origin')
            if origin and origin not in {'http://' + h for h in allowed}:
                return self.reply(403, {'error': 'Same-origin access required'})
            if self.path == '/api/sagnac/capture':
                return self.reply(200, state.report())
            routes = {'/': ('index.html', 'text/html; charset=utf-8'),
                      '/app/': ('index.html', 'text/html; charset=utf-8'),
                      '/app/index.html': ('index.html', 'text/html; charset=utf-8'),
                      '/app/sagnac-core.js': ('sagnac-core.js', 'text/javascript; charset=utf-8'),
                      '/app/sagnac-ui.js': ('sagnac-ui.js', 'text/javascript; charset=utf-8'),
                      '/sagnac-core.js': ('sagnac-core.js', 'text/javascript; charset=utf-8'),
                      '/sagnac-ui.js': ('sagnac-ui.js', 'text/javascript; charset=utf-8')}
            entry = routes.get(self.path)
            if not entry:
                return self.reply(404, {'error': 'Not found'})
            try:
                body = (ROOT / 'app' / entry[0]).read_bytes()
            except OSError:
                return self.reply(500, {'error': 'Application file missing'})
            self.reply(200, body, entry[1])

        def do_POST(self):
            self.reply(405, {'error': 'Read-only bridge: no measurement or actuator commands implemented'})

    return ThreadingHTTPServer(('127.0.0.1', port), Handler)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    source = p.add_mutually_exclusive_group()
    source.add_argument('--capture', type=Path)
    source.add_argument('--device', help='Explicit Linux UART path; no probing')
    p.add_argument('--origin', choices=('synthetic', 'hardware'))
    p.add_argument('--first-sequence', type=int)
    p.add_argument('--frames', type=int, default=4)
    p.add_argument('--baud', type=int, default=1000000)
    p.add_argument('--timeout', type=float, default=120)
    p.add_argument('--raw', type=Path, help='New output file for serial bytes')
    p.add_argument('--port', type=int, default=8766)
    a = p.parse_args()
    if not 1 <= a.frames <= 4096 or not math.isfinite(a.timeout) or a.timeout <= 0 or not 0 <= a.port <= 65535:
        p.error('Invalid frames, timeout or port')
    if (a.capture or a.device) and (a.origin is None or a.first_sequence is None):
        p.error('External input requires --origin and --first-sequence')
    if a.device and (a.raw is None or a.raw.exists() or not a.raw.parent.is_dir()):
        p.error('Serial input requires a NEW --raw path in an existing directory')
    if a.first_sequence is not None and not 0 <= a.first_sequence < 2**64:
        p.error('--first-sequence must be uint64')
    if not a.capture and not a.device and (a.origin is not None or a.first_sequence is not None):
        p.error('Default demo has fixed synthetic provenance and sequence 100')
    state = CaptureState(a.origin or 'synthetic', 100 if a.first_sequence is None else a.first_sequence,
                         'SERIAL_FINITE_CAPTURE' if a.device else 'FILE_REPLAY')
    if not a.device:
        path = a.capture or ROOT / 'device' / 'fixtures' / 'synthetic_chsh_capture.bin'
        try:
            if path.stat().st_size > 4096 * FRAME_BYTES:
                p.error('Capture exceeds 4096 frames')
            state.complete(path.read_bytes())
        except OSError as exc:
            p.error(str(exc))
    server = make_server(state, a.port)
    stop, worker = threading.Event(), None
    if a.device:
        worker = threading.Thread(target=acquire_serial, args=(state, a.device, a.frames, a.baud, a.timeout, a.raw, stop))
        worker.start()
    print(f'X6 Sagnac: http://127.0.0.1:{server.server_port}/app/ — {state.mode}; actuator control unavailable', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()
        if worker:
            worker.join(timeout=2)


if __name__ == '__main__':
    main()
