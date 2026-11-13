#!/usr/bin/env python3
"""Independent exact checks; no amplitude quadrature and no upstream imports."""
from pathlib import Path
import hashlib
import itertools
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
beta=4/s.sqrt(6)
b=[1,-9,16,-8]
def zero(x):
    assert s.simplify(s.expand(x))==0,x
def closure(edges):
    e=set(edges)
    while True:
        ee=e|{(i,k) for i,j in e for jj,k in e if j==jj}
        if ee==e:return e
        e=ee
def interval(e,i,j):
    return sum((i,k) in e and (k,j) in e for k in range(6))

common={(0,1),(0,2),(1,4),(1,5),(2,4),(2,5)}
t=s.symbols('t0:6',real=True)
r=s.symbols('r0:6',real=True)
rows=[]
for c,added in [(1,{(1,3),(3,4)}),(2,{(1,3),(2,3),(3,4)})]:
    e=closure(common|added)
    orbit=set()
    for swapA,swapR in itertools.product([False,True],repeat=2):
        p=list(range(6))
        if swapA:p[1],p[2]=p[2],p[1]
        if swapR:p[4],p[5]=p[5],p[4]
        orbit.add(tuple(sorted((p[i],p[j]) for i,j in e)))
    assert len(orbit)==(4 if c==1 else 2)
    for order in sorted(orbit):
        e=set(order)
        coef={(i,j):b[interval(e,i,j)] if interval(e,i,j)<4 else 0 for i,j in e}
        C=[1+beta*s.Add(*(v*(t[j]-t[i])**2 for (i,jj),v in coef.items() if j==jj))/2 for j in range(6)]
        S=-s.Add(*(r[j]*C[j] for j in range(6)))/2
        for j in (1,2):zero(C[j]-1-beta*(t[j]-t[0])**2/2)
        zero(S.xreplace({x:-x for x in t})-S)
        assert [(i,j) for i,j in e if i in (4,5) and j in (4,5)]==[]
        past={j:sum(jj==j for i,jj in e) for j in range(6)}
        levels=[{j for j in range(6) if past[j]<=k} for k in range(5)]
        assert all(all(i in D for i,j in e if j in D) for D in levels)
        profile=[len(D) for D in levels]
        assert profile==([1,3,4,5,6] if c==1 else [1,3,3,5,6])
        f4=6-sum(coef.values());assert f4==(9 if c==1 else -7)
        rows.append({'class':c,'F4':f4,'past_cardinality_profile':profile})

# Compact atom-plus-positive density measure supplies a characteristic function,
# not a constraint delta. Equality verified algebraically for nonzero C.
C=s.symbols('C',real=True,nonzero=True)
rr=s.symbols('rr',real=True)
factor=s.Rational(1,2)+s.integrate(s.exp(-s.I*C*rr/2),(rr,0,1))/2
expected=s.Rational(1,2)+(1-s.exp(-s.I*C/2))/(s.I*C)
zero(factor-expected)
# The lower bound proof is analytic: sin(u)/u>=0 for |u|<=pi;
# and sin(u)/u>=-1/pi for |u|>=pi.
density_bound=(1-1/s.pi)/2
assert density_bound.is_positive

# Action shift symmetry does not imply translation invariance of compact measure.
x,a=s.symbols('x a',real=True)
moment=s.integrate((x+a)**2/2,(x,-1,1))
zero(moment-(s.Rational(1,3)+a*a))

# Exact operational non-identifiability witness (new ancilla illustration only).
M0=s.diag(s.Rational(1,2),s.Rational(1,3))
MF=s.diag(s.sqrt(3)/2,2*s.sqrt(2)/3)
zero((M0.T*M0+MF.T*MF-s.eye(2)).norm())
psi=s.Matrix([1,1])/s.sqrt(2)
g=s.Matrix([1,0]);V=s.diag(0,1)
U0=s.eye(2);U1=s.Matrix([[1,-s.I],[-s.I,1]])/s.sqrt(2)
zero((U1.conjugate().T*U1-s.eye(2)).norm())
probs=[]
for U in (U0,U1):
    state=s.kronecker_product(psi,g)
    p=[]
    for M in (M0,MF):
        out=s.kronecker_product(M,U)*state
        p.append(s.simplify((out.conjugate().T*out)[0]))
    probs.append(p)
assert probs==[[s.Rational(13,72),s.Rational(59,72)]]*2
means=[s.simplify((g.T*U.conjugate().T*V*U*g)[0]) for U in (U0,U1)]
assert means==[0,s.Rational(1,2)]

# Independently reproduce the support-preserving nine-chain stationary witness.
aa=s.sqrt(s.Rational(163,256)-s.sqrt(6)/32)
T=[-1,-aa,-s.Rational(1,2),-s.Rational(1,4),0,s.Rational(1,4),s.Rational(1,2),aa,1]
assert 0<aa<1
def chainC(T,j):return 1+beta*s.Add(*(b[d-1]*(T[j]-T[j-d])**2 for d in range(1,min(j,4)+1)))/2
zero(chainC(T,4))
rho=s.symbols('rho',positive=True)
tt=s.symbols('tt0:9',real=True)
S9=-rho*s.Add(*(chainC(tt,j) for j in range(9)))/2
sub=dict(zip(tt,T))
zero(s.diff(S9,tt[4]).subs(sub))
Aprime=s.simplify(s.diff(chainC(tt,4),tt[4]).subs(sub))
zero(Aprime-beta*(16*aa-s.Rational(49,4)))
# aa<3/4 yields A'<-beta/4, with radical comparison reduced to squares.
assert aa**2<s.Rational(9,16)
q=s.symbols('q0:9',real=True)
Sphi=-beta*s.Add(*(b[d-1]*(q[j]-q[j-d])**2 for j in range(9) for d in range(1,min(j,4)+1)))/4
zero(s.diff(Sphi,q[4],q[4]))

# N10 has two fully interior scalar variables and a nonsingular scalar block.
q10=s.symbols('Q0:10',real=True)
Sphi10=-beta*s.Add(*(b[d-1]*(q10[j]-q10[j-d])**2 for j in range(10) for d in range(1,min(j,4)+1)))/4
H=s.hessian(Sphi10,[q10[4],q10[5]])
assert H==s.Matrix([[0,beta/2],[beta/2,0]])
zero(H.det()+beta**2/4)

# General block-Hessian determinant checked symbolically for the first two sizes.
h,A=s.symbols('h A',real=True)
assert s.Matrix([[h,-A/2],[-A/2,0]]).det()==-A*A/4
a11,a21,a22,h11,h12,h22=s.symbols('a11 a21 a22 h11 h12 h22')
AA=s.Matrix([[a11,0],[a21,a22]]);HH=s.Matrix([[h11,h12],[h12,h22]])
Hblock=HH.row_join(-AA.T/2).col_join((-AA/2).row_join(s.zeros(2)))
zero(Hblock.det()-AA.det()**2/16)

result={'id':'CST-DUST-INDEPENDENT-AUDIT-0.1','all_checks_pass':True,
 'source_audit':{'six_history_rows':rows,'A_stationary_obstruction':'only freely varied positive A densities','clock_parity_scope':'odd amplitude insertions with reflection-even full support','R_constancy_scope':'intrinsic R order only'},
 'density_measure':{'factor':str(expected),'real_part_lower_bound':str(density_bound),'constraint_delta':False},
 'compact_clock_measure':{'shifted_second_moment':str(moment),'globally_shift_invariant':False},
 'operational_identifiability':{'record_probabilities':[[str(v) for v in p] for p in probs],'geometry_means':[str(v) for v in means],'same_record_probabilities':True,'different_geometry_means':True,'scope':'independent-ancilla witness, not a same-action CST counterexample'},
 'nine_chain':{'clocks':[str(v) for v in T],'density_constraint':0,'inner_clock_EL':0,'constraint_T_derivative':str(Aprime),'within_original_clock_box':True,'full_scalar_regular':False},
 'ten_chain_scalar_block':{'matrix':str(H),'determinant':str(H.det()),'regular':True,'scope':'algebraic block, no physical pairing or continuum claim'},
 'block_hessian_determinants':'m=1 and m=2 symbolically verified; general identity (-1)^m det(A)^2/4^m',
 'new_amplitude_integrations':0,'physical_geometry_dynamics_derived':False}
(ROOT/'results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS independent audit: six histories, density/support, identifiability, nine-chain and scalar/Hessian controls')
