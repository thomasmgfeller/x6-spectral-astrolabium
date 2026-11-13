#!/usr/bin/env python3
"""Full finite Dirichlet/box dust-clock weight, analytic tensor error bound.

Float64 evaluations are not certified interval enclosures. The analytic
quadrature truncation estimate is proved separately from evaluation roundoff.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math
import time
import mpmath as mp
import numpy as np
import sympy as s

ROOT=Path(__file__).resolve().parent
N=11;INNER=(4,5,6);BOUNDARY=tuple(j for j in range(N) if j not in INNER)
BS=(1,-9,16,-8)
BETA=4/math.sqrt(6);DELTA=math.sqrt(2/(19*BETA));L=1.5
RHOS=(s.Rational(1,8),s.Rational(1,4))
ORDERS={'chain':set(),'two_cover_deleted':{(4,5),(5,6)}}

def geometry(removed):
    rel={(i,j) for i in range(N) for j in range(i+1,N)}-removed
    coeff={(i,j):BS[k] if k<4 else 0 for i,j in rel
           for k in [sum((i,z) in rel and (z,j) in rel for z in range(N))]}
    assert all((i,k) in rel for i,j in rel for jj,k in rel if j==jj)
    return coeff,N-sum(coeff.values())

def cvalue(j,T,coeff):
    out=0.0
    for (i,k),value in coeff.items():
        if k==j and value:out=out+value*(T[j]-T[i])**2
    return 1+BETA*out/2

def pack(z):return {'real':float(np.real(z)),'imag':float(np.imag(z))}

def integrate(n,removed):
    coeff,F=geometry(removed)
    nodes,weights=np.polynomial.legendre.leggauss(n)
    times=L*nodes;weights=weights/2
    w23=weights[:,None]*weights[None,:]
    totals=np.zeros((2,8),dtype=complex)
    derivatives=np.zeros((2,8),dtype=complex)
    direct=np.zeros(2,dtype=complex)
    for h in range(n):
        T=[(j-5)*DELTA for j in range(N)]
        T[4]=times[h];T[5]=times[:,None];T[6]=times[None,:]
        CI=[cvalue(j,T,coeff) for j in INNER]
        Bsum=sum(cvalue(j,T,coeff) for j in BOUNDARY)
        E=[np.exp(-1j*C/4)*np.sinc(C/(4*np.pi)) for C in CI]
        weighted=weights[h]*w23
        phases=[np.exp(-.5j*float(rho)*Bsum) for rho in RHOS]
        for idx,bits in enumerate(itertools.product((0,1),repeat=3)):
            factor=1
            for k,bit in enumerate(bits):
                if bit:factor=factor*E[k]
            for q,phase in enumerate(phases):
                term=weighted*phase*factor/8
                totals[q,idx]+=np.sum(term)
                derivatives[q,idx]+=np.sum(term*(-.5j*Bsum))
        product=(1+E[0])*(1+E[1])*(1+E[2])/8
        for q,phase in enumerate(phases):direct[q]+=np.sum(weighted*phase*product)
    totals*=np.exp(1j*F);derivatives*=np.exp(1j*F);direct*=np.exp(1j*F)
    assert np.max(np.abs(totals.sum(axis=1)-direct))<2e-13
    return {'nodes_per_axis':n,'evaluations_per_order':n**3,'F4':F,
      'stratum_order':[list(bits) for bits in itertools.product((0,1),repeat=3)],
      'sources':{str(rho):{'W':pack(totals[q].sum()),'dW_drho':pack(derivatives[q].sum()),
          'stratum_W':[pack(z) for z in totals[q]],'stratum_dW_drho':[pack(z) for z in derivatives[q]],
          'sum_vs_direct_discrepancy':float(abs(totals[q].sum()-direct[q]))}
          for q,rho in enumerate(RHOS)}}

def analytic_bound(n,removed):
    # R=7/4, ellipse semiaxes a=(R+1/R)/2,b=(R-1/R)/2.
    # One complex clock, other clocks real, all fixed clocks bounded by L.
    # |exp(iSd)| <= exp((beta/2)*L*b*L*(a+1)*sum |b_ij|rmax_j).
    # beta<5/3 gives coefficient15/8. Source rho<=1/4.
    coeff,F=geometry(removed);R=s.Rational(7,4)
    aa=(R+1/R)/2;bb=(R-1/R)/2
    sums=[sum(abs(v)*(s.Integer(1) if j in INNER else s.Rational(1,4))
         for (i,j),v in coeff.items() if k in (i,j)) for k in INNER]
    exponents=[s.Rational(15,8)*bb*(aa+1)*v for v in sums]
    # Entire boundary constraint insertion on same ellipse. The loose universal
    # bound uses |z_i-z_j|<=L*(a+b+1), and never drops constant collar terms.
    boundary_abs=sum(abs(v) for (i,j),v in coeff.items() if j in BOUNDARY)
    insertion=s.Rational(len(BOUNDARY),2)+s.Rational(5,12)*s.Rational(9,4)*(aa+bb+1)**2*boundary_abs
    mp.mp.dps=80
    mp.iv.dps=80
    rational=lambda x:mp.iv.mpf(int(s.numer(x)))/int(s.denom(x))
    e=sum(4*mp.iv.exp(rational(x))*rational(R)**(-2*n)/(1-1/rational(R)) for x in exponents)
    # Round UP to two leading decimal digits with a full extra increment.
    def outward_decimal(x):
        x=mp.mpf(x.b)
        e10=int(mp.floor(mp.log10(x)));unit=mp.power(10,e10-1)
        return mp.nstr((mp.ceil(x/unit)+1)*unit,12)
    return {'R':str(R),'incident_weight_sums':[str(v) for v in sums],
      'log_M_upper_rational':[str(v) for v in exponents],
      'exact_error_formula':'sum_k 4 exp(log_M_k) R^(-2n)/(1-R^(-1))',
      'absolute_W_truncation_bound_upward':outward_decimal(e),
      'derivative_insertion_complex_bound':str(insertion),
      'absolute_dW_truncation_bound_upward':outward_decimal(e*rational(insertion)),
      'includes_float_evaluation_roundoff':False}

def exact_checks():
    C=s.symbols('C',real=True,nonzero=True);u=s.symbols('u',real=True)
    D=s.Rational(1,2)+(1-s.exp(-s.I*C/2))/(s.I*C)
    assert s.limit(D,C,0)==1
    assert s.simplify(D-s.Rational(1,2)-s.integrate(s.exp(-s.I*u*C/2),(u,0,1))/2)==0
    e=s.symbols('e0:3')
    assert s.expand(s.prod((1+x)/2 for x in e)-sum(s.prod(e[k] if bit else 1 for k,bit in enumerate(bits))/8 for bits in itertools.product((0,1),repeat=3)))==0
    # Exact global shift invariance belongs to the action, not this box measure.
    return {'D_at_zero':1,'atom_positive_expansion_exact':True,
            'scalar_dust_factorization_exact':'S=F4+Sd(T,r)+Sphi(q); all measures factor under the declared fixed boundary/box completion.',
            'source_derivative_exact':'Wprime=exp(iF4) <(-i/2 sum_B Cj) exp(-i rho sum_B Cj/2) product_I D(Cj)>',
            'on_shell_slope_not_substituted':'23/19 is the derivative of a stationary action difference, not the derivative of log of this complete integral.'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--nodes',nargs='+',type=int,default=[64,96,128,160]);args=parser.parse_args()
    start=time.monotonic();checks=exact_checks();runs={}
    for name,removed in ORDERS.items():
        runs[name]=[]
        for n in args.nodes:
            run=integrate(n,removed);run['analytic_truncation']=analytic_bound(n,removed);runs[name].append(run)
            print(name,n,run['sources'],flush=True)
    def complexof(v):return complex(v['real'],v['imag'])
    summary={}
    for r in map(str,RHOS):
        a=runs['chain'][-1]['sources'][r];b=runs['two_cover_deleted'][-1]['sources'][r]
        W0=complexof(a['W']);W1=complexof(b['W']);D0=complexof(a['dW_drho']);D1=complexof(b['dW_drho'])
        summary[r]={'W1_over_W0':pack(W1/W0),'abs_W1_over_W0':abs(W1/W0),
            'log_ratio_source_derivative':pack(D1/W1-D0/W0),
            'on_shell_phase_slope':23/19,
            'difference_vs_on_shell_log_slope':pack(D1/W1-D0/W0-1j*23/19)}
    empirical={}
    if len(args.nodes)>1:
        for name in ORDERS:
            empirical[name]={r:{key:abs(complexof(runs[name][-1]['sources'][r][key])-complexof(runs[name][-2]['sources'][r][key])) for key in ('W','dW_drho')}for r in map(str,RHOS)}
    result={'id':'FULL-DIRICHLET-BOX-DUST-CLOCK-WEIGHTS-0.1',
      'status':'COMPLETE_FINITE_INTEGRAL_DEFINED_AND_EVALUATED_WITH_SEPARATE_ANALYTIC_TRUNCATION_BOUND',
      'fixed_boundary_T':'(j-5)*sqrt(sqrt(6)/38)','fixed_boundary_r':'rho',
      'inner_clock_measure':'product dTj/3 on [-3/2,3/2]^3','inner_density_measure':'product (delta0+1_(0,1)dr)/2',
      'clock_order_theta_restriction':False,'boundary_states':'fixed Dirichlet data, not normalized physical boundary states',
      'full_weight':'exp(iF4)*E_T[exp(-i*rho*sum_B Cj/2)*product_I D(Cj)]',
      'D':'1/2 + (1-exp(-i*C/2))/(i*C), D(0)=1',
      'all_8_density_strata_weight':'1/8 each before positive integrations',
      'no_stationary_phase_double_count':True,'audit_sources':[str(q) for q in RHOS],
      'exact_checks':checks,'quadrature':runs,'relative_weight_summary':summary,
      'last_two_order_discrepancies':empirical,
      'numerical_qualification':'Float64 evaluation, empirical refinement discrepancies are diagnostics. Analytic truncation bound excludes floating-point nodes, weights, arithmetic and elementary-function roundoff; numerical complex values are NOT fully certified intervals.',
      'global_rigorous_bounds':['abs(W)<=1','abs(Wprime)<=0.5*E_T(abs(sum_B Cj))<=0.5*sup_box(abs(sum_B Cj))'],
      'new_physical_pairing_derived':False,'new_4d_geometry_dynamics_derived':False,
      'runtime_seconds':round(time.monotonic()-start,3)}
    (ROOT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'runtime_seconds':result['runtime_seconds'],'summary':summary,'empirical':empirical},indent=2))

if __name__=='__main__':main()
