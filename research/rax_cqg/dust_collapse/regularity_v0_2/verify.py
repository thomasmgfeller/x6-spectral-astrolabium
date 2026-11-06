#!/usr/bin/env python3
"""Deterministic reference checks. No CST ensemble or physical measurements."""
from pathlib import Path
from fractions import Fraction as F
import csv, json, math, platform
import numpy as np
import scipy
from scipy.integrate import quad
from scipy.fft import dst, idst

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'results'
OUT.mkdir(exist_ok=True)
alpha, beta, kappa, hbar = 1., .5, 1., 1.
z = alpha - 1j*beta
N2 = 2*(2*alpha)**3.5/math.gamma(3.5)
NORM = math.sqrt(N2)
A, J, E = F(7,4), F(7,2), F(79,20)
TB = J/(4*E)
VB = A-J*J/(4*E)
assert TB == F(35,158) and VB == F(77,79)

def wave(q,t):
    tau=kappa*hbar*t
    D=1-4j*z*tau
    return NORM*D**(-3.5)*q*(q*q-6j*tau*D)*np.exp(-z*q*q/D)

def coefficient2(t):
    tau=kappa*hbar*t
    return 36*tau*tau*N2/abs(1-4j*z*tau)**5

def integrate(fun, lo=0.):
    # The split resolves the inverse-moment cutoff and leaves a smooth tail.
    first, e1=quad(fun,lo,4.,epsabs=2e-10,epsrel=2e-11,limit=300)
    last, e2=quad(fun,4.,np.inf,epsabs=2e-10,epsrel=2e-11,limit=300)
    return first+last,e1+e2

def writecsv(name, rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def initial_derivative(q):
    return NORM*np.exp(-z*q*q)*(3*q*q-2*z*q**4)

energy_check,_=integrate(lambda q: hbar*hbar*abs(initial_derivative(q))**2)
current_check,_=integrate(lambda q: 2*hbar*q*np.imag(np.conj(wave(q,0))*initial_derivative(q)))
assert abs(energy_check-float(E))<2e-10 and abs(current_check-float(J))<2e-10

moments=[]
for t in [0., .05, .125, float(TB), .35, .5]:
    norm,err=integrate(lambda q: abs(wave(q,t))**2)
    vol,_=integrate(lambda q: q*q*abs(wave(q,t))**2)
    inv1,_=integrate(lambda q: abs(wave(q,t)/q)**2)
    forecast=float(A-2*J*F(t)+4*E*F(t)**2)
    assert abs(norm-1)<2e-10
    assert abs(vol-forecast)<2e-9
    assert inv1 <= 4*float(E)+1e-10
    moments.append(dict(time=t,norm=norm,volume=vol,volume_exact=forecast,
                        inverse_first=inv1,hardy_upper=4*float(E),linear_coefficient_squared=coefficient2(t)))
inv2_initial,_=integrate(lambda q: abs(wave(q,0)/q**2)**2)
assert abs(inv2_initial-16/15)<2e-10
assert abs(moments[0]['inverse_first']-.8)<2e-10
writecsv('moments.csv',moments)

cuts=[]
for j in range(4,15):
    eps=2.**-j
    value,error=integrate(lambda q: abs(wave(q,float(TB)))**2/q**4,eps)
    cuts.append(dict(j=j,q_cutoff=eps,inverse_second_cutoff=value,
                     scaled=eps*value,coefficient_squared=coefficient2(float(TB)),
                     quadrature_error_estimate=error))
assert abs(cuts[-1]['scaled']/coefficient2(float(TB))-1)<.001
writecsv('cutoff.csv',cuts)

spectral=[]
L=16.
for n in [512,1024,2048,4096,8192]:
    dq=L/(n+1); q=dq*np.arange(1,n+1); k=np.pi*np.arange(1,n+1)/L
    f0=wave(q,0)
    evolved=idst(dst(f0,type=1,norm='ortho')*np.exp(1j*k*k*float(TB)),type=1,norm='ortho')
    exact=wave(q,float(TB))
    l2=math.sqrt(dq*np.sum(abs(evolved-exact)**2))
    norm=dq*np.sum(abs(evolved)**2)
    inv2=dq*np.sum(abs(evolved)**2/q**4)
    spectral.append(dict(interior_nodes=n,dq=dq,l2_error=l2,norm=norm,
                         inverse_second_grid=inv2,dq_times_inverse=dq*inv2,
                         predicted_limit=math.pi**2/6*coefficient2(float(TB))))
    assert l2<2e-10 and abs(norm-1)<2e-10
assert abs(spectral[-1]['dq_times_inverse']/spectral[-1]['predicted_limit']-1)<.01
writecsv('spectral.csv',spectral)

# Exact rational checks of geometric identities in units 6*pi*G=M=hbar=1.
# Then c=1, b=nu^2/4, rho_B=4/nu^2 and Kmax=(16/3)/b^2.
scales=[]
for nu in [F(1),F(1,2),F(1,4),F(1,8)]:
    b=nu*nu/4; rho=1/b; km=F(16,3)/b**2
    scales.append(dict(nu=float(nu),minimum_volume=float(b),rho_B=float(rho),Kmax=float(km)))
for r0,r1 in zip(scales,scales[1:]):
    assert r1['rho_B']==4*r0['rho_B'] and r1['Kmax']==16*r0['Kmax']
writecsv('physical_scale.csv',scales)

mesh=[]
b=F(1,4)
for dt in [F(1,8),F(1,16),F(1,32),F(1,64)]:
    t=dt/2; V=b+t*t; H=2*t/(3*V); Hd=2*(b-t*t)/(3*V*V)
    K=12*((Hd+H*H)**2+H**4)
    mesh.append(dict(time_step=float(dt),nearest_time=float(t),sampled_minimum=float(V),
                     sampled_Kmax=float(K),true_Kmax=float(F(256,3))))
writecsv('numerical_refinement.csv',mesh)

matching=[]
for b in [F(0),F(1,16),F(1,4),F(1)]:
    for t in [F(-2),F(-1,2),F(0),F(1,2),F(2)]:
        V=b+t*t
        if not V: continue
        Vd=2*t; Vdd=F(2)
        H=Vd/(3*V); Hd=(Vdd*V-Vd*Vd)/(3*V*V)
        K=12*((Hd+H*H)**2+H**4)
        numerator=9*b*b-6*b*t*t+5*t**4
        assert K==F(16,27)*numerator/V**4
        mass=Vd*Vd/(4*V) # 24*pi*G=4
        pressure=-(2*V*Vdd-Vd*Vd)/(4*V*V)
        rho_eff=Vd*Vd/(4*V*V)
        assert mass==1-b/V and pressure==-b/V**2
        assert rho_eff==1/V-b/V**2
        if b: assert K<=F(16,3)/b**2
        else: assert mass==1 and pressure==0
        matching.append(dict(b=float(b),time=float(t),volume=float(V),mass_ratio=float(mass),
                             normalized_mismatch=float(1-mass),effective_pressure=float(pressure),K=float(K)))
writecsv('finite_ball.csv',matching)

# Exact polynomial certificate for the global curvature maximum.
lhs=[9*math.comb(4,j) for j in range(5)]
rhs=[9,-6,5,0,0]
certificate=[a-b for a,b in zip(lhs,rhs)]
assert certificate==[0,42,49,36,9] and all(c>=0 for c in certificate)

tails=[]
for n in range(1,9):
    eps=F(1,2**n)
    for power in [1,2,3]:
        weight=eps**power
        mean=(1-weight)+weight*eps
        inv2=(1-weight)+weight/eps**2
        tails.append(dict(n=n,epsilon_volume=float(eps),small_volume_weight_power=power,
                          mean_volume=float(mean),inverse_second=float(inv2)))
writecsv('tail_controls.csv',tails)

summary=dict(status='SCOPED_RESULTS_ONLY_CST_REGULARITY_HOLD',
    parameters=dict(alpha=alpha,beta=beta,kappa=kappa,hbar=hbar),
    exact=dict(T_b=str(TB),V_b=str(VB),A=str(A),J=str(J),E=str(E),
               inverse_second_initial='16/15',inverse_first_initial='4/5'),
    numeric=dict(moment_evaluations=len(moments),cutoff_values=len(cuts),spectral_levels=len(spectral),
                 initial_energy_quadrature=energy_check,initial_current_quadrature=current_check,
                 finite_ball_exact_checks=len(matching),tail_controls=len(tails),
                 max_norm_error=max(abs(r['norm']-1) for r in moments+spectral),
                 max_spectral_l2=max(r['l2_error'] for r in spectral),
                 max_moment_volume_error=max(abs(r['volume']-r['volume_exact']) for r in moments),
                 bounce_coefficient_squared=coefficient2(float(TB)),
                 finest_scaled_cutoff=cuts[-1]['scaled']),
    limitations=['Floating-point checks are not interval certificates.',
                 'Analytic divergence proof is separate from numerical checks.',
                 'No new CST ensemble, density operator, exterior solution or horizon claim.'],
    versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
(OUT/'verification.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
