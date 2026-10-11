import base64
import http.client
import importlib.util
import json
import os
from pathlib import Path
import pty
import tempfile
import termios
import threading
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('sagnac_bridge', ROOT / 'device/sagnac_bridge.py')
bridge = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bridge)
RAW = (ROOT / 'device/fixtures/synthetic_chsh_capture.bin').read_bytes()


class BridgeTests(unittest.TestCase):
    def test_replay_complete_with_exact_raw_and_no_control(self):
        state = bridge.CaptureState('synthetic', 100, 'FILE_REPLAY')
        state.complete(RAW)
        r = state.report()
        self.assertEqual(r['status'], 'COMPLETE')
        self.assertEqual(base64.b64decode(r['raw_base64']), RAW)
        self.assertFalse(r['capabilities']['closed_loop'])
        self.assertEqual(r['physical_quantum_claim'], 'NOT_ASSESSED')

    def test_invalid_capture_clears_previous_success_and_keeps_bad_bytes(self):
        state = bridge.CaptureState('synthetic', 100, 'FILE_REPLAY')
        state.complete(RAW)
        state.complete(RAW[:-1])
        self.assertEqual(state.report()['status'], 'INVALID')
        self.assertEqual(base64.b64decode(state.report()['raw_base64']), RAW[:-1])

    def test_http_read_only_loopback_and_no_filesystem_exposure(self):
        state = bridge.CaptureState('synthetic', 100, 'FILE_REPLAY')
        state.complete(RAW)
        server = bridge.make_server(state, 0)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            def request(method, path, headers=None):
                conn = http.client.HTTPConnection('127.0.0.1', server.server_port)
                conn.request(method, path, headers=headers or {})
                r = conn.getresponse(); out = r.status, r.read(); conn.close(); return out
            self.assertEqual(request('GET', '/api/sagnac/capture')[0], 200)
            self.assertEqual(request('POST', '/api/control')[0], 405)
            self.assertEqual(request('GET', '/api/sagnac/capture', {'Host': 'evil.example'})[0], 403)
            self.assertEqual(request('GET', '/api/sagnac/capture', {'Origin': 'https://evil.example'})[0], 403)
            self.assertEqual(request('GET', '/../../README.md')[0], 404)
            self.assertEqual(request('GET', '/app/')[0], 200)
        finally:
            server.shutdown(); server.server_close(); worker.join(2)

    def run_serial(self, data, *, cancel=False, preexisting=False):
        master, slave = pty.openpty()
        state = bridge.CaptureState('synthetic', 100, 'SERIAL_FINITE_CAPTURE')
        stop = threading.Event()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / 'capture.bin'
                if preexisting: out.write_bytes(b'previous evidence')
                worker = threading.Thread(target=bridge.acquire_serial, args=(state, os.ttyname(slave), 4, 115200, 0.5, out, stop))
                worker.start()
                if not preexisting:
                    deadline = time.monotonic() + 1
                    while termios.tcgetattr(slave)[3] & termios.ICANON:
                        self.assertLess(time.monotonic(), deadline)
                        time.sleep(0.005)
                    for i in range(0, len(data), 37): os.write(master, data[i:i + 37])
                    if cancel:
                        deadline = time.monotonic() + 1
                        while out.stat().st_size != len(data):
                            self.assertLess(time.monotonic(), deadline); time.sleep(0.005)
                        stop.set()
                worker.join(2)
                self.assertFalse(worker.is_alive())
                return state.report(), out.read_bytes()
        finally:
            os.close(master); os.close(slave)

    def test_chunked_serial_receive(self):
        report, raw = self.run_serial(RAW)
        self.assertEqual(report['status'], 'COMPLETE')
        self.assertEqual(raw, RAW)

    def test_timeout_preserves_partial_raw(self):
        report, raw = self.run_serial(RAW[:93])
        self.assertEqual(report['status'], 'INVALID')
        self.assertIn('deadline', report['reason'])
        self.assertEqual(raw, RAW[:93])

    def test_cancel_preserves_partial_raw(self):
        report, raw = self.run_serial(RAW[:91], cancel=True)
        self.assertEqual(report['status'], 'INVALID')
        self.assertIn('cancelled', report['reason'])
        self.assertEqual(raw, RAW[:91])

    def test_existing_raw_file_cannot_be_overwritten(self):
        report, raw = self.run_serial(b'', preexisting=True)
        self.assertEqual(report['status'], 'INVALID')
        self.assertEqual(raw, b'previous evidence')


if __name__ == '__main__':
    unittest.main(verbosity=2)
