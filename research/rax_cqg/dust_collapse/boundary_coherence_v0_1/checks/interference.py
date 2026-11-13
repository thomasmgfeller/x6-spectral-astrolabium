"""Propagate preserved amplitude enclosures; never recompute their integrals.

The coherent instruments here are conditional constructions.  Their new
physical realization is not certified by the inherited numerical enclosure.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import mpmath
from mpmath import iv

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'sources/result_64.json'
PILOT = ROOT / 'sources/pilot.json'
EXPECTED_SOURCE = '5085b0f3d5bf2d9a70a184853c9d236fc2d41d7d2f7003b9c57ad980bdb34eae'
EXPECTED_PILOT = '442cc81227921135ccb046cdc238f8c2d9cae88f2082614490e59cfceba77ba3'
iv.dps = 75


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def real(value):
    q = F(value)
    return iv.mpf(q.numerator) / q.denominator


def read_real(bounds):
    lo, hi = map(F, bounds)
    require(lo <= hi, 'Reversed source interval')
    return iv.mpf([bounds[0], bounds[1]])


def read_complex(record):
    return iv.mpc(read_real(record['real']), read_real(record['imag']))


def boundary(value, upper=False):
    sign, man, exponent, bits = value._mpi_[int(upper)]
    require(bits >= 0, 'Nonfinite arithmetic')
    q = F((-1 if sign else 1) * man) * F(2) ** exponent
    scale = 10 ** 40
    n = -((-q.numerator * scale) // q.denominator) if upper else q.numerator * scale // q.denominator
    return ('-' if n < 0 else '') + str(abs(n) // scale) + '.' + str(abs(n) % scale).zfill(40)


def enc(value):
    if hasattr(value, '_mpi_'):
        return [boundary(value), boundary(value, True)]
    return {'real': enc(value.real), 'imag': enc(value.imag)}


def zero_inside(value):
    if hasattr(value, '_mpi_'):
        return value.a <= 0 <= value.b
    return zero_inside(value.real) and zero_inside(value.imag)


def norm2(z):
    return z.real ** 2 + z.imag ** 2


def conj(z):
    return iv.mpc(z.real, -z.imag)


def mzero():
    return [[iv.mpc(0) for _ in range(2)] for _ in range(2)]


def madd(a, b):
    return [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]


def mscale(t, a):
    if isinstance(t, F):
        t = real(t)
    return [[t * a[i][j] for j in range(2)] for i in range(2)]


def msub(a, b):
    return madd(a, mscale(-1, b))


def outer(row):
    return [[conj(row[i]) * row[j] for j in range(2)] for i in range(2)]


def matrix_enc(a):
    return [[enc(z) for z in row] for row in a]


def matrix_equal_enclosure(a, b):
    return all(zero_inside(a[i][j] - b[i][j]) for i in range(2) for j in range(2))


def effect(rows, gain):
    out = mzero()
    for row in rows:
        out = madd(out, mscale(gain ** 2, outer(row)))
    return out


def failure(effect_matrix, uniform_upper):
    ident = [[iv.mpc(int(i == j)) for j in range(2)] for i in range(2)]
    f = msub(ident, effect_matrix)
    # Analytic positivity is obtained before numerical values are used.
    require(uniform_upper < 1, 'Uniform contraction bound failed')
    f00, f11 = f[0][0].real, f[1][1].real
    det = f00 * f11 - norm2(f[0][1])
    require(det.a > 0, 'Failure determinant enclosure is not positive')
    delta = iv.sqrt(det)
    denom = iv.sqrt(f00 + f11 + 2 * delta)
    k = [[(f[i][j] + (delta if i == j else 0)) / denom for j in range(2)] for i in range(2)]
    kk = [[sum(conj(k[t][i]) * k[t][j] for t in range(2)) for j in range(2)] for i in range(2)]
    require(matrix_equal_enclosure(kk, f), 'Failure square-root enclosure inconsistency')
    return {'effect': matrix_enc(f), 'positive_principal_square_root': matrix_enc(k),
            'analytic_uniform_smallest_eigenvalue_lower_bound': str(1 - uniform_upper),
            'square_root_reconstruction_interval_contains_zero': True}


def rows_from_inputs(inputs):
    return [[inputs[i][j] for i in range(2)] for j in range(len(inputs[0]))]


def input_metrics(inputs, gamma, theta, gain):
    """Order: (atom,+),(atom,-),(positive,+),(positive,-)."""
    phase = iv.exp(iv.j * theta)
    gain_squared = real(gain) ** 2
    distributions = []
    for amps in inputs:
        z = sum(norm2(v) for v in amps)
        require(z.a > 0, 'Zero normalization')
        cross = [amps[s] * conj(amps[s + 2]) for s in range(2)]
        weights = []
        for s in range(2):
            base = norm2(amps[s]) + norm2(amps[s + 2])
            term = (conj(phase) * cross[s]).real
            weights.extend([base / 2 + gamma * term, base / 2 - gamma * term])
        require(all(w.a >= 0 for w in weights), 'Port weight enclosure not nonnegative')
        require(zero_inside(sum(weights) - z), 'Port probability conservation failure')
        plus = weights[0] + weights[2]
        distributions.append({
            'raw_weights': list(map(enc, weights)),
            'conditional_on_success': [enc(w / z) for w in weights],
            'unconditional_ports': [enc(gain_squared * w) for w in weights],
            'normalizer': enc(z), 'success': enc(gain_squared * z),
            'failure': enc(1 - gain_squared * z),
            'plus_conditional_on_success': enc(plus / z),
            'minus_conditional_on_success': enc(1 - plus / z),
            'plus_unconditional': enc(gain_squared * plus),
            'cross_by_stratum': list(map(enc, cross)),
            'cross_sum': enc(sum(cross)),
            'phase_scan_visibility': enc(2 * abs(gamma) * iv.sqrt(norm2(sum(cross))) / z),
            'coarse_stratum_probabilities': [enc((norm2(amps[s]) + norm2(amps[s + 2])) / z) for s in range(2)],
        })
    # Propagate from original interval variables, not rounded display intervals.
    zz = [sum(norm2(v) for v in amps) for amps in inputs]
    pp = []
    for amps, z in zip(inputs, zz):
        cc = sum(amps[s] * conj(amps[s + 2]) for s in range(2))
        pp.append(real('1/2') + gamma * (conj(phase) * cc).real / z)
    difference = pp[1] - pp[0]
    return {'gamma_real': str(gamma), 'theta': str(theta), 'inputs': distributions,
            'source_difference_gplus_minus_g0_plus_given_success': enc(difference),
            'source_difference_excludes_zero': not zero_inside(difference),
            'all_port_sums_equal_inherited_success_algebraically': True}


def direct_common_boundary(inputs, gain, bound):
    gain_squared = real(gain) ** 2
    rows = rows_from_inputs(inputs)
    summed = [[rows[s][i] + rows[s + 2][i] for i in range(2)] for s in range(2)]
    direct_effect = effect(summed, gain)
    distributions = []
    normers = []
    atom = []
    for amps in inputs:
        q = [norm2(amps[s] + amps[s + 2]) for s in range(2)]
        z = sum(q)
        require(z.a > 0, 'Direct coherent success unresolved')
        distributions.append({'raw_stratum_weights': list(map(enc, q)),
            'conditional_strata': [enc(v / z) for v in q],
            'unconditional_strata': [enc(gain_squared * v) for v in q],
            'success': enc(gain_squared * z), 'failure': enc(1 - gain_squared * z)})
        normers.append(z)
        atom.append(q[0] / z)
    contrast = atom[1] - atom[0]
    return {'amplitude_rule': 'C_s(g)=gain*(a_1s(g)+a_2s(g)); s remains a resolved inner stratum',
            'gain': str(gain), 'accepted_effect': matrix_enc(direct_effect),
            'uniform_accepted_effect_upper_bound': str(bound),
            'failure': failure(direct_effect, bound),
            'inputs': distributions,
            'source_difference_gplus_minus_g0_atom_given_success': enc(contrast),
            'source_difference_excludes_zero': not zero_inside(contrast),
            'comparison_to_completed_eraser': 'Direct accepted stratum effects are twice the plus-port effects; this changes success and needs its own failure.'}


def covariance_controls(inputs, gain):
    rows = rows_from_inputs(inputs)
    t0 = effect(rows, gain)
    theta = real(0)
    alpha, beta = real('1/3'), real('-2/5')
    aphase, bphase = iv.exp(iv.j * alpha), iv.exp(iv.j * beta)
    transformed_theta = theta + alpha - beta
    original = []
    transformed = []
    swapped = []
    for s in range(2):
        for sign in [1, -1]:
            original.append([(rows[s][i] + sign * rows[s + 2][i]) / iv.sqrt(2) for i in range(2)])
            transformed.append([(aphase * rows[s][i] + sign * iv.exp(iv.j * transformed_theta) * bphase * rows[s + 2][i]) / iv.sqrt(2) for i in range(2)])
            swapped.append([(rows[s + 2][i] + sign * rows[s][i]) / iv.sqrt(2) for i in range(2)])
    for a, b, c in zip(original, transformed, swapped):
        require(matrix_equal_enclosure(outer(a), outer(b)), 'Rephase covariance failure')
        require(matrix_equal_enclosure(outer(a), outer(c)), 'Class-name exchange failure')
    require(matrix_equal_enclosure(effect(original, gain), t0), 'Full E effect preservation failure')
    # Universal common-scalar control corresponding to the fixed-clock identity.
    e = (1 - iv.exp(-iv.j / 2)) / (iv.j / 2)
    common = (2 * e + e ** 2) / iv.sqrt(3)
    require(norm2(common).a > 0, 'Vanishing control multiplier')
    control_inputs = [inputs[0], [common * a for a in inputs[0]]]
    for gamma in [real(0), real('1/2'), real(1)]:
        control = input_metrics(control_inputs, gamma, theta, gain)
        diff = read_real(control['source_difference_gplus_minus_g0_plus_given_success'])
        require(zero_inside(diff), 'Common multiplier control failure')
    return {'full_E_completed_eraser_effect_preservation': True,
            'rephasing': {'alpha1': '1/3', 'alpha2': '-2/5',
                'rule': 'a_c -> exp(i alpha_c) a_c; theta -> theta+alpha1-alpha2',
                'each_port_effect_difference_encloses_zero': True,
                'meaning': 'Transport the analyzer phase with basis conventions; changing phases alone changes the instrument.'},
            'class_name_exchange_at_theta_zero': True,
            'fixed_clock_algebraic_control': {
                'rule': 'a_cs(gplus)=m*a_cs(g0) for common fixed t0,t1,t2; every nonzero-success normalized instrument response is equal.',
                'example_m': enc(common),
                'example': 'm=(2E(1/2)+E(1/2)^2)/sqrt(3)',
                'checked_gamma': ['0','1/2','1'],
                'not_a_new_fixed_clock_integration': True,
                'not_a_normalized_delta_clock_state': True}}


def history_relabeling(source):
    histories = source['scalar_histories']
    indexed = {tuple(map(tuple, x['relations'])): x for x in histories}
    checks = 0
    for h in histories:
        for aa, rr in product([(1,2),(2,1)], [(4,5),(5,4)]):
            permutation = dict(zip(range(6), (0,*aa,3,*rr)))
            rel = tuple(sorted((permutation[a],permutation[b]) for a,b in h['relations']))
            require(rel in indexed, 'History family not closed under boundary relabeling')
            target = indexed[rel]
            require((h['class'],h['F4'],h['scalar']) == (target['class'],target['F4'],target['scalar']),
                    'Transported scalar/history data changed')
            checks += 1
    return {'boundary_permutation_checks': checks,
            'group': 'S2(A) x S2(R)', 'class_counts': [4,2],
            'original_labelled_amplitude_weights': '1/6',
            'no_reweighting_or_reintegration': True}


def main():
    require(hashlib.sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED_SOURCE, 'Inherited source hash mismatch')
    require(hashlib.sha256(PILOT.read_bytes()).hexdigest() == EXPECTED_PILOT, 'Inherited pilot hash mismatch')
    source = json.loads(SOURCE.read_text())
    inputs = [[read_complex(z) for z in row] for row in source['analysis']['amplitudes']]
    gain = F(1,256)
    old_bound = F(264069,1310720)
    old_effect = effect(rows_from_inputs(inputs), gain)
    cases = {}
    raw_cases = {}
    for kappa in [1,0]:
        adjusted = [[a * iv.exp(iv.j * (kappa-1) * f) for a,f in zip(row,[9,9,-7,-7])] for row in inputs]
        raw_cases[kappa] = adjusted
        probes = {}
        for gamma in [F(0),F(1,2),F(1)]:
            probes[str(gamma)] = input_metrics(adjusted, real(gamma), real(0), gain)
        cases[str(kappa)] = {
            'interpretation': 'original gravity coefficient' if kappa==1 else 'counterfactual removal of gravitational phases only; not another observed physical setting',
            'completed_plus_minus': probes,
            'direct_common_boundary': direct_common_boundary(adjusted, gain, 2*old_bound),
        }
    # Old records have no cross terms; their coarse strata cannot see kappa.
    for row_a,row_b in zip(raw_cases[1],raw_cases[0]):
        for s in range(2):
            require(zero_inside(norm2(row_a[s])+norm2(row_a[s+2])-norm2(row_b[s])-norm2(row_b[s+2])),
                    'Dephased control depends on gravitational phase')
    phase_contrasts = {}
    for gamma in ['0','1/2','1']:
        deltas=[]
        for i in range(2):
            one=read_real(cases['1']['completed_plus_minus'][gamma]['inputs'][i]['plus_conditional_on_success'])
            off=read_real(cases['0']['completed_plus_minus'][gamma]['inputs'][i]['plus_conditional_on_success'])
            delta=one-off
            deltas.append({'kappa1_minus_kappa0':enc(delta),'excludes_zero':not zero_inside(delta)})
        phase_contrasts[gamma]=deltas
    result={
        'id':'BOUNDARY-COHERENCE-INHERITED-INTERVAL-PROPAGATION-0.1',
        'status':'INTERVAL_PROPAGATION_PASS_FROM_INHERITED_ENCLOSURES',
        'source_sha256':EXPECTED_SOURCE,'source_contract_sha256':EXPECTED_PILOT,
        'arithmetic':{'library':'mpmath.iv','version':mpmath.__version__,'decimal_precision':75,
                      'display_decimal_digits':40,'display_rounding':'lower floor, upper ceiling from exact binary interval endpoints'},
        'assumption_inheritance':'All displayed enclosures are conditional on the correctness and declared IEEE/numerical/analytic assumptions of the preserved source amplitude rectangles. This run does not certify their quadrature anew.',
        'new_integrals_evaluated':0,'scientific_amplitude_source':'Preserved result_64.json analysis.amplitudes, all real/imag endpoints used.',
        'frozen_diagnostic_settings':{'theta':'0','gain':'1/256','gamma':['0','1/2','1'],
            'inner_strata':'atom and positive remain distinct','input_order':['g0','gplus'],
            'port_order':[['atom','+'],['atom','-'],['positive','+'],['positive','-']],
            'no_angle_search':True,'theta_zero_was_already_previewed':'Not an independent blind prediction.'},
        'old_accepted_effect':matrix_enc(old_effect),
        'old_uniform_accepted_effect_upper_bound':str(old_bound),
        'old_failure':failure(old_effect,old_bound),
        'cases':cases,'gravity_phase_contrasts':phase_contrasts,
        'controls':covariance_controls(inputs,gain),
        'relabeling':history_relabeling(source),
        'analytic_identities':{
            'gamma_zero':'Classical forgetting/coarse-graining has no interference; q_s=sum_c |a_cs|^2.',
            'gamma_half':'Every port effect is the convex average of gamma=0 and gamma=1 effects, hence completely positive.',
            'completed_eraser':'Sum_(sign,s) E_sign,s = gain^2 sum_(c,s) a_cs^dagger a_cs for all states in E.',
            'direct_bound':'(a+b)^dagger(a+b) <= 2(a^dagger a+b^dagger b); Q_direct <= 2B I < 0.404 I.',
            'phase_sensitive_cross_term':'Re(exp(-i theta) gamma sum_s a_1s a_2s^*)',
            'relative_gravity_phase':'16*kappa-theta plus the retained matter/scalar phase',
            'coherent_dilation_required':'The accepted map V= gain sum_(c,s) a_cs |c,s> before dephasing is a new coherent realization, not a unitary change of the already dephased Kraus list.'},
        'physical_status':'AUXILIARY_INSTRUMENT_ONLY; unobserved environmental class records, physical calibration and gravitational backreaction are not established.'}
    target=Path(__file__).with_name('interference_results.json')
    target.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':result['status'],'new_integrals':0,
        'source_contrast_kappa1_gamma1':cases['1']['completed_plus_minus']['1']['source_difference_gplus_minus_g0_plus_given_success'],
        'phase_contrast_gamma1':phase_contrasts['1'],
        'direct_contrast_kappa1':cases['1']['direct_common_boundary']['source_difference_gplus_minus_g0_atom_given_success'],
        'output':str(target)},indent=2))


if __name__=='__main__':
    main()
