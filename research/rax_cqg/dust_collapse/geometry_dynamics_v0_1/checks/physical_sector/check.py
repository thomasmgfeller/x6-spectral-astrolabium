"""Exact dust and scalar regularity of the buffered affine-chain candidate.
Uses the inherited pair action; never treats density Euler equations as gauge
constraints and never constructs a physical Hilbert space from a chosen norm.
"""
from pathlib import Path
import json
import sympy as s

HERE=Path(__file__).resolve().parent
b={1:s.Integer(1),2:s.Integer(-9),3:s.Integer(16),4:s.Integer(-8)}
beta=4/s.sqrt(6)
Delta=s.sqrt(2/(19*beta))
assert sum(b.values())==0
assert sum(k*v for k,v in b.items())==-1
assert sum(k*k*v for k,v in b.items())==-19
out=[]
for m in range(1,5):
    N=m+8
    x=s.symbols('x:'+str(N),real=True)
    r=s.symbols('r:'+str(N),real=True)
    q=s.symbols('q:'+str(N),real=True)
    I=list(range(4,N-4))
    C=[1+s.Rational(1,19)*sum(b[d]*(x[j]-x[j-d])**2 for d in b if d<=j) for j in range(N)]
    Sd=-sum(r[j]*C[j] for j in range(N))/2
    # S_phi/beta; no density weighting and no scalar mass added.
    Sphi_over_beta=-sum(b[d]*(q[j]-q[j-d])**2 for j in range(N) for d in b if d<=j)/4
    point={**{x[j]:s.Rational(2*j-(N-1),2) for j in range(N)},
           **{r[j]:s.Rational(1,2) for j in range(N)},
           **{q[j]:0 for j in range(N)}}
    assert all(s.simplify(C[j].subs(point))==0 for j in I)
    assert all(s.simplify(s.diff(Sd,x[j]).subs(point))==0 for j in I)
    assert all(s.simplify(s.diff(Sphi_over_beta,q[j]).subs(point))==0 for j in I)
    A=s.Matrix([[s.diff(C[j],x[k]).subs(point) for k in I] for j in I])
    assert all(A[j,k]==0 for j in range(m) for k in range(j+1,m))
    assert all(A[j,j]==-s.Rational(2,19) for j in range(m))
    assert A.det()==(-s.Rational(2,19))**m
    dustvars=[x[j] for j in I]+[r[j] for j in I]
    Hd=s.hessian(Sd,dustvars).subs(point)
    assert Hd[m:,m:]==s.zeros(m,m)
    assert Hd[m:,:m]==-A/2 and Hd[:m,m:]==-A.T/2
    assert s.simplify(Hd.det()-(-1)**m*A.det()**2/4**m)==0
    Hp=s.hessian(Sphi_over_beta,[q[j] for j in I]).subs(point)
    H=s.diag(Hd,beta*Hp)
    row={'N':N,'inner_nodes':I,'C_jacobian_in_scaled_clocks':[[str(v) for v in A.row(j)] for j in range(m)],
         'dust_Hessian_determinant_scaled_clocks':str(Hd.det()),
         'dust_Hessian_inertia':[m,m,0],
         'scalar_Hessian_divided_by_beta':[[str(v) for v in Hp.row(j)] for j in range(m)],
         'scalar_Hessian_determinant_divided_by_beta_power_m':str(Hp.det()),
         'joint_Hessian_nondegenerate':H.det()!=0,
         'outer_clock_max_abs_squared':str(s.simplify(((N-1)*Delta/2)**2)),
         'original_clock_box_supported':bool(s.simplify(((N-1)*Delta/2)**2)<1),
         'local_C_coarea_factor_in_scaled_clocks':str(1/abs(A.det()))}
    out.append(row)
    if m==2:
        assert Hp==s.Matrix([[0,s.Rational(1,2)],[s.Rational(1,2),0]])
        assert Hd.det()==s.Rational(1,19**4)
        # Interior dt/2 and positive density dr/2 give a_star=(Delta/4)^m.
        a_star=(Delta/4)**m
        sqrt_abs_detH=beta/(2*19**2)
        prefactor=s.simplify(a_star/sqrt_abs_detH)
        assert prefactor==s.Rational(57,32)
        stationary_phase={'dimension':6,'signature':0,
          'assumption':'Compact smooth interior localization equal to one near this positive saddle; fixed prepared boundary; semiclassical parameter epsilon -> 0+. Not a physical pairing or full-amplitude result.',
          'measure':'Each inner clock dt/2, positive density dr/2, scalar dq; x=T/Delta.',
          'coefficient_of_(2pi_epsilon)^3_exp(i_Sstar/epsilon)':'57/32',
          'relative_remainder':'O(epsilon) for a smooth localized nondegenerate interior saddle',
          'full_original_measure_or_history_sum_evaluated':False}

# Finite-dimensional arbitrary metric repair is not unique: two exact choices.
A=s.Matrix([[1,1],[0,1],[1,0]])
Aplus=(A.T*A).inv()*A.T
P=s.eye(3)-A*Aplus
metric_examples=[]
for GE,scale in [(s.eye(2),s.Integer(1)),(s.diag(2,3),s.Integer(7))]:
    GF=Aplus.T*GE*Aplus+scale*P
    assert s.simplify(A.T*GF*A-GE)==s.zeros(2,2)
    assert all(v>0 for v in [GF[:j,:j].det() for j in range(1,4)])
    metric_examples.append({'input_metric':[[str(v) for v in GE.row(j)] for j in range(2)],
                            'output_metric':[[str(v) for v in GF.row(j)] for j in range(3)]})
# Independent reconstruction of the new N11 same-boundary order pair.
rho=s.symbols('rho', positive=True)
pair=[]
for removed,ui,ri in [(set(),[4,5,6],[rho,rho,rho]),
                       ({(4,5),(5,6)},[4,4,5],[2*rho,rho,rho])]:
    n=11;inner=[4,5,6];boundary=[j for j in range(n) if j not in inner]
    order={(i,j) for i in range(n) for j in range(i+1,n)}-removed
    assert all((i,k) in order for i,j in order for jj,k in order if j==jj)
    coeff={}
    for i,j in order:
        count=sum((i,k) in order and (k,j) in order for k in range(n))
        coeff[i,j]=[1,-9,16,-8][count] if count<4 else 0
    ux=s.symbols('y0:3',real=True);rx=s.symbols('z0:3',real=True)
    us=list(map(s.Integer,range(n)));rs=[rho]*n
    for j,y,z in zip(inner,ux,rx):us[j]=y;rs[j]=z
    constraints=[1+s.Rational(1,19)*sum(v*(us[j]-us[i])**2 for (i,j),v in coeff.items() if j==k) for k in range(n)]
    F=n-sum(coeff.values());act=F-sum(rs[j]*constraints[j] for j in range(n))/2
    sol={**dict(zip(ux,ui)),**dict(zip(rx,ri))}
    assert all(s.simplify(s.diff(act,x).subs(sol))==0 for x in (*ux,*rx))
    A=s.Matrix([[s.diff(constraints[j],y).subs(sol) for y in ux] for j in inner])
    Hd=s.hessian(act,[*ux,*rx]).subs(sol)
    assert A.det()==(-s.Rational(2,19))**3
    assert Hd.det()==-s.Rational(1,19**6)
    L=s.zeros(n)
    for (i,j),v in coeff.items():L[i,i]+=v;L[j,j]+=v;L[i,j]-=v;L[j,i]-=v
    LII=L.extract(inner,inner);LIB=L.extract(inner,boundary)
    assert L[:,inner].rank()==3
    nulls=LII.nullspace()
    if removed:
        assert nulls==[s.Matrix([0,1,0])]
        assert LIB.T*nulls[0]!=s.zeros(8,1)
    else: assert not nulls
    pair.append({'removed_covers':[list(x) for x in sorted(removed)],'F4':F,
                 'stationary_action':str(s.factor(act.subs(sol))),
                 'dust_Hessian_determinant_in_u_coordinates':str(Hd.det()),
                 'constraint_Coarea_factor_in_u_coordinates':str(1/abs(A.det())),
                 'scalar_internal_nullity':len(nulls),'scalar_full_internal_column_rank':3,
                 'scalar_Gaussian_Abel_pairing_exists':'Follows exactly from full internal column rank: if (E_B+i beta L/2)x=0, its real quadratic form gives x_B=0 and then L[:,I]x_I=0.',
                 'full_physical_pairing_constructed':False})
assert s.simplify(s.sympify(pair[1]['stationary_action'])-s.sympify(pair[0]['stationary_action'])-(8+s.Rational(23,19)*s.Symbol('rho')))==0

result={'status':'PASS_EXACT_FINITE_REGULARITY_AND_SCOPE_CHECKS','chain_checks':out, 'new_N11_pair_independent_checks':pair,
        'stationary_phase_local_diagnostic':stationary_phase,
        'finite_metric_nonuniqueness_examples':metric_examples,
        'derived_physical_Hilbert_space':False,'derived_gauge_constraints':False,
        'new_large_integrations':0,'physical_geometry_status':'HOLD_NOT_DERIVED'}
(HERE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'joint_nondegenerate_by_N':{z['N']:z['joint_Hessian_nondegenerate'] for z in out},'local_prefactor':stationary_phase['coefficient_of_(2pi_epsilon)^3_exp(i_Sstar/epsilon)']}))
