#!/usr/bin/env python3
"""Rebuild the finite controls and exact metadata; no external data or compute jobs."""
from pathlib import Path
from fractions import Fraction as F
import argparse
import json
import normalize_cst_dust_8x8 as n


def build(out):
    out = Path(out)
    for mode in n.MODES:
        n.generate(mode, out/'data')
    source = json.loads((n.ROOT/'inputs/label_quotient.json').read_text())
    selection = n.selection(source)[4]
    # Exact arithmetic for matrices [[a, b sqrt(2)], [c sqrt(2), d]].
    blocks = {'transport': (35, 26, 26, 20, 1),
              'assign_coefficients': (35, 13, 26, 20, 2),
              'assign_covariant': (280, 104, 104, 80, 2)}
    controls = {}
    for mode, (a, b, c, d, radicand) in blocks.items():
        a, b, c, d, radicand = map(F, (a, b, c, d, radicand))
        trace = a*a + d*d + (b*b+c*c)*radicand
        det = (a*d-b*c*radicand)**2
        controls[mode] = {'block_form': '[[a,b*sqrt(r)],[c*sqrt(r),d]]',
                          'a_b_c_d_r_exact': list(map(str, (a, b, c, d, radicand))),
                          'trace_UstarU_exact': str(trace), 'det_UstarU_exact': str(det),
                          'squared_singular_polynomial': f'x^2 - {trace}*x + {det}',
                          'each_singular_value_multiplicity': 4,
                          'defect_8x8_fro_squared_exact': str(4*(trace*trace-2*det-2*trace+2)),
                          'scalar_normalization_can_make_isometric': trace*trace == 4*det}
    cert = {'arithmetic': 'fractions.Fraction', 'z_exact': '1', 'controls': controls,
            'diagonal_product_obstruction': {
               'coefficient_assignment_offdiagonal': '910*u + 520*v',
               'covariant_assignment_offdiagonal': '910/u + 520/v',
               'assumptions': 'u>0,v>0; Gin diagonal; Gout=diag(u,v); aligned selected indicator basis; z=1',
               'claim': 'No positive diagonal input/output products yield isometry for these assignments.',
               'excluded_claims': ['arbitrary nondiagonal metrics', 'other phases', 'full CST no-go']}}
    (out/'results').mkdir(parents=True, exist_ok=True)
    (out/'results/selection.json').write_bytes(n.json_bytes(selection))
    (out/'results/exact_certificates.json').write_bytes(n.json_bytes(cert))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--outdir', type=Path, default=n.ROOT)
    build(parser.parse_args().outdir)
    print('Rebuilt three declared assignments, selection and exact certificates.')
