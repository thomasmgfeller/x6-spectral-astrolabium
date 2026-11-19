"""Bound N14_27613 with the first five density factors on the inherited grid."""
from common import HERE,prior,clocks
import numpy as np
import json

def bound(n,m):
    ref=clocks.reference
    inner,coeff,_=prior.growth.layout((6,27613))
    a,b,c,d,e,f=inner
    # c,d,e here label inner nodes, independently of the outer clock.
    parents={j:tuple(i for i in inner if coeff.get((i,j),0)) for j in inner}
    assert [parents[j] for j in inner[:5]]==[(),(a,),(),(a,b,c),(a,b)]
    x,w=ref.quadrature(n);x=1.5*x
    fixed={j:(j-5)*ref.STEP for j in ref.geometry.P}
    def one(t):
        fixed[3]=t
        def value(j):
            s=parents[j]+(j,)
            v=ref.align(x,(j,),s)
            cost=1+ref.BETA/2*sum(coef*(v-(fixed[i] if i in fixed else ref.align(x,(i,),s)))**2
                      for (i,k),coef in coeff.items() if k==j and coef)
            return abs(ref.density_factor(cost))*ref.align(w,(j,),s)
        # Sum d and e conditional on parents. Drop the sixth factor using |density|<=1.
        tail=value(d).sum(axis=-1)
        return np.sum(value(a)[:,None]*value(b)*((tail*value(c)).sum(axis=-1))*value(e).sum(axis=-1))
    ox,ow=ref.quadrature(m)
    return float(sum(weight*one(-2*ref.STEP+side/16+u/32) for side in (-1,1)
                     for u,weight in zip(ox,ow))/(2*np.sqrt(768)))+1e-12
if __name__=='__main__':
    extra={'N14_27613':{k:bound(n,m) for k,(n,m) in [('coarse',(32,6)),('fine',(48,8))]}}
    (HERE/'extra_cap.json').write_text(json.dumps(extra,indent=2)+'\n');print(extra)
