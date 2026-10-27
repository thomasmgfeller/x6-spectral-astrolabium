"""Exact region-width witnesses on archived v0.3 development observations.

The alternative cell means are in the unrestricted Poisson mean region.
They are NOT asserted to be realizable by a Minkowski landmark geometry.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import json
import numpy as np
import refined
from intervals import I, precision

ROOT = Path(__file__).resolve().parent


def point_interval(cells):
    """Separate interval LDL solve; accepts integer or rational cell means."""
    def scalar(v):
        f = F(v)
        return I(int(f.numerator)) / int(f.denominator)
    C = refined.C
    counts = [sum((scalar(cells[b]) * int(C[j,b]) for b in range(20)), I(0)) for j in range(20)]
    s = [-x.sqrt() for x in counts]
    G = [[sum((s[k] * int(refined.GS2[k,i,j]) / 2 for k in range(20)), I(0)) for j in range(4)] for i in range(4)]
    d = [sum((s[k] * int(refined.DS2[k,i]) / 2 for k in range(20)), I(0)) for i in range(4)]
    L = [[I(int(i == j)) for j in range(4)] for i in range(4)]
    D = []
    for i in range(4):
        pivot = G[i][i] - sum((L[i][k].square() * D[k] for k in range(i)), I(0))
        assert pivot.hi < 0 if i == 0 else pivot.lo > 0
        D.append(pivot)
        for j in range(i + 1,4):
            L[j][i] = (G[j][i] - sum((L[j][k]*L[i][k]*D[k] for k in range(i)), I(0))) / pivot
    z = []
    for i in range(4):
        z.append(d[i] - sum((L[i][k]*z[k] for k in range(i)), I(0)))
    v = [z[i]/D[i] for i in range(4)]
    w = [I(0)]*4
    for i in range(3,-1,-1):
        w[i] = v[i] - sum((L[k][i]*w[k] for k in range(i+1,4)), I(0))
    q = -sum((d[i]*w[i] for i in range(4)), I(0))
    assert q.lo > 0
    return q


def verify(y, alternatives):
    rows = []
    for lam in alternatives:
        assert all(x >= 0 for x in lam)
        assert all(lam[i] > 0 or y[i] == 0 for i in range(20))
        # log u <= u-1 gives D(y||lambda) <= (y-lambda)^2/lambda.
        upper = sum((F((int(y[i])-lam[i])**2,lam[i]) for i in range(20) if lam[i]), F(0))
        assert upper <= 48
        q = point_interval(lam)
        rows.append({'means':lam,'kl_upper_exact':str(upper),'kl_upper_decimal':float(upper),
                     'q_lower':str(q.lo),'q_upper':str(q.hi)})
    rows.sort(key=lambda r: Decimal(r['q_lower']))
    assert 81*F(Decimal(rows[1]['q_lower'])) > 121*F(Decimal(rows[0]['q_upper']))
    return rows


def main():
    precision(60)
    old = np.load(ROOT.parent/'joint_region_v0_3/fresh_counts.npz')['cells']
    gs = json.loads((ROOT.parent/'poisson_v0_2/geometries.json').read_text())
    records = []
    for gi in [3,7,11,15,19]:
        y = old[20+gi,0]
        a = np.array(refined.evaluate(y,diagnostics=True)['gradient'])
        direction = 6*y*a/np.sqrt(np.dot(y,a*a))
        alternatives = [np.maximum(0,y + np.rint(sign*direction).astype(np.int64)).tolist() for sign in [-1,1]]
        records.append({'geometry':gs[gi]['id'],'old_level':1,'old_repeat':0,'observed_cells':y.tolist(),
                        'alternatives':verify(y,alternatives),'no_common_10pct_estimate_on_full_region':True})
    out = {'status':'PASS_REGION_WIDTH_WITNESSES','records':records,
           'scope':'Five archived development observations. Unrestricted cell-mean region only; no physical-geometric realizability or statistical impossibility claim.'}
    (ROOT/'REGION_WITNESSES.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'status':out['status'],'witnesses':len(records)}))
    return out


if __name__ == '__main__':
    main()
