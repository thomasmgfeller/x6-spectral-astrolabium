"""Regression checks for unified evidence, failure modes and local serving."""
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
import warnings
import zipfile

from tools.workflow import cli


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='x6-integration-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def spectral(self):
        folder = self.root / 'run'
        cli.run('spectral', folder, None, 30)
        return folder

    def rehash(self, folder):
        record = cli.read_json(folder / 'run.json')
        record['files'] = cli.inventory(folder, omit={'run.json'})
        (folder / 'run.json').write_bytes(cli.encoded(record))

    def test_spectral_export_replays_without_changing_run(self):
        folder = self.spectral()
        before = cli.inventory(folder)
        archive = self.root / 'export.zip'
        self.assertEqual(cli.export(folder, archive)['status'], 'EXPORTED')
        result = cli.verify(archive, 30)
        self.assertEqual(result['status'], 'REPLAY_PASS')
        self.assertEqual(result['scientific_result']['result'], {'passed': 5, 'total': 5})
        self.assertEqual(before, cli.inventory(folder))

    def test_existing_output_and_archive_are_not_overwritten(self):
        folder = self.spectral()
        before = cli.inventory(folder)
        with self.assertRaises(FileExistsError):
            cli.run('spectral', folder, None, 30)
        archive = self.root / 'export.zip'
        cli.export(folder, archive)
        data = archive.read_bytes()
        with self.assertRaises(FileExistsError):
            cli.export(folder, archive)
        self.assertEqual(data, archive.read_bytes())
        self.assertEqual(before, cli.inventory(folder))

    def test_missing_completion_extra_file_and_digest_tamper_rejected(self):
        folder = self.spectral()
        (folder / 'run.json').rename(folder / 'saved.json')
        with self.assertRaises(FileNotFoundError):
            cli.verify(folder, 30)
        (folder / 'saved.json').rename(folder / 'run.json')
        (folder / 'unexpected.txt').write_text('extra')
        with self.assertRaisesRegex(ValueError, 'inventory'):
            cli.verify(folder, 30)
        (folder / 'unexpected.txt').unlink()
        with (folder / 'summary.json').open('a') as f:
            f.write(' ')
        with self.assertRaisesRegex(ValueError, 'inventory'):
            cli.verify(folder, 30)

    def test_rehashed_forged_summary_is_rejected_by_replay(self):
        folder = self.spectral()
        summary = cli.read_json(folder / 'summary.json')
        summary['scientific_result']['result']['passed'] = 500
        (folder / 'summary.json').write_bytes(cli.encoded(summary))
        self.rehash(folder)
        cli.check_integrity(folder)  # The digest alone cannot establish the claim.
        with self.assertRaises(ValueError):
            cli.verify(folder, 30)

    def test_rehashed_native_rational_result_is_rejected(self):
        folder = self.spectral()
        path = folder / 'native/spectral/python_results.local.json'
        data = cli.read_json(path)
        data['results'][0]['upper'] = '999'
        path.write_bytes(cli.encoded(data))
        self.rehash(folder)
        with self.assertRaisesRegex(ValueError, 'Spectral result mismatch'):
            cli.verify(folder, 30)

    def test_signal_csv_is_checked_against_native_replay(self):
        folder = self.root / 'signal'
        cli.run('signal', folder, None, 30)
        self.assertEqual(cli.verify(folder, 30)['status'], 'REPLAY_PASS')
        csv = folder / 'native/signal/samples.csv'
        csv.write_text(csv.read_text().replace('index,time_s', 'changed,time_s', 1))
        self.rehash(folder)
        with self.assertRaisesRegex(RuntimeError, 'CSV differs'):
            cli.verify(folder, 30)

    def test_native_signal_import_preserves_bytes_and_replays(self):
        source = self.root / 'signal'
        cli.run('signal', source, None, 30)
        evidence = source / 'native/signal/evidence.json'
        imported = self.root / 'imported'
        cli.run('signal', imported, None, 30, imported=evidence)
        self.assertEqual(evidence.read_bytes(), (imported / 'native/signal/evidence.json').read_bytes())
        self.assertEqual(cli.read_json(imported / 'run.json')['operation'], 'IMPORT_SIGNAL')
        self.assertEqual(cli.verify(imported, 30)['status'], 'REPLAY_PASS')

    def test_invalid_signal_job_preserves_failure_without_completion(self):
        folder = self.root / 'invalid'
        job = cli.ROOT / 'experimental/edge_reference/examples/invalid-job.json'
        with self.assertRaises(RuntimeError):
            cli.run('signal', folder, job, 30)
        self.assertFalse((folder / 'run.json').exists())
        self.assertEqual(cli.read_json(folder / 'failure.json')['status'], 'FAILED')
        with self.assertRaises(FileNotFoundError):
            cli.verify(folder, 30)

    def test_source_revision_mismatch_is_not_silently_replayed(self):
        folder = self.spectral()
        record = cli.read_json(folder / 'run.json')
        record['sources']['tests/python/independent_audit.py'] = '0' * 64
        (folder / 'run.json').write_bytes(cli.encoded(record))
        with self.assertRaisesRegex(ValueError, 'Source revision'):
            cli.verify(folder, 30)

    def test_zip_traversal_duplicate_and_symlink_are_rejected(self):
        for case in ['traversal', 'duplicate', 'symlink']:
            with self.subTest(case=case):
                archive = self.root / (case + '.zip')
                with warnings.catch_warnings(), zipfile.ZipFile(archive, 'w') as z:
                    warnings.simplefilter('ignore', UserWarning)
                    if case == 'traversal':
                        z.writestr('../outside', 'bad')
                    elif case == 'duplicate':
                        z.writestr('same', 'a')
                        z.writestr('same', 'b')
                    else:
                        item = zipfile.ZipInfo('link')
                        item.create_system = 3
                        item.external_attr = 0o120777 << 16
                        z.writestr(item, '../outside')
                with self.assertRaises(ValueError):
                    cli.extract(archive, self.root / case)
        self.assertFalse((self.root / 'outside').exists())

    def test_symlink_and_incomplete_exports_are_not_accepted(self):
        folder = self.spectral()
        (folder / 'linked').symlink_to(folder / 'summary.json')
        with self.assertRaises(ValueError):
            cli.export(folder, self.root / 'bad.zip')
        self.assertFalse((self.root / 'bad.zip').exists())

    def test_local_server_serves_both_apps_and_denies_internal_files(self):
        server = cli.ThreadingHTTPServer(('127.0.0.1', 0), cli.LocalHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f'http://127.0.0.1:{server.server_port}'
            for path, fragment in [('/', b'Lokaler Einstieg'), ('/app/index.html', b'tab-signal'), ('/app/signal-lab.html', b'Signal')]:
                with urllib.request.urlopen(base + path) as r:
                    self.assertEqual(r.status, 200)
                    self.assertIn(fragment, r.read())
            for path in ['/.git/config', '/.venv/pyvenv.cfg', '/tools/workflow/cli.py', '/app/../README.md']:
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(base + path)
                self.assertEqual(error.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == '__main__':
    unittest.main()
