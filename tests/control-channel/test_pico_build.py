"""Reject malformed candidate artifacts and preserve earlier build output."""
import importlib.util
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('build_c1',ROOT/'tools/build_c1_pico.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
CANDIDATE=ROOT/'docs/acvm/c1-e01-target-build/firmware'


class BuildArtifactTests(unittest.TestCase):
    def test_real_candidate_matches_binary(self):
        self.assertEqual(builder.uf2_check(CANDIDATE/'acvm_channel.uf2',CANDIDATE/'acvm_channel.bin')['blocks'],111)

    def test_corruption_controls(self):
        original=(CANDIDATE/'acvm_channel.uf2').read_bytes()
        for label,mutate in [
            ('wrong-family',lambda b:b.__setitem__(slice(28,32),struct.pack('<I',0))),
            ('out-of-flash',lambda b:b.__setitem__(slice(12,16),struct.pack('<I',0x20000000))),
            ('duplicate-block',lambda b:b.__setitem__(slice(512,1024),b[:512])),
            ('changed-payload',lambda b:b.__setitem__(40,b[40]^1)),
            ('truncated',lambda b:b.pop())]:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as d:
                data=bytearray(original);mutate(data);p=Path(d)/'bad.uf2';p.write_bytes(data)
                with self.assertRaises(ValueError):builder.uf2_check(p,CANDIDATE/'acvm_channel.bin')

    def test_existing_output_untouched(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'prior';out.mkdir();sentinel=out/'evidence';sentinel.write_bytes(b'keep')
            command=[sys.executable,'-B',str(ROOT/'tools/build_c1_pico.py'),'--sdk',d,
                     '--picotool-dir',d,'--output',str(out)]
            p=subprocess.run(command,capture_output=True,text=True)
            self.assertEqual(p.returncode,1)
            self.assertIn('Output must be new',p.stderr)
            self.assertEqual(list(out.iterdir()),[sentinel]);self.assertEqual(sentinel.read_bytes(),b'keep')


if __name__=='__main__':unittest.main(verbosity=2)
