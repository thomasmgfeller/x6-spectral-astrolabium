"""Replay photon timing calibration groups identified by an independent pulsed reference."""
import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np


def analyse(groups, offsets_ps, full_window_ps, bin_ps):
    if len(offsets_ps) != 4 or not all(math.isfinite(x) for x in offsets_ps):
        raise ValueError("four finite predeclared channel offsets required")
    if min(bin_ps, full_window_ps) <= 0 or not groups:
        raise ValueError("positive bin/window and nonempty calibration required")
    pairs = []
    for a in (0,1):
        for b in (2,3):
            # Subtract integer raw times before converting to float (uint64 input).
            dt = np.array([(events[b]-events[a]) - (offsets_ps[b]-offsets_ps[a])
                           for events in groups.values() if a in events and b in events])
            if not dt.size:
                raise ValueError(f"no independent pulse coincidences for {a}/{b}")
            # Zero-centered fixed bins, conservative outer edges of all half-height bins.
            bins,counts = np.unique(np.floor(dt/bin_ps+.5).astype(np.int64),return_counts=True)
            above=bins[2*counts >= counts.max()]
            pairs.append({"ports":[a,b],"paired_pulses":int(dt.size),
                          "pair_mean_ps":float(dt.mean()),"q01_q99_ps":np.quantile(dt,[.01,.99]).tolist(),
                          "half_height_outer_span_ps":int((above[-1]-above[0]+1)*bin_ps),
                          "fraction_in_fixed_window":float(np.mean(abs(dt)<=full_window_ps/2))})
    return {"scope":"CALIBRATION_DIAGNOSTIC","hardware_gate":"NOT_ASSESSED",
            "pulse_ids_with_any_hit":len(groups),"pairs":pairs}


def read_hits(path):
    groups=defaultdict(dict)
    with path.open(newline="") as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames != ["pulse_id","channel","raw_ps"]:
            raise ValueError("expected pulse_id,channel,raw_ps")
        for row in reader:
            pulse,ch,t=(int(row[k]) for k in reader.fieldnames)
            if pulse<0 or ch not in range(4) or not 0<=t<2**64 or ch in groups[pulse]:
                raise ValueError("invalid or duplicate hit in calibration group")
            groups[pulse][ch]=t
    return groups


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv",type=Path)
    parser.add_argument("--offsets-ps",nargs=4,type=float,required=True)
    parser.add_argument("--bin-ps",type=int,default=50)
    args=parser.parse_args()
    print(json.dumps(analyse(read_hits(args.csv),args.offsets_ps,2000,args.bin_ps),indent=2))
