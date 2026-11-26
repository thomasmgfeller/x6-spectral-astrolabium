"""Enclose every free stationary matter branch on one mixed order."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path

from basis.intervall import Box, SCALE, box

ROOT = Path(__file__).resolve().parent
SOURCE = json.loads((ROOT / 'basis/zweig.json').read_text())
PAST, FUTURE, INNER = (tuple(SOURCE[k]) for k in ('past', 'future', 'inner'))
U, Z = 15, 16
P = frozenset((0, 1, 2))
COLLAR = frozenset(FUTURE)
OLD = frozenset(tuple(edge) for edge in SOURCE['order'])
NODES = range(17)
COEFF = (1, -9, 16, -8)
E = (F(1, 6) - F(1, 2**22), F(1, 6) + F(1, 2**22))
X = (F(999, 2000), F(1001, 2000))


def serial(a):
    return [str(F(v, SCALE)) for v in (a.lo, a.hi)]


def filters():
    rest = [i for i in range(15) if i not in P]
    options = []
    for mask in range(1 << len(rest)):
        f = frozenset(i for k, i in enumerate(rest) if mask >> k & 1)
        if all(a not in f or b in f for a, b in OLD) and all((i, j) in OLD for i in P for j in f):
            options.append(f)
    return [(u, z) for u in options for z in options if z <= u]


def relation(u, z):
    rel = OLD | {(i, n) for i in P for n in (U, Z)} | {(U, Z)}
    rel |= {(U, j) for j in u} | {(Z, j) for j in z}
    assert all(i != j for i, j in rel)
    assert all((i, k) in rel for i, j in rel for v, k in rel if v == j)
    return rel


class Equations:
    def __init__(self, u, z, method):
        self.rel = relation(u, z)
        self.pilot = level(u,z).startswith('pilot')
        self.method = method
        pred = {j: {i for i, v in self.rel if v == j} for j in NODES}
        future = {i: {j for v, j in self.rel if v == i} for i in NODES}
        self.incoming = {j: [] for j in NODES}
        self.outgoing = {j: [] for j in NODES}
        for i, j in sorted(self.rel):
            if method == 'shift':
                n = len(future[i] & pred[j])
            else:
                n = sum((i, k) in self.rel and (k, j) in self.rel for k in NODES)
            if n < len(COEFF):
                self.incoming[j].append((i, COEFF[n]))
                self.outgoing[i].append((j, COEFF[n]))
        assert dict(self.incoming[Z]) == {0: -8, 1: 16, 2: -9, U: 1}
        self.order = sorted((*INNER, Z), key=lambda j: (len(pred[j]), j))
        self.neighbours = {j: (pred[j], future[j]) for j in NODES}

    def clock_ok(self, j, y):
        before, after = self.neighbours[j]
        return all(y[i].lo < y[j].hi for i in before if i in y) and all(
            y[j].lo < y[k].hi for k in after if k in y)

    def clock_roots(self, j, y):
        terms = [(b, y[i]) for i, b in self.incoming[j]]
        a = sum(b for b, _ in terms)
        origin = y[3] if self.method == 'shift' else box(0)
        moment = sum((b * (v - origin) for b, v in terms), box(0))
        constant = 19 + sum((b * (v - origin).square() for b, v in terms), box(0))
        if not a:
            if moment.lo <= 0 <= moment.hi:
                impossible = moment.lo == moment.hi == 0 and not constant.lo <= 0 <= constant.hi
                return [], not impossible
            return [origin + constant / (2 * moment)], False
        if self.method == 'shift':
            disc = moment.square() - a * constant
        else:
            disc = -19*a - sum((b*c*(v-w).square() for (b,v),(c,w) in combinations(terms,2)),box(0))
        if disc.hi < 0:
            return [], False
        root = disc.sqrt_nonnegative_part()
        return [origin + (moment + sign * root) / a for sign in (-1, 1)], False

    def cell(self, erange, xrange, keep=False):
        e, x = Box.hull(*erange), Box.hull(*xrange)
        t = e - 2 + (4 - e) * x
        rad = t.square() + 6*t + 6
        assert rad.lo > 0
        d = rad.sqrt_nonnegative_part()
        y = {j: box(j-5) for j in PAST + FUTURE}
        y.update({3: e-2, Z: t, U: t-d})
        counts = Counter()
        records = []
        evidence = []
        def reject(key, interval=None):
            counts[key] += 1
            if interval is not None:
                evidence.append((key, *serial(interval)))
        if not all(self.clock_ok(j, y) for j in y):
            reject('order_fixed')
            return counts, evidence, records

        def densities(y):
            w = {**{i:box(F(1,8)) for i in PAST}, **{j:box(F(1,64)) for j in FUTURE}, U:box(0)}
            for j in reversed(self.order):
                moment = sum((b*(y[j]-y[i]) for i,b in self.incoming[j]),box(0))
                if j == Z:
                    moment = d - t - 3
                out = sum((b*w[k]*(y[k]-y[j]) for k,b in self.outgoing[j]),box(0))
                if moment.lo <= 0 <= moment.hi:
                    residual = out - Box.hull(0,1)*moment
                    if residual.lo > 0 or residual.hi < 0:
                        reject(f'inconsistent_density_{j}',residual)
                    else:
                        reject(f'open_denominator_{j}')
                    return
                candidate = out / moment
                if candidate.hi <= 0 or candidate.lo >= SCALE:
                    reject(f'density_{j}', candidate)
                    return
                w[j] = candidate.intersection(Box.hull(0,1))
            current = sum((b*w[k]*(y[k]-y[U]) for k,b in self.outgoing[U]),box(0))
            if current.lo > 0 or current.hi < 0:
                reject('vacuum_current', current)
            else:
                reject('open_current', current)
            if keep:
                records.append((dict(y),dict(w),current))

        def clocks(index, y):
            if index == len(self.order):
                densities(y)
                return
            j = self.order[index]
            if j == Z:
                clocks(index+1, y)
                return
            roots, undecided = self.clock_roots(j, y)
            if undecided:
                reject(f'open_linear_{j}')
            elif not roots:
                reject(f'no_real_root_{j}')
            for value in roots:
                state = {**y, j:value}
                if self.clock_ok(j, state):
                    clocks(index+1, state)
                else:
                    reject(f'order_{j}')
                    if self.pilot and j == 14:
                        before, after = self.neighbours[j]
                        predecessor = max((i for i in before if i in y), key=lambda i:y[i].lo)
                        successor = min((k for k in after if k in y), key=lambda k:y[k].hi)
                        evidence.append({'root14':serial(value),'after':predecessor,
                                         'after_lower':serial(y[predecessor])[0],
                                         'before':successor,'before_upper':serial(y[successor])[1]})

        clocks(0, y)
        return counts, evidence, records


def certify(eq, erange, xrange, depth=0):
    reasons, evidence, _ = eq.cell(erange, xrange)
    pending = any(k.startswith('open_') for k in reasons)
    row = {'x':list(map(str,xrange)), 'e':list(map(str,erange)), 'reasons':dict(reasons),
           'intervals':evidence}
    if not pending or depth >= 15:
        row['status'] = 'OPEN' if pending else 'EXCLUDED'
        return [row]
    # Split the wider effective coordinate; both enter t with O(1) derivative.
    if 4*(xrange[1]-xrange[0]) >= erange[1]-erange[0]:
        a,b=xrange
        m=(a+b)/2
        return certify(eq,erange,(a,m),depth+1) + certify(eq,erange,(m,b),depth+1)
    a,b=erange
    m=(a+b)/2
    return certify(eq,(a,m),xrange,depth+1) + certify(eq,(m,b),xrange,depth+1)


def level(u,z):
    if u <= COLLAR:
        return 'archived'
    if 3 in z:
        return 'order'
    if z < COLLAR:
        return 'density'
    if (u & set(INNER)) == {14}:
        return 'pilot_B' if 14 in z else 'pilot_A'
    return 'further'


def run(pilot=False):
    pairs = filters()
    rows = []
    selection = [(u,z) for u,z in pairs if not pilot or level(u,z).startswith('pilot')]
    for u,z in selection:
        eq = Equations(u,z,'shift')
        cells = certify(eq,E,X)
        rows.append({'u':sorted(u), 'z':sorted(z), 'group':level(u,z),
                     'status':'OPEN' if any(c['status']=='OPEN' for c in cells) else 'EXCLUDED',
                     'cells':cells})
    return rows


if __name__ == '__main__':
    import sys
    if not __debug__:
        raise SystemExit('Run without -O')
    print(json.dumps(run('--pilot' in sys.argv),indent=2,sort_keys=True))
