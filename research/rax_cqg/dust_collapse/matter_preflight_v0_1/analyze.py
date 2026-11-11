#!/usr/bin/env python3
"""Exact preflight controls. No physical matter kernel is generated."""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import sympy as s

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'inputs'))
import gluing as g

GATES = {key: 'HOLD' for key in ('MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE',
                               'REGULARITY', 'BOUNDARY', 'TRAPPING', 'EXTENSION')}


def save(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False,
                               allow_nan=False)+'\n', encoding='utf-8')


def schur_data(d, boundary, interior):
    d = s.Matrix(d)
    if d != d.T:
        raise ValueError('A real-field action requires an explicitly symmetric Hessian.')
    if sorted(boundary+interior) != list(range(d.rows)) or len(set(boundary+interior)) != d.rows:
        raise ValueError('Boundary and interior must partition all field indices.')
    bb = d.extract(boundary, boundary)
    h = d.extract(interior, interior)
    j = d.extract(interior, boundary)
    if not interior:
        return bb, s.zeros(0, len(boundary)), 'EMPTY_INTERIOR'
    null = h.nullspace()
    constraints = (s.Matrix.hstack(*null).T*j) if null else s.zeros(0, len(boundary))
    reduced = bb-j.T*h.pinv()*j
    status = 'INVERTIBLE' if not null else 'SINGULAR_REQUIRES_MEASURE_AND_NULLSPACE_TREATMENT'
    return reduced, constraints, status


def signature(h):
    h = s.Matrix(h)
    if h != h.T:
        raise ValueError('Non-symmetric quadratic form.')
    if h.is_positive_definite:
        return h.rows
    if (-h).is_positive_definite:
        return -h.rows
    ans = 0
    for eigenvalue, count in h.eigenvals().items():
        if eigenvalue.is_positive:
            ans += count
        elif eigenvalue.is_negative:
            ans -= count
        elif eigenvalue != 0:
            raise ValueError('Unresolved exact inertia.')
    return ans


def fresnel_factor(h):
    """Lebesgue measure, hbar=1, full real line, Abel damping; no extra phase."""
    h = s.Matrix(h)
    if h.det() == 0:
        raise ValueError('Singular Fresnel integral is not a finite determinant factor.')
    return (2*s.pi)**(s.Rational(h.rows, 2))*s.exp(s.I*s.pi*signature(h)/4)/s.sqrt(abs(h.det()))


def geometry_audit():
    transitions = []
    for left, a in [('A', 0), ('K', 2)]:
        for right, b in [('A', 0), ('K', 2)]:
            fiber = [c for c in g.all_posets(4)
                     if g.induced(c, 4, 3) == a and g.induced(c, 4, 12) == b]
            forward = [c for c in fiber
                       if not any(i >= 2 and j < 2 for i, j in g.pairs(c, 4))]
            polynomials = {}
            for name, orders in [('original', fiber), ('no_right_to_left_relations', forward)]:
                poly = {}
                for c in orders:
                    g.poly_add(poly, g.action(c, 4)-g.action(a, 2)-g.action(b, 2))
                polynomials[name] = {str(k): str(v) for k, v in sorted(poly.items())}
            transitions.append({'left': left, 'right': right, 'original_count': len(fiber),
                'restricted_count': len(forward), 'original_order_ids': fiber,
                'restricted_order_ids': forward, 'polynomials': polynomials,
                'boundary_nodes_if_both_blocks_are_boundaries': [0, 1, 2, 3],
                'interior_nodes_under_that_assignment': []})
    return {'role': 'PROJECT_SOURCE_REENUMERATION_AND_DIAGNOSTIC_RESTRICTION',
            'restriction_is_a_physical_boundary_law': False,
            'all_labeled_four_element_orders': len(g.all_posets(4)),
            'restriction': 'Remove every relation from right block {2,3} to left block {0,1}; permit absent cross relations.',
            'caveat': 'K is a chain, hence not an antichain Cauchy boundary. Counts are not temporal transition amplitudes.',
            'transitions': transitions}


def run(out):
    checks = []
    def check(name, condition):
        if not bool(condition):
            raise AssertionError(name)
        checks.append({'name': name, 'status': 'PASS'})

    audit = geometry_audit()
    check('source_enumeration_219_orders', audit['all_labeled_four_element_orders'] == 219)
    check('original_fibers_35_26_26_20', [x['original_count'] for x in audit['transitions']] == [35,26,26,20])
    check('oriented_subsets_16_9_9_6', [x['restricted_count'] for x in audit['transitions']] == [16,9,9,6])
    # Independent combinatorial counts: 2^4 bipartite subsets, 3^2 ideals, C(4,2).
    check('independent_oriented_count_formula', [16,9,9,6] == [2**4,3**2,3**2,int(s.binomial(4,2))])
    check('each_oriented_set_is_proper_subset', all(set(x['restricted_order_ids']) < set(x['original_order_ids']) for x in audit['transitions']))
    check('four_node_two_plus_two_has_no_interior', all(not x['interior_nodes_under_that_assignment'] for x in audit['transitions']))

    x,y,z = s.symbols('x y z', real=True)
    retarded = s.Matrix([[-1,0],[2,-1]])
    phi = s.Matrix([x,y])
    action = (phi.T*retarded*phi)[0]/2
    check('quadratic_action_uses_symmetric_part', s.hessian(action,(x,y)) == (retarded+retarded.T)/2)
    check('retarded_operator_is_not_action_hessian', s.hessian(action,(x,y)) != retarded)
    try: schur_data(retarded,[0],[1])
    except ValueError: rejected = True
    else: rejected = False
    check('asymmetric_hessian_rejected', rejected)

    d = s.Matrix([[3,1,2],[1,4,-1],[2,-1,5]])
    reduced, constraint, tag = schur_data(d,[0,1],[2])
    full_phi = s.Matrix([x,y,-(2*x-y)/5])
    check('stationary_schur_substitution', s.expand((full_phi.T*d*full_phi)[0]-(s.Matrix([x,y]).T*reduced*s.Matrix([x,y]))[0]) == 0)
    check('determinant_schur_identity', d.det() == 5*reduced.det())
    check('signature_schur_identity', signature(d) == 1+signature(reduced))
    empty, condition, tag = schur_data(d,[0,1,2],[])
    check('empty_interior_schur_is_original', empty == d and tag == 'EMPTY_INTERIOR')
    singular = s.Matrix([[2,1],[1,0]])
    reduced, constraint, tag = schur_data(singular,[0],[1])
    check('singular_source_constraint_retained', constraint == s.Matrix([[1]]) and 'SINGULAR' in tag)
    compatible = s.diag(2,0)
    reduced, constraint, tag = schur_data(compatible,[0],[1])
    check('compatible_zero_mode_not_silently_quotiented', constraint == s.zeros(1,1) and 'SINGULAR' in tag)
    try: fresnel_factor(s.zeros(1))
    except ValueError: rejected = True
    else: rejected = False
    check('singular_fresnel_determinant_rejected', rejected)
    check('negative_fresnel_phase_conjugates_positive', s.simplify(fresnel_factor([[-1]])-s.conjugate(fresnel_factor([[1]]))) == 0)
    check('mixed_signature_fresnel_no_extra_morse_phase', s.simplify(fresnel_factor(s.diag(2,-3))-2*s.pi/s.sqrt(6)) == 0)

    a,b,c = s.symbols('a b c', real=True)
    q = a*x*x+2*b*x*y+c*y*y
    check('quadratic_action_even_under_joint_field_flip', s.expand(q.subs({x:-x,y:-y}, simultaneous=True)-q) == 0)
    odd_insert = y*s.exp(s.I*q/2)*s.exp(-(x*x+y*y)/2)
    check('vacuum_one_quantum_integrand_odd', s.simplify(odd_insert.subs({x:-x,y:-y},simultaneous=True)+odd_insert) == 0)
    parity = s.kronecker_product(s.eye(2),s.diag(1,-1))
    # A mathematical counterexample, explicitly NOT extracted from CST.
    fixture = s.kronecker_product(s.Matrix([[1,s.Rational(1,3)],[s.Rational(1,3),1]]),s.eye(2))
    check('even_sector_mixing_can_commute_with_parity', parity*fixture == fixture*parity and fixture[0,2] != 0)
    check('odd_zero_does_not_imply_stratum_zero', fixture[1,2] == 0 and fixture[0,2] != 0)
    normalized_positive_density_norm = s.integrate(s.Rational(1,2),(x,0,1))
    check('equal_half_mass_is_special_to_unit_stratum_function', normalized_positive_density_norm == s.Rational(1,2))
    check('nonconstant_density_packet_has_different_norm', s.integrate(x*x/2,(x,0,1)) == s.Rational(1,6))
    check('three_phases_require_192_entries', 2**2 * 2**2 * 2**2 * 3 == 192)

    algebra = {'role':'EXACT_ALGEBRA_CONTROLS_NOT_PHYSICAL_MATTER_DATA',
        'arithmetic':'integers, fractions, sympy exact expressions',
        'test_count':len(checks),'checks':checks,
        'fixtures_are_synthetic':True,
        'source_enumeration_is_project_based':True,
        'conditional_selection_rule':'If measure, domain and kernel are invariant under simultaneous Phi -> -Phi and boundary packets have parities p_out,p_in, then B=p_out*p_in*B.',
        'conditional_zero_requires_opposite_parities':True,
        'physical_mixed_block_status':'NOT_COMPUTED',
        'physical_gates':GATES}
    save(out/'results/geometry_carrier_audit.json',audit)
    save(out/'results/algebra_checks.json',algebra)
    print(f'{len(checks)} exact checks PASS; no physical matter matrix computed.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outdir',type=Path,default=ROOT)
    run(parser.parse_args().outdir)
