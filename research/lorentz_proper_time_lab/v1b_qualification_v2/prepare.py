"""SPDX-License-Identifier: Apache-2.0
Run once BEFORE any target clouds. No target sampler is called here.
"""
import hashlib
import json
import secrets
from pathlib import Path
import numpy as np
from scipy.stats import binom
from bounds import cp, interval_table, marginal_specs

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def write(name, obj):
    (HERE/name).write_text(json.dumps(obj, indent=2, allow_nan=False)+'\n')


def prepare():
    assert not (HERE/'protocol.json').exists(), 'Do not replace a frozen protocol/seed draw.'
    m, repetitions, eps = 4096, 8192, .02
    gate_count = 6*3 + sum(len(marginal_specs(d)) for d in [2, 3, 4])
    assert gate_count == 52
    alpha = .05/gate_count
    cells = []
    for d in [2, 3, 4]:
        tab = interval_table(m, d, eps)
        k = np.arange(m+1)
        for theta in [.1, .2, .4, .7]:
            p = theta**d
            weights = binom.pmf(k, m, p)
            coverage = (tab['low'] <= theta) & (theta <= tab['high'])
            precision = tab['radius'] <= .1
            covered = float(weights[coverage].sum())
            joint = float(weights[coverage & precision].sum())
            powers = {}
            for name, target, actual in [('coverage', .95, covered), ('joint', .90, joint)]:
                # Exact critical number of successful independent clouds.
                lo, hi = 0, repetitions
                while lo < hi:
                    mid = (lo+hi)//2
                    if cp(mid, repetitions, alpha)[0] >= target:
                        hi = mid
                    else:
                        lo = mid+1
                powers[name] = dict(critical_successes=lo,
                    ideal_probability_of_passing=float(binom.sf(lo-1, repetitions, actual)))
            cells.append(dict(d=d, theta=theta, primary=theta in [.4, .7], p=p,
                expected_k=m*p, allowable_mean_count_fraction=[p*(1-eps)**d, p*(1+eps)**d],
                ideal_coverage=covered, ideal_precision=float(weights[precision].sum()),
                ideal_joint=joint, powers=powers))
    assert all(c['powers'][name]['ideal_probability_of_passing'] >= .9
               for c in cells if c['primary'] for name in ['coverage', 'joint'])
    write('planning.json', dict(model='Analytic binomial planning, not observed target data', cells=cells))
    prior = json.loads((HERE.parent/'v1b_radial_audit/results/control/schedule.json').read_text())
    excluded = sorted({0, 1, 20261017, 4294967295, 2463401483} |
                      {x['seed'] for x in prior['mulberry32']})
    skipped = []
    def draw(n):
        out = []
        while len(out) < n:
            seed = secrets.randbits(32)
            if seed in excluded:
                skipped.append(seed)
            else:
                out.append(seed)  # New duplicates MUST be retained: sampling with replacement.
        return out
    groups = [dict(id=f'native-d{d}', d=d, arm='native', seeds=draw(repetitions)) for d in [2, 3, 4]]
    groups += [dict(id=f'{arm}-d4', d=4, arm=arm, seeds=draw(512))
               for arm in ['wrong-radius', 'repeated-point']]
    write('seeds.json', dict(method='secrets.randbits(32), with replacement, rejection of fixed prior-seed list only',
        excluded_prior_seeds=excluded, rejected_draws=skipped,
        eligible_population=2**32-len(excluded), groups=groups))
    files = ['prepare.py', 'bounds.py', 'qualified.cjs', 'collect.cjs', 'analyze.py',
             'verify.py', 'DERIVATION.md', 'planning.json', 'seeds.json']
    pins = {x: hashlib.sha256((HERE/x).read_bytes()).hexdigest() for x in files}
    protocol = dict(schema='x6.v1b-scoped-qualification/2', date='2026-10-21',
        base_commit='2bf7b9e29acb120696858758fe8a39d5d71d09db',
        scope='Flat Minkowski; native core.js 1.1; T=1 (homogeneous scaling only); central nested diamonds; d in {2,3,4}; m=4096; theta in {0.4,0.7}; new qualifiedInterval wrapper only.',
        inherited_goal=dict(relative_precision=.1, coverage=.95, joint_covered_and_precise_probability=.90),
        engineering_allocation=dict(scale_equivalent_mean_bias=eps, marginal_cdf_absolute_tolerance=.005),
        m=m, repetitions=repetitions, dimensions=[2,3,4], theta_grid=[.1,.2,.4,.7],
        primary_theta=[.4,.7], family_alpha=.05, gates=gate_count, alpha_per_gate=alpha,
        independent_unit='One cloud from one independently uniform fresh eligible 32-bit seed. No within-cloud independence assumed. OS random source is a declared assumption.',
        mean_method='Clipped empirical Bernstein plus two exact binomial tail upper bounds; four errors alpha_gate/4. See DERIVATION.md.',
        proportion_method='Two-sided exact Clopper-Pearson confidence interval at 1-alpha_gate across independent clouds.',
        decision='PASS if all 52 gates PASS and all engineering/positive controls pass; FAIL if any statistical gate FAIL or hard validation fails; otherwise UNENTSCHIEDEN. Missing/incomplete run is UNENTSCHIEDEN, never PASS.',
        primary_points=3*m*repetitions, control_budget=dict(clouds_per_arm=512,
            wrong_radius_points=512*m, repeated_point_generated_points=512),
        positive_controls='Wrong radius: replace r=A*U^(1/3) by A*U in 4D; at least one radial gate must FAIL. Repeated point: repeat first point m times; both 4D coverage gates must FAIL.',
        zero_radius_policy='Recover the generating normal direction from the accepted candidate uniform calls; do not discard a point.',
        stop_rule='One execution, all frozen seeds in order; keep duplicate seeds and rejected candidates. No additional seeds, no statistical peeking or threshold/source changes. 1200 seconds total collection; exception/timeout preserves partial records and yields UNENTSCHIEDEN. Reanalysis of identical archived records is permitted; new target generation is not.',
        technical_tolerances=dict(transform_absolute=1e-12, native_interval_absolute=2e-10,
                                  archive_float_abs=1e-12, archive_float_rel=1e-12),
        runtime=dict(node_major=24, python='3.12', numpy='2.3.5', scipy='1.17.0'),
        core_sha256=hashlib.sha256((HERE.parent/'core.js').read_bytes()).hexdigest(),
        frozen_files=pins,
        historical_decision='V1b NOT_PASSED remains unchanged; HOLD_PHASE3 remains unchanged.',
        limits=['Finite seed-population guarantee, conditional on uniform independent seed selection; no individual-seed guarantee.',
                'Selected CDF probes are not a global uniformity proof.',
                'No qualification of other theta, m, placements, adaptive stopping, curved space, unknown T/d, or physical reality.',
                'The wrapper is a new reference analysis; the existing browser interval is not changed or newly qualified.',
                'A 2% mean scale-bias bound alone does not imply binomial counts; empirical seed-level coverage is separately required.'])
    write('protocol.json', protocol)
    print(json.dumps(dict(gates=gate_count, seeds=sum(len(g['seeds']) for g in groups),
        primary_points=protocol['primary_points'], planning_primary=[c for c in cells if c['primary']])))


if __name__ == '__main__':
    prepare()
