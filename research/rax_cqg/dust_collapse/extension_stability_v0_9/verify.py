"""Replay the certificates locally. --rebuild also recalculates the clock and Gaussian tables."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def close(a,b,tol):
    if isinstance(a,dict) and isinstance(b,dict) and set(a)==set(b):
        return all(close(a[k],b[k],tol) for k in a)
    if isinstance(a,(tuple,list)) and isinstance(b,(tuple,list)) and len(a)==len(b):
        return all(close(x,y,tol) for x,y in zip(a,b))
    if isinstance(a,(float,int)) and isinstance(b,(float,int)):
        return abs(a-b)<=tol
    return a==b

def main():
    if not __debug__:
        raise RuntimeError("Run without -O")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rebuild",action="store_true")
    args=parser.parse_args()
    for line in (ROOT/"SHA256SUMS").read_text().splitlines():
        expected,path=line.split("  ",1)
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=expected:
            raise ValueError(("Archive checksum",path))
    from reference import full, SOURCE
    from bounds import calculate as bounds, GRIDS, new_clocks
    from planes import calculate as planes
    from controls import calculate as controls
    from mixcheck import calculate as mixcheck
    stored_bounds=full.read(ROOT/"bounds.json")
    if json.loads(json.dumps(bounds()))!=stored_bounds:
        raise ValueError("Seven-subset certificate")
    current=planes()
    if current!=full.read(ROOT/"planes.json"):
        raise ValueError("Supporting-plane certificate")
    if not close(controls(),full.read(ROOT/"controls.json"),1e-12):
        raise ValueError("Independent Cartesian and detector controls")
    if not close(mixcheck(),full.read(ROOT/"mixcheck.json"),1e-10):
        raise ValueError("Independent simplex optimization")
    gate=full.read(SOURCE/"teiltraeger.json")
    for tag in GRIDS:
        case=gate["grids"][tag]["1/20"]
        if case["witness_transfer"]!="50211/1000000" or case["witness_high_density_success_ratio_upper_with_clock_radii"]>=.9:
            raise ValueError("Original counterexample")
        metrics=list(map(F,stored_bounds["metrics"][tag]["1/20"]))
        if metrics[2]>F(1,4) or metrics[3]>=1:
            raise ValueError("Contrast or sign")
    print("PASS: four independent Cartesian controls, four direct detector tests per grid, "
          "three positive anchor blocks, seven subset gates, full-support and five-percent certificates.",flush=True)
    if args.rebuild:
        from anchors import calculate as anchors
        from coupled import FORK, CHAIN, run
        from uhrtest import calculate as original
        clocks=original((45885,45851))
        for mask in (FORK,CHAIN):
            clocks[str(mask)]=run(mask)
        if not close(clocks,new_clocks(),1e-13):
            raise ValueError("Reconstructed clock data")
        if not close(anchors(),full.read(ROOT/"support_rows.json"),1e-13):
            raise ValueError("Reconstructed scalar rows")
        print("PASS: four seven-clock responses on three grids and 3,144 scalar overlaps.",flush=True)

if __name__=="__main__":
    main()
