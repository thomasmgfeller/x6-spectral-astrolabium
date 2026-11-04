import base64
import hashlib
from http.client import HTTPConnection
import json
import os
from pathlib import Path
import pty
import struct
import tempfile
import threading
import time
import unittest
from unittest.mock import Mock, patch
import uuid
import zlib
from http.server import ThreadingHTTPServer

from drivers import BASE, capture_tags, digest, segment_plan, set_axes, shutter
from labor_server import Bench, Conflict, Handler, validate_config

RAW=(BASE/"examples/synthetic_chsh_capture.bin").read_bytes()
CAL=b"lab calibration test only"
CFG=dict(operator="Test",label="Integration",frames=4,first_sequence="100",timeout_s=2,seconds=1,
         local_ready=True, mode="fixed",calibration_sha256=hashlib.sha256(CAL).hexdigest())

class Case(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
    def bench(self,p=None):
        b=Bench(self.temp.name,p or {"source":"example"})
        self.addCleanup(b.close)
        return b
    def request(self,b,action,**more):
        return dict(action=action,run_id=b.state["run_id"],request_id=uuid.uuid4().hex,**more)
    def arm(self,b,**changes):
        return b.command(self.request(b,"arm",config=CFG|changes,calibration_b64=base64.b64encode(CAL).decode()))
    def start(self,b):
        return b.command(self.request(b,"start"))
    def until(self,check):
        start=time.monotonic()
        while not check():
            if time.monotonic()-start>5:self.fail("Zeitlimit")
            time.sleep(.006)
    def serial(self):
        master,slave=pty.openpty()
        self.addCleanup(os.close,master); self.addCleanup(os.close,slave)
        return master,os.ttyname(slave)
    def opened(self,raw,**changes):
        master,path=self.serial()
        b=self.bench({"source":"sagnac","port":path,"baud":1000000})
        self.arm(b,**changes);self.start(b)
        self.until(lambda:b.status()["run"]["source_open"])
        if raw: os.write(master,raw)
        return b
    def final(self,b):
        b.thread.join(5)
        self.assertFalse(b.thread.is_alive())
        return json.loads((b.folder/"manifest.json").read_text())
    def test_fixture_replay_and_seal(self):
        b=self.bench();self.arm(b);self.start(b);m=self.final(b)
        self.assertEqual(b.state["state"],"COMPLETE")
        self.assertEqual(m["files"]["capture.bin"]["sha256"],hashlib.sha256(RAW).hexdigest())
        self.assertEqual(b.state["origin"],"synthetic");self.assertEqual(b.state["last_sequence"],"103")
    def test_real_serial_path_via_pty(self):
        b=self.opened(RAW); m=self.final(b)
        self.assertEqual(m["final"]["frames"],4)
        self.assertEqual((b.folder/"capture.bin").read_bytes(),RAW)
        self.assertEqual((b.folder/"calibration.original").read_bytes(),CAL)
    def test_corrupt_crc_preserves_raw(self):
        bad=bytes([RAW[0]^1])+RAW[1:244]
        b=self.opened(bad);m=self.final(b)
        self.assertIn("CRC",m["final"]["reason"])
        self.assertEqual((b.folder/"capture.bin").read_bytes(),bad)
    def test_sequence_gap(self):
        b=self.opened(RAW[244:488]); m=self.final(b)
        self.assertEqual(m["final"]["state"],"ERROR");self.assertIn("reordered",m["final"]["reason"])
    def test_flags_latched(self):
        raw=bytearray(RAW[:244]);raw[10]=4;struct.pack_into("<I",raw,240,zlib.crc32(raw[:240]))
        b=self.opened(raw);self.final(b)
        self.assertEqual(b.state["flags"],4);self.assertIn("source_loss",b.state["reason"])
    def test_truncated_timeout(self):
        b=self.opened(RAW[:31],timeout_s=1);m=self.final(b)
        self.assertEqual(m["final"]["state"],"ERROR");self.assertEqual(m["files"]["capture.bin"]["bytes"],31)
    def test_stop_aborts_partial_capture(self):
        b=self.opened(RAW[:30]);self.until(lambda:b.status()["run"]["bytes_received"]==30)
        b.command(self.request(b,"abort"));m=self.final(b)
        self.assertEqual(m["final"]["state"],"ABORTED");self.assertEqual(m["files"]["capture.bin"]["bytes"],30)
    def test_retries_concurrent_starts_and_stale_run(self):
        master,path=self.serial();b=self.bench({"source":"sagnac","port":path,"baud":1000000})
        self.arm(b);req=self.request(b,"start");out=[]
        def post():out.append(b.command(req))
        threads=[threading.Thread(target=post) for _ in range(2)]
        for t in threads:t.start()
        for t in threads:t.join()
        self.assertEqual(out[0],out[1])
        with self.assertRaises(Conflict):b.command(self.request(b,"abort")|{"run_id":"00"*16})
        b.command(self.request(b,"stop"));self.assertEqual(self.final(b)["final"]["state"],"STOPPED")
    def test_disk_reserve_and_config_guard(self):
        b=self.bench()
        with patch("labor_server.shutil.disk_usage",return_value=Mock(free=0)),self.assertRaises(OSError):self.arm(b)
        self.arm(b);(b.folder/"config.json").write_text("{}")
        with self.assertRaises(Conflict):self.start(b)
    def test_calibration_and_range(self):
        master,path=self.serial();b=self.bench({"source":"sagnac","port":path,"baud":1000000})
        with self.assertRaises(ValueError):self.arm(b,calibration_sha256="0"*64)
        with self.assertRaises(ValueError):self.arm(b,first_sequence=str(2**64-1))
        self.assertEqual(b.state["state"],"IDLE")
    def test_recovery_lock_and_hash(self):
        d=Path(self.temp.name)/("a"*32);d.mkdir();(d/"capture.bin").write_bytes(b"part")
        (d/"manifest.json.tmp").write_text("partial")
        (d/"config.json.tmp").write_text("partial-config")
        b=self.bench();self.assertEqual(json.loads((d/"manifest.json").read_bytes())["final"]["state"],"INTERRUPTED")
        import verify_run
        self.assertEqual(verify_run.verify(d)["files_verified"],3)
        with self.assertRaises(BlockingIOError):Bench(self.temp.name,{"source":"example"})
    def test_schedule_contract(self):
        p=segment_plan("schedule",1);self.assertEqual(len(p),80);self.assertEqual(sum(s[1] for s in p),2400)
        for i in range(0,80,4):self.assertEqual({s[0] for s in p[i:i+4]},{"00","01","10","11"})
        with self.assertRaises(ValueError):validate_config({"source":"swabian"},CFG|{"mode":"schedule"})
    def tagger(self):
        sdk=Mock();tag=sdk.createTimeTagger.return_value
        tag.getModel.return_value="Time Tagger Ultra";tag.getSerial.return_value="ABC123"
        tag.getTestSignal.return_value=False;tag.getEventDivider.return_value=1;tag.getOverflows.return_value=0
        tag.getTriggerLevel.return_value=.5;tag.getConfiguration.return_value={"source":"mock"}
        sdk.Countrate.return_value.getData.return_value=[1.,1.,1.,0.]
        sdk.Countrate.return_value.getCountsTotal.return_value=[1,1,1,0]
        grp=sdk.SynchronizedMeasurements.return_value
        grp.isRunning.side_effect=[True,False]
        writer=Mock();writer.getTotalEvents.return_value=3
        def filewriter(tagger,path,channels):
            Path(path).write_bytes(b"TEST DOUBLE ONLY");return writer
        sdk.FileWriter.side_effect=filewriter
        return sdk,tag,grp
    def test_sdk_segment_contract(self):
        sdk,tag,g=self.tagger();folder=Path(self.temp.name)
        capture_tags(dict(serial="ABC123",trigger_v=[.5]*4),CFG,folder,lambda:None,Mock(),sdk)
        self.assertTrue(json.loads((folder/"segment-001.json").read_text())["complete"])
        g.startFor.assert_called_once_with(10**12);g.stop.assert_called_once();sdk.freeTimeTagger.assert_called_once_with(tag)
    def test_sdk_overflow_and_cleanup(self):
        sdk,tag,g=self.tagger();tag.getOverflows.side_effect=[0,1]
        with self.assertRaisesRegex(ValueError,"Überlauf"):capture_tags(dict(serial="ABC123",trigger_v=[.5]*4),CFG,Path(self.temp.name),lambda:None,Mock(),sdk)
        self.assertFalse(json.loads((Path(self.temp.name)/"segment-001.json").read_text())["complete"])
        g.stop.assert_called();sdk.freeTimeTagger.assert_called_once()
    def test_ell14_protocol_pty(self):
        info=b"0E1234567820260101016800040000"
        self.assertEqual(len(info),30)
        master,path=self.serial();cmds=[]
        def instrument():
            for cmdlen,reply in [(3,b"0IN"+info),(11,b"0PO00002000"),(3,b"0PO00002000")]:
                cmd=b""
                while len(cmd)<cmdlen:cmd+=os.read(master,cmdlen-len(cmd))
                cmds.append(cmd);os.write(master,reply+b"\r\n")
        thread=threading.Thread(target=instrument,daemon=True);thread.start()
        axis=dict(port=path,address="0",serial="12345678",zero_deg=11.25,direction=1,tolerance_deg=.1)
        # The second arm is deliberately misidentified; the first move must have received a separate position reply.
        samples=[]
        def check():
            if samples:raise InterruptedError("stop")
        with self.assertRaises(InterruptedError):set_axes([axis,axis],"00",check,lambda **x:samples.append(x))
        thread.join(1);self.assertEqual(cmds,[b"0in",b"0ma00002000",b"0gp"]);self.assertEqual(samples[0]["hwp_readback"][0]["readback_deg"],11.25)
    def test_shutter_output_readback(self):
        master,path=self.serial();seen=[]
        def instrument():
            idata=struct.pack("<I",68000001)+b"KSC101\0\0"+bytes(72)
            for reply in [struct.pack("<HHBB",6,len(idata),0x81,0x50)+idata,bytes.fromhex("CD 04 01 02 01 50")]:
                seen.append(os.read(master,6));os.write(master,reply)
        thread=threading.Thread(target=instrument,daemon=True);thread.start()
        z=shutter(dict(port=path,serial="68000001"));thread.join(1)
        self.assertEqual((z["solenoid"],z["blade"]),("OFF","UNKNOWN"))
        self.assertEqual(seen,[bytes.fromhex("05 00 00 00 50 01"),bytes.fromhex("CC 04 01 00 50 01")])
    def test_shutter_deactivate_requires_confirmed_output(self):
        master,path=self.serial();seen=[]
        def instrument():
            idata=struct.pack("<I",68000001)+b"KSC101\0\0"+bytes(72)
            seen.append(os.read(master,6))
            os.write(master,struct.pack("<HHBB",6,len(idata),0x81,0x50)+idata)
            for _ in range(2):seen.append(os.read(master,6))
            os.write(master,bytes.fromhex("CD 04 01 01 01 50"))
        thread=threading.Thread(target=instrument,daemon=True);thread.start()
        with self.assertRaisesRegex(ValueError,"bestätigt"):
            shutter(dict(port=path,serial="68000001"),deactivate=True)
        thread.join(1);self.assertEqual(seen[1:],list(map(bytes.fromhex,["CB 04 01 02 50 01","CC 04 01 00 50 01"])))
    def test_independent_archive_verifier(self):
        import verify_run
        b=self.bench();self.arm(b);self.start(b);self.final(b)
        self.assertEqual(verify_run.verify(b.folder)["run_state"],"COMPLETE")
        (b.folder/"capture.bin").write_bytes(RAW[:-1])
        with self.assertRaises(ValueError):verify_run.verify(b.folder)
    def test_http_full_flow(self):
        b=self.bench();srv=ThreadingHTTPServer(("127.0.0.1",0),Handler)
        self.addCleanup(srv.server_close);threading.Thread(target=srv.serve_forever,daemon=True).start();self.addCleanup(srv.shutdown)
        srv.bench=b;srv.origin=f"http://127.0.0.1:{srv.server_port}";srv.token="TEST";srv.session=uuid.uuid4().hex
        cookie={}
        def http(path,body=None,**headers):
            conn=HTTPConnection("127.0.0.1",srv.server_port,timeout=5)
            hdr={"Origin":srv.origin,"Content-Type":"application/json"}|cookie|headers
            try:
                conn.request("GET" if body is None else "POST",path,None if body is None else json.dumps(body),hdr)
                r=conn.getresponse()
                if r.getheader("Set-Cookie"): cookie["Cookie"]=r.getheader("Set-Cookie").split(";")[0]
                return r.status,r.read()
            finally:conn.close()
        self.assertEqual(http("/api/status")[0],401)
        self.assertEqual(http("/api/login",{"token":"TEST"},Origin="https://other.invalid")[0],403)
        self.assertEqual(http("/api/login",{"token":"bad"})[0],401)
        self.assertEqual(http("/api/login",{"token":"TEST"})[0],200)
        self.assertEqual(http("/api/status",Host="bogus.example")[0],403)
        self.assertEqual(json.loads(http("/api/status")[1])["api"],"x6.bench.v1")
        self.assertEqual(http("/api/command",self.request(b,"arm",config=CFG))[0],200)
        self.assertEqual(http("/api/command",self.request(b,"start"))[0],200);self.final(b)
        self.assertEqual(json.loads(http("/api/archive")[1])[0]["id"],b.folder.name)
        self.assertEqual(http("/api/files/"+b.folder.name+"/capture.bin"),(200,RAW))
        self.assertEqual(http("/api/files/"+b.folder.name+"/..")[0],404)
if __name__=="__main__":unittest.main()
