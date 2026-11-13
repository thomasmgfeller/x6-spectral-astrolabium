#!/usr/bin/env python3
"""N10 action sewing and variation, using exact rational algebra.

The clock coordinates u satisfy T=Delta*(u-9/2), beta*Delta^2=2/19.
No density/clock/scalar integral or physical propagator is computed.
"""
from pathlib import Path
import hashlib
import json
import sympy as s

BASE = Path(__file__).resolve().parent
N = 10
I = (4, 5)
B = tuple(x for x in range(N) if x not in I)
COEFF = (1, -9, 16, -8)
u = s.symbols('u0:10', real=True)
r = s.symbols('r0:10', real=True)
q = s.symbols('q0:10', real=True)
rho = s.symbols('rho', positive=True)


def pairs(rel, vertices):
    return [(a, b, COEFF[n] if n < 4 else 0)
            for a, b in sorted(rel)
            if a in vertices and b in vertices
            for n in [sum((a, z) in rel and (z, b) in rel for z in vertices)]]


def action(rel, vertices):
    rows = pairs(rel, vertices)
    gravity = len(vertices) - sum(c for a, b, c in rows)
    dust = -sum(r[i] for i in vertices) / 2 - sum(
        s.Rational(c, 38) * r[b] * (u[b] - u[a]) ** 2 for a, b, c in rows)
    scalar_over_beta = -sum(s.Rational(c, 4) * (q[b] - q[a]) ** 2 for a, b, c in rows)
    return (s.Integer(gravity), s.expand(dust), s.expand(scalar_over_beta))


def increment(rel, n):
    rows = [(a, b, c) for a, b, c in pairs(rel, set(range(n + 1))) if b == n]
    return (s.Integer(1 - sum(c for a, b, c in rows)),
            s.expand(-r[n] / 2 - sum(s.Rational(c, 38) * r[n] * (u[n] - u[a]) ** 2 for a, b, c in rows)),
            s.expand(-sum(s.Rational(c, 4) * (q[n] - q[a]) ** 2 for a, b, c in rows)))


def encode(x):
    if isinstance(x, s.MatrixBase):
        return [[str(v) for v in row] for row in x.tolist()]
    return str(x)


def run():
    chain = {(a, b) for a in range(N) for b in range(a + 1, N)}
    fork = chain - {(4, 5)}
    results = {}
    checks = 0
    for name, rel in [('chain', chain), ('fork', fork)]:
        full = action(rel, set(range(N)))
        inc = [increment(rel, n) for n in range(N)]
        # Independent prefix differences and every monomial of all sectors.
        for n in range(N):
            before = action(rel, set(range(n))) if n else (0, 0, 0)
            after = action(rel, set(range(n + 1)))
            for k in range(3):
                assert s.expand(after[k] - before[k] - inc[n][k]) == 0
                checks += 1
        for k in range(3):
            assert s.expand(sum(x[k] for x in inc) - full[k]) == 0
            checks += 1
        # Three causal shells, with every endpoint term assigned exactly once.
        shells = [tuple(s.expand(sum(inc[n][k] for n in nodes)) for k in range(3))
                  for nodes in [range(4), range(4, 6), range(6, 10)]]
        point = {r[i]: rho for i in range(N)} | {u[i]: s.Integer(i) for i in range(N)} | {q[i]: 0 for i in range(N)}
        if name == 'fork':
            point[u[5]] = 4
        constraints = [s.simplify(-2 * s.diff(full[1], r[i]).subs(point)) for i in I]
        clock_residual = [s.simplify(s.diff(full[1], u[i]).subs(point)) for i in I]
        scalar_residual = [s.simplify(s.diff(full[2], q[i]).subs(point)) for i in I]
        assert constraints == clock_residual == scalar_residual == [0, 0]
        local_inner = [s.simplify(s.diff(shells[1][1], u[i]).subs(point)) for i in I]
        future = [s.simplify(s.diff(shells[2][1], u[i]).subs(point)) for i in I]
        assert all(s.simplify(a + b) == 0 for a, b in zip(local_inner, future))
        assert any(x != 0 for x in local_inner)
        H = s.hessian(full[2], q)
        HII = H.extract(I, I)
        HIB = H.extract(I, B)
        on_shell = s.simplify(full[0] + full[1].subs(point))
        expected = (9 - s.Rational(151, 38) * rho if name == 'chain'
                    else 8 - s.Rational(148, 38) * rho)
        assert on_shell == expected
        # Envelope theorem: solve/free variables are stationary before differentiating boundary data.
        boundary_clock_momenta = [s.simplify(s.diff(full[1], u[b]).subs(point)) for b in B]
        results[name] = {
            'F4': encode(full[0]), 'on_shell_total_action_q0': encode(on_shell),
            'inner_density_constraints': list(map(encode, constraints)),
            'inner_clock_stationarity': list(map(encode, clock_residual)),
            'inner_scalar_stationarity': list(map(encode, scalar_residual)),
            'inner_shell_clock_gradient': list(map(encode, local_inner)),
            'future_shell_clock_gradient': list(map(encode, future)),
            'boundary_clock_derivative_in_u_units': list(map(encode, boundary_clock_momenta)),
            'HII_over_beta': encode(HII), 'HIB_over_beta': encode(HIB),
            'full_scalar_rank': H.rank(),
            'incoming_nonzero_predecessors_by_vertex': [[a for a, b, c in pairs(rel, set(range(N))) if b == n and c] for n in range(N)],
        }
        if name == 'chain':
            assert HII.det() == -s.Rational(1, 4)
            assert all(len(x) <= 4 for x in results[name]['incoming_nonzero_predecessors_by_vertex'])
        else:
            v = s.zeros(N, 1); v[4] = 1; v[5] = -1
            assert H * v == s.zeros(N, 1)
            assert HII == s.zeros(2)
            assert HIB.rank() == 1
            results[name]['full_null_vector'] = list(map(str, v))
            results[name]['unpaired_scalar_contrast'] = '(q4-q5)/sqrt(2)'
            results[name]['Abel_zero_mode_factor'] = 'sqrt(2*pi/epsilon)'
            results[name]['full_amplitude_status'] = 'DIVERGENT_FOR_GENERIC_BOUNDARY_PACKETS_WITH_UNCHANGED_SCALAR_MEASURE'
    # Nonzero outer source response at fixed collar and q=0; it is stationary action data, not probability.
    results['on_shell_action_difference_chain_minus_fork'] = str(s.simplify((9-s.Rational(151,38)*rho)-(8-s.Rational(148,38)*rho)))
    # Compact density integration: at C=2*pi the exact square defect is negative.
    d = s.Rational(1, 2) - s.I / s.pi
    defect = s.simplify(d*d-d)
    assert defect == -s.Rational(1, 4) - 1/s.pi**2
    out = {
        'all_checks_pass': True, 'exact_prefix_sector_identities_checked': checks,
        'fixed_boundary': list(B), 'free_interior': list(I),
        'clock_normalization': 'T_j=Delta*(u_j-9/2), beta*Delta^2=2/19',
        'beta': '4/sqrt(6)', 'rho_range': '0<rho<1',
        'clock_support_qualification': 'Affine chain/fork collar requires |T|<=4.5*Delta, approximately1.1425; exceeds original [-1,1] box.',
        'results': results,
        'density_factor': {'D(C)': '1/2+i*(exp(-i*C/2)-1)/C; D(0)=1',
                           'C_D(C)': 'C/2+i*(exp(-i*C/2)-1)',
                           'D(2*pi)': str(d), 'D_squared_minus_D_at_2pi': str(defect),
                           'automatic_constraint_projector': False},
        'new_integrations': 0,
        'scope': 'Exact action composition and stationary boundary response only. No physical state pairing, normalized geometry dynamics, or finite fork amplitude derived.'}
    (BASE/'results.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    run()
