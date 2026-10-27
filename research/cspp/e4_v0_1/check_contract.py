#!/usr/bin/env python3
"""Check the E4 draft and refuse premature confirmation; no field simulation.

Standard library only. Scientific evidence verification is deliberately absent
in draft-1, so --require-frozen always blocks until a reviewed implementation
of that verifier is added. Never use Python assertions as execution gates.
"""
import argparse
import copy
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
EVIDENCE_VERIFIER_IMPLEMENTED = False


def fraction(value):
    return Fraction(str(value))


def structural_errors(c):
    errors = []

    def require(ok, message):
        if not ok:
            errors.append(message)

    try:
        require(c['schema'] == 'cspp.e4.contract/0.1', 'wrong schema')
        require(bool(re.fullmatch(r'[0-9a-f]{40}', c['base_commit'])), 'invalid base commit')
        require(c['status'] in ('DRAFT', 'FROZEN'), 'unknown contract status')
        require(c['execution_status'] == 'NOT_RUN', 'draft checker cannot attest experiment execution')
        require(c['units']['metric_diagonal'] == [-1, 1, 1, 1], 'signature changed without checker revision')
        g, s, d = c['geometry'], c['source'], c['detector']
        half = fraction(g['diamond_half_duration_L0'])
        volume_coefficient = (2 * half)**4 / 24
        require(volume_coefficient == fraction(g['four_volume_over_pi_L0_4']), 'diamond volume mismatch')
        require(g['sprinkling'] == 'homogeneous_Poisson' and not g['fixed_N_primary'], 'primary law must be Poisson')
        t0, td, radius = map(fraction, (s['time_L0'], d['time_L0'], s['radius_L0']))
        require(t0 < td and radius > 0, 'invalid source/time order')
        require(s['center_L0'] == [0, 0, 0], 'support proof assumes centered source')
        margin = half - abs(td) - (radius + td - t0)
        require(margin > 0 and margin == fraction(d['wave_support_margin_at_detector_L0']), 'source support touches diamond boundary')
        require(radius < half - abs(t0), 'initial source outside diamond')
        dc = d['center_L0']
        require(dc[:2] == [0, 0], 'detector containment checker assumes z-axis center')
        require(abs(fraction(dc[2])) + fraction(d['radius_L0']) < half - abs(td), 'detector outside diamond')
        require(0 < d['conditional_q_lower_min'] < 1, 'conditional normalization needs positive lower bound')
        require(not d['same_node_ids_across_clouds'], 'cross-cloud node IDs cannot identify detectors')
        require(c['matter']['flavors'] == ['f0', 'f1'], 'this checker is two-flavor only')
        require(len(c['matter']['masses_L0']) == 2, 'two masses required')
        require(sum(x*x for x in s['spinor_real']) == 1, 'source spinor is not normalized')
        require(not s['positive_energy_projected'], 'compact-source reference changed')
        o, a, st = c['observables'], c['accuracy'], c['statistics']
        require(o['primary'] == ['w0', 'w1', 'C_det'], 'primary targets changed')
        require(len(o['ensemble_channels']) == st['ensemble_channels_per_cell'] == 8, 'multiplicity must cover eight channels')
        require(len(o['channel_ranges']) == 8, 'missing bounded ranges')
        require(all(fraction(hi)-fraction(lo) == 1 for lo, hi in o['channel_ranges']), 'Hoeffding formula assumes width one')
        require(o['store_complex_offdiagonals'] and not o['silently_clip_or_renormalize'], 'state information or validation lost')
        require(not o['extra_measurement_shots'], 'shot noise requires a new budget')
        state_error = sum(map(fraction, a['trace_distance_budget'].values()))
        h = fraction(a['mean_statistical_halfwidth_max'])
        require(all(fraction(v) >= 0 for v in a['trace_distance_budget'].values()), 'negative error allocation')
        require(state_error + h <= fraction(a['weight_absolute_tolerance']), 'weight budget exceeded')
        require(2*state_error + h <= fraction(a['C_det_absolute_tolerance']), 'coherence budget exceeded')
        require(a['C_det_trace_distance_lipschitz'] == 2, 'wrong coherence Lipschitz factor')
        risk = sum(map(fraction, st['alpha'].values()))
        require(risk <= fraction(st['alpha_total']) <= Fraction(1, 20), 'campaign alpha exceeded')
        require(all(0 < fraction(v) < 1 for v in st['alpha'].values()), 'invalid alpha allocation')
        require(st['mode'] == 'fixed_M_after_independent_pilot' and not st['adaptive_stopping_allowed'], 'fixed-sample fallback cannot support adaptive stopping')
        gates = c['gates']
        require(gates['keep_all_planned_realizations'] and not gates['conditional_G2_statistics_primary'], 'selection bias in primary target')
        require(not gates['assert_only_gate'], 'execution guard must not rely on assertions')
        require(all(gates[k]['status'] == 'NOT_RUN' for k in ('G1', 'G2', 'G3')), 'draft cannot claim numerical gate PASS')
        require(0 < gates['availability_lower_min'] < 1, 'invalid availability target')
        p, r = c['pilot'], c['rng']
        require(all(x > 0 for x in p['nu_grid']) and len(set(p['nu_grid'])) == len(p['nu_grid']), 'invalid pilot density grid')
        require(0 < p['initial_realizations_per_cell'] <= p['maximum_realizations_per_cell'], 'invalid pilot sizes')
        require(not p['uses_confirmation_data'], 'pilot leaks confirmation data')
        require(r['bit_generator'] == 'PCG64DXSM', 'generator not pinned')
        require(len(set(r['phase_ids'].values())) == len(r['phase_ids']), 'phase IDs collide')
        require(len(set(r['role_ids'].values())) == len(r['role_ids']), 'role IDs collide')
        require(all(isinstance(x, int) and x >= 0 for x in list(r['phase_ids'].values()) + list(r['role_ids'].values())), 'RNG IDs must be nonnegative integers')
        require(not r['python_hash_seed_derivation'] and r['preserve_raw_clouds'], 'RNG provenance insufficient')
        require(not c['visualization']['BD_layers_are_time_frames'], 'BD layers are not time frames')
        require(not c['scaling']['finite_scan_proves_limit'], 'finite scan cannot prove a limit')
        if c['status'] == 'DRAFT':
            require(c['freeze_status'] == 'NOT_FROZEN', 'draft falsely labeled frozen')
            require(c['freeze']['timestamp_UTC'] is None and not c['freeze']['evidence_verifier_pass'], 'draft has false freeze attestation')
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append('malformed contract: ' + str(exc))
    return errors


def freeze_blockers(c):
    blocks = []
    if c.get('status') != 'FROZEN' or c.get('freeze_status') != 'FROZEN':
        blocks.append('contract is explicitly NOT_FROZEN')
    for key, value in c.get('open_decisions', {}).items():
        if value is None:
            blocks.append('open decision: ' + key)
    if c.get('rng', {}).get('confirmation_master_seed') is None:
        blocks.append('confirmation master seed not fixed')
    for key in ('timestamp_UTC', 'source_digest_manifest', 'protocol_digest'):
        if c.get('freeze', {}).get(key) is None:
            blocks.append('missing freeze field: ' + key)
    if not EVIDENCE_VERIFIER_IMPLEMENTED:
        blocks.append('draft checker has no implemented scientific evidence/hash verifier')
    return blocks


def add(a, b):
    return [[x+y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, z):
    return [[z*x for x in row] for row in a]


def mul(a, b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def algebra_checks():
    # Integer/Gaussian-integer entries: all equalities below are exact.
    count = 0
    I, zero = identity(4), [[0]*4 for _ in range(4)]
    pauli = [[[0, 1], [1, 0]], [[0, -1j], [1j, 0]], [[1, 0], [0, -1]]]
    beta = [[(1 if i < 2 else -1) if i == j else 0 for j in range(4)] for i in range(4)]
    alpha = [[[s[i % 2][j % 2] if (i < 2) != (j < 2) else 0 for j in range(4)] for i in range(4)] for s in pauli]
    gamma = [scale(beta, 1j)] + [scale(mul(beta, a), 1j) for a in alpha]
    eta = [-1, 1, 1, 1]
    for i in range(4):
        for j in range(4):
            target = scale(I, 2*eta[i]) if i == j else zero
            if add(mul(gamma[i], gamma[j]), mul(gamma[j], gamma[i])) != target:
                raise ValueError('Clifford convention failed')
            count += 1
    for mass in (0, 1, 2):
        for momentum in ((0, 0, 0), (1, 2, 3), (-2, 0, 1)):
            H = scale(beta, mass)
            for p, a in zip(momentum, alpha):
                H = add(H, scale(a, p))
            if mul(H, H) != scale(I, mass*mass + sum(p*p for p in momentum)):
                raise ValueError('Hamiltonian square failed')
            count += 1
    # Same diagonal, opposite relative phase: same color, different state.
    rho_plus = [[0.5, 0.5], [0.5, 0.5]]
    rho_minus = [[0.5, -0.5], [-0.5, 0.5]]
    mean = scale(add(rho_plus, rho_minus), 0.5)
    if 2*abs(rho_plus[0][1]) != 1 or 2*abs(rho_minus[0][1]) != 1 or mean != [[0.5, 0], [0, 0.5]]:
        raise ValueError('coherence distinction failed')
    return count + 1


def negative_controls(c):
    mutations = [
        ('wrong_volume', lambda x: x['geometry'].update(four_volume_over_pi_L0_4='511/3')),
        ('boundary_contact', lambda x: x['source'].update(radius_L0=1)),
        ('zero_normalization_guard', lambda x: x['detector'].update(conditional_q_lower_min=0)),
        ('alpha_overrun', lambda x: x['statistics']['alpha'].update(geometry_campaign=0.2)),
        ('state_budget_overrun', lambda x: x['accuracy']['trace_distance_budget'].update(geometry=0.02)),
        ('optional_stopping_with_fixed_interval', lambda x: x['statistics'].update(adaptive_stopping_allowed=True)),
        ('survivorship_bias', lambda x: x['gates'].update(conditional_G2_statistics_primary=True)),
        ('phase_collision', lambda x: x['rng']['phase_ids'].update(confirmation=1)),
        ('false_gate_PASS', lambda x: x['gates']['G2'].update(status='PASS')),
        ('BD_time_frames', lambda x: x['visualization'].update(BD_layers_are_time_frames=True)),
    ]
    names = []
    for name, mutate in mutations:
        candidate = copy.deepcopy(c)
        mutate(candidate)
        if not structural_errors(candidate):
            raise ValueError('negative control not rejected: ' + name)
        names.append(name)
    forged = copy.deepcopy(c)
    forged['status'] = forged['freeze_status'] = 'FROZEN'
    forged['open_decisions'] = {k: 'unverified claim' for k in forged['open_decisions']}
    forged['freeze'].update(timestamp_UTC='unverified', source_digest_manifest='unverified', protocol_digest='unverified', evidence_verifier_pass=True)
    forged['rng']['confirmation_master_seed'] = 1
    if not freeze_blockers(forged):
        raise ValueError('forged metadata bypassed evidence-verifier requirement')
    names.append('forged_freeze_without_evidence_verifier')
    return names


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--contract', type=Path, default=ROOT/'contract.json')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--require-frozen', action='store_true')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = args.contract.read_bytes()
    c = json.loads(raw)
    errors = structural_errors(c)
    if errors:
        print(json.dumps({'status': 'FAIL_CONTRACT', 'errors': errors}, indent=2))
        return 1
    blocks = freeze_blockers(c)
    report = {
        'status': 'PASS_CONTRACT_DRAFT',
        'experiment_status': 'NOT_RUN',
        'claim': 'contract consistency and finite algebra only; no field evolution or statistical campaign',
        'contract_sha256': hashlib.sha256(raw).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'structural_errors': [],
        'exact_algebra_checks': algebra_checks(),
        'negative_controls_rejected': negative_controls(c) if args.self_test else [],
        'freeze_blockers': blocks,
        'hypothetical_Hoeffding_M_per_cell_for_four_cells': math.ceil(math.log(2*8*4/c['statistics']['alpha']['ensemble_simultaneous'])/(2*c['accuracy']['mean_statistical_halfwidth_max']**2)),
        'sample_size_note': 'planning illustration only; neither selected nor executed ensemble size',
    }
    if args.require_frozen and blocks:
        report['status'] = 'BLOCKED_NOT_FROZEN'
    result = json.dumps(report, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.write_text(result, encoding='utf-8')
    print(result, end='')
    return 2 if args.require_frozen and blocks else 0


if __name__ == '__main__':
    sys.exit(main())
