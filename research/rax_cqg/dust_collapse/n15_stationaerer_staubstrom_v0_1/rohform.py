"""Repeat exceptional right-window cases without the minimal-clock and fork-root formulas."""
from collections import Counter
from pruefung import ROOT, WINDOWS, cover, local_witness, support
from gegenprobe import read_geometry
import json


def run():
    rows={}
    for code in support.catalogue():
        rel,edges,_=read_geometry(code)
        if local_witness(rel,'rechts') is None:
            depths=cover(rel,edges,*WINDOWS['rechts'],specialized=False)
            assert sum(2**(max(depths)-d) for d in depths)==2**max(depths)
            rows[str(code)]={str(d):n for d,n in sorted(Counter(depths).items())}
    return rows


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
