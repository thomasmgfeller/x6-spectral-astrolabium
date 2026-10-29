"""Fail-closed source, numerical, geometry and decision verification."""
import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from flint import arb, ctx
from support import HERE, check, sha, plan, freeze_check, gzread, unpack, load, write

runner = load('v09_runner_for_verifier', HERE / 'run.py')
audit = load('v09_audit_for_verifier', HERE / 'audit.py')


def compare(a, b):
    check(len(a['rows']) == len(b['rows']), 'same trial inventory')
    values = 0
    for r, s in zip(a['rows'], b['rows']):
        check(r['key'] == s['key'] and r['status'] == s['status'], 'same trial identity and availability')
        if r['status'] != 'COMPLETE':
            continue
        for key in ['N', 'active_before_last_window', 'history_nodes', 'coordinates_sha256',
                    'relations_sha256', 'counts_sha256', 'query_relations_sha256',
                    'query_counts_sha256', 'domain_mask_sha256', 'numeric_budget_pass']:
            check(r[key] == s[key], 'exact geometry/control replay ' + key)
        for u, v in zip(r['windows'], s['windows']):
            check(u['time'] == v['time'], 'same time windows')
            for key in ['partition_sha256', 'leaves', 'inside_cells', 'sphere_boundary_cells',
                        'outside_cells', 'integer_coordinate_exponent', 'all_point_box_and_sphere_decisions_exact']:
                check(u['geometry'][key] == v['geometry'][key], 'exact point/box and sphere geometry replay')
            check(u['field_budget_pass'] == v['field_budget_pass'], 'same integration budget decisions')
            for key in ['values', 'oracle_wave_values', 'continuum_wave_reference',
                        'query_weights', 'history_transfer_weights']:
                check(len(u[key]) == len(v[key]), 'complete transfer inventory')
                for x, y in zip(u[key], v[key]):
                    check(unpack(x).overlaps(unpack(y)), 'enclosed replay ' + key)
                    values += 1
    return values


def verify(source):
    p = plan()
    freeze_check()
    registration = json.loads((HERE / 'REGISTRATION.json').read_text())
    ctx.prec = 256
    docs = [gzread(source / f'BENCHMARK_{bits}.json.gz') for bits in p['precision_bits']]
    for bits, doc in zip(p['precision_bits'], docs):
        check(doc['new_random_clouds'] == 0 and doc['protocol_sha256'] == sha(HERE / 'PROTOCOL.json'), 'development provenance')
        check([r['key'] for r in doc['rows']] == p['clouds'], 'all predeclared archived slots')
        compute = json.loads((source / f'COMPUTE_{bits}.json').read_text())
        check(datetime.datetime.fromisoformat(compute['started_UTC']) >
              datetime.datetime.fromisoformat(registration['published_UTC'].replace('Z', '+00:00')),
              'detector production follows public development registration')
        check(compute['maximum_RSS_MiB'] < 4096 and compute['wall_seconds'] <= 21600, 'measured resource budget')
        for row in doc['rows']:
            if row['status'] != 'COMPLETE':
                continue
            for window in row['windows']:
                check(window['geometry']['all_point_box_and_sphere_decisions_exact'], 'exact detector geometry flag')
                check(window['geometry']['leaves'] <= p['detector']['partition_leaves_per_window'], 'frozen cubature cap')
                check(len(window['values']) == 5 and len(window['oracle_wave_values']) == 4, 'all fields retained')
                check(len(window['query_weights']) == row['active_before_last_window'], 'all query coefficients')
                check(len(window['history_transfer_weights']) == row['history_nodes'], 'all history coefficients')
                scales = [arb(1)] * 4 + [unpack(doc['normalization_A']).real / arb(1).exp()]
                for i, value in enumerate(window['values']):
                    z = unpack(value)
                    if window['field_budget_pass'][i]:
                        check(max(z.real.rad(), z.imag.rad()) / scales[i] <= arb(p['error_budgets']['detector_component_radius_over_field_scale_max']), 'reported integration success remains enclosed')
                check(window['quadrature_budget_pass'] == all(window['field_budget_pass']), 'derived window budget')
                for k in range(4):
                    total = unpack(window['values'][k]) - unpack(window['continuum_wave_reference'][k])
                    split = unpack(window['wave_history_component'][k]) + unpack(window['wave_operator_domain_component'][k])
                    check(total.overlaps(split), 'separate signed detector errors telescope')
            if row['numeric_budget_pass']:
                for e in row['numeric_controls']:
                    check(unpack(e['normalized_nodal_component_radius']).real <= arb(p['error_budgets']['nodal_Arb_component_radius_over_scale_max']), 'nodal numerical budget')
                    check(unpack(e['normalized_input_rounding_detector_upper']).real + unpack(e['normalized_float_nodal_solve_detector_upper']).real <= arb(p['error_budgets']['rounded_history_and_float_nodal_forward_effect_over_scale_max']), 'forward numerical budget')
        derived = runner.summarize(doc['rows'])
        saved = json.loads((source / f'DECISION_{bits}.json').read_text())
        for key in ['decision', 'planned_clouds', 'completed_clouds', 'window_field_budgets_passed',
                    'window_field_budgets_total', 'fresh_confirmation', 'predictive_operator_noise_kernel',
                    'compact_continuum_detector_reference', 'scientific_status']:
            check(derived[key] == saved[key], 'derived decision ' + key)
        for f, g in zip(derived['finite_sample_moments'], saved['finite_sample_moments']):
            for x, y in zip(f['finite_sample_mean'], g['finite_sample_mean']):
                check(unpack(x).overlaps(unpack(y)), 'enclosed sample means replay')
            for r, s in zip(f['finite_sample_covariance'], g['finite_sample_covariance']):
                for x, y in zip(r, s):
                    check(unpack(x).overlaps(unpack(y)), 'enclosed sample covariance replay')
    overlap_count = compare(*docs)
    baseline = gzread(source / 'BASELINE_128.json.gz')
    overlap_count += compare(docs[0], baseline)
    check(audit.compute()['status'] == 'PASS', 'independent analytic controls')
    decision = runner.summarize(docs[0]['rows'])
    return {'status': 'PASS', 'enclosure_overlaps': overlap_count,
            'archived_clouds': decision['completed_clouds'], 'new_random_clouds': 0,
            'detector_decision': decision['decision'],
            'window_field_budgets_passed': decision['window_field_budgets_passed'],
            'window_field_budgets_total': decision['window_field_budgets_total'],
            'scientific_status': p['scientific_status']}


def replay():
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='cspp-detector-replay-') as temp:
        root = Path(temp)
        for bits in [128, 192]:
            subprocess.run([sys.executable, '-B', str(HERE / 'run.py'), '--bits', str(bits), '--out', str(root)], check=True, env=env)
        baseline = root / 'baseline'
        benv = dict(env, NPY_DISABLE_CPU_FEATURES=plan()['cpu_modes'][1])
        subprocess.run([sys.executable, '-B', str(HERE / 'run.py'), '--bits', '128', '--out', str(baseline)], check=True, env=benv)
        (root / 'BASELINE_128.json.gz').write_bytes((baseline / 'BENCHMARK_128.json.gz').read_bytes())
        result = verify(root)
        for bits in [128, 192]:
            compare(gzread(root / f'BENCHMARK_{bits}.json.gz'), gzread(HERE / 'results' / f'BENCHMARK_{bits}.json.gz'))
        return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--preflight', action='store_true')
    parser.add_argument('--replay', action='store_true')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    if (HERE / 'SHA256SUMS').exists():
        for line in (HERE / 'SHA256SUMS').read_text().splitlines():
            expected, name = line.split('  ', 1)
            check(sha(HERE / name) == expected, 'package hash ' + name)
    if args.preflight:
        freeze_check()
        result = audit.compute()
    else:
        result = replay() if args.replay else verify(HERE / 'results')
    if args.out:
        write(args.out, result)
    print(json.dumps(result, indent=2))
