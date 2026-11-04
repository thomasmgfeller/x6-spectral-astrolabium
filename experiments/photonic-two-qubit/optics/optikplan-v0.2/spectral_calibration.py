"""Overlap on a common fully populated rectangular spectral grid in A/B port coordinates."""
import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np


def compare(path):
    fields=["u_THz","v_THz","cw_density","ccw_density"]
    phase_field="relative_phase_rad"
    with path.open(newline="") as stream:
        reader=csv.DictReader(stream)
        if reader.fieldnames not in (fields,fields+[phase_field]):
            raise ValueError("expected four spectral fields and optionally relative_phase_rad")
        has_phase=phase_field in reader.fieldnames
        cells={}
        for row in reader:
            values=[float(row[k]) for k in reader.fieldnames]
            u,v,a,b=values[:4]
            if not all(map(math.isfinite,values)) or min(a,b)<0 or (u,v) in cells:
                raise ValueError("invalid spectral value or duplicate grid point")
            cells[u,v]=values[2:]
    u=sorted({x for x,_ in cells}); v=sorted({y for _,y in cells})
    if min(len(u),len(v))<2 or len(cells)!=len(u)*len(v):
        raise ValueError("a complete 2D grid with at least two points per axis is required")
    def weights(points):
        delta=np.diff(points)
        return (np.r_[0,delta]+np.r_[delta,0])/2
    area=weights(u)[:,None]*weights(v)[None,:]
    grid=np.array([[cells[x,y] for y in v] for x in u])
    a,b=grid[:,:,0],grid[:,:,1]
    ia,ib=float(np.sum(area*a)),float(np.sum(area*b))
    if min(ia,ib)<=0:
        raise ValueError("both directions require nonzero integrated counts")
    integrand=area*np.sqrt(a*b)
    normal=math.sqrt(ia*ib)
    result={"power_ratio_ccw_over_cw":ib/ia,
            "spectral_overlap_abs_upper":float(integrand.sum()/normal),
            "phase_supplied":has_phase,"gamma_abs":None,"signed_DA_coherent_term":None,
            "hardware_gate":"NOT_ASSESSED"}
    if has_phase:
        cross=np.sum(integrand*np.exp(1j*grid[:,:,2]))
        result.update(gamma_abs=float(abs(cross)/normal),
                      signed_DA_coherent_term=float(2*cross.real/(ia+ib)))
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("grid",type=Path)
    print(json.dumps(compare(parser.parse_args().grid),indent=2,allow_nan=False))
