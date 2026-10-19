"""Fixed descriptive feasibility decision; no operator-performance claim."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
from jf_common import config, encode
from volume_analysis import load
from joint import design_check
from intrinsic import ETA, noise_guard


def stats(values):
    return dict(minimum=float(min(values)), median=float(np.median(values)), maximum=float(max(values))) if values else None


def validate(row, c, guards):
    s = row['selection']; w = s['selected']
    assert hashlib.sha256(encode(s).encode()).hexdigest() == row['selection_seal']
    assert row['joint_pass'] == (w is not None and row['audit']['passed'])
    if w is None:
        assert row['audit']['status'] == 'not_selected'
        return True
    assert s['status'] == 'selected' and len(set(w['support'])) == len(w['support'])
    assert min(map(len, w['support_sides'])) >= c['minimum_support_per_side']
    assert max(map(len, w['support_sides'])) <= c['maximum_support_per_side']
    assert set(w['support']) == set(w['temporal']+w['support_sides'][0]+w['support_sides'][1])
    for branch in [w['certificate'], row['audit']['certificate']]:
        assert branch['status'] == 'ok'
        h, v, t = [np.array(branch[k]) for k in ('gram', 'vectors', 'transform')]
        np.testing.assert_allclose(t@h@t.T, ETA, atol=1e-9, rtol=1e-9)
        np.testing.assert_allclose((t@v).T, branch['features'], atol=1e-9, rtol=1e-9)
        hd = list(zip(map(np.array, branch['half_grams']), map(np.array, branch['half_vectors'])))
        recomputed = noise_guard(h, v, t, hd, branch['interval_counts'], branch['half_interval_counts'], branch['condition'], guards)
        assert recomputed['checks'] == branch['guard']['checks']
        assert recomputed['passed'] == branch['guard']['passed']
    assert w['certificate']['guard']['passed']
    assert row['audit']['passed'] == row['audit']['certificate']['guard']['passed']
    assert design_check(w['certificate']['features'], w['scale'], c)['passed']
    assert row['direct_control']['selection_guard']
    return True


def summarize(directory):
    c, oc, guards, cfg = config()
    execution, rows = load(directory)
    expected = [(rho, seed) for i, rho in enumerate(c['densities']) for seed in
                (c['development_seeds'] if execution['mode'] == 'development' else
                 [c['test_seed_base']+100*i+j for j in range(c['test_replicates_per_density'])])]
    complete = execution['status'] == 'COMPLETE' and [(r['rho'], r['seed']) for r in rows] == expected
    budget = execution['seconds'] <= c['wall_budget_seconds'] and execution['peak_mib'] <= c['memory_budget_mib']
    controls = execution['controls']['status'] == 'PASS' and all(r['direct_control']['status'] == 'PASS' and
                (r['transport_control'] is None or r['transport_control']['status'] == 'PASS') for r in rows)
    certificates = all(validate(r, c, guards) for r in rows)
    cells = []
    for rho in c['densities']:
        group = [r for r in rows if r['rho'] == rho]
        selected = [r for r in group if r['selection']['selected'] is not None]
        reasons, failures = {}, {}
        for r in group:
            status = r['selection']['status']; reasons[status] = reasons.get(status, 0)+1
            if r['selection']['selected'] is not None and not r['audit']['passed']:
                for key in r['audit']['certificate']['guard']['reasons']:
                    failures[key] = failures.get(key, 0)+1
        cells.append(dict(rho=rho, total=len(group), original_guarded=sum(r['original_guard_pass'] for r in group),
                          temporal_count_pass=sum(any(s['status'] == 'searched' for s in r['selection']['shells']) for r in group),
                          any_count_triple=sum(any(s.get('frames', {}).get('count_qualified_triples', 0)>0 for s in r['selection']['shells']) for r in group),
                          any_conditioned_frame=sum(any(s.get('frames', {}).get('signature_condition', 0)>0 for s in r['selection']['shells']) for r in group),
                          any_stable_gram=sum(any(s.get('frames', {}).get('stable_gram', 0)>0 for s in r['selection']['shells']) for r in group),
                          selected=len(selected), joint_pass=sum(r['joint_pass'] for r in group),
                          selection_statuses=reasons, held_out_failure_reasons=failures,
                          selected_count_scales={str(k): sum(r['selection']['selected']['lower_count'] == k for r in selected) for k in c['count_shell_lower_bounds']},
                          scale_ratio=stats([r['selection']['selected']['scale_ratio'] for r in selected]),
                          support_sizes=stats([len(r['selection']['selected']['support']) for r in selected]),
                          frame_condition=stats([r['selection']['selected']['certificate']['condition'] for r in selected]),
                          design_condition=stats([r['selection']['selected']['design']['condition'] for r in selected]),
                          coordinate_lorentz_gram_error=stats([r['coordinate_diagnostic']['lorentz_gram_relative_error'] for r in selected])))
    primary = next(x for x in cells if x['rho'] == c['primary_density'])
    rate = primary['joint_pass']/primary['total'] if primary['total'] else 0.
    supported = complete and budget and controls and certificates and rate >= c['minimum_joint_fraction']
    return dict(schema='x6.bk-joint-summary/1', mode=execution['mode'], complete=complete,
                budget_pass=budget, controls_pass=controls, certificates_pass=certificates,
                clouds=len(rows), cells=cells, primary_joint_fraction=rate,
                decision=('JOINT_FEASIBILITY_SUPPORTED' if supported else 'JOINT_FEASIBILITY_HOLD') if execution['mode'] == 'test' else 'DEVELOPMENT_ONLY',
                phase3='HOLD_PHASE3', limits='Bounded search, changed supports and resolution; thinning checks are not confidence guarantees; no derivative or curvature qualification.')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('directory', type=Path); a = p.parse_args()
    summary = summarize(a.directory)
    output = a.directory/'summary.json'
    if output.exists():
        raise SystemExit('Refusing to overwrite summary')
    output.write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))
