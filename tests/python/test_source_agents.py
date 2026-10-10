"""Source semantics, corruption rejection and failure evidence, without network."""
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import h5py
import numpy as np

from agent.atlas_checks import atlas_cases
from agent.measurement_sources import normalized, nasa_window, qutech_windows, valid_nasa_cache
from agent.run_sources import main
from agent.source_transport import download, read_zip_member


class SourceTests(unittest.TestCase):
    def test_complete_atlas_and_scopes(self):
        cases = list(atlas_cases())
        self.assertEqual(len(cases), 1253)
        self.assertEqual(sum(c['connected'] for c in cases), 995)
        self.assertEqual(cases[0]['nodes'], 0)
        self.assertEqual(cases[1]['source'], 'v0')
        # Isolated vertices must not vanish from disconnected graph input.
        for c in cases:
            if not c['connected']:
                for i in range(c['nodes']):
                    self.assertIn(f'v{i}', c['source'].splitlines())

    def test_normalization_rejects_missing_constant_wrong_length(self):
        for values in [[1.0]*128, list(range(127)), [float('nan')]+list(range(127))]:
            with self.assertRaises(ValueError):
                normalized(values, {})

    def test_nasa_shape_and_window_alignment(self):
        matrix = np.arange(20480*4, dtype=float).reshape(20480, 4)
        stream = io.BytesIO()
        np.savetxt(stream, matrix)
        window = nasa_window(stream.getvalue(), 'fixture')
        self.assertEqual(window['original_values'], matrix[:1024, 0].tolist())
        self.assertEqual(window['axis_values'][-1], 1023/20000)
        self.assertIsNone(window['health_label'])
        for bad in [b'1 2 3 4\n', stream.getvalue().replace(b'0.000000000000000000e+00', b'nan', 1)]:
            with self.assertRaises(ValueError):
                nasa_window(bad, 'fixture')

    def test_qubit_axes_not_flattened_and_missing_values_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'q.hdf5'
            with h5py.File(path, 'w') as f:
                f.attrs.update(uuid=1730672289460108893, title='fixture', measurement_time='fixture')
                data = np.arange(200000, dtype=float).reshape(200, 1000)
                f.create_dataset('_m0', data=data).attrs['units'] = 'mV'
                f.create_dataset('repetition', data=np.arange(1000))
                f.create_dataset('wait_time', data=np.linspace(1000, 8000, 200)).attrs['units'] = 'ns'
            windows = qutech_windows(path)
            self.assertEqual([w['row'] for w in windows], [0, 99, 199])
            self.assertEqual(windows[1]['original_values'], data[99, :512].tolist())
            self.assertIsNone(windows[0]['sampling_rate_hz'])
            with h5py.File(path, 'r+') as f:
                f['_m0'][99, 2] = np.nan
            with self.assertRaises(ValueError):
                qutech_windows(path)

    def test_cache_missing_or_corrupt_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)
            self.assertFalse(valid_nasa_cache(path))
            from agent.measurement_sources import NASA_FILES, NASA_README
            for name in [*NASA_FILES, NASA_README]:
                (path/name).write_bytes(b'corrupt')
            self.assertFalse(valid_nasa_cache(path))

    def test_zip_member_range_and_tamper_rejection(self):
        import hashlib
        payload = bytes(range(256))*100
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('data/x.hdf5', payload)
            z.writestr('padding', bytes(range(256))*100)
            z.comment = b'x'*5000
        raw = buffer.getvalue()
        def mock_download(url, dest, limit, byte_range=None, **kwargs):
            if byte_range.startswith('-'):
                begin, end = max(0, len(raw)-int(byte_range[1:])), len(raw)-1
            else:
                begin, end = map(int, byte_range.split('-'))
            Path(dest).write_bytes(raw[begin:end+1])
            return {'content_range': f'bytes {begin}-{end}/{len(raw)}'}
        with tempfile.TemporaryDirectory() as d, patch('agent.source_transport.download', mock_download):
            dst = Path(d)/'out'
            read_zip_member('unused', 'data/x.hdf5', dst, d, hashlib.sha256(payload).hexdigest())
            self.assertEqual(dst.read_bytes(), payload)
            with self.assertRaises(ValueError):
                read_zip_member('unused', 'data/x.hdf5', dst, d, '0'*64)

    def test_range_ignored_by_server_is_rejected_without_full_download(self):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        opener = unittest.mock.MagicMock()
        opener.open.return_value = response
        with tempfile.TemporaryDirectory() as d, patch('agent.source_transport.urllib.request.build_opener', return_value=opener), patch('agent.source_transport.time.sleep'):
            with self.assertRaises(RuntimeError):
                download('https://zenodo.org/example', Path(d)/'download', 64, '0-63')
            response.read.assert_not_called()

    def test_failed_fetch_leaves_failed_report_and_nonzero_exit(self):
        with tempfile.TemporaryDirectory() as d, patch('agent.measurement_sources.fetch_qutech', side_effect=RuntimeError('fixture unavailable')):
            self.assertEqual(main(['--source', 'qutech', '--output', d]), 1)
            report = json.loads((Path(d)/'report.json').read_text())
            self.assertEqual(report['status'], 'FAIL')
            self.assertEqual(report['windows'], [])
            self.assertIn('fixture unavailable', report['error'])
            self.assertTrue((Path(d)/'SHA256.json').is_file())


if __name__ == '__main__':
    unittest.main()
