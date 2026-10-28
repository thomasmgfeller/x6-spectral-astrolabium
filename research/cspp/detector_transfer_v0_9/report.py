"""Post-run descriptive report; no change to the frozen decisions or sample.

The compact-source support count was added after inspecting v0.9 outputs.
It diagnoses exactly-zero H1 histories; it is not an independent hypothesis test.
"""
import argparse
from fractions import Fraction
from pathlib import Path

import numpy as np
from flint import arb, ctx
from support import HERE, plan, gzread, unpack, check, write, digest


def compute():
    ctx.prec = 256
    p = plan()
    doc = gzread(HERE / 'results/BENCHMARK_128.json.gz')
    archive = np.load(HERE.parent / 'scalar_pilot_v0_1/results/clouds.npz')
    source_support = []
    wave_radii = []
    compact_nonzero_radii = []
    input_errors, solve_errors, node_radii = [], [], []
    zero_passes = 0
    for row in doc['rows']:
        if row['status'] != 'COMPLETE':
            continue
        x = archive[row['key']]
        check(digest(x) == row['coordinates_sha256'], 'same archived diagnostic cloud')
        hits = [i for i, point in enumerate(x) if point[0] <= -1 and
                sum(Fraction(float(v)) ** 2 for v in point[1:]) < Fraction(1, 4)]
        source_support.append({'key': row['key'], 'nonzero_compact_H1_history_nodes': len(hits)})
        for window in row['windows']:
            wave_radii += window['normalized_component_radii_upper'][:4]
            compact = unpack(window['values'][4])
            if not hits:
                check(compact.is_zero(), 'zero source history gives exactly zero compact signal')
                zero_passes += int(window['field_budget_pass'][4])
            else:
                compact_nonzero_radii.append(window['normalized_component_radii_upper'][4])
        for error in row['numeric_controls']:
            input_errors.append(float(unpack(error['normalized_input_rounding_detector_upper']).real.upper()))
            solve_errors.append(float(unpack(error['normalized_float_nodal_solve_detector_upper']).real.upper()))
            node_radii.append(float(unpack(error['normalized_nodal_component_radius']).real.upper()))
    return {'schema': 'cspp.detector-transfer.descriptive-report/0.9',
            'analysis_timing': 'post-run description of frozen archived development outputs; not preregistered inference',
            'compact_source_support': source_support,
            'empty_compact_history_clouds': sum(row['nonzero_compact_H1_history_nodes'] == 0 for row in source_support),
            'quadrature_passes_from_exactly_zero_source_histories': zero_passes,
            'normalized_wave_component_radius_display_range': [min(wave_radii), max(wave_radii)],
            'normalized_compact_nonzero_component_radius_display_range': [min(compact_nonzero_radii), max(compact_nonzero_radii)],
            'maximum_normalized_input_rounding_display': max(input_errors),
            'maximum_normalized_float_nodal_forward_effect_display': max(solve_errors),
            'maximum_normalized_nodal_Arb_radius_display': max(node_radii),
            'interpretation': 'all six tight values arise from zero compact H1 histories; not successful physical source propagation; wide remaining intervals measure quadrature uncertainty, not physical noise amplitude'}


if __name__ == '__main__':
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = compute()
    if args.out:
        write(args.out, result)
    print(json.dumps(result, indent=2))
