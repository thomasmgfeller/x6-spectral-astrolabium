#!/usr/bin/env python3
"""Independent exact audit of N11 source separation and boundary Legendre maps.

Reconstructs all intervals from the two orders, without importing peer scripts.
No quadrature, physical Hilbert-space assertion, or universal no-go is made.
"""
from pathlib import Path
from functools import reduce
from math import gcd
import json
import sympy as s

OUT=Path(__file__).resolve().parent
P=list(range(4)); I=[4,5,6]; F=list(range(7,11))
u=s.symbols('u0:11',real=True); r=s.symbols('r0:11',real=True)
q=s.symbols('q0:11',real=True); rho=s.symbols('rho',positive=True)
rp,rf=s.symbols('rho_P rho_F',real=True)
qp=s.Matrix(s.symbols('a0:4',real=True)); pp=s.Matrix(s.symbols('b0:4',real=True))
qf=s.Matrix(s.symbols('c0:4',real=True)); pf=s.Matrix(s.symbols('d0:4',real=True))
initial=list(qp)+list(pp); final=list(qf)+list(pf)
J=s.zeros(8);J[:4,4:]=s.eye(4);J[4:,:4]=-s.eye(4)
allrel={(i,j) for i in range(11) for j in range(i+1,11)}
orders=[('chain',allrel),('variant',allrel-{(4,5),(5,6)})]

def canonical_linear(expr,variables):
    row=[s.expand(expr).coeff(v) for v in variables]
    den=s.ilcm(*[v.q for v in row])
    ints=[int(v*den) for v in row]
    div=reduce(gcd,ints)
    ints=[v//div for v in ints]
    if next(v for v in ints if v)!=abs(next(v for v in ints if v)):
        ints=[-v for v in ints]
    return s.Matrix([ints])

def strings(M):return [[str(v) for v in row] for row in M.tolist()]
rows=[]; scalar=[]
for name,rel in orders:
    assert all((a,c) in rel for a,b in rel for bb,c in rel if b==bb)
    coeff={}
    for a,b in rel:
        n=sum((a,k) in rel and (k,b) in rel for k in range(11))
        coeff[a,b]=[1,-9,16,-8][n] if n<4 else 0
    C=[s.expand(1+sum(s.Rational(v,19)*(u[b]-u[a])**2
                      for (a,b),v in coeff.items() if b==j)) for j in range(11)]
    S=-sum(r[j]*C[j] for j in range(11))/2
    # Past coefficients depend only on past clocks, identically before substitution.
    assert all(not (set(C[j].free_symbols)&set(u[4:])) for j in P)
    CP=[s.simplify(C[j].subs({u[k]:k for k in P})) for j in P]
    assert CP==[1,s.Rational(20,19),-s.Rational(16,19),s.Rational(128,19)]
    assert sum(CP)==s.Rational(151,19)
    prepared=s.expand(S.subs({r[j]:rp for j in P}|{r[j]:rf for j in F})
                        .subs({u[j]:j for j in P+F}))
    assert s.diff(prepared,rp)==-s.Rational(151,38)
    assert s.diff(prepared,rp,rf)==0
    assert all(s.diff(prepared,rp,u[j])==0 for j in I)

    L=s.zeros(11)
    for (a,b),v in coeff.items():
        L[a,a]+=v;L[b,b]+=v;L[a,b]-=v;L[b,a]-=v
    H=-L/2  # H divided by beta; canonical variables are (q,pi=p/beta).
    A=H.extract(I+P,I+F)
    rhs=(-H.extract(I,P)*qp).col_join(-pp-H.extract(P,P)*qp)
    Ap=H.extract(I+F,I+P)
    rhsp=(-H.extract(I,F)*qf).col_join(pf-H.extract(F,F)*qf)
    srow={'order':name,'scalar_Legendre_rank':A.rank(),
          'scalar_Legendre_determinant_divided_by_beta7':str(A.det())}
    if name=='chain':
        assert A.det()==-16384
        solved=A.inv()*rhs
        allq=s.zeros(11,1)
        for j,v in zip(P,qp):allq[j]=v
        for j,v in zip(I+F,solved):allq[j]=v
        outgoing=allq.extract(F,[0]).col_join((H*allq).extract(F,[0]))
        M0=outgoing.jacobian(initial)
        assert M0*J*M0.T==J
        srow['endpoint_map_in_q_pi']=strings(M0)
        srow['endpoint_map_symplectic']=True
    else:
        assert A.rank()==6 and Ap.rank()==6
        pre=canonical_linear((A.T.nullspace()[0].T*rhs)[0],initial)
        post=canonical_linear((Ap.T.nullspace()[0].T*rhsp)[0],final)
        # Independently normalized integer representatives, positive first coefficient.
        assert pre==s.Matrix([[128,-241,-119,232,46,32,16,0]])
        assert post==s.Matrix([[232,-119,-241,128,0,-16,-32,-46]])
        pulled=post*M0
        bracket=(pre*J*pulled.T)[0]
        assert bracket==-s.Rational(52625,32)
        srow.update({'pre_constraint_q_pi':strings(pre),
                     'post_constraint_q_pi':strings(post),
                     'chain_pullback_of_post_constraint':strings(pulled),
                     'pre_vs_chain_pullback_Poisson_bracket_q_pi':str(bracket),
                     'original_q_p_bracket':str(bracket)+'/beta',
                     'scope':'No common nonzero simultaneous strong-constraint vector on a compatible CCR domain; not a no-go for second-class reduction or other boundary contracts.'})
    scalar.append(srow)

    # Full clock/density boundary Legendre relation, retaining all inner variables.
    inner=[u[j] for j in I]+[r[j] for j in I]
    past=[u[j] for j in P]+[r[j] for j in P]
    future=[u[j] for j in F]+[r[j] for j in F]
    raw=s.Matrix([s.diff(S,v) for v in inner+past]).jacobian(inner+future)
    assert raw[10:,:]==s.zeros(4,14)  # Exact, at every field configuration.
    point={u[j]:j for j in range(11)}|{r[j]:rho for j in range(11)}
    if name=='variant':point.update({u[4]:4,u[5]:4,u[6]:5,r[4]:2*rho})
    M=raw.subs(point)
    for j in range(6,14):M[j,:]=-M[j,:]
    fixed=M[:10,:10]
    HII=s.hessian(S,inner).subs(point)
    assert HII.det()==-s.Rational(1,19**6)
    if name=='chain':
        assert fixed.det()==2**27*rho**4/s.Integer(19)**10
        assert M.rank()==10
    else:
        assert fixed.det()==0 and fixed.rank()==9 and M.rank()==9
        direction=s.Matrix([0]*6+[0,s.Rational(8,23),s.Rational(16,23),1])
        assert fixed*direction==s.zeros(10,1)
        # Integrate the tangent null direction: it is an exact distinct-output family.
        alpha=s.symbols('alpha',real=True)
        shifted=point|{u[j]:point[u[j]]+alpha*v for j,v in zip(F,[0,8,16,23])}
        assert all(s.simplify(s.diff(S,v).subs(shifted))==0 for v in inner)
        assert all(s.simplify(s.diff(S,v).subs(shifted)-s.diff(S,v).subs(point))==0 for v in past)
        action_change=s.factor(S.subs(shifted)-S.subs(point))
        assert action_change==-alpha*rho*(932*alpha+217)/19
        dpuf=s.Matrix([s.simplify(s.diff(S,u[j]).subs(shifted)-s.diff(S,u[j]).subs(point)) for j in F])
        assert dpuf==alpha*rho*s.Matrix([232,-119,-241,128])/19
        dprf=s.Matrix([s.simplify(s.diff(S,r[j]).subs(shifted)-s.diff(S,r[j]).subs(point)) for j in F])
        expected=s.Matrix([0,16*alpha*(2*alpha-1),-8*alpha*(244*alpha+173),13*alpha*(76*alpha+91)])/19
        assert (dprf-expected).applyfunc(s.simplify)==s.zeros(4,1)
        nonlinear={'future_clock_direction':[0,8,16,23],
                   'all_inner_Euler_residuals_zero':True,
                   'all_initial_canonical_data_unchanged':True,
                   'action_change':str(action_change),
                   'future_clock_momentum_change':strings(dpuf),
                   'future_density_momentum_change':strings(dprf),
                   'gauge_equivalence_derived':False}
    rows.append({'order':name,'past_C_at_affine_clock':[str(v) for v in CP],
                 'past_action_derivative':str(s.diff(prepared,rp)),
                 'exact_zero_past_density_rows':4,
                 'full_clock_density_Legendre_rank_at_stationary_family':M.rank(),
                 'fixed_future_density_minor_determinant':str(s.factor(fixed.det())),
                 'inner_clock_density_Hessian_determinant':str(HII.det()),
                 'exact_distinct_output_family':nonlinear if name=='variant' else None})

# A surviving conditional common scalar reduction. This deliberately does NOT
# impose both pre and pulled-back post constraints as simultaneous strong kernels.
# Input section q0=0, Apre=0; output section q10=0, Apost=0.
J6=s.zeros(6);J6[:3,3:]=s.eye(3);J6[3:,:3]=-s.eye(3)
Ein=s.zeros(8,6)
for j in range(3):Ein[j+1,j]=1;Ein[j+5,j+3]=1
Ein[4,:]=s.Matrix([[s.Rational(241,46),s.Rational(119,46),-s.Rational(232,46),-s.Rational(32,46),-s.Rational(16,46),0]])
assert pre*Ein==s.zeros(1,6) and Ein.T*J*Ein==J6
B=post*M0
k=(pre*J*B.T)[0]
gaugefixed_input=Ein+(J*pre.T)*(B*Ein)/k
assert pre*gaugefixed_input==s.zeros(1,6) and B*gaugefixed_input==s.zeros(1,6)
rawout0=M0*gaugefixed_input
fixedout0=rawout0-(J*post.T)*rawout0[3,:]/(J*post.T)[3]
outindices=[0,1,2,4,5,6]
M0red=fixedout0.extract(outindices,list(range(6)))
assert post*fixedout0==s.zeros(1,6) and fixedout0[3,:]==s.zeros(1,6)
assert M0red.T*J6*M0red==J6
# At loop exit A,H are the independently reconstructed variant matrices.
rhsred=(-H.extract(I,P)*Ein[:4,:]).col_join(-Ein[4:,:]-H.extract(P,P)*Ein[:4,:])
gauge=s.zeros(1,7);gauge[0,6]=1
zred,parameters=A.col_join(gauge).gauss_jordan_solve(rhsred.col_join(s.zeros(1,6)))
assert parameters.rows==0
allqred=s.zeros(11,6)
for j,row in zip(P,range(4)):allqred[j,:]=Ein[row,:]
for j,row in zip(I+F,range(7)):allqred[j,:]=zred[row,:]
out1=allqred.extract(F,list(range(6))).col_join((H*allqred).extract(F,list(range(6))))
assert post*out1==s.zeros(1,6) and out1[3,:]==s.zeros(1,6)
M1red=out1.extract(outindices,list(range(6)))
assert M1red.T*J6*M1red==J6
assert M0red!=M1red
unitaries=[]
for name,Mred in [('chain',M0red),('variant',M1red)]:
    Ar=Mred[:3,:3];Br=Mred[:3,3:];Cr=Mred[3:,:3]
    assert Ar.det()!=0
    lower=Cr*Ar.inv();upper=Ar.inv()*Br
    assert lower==lower.T and upper==upper.T
    shear_lower=s.eye(6);shear_lower[3:,:3]=lower
    dilation=s.diag(Ar,Ar.inv().T)
    shear_upper=s.eye(6);shear_upper[:3,3:]=upper
    assert shear_lower*dilation*shear_upper==Mred
    unitaries.append({'order':name,'A_determinant':str(Ar.det()),
                       'position_chirp_matrix_C_Ainv':strings(lower),
                       'momentum_chirp_matrix_Ainv_B':strings(upper),
                       'exact_lower_dilation_upper_factorization':True,
                       'L2_construction':'U=position_chirp(C*A^-1) times unitary_dilation(A) times Fourier_momentum_chirp(A^-1*B). Each factor unitary under declared Lebesgue L2; no inverse of B required.'})
reduced={'input_section':'q0=0 and Apre=0; coordinates (q1,q2,q3,pi1,pi2,pi3)',
         'output_section':'q10=0 and Apost=0; coordinates (q7,q8,q9,pi7,pi8,pi9)',
         'chain_extra_operation':'Gauge-fix B=Apost composed with M0 to zero along Apre flow before evolution; then quotient output.',
         'chain_reduced_map':strings(M0red),'variant_reduced_map':strings(M1red),
         'both_maps_symplectic':True,'maps_distinct':True,
         'chain_reduced_qp_block_determinant':str(M0red[:3,3:].det()),
         'variant_reduced_qp_block_determinant':str(M1red[:3,3:].det()),
         'explicit_unitary_factorizations':unitaries,
         'scope':'Conditional shared scalar three-pair reduction exists. Quantizing these maps requires declared rigging, normalization and phase conventions; full compact dust-clock physical norm is not derived.'}

result={'id':'PHYSICAL-BOUNDARY-INDEPENDENT-AUDIT-0.1','all_checks_pass':True,
        'source_and_clock_density':rows,'scalar_boundary':scalar,
        'source_factorization':'W_c(rho_P,rho_F)=exp(-i*151*rho_P/38)*V_c(rho_F)',
        'source_scope':'Fixed past clocks and common preparations/history weights. Integrating variable clock wavepackets can defeat cancellation.',
        'conditional_common_scalar_reduction':reduced,
        'physical_Hilbert_space_derived':False,'universal_no_go_claimed':False}
(OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS exact independent past-source cancellation, scalar boundary bracket, and clock/density Legendre ranks')
