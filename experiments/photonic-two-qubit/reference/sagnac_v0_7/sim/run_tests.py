#!/usr/bin/env python3
"""Compile RTL, run GHDL, compare all counters/flags to batch oracle, call host CLI."""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import random
import re
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"host"))
from analyze import FORMAT
from frame_codec import decode_frame,decode_stream
from reference import reference
W=1000; CAL=7

def dump(path,obj):
    path.write_text(json.dumps(obj,indent=2,allow_nan=False)+"\n")

def record(start,stop,counts,flags,setting=0):
    return {"format":FORMAT,"origin":"synthetic","complete":True,
            "setting_index":setting,"calibration_id":str(CAL),"flags":flags,
            "configuration":{"start_ps":str(start),"stop_ps":str(stop),"window_ps":str(W)},
            "counters":[str(c) for c in counts]}

def cases():
    a=50000
    def c(name,n,ev,bits=64,start=a,stop=None,complete=True):
        stop=start+n*W if stop is None else stop
        ev=list(ev)
        if complete: ev.append((4,stop,CAL,0))
        return dict(name=name,start=start,stop=stop,events=ev,bits=bits,complete=complete)
    ev=[(ch,a+i*W+10,CAL,0) for i in range(16) for ch in range(4) if i&(1<<ch)]
    yield c("all_16_masks",16,ev)
    ev=[(0,a+i*W+dt,CAL,0) for i in range(61) for dt in (10,210)]
    yield c("same_channel_repeat_61",61,ev)
    yield c("half_open_boundaries",4,[(0,a,CAL,0),(2,a+999,CAL,0),
              (4,a+1000,CAL,0),(1,a+1000,CAL,0),(3,a+1000,CAL,0),(0,a+3000,CAL,0)])
    for label,order in (("forward",range(4)),("reverse",reversed(range(4)))):
        yield c("equal_timestamps_"+label,2,[(ch,a+100,CAL,0) for ch in order])
    yield c("empty_windows",300,[])
    yield c("billion_empty_windows",1000000000,[])
    yield c("billion_windows_two_hits",1000000000,[(0,a+10,CAL,0),(2,a+999999999*W+999,CAL,0)])
    yield c("bulk_saturation",1000000000,[],bits=4)
    high=(1<<64)-1-10000
    yield c("near_u64_limit",10,[(0,high,CAL,0),(2,high+9999,CAL,0)],start=high)
    yield c("source_loss",2,[(0,a+10,CAL,1)])
    yield c("calibration_mismatch",2,[(0,a+10,CAL+1,0)])
    yield c("nonmonotonic_time",2,[(0,a+20,CAL,0),(1,a+10,CAL,0)])
    yield c("before_run",2,[(0,a-1,CAL,0)])
    yield c("hit_at_stop",2,[(0,a+2000,CAL,0)])
    yield c("invalid_kind",2,[(7,a+10,CAL,0)])
    yield c("counter_saturation",20,[],bits=4)
    yield c("invalid_zero_duration",0,[],complete=False)
    yield c("invalid_partial_window",0,[],stop=a+1500,complete=False)
    yield c("missing_final_watermark",2,[(0,a+10,CAL,0)],complete=False)
    for seed in (104729,37,8191):
        rng=random.Random(seed); ev=[]
        for i in range(257):
            for _ in range(rng.randrange(9)):
                ev.append((rng.randrange(4),a+i*W+rng.randrange(W),CAL,0))
        ev.sort(key=lambda e:e[1])
        yield c("random_seed_"+str(seed),257,ev)
    # Synthetic singlet probabilities; iid bins, photon loss eta=0.75 each side.
    # This constructs a software fixture and is not physical evidence.
    for setting,(aa,bb) in enumerate(((0,22.5),(0,-22.5),(45,22.5),(45,-22.5))):
        rng=random.Random(104729+setting); ev=[]
        e=-math.cos(math.radians(2*(aa-bb)))
        for i in range(4000):
            alice=rng.choice((1,-1)); bob=alice if rng.random()<(1+e)/2 else -alice
            if rng.random()<0.75: ev.append((0 if alice==1 else 1,a+i*W+100,CAL,0))
            if rng.random()<0.75: ev.append((2 if bob==1 else 3,a+i*W+110,CAL,0))
        item=c("synthetic_chsh_"+str(setting),4000,ev);item["setting"]=setting
        yield item

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ghdl",default=os.environ.get("GHDL","ghdl"))
    args=parser.parse_args(); ghdl=args.ghdl
    build=ROOT/"build";build.mkdir(exist_ok=True)
    evidence=ROOT/"validation";evidence.mkdir(exist_ok=True)
    def run(cmd,timeout=60):
        return subprocess.run(cmd,cwd=build,text=True,capture_output=True,timeout=timeout)
    version=run([ghdl,"--version"])
    if version.returncode: raise RuntimeError(version.stderr)
    (evidence/"ghdl_version.txt").write_text(version.stdout)
    compile_result=run([ghdl,"-a","--std=08",str(ROOT/"rtl/sagnac_pkg.vhd"),
                        str(ROOT/"rtl/sagnac_core.vhd"),str(ROOT/"rtl/snapshot_framer.vhd"),
                        str(ROOT/"rtl/uart_tx.vhd"),str(ROOT/"rtl/sagnac_uart_top.vhd"),
                        str(ROOT/"sim/tb_sagnac.vhd"),str(ROOT/"sim/tb_uart_top.vhd")])
    (evidence/"compile.log").write_text(compile_result.stdout+compile_result.stderr)
    if compile_result.returncode:raise RuntimeError(compile_result.stderr)
    results=[]; chsh=[]; frames=[]
    for case in cases():
        name=case["name"]; start,stop=case["start"],case["stop"]
        setting=case.get("setting",0)
        src=build/(name+".txt");out=build/(name+"_snapshot.txt")
        if out.exists():out.unlink()
        text=f"{start:016X} {stop:016X} {CAL:08X} {setting}\n"
        text+=''.join(f"{k} {t:016X} {cal:08X} {err}\n" for k,t,cal,err in case["events"])
        src.write_text(text)
        began=time.monotonic()
        process=run([ghdl,"-r","--std=08","tb_sagnac",f"-gINPUT_FILE={src}",
                     f"-gOUTPUT_FILE={out}",f"-gCOUNTER_BITS={case['bits']}","--assert-level=error"])
        (evidence/(name+".log")).write_text(process.stdout+process.stderr)
        if name=="missing_final_watermark":
            assert process.returncode!=0 and "snapshot timeout" in process.stdout and not out.exists(),process.stdout
            results.append({"name":name,"status":"PASS_EXPECTED_TIMEOUT","events":len(case["events"])});continue
        assert process.returncode==0,(name,process.stdout,process.stderr)
        lines=out.read_text().splitlines(); flags=int(lines[0].split()[1],16)
        counts=[int(line.split()[1],16) for line in lines[1:]]
        expected,eflags=reference(start,stop,W,case["events"],CAL,case["bits"])
        assert counts==expected,(name,counts,expected)
        assert flags==eflags,(name,flags,eflags)
        snap=record(start,stop,counts,flags,setting)
        frame=bytes.fromhex(Path(str(out)+".frame.hex").read_text())
        decoded=decode_frame(frame,origin="synthetic",expected_sequence=100+setting)
        for key,value in snap.items():assert decoded[key]==value,(name,key)
        core_cycles=int(re.search(r"SAGNAC_CORE_CYCLES=(\d+)",process.stdout).group(1))
        if name.startswith("billion_") or name=="bulk_saturation":assert core_cycles<40,(name,core_cycles)
        (evidence/(name+".frame.bin")).write_bytes(frame)
        snap=decoded
        dump(evidence/(name+".json"),snap)
        if name=="same_channel_repeat_61":
            assert counts[17]==61 and counts[22]==61 and counts[1]==61 and counts[23]==0
        if name.startswith("synthetic_chsh_"):chsh.append(snap);frames.append(frame)
        results.append({"name":name,"status":"PASS","events":len(case["events"]),
                        "flags":flags,"core_cycles":core_cycles,"seconds":round(time.monotonic()-began,4),
                        "stimulus_sha256":hashlib.sha256(src.read_bytes()).hexdigest()})
    top_output=build/"top.frame.hex"
    top=run([ghdl,"-r","--std=08","tb_uart_top",f"-gOUTPUT_FILE={top_output}","--assert-level=error"])
    (evidence/"top_integration.log").write_text(top.stdout+top.stderr)
    assert top.returncode==0,(top.stdout,top.stderr)
    top_frame=bytes.fromhex(top_output.read_text())
    top_record=decode_frame(top_frame,origin="synthetic",expected_sequence=(1<<64)-2)
    expected_top=[0]*24
    expected_top[0]=999999999;expected_top[1]=1;expected_top[16]=1000000000;expected_top[18]=1
    assert [int(x) for x in top_record["counters"]]==expected_top
    assert top_record["flags"]==0
    (evidence/"top_integration.frame.bin").write_bytes(top_frame)
    results.append({"name":"top_integration","status":"PASS","events":2})
    source=ROOT/"examples/synthetic_chsh_snapshots.json"
    binary=ROOT/"examples/synthetic_chsh_capture.bin";binary.write_bytes(b''.join(frames))
    p=run([sys.executable,str(ROOT/"host/frame_codec.py"),str(binary),"--output",str(source),
           "--origin","synthetic","--first-sequence","100"])
    assert p.returncode==0,(p.stdout,p.stderr)
    assert json.loads(source.read_text())["records"]==chsh
    output=ROOT/"examples/synthetic_chsh_analysis.json"
    p=run([sys.executable,str(ROOT/"host/analyze.py"),str(source),"--output",str(output)])
    assert p.returncode==0,(p.stdout,p.stderr)
    analysis=json.loads(output.read_text())
    assert analysis["conditional_coincidences"]["model_conditional_gate"] is True
    assert analysis["all_trials_fixed_assignment"]["model_conditional_gate"] is False
    assert analysis["physical_quantum_claim"]=="NOT_ASSESSED"
    # End-to-end rejection: use the RTL-produced source-loss snapshot.
    bad=json.loads(json.dumps(chsh));bad[0]=json.loads((evidence/"source_loss.json").read_text())
    invalid=ROOT/"examples/invalid_source_loss.json";dump(invalid,{"records":bad})
    p=run([sys.executable,str(ROOT/"host/analyze.py"),str(invalid),"--output",str(ROOT/"examples/invalid_source_loss_analysis.json")])
    assert p.returncode==2,(p.stdout,p.stderr)
    result={"status":"PASS","rtl_cases":results,"case_count":len(results),
            "host_integration":"PASS_RTL_UART_CRC_JSON_ANALYSIS_AND_INVALID","origin":"synthetic",
            "physical_quantum_claim":"NOT_ASSESSED",
            "conditional_S":analysis["conditional_coincidences"]["S"],
            "all_trials_S":analysis["all_trials_fixed_assignment"]["S"]}
    dump(evidence/"test_summary.json",result)
    print(json.dumps({k:v for k,v in result.items() if k!="rtl_cases"},indent=2))

if __name__=="__main__": main()
