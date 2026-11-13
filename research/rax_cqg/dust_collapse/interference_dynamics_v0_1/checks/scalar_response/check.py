#!/usr/bin/env python3
"""Exact N11 scalar factorization and independently phased Gaussian pairing."""
from pathlib import Path
import hashlib
import json
import sympy as sp
import mpmath as mp

ROOT = Path(__file__).resolve().parent
N = 11
B = [0, 1, 2, 3, 7, 8, 9, 10]
I = [4, 5, 6]
COEFFICIENTS = (1, -9, 16, -8)
PRECISION = 80
TOLERANCE = mp.mpf('1e-60')


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def build_laplacian(removed):
    order = {(i, j) for i in range(N) for j in range(i + 1, N)} - removed
    require(all((i, k) in order for i, j in order for jj, k in order if j == jj),
            'Order is not transitive')
    L = sp.zeros(N)
    for i, j in order:
        n = sum((i, k) in order and (k, j) in order for k in range(N))
        weight = COEFFICIENTS[n] if n < 4 else 0
        L[i, i] += weight
        L[j, j] += weight
        L[i, j] -= weight
        L[j, i] -= weight
    return L


def to_mp(M):
    return mp.matrix([[mp.mpf(str(M[i, j])) for j in range(M.cols)]
                      for i in range(M.rows)])


def complex_record(value):
    return {'real': mp.nstr(mp.re(value), 60), 'imag': mp.nstr(mp.im(value), 60)}


def matrix_record(M):
    return [[complex_record(M[i, j]) for j in range(M.cols)] for i in range(M.rows)]


def max_error(A, Bmat):
    return max(abs(A[i, j] - Bmat[i, j]) for i in range(A.rows) for j in range(A.cols))


def phase_from_real_symmetric(S, t):
    values = mp.eigsy(S, eigvals_only=True)
    # Each factor has real part one; its logarithm has no branch ambiguity.
    return mp.exp(-mp.fsum(mp.log(1 + 1j * t * v) for v in values) / 2)


def evaluate(label, removed):
    L = build_laplacian(removed)
    require(L[:, I].rank() == len(I), 'Boundary-decoupled scalar zero mode')
    z = sp.Symbol('z')
    E = sp.diag(*[int(j in B) for j in range(N)])
    exact_matrix = E + z * L
    determinant = sp.factor(exact_matrix.det(method='domain-ge'))
    # (A^-1)[0,10] = cofactor[10,0]/det(A); sign is even.
    numerator = sp.factor(exact_matrix.minor_submatrix(10, 0).det(method='domain-ge'))
    h_rational_z = sp.cancel(numerator / determinant)
    z_value = sp.I * sp.sqrt(6) / 3
    h_exact = sp.simplify(sp.expand_complex(h_rational_z.subs(z, z_value)))
    d_exact = sp.simplify(sp.expand(determinant.subs(z, z_value)))
    require(d_exact != 0, 'Joint Gaussian matrix singular')

    t = mp.sqrt(mp.mpf(2) / 3)  # beta/2
    Lmp = to_mp(L)
    Amp = mp.matrix([[mp.mpf(int(i == j and i in B)) + 1j * t * Lmp[i, j]
                     for j in range(N)] for i in range(N)])
    inverse = Amp ** -1
    M = mp.matrix([[inverse[i, j] for j in B] for i in B])
    common_prefactor = mp.pi ** -2 * (2 * mp.pi) ** (mp.mpf(N) / 2)

    if label == 'chain':
        G = L.extract(I, I)
        Schur = L.extract(B, B) - L.extract(B, I) * G.inv() * L.extract(I, B)
        require(G.det() != 0, 'Reference inner scalar block singular')
        eigenvalues = mp.eigsy(to_mp(G), eigvals_only=True)
        signature_H = -sum(1 if v > 0 else -1 for v in eigenvalues)
        require(signature_H == 1, 'Unexpected reference Fresnel signature')
        g = (common_prefactor / mp.sqrt(abs(mp.det(t * to_mp(G)))) *
             mp.exp(1j * mp.pi * signature_H / 4) * phase_from_real_symmetric(to_mp(Schur), t))
        independent_M = (mp.eye(len(B)) + 1j * t * to_mp(Schur)) ** -1
        method = 'Three-variable Fresnel integral with signature +1, followed by eight-variable boundary Schur Gaussian.'
    else:
        J = [4, 6]
        G = L.extract(J, J)
        require(G.det() == -1, 'Unexpected nonzero inner scalar pair')
        require(L[5, 5] == 0 and all(L[5, j] == 0 for j in J), 'Wrong null direction')
        Schur = L.extract(B, B) - L.extract(B, J) * G.inv() * L.extract(J, B)
        w = mp.matrix([int(L[5, j]) for j in B])
        norm_w = mp.sqrt(mp.fdot(w, w))
        # Householder gives a deterministic orthonormal basis of w-perp.
        v = mp.matrix(w)
        v[0] += norm_w
        reflection = mp.eye(len(B)) - 2 * v * v.T / mp.fdot(v, v)
        Q = mp.matrix([[reflection[i, j] for j in range(1, len(B))]
                       for i in range(len(B))])
        require(max_error(Q.T * Q, mp.eye(7)) < TOLERANCE, 'Nonorthogonal hyperplane basis')
        require(max(abs(vv) for vv in w.T * Q) < TOLERANCE, 'Wrong boundary hyperplane')
        restricted = Q.T * to_mp(Schur) * Q
        # q4,q6: factor 2pi/t and zero signature. q5: (2pi/t) delta(w.qB).
        g = common_prefactor / (t * t * norm_w) * phase_from_real_symmetric(restricted, t)
        independent_M = Q * (mp.eye(7) + 1j * t * restricted) ** -1 * Q.T
        method = 'Two-variable Fresnel pair, q5 Fourier delta, then seven-variable boundary hyperplane Gaussian.'
        require(max(abs(vv) for vv in M * w) < TOLERANCE,
                'Boundary covariance does not annihilate the delta constraint')

    matrix_error = max_error(M, independent_M)
    require(matrix_error < TOLERANCE, 'Independent boundary insertion matrix disagrees')
    # The determinant fixes the square but does not choose the Fresnel sign.
    square_error = abs(g * g * mp.det(Amp) / (common_prefactor * common_prefactor) - 1)
    require(square_error < TOLERANCE, 'Scalar amplitude/determinant mismatch')
    hr = mp.mpf(str(sp.N(sp.re(h_exact), PRECISION)))
    hi = mp.mpf(str(sp.N(sp.im(h_exact), PRECISION)))
    require(abs(M[0, 7] - mp.mpc(hr, hi)) < TOLERANCE,
            'Exact q0*q10 cofactor disagrees with Gaussian insertion')
    require(max_error(M, M.T) < TOLERANCE, 'Insertion matrix not complex symmetric')
    return {
        'label': label, 'removed_relations': [list(e) for e in sorted(removed)],
        'boundary_order': B, 'interior_order': I,
        'L': [[int(L[i, j]) for j in range(N)] for i in range(N)],
        'determinant_polynomial': str(determinant),
        'determinant_exact_at_z_i_beta_over_2': str(d_exact),
        'q0q10_cofactor_numerator': str(numerator),
        'q0q10_exact': str(h_exact),
        'g_at_zero': complex_record(g),
        'M_boundary': matrix_record(M),
        'q0q10': complex_record(M[0, 7]),
        'phase_method': method,
        'independent_M_max_abs_error': mp.nstr(matrix_error, 12),
        'g_squared_determinant_relative_error': mp.nstr(square_error, 12),
        'rho_dependence': 'None: scalar H and the identical normalized Gaussian boundary state are fixed; scalar action has no direct dust or clock coupling.'
    }, g, M[0, 7]


def main():
    mp.mp.dps = PRECISION
    c0, g0, h0 = evaluate('chain', set())
    c1, g1, h1 = evaluate('double_cover_deletion', {(4, 5), (5, 6)})
    require(abs(h1 - h0) > mp.mpf('0.08'), 'Selected scalar insertion is insensitive to order')
    ratio = g1 / g0
    rho = sp.Symbol('rho', real=True)
    W0, W1 = sp.Function('W0')(rho), sp.Function('W1')(rho)
    a0, a1, hh0, hh1 = sp.symbols('a0 a1 h0 h1')
    total = a0 * W0 + a1 * W1
    insertion = (hh0 * a0 * W0 + hh1 * a1 * W1) / total
    derivative = ((hh1 - hh0) * a0 * a1 * (W0 * sp.diff(W1, rho) - W1 * sp.diff(W0, rho)) /
                  total ** 2)
    require(sp.simplify(sp.diff(insertion, rho) - derivative) == 0,
            'Source response identity failed')
    output = {
        'id': 'CST-DUST-N11-SCALAR-SOURCE-INSERTION-0.1',
        'model': 'Same N11 two-order family; common original massless scalar action.',
        'fixed_boundary_state': 'pi^(-2)*exp(-sum_B q_b^2/2), an L2-normalized Schwartz test function on eight scalar boundary coordinates with Lebesgue measure. It is not an L1 probability density or a derived physical norm.',
        'source_definition': 'J has components only on B and enters as exp(J_B^T q_B).',
        'common_Abel_factor': 'exp(-epsilon*sum_I q_i^2/2), epsilon down to zero after common boundary pairing.',
        'precision_decimal_digits': PRECISION,
        'numeric_consistency_tolerance': '1e-60 (high-precision agreement, not an interval certificate)',
        'orders': [c0, c1],
        'g1_over_g0': complex_record(ratio),
        'g_ratio_modulus': mp.nstr(abs(ratio), 60),
        'g_ratio_phase_radians': mp.nstr(mp.arg(ratio), 60),
        'q0q10_insertion_difference_h1_minus_h0': complex_record(h1 - h0),
        'full_amplitude': 'A(J,rho)=omega0*W0(rho)*g0*exp(J^T*M0*J/2)+omega1*W1(rho)*g1*exp(J^T*M1*J/2). W includes exp(i*F4) and full dust/clock integration. Do not multiply by exp(i*S_on).',
        'conditional_ratio': 'H=(h0+R*h1)/(1+R); R=omega1*W1*g1/(omega0*W0*g0); h_c=(M_c)_(0,10).',
        'source_derivative': "H'=(h1-h0)*omega0*omega1*g0*g1*(W0*W1'-W1*W0')/(omega0*g0*W0+omega1*g1*W1)^2, for source-independent omega and nonzero total amplitude.",
        'source_dependence_location': 'Only W and any separately changed history weights. g and M are independent of rho for this frozen model.',
        'null_conditions': ['If one history coefficient vanishes, this scalar insertion has no source response.', 'If W1/W0 is source-independent where defined, response vanishes.', 'If total amplitude vanishes, normalized insertion is undefined.'],
        'qualification': 'Complex Lorentzian amplitude insertion, not a positive covariance, a probability, a detector correlation or physical geometry dynamics.',
        'new_clock_integrals': 0,
        'physical_history_measure_derived': False,
        'all_checks_passed': True
    }
    (ROOT / 'results.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
    print('PASS: exact scalar cofactors and determinants; independent Fresnel/delta branch; all boundary insertion entries; source derivative identity.')
    print('g1/g0 =', mp.nstr(ratio, 20))
    print('h0 =', mp.nstr(h0, 20), '; h1 =', mp.nstr(h1, 20))
    print('Scope: complex amplitude insertion only; full W inputs are computed separately.')


if __name__ == '__main__':
    main()
