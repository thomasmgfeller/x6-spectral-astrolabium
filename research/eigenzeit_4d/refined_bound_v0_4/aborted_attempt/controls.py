"""Exact rational controls for the two sharper bounds and region witnesses."""
from fractions import Fraction as F
from decimal import Decimal
from pathlib import Path
import json,random
import numpy as np
import refined,witnesses
from intervals import I,precision

ROOT=Path(__file__).resolve().parent


def main():
    precision(60);rng=random.Random(2026102709);checks=0
    # Exact Cauchy-Schwarz inequality for matrix-valued linear fluctuations.
    for _ in range(100):
        bs=[];delta=[F(rng.randint(-9,9),7) for b in range(5)]
        u=[F(rng.randint(1,9),3) for b in range(5)]
        v=[F(rng.randint(-9,9),5) for i in range(4)]
        for b in range(5):
            a=[[F(rng.randint(-9,9),11) for j in range(4)] for i in range(4)]
            bs.append([[a[i][j]+a[j][i] for j in range(4)] for i in range(4)])
        bv=[[sum(bs[b][i][j]*v[j] for j in range(4)) for i in range(4)] for b in range(5)]
        lhs=sum(sum(delta[b]*bv[b][i] for b in range(5))**2 for i in range(4))
        rhs=sum(delta[b]**2/u[b] for b in range(5))*sum(u[b]*sum(x*x for x in bv[b]) for b in range(5))
        assert lhs<=rhs;checks+=1
    # Perfect-square n,m make the exact square-root remainder rational.
    for a in range(1,21):
        for b in range(1,21):
            n=F(a*a);m=F(b*b)
            residual=F(a-b)+(m-n)/(2*a)
            exact=(m-n)**2/(2*a*(a+b)**2)
            assert residual==exact and residual>=0;checks+=1
            L=min(n,m)
            old=(m-n)**2/(8*F(min(a,b))**3)
            sharper=(m-n)**2/(2*a*(min(a,b)+a)**2)
            assert residual<=sharper<=old;checks+=1
    # Exact inequality certifying the confidence level, inherited unchanged.
    import math
    assert sum((F(24)**k/math.factorial(k) for k in range(101)),F(0))>20*2**30;checks+=1
    # Separate 60-digit point solve agrees with the reconstruction enclosure.
    y=np.load(ROOT.parent/'joint_region_v0_3/fresh_counts.npz')['cells'][20,0]
    r=refined.evaluate(y,True);q=witnesses.point_interval(y)
    assert q.lo<=Decimal(r['qhat_upper']) and q.hi>=Decimal(r['qhat_lower']);checks+=1
    assert r['certified'];checks+=1
    assert refined.evaluate([0]*20)['reason']=='COUNT_GUARD';checks+=1
    assert refined.evaluate([-1]+[100]*19)['reason']=='INVALID_CELL_COUNTS';checks+=1
    # Recheck the explicit integer witnesses, without the floating search.
    records=json.loads((ROOT/'REGION_WITNESSES.json').read_text())['records']
    for row in records:
        out=witnesses.verify(row['observed_cells'],[a['means'] for a in row['alternatives']])
        assert out==row['alternatives'];checks+=1
    return {'status':'PASS_CONTROLS','checks':checks,'region_width_witnesses':len(records)}


if __name__=='__main__':print(json.dumps(main(),indent=2))
