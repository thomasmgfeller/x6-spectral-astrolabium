"""Host regressions, independent binary oracles and corruption checks. Apache-2.0."""
import copy
import json
import os
from pathlib import Path
import pty
import shutil
import struct
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
import zlib

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from experimental.control_channel import channel as c, reference as r, cli


class ChannelTests(unittest.TestCase):
    def setUp(self):
        self.plan=c.read_json(cli.EXAMPLE)

    def test_independent_plan_reader(self):
        data=c.compile_plan(self.plan)
        duration,points=r.read_compiled(data)
        self.assertEqual(duration,1200)
        self.assertEqual(points,[(0,0),(200,819),(400,1638),(600,2457),(800,3276),(1000,0)])
        self.assertEqual(data[:16].hex(),'b0040000060000000000000000000000')

    def test_strict_units_types_and_limits(self):
        for value in [True,False,1.0,float('nan'),float('inf'),-1,5001,2**64]:
            plan=copy.deepcopy(self.plan);plan['duration_ms']=value
            with self.subTest(value=value),self.assertRaises(ValueError):c.compile_plan(plan)
        for key,value in [('profile','volts'),('extra',0)]:
            plan=copy.deepcopy(self.plan);plan[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):c.compile_plan(plan)
        for code in [-1,3277,True,1.1]:
            plan=copy.deepcopy(self.plan);plan['points'][1]['dac_code']=code
            with self.subTest(code=code),self.assertRaises(ValueError):c.compile_plan(plan)

    def test_point_order_capacity_and_spacing(self):
        for points in [[],[{'at_ms':i*10,'dac_code':0} for i in range(65)],
                       [{'at_ms':1,'dac_code':0}], [{'at_ms':0,'dac_code':0},{'at_ms':9,'dac_code':1}],
                       [{'at_ms':0,'dac_code':0},{'at_ms':1191,'dac_code':1}]]:
            plan=copy.deepcopy(self.plan);plan['points']=points
            with self.subTest(points=len(points)),self.assertRaises(ValueError):c.compile_plan(plan)

    def test_duplicate_json_and_nonfinite_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'input.json'
            for data in ['{"a":1,"a":2}','{"a":NaN}','{"a":Infinity}']:
                path.write_text(data)
                with self.assertRaises(ValueError):c.read_json(path)

    def test_truncated_or_extended_compiled_rejected(self):
        data=c.compile_plan(self.plan)
        for bad in [data[:-1],data[:-8],data+b'\0'*8,b'']:
            with self.assertRaises(ValueError):r.read_compiled(bad)

    def test_complete_payload_protected_beyond_256_bytes(self):
        plan=copy.deepcopy(self.plan);plan['points']=[{'at_ms':i*10,'dac_code':i} for i in range(64)]
        data=c.compile_plan(plan);mutated=bytearray(data);mutated[404]^=1
        self.assertNotEqual(zlib.crc32(data),zlib.crc32(mutated))
        self.assertNotEqual(r.read_compiled(data),r.read_compiled(mutated))

    def test_model_output_requires_order_and_timing(self):
        data=c.compile_plan(self.plan)
        events=[{'model_ms':0,'code':0,'enabled':False} for _ in range(2)]
        events += [{'model_ms':t,'code':code,'enabled':True} for t,code in r.read_compiled(data)[1]]
        events += [{'model_ms':1200,'code':0,'enabled':False}]
        self.assertEqual(r.model_oracle(data,events)['status'],'PASS')
        for index,field,value in [(3,'code',818),(3,'model_ms',221),(8,'enabled',True)]:
            bad=copy.deepcopy(events);bad[index][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):r.model_oracle(data,bad)

    def test_golden_request_frame(self):
        data=c.packet(c.OPEN,17,0,c.PROFILE)
        self.assertEqual(data[:16].hex(),'41435631010000001100000000000000')
        # Independent polynomial implementation against Python's CRC primitive.
        crc=0xffffffff
        for byte in data[:44]:
            crc^=byte
            for _ in range(8):crc=(crc>>1)^(0xedb88320 if crc&1 else 0)
        self.assertEqual((crc^0xffffffff).to_bytes(4,'little'),data[44:])

    def test_unsafe_plan_never_opens_port(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'plan.json';plan=copy.deepcopy(self.plan);plan['points'][0]['dac_code']=9999;path.write_bytes(c.json_bytes(plan))
            with patch.object(c,'Transport') as transport,self.assertRaises(ValueError):c.run(path,'/dev/not-real',Path(d)/'out','HARDWARE_DECLARED')
            transport.assert_not_called()

    def test_lost_ack_retries_identical_frame(self):
        class Transport:
            def __init__(self):self.writes=[];self.calls=0
            def write(self,data):self.writes.append(data)
            def read(self,timeout):
                self.calls+=1
                if self.calls==1:raise TimeoutError()
                request=self.writes[-1]
                data=c.WIRE.pack(b'ACV1',c.OPEN,1,2,int.from_bytes(request[8:12],'little'),0,0,0,0,0,0,0,c.PROFILE)
                return data+struct.pack('<I',zlib.crc32(data))
        transport=Transport();client=c.Client(transport,'MODEL');reply=client.command(c.OPEN,c.PROFILE)
        self.assertTrue(reply['replayed']);self.assertEqual(transport.writes[0],transport.writes[1]);self.assertEqual(client.seq,1)

    def test_hardware_claim_rejected_for_model_reply(self):
        class Transport:
            def write(self,data):self.data=data
            def read(self,timeout):
                data=c.WIRE.pack(b'ACV1',c.OPEN,1,0,int.from_bytes(self.data[8:12],'little'),0,0,0,0,0,0,0,c.PROFILE)
                return data+struct.pack('<I',zlib.crc32(data))
        with self.assertRaisesRegex(ValueError,'Endpoint class'):c.Client(Transport(),'HARDWARE_DECLARED').command(c.OPEN,c.PROFILE)


class SerialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory();cls.binary=cli.build_native(cls.temp.name)

    @classmethod
    def tearDownClass(cls):cls.temp.cleanup()

    def setUp(self):
        self.event_file=tempfile.TemporaryFile(mode='w+')
        master,self.slave=pty.openpty()
        self.proc=subprocess.Popen([str(self.binary)],stdin=master,stdout=master,stderr=self.event_file,close_fds=True)
        os.close(master)
        self.transport=c.Transport(os.ttyname(self.slave))
        self.client=c.Client(self.transport,'MODEL')
        self.plan={'schema':'acvm.channel.plan/1','profile':c.PROFILE_NAME,'duration_ms':2000,
                   'points':[{'at_ms':0,'dac_code':1000}]}

    def tearDown(self):
        if self.transport:self.transport.close()
        if self.proc.poll() is None:self.proc.terminate()
        self.proc.wait(timeout=2)
        if self.slave is not None:os.close(self.slave)
        self.event_file.close()

    def test_lost_start_ack_over_real_pty(self):
        self.client.load(self.plan)
        packet=c.packet(c.START,self.client.session,self.client.seq)
        self.transport.write(packet)
        first=c.decode(self.transport.read())  # deliberately discard ACK
        self.transport.write(packet)
        second=c.decode(self.transport.read())
        self.assertEqual(first['run_counter'],1);self.assertEqual(second['run_counter'],1)
        self.assertTrue(second['replayed']);self.assertEqual(second['state'],'RUNNING')
        self.client.seq+=1;self.client.stop()

    def test_missing_heartbeat_returns_to_zero(self):
        self.client.load(self.plan);self.client.command(c.START)
        time.sleep(0.55)
        with self.assertRaisesRegex(RuntimeError,'LEASE'):self.client.command(c.POLL)
        self.assertEqual(self.client.last['state'],'FAULT')
        self.assertEqual(self.client.last['commanded_dac_code'],0)
        self.event_file.seek(0);events=[json.loads(x) for x in self.event_file.readlines()]
        self.assertFalse(events[-1]['enabled']);self.assertEqual(events[-1]['code'],0)
        self.assertGreaterEqual(events[-1]['model_ms']-events[-2]['model_ms'],500)

    def test_serial_disconnect_leaves_device_lease_running(self):
        self.client.load(self.plan);self.client.command(c.START)
        self.transport.close();self.transport=None
        os.close(self.slave);self.slave=None
        self.proc.wait(timeout=2)
        self.assertEqual(self.proc.returncode,0)
        self.event_file.seek(0);events=[json.loads(x) for x in self.event_file.readlines()]
        self.assertEqual(events[-1]['code'],0);self.assertFalse(events[-1]['enabled'])
        self.assertGreaterEqual(events[-1]['model_ms']-events[-2]['model_ms'],500)

    def test_corrupt_packet_causes_fault_and_zero(self):
        self.client.load(self.plan);self.client.command(c.START)
        bad=bytearray(c.packet(c.POLL,self.client.session,self.client.seq));bad[24]^=1
        self.transport.write(bad)
        with self.assertRaises(TimeoutError):self.transport.read(0.1)
        with self.assertRaisesRegex(RuntimeError,'FORMAT'):self.client.command(c.POLL)
        self.assertEqual(self.client.last['commanded_dac_code'],0)

    def test_byte_fragmentation_and_noise_resynchronization(self):
        self.transport.write(b'garbage')
        packet=c.packet(c.OPEN,self.client.session,0,c.PROFILE)
        for byte in packet:self.transport.write(bytes([byte]))
        reply=c.decode(self.transport.read())
        self.assertEqual(reply['state'],'IDLE');self.assertEqual(reply['session'],self.client.session)

    def test_stop_before_all_points_loaded(self):
        self.client.command(c.OPEN,c.PROFILE);self.client.command(c.BEGIN,2,1000,0)
        self.client.command(c.POINT,0,0,1000)
        response=self.client.stop()
        self.assertEqual(response['state'],'ABORTED');self.assertEqual(response['commanded_dac_code'],0)

    def test_reset_endpoint_does_not_resume(self):
        # A fresh firmware instance has session zero and refuses a previous session's START.
        self.transport.write(c.packet(c.START,123456,7))
        response=c.decode(self.transport.read())
        self.assertEqual(response['error'],'SESSION');self.assertEqual(response['run_counter'],0)
        self.assertEqual(response['commanded_dac_code'],0)


if __name__=='__main__':unittest.main(verbosity=2)
