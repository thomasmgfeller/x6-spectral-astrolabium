"""Tensor Gauss integration of the archived collar packet, bounded-memory graph contractions."""
from functools import lru_cache
import finite_grid
import numpy as np

BETA=4/np.sqrt(6.)
STEP=np.sqrt(2/(19*BETA))
P,F=(0,1,2,3),(7,8,9,10)
INNER=(4,5,6,11,12,13)

@lru_cache(None)
def rule(n):
    x,w=np.polynomial.legendre.leggauss(n)
    return x,w/2

def packet(intervals,gravity,sizes,outer_n,density_n,checked=False):
    rule_used=finite_grid.checked_rule if checked else rule
    phase=finite_grid.phase if checked else lambda x:np.exp(1j*x)
    sinc=finite_grid.sinc if checked else lambda x:np.sinc(x/np.pi)
    def density(c):
        return (1+phase(-.25*c)*sinc(c/4))/2

    grids={k: (1.5*rule_used(n)[0],rule_used(n)[1]) for k,n in zip(INNER,sizes)}
    broad=next((j for j in INNER if sum(bool(intervals.get((i,j))) for i in INNER)>=4),None)
    times={k:(k-5)*STEP for k in (*P,*F)}
    x,w=rule_used(outer_n)
    def integrate():
        def collar(j,t):
            return 1+BETA/2*sum(intervals.get((i,j),0)*(t-times[i])**2 for i in P+F if (i,j) in intervals)
        constant=phase(gravity-sum(collar(j,times[j]) for j in F)/16)
        past=sum(collar(k,times[k]) for k in P)
        # Each inner-to-future clock term attaches to the inner variable as a unary phase.
        def unary(k):
            v,wk=grids[k]
            phi=sum(intervals.get((k,j),0)*(times[j]-v)**2 for j in F)
            return wk*phase(-BETA/32*phi)
        unary_all={k:unary(k) for k in INNER}
        base={k:collar(k,grids[k][0]) for k in INNER}
        def incoming(j,v,known):
            return BETA/2*sum(b*(v-t)**2 for k,t in known.items() if (b:=intervals.get((k,j),0)))
        if broad is None:
            # At fixed T4,T5,T6 the three remaining events are mutually unrelated.
            leaves=(11,12,13)
            assert all(not intervals.get((a,b),0) for a in leaves for b in leaves)
            t5=grids[5][0][:,None];t6=grids[6][0][None,:]
            result=0j
            for idx,t4 in enumerate(grids[4][0]):
                front=unary_all[4][idx]*density(base[4][idx])
                vals=front*(unary_all[5]*density(base[5]+incoming(5,grids[5][0],{4:t4})))[:,None]
                vals=vals*(unary_all[6]*density(base[6]+incoming(6,t6,{4:t4,5:t5})))
                parents={4:t4,5:t5[:,:,None],6:t6[:,:,None]}
                for k in leaves:
                    v=grids[k][0]
                    vals=vals*np.sum(unary_all[k]*density(base[k]+incoming(k,v,parents)),axis=-1)
                result+=np.sum(vals)
        else:
            # At fixed T4,T5,T_b and rho_b all other inner clocks separate.
            leaves=[k for k in INNER if k not in (4,5,broad)]
            assert all(not intervals.get((a,b),0) for a in leaves for b in leaves)
            assert all(not intervals.get((broad,k),0) for k in INNER)
            r0,rw=rule_used(density_n)
            r=np.r_[0.,(1+r0)/2];rw=np.r_[.5,rw/2]
            vb=grids[broad][0]
            kernels={}
            for k in leaves:
                coeff=intervals.get((k,broad),0)
                if coeff:
                    v=grids[k][0]
                    dist=(vb[None,:]-v[:,None])**2
                    kernels[k]=phase(-BETA/4*coeff*dist[:,:,None]*r).reshape(len(v),-1)
            result=0j
            for idx,t4 in enumerate(grids[4][0]):
                t5=grids[5][0][:,None]
                known={4:t4,5:t5}
                front=unary_all[4][idx]*density(base[4][idx])
                weights=front*unary_all[5]*density(base[5]+incoming(5,grids[5][0],{4:t4}))
                c=base[broad]+incoming(broad,vb,known)
                vals=unary_all[broad][:,None]*rw*phase(-.5*c[:,:,None]*r)
                for k in leaves:
                    v=grids[k][0]
                    row=unary_all[k]*density(base[k]+incoming(k,v,known))
                    row=np.broadcast_to(row,(len(t5),len(v)))
                    if checked and k in kernels:
                        contracted=np.einsum('ij,jk->ik',row,kernels[k],optimize=False)
                    else:
                        contracted=row@kernels[k] if k in kernels else None
                    factor=contracted.reshape(len(t5),len(vb),len(r)) if k in kernels else np.sum(row,axis=1)[:,None,None]
                    vals=vals*factor
                result+=np.sum(weights[:,None,None]*vals)
        return past,constant*result
    answer=np.zeros(2,dtype=complex)
    for side in (-1,1):
        for t,wt in zip(x,w):
            times[3]=-2*STEP+side/16+t/32
            past,z=integrate()
            answer+=wt*z*sinc(past/64)*phase(-.5*np.array([.125,.25])*past)
    return answer/np.sqrt(3072.)
