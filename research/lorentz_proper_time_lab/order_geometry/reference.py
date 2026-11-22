"""Build the fixed-size Minkowski reference bank and audit browser exports.

python reference.py --build        Reproduce reference.json (NumPy PCG64).
python reference.py result.json    Recount the selected strict order.
"""
import argparse
import json
from collections import Counter
from fractions import Fraction
from math import exp, factorial, lgamma, log, prod, sqrt
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BANK_SIZE = 255
MAX_K = 128
SEED = 20261122
GRID = (15, 30, 50, 100, 256, 1024, 4096, 16384)


def lis_counts(n):
    """Robinson–Schensted and the hook-length formula, both endpoints excluded."""
    def partitions(total, cap):
        if total == 0:
            yield ()
        for first in range(min(total, cap), 0, -1):
            for tail in partitions(total - first, first):
                yield (first,) + tail

    counts = [0] * (n + 1)
    for shape in partitions(n, n):
        hooks = (length-j+sum(size > j for size in shape[i+1:])
                 for i, length in enumerate(shape) for j in range(length))
        tableaux = factorial(n) // prod(hooks)
        counts[shape[0]] += tableaux**2
    assert sum(counts) == factorial(n)
    return counts


def sample(random, shape, d):
    """Uniform time slices, then uniform spatial ball conditional on time."""
    a = 0.5 * random.random(shape)**(1/d)
    t = (0.5-a) * random.choice([-1, 1], size=shape)
    direction = random.normal(size=(*shape, d-1))
    direction /= np.linalg.norm(direction, axis=-1, keepdims=True)
    radius = a * random.random(shape)**(1/(d-1))
    return np.concatenate((t[..., None], radius[..., None]*direction), axis=-1)


def conditional_bank(d):
    random = np.random.default_rng([SEED, 0, d])
    pts = sample(random, (BANK_SIZE, MAX_K), d)
    # Prefixes in original sampling order are nested iid fixed-K clouds.
    delta = pts[:, None, :, 0] - pts[:, :, None, 0]
    space = sum((pts[:, None, :, i]-pts[:, :, None, i])**2 for i in range(1,d))
    relation = (delta > 0) & (delta**2 > space)
    bank, rows = [[0, 0, 0]], np.arange(BANK_SIZE)[:, None, None]
    for k in range(1, MAX_K+1):
        order = np.argsort(pts[:, :k, 0], axis=1)
        rel = relation[rows, order[:, :, None], order[:, None, :]]
        heights = np.ones((BANK_SIZE, k), dtype=np.int16)
        for j in range(1, k):
            heights[:, j] += np.max(np.where(rel[:, :j, j], heights[:, :j], 0), axis=1)
        pairs = np.sort(rel.sum(axis=(1, 2)))
        # At two-sided level .025 with B=255, accept the inclusive
        # third-smallest to third-largest reference count (ties retained).
        bank.append([int(pairs[2]), int(pairs[-3]), int(heights.max(axis=1).sum())])
    return bank


def large_stats(points):
    """Time-ordered dynamic programming, linear working memory per cloud."""
    p = points[np.argsort(points[:, 0])].T.copy()
    heights = np.ones(p.shape[1], dtype=np.int16)
    count = 0
    for j in range(1, len(heights)):
        dt = p[0, j] - p[0, :j]
        square = dt*dt
        for axis in p[1:]:
            square -= (axis[j]-axis[:j])**2
        past = (square > 0) & (dt > 0)
        count += np.count_nonzero(past)
        heights[j] += heights[:j].max(where=past, initial=0)
    return int(heights.max()), int(count)


def scaling(d, k):
    trials = 48 if k <= 1024 else 12
    random = np.random.default_rng([SEED, 1, d, k])
    heights, pairs = np.array([large_stats(sample(random,(k,),d)) for _ in range(trials)]).T
    return dict(k=k, trials=trials, heightMean=float(heights.mean()),
                heightSE=float(heights.std(ddof=1)/sqrt(trials)),
                pairMean=float(pairs.mean()))


def analyse(nodes, edges, endpoints=None):
    ids = list(nodes)
    if len(set(ids)) != len(ids):
        raise ValueError('duplicate node ID')
    index = {v:i for i,v in enumerate(ids)}
    rel = np.zeros((len(ids),len(ids)), dtype=bool)
    for a,b in edges:
        rel[index[a],index[b]] = True
    for mid in range(len(ids)):
        rel |= rel[:, mid, None] & rel[mid, None, :]
    if rel.diagonal().any():
        raise ValueError('cyclic order')
    if endpoints is not None:
        a,b = (index[x] for x in endpoints)
        if not rel[a,b]:
            raise ValueError('unordered endpoints')
        keep = rel[a] & rel[:,b]
        rel = rel[np.ix_(keep,keep)]
    between = rel.astype(int) @ rel.astype(int)
    layers = Counter(between[rel].tolist())
    heights = np.ones(len(rel), dtype=int)
    for j in np.argsort(rel.sum(axis=0)):
        heights[j] += heights.max(where=rel[:,j], initial=0)
    return dict(k=len(rel), pairs=int(rel.sum()), height=int(heights.max(initial=0)),
                layers=[layers[i] for i in range(4)], matrix=rel.astype(int).tolist())


def mm_grid():
    grid = []
    for d in np.linspace(2,4,201):
        grid.append(exp(lgamma(d+1)+lgamma(d/2)-log(2)-lgamma(1.5*d)))
    grid[0], grid[-1] = 0.5, 0.1
    return grid


def build():
    counts = lis_counts(15)
    assert Fraction(sum(i*n for i,n in enumerate(counts)),sum(counts)) == Fraction(96968880223,17435658240)
    bank = {d:conditional_bank(d) for d in (2,3,4)}
    curves = {d:[scaling(d,k) for k in GRID] for d in (2,3,4)}
    result = dict(version='flat-bank/1', generator='NumPy PCG64', seed=SEED,
                  samples=BANK_SIZE, maxK=MAX_K, conditional=bank, scaling=curves,
                  lis15=counts, mmGrid=mm_grid())
    (HERE/'reference.json').write_text(json.dumps(result,separators=(',',':'))+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--build',action='store_true')
    parser.add_argument('export',nargs='?',type=Path)
    args=parser.parse_args()
    if args.build:
        build()
    elif args.export:
        data=json.loads(args.export.read_text())
        graph=data['graph']
        audit=analyse(graph['nodes'],graph['edges'],data['endpoints'])
        assert audit=={key:data['observables'][key] for key in audit}
        print('PASS', {key:v for key,v in audit.items() if key!='matrix'})
    else:
        parser.error('supply --build or a browser export')
