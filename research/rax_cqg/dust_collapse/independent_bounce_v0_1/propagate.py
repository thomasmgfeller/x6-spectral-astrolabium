"""Late evolution. Receives initial state and grid only, never forecast moments.

Crank-Nicolson with a central second difference Hamiltonian and Dirichlet ends.
"""
import numpy as np
from scipy.sparse import diags
from scipy.sparse.linalg import splu
from states import image_state


def evolution(case,reference,level):
    n,h,dt=level['N'],case['hbar'],level['dt']
    dx=reference['domain_L']/(n+1)
    q=dx*np.arange(1,n+1)
    psi=image_state(q,case)
    # Discrete initialization only; no use of an analytic bounce-time or volume formula.
    psi/=np.sqrt(dx*np.vdot(psi,psi).real)
    off=1j*dt*h/(2*dx*dx)
    diag=1-2*off
    A=diags([np.full(n-1,off),np.full(n,diag),np.full(n-1,off)],[-1,0,1],format='csc')
    solver=splu(A)
    bdiag,boff=np.conj(diag),np.conj(off)
    steps=round(reference['T_end']/dt)
    every=round(reference['readout_dt']/dt)
    if abs(every*dt-reference['readout_dt'])>1e-12:raise ValueError('Readout grid mismatch')
    rows=[];max_norm_error=0.
    for step in range(steps+1):
        if step%every==0:
            prob=abs(psi)**2
            norm=float(dx*np.sum(prob));volume=float(dx*np.dot(q*q,prob))
            max_norm_error=max(max_norm_error,abs(norm-1))
            rows.append({'T':step*dt,'V':volume,'norm':norm})
        if step==steps:break
        rhs=bdiag*psi
        rhs[:-1]+=boff*psi[1:]
        rhs[1:]+=boff*psi[:-1]
        psi=solver.solve(rhs)
    values=np.array([r['V'] for r in rows]);index=int(np.argmin(values))
    if index==0 or index==len(rows)-1:
        return {'interior_minimum':False,'max_norm_error':max_norm_error,'trace':rows}
    left,middle,right=values[index-1:index+2]
    step=reference['readout_dt'];denom=left-2*middle+right
    shift=.5*(left-right)/denom
    tb=rows[index]['T']+shift*step
    vb=middle-(right-left)**2/(8*denom)
    return {'interior_minimum':True,'strict_turn':bool(left>middle and right>middle),
            'T_b_observed':float(tb),'V_b_observed':float(vb),
            'max_norm_error':max_norm_error,'trace':rows}
