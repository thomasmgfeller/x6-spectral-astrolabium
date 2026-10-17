"""Frozen stream, transparent IO, generator and matching; no test-based tuning."""
from collections import Counter, defaultdict
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import numpy as np
from proper_core import require

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('proper_prior_core', ROOT/'research/lorentz_matching_geometry/core.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
Stream = prior.Stream
NS = 'lorentz-proper-time-v1'
MODELS = ['V', 'L', 'C0', 'D']


def token(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def save(path, x):
    path.write_text(json.dumps(x, indent=2, ensure_ascii=False, allow_nan=False)+'\n')


def savez(path, x):
    with path.open('wb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', mtime=0, filename='') as z:
        for block in json.JSONEncoder(sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False).iterencode(x):
            z.write(block.encode())


def readz(path):
    with gzip.open(path, 'rt') as handle:
        return json.load(handle)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packet(record):
    return {k: record[k] for k in ['N', 'marks', 'relation_rows']}


def sample(family, m, split, draw, namespace=NS):
    require(family in ['uniform', 'jittered_grid'] and m > 0, 'generator parameters')
    key = [namespace, family, m, split, draw]
    rng = Stream(*key)
    for attempts in range(1, 10001):
        p, q = [rng.unit(), rng.unit()], [rng.unit(), rng.unit()]
        if p[0] < q[0] and p[1] < q[1]:
            break
    else:
        raise ValueError('endpoint attempt limit '+token(key))
    coords = [p, q]
    if family == 'uniform':
        coords.extend([[rng.unit(), rng.unit()] for _ in range(m)])
    else:
        side = 2*math.isqrt(m)
        require(side*side == 4*m, 'square background size')
        sites = rng.shuffle(range(side*side))[:m]
        coords.extend([[(site//side+0.5+0.4*(rng.unit()-0.5))/side,
                        (site % side+0.5+0.4*(rng.unit()-0.5))/side] for site in sites])
    ties = {name: sum(v*(v-1)//2 for v in Counter(row[axis] for row in coords).values())
            for axis, name in enumerate(['u_equal_pairs', 'v_equal_pairs'])}
    ties['duplicate_points'] = len(coords)-len(set(map(tuple, coords)))
    require(ties['duplicate_points'] == 0, 'duplicate point '+token(key))
    xy = np.asarray(coords)
    c = (xy[:, None, 0] <= xy[None, :, 0]) & (xy[:, None, 1] <= xy[None, :, 1])
    np.fill_diagonal(c, False)
    a = (q[0]-p[0])*(q[1]-p[1])
    return dict(id=f'{family}-m{m}-{split}-{draw:04d}', family=family, m=m, N=m+2,
                split=split, draw=draw, rng_key=key, endpoint_attempts=attempts,
                ties=ties, coordinates=coords, marks=[0, 1], a=a, theta=math.sqrt(a),
                relation_rows=[''.join('1' if x else '0' for x in row) for row in c])


def expected_keys(cfg):
    g = cfg['sampling']
    return {(family, m, split, draw) for m in g['m_values'] for family in g['families']
            for split in ['calibration', 'test']
            for draw in range(g['test_per_family_m'] if split == 'test' else g['calibration'][family+'_per_m'])}


def coverage(records, cfg):
    keys = [(r['family'], r['m'], r['split'], r['draw']) for r in records]
    require(len(keys) == len(set(keys)) and set(keys) == expected_keys(cfg), 'complete unique cohort')
    require(len({r['id'] for r in records}) == len(records), 'unique identities')
    g = cfg['sampling']
    ordered = [(family, m, split, draw) for m in g['m_values'] for family in g['families']
               for split in ['calibration', 'test']
               for draw in range(g['test_per_family_m'] if split == 'test' else g['calibration'][family+'_per_m'])]
    require(keys == ordered, 'prespecified observation order')


def matching(records, cfg):
    out = {}
    for m in cfg['sampling']['m_values']:
        groups = {f: defaultdict(list) for f in cfg['sampling']['families']}
        for r in records:
            if r['m'] == m and r['split'] == 'test':
                f = r['features']
                groups[r['family']][(f['R'], f['H'])].append((r['draw'], r['id']))
        u, j = groups['uniform'], groups['jittered_grid']
        pairs, strata = [], []
        for R, H in sorted(u.keys() | j.keys()):
            aa, bb = sorted(u.get((R, H), [])), sorted(j.get((R, H), []))
            strata.append(dict(R=R, H=H, uniform=len(aa), jittered_grid=len(bb)))
            for a, b in zip(aa, bb):
                ids = [a[1], b[1]]
                priority = hashlib.sha256(token([NS, 'match', m, *ids]).encode()).hexdigest()
                pairs.append(dict(ids=ids, R=R, H=H, priority=priority))
        pairs.sort(key=lambda p: (p['priority'], p['ids']))
        cap = cfg['matched_transfer']['minimum_pairs']
        out[str(m)] = dict(m=m, N=m+2, eligible=len(pairs), required=cap,
                          status='EVALUABLE' if len(pairs) >= cap else 'INSUFFICIENT_COMMON_SUPPORT',
                          all_eligible_pairs=pairs, selected_pairs=pairs[:cap] if len(pairs) >= cap else [], strata=strata)
    return out
