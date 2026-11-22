from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
import json
from antwort import spectrum
from transfer import frozen

def row(args):
    k,rho=args
    m=2.**(-k)
    c=frozen()
    r=spectrum(m,float(rho),'positive',3,4)['raw']
    y=spectrum(m,float(rho),'positive',4,8)['raw']
    assert abs(r-y)<1e-8
    q=float(c['gain'])*(y-float(c['offset']))
    return str(rho)+'|'+str(k),dict(raw=y,calibrated=q,relative_raw=y/m-1,relative_calibrated=q/m-1,
                                    raw_within=abs(y/m-1)<=.02,calibrated_within=abs(q/m-1)<=.02,
                                    refinement=abs(r-y))

def run():
    with ProcessPoolExecutor(max_workers=3) as pool:
        return dict(pool.map(row,[(k,r) for k in range(6,21) for r in (Q(1,8),Q(1,4))]))

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
