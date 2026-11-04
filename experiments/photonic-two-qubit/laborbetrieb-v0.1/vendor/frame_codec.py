#!/usr/bin/env python3
"""Strict snapshot transport decoding. No implicit resynchronization or CRC repair."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import zlib
from analyze import FORMAT

MAGIC=b"SGNCv007"
HEADER=struct.Struct("<8sBBBBIQQQQ")
PAYLOAD=struct.Struct("<24Q")
FRAME_BYTES=244

class FrameError(ValueError):pass

def decode_frame(frame, *, origin, expected_sequence=None):
    if origin not in ("synthetic","hardware"):raise FrameError("explicit origin required")
    if len(frame)!=FRAME_BYTES:raise FrameError("frame length mismatch")
    expected_crc=struct.unpack_from("<I",frame,240)[0]
    if zlib.crc32(frame[:240])!=expected_crc:raise FrameError("CRC32 mismatch")
    magic,version,setting,flags,reserved,cal,start,stop,width,seq=HEADER.unpack_from(frame)
    if magic!=MAGIC or version!=7 or reserved!=0:raise FrameError("unknown framing/version/reserved field")
    if setting>3:raise FrameError("invalid setting")
    if expected_sequence is not None and seq!=expected_sequence:raise FrameError("missing/repeated/reordered snapshot")
    counts=PAYLOAD.unpack_from(frame,HEADER.size)
    return {"format":FORMAT,"origin":origin,"complete":True,"setting_index":setting,
            "calibration_id":str(cal),"flags":flags,
            "configuration":{"start_ps":str(start),"stop_ps":str(stop),"window_ps":str(width)},
            "counters":[str(x) for x in counts],
            "transport":{"format":"SGNCv007","sequence":str(seq),"crc32":f"{expected_crc:08x}",
                         "frame_sha256":hashlib.sha256(frame).hexdigest()}}

def decode_stream(data, *, origin, expected_first_sequence):
    if not isinstance(expected_first_sequence,int) or isinstance(expected_first_sequence,bool) or not 0<=expected_first_sequence<1<<64:
        raise FrameError("valid explicit first sequence required")
    if not data or len(data)%FRAME_BYTES:raise FrameError("empty or truncated capture")
    records=[]
    for index,pos in enumerate(range(0,len(data),FRAME_BYTES)):
        seq=expected_first_sequence+index
        if seq>=1<<64:raise FrameError("sequence wrap prohibited")
        records.append(decode_frame(data[pos:pos+FRAME_BYTES],origin=origin,expected_sequence=seq))
    return {"format":"sagnac.capture.v0.7","records":records,
            "capture_sha256":hashlib.sha256(data).hexdigest()}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("input",type=Path);p.add_argument("--output",required=True,type=Path)
    p.add_argument("--origin",required=True,choices=("synthetic","hardware"))
    p.add_argument("--first-sequence",required=True,type=int)
    a=p.parse_args()
    try:
        result=decode_stream(a.input.read_bytes(),origin=a.origin,expected_first_sequence=a.first_sequence);code=0
    except (OSError,FrameError) as e:
        result={"transport":"INVALID","reason":str(e),"physical_quantum_claim":"NOT_ASSESSED"};code=2
    a.output.write_text(json.dumps(result,indent=2)+"\n");return code

if __name__=="__main__":raise SystemExit(main())
