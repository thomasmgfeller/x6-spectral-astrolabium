#!/usr/bin/env python3
"""Independent elementary checks of Ward, packet, prior and pointer contracts."""
from pathlib import Path
from itertools import permutations
import json
import sympy as s

OUT=Path(__file__).resolve().parent
u=s.symbols('u',real=True)
J=s.integrate((1-u*u)**6,(u,-1,1))
assert J==s.Rational(2048,3003)
assert s.integrate(u*u*(1-u*u)**6,(u,-1,1))/J==s.Rational(1,15)
eps,eta,L=s.symbols('eps eta L',positive=True)
assert s.simplify((s.Rational(3003,1024)/eps)*eps*J/2)==1
assert s.simplify((s.Rational(3003,1024)*L/eta)*eta*J/(2*L))==1
assert all(s.diff((1-u*u)**3,u,j).subs(u,1)==0 for j in range(3))
assert s.diff((1-u*u)**3,u,3).subs(u,1)!=0  # C2, not C-infinity.

C=s.symbols('C',real=True,nonzero=True)
r=s.symbols('r',real=True)
D=s.Rational(1,2)+(1-s.exp(-s.I*C/2))/(s.I*C)
assert D.subs(C,4*s.pi)==s.Rational(1,2)
assert (C*D).subs(C,4*s.pi)==2*s.pi
test=2+3*r+5*r**2
ward=s.diff(test*s.exp(-s.I*r*C/2),r)
assert s.simplify(ward-(s.diff(test,r)-s.I*C*test/2)*s.exp(-s.I*r*C/2))==0
toy_flux=(s.exp(-49*s.I/32)-s.exp(-25*s.I/32))/3
assert s.simplify(s.expand_complex(toy_flux*s.conjugate(toy_flux))-(2*s.sin(s.Rational(3,8))/3)**2)==0

# Two legitimate, inequivalent positive scalar history priors; no quantum claim.
allrel={(a,b) for a in range(11) for b in range(a+1,11)}
prior=[]
for name,rel in [('chain',allrel),('variant',allrel-{(4,5),(5,6)})]:
    covers={(a,b) for a,b in rel if not any((a,k) in rel and (k,b) in rel for k in range(11))}
    extensions=[]
    aut=0
    for p in permutations([4,5,6]):
        sequence=[0,1,2,3]+list(p)+[7,8,9,10]
        position={j:i for i,j in enumerate(sequence)}
        if all(position[a]<position[b] for a,b in rel):extensions.append(p)
        relabel=dict(zip([4,5,6],p))|{j:j for j in [0,1,2,3,7,8,9,10]}
        aut+=({(relabel[a],relabel[b]) for a,b in rel}==rel)
    counts=(len(rel),len(covers),55-len(rel),len(extensions),aut)
    assert counts==((55,10,0,1,1) if name=='chain' else (53,11,2,3,1))
    prior.append({'order':name,'R_L_I_extensions_AutB':counts})
p=s.symbols('p',positive=True)
ratio=p*(1-p)**2
assert ratio.subs(p,s.Rational(1,2))==s.Rational(1,8)
assert ratio.subs(p,s.Rational(3,4))==s.Rational(3,64)

# Normalized Gaussian pointer on a declared auxiliary Hilbert space.
y,z,zp,g=s.symbols('y z zp g',real=True)
sigma=s.symbols('sigma',positive=True)
norm=s.sqrt(2*s.pi)*sigma
square=s.exp(-(y-g*z)**2/(2*sigma**2))/norm
assert s.simplify(s.integrate(square,(y,-s.oo,s.oo)))==1
mean=g*(z+zp)/2
overlap_exponent=-((y-g*z)**2+(y-g*zp)**2)/(4*sigma**2)
completed=-(y-mean)**2/(2*sigma**2)-g*g*(z-zp)**2/(8*sigma**2)
assert s.expand(overlap_exponent-completed)==0
# Along a constraint translation coordinate t, Gaussian integration gives
# integral dt |phi(y-g(z+a*t))|^2 = 1/|g*a|, independent of y.
t,a,gg=s.symbols('t a gg',positive=True)
along=s.exp(-(y-gg*(z+a*t))**2/(2*sigma**2))/norm
assert s.simplify(s.integrate(along,(t,-s.oo,s.oo))-1/(gg*a))==0

result={'id':'PHYSICAL-BOUNDARY-INDEPENDENT-CONTRACT-CHECKS-0.1','all_checks_pass':True,
        'packet_polynomial_norm':str(J),'packet_variance_in_scaled_coordinate':'1/15',
        'packet_regularity':'C2, not C-infinity','density_Ward_positive_component_only':True,
        'constraint_delta_counterexample_C_D_at_4pi':'2*pi',
        'compact_clock_shift_nonzero_flux_squared':'4*sin(3/8)^2/9',
        'history_counts':prior,'normalized_gaussian_pointer':True,
        'pointer_coherence_multiplier':'exp(-g^2*(z-zprime)^2/(8*sigma^2))',
        'constraint_translation_conditional_record_weight':'1/abs(g*a), constant in y and nonintegrable',
        'physical_measure_selected':False,'physical_state_normalized':False}
(OUT/'contract_results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS independent compact Ward, packet norms, history counts and Gaussian-pointer identities')
