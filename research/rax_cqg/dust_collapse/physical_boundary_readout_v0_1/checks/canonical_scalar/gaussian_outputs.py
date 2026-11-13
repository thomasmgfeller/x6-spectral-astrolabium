#!/usr/bin/env python3
"""Normalized outgoing Gaussians with the explicitly inherited kernel phases.

Reads only this check's exact results. Complex square roots are fixed by analytic
continuation from a positive real Gaussian, not by sqrt(det(Q)) on an arbitrary
principal determinant branch. Numerical values use 70 decimal digits.
"""
import json
from pathlib import Path
import sympy as s
import mpmath as mp

mp.mp.dps = 70
here = Path(__file__).parent
data = json.loads((here/'results.json').read_text())
def matrix(raw): return s.Matrix([[s.sympify(x) for x in row] for row in raw])
def numerical(M):
    return mp.matrix([[mp.mpc(str(s.re(z).evalf(75)), str(s.im(z).evalf(75))) for z in row] for row in M.tolist()])
def positive_gaussian_root(Q):
    """sqrt(det(R-iS)), continued along R-i*t*S, 0<=t<=1, R>0."""
    R = Q.applyfunc(s.re); S = -Q.applyfunc(s.im)
    rr, ss = numerical(R), numerical(S)
    rr = mp.matrix([[mp.re(z) for z in row] for row in rr.tolist()])
    ss = mp.matrix([[mp.re(z) for z in row] for row in ss.tolist()])
    L = mp.cholesky(rr)
    Li = L**-1
    ev, _ = mp.eigsy(Li*ss*Li.T)
    logroot = mp.log(mp.det(rr))/2 + sum(mp.log(1-1j*lam)/2 for lam in ev)
    root = mp.exp(logroot)
    assert abs(root**2-mp.det(numerical(Q))) < mp.mpf('1e-50')*max(1, abs(root**2))
    return root, [mp.nstr(v, 55) for v in ev]
def cmplx(z): return {'re': mp.nstr(mp.re(z), 55), 'im': mp.nstr(mp.im(z), 55)}
def nmatrix(M): return [[cmplx(z) for z in row] for row in numerical(M).tolist()]

K0 = matrix(data['C0_quantum_sandwich']['reduced_phase_Hessian'])
K1 = matrix(data['C1_quantum_quotient']['phase_Hessian'])
R0 = matrix(data['common_reduction']['R0']); R1 = matrix(data['common_reduction']['R1'])
X,Y,Z = K0[:3,:3],K0[:3,3:],K0[3:,3:]
Q0 = s.eye(3)-s.I*X
Omega0 = (Y.T*Q0.inv()*Y-s.I*Z).applyfunc(s.simplify)
root0, ev0 = positive_gaussian_root(Q0)
nrel0 = mp.sqrt(abs(mp.mpf(str(Y.det()))))*mp.exp(-1j*mp.pi/4)/root0

# delta ell=c*x+d*y; eliminate x0, giving dx*delta(ell)=du/8.
c=s.Matrix([[8,-s.Rational(9,2),s.Rational(1,2)]])
d=s.Matrix([[s.Rational(1,2),-s.Rational(9,2),8]])
T=s.Matrix([[-c[1]/c[0],-c[2]/c[0]],[1,0],[0,1]])
v=s.zeros(3);v[0,:]=-d/c[0]
E=T.row_join(v).col_join(s.zeros(3,2).row_join(s.eye(3)))
Qall=s.diag(1,1,1,0,0,0)-s.I*K1
Qnew=E.T*Qall*E
Q1=Qnew[:2,:2]
Omega1=(Qnew[2:,2:]-Qnew[2:,:2]*Q1.inv()*Qnew[:2,2:]).applyfunc(s.simplify)
root1, ev1 = positive_gaussian_root(Q1)
nrel1=(23*mp.sqrt(2)/2)/root1

for R,Om in [(R0,Omega0),(R1,Omega1)]:
    standard=-s.I*(R[3:,:3]+s.I*R[3:,3:])*(R[:3,:3]+s.I*R[:3,3:]).inv()
    assert (Om-standard).applyfunc(s.simplify)==s.zeros(3)
    assert Om==Om.T

beta=4/mp.sqrt(6)
n_input=(beta/mp.pi)**mp.mpf('0.75')
outs=[]
for name,Om,nrel,ev in [('C0',Omega0,nrel0,ev0),('C1',Omega1,nrel1,ev1)]:
    norm=abs(nrel)**2/mp.sqrt(mp.det(numerical(Om.applyfunc(s.re))))
    assert abs(norm-1)<mp.mpf('1e-50')
    outs.append({'history':name,'Omega_scaled_exact':[[str(z) for z in row] for row in Om.tolist()],
                 'Omega_scaled':nmatrix(Om),'P_equals_beta_Omega':[[cmplx(beta*z) for z in row] for row in numerical(Om).tolist()],
                 'N_relative_to_input_prefactor':cmplx(nrel),'N':cmplx(n_input*nrel),
                 'norm_check':cmplx(norm),'Gaussian_root_continuation_eigenvalues':ev})
Qsum=Omega0.conjugate()+Omega1
rootsum,evsum=positive_gaussian_root(Qsum)
overlap=mp.power(2,mp.mpf('1.5'))*mp.conj(nrel0)*nrel1/rootsum
u=1+(Qsum.inv()[0,0])/s.sympify('4/sqrt(6)')
result={'status':'PASS; conditional on explicit common scalar CCR/rigging/Fresnel contract',
 'wavefunction_convention':'psi_c(Q)=N_c*exp(-Q^T P_c Q/2); P_c=beta*Omega_c',
 'input':'(beta/pi)^(3/4) exp(-beta*x^T*x/2)',
 'phase_convention':{'C0_reduced_kernel':'exp(-i*pi/4) times positive amplitude','C1_reduced_kernel':'positive delta-kernel amplitude; phase zero'},
 'branches':outs,'overlap_z_equals_integral_conj_psi0_psi1':cmplx(overlap),'overlap_magnitude':mp.nstr(abs(overlap),55),
 'detector_cross_u_g1_sigma1':cmplx(numerical(s.Matrix([[u]]))[0]),
 'root_rule':'R-iS -> sqrt(det R)*exp(1/2 sum_j Log(1-i lambda_j)); lambda_j real eigenvalues of R^(-1/2) S R^(-1/2); this fixes continuation from t=0.'}
(here/'gaussian_outputs.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('PASS: both outgoing Gaussians match exact symplectic maps and normalize; Abel/Fresnel phases tracked.')
print('overlap z =',mp.nstr(overlap,45),'|z| =',mp.nstr(abs(overlap),45))
