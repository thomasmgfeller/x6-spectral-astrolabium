#!/usr/bin/env python3
"""Independent phase-aware reduced Gaussian/pointer audit.

Uses this audit's own rational maps and delta-generating phase. Gaussian roots
are computed by sequential complex Schur pivots, independently of the peer's
Cholesky-whitened eigenvalue method. No high-dimensional quadrature is used.
"""
from pathlib import Path
import json
import sympy as s
import mpmath as mp

mp.mp.dps=70
OUT=Path(__file__).resolve().parent
PACKAGE=OUT.parents[1]
maps=json.loads((OUT/'results.json').read_text())['conditional_common_scalar_reduction']
kernels=json.loads((OUT/'reduced_kernel_results.json').read_text())
R0=s.Matrix(maps['chain_reduced_map']);R1=s.Matrix(maps['variant_reduced_map'])
def numeric(M):
    return mp.matrix([[mp.mpc(str(s.re(z).evalf(75)),str(s.im(z).evalf(75))) for z in row] for row in M.tolist()])
def root(Q):
    """Gaussian integral branch via successive Schur pivots with Re(pivot)>0."""
    M=numeric(Q);answer=mp.mpc(1);pivots=[]
    while M.rows:
        v=M[0,0]
        assert mp.re(v)>0
        answer*=mp.sqrt(v);pivots.append([mp.nstr(mp.re(v),50),mp.nstr(mp.im(v),50)])
        if M.rows==1:break
        M=mp.matrix([[M[i,j]-M[i,0]*M[0,j]/v for j in range(1,M.cols)] for i in range(1,M.rows)])
    assert abs(answer**2-mp.det(numeric(Q)))<mp.mpf('1e-50')*max(1,abs(answer**2))
    return answer,pivots
def pack(z):return {'real':mp.nstr(mp.re(z),50),'imag':mp.nstr(mp.im(z),50)}

A,B,C,D=R0[:3,:3],R0[:3,3:],R0[3:,:3],R0[3:,3:]
X,Y,Z=B.inv()*A,-B.inv(),D*B.inv()
assert X==X.T and Z==Z.T
Q0=s.eye(3)-s.I*X
Omega0=(Y.T*Q0.inv()*Y-s.I*Z).applyfunc(s.simplify)
root0,pivots0=root(Q0)
Nrel0=mp.sqrt(abs(mp.mpf(str(Y.det()))))*mp.exp(-mp.j*mp.pi/4)/root0

x=s.symbols('x0:3');y=s.symbols('y0:3')
Phi=s.sympify(kernels['variant_delta_phase']);ell=s.sympify(kernels['variant_delta_argument'])
x0solve=s.solve(ell,x[0])[0]
quad=s.expand((sum(v*v for v in x)-2*s.I*Phi).subs(x[0],x0solve))
Qnew=s.hessian(quad,[x[1],x[2],*y])/2
Q1=Qnew[:2,:2]
Omega1=(Qnew[2:,2:]-Qnew[2:,:2]*Q1.inv()*Qnew[:2,2:]).applyfunc(s.simplify)
root1,pivots1=root(Q1)
Nrel1=23*mp.sqrt(2)/(2*root1)
beta=4/mp.sqrt(6)
variances=[]
for R,Omega,Nrel in [(R0,Omega0,Nrel0),(R1,Omega1,Nrel1)]:
    standard=-s.I*(R[3:,:3]+s.I*R[3:,3:])*(R[:3,:3]+s.I*R[:3,3:]).inv()
    assert (Omega-standard).applyfunc(s.simplify)==s.zeros(3)
    Re=mp.matrix([[mp.re(v) for v in row] for row in numeric(Omega.applyfunc(s.re)).tolist()])
    assert all(mp.det(Re[:k,:k])>0 for k in range(1,4))
    norm=abs(Nrel)**2/mp.sqrt(mp.det(Re))
    assert abs(norm-1)<mp.mpf('1e-50')
    variances.append((Re**-1)[0,0]/(2*beta))
T=Omega0.conjugate()+Omega1
rootT,pivotsT=root(T)
z=2**mp.mpf('1.5')*mp.conj(Nrel0)*Nrel1/rootT
u=1+numeric(T.inv())[0,0]/beta
assert mp.re(u)>0
G0=R0*R0.T;G1=R1*R1.T
zabs2=8/mp.sqrt(mp.mpf(str((G0+G1).det())))
assert abs(abs(z)**2-zabs2)<mp.mpf('1e-50')

# Independent scalar Woodbury/completing-square derivation of the record cross term.
t,gg,ss=s.symbols('t g sigma',nonzero=True)
uf=ss**2+gg**2*t
assert s.simplify(-1/(2*ss**2)+gg**2*t/(2*ss**4*(1+gg**2*t/ss**2))+1/(2*uf))==0
assert s.simplify(ss**2*(1+gg**2*t/ss**2)-uf)==0

# Numerical diagnostics retain the existing Float64 W limitation explicitly.
clock=json.loads((PACKAGE/'checks/ward_clock/results.json').read_text())
c0=clock['quadrature']['chain'][-1]['sources']
c1=clock['quadrature']['two_cover_deleted'][-1]['sources']
def wz(row):return mp.mpc(str(row['W']['real']),str(row['W']['imag']))
records=[]
for key in c0:
    a0,a1=wz(c0[key])/2,wz(c1[key])/2
    cross=mp.conj(a0)*a1*z
    probability=abs(a0)**2+abs(a1)**2+2*mp.re(cross)
    variance=(abs(a0)**2*(1+variances[0])+abs(a1)**2*(1+variances[1])+2*mp.re(cross*u))/probability
    binprob=(abs(a0)**2*mp.erf(1/mp.sqrt(2*(1+variances[0])))+
             abs(a1)**2*mp.erf(1/mp.sqrt(2*(1+variances[1])))+
             2*mp.re(cross*mp.erf(1/mp.sqrt(2*u))))/probability
    assert 0<probability<1 and variance>0 and 0<binprob<1
    records.append({'rhoP_rhoF':key,'accept_probability':mp.nstr(probability,35),
                    'conditional_pointer_variance':mp.nstr(variance,35),
                    'conditional_P_abs_y_le_1':mp.nstr(binprob,35)})

result={'id':'INDEPENDENT-COHERENT-GAUSSIAN-AUDIT-0.1','all_checks_pass':True,
        'phase_convention':'C0 reduced kernel exp(-i*pi/4); C1 delta kernel positive real',
        'root_method':'successive complex Schur pivots with positive real part',
        'root_pivots_C0':pivots0,'root_pivots_C1':pivots1,'root_pivots_overlap':pivotsT,
        'overlap_z':pack(z),'cross_pointer_u_g_sigma_1':pack(u),
        'cross_record_density':'z*exp(-y^2/(2*u))/sqrt(2*pi*u), continuation on Re(u)>0',
        'cross_record_integral':'z','cross_record_second_moment':'z*u',
        'cross_record_symmetric_bin':'z*erf(a/sqrt(2*u))',
        'source_diagnostics':records,
        'numerical_scope':'Scalar Gaussian evaluation at 70 digits; W inputs retain existing Float64 quadrature uncertainty. Not interval-certified physical predictions.'}
(OUT/'coherent_gaussian_results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS independent continued Gaussian roots, coherent overlap and normalized pointer formulas')
print('z =',mp.nstr(z,45),'u =',mp.nstr(u,45))
