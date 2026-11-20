"""Exact rank of the marked-orbit marginal and of the output at prefix 1564."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations
from pathlib import Path
from sys import argv
from zipfile import ZipFile
import hashlib
import json

from sympy import Matrix, ZZ

ARCHIVE_SHA256 = "4a2b985578e9bf41662af0dede7c2054c8406de4f49d077891f505b0fffd917e"
PREFIX = 1564
EDGES = list(combinations(range(6), 2))
LABELS = list(permutations(range(6)))
MARKS = [(0, 1, 2, *p) for p in permutations((3, 4, 5))]
MASK = sum(1 << (6*i+j) for i in range(5) for j in range(5) if i != j)


def relabel(edges, labels):
    return sum(1 << (6*labels[i]+labels[j]) for i, j in edges)


def decode(code):
    return [divmod(i, 6) for i in range(36) if code & (1 << i)]


def rank(rows):
    return Matrix(rows).to_DM(domain=ZZ).rank()


def analyse(data, residual, probe):
    pair_law = {}
    for key, value in data["target_pair_marginal"].items():
        code = int(key)
        other = relabel(decode(code), (0, 1, 2, 4, 3, 5))
        pair = {code, other}
        for marked in pair:
            assert marked not in pair_law
            pair_law[marked] = Fraction(value)/len(pair)
    assert sum(pair_law.values()) == 1
    orbits = {}
    for end in data["fully_admissible_end_types"]:
        edges = [edge for i, edge in enumerate(EDGES) if end & (1 << i)]
        for code in sorted({relabel(edges, labels) for labels in LABELS}):
            if (code & MASK) not in pair_law:
                continue
            orbit = {relabel(decode(code), labels) for labels in MARKS}
            if min(orbit) == code and all(mark & MASK in pair_law for mark in orbit):
                orbits[code] = end, orbit
    columns = [(end, Counter(code & MASK for code in orbit)) for end, orbit in orbits.values()]
    count = sum(sum(counts.values()) for _, counts in columns)
    assert (len(columns), count) == (data["fully_admissible_orbits"], data["paths_valid_in_all_six_orders"])
    uniform = Fraction(data["max_uniform_labelled_path_component"])
    assert 0 < uniform <= 1
    # x[o] is mass PER labelled path in orbit o. Witness lies in the strict interior.
    weights = [uniform/count + (1-uniform)*Fraction(residual.get(str(key), 0))/len(orbit)
               for key, (_, orbit) in orbits.items()]
    assert min(weights) > 0
    rows = [[counts[p] for _, counts in columns] for p in sorted(pair_law)]
    for p, row in zip(sorted(pair_law), rows):
        assert sum(x*f for x, f in zip(weights, row)) == pair_law[p]
    r = rank(rows)
    out = {"orbits": len(columns), "marked_paths": count, "marginal_rank": r,
           "free_dimensions": len(columns)-r}
    if probe:
        types = sorted({end for end, counts in columns if counts[PREFIX]})
        local = [[counts[PREFIX] if end == t else 0 for end, counts in columns] for t in types]
        total = sum(sum(row) for row in local)
        assert total == 16 and len(types) == 10 and pair_law[PREFIX] == Fraction(1,147)
        joint = rank(rows+local)
        # Independently find local motions by swapping pairs of identical marginal columns.
        # Every such swap (unit +1 and -1) fixes the global marked marginal exactly.
        groups = {}
        for idx, col in enumerate(zip(*rows)):
            groups.setdefault(col, []).append(idx)
        swaps = [[row[j]-row[indices[0]] for row in local]
                 for indices in groups.values() for j in indices[1:]]
        swap_rank = rank(swaps)
        out["prefix"] = {"code": PREFIX, "end_types": types, "marked_paths": total,
                         "joint_rank": joint, "local_free_dimensions": joint-r,
                         "local_rank_from_equal_column_swaps": swap_rank}
        # Keep an exact invertible subsystem to find one lift of each local transfer.
        matrix = Matrix(rows+local)
        basis_rows = list(matrix.T.to_DM(domain=ZZ).rref()[1])
        reduced = matrix[basis_rows, :]
        basis_cols = list(reduced.to_DM(domain=ZZ).rref()[1])
        inverse = reduced[:, basis_cols].inv()
        reference = 1790
        keys = list(orbits)
        moves = {}
        for target in types:
            if target == reference:
                continue
            rhs = Matrix([0]*len(rows) + [pair_law[PREFIX]*((t == target)-(t == reference)) for t in types])
            lifted = inverse * rhs[basis_rows, :]
            assert matrix[:, basis_cols]*lifted == rhs
            step = min(weights[i]/abs(Fraction(v)) for i, v in zip(basis_cols, lifted) if v)/2
            delta = {str(keys[i]): str(v) for i, v in zip(basis_cols, lifted) if v}
            moves[str(target)] = {"symmetric_positive_step": str(step), "path_deltas": delta}
        out["prefix"]["reference_type"] = reference
        out["prefix"]["moves"] = moves
    return out


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so that certificate checks are active")
    archive = Path(argv[1])
    if hashlib.sha256(archive.read_bytes()).hexdigest() != ARCHIVE_SHA256:
        raise SystemExit("Archive SHA-256 mismatch")
    with ZipFile(archive) as z:
        def read(name):
            return json.loads(z.read("prefix_1564_selection_v0_1/inputs/" + name))
        exchange = read("exchange.json")
        cert = read("exchange_certificate.json")
    results = {k: analyse(data, cert[k]["residual_orbit_masses"], k == "one")
               for k, data in exchange.items()}
    print(json.dumps(results, indent=2))
