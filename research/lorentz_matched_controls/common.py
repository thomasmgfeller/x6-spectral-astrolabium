"""Design-only exact matching on N, number of relations and height."""
from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT/'research/lorentz_matching_geometry'))
import core as prior_core
import geometry as prior_geometry
sys.path.pop(0)

require = prior_core.require
token = prior_core.token
NAMESPACE = 'density-height-controls-v1'


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def savez(path, value):
    path.write_bytes(gzip.compress((token(value)+'\n').encode(), mtime=0))


def readz(path):
    return json.loads(gzip.decompress(path.read_bytes()))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix(record):
    return [[int(x) for x in row] for row in record['relation_rows']]


def relation_digest(record):
    return hashlib.sha256(token(record['relation_rows']).encode()).hexdigest()


def sample(family, n, split, draw):
    rng_split = NAMESPACE+':'+split
    record = prior_geometry.sample(family, n, rng_split, draw)
    record['rng_split'] = rng_split
    record['split'] = split
    return record


def profile(record):
    rows = record['relation_rows']
    n = len(rows)
    counts = [sum(rows[i][j] == '1' for i in range(n)) for j in range(n)]
    rank = [1]*n
    for j in sorted(range(n), key=lambda j: counts[j]):
        rank[j] = 1+max((rank[i] for i in range(n) if rows[i][j] == '1'), default=0)
    return sum(row.count('1') for row in rows), max(rank)


def ledger_entry(record):
    relations, height = profile(record)
    return {**{k: record[k] for k in ['id', 'family', 'n', 'split', 'draw', 'rng_split']},
            'R': relations, 'H': height, 'relation_sha256': relation_digest(record)}


def priority(control, n, split, first, second):
    return hashlib.sha256(token([NAMESPACE, 'pair-priority', control, n, split, first, second]).encode()).hexdigest()


def select(ledger, cfg):
    result = {}
    for n in cfg['generators']['sizes']:
        for control in cfg['matching']['controls']:
            cell = dict(n=n, control=control)
            for split in cfg['generators']['splits']:
                groups = [defaultdict(list), defaultdict(list)]
                for r in ledger:
                    if r['n'] == n and r['split'] == split and r['family'] in ['minkowski', control]:
                        groups[int(r['family'] == control)][(r['R'], r['H'])].append(r)
                pairs, strata = [], []
                for R, H in sorted(groups[0].keys() | groups[1].keys()):
                    a, b = (sorted(g.get((R, H), []), key=lambda r: r['draw']) for g in groups)
                    strata.append(dict(R=R, H=H, minkowski=len(a), control=len(b), eligible=min(len(a), len(b))))
                    for x, y in zip(a, b):
                        pairs.append(dict(ids=[x['id'], y['id']], R=R, H=H,
                                          priority=priority(control, n, split, x['id'], y['id'])))
                pairs.sort(key=lambda p: (p['priority'], p['ids']))
                cap = cfg['matching'][split+'_pairs']
                cell[split] = dict(eligible=len(pairs), required=cap, pairs=pairs[:cap],
                                   all_eligible_pairs=pairs, strata=strata,
                                   unused_per_family=cfg['generators']['pool_per_family_size_split']-min(cap, len(pairs)))
            cell['status'] = ('EVALUABLE' if all(cell[s]['eligible'] >= cell[s]['required'] for s in ['train', 'test'])
                              else 'INSUFFICIENT_COMMON_SUPPORT')
            result[f'{control}/n{n}'] = cell
    return result


def selected_ids(selection):
    return sorted({name for cell in selection.values() if cell['status'] == 'EVALUABLE'
                   for split in ['train', 'test'] for pair in cell[split]['pairs'] for name in pair['ids']})


def expected_keys(cfg):
    return {(f, n, s, d) for f in cfg['generators']['families'] for n in cfg['generators']['sizes']
            for s in cfg['generators']['splits'] for d in range(cfg['generators']['pool_per_family_size_split'])}


def validate_ledger(ledger, cfg):
    keys = [(r['family'], r['n'], r['split'], r['draw']) for r in ledger]
    require(len(keys) == len(set(keys)) and set(keys) == expected_keys(cfg), 'complete unique candidate ledger')
    require(len({r['id'] for r in ledger}) == len(ledger), 'unique candidate identities')


def validate_pairs(selection, ledger):
    lookup = {r['id']: r for r in ledger}
    for cell in selection.values():
        used = set()
        for split in ['train', 'test']:
            for pair in cell[split]['pairs']:
                a, b = [lookup[name] for name in pair['ids']]
                require(a['family'] == 'minkowski' and b['family'] == cell['control'], 'pair roles')
                require(a['n'] == b['n'] == cell['n'] and a['R'] == b['R'] == pair['R']
                        and a['H'] == b['H'] == pair['H'], 'exact N R H matching')
                require(a['split'] == b['split'] == split and not (set(pair['ids']) & used), 'no split leakage or replacement')
                used.update(pair['ids'])
