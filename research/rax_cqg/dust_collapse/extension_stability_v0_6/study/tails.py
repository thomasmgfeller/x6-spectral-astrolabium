"""Finite-grid contraction, integrating high-valence sink clocks once.

The frozen C99 tail contraction sums one Gauss clock conditional on its parents.
For a sink without a link from boundary clock 3 this tensor is shared by every
outer-clock node. All other factors use the original density function.
"""
from itertools import permutations
from tempfile import TemporaryDirectory
from common import HERE, clocks, prior
import numpy as np
from quadrature import build

def packet(key,n,m,lib):
    ref=clocks.reference
    inner,coef,gravity=prior.growth.layout(key)
    p,f=ref.geometry.P,ref.geometry.F
    gx,gw=ref.quadrature(n);x=1.5*gx
    fixed={j:(j-5)*ref.STEP for j in p+f}
    edges={j:tuple(i for i in inner if coef.get((i,j),0)) for j in inner}
    unary={j:gw*np.exp(-1j*ref.BETA/32*sum(coef[j,k]*(fixed[k]-x)**2 for k in f)) for j in inner}
    base={j:1+ref.BETA/2*sum(coef[i,j]*(fixed[i]-x)**2 for i in p if i!=3) for j in inner}
    large=[j for j in inner if len(edges[j])>=4]
    constants=[];remaining=[j for j in inner if j not in large]
    assert all(len(edges[j])==4 and coef[3,j]==0 and all(j not in e for e in edges.values()) for j in large),key
    for j in large:
        # C tail uses axes (node clock index, parent clock index).
        weights=np.ascontiguousarray([ref.BETA/2*coef[i,j]*(x[:,None]-x[None,:])**2 for i in edges[j]])
        tail=np.empty((n,)*len(edges[j]),complex)
        lib.tail(n,len(edges[j]),base[j],np.exp(-.5j*base[j]),unary[j],
                 weights,np.ascontiguousarray(np.exp(-.5j*weights)),tail.reshape(-1))
        constants.append((edges[j],tail))
    active=tuple(sorted(set(remaining)|{i for s,_ in constants for i in s}))
    scopes=[frozenset((*edges[j],j)) for j in remaining]+[frozenset(s) for s,_ in constants]
    def cost(order):
        scopes1=list(scopes);work=0
        for i in order:
            touch=[s for s in scopes1 if i in s]; joint=frozenset.union(*touch)
            work+=n**len(joint);scopes1=[s for s in scopes1 if i not in s]+[joint-{i}]
        return work
    order=min(permutations(active),key=cost)
    assert cost(order)<5*n**4+n**3*6,(key,cost(order))
    def point(t):
        fixed[3]=t
        def collar(j):
            return 1+ref.BETA/2*sum(b*(fixed[j]-fixed[i])**2 for (i,k),b in coef.items()
                                     if k==j and i in fixed and b)
        past=sum(collar(j) for j in p)
        overall=np.exp(1j*(gravity-sum(collar(j) for j in f)/16))
        factors=constants.copy()
        for j in remaining:
            scope=tuple(sorted((*edges[j],j)))
            v=ref.align(x,(j,),scope)
            c=ref.align(base[j]+ref.BETA/2*coef[3,j]*(t-x)**2,(j,),scope)
            for i in edges[j]:
                c=c+ref.BETA/2*coef[i,j]*(v-ref.align(x,(i,),scope))**2
            factors.append((scope,ref.density_factor(c)*ref.align(unary[j],(j,),scope)))
        for j in order:
            touch=[(s,a) for s,a in factors if j in s]
            factors=[(s,a) for s,a in factors if j not in s]
            scope=tuple(sorted(set().union(*(s for s,a in touch))))
            prod=1.
            for s,a in touch:prod=prod*ref.align(a,s,scope)
            factors.append((tuple(i for i in scope if i!=j),prod.sum(axis=scope.index(j))))
        return past,overall*np.prod([a for s,a in factors])
    ox,ow=ref.quadrature(m); result=np.zeros(2,complex)
    for side in (-1,1):
        for xx,ww in zip(ox,ow):
            past,z=point(-2*ref.STEP+side/16+xx/32)
            result+=ww*z*np.sinc(past/(64*np.pi))*np.exp(-.5j*past*np.array(ref.RHO))/np.sqrt(3072)
    return result

def go(masklist):
    import json
    from unittest.mock import patch
    path=HERE/'direct.json'
    results=json.loads(path.read_text()) if path.exists() else {}
    with TemporaryDirectory() as temp,patch.object(clocks.reference,'layout',prior.growth.layout):
        lib=build(temp)
        for mask in masklist:
            s=f'N14_{mask}'
            if s in results:continue
            k=prior.key(s)
            zz=packet(k,4,3,lib)
            independently=clocks.direct_packet(k,4,3)[0].sum(axis=1)/np.sqrt(2)
            err=float(max(abs(zz-independently)))
            assert err<1e-13,(s,err)
            rows={};status={}
            for tag,(n,m) in [('coarse',(32,6)),('fine',(48,8))]:
                z=packet(k,n,m,lib)
                rows[tag]=[[v.real,v.imag] for v in z]
            results[s]={'rows':rows,'cartesian_error':err}
            path.write_text(json.dumps(results,indent=2)+'\n')
            print(s,flush=True)
if __name__=='__main__':
    import sys
    go([int(x) for x in sys.argv[1:]])
