#!/usr/bin/env python3
"""Exact source-clock witnesses on thick-collar chains; no amplitude integration."""
from pathlib import Path
from fractions import Fraction
import hashlib
import json
import math
import sympy as s

OUT=Path(__file__).resolve().parent
beta=4/s.sqrt(6)
bs=[s.Integer(x) for x in (1,-9,16,-8)]
rho=s.symbols('rho', positive=True)
Delta=s.sqrt(2/(19*beta))
checks=[]
def zero(e):
    assert s.simplify(s.expand(e))==0, e
def serial(e): return str(s.simplify(e))
def chain(n): return {(i,j):bs[j-i-1] for i in range(n) for j in range(i+1,min(n,i+5))}
def constraint(j,t): return 1+beta*s.Add(*(bs[k-1]*(t[j]-t[j-k])**2 for k in range(1,5)))/2
def balance(j,t,r):
    n=len(t); coeff=chain(n)
    return beta*(sum(r[k]*b*(t[k]-t[j]) for (i,k),b in coeff.items() if i==j)
                 -sum(r[j]*b*(t[j]-t[i]) for (i,k),b in coeff.items() if k==j))/2
def flux(cut,t,r): return beta*sum(r[j]*b*(t[j]-t[i]) for (i,j),b in chain(len(t)).items() if i<=cut<j)/2

moments=[sum(bs[k-1]*k**p for k in range(1,5)) for p in range(3)]
assert moments==[0,-1,-19]
affine=[]
for n in range(9,17):
    t=[(s.Integer(j)-s.Rational(n-1,2))*Delta for j in range(n)]
    r=[rho]*n
    for j in range(4,n-4):
        zero(constraint(j,t));zero(balance(j,t,r))
        zero(beta*sum(bs[k-1]*(t[j]-t[j-k]) for k in range(1,5))+beta*Delta)
    for cut in range(3,n-4): zero(flux(cut,t,r)+19*beta*rho*Delta/2)
    affine.append({'N':n,'free_nodes':list(range(4,n-4)),
                   'clock_half_extent':serial(s.Rational(n-1,2)*Delta),
                   'clock_half_extent_decimal':str(s.N(s.Rational(n-1,2)*Delta,20)),
                   'all_constraints_and_clock_balances_zero':True,
                   'complete_bulk_cut_current':'-19*beta*rho*Delta/2'})
checks.append('affine_constraints_full_clock_balances_and_cut_flux_N9_to_N16')

# Recursion is derived directly from C_j=0 using sum b=0.
x=s.symbols('x',real=True);past=s.symbols('p1:5',real=True)
C=1+beta*sum(b*(x-y)**2 for b,y in zip(bs,past))/2
nextclock=(1+beta*sum(b*y*y for b,y in zip(bs,past))/2)/(beta*sum(b*y for b,y in zip(bs,past)))
zero(C.subs(x,nextclock))
zero(s.diff(C,x)+beta*sum(b*y for b,y in zip(bs,past)))
z=s.symbols('z')
clock_char=z**4+z**3-18*z**2+48*z-32
zero(clock_char-(z-1)*(z**3+2*z**2-16*z+32))
assert clock_char.subs(z,-6)>0 and clock_char.subs(z,-5)<0
density_char=1+z-18*z**2+48*z**3-32*z**4
zero(density_char-z**4*clock_char.subs(z,1/z))
checks.append('exact_clock_recursion_and_growing_linearized_mode_interval_minus6_minus5')

# Nine-node same-box witness: only the dust block is regular; scalar has a null mode.
a9=s.sqrt(s.Rational(163,256)-s.sqrt(6)/32)
t9=[-1,-a9,-s.Rational(1,2),-s.Rational(1,4),0,s.Rational(1,4),s.Rational(1,2),a9,1]
zero(constraint(4,t9));zero(balance(4,t9,[rho]*9))
der9=beta*(16*a9-s.Rational(49,4))
zero(beta*sum(bs[k-1]*(t9[4]-t9[4-k]) for k in range(1,5))-der9)
assert s.simplify(s.Rational(9,16)-a9*a9)>0
assert s.simplify(a9*a9-s.Rational(1,4))>0
zero(sum(chain(9)[i,j] for i,j in chain(9) if i==4 or j==4))
checks.append('boxed_N9_stationary_regular_dust_but_scalar_null_mode')

# Stronger same-box N10 witness. Define d by an isolated quartic root over Q(sqrt(6)).
b,d=s.symbols('b d',real=True);c=s.Rational(1,4)
a=(25*b-10*c+d+8)/24
t10=[-1,-a,-b,-c,-d,d,c,b,a,1]
f=s.expand(constraint(4,t10)/(beta/2))
g=s.expand(constraint(5,t10)/(beta/2))
zero(balance(4,t10,[rho]*10));zero(balance(5,t10,[rho]*10))
G=s.groebner([f,g],b,d,extension=s.sqrt(6))
assert len(G.polys)==2
P=s.Poly(G.polys[1].as_expr(),d)
b_of_d=s.solve(G.polys[0].as_expr(),b)[0]
assert s.Poly(G.polys[0].as_expr(),b).degree()==1
zero(s.rem(s.together(f.subs(b,b_of_d)),P.as_expr(),d))
zero(s.rem(s.together(g.subs(b,b_of_d)),P.as_expr(),d))

# Rational interval arithmetic: every coefficient and operation encloses exactly.
class IV:
    def __init__(self,lo,hi=None): self.lo=Fraction(lo);self.hi=Fraction(lo if hi is None else hi)
    def __add__(self,o):
        o=o if isinstance(o,IV) else IV(o);return IV(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return IV(-self.hi,-self.lo)
    def __sub__(self,o):return self+-o if isinstance(o,IV) else self+(-Fraction(o))
    def __mul__(self,o):
        o=o if isinstance(o,IV) else IV(o);v=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi];return IV(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=o if isinstance(o,IV) else IV(o);assert not o.lo<=0<=o.hi;return self*IV(1/o.hi,1/o.lo)
    def bounds(self):return [str(self.lo),str(self.hi)]

scale=10**60;floor=math.isqrt(6*scale*scale);sqrt6=IV(Fraction(floor,scale),Fraction(floor+1,scale))
def qfrac(x):return Fraction(int(s.numer(x)),int(s.denom(x)))
def coeff_iv(x):
    x=s.expand(x);v=s.expand(x).coeff(s.sqrt(6));u=s.simplify(x-v*s.sqrt(6))
    assert u.is_Rational and v.is_Rational
    return IV(qfrac(u))+sqrt6*qfrac(v)
def poly_iv(expr,box):
    ans=IV(0)
    for coef in s.Poly(expr,d).all_coeffs():ans=ans*box+coeff_iv(coef)
    return ans
lo=Fraction(12321176887857,10**14);hi=Fraction(12321176887858,10**14)
plo=poly_iv(P.as_expr(),IV(lo));phi=poly_iv(P.as_expr(),IV(hi))
assert plo.lo>0 and phi.hi<0 or plo.hi<0 and phi.lo>0
dbox=IV(lo,hi);derbox=poly_iv(s.diff(P.as_expr(),d),dbox)
assert not derbox.lo<=0<=derbox.hi
bbox=poly_iv(b_of_d,dbox)
abox=(bbox*25+dbox+IV(Fraction(11,2)))/24
assert 0<dbox.lo<dbox.hi<Fraction(1,4)<bbox.lo<bbox.hi<abox.lo<abox.hi<1
diagbox=(bbox*23+dbox*2-IV(Fraction(49,4)))/3
assert diagbox.hi<0
checks.append('boxed_N10_quartic_root_exists_unique_in_rational_interval')
checks.append('boxed_N10_positive_density_causal_monotone_clock_stationary_all_fields')

# C Jacobian is triangular with equal nonzero diagonal (apart from positive beta).
T=s.symbols('T0:10',real=True)
C4=constraint(4,T);C5=constraint(5,T)
A=s.Matrix([C4,C5]).jacobian([T[4],T[5]])
sub=dict(zip(T,t10))
A10=s.simplify(A.subs(sub)/beta)
diag=(23*b-17*c+2*d-8)/3
zero(A10[0,0]-diag);zero(A10[0,1]);zero(A10[1,0]+2*d);zero(A10[1,1]-diag)
zero(A10.det()-diag**2)
scalarH=s.Matrix([[0,beta/2],[beta/2,0]])
zero(scalarH.det()+beta**2/4)
R=s.symbols('r0:10',real=True);Q=s.symbols('q0:10',real=True)
coeff=chain(10)
full_action=9-s.Add(*R)/2-beta*s.Add(*(bij*(R[j]*(T[j]-T[i])**2+(Q[j]-Q[i])**2) for (i,j),bij in coeff.items()))/4
for j in (4,5):
    zero(-2*s.diff(full_action,R[j])-constraint(j,T))
    zero(s.diff(full_action,T[j])-balance(j,T,R))
    zero(s.diff(full_action,Q[j]).subs({v:0 for v in Q}))
computedH=s.hessian(full_action,[Q[4],Q[5]])
assert computedH==scalarH
checks.append('boxed_N10_nonzero_constraint_jacobian_and_scalar_hessian')
checks.append('full_action_independent_partial_derivative_checks_all_six_inner_fields')

# Complete cut currents are conserved and nonzero on this same-box solution.
cuts=[s.simplify(flux(k,t10,[rho]*10)/rho) for k in (3,4,5)]
for v in cuts[1:]:zero(v-cuts[0])
cut_expr=s.simplify(cuts[0]/beta)
cutbox=poly_iv(s.expand(cut_expr.subs(b,b_of_d)),dbox)
assert cutbox.hi<0
checks.append('boxed_N10_complete_cut_flux_negative_so_Q_minus_flux_positive')

result={
 'id':'SOURCE-CLOCK-REGULAR-CHAIN-0.1', 'checks_passed':True,'checks':checks,
 'original_action':'F4(C)-sum(r)/2-beta/4*sum_{i<j}b_ij*(r_j*(Tj-Ti)^2+(qj-qi)^2)',
 'beta':serial(beta),'interval_coefficients':[1,-9,16,-8],'layer_moments':[serial(x) for x in moments],
 'affine_family':affine,'Delta':serial(Delta),'Delta_decimal':str(s.N(Delta,25)),
 'clock_recursion':serial(nextclock),'denominator_required_nonzero':True,
 'recursion_linearized_polynomial':str(clock_char),'growing_real_multiplier_interval':['-6','-5'],
 'recursion_scope':'Algebraic stationary-field continuation on a fixed order; not stable physical Cauchy evolution.',
 'boxed_N9':{'a':serial(a9),'a_decimal':str(s.N(a9,25)),'C4':0,'clock_Euler4':0,'constraint_derivative':serial(der9),'scalar_H44':0},
 'boxed_N10':{'clock':'(-1,-a,-b,-1/4,-d,d,1/4,b,a,1)','free_nodes':[4,5],
    'boundary_nodes':[0,1,2,3,6,7,8,9],'density':'r_j=rho with 0<rho<1','scalar':'q_j=0',
    'a_definition':str(a),'quartic_P':str(P.as_expr()),'b_of_d':str(b_of_d),
    'd_interval':dbox.bounds(),'b_interval':bbox.bounds(),'a_interval':abox.bounds(),
    'root_existence':'opposite rationally enclosed endpoint signs; polynomial derivative interval excludes zero',
    'P_at_left_interval':plo.bounds(),'P_at_right_interval':phi.bounds(),'P_derivative_interval':derbox.bounds(),
    'constraint_jacobian_over_beta':str(A10),'constraint_diagonal_over_beta_interval':diagbox.bounds(),
    'all_inner_Euler_equations':'ZERO_EXACT_ON_QUARTIC_ROOT',
    'scalar_hessian':str(scalarH),'scalar_determinant':serial(scalarH.det()),
    'cut_current_over_beta_rho':str(cut_expr),'cut_current_over_beta_rho_interval':cutbox.bounds(),
    'full_positive_particle_edge_flow':False},
 'new_assumptions':['thick four-layer fixed past and future collars','chain control family replaces six-history pilot','directed boundary clock data and positive terminal densities'],
 'unchanged':['full action formula','beta','massless scalar','positive density range (0,1)','clock box [-1,1] for boxed witnesses'],
 'not_established':['physical quantum pairing','physical mass normalization','four-dimensional continuum approximation','order/metric evolution','physical geometry response','stable clock Cauchy evolution','global exterior','singularity resolution'],
 'new_large_integrations':0,
}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'checks_passed':True,'groups':len(checks),'boxed_N10':'regular stationary field witness on fixed chain','geometry_dynamics':'NOT_DERIVED'},indent=2))
