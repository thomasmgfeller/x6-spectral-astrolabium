#!/usr/bin/env python3
"""Selected auxiliary-basis control at z=1; no physical boundary reduction."""
from pathlib import Path
from fractions import Fraction
import argparse
import hashlib
import io
import json
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parent
BASIS = [f'{g}|{s}|{m}m' for s in ('0', '+') for g in ('A', 'K') for m in (0, 1)]
MODES = ('transport', 'assign_coefficients', 'assign_covariant')
GATES = {k: 'HOLD' for k in ('MODEL', 'CURRENT', 'CORRESPONDENCE', 'BOUNCE',
                           'REGULARITY', 'BOUNDARY', 'TRAPPING', 'EXTENSION')}
TOL = 1e-12  # numerical guard only, not a physical acceptance tolerance


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def json_bytes(value):
    return (json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n').encode()


def npz_bytes(arrays):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, value in sorted(arrays.items()):
            data = io.BytesIO()
            np.save(data, np.asarray(value), allow_pickle=False)
            info = zipfile.ZipInfo(name + '.npy', (2026, 11, 11, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data.getvalue())
    return stream.getvalue()


def matrix(value):
    a = np.asarray(value, dtype=np.complex128)
    require(a.ndim == 2 and np.isfinite(a).all(), 'matrix must be finite and two dimensional')
    return a


def roots(gram):
    """Reject non-Hermitian/ill-conditioned input BEFORE roundoff symmetrization."""
    g = matrix(gram)
    require(g.shape[0] == g.shape[1] and len(g) > 0, 'Gram must be nonempty and square')
    scale = max(1.0, float(np.linalg.norm(g, 2)))
    defect = float(np.linalg.norm(g - g.conj().T, 2))
    require(defect <= TOL * scale, 'Gram is not Hermitian within numerical tolerance')
    # Only the already accepted <=TOL roundoff component is removed; never clip eigenvalues.
    w, v = np.linalg.eigh((g + g.conj().T) / 2)
    require(w.min() > TOL * max(1.0, float(w.max())), 'Gram is not safely positive definite')
    return ((v * np.sqrt(w)) @ v.conj().T,
            (v / np.sqrt(w)) @ v.conj().T,
            {'hermiticity_defect_2': defect, 'minimum_eigenvalue': float(w.min()),
             'maximum_eigenvalue': float(w.max()), 'condition_number': float(w.max()/w.min())})


def normalize_coefficients(a, gin, gout):
    si, ii, _ = roots(gin)
    so, io_, _ = roots(gout)
    a = matrix(a)
    require(a.shape == (len(so), len(si)), 'coefficient map dimensions disagree')
    return so @ a @ ii


def normalize_covariant(b, gin, gout):
    si, ii, _ = roots(gin)
    so, io_, _ = roots(gout)
    b = matrix(b)
    require(b.shape == (len(so), len(si)), 'covariant kernel dimensions disagree')
    return io_ @ b @ ii


def selection(source):
    require(source['role'] == 'auxiliary_history_space_not_physical_boundary_space', 'wrong orbit source role')
    cases = [c for c in source['cases'] if c['m'] == 2]
    require(len(cases) == 1, 'need exactly one m=2 case')
    c = cases[0]
    orbits = c['orbits']
    require(c['N'] == 4 and len(orbits) == 7, 'wrong auxiliary orbit count')
    weights = [Fraction(o['indicator_norm_squared']) for o in orbits]
    for o, w in zip(orbits, weights):
        require(w == Fraction(1, 4*o['stabilizer']), 'orbit/aut weight mismatch')
        require(w == Fraction(c['point_weight'])*len(o['indices']), 'orbit/point weight mismatch')
        require(len(o['indices']) == o['orbit_size'], 'orbit size mismatch')
    gram7 = [[Fraction(x) for x in row] for row in c['Gram_orbit_indicators']]
    require(gram7 == [[weights[i] if i == j else Fraction(0) for j in range(7)]
                     for i in range(7)], 'source Gram mismatch')
    representatives = [(2190, 0), (2254, 0), (2190, 3), (2254, 3)]
    chosen = []
    for rep in representatives:
        matches = [i for i, o in enumerate(orbits) if tuple(o['representative']) == rep]
        require(len(matches) == 1, 'missing or duplicate selected orbit')
        chosen.append(matches[0])
    require([orbits[i]['positive_marks'] for i in chosen] == [0, 0, 2, 2], 'selected strata mismatch')
    e = np.kron(np.eye(7)[:, chosen], np.eye(2))
    parent = np.kron(np.diag([float(w) for w in weights]), np.eye(2))
    g = e.T @ parent @ e
    _, inv, _ = roots(g)
    j = e @ inv
    report = {'source_m': 2, 'source_N': 4, 'parent_orbits': 7,
              'selected_source_orbit_indices': chosen,
              'excluded_source_orbit_indices': [i for i in range(7) if i not in chosen],
              'selected_representatives': representatives,
              'parent_gram7_diagonal_exact': list(map(str, weights)),
              'selected_gram8_diagonal_exact': [str(weights[i]) for i in chosen for _ in range(2)],
              'basis': BASIS, 'external_test_factor_dimension': 2,
              'external_test_factor_is_derived_matter_space': False,
              'dynamical_closure_of_selection': 'NOT_ESTABLISHED'}
    return g, parent, e, j, report


def canonical_input(arrays, meta):
    require(meta['dataset_role'] == 'GEOMETRY_SPECTATOR_CONTROL', 'wrong source role')
    require(str(arrays['role']) == meta['dataset_role'], 'NPZ/JSON role mismatch')
    require(meta['diagnostic_operator_convention'] == 'coefficient_map' and
            str(arrays['diagnostic_operator_convention']) == 'coefficient_map', 'source is not a coefficient map')
    require(meta['physical_kernel'] is False and meta['physical_gram'] is None and
            meta['physical_clock'] is None and meta['delta_chi'] is None, 'unexpected physical claim')
    require(meta['physical_gates'] == GATES, 'unexpected physical gate status')
    require(meta['n_channels'] == int(arrays['n_channels']) == 2 and
            meta['states_per_channel'] == int(arrays['states_per_channel']) == 4,
            'source dimensions disagree')
    basis = list(map(str, arrays['basis']))
    require(basis == meta['basis'] and len(basis) == 8 and set(basis) == set(BASIS), 'invalid/duplicate basis')
    require(meta['basis_layout'] == str(arrays['basis_layout']), 'basis layout metadata disagree')
    if meta['basis_layout'] == 'stratum_geometry_matter':
        require(basis == BASIS, 'canonical layout has wrong order')
    else:
        require(meta['basis_layout'] == 'explicit_permutation', 'unsupported basis layout')
    p = [basis.index(label) for label in BASIS]
    k = matrix(arrays['K'])
    require(k.shape == (8, 8), 'K must be 8x8')
    for name in ('G_in_diagnostic', 'G_out_diagnostic'):
        g = matrix(arrays[name])
        require(g.shape == (8, 8) and np.array_equal(g[np.ix_(p, p)], np.eye(8)), 'source Gram must be I8')
    for name, slot, values in [('stratum_index', 1, ['0', '+']),
                               ('geometry_index', 0, ['A', 'K']),
                               ('matter_index', 2, ['0m', '1m'])]:
        require(np.array_equal(arrays[name], [values.index(b.split('|')[slot]) for b in basis]),
                'index labels inconsistent with basis')
    require(complex(arrays['z']) == 1 and meta['phase_exact'] == '1' and
            meta['z'] == {'real': 1.0, 'imag': 0.0}, 'this benchmark requires z=1')
    k = k[np.ix_(p, p)]
    kg = np.array([[35, 26], [26, 20]])
    require(np.array_equal(k, np.kron(np.eye(2), np.kron(kg, np.eye(2)))), 'z=1 source control failed')
    return k


def read_input(npz_path, json_path):
    meta = json.loads(Path(json_path).read_text())
    require(sha(npz_path) == meta['npz_sha256'], 'NPZ hash mismatch')
    with np.load(npz_path, allow_pickle=False) as archive:
        arrays = {k: archive[k] for k in archive.files}
    return canonical_input(arrays, meta)


def mixing(a, basis=BASIS):
    parts = [b.split('|') for b in basis]
    s = np.array([b[1] for b in parts])
    m = np.array([b[2] for b in parts])
    smask, mmask = s[:, None] != s[None, :], m[:, None] != m[None, :]
    return {'stratum_mixing_fro': float(np.linalg.norm(a[smask])),
            'test_label_mixing_fro': float(np.linalg.norm(a[mmask])),
            'either_label_mixing_fro': float(np.linalg.norm(a[smask | mmask]))}


def calculate(source, a0, mode):
    require(mode in MODES, 'unknown assignment mode')
    g, parent, e, j, sel = selection(source)
    s, inv, gd = roots(g)
    if mode == 'transport':
        a = inv @ a0 @ s
        b = g @ a
    elif mode == 'assign_coefficients':
        a = a0.copy()
        b = g @ a
    else:
        b = a0.copy()
        a = np.linalg.solve(g, b)
    u = normalize_coefficients(a, g, g)
    v = normalize_covariant(b, g, g)
    residuals = {
        'pullback_gram_fro': float(np.linalg.norm(e.T @ parent @ e - g)),
        'normalized_embedding_fro': float(np.linalg.norm(j.conj().T @ parent @ j - np.eye(8))),
        'covariant_relation_relative_fro': float(np.linalg.norm(b - g @ a)/max(1, np.linalg.norm(b))),
        'convention_agreement_relative_fro': float(np.linalg.norm(u-v)/max(1, np.linalg.norm(u)))}
    if mode == 'transport':
        residuals['source_transport_relative_fro'] = float(np.linalg.norm(u-a0)/max(1, np.linalg.norm(a0)))
    require(all(x <= TOL for x in residuals.values()), 'normalization identity failed')
    mix = mixing(u)
    require(all(x == 0 for x in mix.values()), 'unexpected mixing in control')
    defect = u.conj().T @ u - np.eye(8)
    diagnostics = {**mix, 'unitarity_defect_2': float(np.linalg.norm(defect, 2)),
                   'unitarity_defect_fro': float(np.linalg.norm(defect)),
                   'singular_values': np.linalg.svd(u, compute_uv=False).tolist()}
    require(diagnostics['unitarity_defect_2'] > 1, 'expected non-isometric control missing')
    arrays = {'A_source_orthonormal': a0, 'A_indicator': a, 'B_indicator': b,
              'normalized_from_coefficients': u, 'normalized_from_covariant': v,
              'G_selected_aux': g, 'G_parent_aux': parent,
              'embedding_indicators': e, 'embedding_orthonormal': j,
              'defect_diagnostic_I8': defect, 'basis': BASIS, 'mode': mode,
              'role': 'SELECTED_AUXILIARY_NORM_CONTROL', 'z': 1+0j}
    report = {'version': '0.1', 'dataset_role': 'SELECTED_AUXILIARY_NORM_CONTROL',
              'mode': mode, 'basis': BASIS, 'selection': sel, 'gram_diagnostics': gd,
              'identities': residuals, 'diagnostics': diagnostics,
              'algebra_checks': 'PASS', 'isometry_of_declared_test_map': 'FAIL',
              'physical_kernel': False, 'physical_gram': 'NOT_DERIVED',
              'physical_8x8_matter_matrix': 'NOT_CONSTRUCTED', 'physical_K_0plus': 'NOT_COMPUTED',
              'physical_clock': None, 'delta_chi': None, 'physical_gates': GATES,
              'basis_transport_only': mode == 'transport',
              'additional_assignment': 'chosen identification of normalized orbit indicators with formal source basis',
              'numerical_policy': {'dtype': 'complex128', 'identity_tolerance': TOL,
                 'gram_hermiticity_relative_tolerance': TOL,
                 'gram_eigenvalue_floor': '1e-12 * max(1, largest_eigenvalue)',
                 'physical_tolerance': None}}
    return arrays, report


def generate(mode='transport', outdir=ROOT/'data', npz_path=ROOT/'inputs/geometry_z1.npz',
             json_path=ROOT/'inputs/geometry_z1.json', orbit_path=ROOT/'inputs/label_quotient.json'):
    a0 = read_input(npz_path, json_path)
    arrays, report = calculate(json.loads(Path(orbit_path).read_text()), a0, mode)
    content = npz_bytes(arrays)
    report['npz_sha256'] = hashlib.sha256(content).hexdigest()
    report['producer_sha256'] = sha(__file__)
    report['source_sha256'] = {'geometry_npz': sha(npz_path), 'geometry_json': sha(json_path),
                               'label_quotient_json': sha(orbit_path)}
    serialized = json_bytes(report)  # validate everything before creating output files
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    stem = f'cst_dust_auxnorm_{mode}_z1'
    (outdir/(stem+'.npz')).write_bytes(content)
    (outdir/(stem+'.json')).write_bytes(serialized)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=MODES, default='transport')
    parser.add_argument('--outdir', type=Path, default=ROOT/'data')
    parser.add_argument('--input', type=Path, default=ROOT/'inputs/geometry_z1.npz')
    parser.add_argument('--metadata', type=Path, default=ROOT/'inputs/geometry_z1.json')
    parser.add_argument('--orbits', type=Path, default=ROOT/'inputs/label_quotient.json')
    args = parser.parse_args()
    try:
        r = generate(args.mode, args.outdir, args.input, args.metadata, args.orbits)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(2, f'REJECTED: {error}\n')
    print(f"{args.mode}: algebra PASS; declared test-map isometry FAIL; physical gates HOLD")
    print(f"diagnostic spectral defect = {r['diagnostics']['unitarity_defect_2']:.12g}")


if __name__ == '__main__':
    main()
