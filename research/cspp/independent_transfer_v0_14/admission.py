"""Deterministic, fail-closed review of the concrete published v0.13 model."""
import argparse
from fractions import Fraction as F
import gzip
import hashlib
import json
from math import comb
from pathlib import Path
from flint import arb, acb, ctx
from inference import require

HERE = Path(__file__).resolve().parent
PREVIOUS = HERE.parent/'fluctuation_transfer_v0_13'


def read(path):
    return json.loads(Path(path).read_text())


def encode(value):
    if isinstance(value, arb):
        return value.str(70)
    if isinstance(value, acb):
        return {'re': encode(value.real), 'im': encode(value.imag)}
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [encode(v) for v in value]
    return value


def freeze_check():
    for name, digest in read(HERE/'FREEZE.json')['sha256'].items():
        require(hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest,
                'input integrity: '+name)


def exact_geometry():
    # 4*pi int_0^(1/2) r^2(3-r) dr; history volume/pi = (4/3) int_0^3 s^3 ds.
    R = F(1, 2)
    return {'source_volume_over_pi': 4*(R**3-R**4/4),
            'history_volume_over_pi': F(4, 3)*F(3**4, 4)}


def structural_certificates():
    geometry = exact_geometry()
    lam = 3*geometry['source_volume_over_pi']
    lamH = 3*geometry['history_volume_over_pi']
    p = (-arb(lam.numerator)/lam.denominator).exp()
    H = arb(lamH.numerator)/lamH.denominator
    failure = (-H).exp()*sum(H**j/arb(j).fac() for j in range(4))
    with gzip.open(HERE.parent/'full_continuum_v0_12/results/BENCHMARK_192.json.gz', 'rt') as f:
        reference = json.load(f)
    c = [acb(arb(w['normalized_value'][0]), arb(w['normalized_value'][1]))
         for w in reference['reference']['windows']]
    tau = arb(read(HERE.parent/'full_continuum_v0_12/PROTOCOL.json')['comparison_tolerance'])
    require(all(z.abs_lower() > tau for z in c), 'zero response exceeds historical pointwise tolerance')
    # Independent rational verification of the global weight bound, not a sample maximum.
    weights = [sum(F(coef)*comb(n, j)*F(1, 16)**j*F(15, 16)**(n-j)
                   for j, coef in enumerate((1, -9, 16, -8)) if j <= n)
               for n in range(128)]
    N = 128; r = arb(15)/16; u = arb(1)/15
    tail = r**N*(1+9*N*u+8*N*N*u*u+arb(4)/3*N**3*u**3)
    require(max(abs(w) for w in weights) < 2 and N*(-r.log()) > 3 and tail < 2,
            'global weight bound for all nonnegative counts')
    rho = 3/arb.pi(); a = 4*(rho/96).sqrt(); beta = a/(16*(a+1)); b = 2*beta
    V2 = (512*((1+b)**2-1)).exp()
    V4 = (512*((1+b)**4-1)).exp()
    return {'geometry': {k: str(v) for k,v in geometry.items()},
            'source_history_mean': str(lam), 'history_mean': str(lamH),
            'zero_response_probability_lower': p,
            'joint_historical_tolerance_failure_probability_lower': p,
            'joint_historical_tolerance_success_probability_upper': 1-p,
            'historical_per_realization_tolerance': tau,
            'reference': c, 'reference_magnitudes': [abs(z) for z in c],
            'RMS_error_floor_enclosures': [p.sqrt()*abs(z) for z in c],
            'mean_covariance_PSD_factor': p/(1-p),
            'nonlocal_undefined_probability_lower': failure,
            'beta': beta, 'global_weight_abs_upper': 2,
            'local_second_moment_majorant': V2,
            'local_fourth_moment_majorant': V4,
            'moment_majorants_are_predictions': False,
            'macroscopic_mean_rejected': False,
            'new_RMS_target_selected': False}


def assess(checks, prediction, method_evidence):
    require(checks['status'] == 'PASS', 'predecessor implementation checks must pass')
    require(checks['analytical_tests'] == 27 and checks['enclosed_prediction_comparisons'] == 105,
            'known control inventory')
    require(prediction['original_ensemble_moments'] == 'NOT_EVALUATED' and
            prediction['nonlocal_ensemble'] == 'MODEL_HOLD', 'unexpected evidence requires new reviewed revision')
    required = read(HERE/'PROTOCOL.json')['required_method_certificates']
    candidates = {}
    for name, evidence in method_evidence.items():
        require(name in ['local_H1','nonlocal_PU_H1'], 'no substitute candidate allowed')
        require(evidence.get('joint_original_moments') != 'PASS',
                'a control pass cannot replace absent original moment enclosures')
        if name == 'nonlocal_PU_H1':
            require(evidence.get('total_ensemble_map') != 'PASS',
                    'the frozen nonlocal map is not total')
        failed = [key for key in required if evidence.get(key) != 'PASS']
        candidates[name] = {'method_evidence': evidence, 'missing_certificates': failed,
                            'decision': 'REJECTED_FOR_CONFIRMATORY_RUN'}
    return candidates


def compute(bits):
    freeze_check(); ctx.prec = bits
    p = read(HERE/'PROTOCOL.json')
    require(all(value is None for value in p['new_design'].values()), 'no premature confirmatory design')
    checks = read(PREVIOUS/'results/CHECKS.json')
    prediction = read(PREVIOUS/'results/PREDICTIONS_192.json')
    proof = structural_certificates()
    common = {'control_reproduction': 'PASS',
              'joint_original_moments': 'NOT_EVALUATED',
              'ensemble_numerical_error': 'NOT_CERTIFIED',
              'sampling_law_alignment': 'NOT_CERTIFIED'}
    evidence = {
        'local_H1': dict(common, total_ensemble_map='PASS', fourth_moment_or_valid_tail_control='PASS'),
        'nonlocal_PU_H1': dict(common, total_ensemble_map='UNDEFINED_ON_POSITIVE_PROBABILITY_SET',
                             fourth_moment_or_valid_tail_control='NOT_CERTIFIED')}
    candidates = assess(checks, prediction, evidence)
    old = read(HERE.parent/'independent_g1_v0_8/results/DECISION_128.json')
    cell = next(c for c in old['cells'] if c['nu'] == 512 and c['epsilon'] == '1/16')
    require(cell['status'] == 'REJECTED', 'known necessary operator condition')
    return encode({'schema': p['schema'], 'precision_bits': bits, 'base_commit': p['base_commit'],
        'admission': 'REJECTED_FOR_CONFIRMATORY_RUN', 'candidates': candidates,
        'fluctuation_prediction_decision': 'NOT_TESTED_METHOD_GATE_FAILED',
        'macroscopic_decision': {
            'ensemble_mean': 'NOT_ESTABLISHED',
            'local_almost_sure_historical_tolerance_claim': 'ANALYTICALLY_REFUTED',
            'local_RMS': 'RIGOROUS_LOWER_BOUNDS_ONLY_NO_NEW_TARGET',
            'nonlocal_full_ensemble': 'UNDEFINED',
            'previous_operator_cell': cell['status'],
            'previous_operator_rejected_fields': sum(t['status'] == 'REJECT_RMS_LE_0.1' for t in cell['tests']),
            'previous_operator_evidence_is_new_detector_test': False},
        'structural_certificates': proof,
        'new_design': p['new_design'], 'power_and_cost': 'NOT_DESIGNED_METHOD_GATE_FAILED',
        'new_random_clouds': 0, 'new_rng_calls': 0, 'confirmation_seed_used': False,
        'public_preregistration': False, 'fresh_data_evidence': None,
        'overall_status': 'METHOD_HOLD', 'G1': 'HOLD'})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bits', type=int, choices=[128,192], required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = compute(args.bits)
    args.out.write_text(json.dumps(result, indent=2)+'\n')
    print(result['admission'])
