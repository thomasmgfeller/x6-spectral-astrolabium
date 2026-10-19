"""Predeclared primary arm; every missing cloud and fallback stays visible."""
import argparse
from collections import Counter
import json
from pathlib import Path
from od_common import config
from im_analysis import validate_record
from volume_analysis import load, rms
from moment_analysis import stats


def validate(row, ic):
    certificates = True
    for stage in row['stages']:
        certificates = validate_record(dict(rho=row['rho'], selection=row['selection'],
            inference=stage['inference'], coordinate_oracle=row['coordinate_oracle'], arms=stage['arms']), ic) and certificates
        assert stage['invariant_inner_pass']
        if row['immutable_inner_guard_obstruction']:
            assert not stage['arms']['intrinsic_guarded']['adopted']
        if stage['inference']['frame'].get('eligible_triples', 0):
            assert any(side['witness'] is not None for side in stage['coverage']['sides'].values())
    return certificates


def summarize(directory):
    c, ic, _ = config()
    execution, rows = load(directory)
    mode = execution['mode']
    expected = [(rho, seed) for i, rho in enumerate(c['densities']) for seed in
        (c['development_seeds'] if mode == 'development' else
         [c['test_seed_base']+100*i+j for j in range(c['test_replicates_per_density'])])]
    complete = execution['status'] == 'COMPLETE' and [(r['rho'], r['seed']) for r in rows] == expected
    complete = complete and all([s['duration'] for s in r['stages']] == c['outer_durations'] for r in rows)
    budget = execution['seconds'] <= c['wall_budget_seconds'] and execution['peak_mib'] <= c['memory_budget_mib']
    certificates = all([validate(r, ic) for r in rows])
    controls = execution['controls']['status'] == 'PASS' and all(
        (s['controls'] is None or s['controls']['status'] == 'PASS') and
        all(a['status'] != 'ok' or a['evaluation']['algebra_pass'] for a in s['arms'].values())
        for r in rows for s in r['stages'])
    cells = []
    for rho in c['densities']:
        group = [r for r in rows if r['rho'] == rho]
        for index, duration in enumerate(c['outer_durations']):
            stages = [r['stages'][index] for r in group]
            arms = {}
            for name in ic['methods']:
                available = [s for s in stages if s['arms'][name]['status'] == 'ok']
                ev = [s['arms'][name]['evaluation'] for s in available]
                baseline = [s['arms']['volume_shell']['evaluation'] for s in available]
                paired = {}
                for key in ['independent_field_rms', 'metric_error', 'affine_drift']:
                    a, b = rms([v[key] for v in baseline]), rms([v[key] for v in ev])
                    paired[key] = dict(baseline_rms=a, candidate_rms=b, ratio=b/a if a else None,
                        squared_reduction=stats([x[key]**2-y[key]**2 for x, y in zip(baseline, ev)]))
                adopted = sum(s['arms'][name]['adopted'] for s in stages)
                arms[name] = dict(available=len(available), adopted=adopted,
                    availability=len(available)/len(group) if group else 0,
                    adoption_fraction=adopted/len(group) if group else 0,
                    paired=paired, lorentz_signatures=sum(v['lorentz_signature'] for v in ev),
                    fallback_reasons=dict(Counter(reason for s in stages for reason in s['arms'][name]['fallback_reasons'])),
                    absolute_mass=stats([v['absolute_mass'] for v in ev]),
                    iid_noise_variance_factor=stats([v['iid_noise_variance_factor'] for v in ev]))
            frames = [s['inference']['frame'] for s in stages if s['inference']['frame']['status'] == 'ok']
            uncapped = sum(s['coverage']['status'] == 'ok' and any(q['witness'] is not None for q in s['coverage']['sides'].values()) for s in stages)
            cells.append(dict(rho=rho, duration=duration, clouds=len(group), arms=arms,
                uncapped_triple_clouds=uncapped,
                capped_triple_clouds=sum(s['inference']['frame'].get('eligible_triples', 0) > 0 for s in stages),
                frame_clouds=len(frames), frame_status=dict(Counter(s['inference']['frame']['status'] for s in stages)),
                immutable_inner_guard_obstructions=sum(r['immutable_inner_guard_obstruction'] for r in group),
                frames=dict(condition=stats([f['condition'] for f in frames]),
                    minimum_interval=stats([min(f['interval_counts']) for f in frames]),
                    worst_half_gram_error=stats([max(v['gram_error'] for v in f['guard']['halves']) for f in frames]),
                    worst_half_feature_error=stats([max(v['feature_error'] for v in f['guard']['halves']) for f in frames]),
                    guard_failures=dict(Counter(reason for f in frames for reason in f['guard']['reasons']))),
                physical_population=stats([s['physical_count'] for s in stages]),
                seconds=stats([s['seconds'] for s in stages])))
    primary = next(v for v in cells if v['rho'] == c['primary_density'] and v['duration'] == c['primary_duration'])['arms']['intrinsic_guarded']
    gates = dict(availability=primary['availability'] >= c['minimum_adoption'],
                 guarded_adoption=primary['adoption_fraction'] >= c['minimum_adoption'])
    for key in ['independent_field_rms', 'metric_error', 'affine_drift']:
        ratio = primary['paired'][key]['ratio']
        gates[key] = ratio is not None and ratio <= c['maximum_rms_ratio']
    passed = complete and budget and certificates and controls and all(gates.values())
    return dict(schema='x6.bk-outer-diamond-summary/1', mode=mode, clouds=len(rows),
        complete=complete, budget_pass=budget, certificates_pass=certificates, controls_pass=controls,
        cells=cells, primary_gates=gates,
        decision=('OUTER_DIAMOND_IMPROVEMENT' if passed else 'OUTER_DIAMOND_HOLD') if mode == 'test' else 'DEVELOPMENT_ONLY',
        phase3='HOLD_PHASE3', note='Paired fixed inner supports, unchanged count/guard requirements; no locality, convergence, 3+1 or curvature claim.')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('directory', type=Path)
    args = p.parse_args()
    summary = summarize(args.directory)
    (args.directory/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps({k: v for k, v in summary.items() if k != 'cells'}, indent=2))
