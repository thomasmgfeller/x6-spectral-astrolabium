#!/usr/bin/env python3
"""Compact-measure Ward identities, exact packet norms, one-sided source audit."""
from pathlib import Path
import itertools
import json
import math
import time
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parent
N=11;INNER=(4,5,6);PAST=(0,1,2,3);FUTURE=(7,8,9,10)
BS=(1,-9,16,-8);BETA=4/math.sqrt(6);DELTA=math.sqrt(2/(19*BETA));L=1.5
SOURCE_VALUES=(s.Rational(1,8),s.Rational(1,4))
PAIRS=list(itertools.product(SOURCE_VALUES,repeat=2))
ORDERS={'chain':set(),'two_cover_deleted':{(4,5),(5,6)}}
def coeffs(removed):
    rel={(i,j) for i in range(N) for j in range(i+1,N)}-removed
    c={(i,j):BS[k] if k<4 else 0 for i,j in rel
        for k in [sum((i,z) in rel and (z,j) in rel for z in range(N))]}
    return c,N-sum(c.values())
def cvalue(j,T,c):return 1+BETA*sum(v*(T[j]-T[i])**2 for (i,k),v in c.items() if k==j)/2
def pack(z):return {'real':float(np.real(z)),'imag':float(np.imag(z))}
def unpack(z):return complex(z['real'],z['imag'])
def key(p,f):return str(p)+'|'+str(f)

def exact_checks():
    r,C=s.symbols('r C',real=True);u=s.symbols('u',real=True)
    f=1+2*r+3*r*r
    derivative=s.diff(f*s.exp(-s.I*r*C/2),r)
    assert s.simplify(derivative-(s.diff(f,r)-s.I*C*f/2)*s.exp(-s.I*r*C/2))==0
    assert s.simplify((s.Rational(1,2)+(1-s.exp(-s.I*C/2))/(s.I*C)).subs(C,4*s.pi))==s.Rational(1,2)
    # A direct polynomial moment check includes the half atom and half interval.
    moment=lambda p:s.expand(p).subs(r,0)/2+s.integrate(p,(r,0,1))/2
    assert moment(1+r*0)==1 and moment(r)==s.Rational(1,4)
    Jpoly=s.integrate((1-u*u)**6,(u,-1,1))
    assert Jpoly==s.Rational(2048,3003)
    eps,eta,Lsym=s.symbols('eps eta L',positive=True)
    Ar2=s.Rational(3003,1024)/eps
    AT2=s.Rational(3003,1024)*Lsym/eta
    assert s.simplify(Ar2*eps*Jpoly/2)==1
    assert s.simplify(AT2*eta*Jpoly/(2*Lsym))==1
    variance=s.simplify(s.integrate(u*u*(1-u*u)**6,(u,-1,1))/Jpoly)
    assert variance==s.Rational(1,15)
    assert s.diff((1-u*u)**3,u).subs(u,1)==0
    assert s.diff((1-u*u)**3,u,2).subs(u,1)==0
    beta=4/s.sqrt(6);delta=s.sqrt(s.sqrt(6)/38)
    t=s.symbols('T0:11',real=True)
    data={t[j]:(j-5)*delta for j in (*PAST,*FUTURE)}
    past_rows={}
    for name,removed in ORDERS.items():
        c,F=coeffs(removed)
        Cs=[1+beta*sum(v*(t[j]-t[i])**2 for (i,k),v in c.items() if k==j)/2 for j in range(N)]
        Bpast=s.simplify(sum(Cs[j] for j in PAST).subs(data))
        assert Bpast==s.Rational(151,19)
        assert all(s.diff(Bpast,t[j])==0 for j in INNER)
        densities=s.symbols('r0:11',real=True)
        S=F-sum(densities[j]*Cs[j] for j in range(N))/2
        assert s.simplify(sum(s.diff(S,x) for x in t))==0
        past_rows[name]={'C_past':[str(s.simplify(Cs[j].subs(data))) for j in PAST],
                         'sum_C_past':str(Bpast),'global_action_shift_derivative':0}
    return {
      'positive_density_Ward':'integral_0^1 (fprime-i*C*f/2)*exp(-i*r*C/2) dr/2 = [f(1)*exp(-i*C/2)-f(0)]/2',
      'full_density_atom_not_differentiated':True,
      'D_at_C4pi':'1/2','C_D_at_C4pi':'2*pi',
      'clock_Ward':'integral (partial_T psi+i*E_T*psi)*exp(iS) dT/(2L) = [psi*exp(iS)]_-L^L/(2L)',
      'global_shift_fixed_box':'sum_B partial_TB K = -sum_I boundary_face_integrals/(2L)',
      'nonzero_toy_shift_flux':'for S=-(t-tau)^2/2,L=3/2,tau=1/4: Kprime=(exp(-49i/32)-exp(-25i/32))/3, abs=2*sin(3/8)/3>0',
      'packet_polynomial_integral':str(Jpoly),'positive_density_amplitude_squared':str(Ar2),
      'clock_amplitude_squared':str(AT2),'scaled_variance':str(variance),
      'polynomial_packet_regularities':'C2 compact support, sufficient for the displayed first-order integration by parts; not called C-infinity',
      'smooth_packet':'b(u)=exp(-1/(1-u^2))*1_|u|<1, J=integral_-1^1 b(u)^2 du; density prefactor sqrt(2/(eps*J)), clock prefactor sqrt(2L/(eta*J))',
      'packet_centers':['1/8','1/4'],'density_half_width':'1/32','clock_half_width':'1/16',
      'packet_mean_density':'center','packet_mean_clock':'center',
      'normalization_scope':'exact in declared positive auxiliary product measure; no physical inner product derived',
      'past_constraints':past_rows,
      'one_sided_factorization':'Wc(rhoP,rhoF)=exp(-i*151*rhoP/38)*Vc(rhoF)',
      'relative_past_density_response':'EXACT_ZERO_AT_FIXED_PAST_CLOCKS_AND_FUTURE_DATA',
      'scope':'Not a general no-go: integrating common past-clock packets can couple a past density preparation to future amplitudes.'}

def integrate(n,removed):
    c,F=coeffs(removed);x,w=np.polynomial.legendre.leggauss(n);times=L*x;w=w/2
    w23=w[:,None]*w[None,:]
    vals=np.zeros(4,dtype=complex);dp=vals.copy();df=vals.copy()
    for h in range(n):
        T=[(j-5)*DELTA for j in range(N)];T[4]=times[h];T[5]=times[:,None];T[6]=times[None,:]
        CI=[cvalue(j,T,c) for j in INNER]
        BP=sum(cvalue(j,T,c) for j in PAST);BF=sum(cvalue(j,T,c) for j in FUTURE)
        D=[(1+np.exp(-1j*C/4)*np.sinc(C/(4*np.pi)))/2 for C in CI]
        factor=w[h]*w23*D[0]*D[1]*D[2]
        for q,(p,f) in enumerate(PAIRS):
            term=factor*np.exp(-.5j*(float(p)*BP+float(f)*BF))
            vals[q]+=np.sum(term);dp[q]+=np.sum(term*(-.5j*BP));df[q]+=np.sum(term*(-.5j*BF))
    vals*=np.exp(1j*F);dp*=np.exp(1j*F);df*=np.exp(1j*F)
    source={key(p,f):{'rho_past':str(p),'rho_future':str(f),'W':pack(vals[q]),
             'partial_past':pack(dp[q]),'partial_future':pack(df[q]),
             'past_derivative_identity_discrepancy':float(abs(dp[q]+1j*151/38*vals[q]))}
             for q,(p,f) in enumerate(PAIRS)}
    phase=np.exp(-1j*151/38*float(SOURCE_VALUES[1]-SOURCE_VALUES[0]))
    residuals={str(f):abs(unpack(source[key(SOURCE_VALUES[1],f)]['W'])-phase*unpack(source[key(SOURCE_VALUES[0],f)]['W'])) for f in SOURCE_VALUES}
    assert max(residuals.values())<3e-13
    assert max(e['past_derivative_identity_discrepancy'] for e in source.values())<3e-13
    return {'nodes_per_axis':n,'sources':source,'past_common_phase_residual':residuals}

def main():
    start=time.monotonic();exact=exact_checks();runs={}
    for name,removed in ORDERS.items():runs[name]=[integrate(n,removed) for n in (128,160)]
    summary={}
    for p,f in PAIRS:
        kk=key(p,f);z0=runs['chain'][-1]['sources'][kk];z1=runs['two_cover_deleted'][-1]['sources'][kk]
        a=unpack(z0['W']);b=unpack(z1['W'])
        summary[kk]={'W1_over_W0':pack(b/a),'abs_ratio':abs(b/a),
          'partial_past_log_ratio':pack(unpack(z1['partial_past'])/b-unpack(z0['partial_past'])/a),
          'partial_future_log_ratio':pack(unpack(z1['partial_future'])/b-unpack(z0['partial_future'])/a)}
    discrepancy={name:{kk:{quantity:abs(unpack(rr[-1]['sources'][kk][quantity])-unpack(rr[-2]['sources'][kk][quantity])) for quantity in ('W','partial_past','partial_future')} for kk in rr[-1]['sources']}for name,rr in runs.items()}
    result={'id':'COMPACT-WARD-AND-ONE-SIDED-SOURCE-0.1','exact_checks_pass':True,'exact':exact,
      'new_experiment':'Separate past/future collar densities with fixed affine boundary clocks; common fixed future in each one-sided comparison.',
      'source_pairs':[[str(p),str(f)]for p,f in PAIRS],
      'original_inner_density_measure':'(delta0+dr_(0,1))/2 at each of3innernodes',
      'original_inner_clock_measure':'dT/3 on[-3/2,3/2] at eachof3innernodes',
      'all_8_density_strata_in_product_D':True,'added_clock_theta_restriction':False,
      'quadrature':runs,'relative_weight_summary':summary,'n128_n160_discrepancies':discrepancy,
      'analytic_truncation':'Same W bounds as prior full_weight hold because all future densities<=1/4 and past density only gives a unit-modulus constant phase: chain1.2e-25,alternative1.6e-32 atn160; not a float roundoff certificate.',
      'numerical_scope':'Float64 diagnostic. Exact zero past response is proved algebraically, not inferred from numerical cancellation.',
      'physical_boundary_norm_derived':False,'physical_initial_value_evolution_derived':False,
      'runtime_seconds':round(time.monotonic()-start,3)}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'exact_checks_pass':True,'relative_weight_summary':summary,'runtime_seconds':result['runtime_seconds']},indent=2))

if __name__=='__main__':main()
