"""Exact additional linear coordinates for the inherited centred N14 scalar output."""
import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys

import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT / "prior"
sys.path.insert(0, str(PRIOR))
from cuts import action
import exchange as ex


def scalar_precision(mask, audit):
    """Stationary elimination of (input, interior, collar) with seed precision I."""
    assert audit["status"] == "ADMISSIBLE" and audit["symplectic_both_directions"]
    g, _, _ = action(mask)
    output = [3, 4, 5]
    internal = [0, 1, 2] + list(range(6, g.rows))
    size = len(internal)
    seed = sp.diag(1, 1, 1, *([0] * (size-3)))
    q = (g[internal, internal] + sp.I * seed).to_DM().convert_to(sp.QQ_I)
    cross = g[internal, output].to_DM().convert_to(sp.QQ_I)
    pivot = list(q.rref()[1])
    # Free collar directions, if any, neither fix an output nor alter its exponent.
    assert size - len(pivot) == audit["free_directions"]
    selected = cross.extract(pivot, [0, 1, 2])
    z, den = q.extract(pivot, pivot).solve_den(selected)
    assert q.extract(list(range(size)), pivot) * z == cross.scalarmul(den)
    yy = g[output, output].to_DM().convert_to(sp.QQ_I)
    eff = yy - (selected.transpose() * z).scalarmul(1/den)
    omega = eff.scalarmul(sp.QQ_I(0, -1)).to_Matrix()
    assert omega == omega.T
    real = omega.applyfunc(sp.re)
    assert all(real[:i, :i].det() > 0 for i in (1, 2, 3))
    return omega


def archived_clocks():
    """Use common stored grids; a dyadic argument tests nonvanishing of stored values."""
    packets = {}
    for file in ("clock14.json", "clock14_extra.json"):
        clock = ex.read_json(PRIOR / "v05" / file)
        for mask in clock["selection"]:
            grids = clock["branches"][f"N14_{mask}"]["grids"]
            packets[mask] = {tuple(g["grid"]):g["amplitudes"]["lobes"] for g in grids}
    central = ex.read_json(PRIOR / "response.json")
    for j, mask in enumerate(central["order"]):
        assert mask not in packets
        packets[mask] = {tuple(g["grid"]):g["packets"][j]["lobes"] for g in central["production_grids"]}
    grids = sorted(set.intersection(*(set(d) for d in packets.values())))
    assert grids == [(32, 6), (48, 8)] and len(packets) == 12
    summary = {}
    for grid in grids:
        squares = []
        for mask, readings in sorted(packets.items()):
            densities = readings[grid]
            assert len(densities) == 2
            for j, (left, right) in enumerate(densities):
                re, im = (Fraction(a) + Fraction(b) for a, b in zip(left, right))
                square = (re*re + im*im) / 2
                assert square > 0
                squares.append((square, mask, central["densities"][j]))
        minimum, mask, rho = min(squares)
        summary["x".join(map(str, grid))] = {
            "density_values":central["densities"], "tested_amplitudes":len(squares),
            "minimum_stored_squared_modulus":str(minimum),
            "minimum_modulus_approx":float(minimum)**0.5, "minimum_at":[mask, rho]}
    return set(packets), summary


def matrices(orbits, target, columns, labels):
    types = sorted({labels[o] for o in orbits})
    # Common denominator six from the S3 average. Scaling C preserves its kernel.
    c = [[6*columns[o].get(p, 0) for o in orbits] for p in sorted(target)]
    assert all(x == int(x) for row in c for x in row)
    b = [[int(labels[o] == m) for o in orbits] for m in types]
    return (DomainMatrix.from_list([[int(x) for x in row] for row in c], sp.ZZ).to_sparse(),
            DomainMatrix.from_list(b, sp.ZZ).to_sparse(), types)


def dimensions(c, b, types, known):
    nc = c.shape[0]
    used = [j for j, m in enumerate(types) if m in known]
    remaining = [j for j, m in enumerate(types) if m not in known]
    order = used + remaining
    allcols = list(range(c.shape[1]))
    reindexed = b.extract(order, allcols)
    piv = c.vstack(reindexed).transpose().rref()[1]
    selected = [types[order[j-nc]] for j in piv if j >= nc]
    crank = sum(j < nc for j in piv)
    knownrank = sum(m in known for m in selected)
    return {"orbits":c.shape[1], "end_types":len(types), "rank_C":crank,
            "rank_C_and_known_endpoints":crank+knownrank,
            "rank_C_and_all_endpoints":len(piv), "additional_known_coordinates":knownrank,
            "additional_all_coordinates":len(selected), "additional_endpoint_basis":selected}


def positive_witnesses(target, columns, sizes, certificate, orbits, types, c, b, known):
    """Three exact tangent vectors with visible endpoint changes equal to the unit vectors."""
    included = [j for j, t in enumerate(types) if t in known]
    k = len(included)
    allcols = list(range(len(orbits)))
    independent = list(c.transpose().rref()[1])
    visible = b.extract(included, allcols)
    system = c.extract(independent, allcols).vstack(visible)
    support = list(system.rref()[1])
    rows = list(range(system.shape[0]))
    assert len(support) == len(rows)
    rhs = DomainMatrix.zeros((len(independent), k), sp.ZZ).vstack(DomainMatrix.eye(k, sp.ZZ))
    num, den = system.extract(rows, support).solve_den(rhs)
    assert visible.extract(list(range(k)), support) * num == DomainMatrix.eye(k, sp.ZZ).scalarmul(den)
    assert (c.extract(list(range(c.shape[0])), support) * num).is_zero_matrix
    entries = num.to_list()
    vectors = [{orbits[i]:Fraction(int(entries[l][j]), int(den))
                for l, i in enumerate(support) if entries[l][j]} for j in range(k)]
    uniform, cap, _ = ex.residual_target(target, columns, sizes)
    residual = certificate["residual_orbit_masses"]
    base = {o:cap*u+(1-cap)*Fraction(residual.get(str(o), 0)) for o,u in uniform.items()}
    assert min(base.values()) > 0 and ex.marginal(columns, base) == Counter(target)
    total_abs = {o:sum(abs(v.get(o, 0)) for v in vectors) for o in orbits}
    radius = min(base[o]/(2*t) for o,t in total_abs.items() if t)
    assert all(base[o]-radius*total_abs[o] > 0 for o in orbits)
    return {"real_cube_radius":str(radius),
            "directions_by_visible_endpoint":{
                str(types[idx]):{str(o):str(a) for o,a in v.items()}
                for idx, v in zip(included, vectors)}}


def joint_preparation(parts, known, results):
    """Independent conditional lifts, inherited root amplitudes 1/2, common endpoint space."""
    names = sorted(parts)
    (c1, labels1), (c2, labels2) = (parts[n] for n in names)
    c = c1.hstack(DomainMatrix.zeros((c1.shape[0], c2.shape[1]), sp.ZZ)).vstack(
        DomainMatrix.zeros((c2.shape[0], c1.shape[1]), sp.ZZ).hstack(c2))
    # 2 B has a single 1 per column; equal end masks from both roots share a row.
    labels = labels1 + labels2
    types = sorted(set(labels))
    b = DomainMatrix.from_list([[int(m == e) for e in labels] for m in types], sp.ZZ).to_sparse()
    full = dimensions(c, b, types, known)
    indices = [i for i, e in enumerate(labels) if e in known]
    visible = [j for j, m in enumerate(types) if m in known]
    limited = dimensions(c.extract(list(range(c.shape[0])), indices), b.extract(visible, indices),
                         [types[j] for j in visible], known)
    assert set(labels1).intersection(labels2).isdisjoint(known)
    assert full["additional_known_coordinates"] == sum(
        results[n]["all_orbits"]["additional_known_coordinates"] for n in names)
    # Each root witness produces a half-unit output change, so coefficients in
    # the common endpoint basis may vary in a real cube of half the root radius.
    radius = min(Fraction(results[n]["full_fibre_witnesses"]["real_cube_radius"])
                 for n in names) / 2
    return {"root_coefficients":dict.fromkeys(names, "1/2"),
            "marginal":"Separate fixed N13 marginals, conditional lifts may vary independently",
            "endpoint_aggregation":"Coherent sum at common N14 masks before readout",
            "shared_end_types":len(set(labels1).intersection(labels2)),
            "known_clock_masks_on_support":[types[j] for j in visible],
            "known_endpoint_real_cube_radius":str(radius),
            "all_orbits":full, "known_clock_orbits_only":limited}


def run():
    if not __debug__:
        raise RuntimeError("Keep Python assertions enabled")
    source = PRIOR / "v05"
    growth = ex.read_json(source / "growth.json")
    good = ex.admissible_orders(growth["sequential_admissible"])
    roots = ex.read_json(source / "upstream/v03/results.json")["paths_by_root"]
    certs = ex.read_json(source / "exchange_certificate.json")
    known, clocks = archived_clocks()
    eigen = {}
    results = {}
    parts = {}
    for name, row in sorted(roots.items()):
        target, columns, sizes, _ = ex.build(row, good)
        orbits = sorted(columns)
        c, b, types = matrices(orbits, target, columns, good)
        parts[name] = (c, [good[o] for o in orbits])
        full = dimensions(c, b, types, known)
        visible = sorted(set(types) & known)
        assert full["additional_known_coordinates"] == len(visible) == 3
        witnesses = positive_witnesses(target, columns, sizes, certs[name], orbits, types, c, b, known)
        limited = [o for o in orbits if good[o] in known]
        ck, bk, tk = matrices(limited, target, columns, good)
        restricted = dimensions(ck, bk, tk, known)
        results[name] = {"all_orbits":full, "known_clock_masks_on_support":visible,
                         "known_clock_orbits_only":restricted, "full_fibre_witnesses":witnesses}
        for mask in types:
            if mask not in eigen:
                omega = scalar_precision(mask, growth["audit"][str(mask)])
                eigen[mask] = omega[0, 0]

    # On the real line y = (t,0,0), the Gaussian exponents already separate.
    # Vandermonde independence of exp(-beta*lambda*u/2), u=t^2, is exact.
    assert len(set(eigen.values())) == len(eigen) == 101
    ref = ex.read_json(PRIOR / "sector.json")["conditional_scalar_branches"]
    for m, rec in ref.items():
        assert eigen[int(m)] == sp.sympify(rec["first_diagonal_precision_over_beta"])
    return {"scalar_seed":"I, output precision beta*Omega, beta=4/sqrt(6)",
            "bare_scalar_linearly_independent_states":len(eigen),
            "separating_line":[1, 0, 0],
            "Omega_11_by_N14_mask":{
                str(m):[str(sp.re(v)), str(sp.im(v))] for m,v in sorted(eigen.items())},
            "clock_masks_in_archive":sorted(known), "clock_grid_nonzero_checks":clocks,
            "rank_field":"Q for endpoint and marginal matrices, extended to C for linear coherent output",
            "observable":"Inherited unnormalized coherent N14 state before readout or postselection",
            "joint_preparation":joint_preparation(parts, known, results),
            "roots":results}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(), sort_keys=True, indent=2, allow_nan=False) + "\n")
