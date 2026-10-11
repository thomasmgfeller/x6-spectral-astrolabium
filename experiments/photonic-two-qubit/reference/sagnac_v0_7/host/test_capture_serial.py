import os
from pathlib import Path
import threading
import time
import unittest
from capture_serial import capture
from frame_codec import decode_stream
ROOT=Path(__file__).resolve().parents[1]
class CaptureTests(unittest.TestCase):
    def exercise(self,data,frames,timeout):
        master,slave=os.openpty();name=os.ttyname(slave)
        def writer():
            time.sleep(0.05)
            for pos in range(0,len(data),17):
                os.write(master,data[pos:pos+17]);time.sleep(0.0002)
        worker=threading.Thread(target=writer);worker.start()
        try:return capture(name,frames,115200,timeout)
        finally:worker.join();os.close(master);os.close(slave)
    def test_chunked_pseudoterminal_capture(self):
        data=(ROOT/"examples/synthetic_chsh_capture.bin").read_bytes()
        got,error=self.exercise(data,4,2)
        self.assertIsNone(error);self.assertEqual(got,data)
        self.assertEqual(len(decode_stream(got,origin="synthetic",expected_first_sequence=100)["records"]),4)
    def test_partial_capture_is_retained(self):
        data=b'partial'
        got,error=self.exercise(data,1,0.2)
        self.assertEqual(got,data);self.assertIsNotNone(error)

if __name__=="__main__":unittest.main(verbosity=2)
