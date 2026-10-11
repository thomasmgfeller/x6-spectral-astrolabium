import json
from pathlib import Path
import struct
import unittest
import zlib
from frame_codec import decode_frame,decode_stream,FrameError,FRAME_BYTES
from analyze import analyze,InvalidRecord
ROOT=Path(__file__).resolve().parents[1]
class FrameTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=(ROOT/"examples/synthetic_chsh_capture.bin").read_bytes()
        cls.frame=cls.data[:FRAME_BYTES]
    def test_rtl_uart_frame(self):
        result=decode_stream(self.data,origin="synthetic",expected_first_sequence=100)
        self.assertEqual(len(result["records"]),4)
        self.assertEqual(analyze(result["records"])["physical_quantum_claim"],"NOT_ASSESSED")
    def test_all_single_bit_corruptions(self):
        for bit in range(FRAME_BYTES*8):
            b=bytearray(self.frame);b[bit//8]^=1<<(bit%8)
            with self.subTest(bit=bit):
                with self.assertRaises(FrameError):decode_frame(b,origin="synthetic")
    def test_missing_duplicated_reordered(self):
        for b in (self.data[FRAME_BYTES:],self.frame+self.data,
                  self.data[FRAME_BYTES:2*FRAME_BYTES]+self.frame+self.data[2*FRAME_BYTES:]):
            with self.assertRaises(FrameError):decode_stream(b,origin="synthetic",expected_first_sequence=100)
    def test_truncation_and_garbage(self):
        for b in (b'',self.data[:-1],b'X'+self.data,self.data+b'X'):
            with self.assertRaises(FrameError):decode_stream(b,origin="synthetic",expected_first_sequence=100)
    def test_crc_does_not_replace_semantic_checks(self):
        b=bytearray(self.frame);struct.pack_into('<Q',b,48+16*8,0)
        struct.pack_into('<I',b,240,zlib.crc32(b[:240]))
        record=decode_frame(b,origin="synthetic")
        records=decode_stream(self.data,origin="synthetic",expected_first_sequence=100)["records"]
        records[0]=record
        with self.assertRaises(InvalidRecord):analyze(records)
    def test_version_and_reserved_even_with_recomputed_crc(self):
        for offset in (0,8,9,11):
            b=bytearray(self.frame);b[offset]=255
            struct.pack_into('<I',b,240,zlib.crc32(b[:240]))
            with self.assertRaises(FrameError):decode_frame(b,origin="synthetic")
    def test_loss_flag_survives_transport(self):
        b=(ROOT/"validation/source_loss.frame.bin").read_bytes()
        r=decode_frame(b,origin="synthetic")
        self.assertEqual(r["flags"],4)

if __name__=="__main__":unittest.main(verbosity=2)
