#!/usr/bin/env python3
"""Capture a prescribed number of snapshot frames from an explicit Linux UART.

Keeps raw bytes even on failure. Does not flush, resync, change GPIO or start FPGA.
"""
import argparse
import json
import os
from pathlib import Path
import select
import termios
import time
import tty
from frame_codec import FRAME_BYTES,decode_stream,FrameError

def capture(device,frames,baud,timeout):
    if not 1<=frames<=4096 or timeout<=0:raise ValueError("invalid capture length/deadline")
    speed=getattr(termios,"B"+str(baud),None)
    if speed is None:raise ValueError("baud unsupported by this Linux termios build")
    fd=os.open(device,os.O_RDONLY|os.O_NOCTTY|os.O_NONBLOCK)
    raw=bytearray();reason=None;old=None
    try:
        old=termios.tcgetattr(fd);tty.setraw(fd,when=termios.TCSANOW)
        attrs=termios.tcgetattr(fd);attrs[4]=speed;attrs[5]=speed
        attrs[2]|=termios.CLOCAL|termios.CREAD
        attrs[2]&=~(termios.CSTOPB|getattr(termios,"CRTSCTS",0))
        termios.tcsetattr(fd,termios.TCSANOW,attrs)
        deadline=time.monotonic()+timeout;target=frames*FRAME_BYTES
        while len(raw)<target:
            left=deadline-time.monotonic()
            if left<=0:reason="capture deadline exceeded";break
            ready,_,_=select.select([fd],[],[],left)
            if not ready:reason="capture deadline exceeded";break
            try:chunk=os.read(fd,target-len(raw))
            except BlockingIOError:continue
            if not chunk:reason="UART closed before prescribed frame count";break
            raw.extend(chunk)
    except OSError as exc:reason=str(exc)
    finally:
        if old is not None:
            try:termios.tcsetattr(fd,termios.TCSANOW,old)
            except OSError:pass
        os.close(fd)
    return bytes(raw),reason

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--device",required=True);p.add_argument("--frames",type=int,default=4)
    p.add_argument("--baud",type=int,default=1000000);p.add_argument("--timeout",type=float,default=120)
    p.add_argument("--first-sequence",type=int,required=True)
    p.add_argument("--origin",choices=("hardware","synthetic"),required=True)
    p.add_argument("--raw",type=Path,required=True);p.add_argument("--output",type=Path,required=True)
    a=p.parse_args();data=b''
    if a.raw.resolve()==a.output.resolve():p.error("raw and JSON output paths must differ")
    try:
        data,reason=capture(a.device,a.frames,a.baud,a.timeout)
        if reason:raise FrameError(reason)
        report=decode_stream(data,origin=a.origin,expected_first_sequence=a.first_sequence);code=0
    except (OSError,ValueError) as e:
        report={"transport":"INVALID","reason":str(e),"physical_quantum_claim":"NOT_ASSESSED"};code=2
    a.raw.write_bytes(data);a.output.write_text(json.dumps(report,indent=2)+"\n")
    return code

if __name__=="__main__":raise SystemExit(main())
