"""Check visibility directly from the ordered open intervals for every catalogue type."""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import json

from randquelle import PAST, DEPTH_ROWS, PROFILE, edge_weight

INNER = (4, 5, 6, 11, 12, 13, 14)
FUTURE = (7, 8, 9, 10)
ROOT = Path(__file__).resolve().parent / 'katalog'


def load(name):
    return json.loads((ROOT / name).read_text())


def relation(code):
    ordered = set(combinations(PAST, 2)) | set(combinations(FUTURE, 2))
    ordered.update(product(PAST, INNER + FUTURE))
    ordered.update(product(INNER, FUTURE))
    ordered.update(link for bit, link in enumerate(combinations(INNER, 2)) if code & (1 << bit))
    return ordered


def inspect(code):
    ordered = relation(code)
    def interval(i, j):
        return sum((i, k) in ordered and (k, j) in ordered for k in range(15))
    counts = {j:sum((k, j) in ordered for k in INNER) for j in INNER}
    for j in INNER + FUTURE:
        row = tuple(edge_weight(interval(i, j)) for i in PAST)
        depth = counts.get(j, len(INNER))
        assert row == (DEPTH_ROWS[depth] if depth < 4 else (0,)*4)
        assert sum(x*y for x,y in zip(row, PROFILE)) == (-64 if depth < 4 else 0)
    return {j:d for j,d in counts.items() if d >= 4}


def audit():
    ranks = load('catalog.json')['ranks_pure_free_mixed']
    allowed = sorted(int(code) for code, (a, _, b) in ranks.items() if a == b == 0)
    hidden = {i:inspect(i) for i in allowed}
    complete = {i for i,deep in hidden.items() if not deep}
    base = load('weights.json')['laws']
    chain = load('chain.json')['law']
    support = {int(i) for i in set(chain) | set(base['1:1'])}
    assert set(base['1:1']) == set(base['1:3']) and support <= set(allowed)
    assert len(allowed) == 1048 and len(support) == 453 and 375841 in complete
    masses = {}
    for label, law in base.items():
        weights = {i:(Q(law.get(str(i), 0)) + Q(chain.get(str(i), 0)))/2 for i in support}
        assert sum(weights.values()) == 1 and min(weights.values()) > 0
        masses[label] = sum(weights[i] for i in complete & support)
    witness = min(support - complete)
    return {
        'typen':len(allowed), 'vollstaendige_typen':len(complete),
        'anzahl_typen_nach_zahl_unsichtbarer_ereignisse':
            dict(sorted(Counter(map(len,hidden.values())).items())),
        'ensemble_traeger':len(support), 'ensemble_vollstaendig':len(complete & support),
        'anteil_des_eingesetzten_typgewichts_auf_vollstaendigen_typen':masses,
        'gegenbeispiel_im_ensemble':{'typ':witness, 'unsichtbare_ereignisse_und_vorgaengerzahl':hidden[witness]},
    }
