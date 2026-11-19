"""Phase-free per-geometry clock modulus bounds from a subset of density factors.

Select density factors whose scopes fit a cover by components of at most 3 clocks.
Remaining factors have modulus at most one. Optimize the cover before averaging
over the outer lobe nodes. Independent components factor exactly.
"""
from common import HERE, clocks, prior, setup, archived
import numpy as np
import json
from itertools import combinations

def partitions(nodes):
    if not nodes:
        yield ()
        return
    first,*rest=nodes
    for k in range(min(2,len(rest))+1):
        for chosen in combinations(rest,k):
            group=(first,*chosen)
            for tail in partitions(tuple(j for j in rest if j not in chosen)):
                yield (group,*tail)

def bound(key,n,m):
    ref=clocks.reference
    inner,coeff,_=prior.growth.layout(key)
    gx,gw=ref.quadrature(n); ox,ow=ref.quadrature(m)
    fixed={j:(j-5)*ref.STEP for j in (*ref.geometry.P,*ref.geometry.F)}
    scopes={j:tuple([i for i in inner if coeff.get((i,j),0)]+[j]) for j in inner}
    part=list(partitions(inner))
    groups=sorted(set(g for p in part for g in p))
    def value(t):
        fixed[3]=t
        densities={}
        for j,s in scopes.items():
            if len(s)>3:continue
            times={i:ref.align(1.5*gx,(i,),s) for i in s}
            c=1+ref.BETA/2*sum(k*(times[j]-(fixed[i] if i in fixed else times[i]))**2
                                 for (i,h),k in coeff.items() if h==j and k)
            densities[j]=abs(ref.density_factor(c))
        vals={}
        for g in groups:
            factors=[j for j in densities if set(scopes[j])<=set(g)]
            if not factors: vals[g]=1.; continue
            used=tuple(i for i in g if any(i in scopes[j] for j in factors))
            v=1.
            for j in factors:
                v=v*ref.align(densities[j],scopes[j],used)
            for i in used:v=v*ref.align(gw,(i,),used)
            vals[g]=v.sum()
        return min(np.prod([vals[g] for g in p]) for p in part)
    return sum(w*value(-2*ref.STEP+side/16+x/32) for side in (-1,1) for x,w in zip(ox,ow))/2/np.sqrt(768)

def run():
    names,_=setup();known=archived(); out={}
    # Compute an independent modulus cap for all 129 previously untabulated clocks.
    for name in names:
        if name in known:continue
        caps={}
        for tag,(n,m) in [('coarse',(32,6)),('fine',(48,8))]:
            caps[tag]=float(bound(prior.key(name),n,m))+1e-12
        out[name]=caps
    (HERE/'caps.json').write_text(json.dumps(out,indent=2)+'\n')
if __name__=='__main__':run()
