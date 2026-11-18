"""Enumerate labelled insertions, their unmarked quotients, and scalar domains."""
from collections import Counter
from contextlib import contextmanager
from functools import cache
from itertools import combinations, permutations, product
from pathlib import Path
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "upstream"))
import geometry

NODES = (4, 5, 6, 11, 12)
ROOTS = {"chain": frozenset([(0, 1), (0, 2), (1, 2)]), "one": frozenset([(0, 2)])}


def transitive(edges):
    return all((a, d) in edges for a, b in edges for c, d in edges if b == c)


def bit_edges(n, mask):
    return frozenset(pair for bit, pair in enumerate(combinations(range(n), 2)) if mask & (1 << bit))


@cache
def orbit_table(n):
    table = {}
    for mask in range(1 << (n * (n - 1) // 2)):
        edges = bit_edges(n, mask)
        if edges in table or not transitive(edges):
            continue
        for perm in permutations(range(n)):
            table[frozenset((perm[i], perm[j]) for i, j in edges)] = mask
    expected = {3: (19, 5), 4: (219, 16), 5: (4231, 63)}
    assert (len(table), len(set(table.values()))) == expected[n]
    return table


def extend(old, n):
    for pattern in product((-1, 0, 1), repeat=n):
        extra = {(i, n) if s < 0 else (n, i) for i, s in enumerate(pattern) if s}
        candidate = old | extra
        if transitive(candidate):
            yield candidate


def swapped(edges):
    ids = (0, 1, 2, 4, 3)
    return frozenset((ids[i], ids[j]) for i, j in edges)


def restrict(edges, n):
    return frozenset((i, j) for i, j in edges if max(i, j) < n)


def paths():
    four, five = orbit_table(4), orbit_table(5)
    families = {}
    for root, old in ROOTS.items():
        marked = {end for middle in extend(old, 3) for end in extend(middle, 4)}
        direct = {end for end in five if restrict(end, 3) == old}
        assert marked == direct and all(swapped(end) in marked for end in marked)
        families[root] = {end: (four[restrict(end, 4)], four[restrict(swapped(end), 4)], five[end])
                          for end in sorted(marked, key=lambda e: tuple(sorted(e)))}
    return families


def layout(key):
    n, mask = key
    inner = NODES[:n]
    p, f = geometry.P, geometry.F
    edges = set(combinations(p, 2)) | set(combinations(f, 2)) | set(product(p, inner + f))
    edges.update(product(inner, f))
    edges.update((inner[i], inner[j]) for i, j in bit_edges(n, mask))
    assert transitive(edges)
    coefficients = {}
    for i, j in sorted(edges):
        size = sum((i, h) in edges and (h, j) in edges for h in (*p, *inner, *f))
        coefficients[i, j] = (1, -9, 16, -8)[size] if size <= 3 else 0
    return inner, coefficients, 8 + n - sum(coefficients.values())


@contextmanager
def scalar_layouts():
    # Both upstream scalar implementations derive every matrix from this one layout.
    with patch.object(geometry, "order", layout):
        yield


def screen(families):
    keys = {(3, orbit_table(3)[old]) for old in ROOTS.values()}
    for ends in families.values():
        for middle, alternate, end in ends.values():
            keys.update(((4, middle), (4, alternate), (5, end)))
    audit, states = {}, {}
    geometry.mp.mp.dps = 55
    with scalar_layouts():
        for key in sorted(keys):
            row, state = geometry.kernel(key)
            audit[key] = row
            if state is not None:
                states[key] = state
    return audit, states


def daughter_counts(key):
    n, mask = key
    tab = orbit_table(n + 1)
    return Counter(tab[end] for end in extend(bit_edges(n, mask), n))


def label(key):
    return f"N{8 + key[0]}_{key[1]}"
