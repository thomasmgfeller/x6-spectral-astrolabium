"""Bounded archived-data feasibility study; no fresh random generator is used."""
import argparse
import datetime
import os
import resource
import time
from pathlib import Path

import numpy as np
from flint import arb, acb, ctx
from support import (HERE, check, digest, write, plan, pack, unpack, gzwrite,
                     freeze_check, geometry, initial_data as data, propagation as prop)
from detector import IntegerGeometry, integrate, wave_reference, sample_moments


def forward(x, counts, A):
    p = plan()
    nh = int(np.searchsorted(x[:, 0], -1, side='right'))
    check(nh > 0, 'nonempty unchanged history')
    hfloat = np.column_stack([data.float_wave_history(x[:nh], k, 1) for k in [0, 2, 4, 8]]
                            + [data.float_bump_history(x[:nh], 1, 1, float(A.mid()))])
    history = []
    for i, point in enumerate(x[:nh]):
        waves = [data.wave(point, k) for k in [0, 2, 4, 8]]
        exact = [data.extension(point, row[1:], 1) for row in waves]
        exact += [data.extension(point, data.bump_jets(point, 1, A), 1)]
        history.append(exact + [acb(complex(z)) for z in hfloat[i]] + [w[0] for w in waves])
    empty = np.empty((0, len(x)), dtype=np.int32)
    _, values, _, edges, _ = prop.solve(counts, empty, p['nu'], p['epsilon'], 1, history, nh)
    table = prop.coefficient_table(len(x), p['nu'], p['epsilon'], 1)
    numeric = np.empty((len(x), 5), dtype=complex)
    numeric[:nh] = hfloat
    for i in range(nh, len(x)):
        js = np.array([j for j, w in edges[i]], dtype=int)
        ws = np.array([float(w.mid()) for j, w in edges[i]])
        numeric[i] = ws @ numeric[js] if len(js) else 0
    check(np.isfinite(numeric).all(), 'finite float nodal control')
    maximum_weight = max(w.abs_upper() for w in table)
    scales = [arb(1)] * 4 + [A / arb(1).exp()]
    errors = []
    for f in range(5):
        input_error = maximum_weight * sum((v[f + 5] - v[f]).abs_upper() for v in values)
        solve_error = maximum_weight * sum((acb(complex(z[f])) - v[f + 5]).abs_upper()
                                          for z, v in zip(numeric, values))
        node_radius = max(max(v[f].real.rad(), v[f].imag.rad()) for v in values)
        errors.append({'field': p['fields'][f],
                       'normalized_input_rounding_detector_upper': pack(input_error / scales[f]),
                       'normalized_float_nodal_solve_detector_upper': pack(solve_error / scales[f]),
                       'normalized_nodal_component_radius': pack(node_radius / scales[f]),
                       'scope': 'uniform forward bound through exact query coefficients; not an independently rounded floating-point cubature'})
    return values, history, edges, table, scales, errors


def adjoint(q, edges, nh):
    weights = list(q)
    for i in range(len(weights) - 1, nh - 1, -1):
        for j, w in edges[i]:
            weights[j] += weights[i] * w
    return weights[:nh]


def evaluate(q, values, history, edges):
    t = adjoint(q, edges, len(history))
    columns = list(range(5)) + list(range(10, 14))
    output = []
    for f in columns:
        forward_value = sum(w * v[f] for w, v in zip(q, values))
        adjoint_value = sum(w * h[f] for w, h in zip(t, history))
        check(forward_value.overlaps(adjoint_value), 'independent forward/adjoint enclosure overlap')
        output.append(acb(forward_value.real.intersection(adjoint_value.real),
                          forward_value.imag.intersection(adjoint_value.imag)))
    return output, t


def summarize(rows):
    p = plan()
    complete = [r for r in rows if r['status'] == 'COMPLETE']
    fields = []
    if len(complete) == len(p['clouds']):
        for f, name in enumerate(p['fields']):
            samples = [[unpack(w['values'][f]) for w in r['windows']] for r in complete]
            means, covariance = sample_moments(samples)
            fields.append({'field': name, 'finite_sample_mean': [pack(v) for v in means],
                           'finite_sample_covariance': [[pack(v) for v in row] for row in covariance],
                           'population_inference': 'NONE'})
    flags = [w['quadrature_budget_pass'] for r in complete for w in r['windows']]
    numeric = all(r['numeric_budget_pass'] for r in complete)
    status = ('RESOURCE_HOLD' if len(complete) != len(p['clouds']) else
              'NUMERIC_HOLD' if not numeric else
              'QUADRATURE_HOLD' if not all(flags) else 'DETECTOR_INTEGRATION_READY_ONLY')
    return {'decision': status, 'planned_clouds': len(p['clouds']), 'completed_clouds': len(complete),
            'window_field_budgets_passed': sum(sum(w['field_budget_pass']) for r in complete for w in r['windows']),
            'window_field_budgets_total': len(p['clouds']) * 2 * 5,
            'finite_sample_moments': fields, 'fresh_confirmation': 'NOT_RUN',
            'predictive_operator_noise_kernel': 'NOT_QUALIFIED',
            'compact_continuum_detector_reference': 'NOT_QUALIFIED',
            'scientific_status': p['scientific_status']}


def compute(bits, out):
    p = plan()
    freeze_check()
    ctx.prec = bits
    start = time.monotonic()
    stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    archive = np.load(HERE.parent / 'scalar_pilot_v0_1/results/clouds.npz')
    A = data.source.normalization(bits)[0]
    rows = []
    for key in p['clouds']:
        if time.monotonic() - start > p['resources']['wall_seconds_per_process']:
            rows.append({'key': key, 'status': 'RESOURCE_HOLD'})
            continue
        original = archive[key]
        if len(original) > p['resources']['max_points_per_cloud']:
            rows.append({'key': key, 'status': 'RESOURCE_HOLD'})
            continue
        probes = np.array([[.875, 0., 0., 1.5], [1.125, 0., 0., 1.5]])
        cc, pc, relations, query_relations, stats = geometry.inventory(original, probes)
        membership, region_stats = geometry.region(original, 4)
        check(np.all(membership), 'exact Omega4 membership')
        n = int(np.searchsorted(original[:, 0], 1.25, side='left'))
        x, c = original[:n], cc[:n, :n]
        values, history, edges, table, scales, errors = forward(x, c, A)
        geo = IntegerGeometry(x, c)
        # Check all midpoint query relations and interval counts independently.
        for i, point in enumerate(probes):
            past = geo.point_past(point)
            for j in range(n):
                count = (geo.successors[j] & past).bit_count() if past & (1 << j) else -1
                check(count == int(pc[i, j]), 'integer point/interval graph equals predecessor CPU kernel')
        windows = []
        for time_window in p['detector']['time_windows']:
            q, audit = integrate(geo, table, time_window, p['detector']['partition_leaves_per_window'])
            field, transfer = evaluate(q, values, history, edges)
            passes = [bool(max(z.real.rad(), z.imag.rad()) / s <= arb(p['error_budgets']['detector_component_radius_over_field_scale_max']))
                      for z, s in zip(field[:5], scales)]
            references = [wave_reference(k, time_window) for k in [0, 2, 4, 8]]
            check(all(max(z.real.rad(), z.imag.rad()) <= arb(p['error_budgets']['continuum_wave_reference_component_radius_max'])
                      for z in references), 'analytic wave detector references')
            windows.append({'time': time_window, 'values': [pack(z) for z in field[:5]],
                            'oracle_wave_values': [pack(z) for z in field[5:]],
                            'continuum_wave_reference': [pack(z) for z in references],
                            'wave_history_component': [pack(field[k] - field[5 + k]) for k in range(4)],
                            'wave_operator_domain_component': [pack(field[5 + k] - references[k]) for k in range(4)],
                            'normalized_component_radii_upper': [float((max(z.real.rad(), z.imag.rad()) / s).upper()) for z, s in zip(field[:5], scales)],
                            'field_budget_pass': passes, 'quadrature_budget_pass': all(passes),
                            'query_weights': [pack(z) for z in q],
                            'history_transfer_weights': [pack(z) for z in transfer],
                            'history_linf_gain_upper': pack(sum(z.abs_upper() for z in transfer)),
                            'geometry': audit})
        numeric_pass = all(unpack(e['normalized_nodal_component_radius']).real <= arb(p['error_budgets']['nodal_Arb_component_radius_over_scale_max'])
                           and unpack(e['normalized_input_rounding_detector_upper']).real + unpack(e['normalized_float_nodal_solve_detector_upper']).real <= arb(p['error_budgets']['rounded_history_and_float_nodal_forward_effect_over_scale_max'])
                           for e in errors)
        row = {'key': key, 'status': 'COMPLETE', 'N': len(original), 'active_before_last_window': n,
               'history_nodes': len(history), 'coordinates_sha256': digest(original),
               'relations_sha256': digest(relations), 'counts_sha256': digest(cc),
               'query_relations_sha256': digest(query_relations), 'query_counts_sha256': digest(pc),
               'domain_mask_sha256': digest(membership), 'geometry_stats': stats,
               'numeric_budget_pass': bool(numeric_pass), 'numeric_controls': errors, 'windows': windows}
        rows.append(row)
        print('detector', bits, key, 'quadrature', [w['field_budget_pass'] for w in windows], flush=True)
        gzwrite(out / f'BENCHMARK_{bits}.json.gz', {'precision_bits': bits, 'rows': rows})
    result = {'schema': p['schema'], 'precision_bits': bits, 'new_random_clouds': 0,
              'normalization_A': pack(A), 'protocol_sha256': __import__('support').sha(HERE / 'PROTOCOL.json'), 'rows': rows}
    gzwrite(out / f'BENCHMARK_{bits}.json.gz', result)
    decision = summarize(rows)
    write(out / f'DECISION_{bits}.json', decision)
    write(out / f'COMPUTE_{bits}.json', {'started_UTC': stamp, 'wall_seconds': time.monotonic() - start,
          'maximum_RSS_MiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024,
          'cpu_features_disabled': os.getenv('NPY_DISABLE_CPU_FEATURES', 'default'),
          'numpy': np.__version__, 'new_random_clouds': 0})
    return decision


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bits', type=int, choices=[128, 192], required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    resource.setrlimit(resource.RLIMIT_AS, (4 * 1024 ** 3, 4 * 1024 ** 3))
    print(compute(args.bits, args.out)['decision'])
