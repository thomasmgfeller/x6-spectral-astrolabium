#!/usr/bin/env python3
"""Independent source-dependent geometry-action comparison, exact rational algebra."""
from pathlib import Path
import json
import sympy as s

ROOT=Path(__file__).resolve().parent
N=11;I=[4,5,6];B=[0,1,2,3,7,8,9,10]
weights=[1,-9,16,-8]
rho=s.symbols('rho',positive=True)
u=s.symbols('u0:11',real=True);r=s.symbols('r0:11',real=True)
allpairs={(i,j) for i in range(N) for j in range(i+1,N)}
rows=[]
for name,edges,inner_u,inner_r in [
    ('chain',allpairs,[4,5,6],[1,1,1]),
    ('two_cover_deletion',allpairs-{(4,5),(5,6)},[4,4,5],[2,1,1])]:
    assert all((i,k) in edges for i,j in edges for jj,k in edges if j==jj)
    coefficient={}
    for i,j in edges:
        interval=sum((i,k) in edges and (k,j) in edges for k in range(N))
        coefficient[i,j]=weights[interval] if interval<4 else 0
    F=N-sum(coefficient.values())
    # T_j=Delta*u_j, Delta^2=2/(19*beta).
    C=[1+s.Add(*(v*(u[j]-u[i])**2 for (i,jj),v in coefficient.items() if jj==j))/19 for j in range(N)]
    S=F-s.Add(*(r[j]*C[j] for j in range(N)))/2
    uu=list(range(N));rr=[rho]*N
    for k,j in enumerate(I):uu[j]=inner_u[k];rr[j]=inner_r[k]*rho
    sub=dict(zip(u,uu))|dict(zip(r,rr))
    Ci=[s.simplify(C[j].subs(sub)) for j in I]
    Ei=[s.simplify(s.diff(S,u[j]).subs(sub)) for j in I]
    assert Ci==[0,0,0] and Ei==[0,0,0]
    on_shell=s.simplify(S.subs(sub))
    A=s.Matrix([C[j] for j in I]).jacobian([u[j] for j in I]).subs(sub)
    assert A.det()==-s.Rational(8,6859)
    Q=s.zeros(N) # Q=2*H_phi/beta
    for (i,j),v in coefficient.items():
        Q[i,i]-=v;Q[j,j]-=v;Q[i,j]+=v;Q[j,i]+=v
    HII=Q.extract(I,I);full_cols=Q.extract(range(N),I)
    assert full_cols.rank()==3
    nullspace=HII.nullspace()
    for z in nullspace:assert Q.extract(B,I)*z!=s.zeros(len(B),1)
    rows.append({'name':name,'F4':F,'inner_u':inner_u,
      'inner_density_multipliers':inner_r,'inner_constraints':[str(v) for v in Ci],
      'inner_clock_EL':[str(v) for v in Ei], 'on_shell_action':str(on_shell),
      'constraint_jacobian':str(A),'constraint_jacobian_determinant':str(A.det()),
      'scaled_scalar_inner_block':str(HII),'scaled_scalar_inner_determinant':str(HII.det()),
      'full_scalar_inner_column_rank':full_cols.rank(),
      'scalar_inner_nullspace':[str(v) for v in nullspace],
      'all_inner_nulls_couple_to_boundary':True})
    if name=='chain':S1=on_shell;outer_order={(i,j) for i,j in edges if i in B and j in B}
    else:S2=on_shell;assert {(i,j) for i,j in edges if i in B and j in B}==outer_order
assert s.simplify(S1-10+151*rho/38)==0
assert s.simplify(S2-18+105*rho/38)==0
delta=s.simplify(S2-S1);assert delta==8+23*rho/19
beta=4/s.sqrt(6);Delta=s.sqrt(2/(19*beta))
assert 5*Delta>1
result={'id':'CST-DUST-N11-INDEPENDENT-AUDIT-0.1','all_checks_pass':True,
 'same_outer_order_and_clock_density_scalar_data':True,'rows':rows,
 'action_difference':str(delta),'derivative_wrt_common_source_density':str(s.diff(delta,rho)),
 'density_domain':'0<rho<1/2','clock_halfwidth_required':str(5*Delta),
 'outside_original_clock_box':True,'scalar_pairing':'Gaussian on all 8 boundary fields; Abel-regulated interior, full column rank excludes unpaired null',
 'scope':'two stationary geometry-action branches at shared boundary; not physical transition probabilities or an effective gravitational field equation',
 'new_amplitude_integrations':0,'physical_evolution_derived':False}
(ROOT/'n11_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS N11: two stationary common-boundary geometries, exact source-sensitive action difference, regular dust Jacobians and paired scalar null')
