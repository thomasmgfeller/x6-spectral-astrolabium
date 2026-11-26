"""Enumerate strict past cones on a fixed induced order. Python 3.10+."""
import json
from itertools import combinations_with_replacement
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = json.loads((ROOT / 'quelle/zweig.json').read_text())
COUNT = 15
U, V, Z = range(COUNT, COUNT + 3)
OLD = (1 << COUNT) - 1


def members(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


OLD_PAST = tuple(sum(1 << i for i, j in SOURCE['order'] if j == node)
                 for node in range(COUNT))
IDEALS = tuple(mask for mask in range(OLD + 1)
               if all(not OLD_PAST[node] & ~mask for node in members(mask)))


def links(ideal):
    """Possible old past and old future of a point, within the ideal."""
    downs = [p for p in IDEALS if not p & ~ideal]
    return [(p, ideal ^ d) for p in downs for d in downs if not p & ~d
            and all(not p & ~OLD_PAST[j] for j in members(ideal ^ d))]


def direct(ideal):
    """0 incomparable, 1 chain oriented u<v. Old labels are fixed."""
    positions = links(ideal)
    for left, right in combinations_with_replacement(sorted(positions), 2):
        p, f = left
        q, g = right
        if not (f & q or g & p):
            yield (0, p, f, q, g)
    for p, f in positions:
        for q, g in positions:
            if not (p & ~q or g & ~f):
                yield (1, p, f, q, g)


def downsets(nodes, predecessors):
    """Build ideals successively in topological order."""
    ideals = [0]
    for j in sorted(members(nodes), key=lambda k: predecessors[k].bit_count()):
        includes = [d | (1 << j) for d in ideals if not predecessors[j] & ~d]
        ideals.extend(includes)
    return ideals


def insertions(nodes, predecessors):
    """Insert one point in a poset via an ideal and an upset."""
    ideals = downsets(nodes, predecessors)
    for past in ideals:
        for complement in ideals:
            future = nodes ^ complement
            if past & future:
                continue
            if all(not past & ~predecessors[j] for j in members(future)):
                yield past, future


def successive(ideal):
    """Insert a first point, then a second in the entire augmented poset.

    Orient chains by temporal order and canonicalise incomparable pairs.
    """
    keys = set()
    for p, f in insertions(ideal, OLD_PAST):
        augmented = [bits | ((1 << U) if f >> i & 1 else 0)
                     for i, bits in enumerate(OLD_PAST)] + [p]
        for past, future in insertions(ideal | (1 << U), augmented):
            first, second = (p, f), (past & OLD, future & OLD)
            if past >> U & 1:
                topology = 1
            elif future >> U & 1:
                topology = 1
                first, second = second, first
            else:
                topology = 0
                first, second = sorted((first, second))
            keys.add((topology, *first, *second))
    return keys


def predecessors(ideal, positions, chain=False):
    preds = {j: OLD_PAST[j] for j in members(ideal)}
    for new, (past, future) in enumerate(positions, U):
        preds[new] = past
        for j in members(future):
            preds[j] |= 1 << new
    if chain:
        preds[V] |= 1 << U
    preds[Z] = ideal | sum(1 << j for j in range(U, U + len(positions)))
    return preds
