"""Test the N13 marginal as a state description and the coherence of the N14 detector."""
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

import sympy as sp

from cuts import reduced
from sector import scalar_image

ROOT = Path(__file__).resolve().parent


def scalar_isometry():
    """K=A U_a + B U_b: a scalar isometry requires a quadratic identity for W=U_a^*U_b."""
    left, right = [reduced(i)[0] for i in (1790, 5374)]
    swap = [3, 4, 5, 0, 1, 2]
    adjoint = -left[swap, swap]
    seed = sp.eye(3)
    assert scalar_image(adjoint, scalar_image(left, seed)) == seed
    first = scalar_image(adjoint, scalar_image(right, seed))
    second = scalar_image(adjoint, scalar_image(right, first))
    rates = [s[0,0] for s in (seed, first, second)]
    assert len(set(rates)) == 3
    for r in rates:
        assert sp.re(r) > 0
    return {"gaussian_rates_on_first_coordinate_line": [str(v) for v in rates],
            "dimension_of_span_g_Wg_W2g": 3,
            "nonzero_two_branch_coherent_sum_scalar_isometry_on_whole_chart": False}


def flat_prefactor():
    # Equal bulk Lebesgue measure on the two histories is an extra convention.
    # Identical powers of beta and 2pi cancel between these equal dimensions.
    products = []
    for mask in (1790, 5374):
        k, det, signature = reduced(mask)
        products.append(abs(det*k[:3,3:].det()))
    ratio_squared = sp.cancel(products[1]/products[0])
    assert ratio_squared == sp.Rational(42368,1995)
    return {"raw_norm_A_over_B_squared":str(ratio_squared),
            "raw_norm_A_over_B":float(sp.sqrt(ratio_squared)),
            "individually_normalized_scalar_transport_norm_ratio":1}


def run(input_dir):
    def read(name):
        return json.loads((input_dir / (name + '.json')).read_text())
    weights, sector, response = (read(n) for n in ('weights','sector','response'))
    assert [weights[k]['end'] for k in ('A','B')] == sector['order'] == response['order']
    step = Q(weights['example_shift'])
    base_mass = Q(weights['base_mass_per_selected_orbit'])
    assert 0 < step < base_mass and sum(map(Q,weights['common_unit_column_in_each_of_six_marked_cuts'].values())) == 1
    assert sector['rank'] == 2 and Q(sector['absolute_overlap_fourth_power_exact']) < 1
    root_weight = Q(1, 2)
    grids = []
    for grid in response['production_grids'][-2:]:
        density_rows = []
        for r, effects in enumerate(grid['coherent_effects']):
            curvatures, defects = [], []
            for i, m in enumerate(effects):
                real = [[Q(x[0]) for x in row] for row in m]
                # The anti-Hermitian part from floating-point assembly does not affect
                # the real quadratic form on these real amplitude coefficients.
                defect = real[0][0]+real[1][1]-real[0][1]-real[1][0]
                assert defect > 0
                assert abs(float(defect)-grid['delta_quadratic'][r][i]) < 1e-17
                # Cross-check against three independently evaluated two-branch preparations.
                minus, zero, plus = (Q(row[r][i]) for row in grid['pair_preparations'])
                assert abs(plus+minus-2*zero-defect/8) < Q(1,10**16)
                defects.append(defect)
                curvatures.append(2*(root_weight*step)**2*defect)
            success = sum(curvatures)
            # On c_A+c_B=1 the inherited failure probability is the complement.
            # In the linear coefficient chart its homogeneous representative J-S
            # evaluates to -||T delta||^2 in the marginal-null direction.
            assert sum(defects)>0
            conditional_fail_samples = [Q(state[r][3]) for state in grid['pair_preparations']]
            observed = conditional_fail_samples[2]+conditional_fail_samples[0]-2*conditional_fail_samples[1]
            assert observed < 0 and abs(observed+sum(defects)/8)<Q(1,10**14)
            density_rows.append({
                'density':response['densities'][r],
                'squared_norm_of_branch_difference':float(sum(defects)),
                'homogeneous_failure_form_on_marginal_null_vector':-float(sum(defects)),
                'second_difference_of_four_outcomes':list(map(float,curvatures+[-success])),
                'second_difference_of_success':float(success),
                'at_least_one_success_displacement_from_center':float(success/2)})
        grids.append({'grid':grid['grid'], 'densities':density_rows})
    for a,b in zip(grids[0]['densities'], grids[1]['densities']):
        assert abs(a['second_difference_of_success']-b['second_difference_of_success']) < 1e-21
    return {'checked_grids':grids, 'root_weight':str(root_weight), 'conditional_step':str(step),
            'full_endpoint_transfer':True,
            'relative_phase_optimized_squared_scalar_distance':2*(1-sector['absolute_overlap']),
            'minimal_extra_complex_coordinates_on_this_pair':1,
            'coherent_scalar_isometry_test':scalar_isometry(), 'scalar_norm_conventions':flat_prefactor()}


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Assertions must be enabled')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('output', type=Path)
    p.add_argument('--inputs', type=Path, default=ROOT)
    args = p.parse_args()
    args.output.write_text(json.dumps(run(args.inputs),sort_keys=True,indent=2,allow_nan=False)+'\n')
