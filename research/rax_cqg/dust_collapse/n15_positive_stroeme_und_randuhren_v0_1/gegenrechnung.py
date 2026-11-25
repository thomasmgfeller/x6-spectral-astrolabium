"""Independent linear programs and complex finite-arm readout from original action arguments."""
from fractions import Fraction as F
import json
import math
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import linprog
from quadratur import fields,REL,EDGES,I,P,FUT,tensor
from fluss import masks,key,STEP,PHASE_ERROR

H=float(STEP)
GROUPS=masks()
R=Path(__file__).resolve().parent


def linear_program(e):
    y,w=fields(e)
    result={}
    for mode in ('all','kernel','cover'):
        edges=sorted((i,j) for i,j in REL if (i in P and j in I) or (i in I and j in I+FUT))
        if mode=='kernel':
            supported={(i,j) for i,j,b in EDGES}
            edges=[z for z in edges if z in supported]
        if mode=='cover':
            edges=[(i,j) for i,j in edges if not any((i,k) in REL and (k,j) in REL for k in range(15))]
        c=np.array([float(i in P) for i,j in edges])
        mat=np.array([[float(j==v)-float(i==v) for i,j in edges] for v in I]+
                     [[y[j]-y[i] if j==v else 0. for i,j in edges] for v in I])
        rhs=np.r_[np.zeros(7),19*w[list(I)]]
        sol=linprog(c,A_eq=mat,b_eq=rhs,bounds=(0,None),method='highs')
        if mode=='cover':
            assert sol.status==2
            result[mode]={'infeasible':True}
        else:
            assert sol.success
            dual=sol.eqlin.marginals
            assert max(abs(mat@sol.x-rhs))<1e-10 and max(mat.T@dual-c)<1e-10 and abs(dual@rhs-sol.fun)<1e-10
            result[mode]={'objective':float(sol.fun),'dual_objective':float(dual@rhs),
                          'max_balance_or_moment_residual':float(max(abs(mat@sol.x-rhs)))}
    return result


def integrate(level,order,groups=GROUPS,scale=1.0,atom=False):
    grid,wt=tensor(order,7)
    ex,ew=leggauss(order)
    arms=np.zeros((len(groups),2),complex)
    base=0j
    for node,omega in zip(ex,ew):
        e=1/6+node*2**-22
        y,w=fields(e)
        w[list(I)+list(FUT)]*=scale
        if atom:
            w[list(I)]=0
        hy=(4-e)/(64*2**level)
        hw=w[list(I)]/(100*2**level)
        jac=omega*(2*hy)**7*(1 if atom else np.prod(2*hw))
        clocks=np.broadcast_to(y,(len(grid),15)).copy()
        clocks[:,I]+=hy*grid
        # Sum the raw action rows at the unpulsed clocks.
        C=np.full((len(grid),15),19.0)
        for i,j,b in EDGES:
            C[:,j]+=b*(clocks[:,i]-clocks[:,j])**2
        def integrate_rows(rows):
            center=-(rows@w)/38
            beta=-rows[:,I]*hw/38
            mod=np.prod(np.sinc(beta/np.pi),axis=1)
            return wt@(mod*np.exp(1j*center))
        base+=jac*integrate_rows(C)
        for n,g in enumerate(groups):
            for m,h in enumerate((-H,H)):
                rows=C.copy()
                # The known correction subtracts the CHANGE of all purely past terms exactly.
                # For a receiver outside P, evaluate its original squared distance at the new argument.
                for i,j,b in EDGES:
                    if i in g and j not in P:
                        diff=clocks[:,i]-clocks[:,j]
                        rows[:,j]+=b*((clocks[:,i]+h-clocks[:,j])**2-diff**2)
                arms[n,m]+=jac*integrate_rows(rows)
    ans={}
    for g,(minus,plus) in zip(groups,arms):
        phi=float(np.angle(minus*plus.conjugate()))
        # Equivalent visibility formula avoids a rounded ratio above one.
        vis=float(1-(abs(minus)-abs(plus))**2/(abs(minus)**2+abs(plus)**2))
        ans[key(g)]={'relative_phase_rad':phi,'charge_from_phase':19*phi/(2*H),'visibility':vis,
                     'Y_port_probability':(1+vis*np.sin(phi))/2}
    return ans


def original_point_checks():
    from fractions import Fraction as Rat
    from gegenprobe import original_normalized_action
    from pruefung import encode
    code=encode(REL,15)
    count=0
    for e in (1/6-2**-22,1/6,1/6+2**-22):
        y0,w0=fields(e)
        y=[Rat(str(round(n,8))) for n in y0]
        w=[Rat(str(round(n,8))) for n in w0]
        only_p=[x if i in P else Rat(0) for i,x in enumerate(w)]
        for g in GROUPS:
            q=sum(b*w[j]*(y[i]-y[j]) for i,j,b in EDGES if i in g and j not in P)
            K=-sum(b*w[j] for i,j,b in EDGES if i in g and j not in P)/38
            ref=original_normalized_action(code,y,w)
            p0=original_normalized_action(code,y,only_p)
            for h in (-STEP,STEP):
                yy=[v+h if j in g else v for j,v in enumerate(y)]
                observed=original_normalized_action(code,yy,w)-original_normalized_action(code,yy,only_p)+p0-ref
                assert observed==-h*q/19+h*h*K
                count+=1
    return count


def run():
    solvers=[linear_program(1/6+z*2**-22) for z in (-1,0,1)]
    rows={}
    for k,n in ((0,3),(0,4),(3,3)):
        rows[f'{k}_{n}']=integrate(k,n)
    vac=integrate(0,3,atom=True)
    assert all(abs(v['relative_phase_rad'])<1e-12 for v in vac.values())
    scales={str(s):integrate(0,3,(frozenset([1]),frozenset(P)),s) for s in (0.5,2.)}
    return {'linear_programs':solvers,'quadrature_by_level_order':rows,'empty_interior':vac,
            'future_density_scale_controls':scales,'rational_source_checks':original_point_checks()}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
