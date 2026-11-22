"""Secondary model intervention: consistent reassignment of both adjacent dwell cells."""
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as F
from itertools import product
import json
from randquelle import ROOT,EDGES,INNER,PAST,ORDER,ETA,profile,support_check
from modell import dwell,INNER_MEANS

def exact():
    weights=profile(5)
    # Direct mixed coefficients for all past, inner and future basis densities.
    for j in ORDER:
        val=-sum(b*(int(t in PAST)-int(i in PAST))*(weights.get(t,0)-weights.get(i,0))
                 for (i,t),b in EDGES.items() if t==j)
        assert val==int(j==5)
    u=INNER_MEANS.copy()
    shifted=u.copy();step=F(1,32);shifted[INNER.index(6)]+=step
    diff={j:(dwell(shifted)[j]-dwell(u)[j])/step for j in INNER}
    assert diff[5]==F(1,2) and diff[11]==-F(1,2) and sum(abs(v) for v in diff.values())==1
    hi=F(support_check()['pulsversatz_in_u'][1])
    return {'profil_5':list(map(str,weights.values())),'zellableitungen':{str(k):str(v) for k,v in diff.items()},
            'maximaler_rel_jitterrest_zweiseitig':str(ETA*hi)}

def run():
    from auslese import calc
    cases=[(1,n,k,m,j) for (n,k,m),j in product([(5,10,'gauss'),(5,9,'cc')],(5,11))]
    with ProcessPoolExecutor(max_workers=3) as pool:rows=dict(pool.map(calc,cases))
    return {'algebra':exact(),'numerik':rows}

if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
