"""Independent assembly by target; exact integration of density jitters, two tensor quadratures."""
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
import json
import math
import numpy as np
from transport import ROOT, ORDER, PAST, INNER, FUTURE, EDGES, START, RANK, CUTS
from modell import clocks, dwell, H
from quadratur import rule, average, readout, settings

DELTA=(3/722)**.25
V=dict(zip(PAST,[k/64 for k in (76,47,24,8)]))

def coefficients(y, slot, shift, last, carry):
    split=RANK[last]+1
    buffer=ORDER[split-4:split]
    c=dict.fromkeys(ORDER,-.5)
    for j in ORDER:
        for i in ORDER[:RANK[j]]:
            b=EDGES.get((i,j),0)
            if not b:
                continue
            gap=y[j]-y[i]
            if i==slot and i in buffer and RANK[j]>=split:
                gap=gap-shift
            c[j]=c[j]-(b/38)*gap**2
            if carry and i==slot and START<=RANK[j]<split:
                c[j]=c[j]+(b/38)*(2*gap*shift-shift**2)
    return c

def run_case(case):
    last,mode,n,m,method=case
    inner_nodes,unused=rule(n,method)
    u=[(k+1)/8+inner_nodes.reshape((1,)*k+(n,)+(1,)*(6-k))/64 for k in range(7)]
    base_cells=dwell(u)
    rhos=(.125,.25)
    result={rho:{key:0j for key in settings()} for rho in rhos}
    norm=0.
    for centre in (-1/16,1/16):
        for point,weight in zip(*rule(m,method)):
            e=(centre+point/32)/DELTA
            D=DELTA*(4-e)
            y0=clocks(e,u)
            weight=weight*D**14/2
            norm+=weight*average([8*base_cells[j] for j in INNER],n,method)
            for key,(slot,s,U,W) in settings().items():
                y=dict(y0)
                for i in PAST:y[i]=y[i]+(U+W*V[i])/math.sqrt(D)
                t=s/math.sqrt(D)
                c=coefficients(y,slot,t,last,mode!='vergessen')
                cells=dict(base_cells)
                if mode=='gemeinsam' and slot==6:
                    assert last==11
                    cells[11]=cells[11]-DELTA*t/(2*D)
                inner=[]
                for j in INNER:
                    phase=c[j]*D*cells[j]
                    inner.append(8*cells[j]*np.exp(1j*phase)*np.sinc(phase/(100*np.pi)))
                # The early density produces a scalar factor independent of all seven inner axes.
                past=sum(c[j] for j in PAST)
                future=sum(c[j] for j in FUTURE)/8
                z=average([np.exp(1j*future)]+inner,n,method)*np.sinc(past/(32*np.pi))
                for rho in rhos:result[rho][key]+=weight*z*np.exp(1j*rho*past)
    calibration=json.loads((ROOT/'quellen/eichung.json').read_bytes())
    values={}
    for rho,zs in result.items():
        z={k:v/norm for k,v in zs.items()}
        r=readout(z)
        r['masse']=float(calibration['gain'])*(r['raw']-float(calibration['offset']))
        r['amplituden']={k:[v.real,v.imag] for k,v in z.items()}
        values[str(F(rho))]=r
    return f'{last}|{mode}|{method}{n}x{m}',values

def run():
    cases=[(cut,mode,n,m,method) for cut in CUTS
           for mode in (('transport','gemeinsam') if cut==11 else ('transport','vergessen'))
           for n,m,method in ((5,10,'gauss'),(5,9,'cc'))]
    with ProcessPoolExecutor(max_workers=3) as pool:return dict(pool.map(run_case,cases))

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
