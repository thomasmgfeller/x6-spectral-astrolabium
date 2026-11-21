"""Independent direct rational edge sums for the additional three-axis witness."""
from fractions import Fraction as Q
from random import Random
import json

from basis_340.quellen import density_translation_375841 as src

def run():
    rel, chains, _ = src.local_geometry()
    coefficients = {}
    for i,j in rel:
        count=len({k for k in range(15) if (i,k) in rel and (k,j) in rel})
        coefficients[i,j]=(1,-9,16,-8)[count] if count<4 else 0
    rng=Random(198431)
    p0=[]
    for n in range(33):
        def offset(radius):
            return Q(0) if n==0 else radius*Q(rng.randrange(-99,100),100)
        e=-Q(1,4)+offset(src.RADIUS)
        u={v:src.CENTER[v]+offset(src.RADIUS) for v in src.INNER}
        y={v:Q(v-5) for v in src.PAST+src.FUTURE}
        y[3]+=e
        y.update({v:-2+e+(4-e)*u[v] for v in src.INNER})
        for v in src.FUTURE[1:]:
            y[v]+=offset(Q(1,2**20))
        f={v:Q(0) for v in src.INNER}
        for chain in chains:
            walls=[0]+[(u[i]+u[j])/2 for i,j in zip(chain,chain[1:])]+[1]
            for v,a,b in zip(chain,walls,walls[1:]):
                f[v]+=(b-a)/2
        def C(v):
            return 1+sum(b*(y[j]-y[i])**2 for (i,j),b in coefficients.items() if j==v)/19
        d={v:src.COFACTOR_SCALE*(C(i)-C(j)) for v,i,j in [(4,12,13),(12,13,4),(13,4,12)]}
        xi={v:offset(src.RADIUS) for v in src.INNER}
        profiles=[{v:f[v]+xi[v]+sgn*d.get(v,0) for v in src.INNER} for sgn in (-1,1)]
        assert all(profiles[0][v]==profiles[1][v] for v in (5,11))
        assert sum(profiles[0].values())==sum(profiles[1].values())
        # Difference of dust actions divided by their common inner density scale.
        def inner_action(x):
            return -(sum(x.values())+sum(b*x[j]*(y[i]-y[j])**2
                    for (i,j),b in coefficients.items() if j in x)/19)/2
        assert inner_action(profiles[0])==inner_action(profiles[1])
        # Direct symmetric shifts in Y, rescaled back to the original p in T.
        step=Q(1,128)
        charges=[]
        for x in profiles:
            for v in src.PAST: y[v]+=step
            right=inner_action(x)
            for v in src.PAST: y[v]-=2*step
            left=inner_action(x)
            for v in src.PAST: y[v]+=step
            charges.append(Q(1,4)*(4-e)*(left-right)/(2*step))
        assert charges[0]>0>charges[1]
        if n==0: p0=list(map(str,charges))
    assert p0==['1754179/1520000000','-904179/1520000000']
    return {'rationale_feldpunkte':33,'direkte_wirkungsdifferenz':0,
            'beide_schnittdichten_identisch':True,'quellableitungen_zentrum':p0,
            'getrennte_anfangsvorzeichen_an_allen_punkten':True}

if __name__=='__main__':
    if not __debug__: raise RuntimeError('Bitte ohne -O ausführen.')
    print(json.dumps(run(),indent=2,ensure_ascii=False))
