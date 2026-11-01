"""Network-free tests. Origin is a local bare Git repository and all bytes synthetic."""
import hashlib
import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch

from agent import anu_qrng as anu


class AnuTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.archive = root / "archive"
        self.remote = root / "bare.git"
        self.git(root, "init", "-q", "--bare", self.remote)
        self.git(root, "init", "-q", "-b", "unborn", self.archive)
        self.git(self.archive, "remote", "add", "origin", self.remote)
        self.git(self.archive, "config", "user.email", "test@example.invalid")
        self.git(self.archive, "config", "user.name", "Offline Test")
        self.now = datetime(2026, 11, 1, 12, tzinfo=timezone.utc)
        self.fetch = Mock(return_value=bytes(range(256)) * 4)

    def git(self, cwd, *args):
        return subprocess.run(["git", "-C", cwd, *args], check=True, capture_output=True,
                              text=True).stdout

    def collect(self, key="offline-dummy", reviewed="2026-11-01"):
        return anu.collect(self.archive, key, reviewed, clock=lambda: self.now, fetch=self.fetch)

    def test_archive_publication_and_same_week_replay(self):
        self.assertTrue(self.collect())
        self.assertFalse(self.collect())
        self.fetch.assert_called_once()
        get = lambda path: self.git(self.remote, "show", "anu-qrng-data:" + path)
        record = json.loads(get("latest.json"))
        self.assertEqual(record["sha256"], hashlib.sha256(self.fetch.return_value).hexdigest())
        self.assertEqual(bytes.fromhex(record["data_hex"]), self.fetch.return_value)
        self.assertEqual(get("latest.json"), get("2026-11-01.json"))
        self.assertNotIn("offline-dummy", get("latest.json") + get("last-attempt.json"))
        self.now += timedelta(days=1)
        self.assertTrue(self.collect())

    def test_failure_consumes_remote_slot_and_keeps_previous_success(self):
        self.collect()
        before = (self.archive / "latest.json").read_bytes()
        self.now += timedelta(days=1)
        self.fetch.side_effect = TimeoutError
        with self.assertRaises(TimeoutError):
            self.collect()
        self.assertFalse(self.collect())
        self.assertEqual(self.fetch.call_count, 2)
        self.assertEqual((self.archive / "latest.json").read_bytes(), before)
        reservation = self.git(self.remote, "show", "anu-qrng-data:last-attempt.json")
        self.assertEqual(json.loads(reservation)["reserved_at"], self.now.isoformat())

    def test_failed_reservation_cannot_trigger_download(self):
        self.git(self.archive, "remote", "set-url", "origin", self.remote.with_name("absent"))
        with self.assertRaises(subprocess.CalledProcessError):
            self.collect()
        self.fetch.assert_not_called()

    def test_terms_credentials_and_clock(self):
        for key, reviewed in [(None, "2026-11-01"), ("k", ""), ("k", "2026-08-03"),
                              ("k", "2026-11-02"), ("k", "invalid")]:
            with self.assertRaises(ValueError):
                self.collect(key, reviewed)
        self.fetch.assert_not_called()
        self.now = self.now.replace(hour=23, minute=59, second=55)
        self.collect()
        self.now += timedelta(seconds=10)
        self.assertFalse(self.collect())
        self.now -= timedelta(days=1)
        with self.assertRaises(ValueError):
            self.collect()
        self.fetch.assert_called_once()

    def test_payload_validation(self):
        good = {"data": list(self.fetch.return_value)}
        self.assertEqual(anu.parse_block(good), self.fetch.return_value)
        for bad in [None, {"data": []}, {**good, "success": False}, {**good, "length": 1024.0},
                    {**good, "type": "uint16"}, *({"data": [x] * 1024} for x in (True, -1, 256, 1.0))]:
            with self.assertRaises(ValueError):
                anu.parse_block(bad)

    @patch("agent.anu_qrng.http.client.HTTPSConnection")
    def test_transport_is_one_get_and_never_follows_redirect_or_retries(self, connection):
        for status in [200, 302, 403, 429, 500]:
            connection.reset_mock()
            reply = connection.return_value.getresponse.return_value
            reply.status = status
            reply.read.return_value = json.dumps({"data": list(self.fetch.return_value)}).encode()
            if status == 200:
                self.assertEqual(anu.download("fake"), self.fetch.return_value)
            else:
                with self.assertRaisesRegex(ValueError, str(status)):
                    anu.download("fake")
                reply.read.assert_not_called()
            connection.assert_called_once_with(anu.HOST, timeout=20)
            connection.return_value.request.assert_called_once_with(
                "GET", anu.QUERY, headers={"x-api-key": "fake", "Accept": "application/json"})
            connection.return_value.close.assert_called_once()
        reply.status = 200
        reply.read.return_value = b"x" * 16385
        with self.assertRaisesRegex(ValueError, "exceeds"):
            anu.download("fake")
