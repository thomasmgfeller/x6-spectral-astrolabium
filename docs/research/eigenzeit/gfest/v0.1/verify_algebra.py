"""GFEST draft: exact algebra controls and finite numerical diagnostics.
Not a proof assistant, a uniform domain certificate, or a statistical calibration.
"""
import json, math, platform
from pathlib import Path
import sympy as s
import numpy as np
import mpmath as mp

HERE=Path(__file__).resolve().parent
J=s.diag(1,-1,-1)
d=3
def q(x,y):
    v=x-y
    return (v.T*J*v)[0]
def phi(x):
    return s.Matrix([1,*x,*[v*v for v in x],x[0]*x[1],x[0]*x[2],x[1]*x[2]])
def rhs(G):
    H=G.inv()
    return s.Matrix([0,0,0,0,*[-2*H[i,i] for i in range(3)],-2*H[0,1],-2*H[0,2],-2*H[1,2]])
def reconstruct(landmarks,points):
    l0=landmarks[0]
    G=s.Matrix(3,3,lambda i,j:(q(landmarks[i+1],l0)+q(landmarks[j+1],l0)-q(landmarks[i+1],landmarks[j+1]))/2)
    B=s.Matrix.hstack(*[x-l0 for x in landmarks[1:]])
    assert G==B.T*J*B
    def v(x):return s.Matrix([(q(x,l0)+q(li,l0)-q(x,li))/2 for li in landmarks[1:]])
    cc=[G.inv()*(v(x)-v(points[0])) for x in points]
    assert all(c==B.inv()*(x-points[0]) for c,x in zip(cc,points))
    A=s.Matrix.hstack(*[phi(c) for c in cc]); b=rhs(G)
    assert A.rank()==10
    w=A.T*(A*A.T).inv()*b
    Ap=s.Matrix.hstack(*[phi(x-points[0]) for x in points]);bp=rhs(J)
    wp=Ap.T*(Ap*Ap.T).inv()*bp
    assert w==wp and A*w==b
    return G,cc,A,b,w

landmarks=[s.Matrix(v) for v in ((10,0,0),(12,1,0),(14,0,1),(16,0,0))]
points=[s.zeros(3,1)]
for i in range(3):
    for sign in (-1,1):
        v=s.zeros(3,1);v[i]=sign;points.append(v)
for i,j in ((0,1),(0,2),(1,2)):
    v=s.zeros(3,1);v[i]=v[j]=1;points.append(v)
points += [s.Matrix(v) for v in ((1,1,1),(-1,1,0),(1,-1,1),(0,1,-1),(-1,0,1),(2,0,0),(0,2,0))]
assert len(points)==17
Gp,cp,A,b,w=reconstruct(landmarks,points)
moved_landmarks=[x+s.Matrix([s.Rational(i+1,100),s.Rational(i-1,200),s.Rational(2-i,300)]) for i,x in enumerate(landmarks)]
moved_points=[x+s.Matrix([s.Rational((i%3)-1,150),s.Rational((i%4)-2,180),s.Rational((i%5)-2,210)]) for i,x in enumerate(points)]
Gq,cq,At,bt,wt=reconstruct(moved_landmarks,moved_points)
assert bt!=b
Apinv=A.T*(A*A.T).inv();Bpinv=At.T*(At*At.T).inv();E=At-A
assert Bpinv-Apinv==-Bpinv*E*Apinv+(s.eye(17)-Bpinv*At)*E.T*(A*A.T).inv()
def required_q(ls,ps):
    return [q(ls[i],ls[j]) for i in range(4) for j in range(i)]+[q(x,l) for x in ps for l in ls]
qs,qt=required_q(landmarks,points),required_q(moved_landmarks,moved_points)
assert min(qs+qt)>0
conv=lambda x:np.array(x,dtype=float)
Q=float(max(qs+qt));qmin=float(min(qs+qt));gamma=.9*min(np.linalg.svd(conv(Gp),compute_uv=False)[-1],np.linalg.svd(conv(Gq),compute_uv=False)[-1])
kappa=.9*min(np.linalg.svd(conv(A),compute_uv=False)[-1],np.linalg.svd(conv(At),compute_uv=False)[-1])
R=np.sqrt(d)*Q/gamma;M=np.sqrt(17*(1+R*R+R**4));aG=1.5*d
Cc=2*np.sqrt(d)/gamma+aG*np.sqrt(d)*Q/gamma**2
CA=4*np.sqrt(d+(d+3)*R**2)*Cc
Cb=2*np.sqrt(d)*aG/gamma**2;B0=2*np.sqrt(d)/gamma
Cw=2*B0*CA*kappa**-2+Cb/kappa
delta=float(max(abs(x-y) for x,y in zip(qs,qt)))
assert np.linalg.norm(conv(Gq-Gp),2)<=aG*delta
assert max(np.linalg.norm(conv(x-y)) for x,y in zip(cp,cq))<=Cc*delta
assert np.linalg.norm(conv(At-A),2)<=CA*delta
assert np.linalg.norm(conv(bt-b))<=Cb*delta
assert np.linalg.norm(conv(wt-w))<=Cw*delta
wmin=np.sqrt(2/d)/(Q*M)
assert min(np.linalg.norm(conv(w)),np.linalg.norm(conv(wt)))>=wmin

t,x,y=s.symbols('t x y',real=True)
ph=phi(s.Matrix([t,x,y]));Dph=ph.jacobian([t,x,y])
assert s.expand(sum(v*v for v in Dph)-(3+6*(t*t+x*x+y*y)))==0
scaled=reconstruct([2*z for z in landmarks],[2*z for z in points])
assert scaled[-1]==w/4

mp.mp.dps=90
poisson=[]
for ma,mb in [(0,0),(0,mp.mpf('.1')),(mp.mpf('.2'),mp.mpf('.3')),(1,2),(4,4),(10,11),(20,22),(mp.mpf('.00001'),mp.mpf('.00002'))]:
    ma,mb=mp.mpf(ma),mp.mpf(mb);N=400
    pa,pb=mp.exp(-ma),mp.exp(-mb);tv=abs(pa-pb)/2;aff=mp.sqrt(pa*pb)
    for k in range(1,N+1):
        pa*=ma/k;pb*=mb/k;tv+=abs(pa-pb)/2;aff+=mp.sqrt(pa*pb)
    af=mp.exp(-(mp.sqrt(ma)-mp.sqrt(mb))**2/2)
    assert abs(aff-af)<mp.mpf('1e-75')
    assert 1-af<=tv+mp.mpf('1e-75')
    Lam=max(ma,mb)
    if tv==0:bound=mp.mpf(0)
    else:bound=min(Lam,mp.log1p(mp.exp(Lam)*tv),2*mp.sqrt(Lam)*mp.sqrt(-2*mp.log1p(-tv)))
    assert abs(ma-mb)<=bound+mp.mpf('1e-65')
    poisson.append({'mu':str(ma),'nu':str(mb),'tv_diagnostic':str(tv),'mean_bound':str(bound)})

result={'status':'PASS','exact_rational_configurations':3,'all_stencil_nodes':17,'all_landmarks':4,'moment_rows':10,'gram_reconstruction':True,'coordinate_reconstruction':True,'intrinsic_cartesian_minimum_norm_identity':True,'moving_landmark_rhs_change_detected':True,'physical_scale_weight_law':True,'symbolic_monomial_jacobian_identity':True,'finite_endpoint_inequalities_checked':6,'poisson_pairs':poisson,'numerical_constants_not_certified':{'q_min':qmin,'Q':Q,'gamma':gamma,'kappa':kappa,'delta_q':delta,'actual_absolute_gap':float(np.linalg.norm(conv(wt-w))),'very_conservative_absolute_bound':Cw*delta},'versions':{'python':platform.python_version(),'sympy':s.__version__,'numpy':np.__version__,'mpmath':mp.__version__},'limits':'Exact rational identities and numerical diagnostics only. No uniform X6 parameter-domain certificate, no formal proof-assistant verification, no independent reviewer.'}
result['exact_pseudoinverse_identity']=True
(HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
