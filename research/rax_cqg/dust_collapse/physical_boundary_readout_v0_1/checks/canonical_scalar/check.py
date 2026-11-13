#!/usr/bin/env python3
"""Exact standalone N11 scalar Legendre, reduction and kernel-normalization audit.

All matrices are reconstructed from comparable pairs, never imported from another
check. Hbar=H/beta, pi=p/beta, hbar=1. Matrix symplectic tests use scaled J;
physical Poisson brackets of (q,pi) are J/beta. Fourier integrals are understood
as tempered distributions with the stated Abel/Fresnel prescription.
"""
import json
from pathlib import Path
import sympy as s

P, I, F = list(range(4)), [4, 5, 6], list(range(7, 11))
beta = s.symbols('beta', positive=True)
def J(n):
    return s.zeros(n).row_join(s.eye(n)).col_join((-s.eye(n)).row_join(s.zeros(n)))
J8, J6 = J(4), J(3)
def hbar(which):
    order = {(i, j) for i in range(11) for j in range(i+1, 11)}
    if which:
        order -= {(4, 5), (5, 6)}
    assert all((i, k) in order for i, j in order for j2, k in order if j == j2)
    L = s.zeros(11)
    for i, j in order:
        k = sum((i, m) in order and (m, j) in order for m in range(11))
        w = [1, -9, 16, -8][k] if k < 4 else 0
        L[i, i] += w; L[j, j] += w; L[i, j] -= w; L[j, i] -= w
    return -L/2

H0, H1 = hbar(0), hbar(1)
A0, A1 = [H.extract(I+P, I+F) for H in (H0, H1)]
Jpred = s.zeros(7, 4); Jpred[3:, :] = s.eye(4)
rhs0 = (-H0.extract(I+P, P)).row_join(-Jpred)
rhs1 = (-H1.extract(I+P, P)).row_join(-Jpred)
Y = A0.inv()*rhs0
M0 = Y[3:, :].col_join(H0.extract(F, P).row_join(s.zeros(4)) + H0.extract(F, I+F)*Y)
assert A0.det() == -16384 and A1.rank() == 6
assert M0.T*J8*M0 == J8
assert M0[:4, 4:].det() == s.Rational(9, 65536)
assert H0.extract(I, I).det() == -s.Rational(9, 4)
assert H1.extract(I, I).rank() == 2

am = s.Matrix([[-128, 241, 119, -232, -46, -32, -16, 0]])
ap = s.Matrix([[-232, 119, 241, -128, 0, 16, 32, 46]])
left = s.Matrix([[0, 0, 0, s.Rational(23, 8), 2, 1, 0]])
assert left*A1 == s.zeros(1, 7)
assert 16*left*rhs1 == am
amin, apout = s.zeros(1, 11), s.zeros(1, 11)
for j, k in enumerate(P): amin[k] = am[j]
for j, k in enumerate(F): apout[k] = ap[j]
assert amin-am[:, 4:]*H1[P, :] == s.zeros(1, 11)
assert apout+ap[:, 4:]*H1[F, :] == s.zeros(1, 11)
B = ap*M0
kappa = (am*J8*B.T)[0]
assert kappa == -s.Rational(52625, 32)
assert am.col_join(B).rank() == 2

# Common Darboux sections q0=0 on input and q10=0 on output, A_-/A_+=0.
Em = s.zeros(8, 6); Em[1:4, :3] = s.eye(3); Em[5:8, 3:] = s.eye(3)
Em[4, :] = -(am*Em)/am[4]
Ep = s.zeros(8, 6); Ep[:3, :3] = s.eye(3); Ep[4:7, 3:] = s.eye(3)
Ep[7, :] = -(ap*Ep)/ap[7]
Rp = s.zeros(6, 8); Rp[:3, :3] = s.eye(3); Rp[3:, 4:7] = s.eye(3)
assert am*Em == s.zeros(1, 6) and ap*Ep == s.zeros(1, 6)
assert Em.T*J8*Em == J6 and Ep.T*J8*Ep == J6
Tin = s.eye(8)+J8*am.T*B/kappa
Tout = s.eye(8)-J8*ap.T*s.eye(8)[3, :]/ap[7]
assert B*Tin == s.zeros(1, 8)
R0 = Rp*Tout*M0*Tin*Em
g = s.zeros(1, 7); g[0, 6] = 1
AA = A1.col_join(g); RR = (rhs1*Em).col_join(s.zeros(1, 6))
YY = (AA.T*AA).inv()*AA.T*RR
assert AA*YY == RR
out1 = YY[3:, :].col_join(H1.extract(F, P)*Em[:4, :] + H1.extract(F, I+F)*YY)
R1 = Rp*out1
assert ap*out1 == s.zeros(1, 6)
assert R0.T*J6*R0 == J6 and R1.T*J6*R1 == J6
assert R0 != R1
assert R0[:3, 3:].det() == s.Rational(737, 35633440)
assert R1[:3, 3:].rank() == 2
ldu = {}
for name, R in [('C0', R0), ('C1', R1)]:
    A, BB, C = R[:3, :3], R[:3, 3:], R[3:, :3]
    Q, V = A.inv()*BB, C*A.inv()
    assert Q == Q.T and V == V.T
    lower = s.eye(3).row_join(s.zeros(3)).col_join(V.row_join(s.eye(3)))
    diag = A.row_join(s.zeros(3)).col_join(s.zeros(3).row_join(A.inv().T))
    upper = s.eye(3).row_join(Q).col_join(s.zeros(3).row_join(s.eye(3)))
    assert lower*diag*upper == R
    ldu[name] = {'det_qq': A.det(), 'momentum_shear': Q, 'position_chirp': V}

# Exact Gaussian realization of <A_+=0|U0|A_-=0>.
x = s.Matrix(s.symbols('x0:3')); y = s.Matrix(s.symbols('y0:3'))
tm, tp = s.symbols('t_minus t_plus')
qm = s.Matrix([0, *x])+am[:, 4:].T*tm
qp = s.Matrix([*y, 0])+ap[:, 4:].T*tp
fm = tm*(am[:, :4]*s.Matrix([0, *x]))[0]+(am[:, :4]*am[:, 4:].T)[0]*tm**2/2
fp = tp*(ap[:, :4]*s.Matrix([*y, 0]))[0]+(ap[:, :4]*ap[:, 4:].T)[0]*tp**2/2
qb = qm.col_join(qp)
Hb0 = H0.extract(P+F, P+F)-H0.extract(P+F, I)*H0.extract(I, I).inv()*H0.extract(I, P+F)
assert Hb0[:4, 4:].det() == s.Rational(65536, 9)
phase0 = s.expand((qb.T*Hb0*qb)[0]/2+fp-fm)
K0 = s.hessian(phase0, list(x)+list(y)+[tm, tp])
D = K0[6:, 6:]
assert D == s.Matrix([[-s.Rational(7696, 9), -s.Rational(4096, 9)], [-s.Rational(4096, 9), -s.Rational(7696, 9)]])
assert D.det() == s.Rational(4716800, 9) and D.trace() < 0
Kred = K0[:6, :6]-K0[:6, 6:]*D.inv()*K0[6:, :6]
G = Kred[:3, 3:]
Yred = (-G.inv()*Kred[:3, :3]).row_join(-G.inv())
Pred = Kred[3:, :3].row_join(s.zeros(3))+Kred[3:, 3:]*Yred
assert Yred.col_join(Pred) == R0
assert G.det() == -s.Rational(35633440, 737)
defect = s.factor(46**2*(beta/(2*s.pi))*R0[:3, 3:].det()/(M0[:4, 4:].det()*D.det()))
assert s.simplify(defect-beta/(2*s.pi*abs(kappa))) == 0

# C1 quotient: q5 integral is a delta; regular q4,q6 Gaussian has signature zero.
Reg = [4, 6]
assert H1.extract(Reg, Reg).det() == -s.Rational(1, 4)
Hb1 = H1.extract(P+F, P+F)-H1.extract(P+F, Reg)*H1.extract(Reg, Reg).inv()*H1.extract(Reg, P+F)
qbs = s.Matrix([0, *x, *y, 0])
phi1 = s.expand((qbs.T*Hb1*qbs)[0]/2)
ell = s.expand((H1.extract([5], P+F)*qbs)[0])
assert s.expand((H1.extract([5], P+F)*qb)[0]-ell) == 0
assert s.expand((qb.T*Hb1*qb)[0]/2+fp-fm-phi1) == 0
K1 = s.hessian(phi1, list(x)+list(y))
c = s.Matrix([[s.diff(ell, v) for v in x]])
d = s.Matrix([[s.diff(ell, v) for v in y]])
mix = K1[:3, 3:]
# Stationary delta-generating function Phi+lambda*ell reproduces R1.
delta_A = mix.row_join(c.T).col_join(d.row_join(s.zeros(1)))
delta_rhs = (-K1[:3, :3]).row_join(-s.eye(3)).col_join((-c).row_join(s.zeros(1, 3)))
sol = delta_A.inv()*delta_rhs
pout = K1[3:, :3].row_join(s.zeros(3))+K1[3:, 3:]*sol[:3, :]+d.T*sol[3, :]
assert sol[:3, :].col_join(pout) == R1
# K^dagger K: eliminate y2 with first delta, Fourier-integrate y0,y1.
V0 = mix[:, 0]-d[0]/d[2]*mix[:, 2]
V1 = mix[:, 1]-d[1]/d[2]*mix[:, 2]
T = c.col_join(V0.T).col_join(V1.T)
unit_coefficient_squared = abs(d[2]*T.det())*(beta/(2*s.pi))**2
assert d[2]*abs(T.det()) == 16928
# KK^dagger, eliminating x0, gives the same normalization.
W1 = mix[1, :]-c[1]/c[0]*mix[0, :]
W2 = mix[2, :]-c[2]/c[0]*mix[0, :]
Trev = d.col_join(W1).col_join(W2)
assert abs(c[0]*Trev.det()) == 16928
C1unit = s.sqrt(unit_coefficient_squared)
N1 = s.factor(C1unit/(8*s.pi**2/beta**2))
assert s.simplify(N1-23*s.sqrt(2)*beta**3/(4*s.pi**3)) == 0

results = {
 'status': 'PASS; conditional scalar CCR/rigging contract, not a derivation of full CST physical pairing',
 'conventions': {'H': 'beta*Hbar', 'beta': '4/sqrt(6)', 'pi': 'p/beta', 'CCR': '[q,pi]=i/beta', 'P': P, 'I': I, 'F': F, 'input_reduced': '(q1,q2,q3,pi1,pi2,pi3) at q0=0,A_-=0', 'output_reduced': '(q7,q8,q9,pi7,pi8,pi9) at q10=0,A_+=0'},
 'legendre': {'C0_Hbar': H0, 'C1_Hbar': H1, 'C0_Abar_det': A0.det(), 'C1_Abar_rank': A1.rank(), 'C1_Abar_left_null': left, 'C1_Abar_right_null': A1.nullspace()[0], 'C0_M': M0, 'C0_B_det': M0[:4,4:].det(), 'C0_bare_to_unitary_positive_factor': 128*(beta/(2*s.pi))**s.Rational(7,2)},
 'constraints': {'A_minus': am, 'A_plus': ap, 'pointwise_integrand_identities': True, 'A_plus_pullback_C0': B, 'scaled_bracket': kappa, 'physical_bracket': kappa/beta, 'strong_common_kernel': 'zero; this does not exclude rigging sandwiches'},
 'common_reduction': {'input_embedding': Em, 'output_embedding': Ep, 'R0': R0, 'R1': R1, 'R0_symplectic': True, 'R1_symplectic': True, 'distinct': True, 'R0_B_det': R0[:3,3:].det(), 'R1_B_rank': R1[:3,3:].rank(), 'ldu': ldu},
 'C0_quantum_sandwich': {'phase_Hessian_after_chirp': K0, 'gauge_Hessian': D, 'gauge_Hessian_det': D.det(), 'gauge_Hessian_signature': -2, 'reduced_phase_Hessian': Kred, 'mixed_Hessian_det': G.det(), 'sandwich_SdaggerS': defect, 'positive_FP_to_unitary': s.sqrt(1/defect), 'inherited_Fresnel_phase': '-pi/4', 'Fourier_convention': '<t|a>=sqrt(beta/(2pi))*exp(i beta a t)', 'coordinate_kernel_Jacobian': 46},
 'C1_quantum_quotient': {'ell': ell, 'phase': phi1, 'phase_Hessian': K1, 'gauge_independence_after_chirp': True, 'bare_section_kernel': '(8*pi**2/beta**2)*delta(ell)*exp(i*beta*Phi)', 'composition_matrix': T, 'composition_det': T.det(), 'unitary_delta_coefficient': C1unit, 'positive_normalization_of_bare_section': N1, 'inherited_Fresnel_phase': '0', 'direct_double_group_average': 'diverges; factor/quotient gauge volume, do not multiply distributions blindly'},
 'assumptions': ['Canonical CCR and Liouville/Lebesgue scalar pairing are additional quantization postulates.', 'Impose C1-derived boundary constraints on both histories as a new common rigging contract.', 'Use stated Fourier normalization, Abel/Fresnel phases, and positive kernel normalizations.', 'Fixed outer clock/density Dirichlet data are not normalized physical boundary states.', 'Original compact density integral does not derive this group averaging.'],
}
def encode(obj):
    if isinstance(obj, s.MatrixBase): return [[str(v) for v in row] for row in obj.tolist()]
    if isinstance(obj, s.Basic): return str(obj)
    raise TypeError(type(obj))
destination = Path(__file__).with_name('results.json')
destination.write_text(json.dumps(results, default=encode, ensure_ascii=False, indent=2)+'\n')
print('PASS: exact Legendre ranks, constraints, two symplectic reductions, Gaussian sandwich normalization and delta-kernel two-sided unitarity.')
print(destination)
