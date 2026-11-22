"""Forward kernels on the fixed reference preparation; the decoder is separate."""
from pathlib import Path
import math
import sys
import numpy as np

sys.path.insert(0,str(Path(__file__).resolve().parent/'quellen'))
import kern as upstream
from auslese import readout,settings

INNER = upstream.INNER
PAST = upstream.PAST
FUTURE = upstream.FUTURE

def site_product(n, offset, rho, mass, sector, source, stream):
    duration = 4*upstream.DELTA - offset
    a,b,u,v,t = map(float,source)
    factors = []
    past_sum = 0.
    is_atom = sector in ('empty','vacuum')
    positive_collar = sector != 'vacuum'
    for key,slope,_,_,_,_,share in upstream.site_data(n,offset,(a,b,u,v),stream):
        if key in PAST:
            past_sum = past_sum + slope
            if key == PAST[-1] and positive_collar:
                factors.append(np.exp(1j*rho*past_sum)*upstream.sinc(past_sum/32))
        elif key in FUTURE:
            if positive_collar:
                factors.append(np.exp(.125j*slope))
        else:
            if is_atom:
                factors.append(np.ones_like(share))
            else:
                centre = mass*duration*share
                factors.append(8*share*np.exp(1j*centre*slope)*upstream.sinc(.01*centre*slope))
    val = upstream.contract(factors,n,stream)
    collar = -7/8 if positive_collar else 0.
    return val*duration**(7 if is_atom else 14)*np.exp(1j*t*collar/duration)

def spectrum(mass, rho, sector, n, outer, stream=True):
    assert sector in ('positive','limit','empty','vacuum')
    assert (mass>0) == (sector=='positive')
    rows = settings()
    samples = {key:0j for key in rows}
    normalization = 0.
    for centre in (-1/16,1/16):
        abscissas,weights = upstream.gauss(outer)
        for node,weight in zip(abscissas,weights):
            offset = centre+node/32
            duration = 4*upstream.DELTA-offset
            for key,(source,_) in rows.items():
                samples[key] += weight/2*site_product(n,offset,rho,mass,sector,source,stream)
            if sector in ('empty','vacuum'):
                norm = duration**7
            else:
                _,shares = upstream.clocks(n,offset/upstream.DELTA)
                norm = duration**14*upstream.contract([8*f for f in shares.values()],n,stream)
            normalization += weight*norm/2
    if sector=='vacuum':
        assert all(abs(v/normalization-1)<1e-13 for v in samples.values())
    normalized = {key: v/normalization for key,v in samples.items()}
    return {'raw':readout(normalized),'min_modulus':float(min(map(abs,normalized.values()))),
            'complex_kernels':{k:[float(v.real),float(v.imag)] for k,v in normalized.items()}}
