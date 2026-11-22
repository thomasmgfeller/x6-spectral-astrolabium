"""Direct center quadrature for the registered transfer on type 42429.

Only the earlier hand witness is used for input checks. Discrete edges are
rebuilt from the four maximal inner paths; no certified-result tables enter.
"""
from fractions import Fraction as Q
from itertools import product
import json
from pathlib import Path
import sys
import mpmath as mp

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "basis"))
import zeuge42429 as witness

PAST = (0, 1, 2, 3)
INNER = (4, 5, 6, 11, 12, 13, 14)
FUTURE = (7, 8, 9, 10)
PATHS = ((4, 5, 11, 12), (4, 5, 14), (4, 13), (6, 13))
IDEAL = set(PAST + PATHS[0])
MID, H = Q(1, 8), Q(1, 2**20)
RESOLUTIONS = ((3, 65), (4, 85))


def geometry():
    successors = {k: set() for k in range(17)}
    for path in PATHS:
        chain = PAST + path + FUTURE
        for i, j in zip(chain, chain[1:]):
            successors[i].add(j)
    successors[12].add(15)
    successors[15].add(16)
    successors[10].add(16)
    def visit(k):
        seen, todo = set(), list(successors[k])
        while todo:
            v = todo.pop()
            if v not in seen:
                seen.add(v)
                todo.extend(successors[v])
        return seen
    closure = {k: visit(k) for k in successors}
    ancestors = {j: {k for k in closure if j in closure[k]} for j in closure}
    assert ancestors[15] == IDEAL and ancestors[16] == set(range(16))
    original = {(i,j) for i in range(15) for j in closure[i] if j < 15}
    assert original == witness.build_order()
    rows = []
    for j in range(17):
        row = []
        for i in sorted(ancestors[j]):
            size = len(closure[i] & ancestors[j])
            if size < 4:
                row.append((i, (1, -9, 16, -8)[size]))
        rows.append(row)
    return rows, original


def packet(shift, relation):
    center = {v: Q(max(p.index(v)+1 for p in PATHS if v in p),5) for v in INNER}
    assert center == witness.CENTER
    center[11] += shift
    f = dict.fromkeys(INNER, Q(0))
    for path in PATHS:
        cuts = [Q(0), *((center[a] + center[b])/2 for a,b in zip(path, path[1:])), Q(1)]
        for i,v in enumerate(path):
            f[v] += (cuts[i+1] - cuts[i]) / 4
    p_over_M, original_f = witness.source_charge(relation, center)
    assert original_f == f and sum(f.values()) == 1
    y = dict(zip(PAST, (Q(-5), Q(-4), Q(-3), Q(-7,4))))
    y.update({v: Q(-7,4) + Q(15,4)*center[v] for v in INNER})
    y.update(dict(zip(FUTURE + (15, 16), map(Q, (2,3,4,5,6,7)))))
    inner_densities = {v: Q(15,16)*f[v] for v in INNER}
    return [y[k] for k in range(17)], inner_densities, p_over_M / 4


def number(q):
    return mp.mpf(q.numerator)/q.denominator


def direct(order, digits, rows, y0, W):
    with mp.workdps(digits):
        mid, h = number(MID), number(H)
        delta = (mp.mpf(3)/722)**(mp.mpf(1)/4)
        xs, weights = mp.gauss_quadrature(order, "legendre")
        grid = list(zip(xs, [w/2 for w in weights]))
        t = [mid + h*(side + x)/2 for side in (-1,1) for x,_ in grid]
        def slope(y, j):
            return -mp.mpf("0.5")-mp.fsum(b*(y[i]-y[j])**2 for i,b in rows[j])/38
        def average_phase(d, radius):
            return mp.expj(mid*d)*mp.sinc(radius*d)
        # Index 0 is the reference x=0; the rest are the clock quadrature nodes.
        clock = [mp.mpf(0)] + [h*u for u,_ in grid]
        conditional = [[mp.mpc(0) for _ in t] for _ in clock]
        for cells in product(grid, repeat=3):
            y = [number(v) for v in y0]
            for i, (u,_) in zip(FUTURE[1:],cells):
                y[i] += h*u
            d = [slope(y,j) for j in range(15)]
            old = mp.fprod(w for _,w in cells)
            old *= average_phase(mp.fsum(d[v] for v in PAST), number(Q(1,32)))
            old *= mp.expj(delta*mp.fsum(number(W[v])*d[v] for v in INNER))
            old *= mp.fprod(average_phase(d[v], h) for v in FUTURE)
            for j,x in enumerate(clock):
                y[15] = 6+x
                coeff = old*average_phase(slope(y,15),h)
                terminal = slope(y,16)
                for i,rho in enumerate(t):
                    conditional[j][i] += coeff*mp.expj(rho*terminal)
        data = {}
        for arm in ("sharp","mix","coherent"):
            intensity = []
            for i in range(len(t)):
                if arm == "sharp":
                    v = abs(conditional[0][i])**2
                elif arm == "mix":
                    v = mp.fsum(w*abs(conditional[j+1][i])**2 for j,(_,w) in enumerate(grid))
                else:
                    v = abs(mp.fsum(w*conditional[j+1][i] for j,(_,w) in enumerate(grid)))**2
                intensity.append(v)
            lo, hi = [mp.fsum(w*intensity[j+i*order]/2 for j,(_,w) in enumerate(grid))
                      for i in (0,1)]
            total = lo+hi
            assert total > 0
            data[arm] = (hi/total, total)
        return data


def run():
    if not __debug__:
        raise RuntimeError("Run without -O")
    rows, relation = geometry()
    out = {"type":42429,"preregistration_commit":"7baa149a5c42de920d9249f30caeba6d527ebc9b",
           "scope":"packet centers, conditional dust probabilities; common scalar factor omitted",
           "mass":"1/4","end_effect":"t>1/8","h":str(H),"cases":{},"resolutions":{}}
    centers = {}
    for shift in (Q(-1,128),Q(1,128)):
        Y,W,p = packet(shift, relation)
        label = "positive" if p>0 else "negative"
        assert p and label not in centers
        centers[label] = (Y,W)
        out["cases"][label] = {"shift_u11":str(shift),"current":str(p)}
    previous = None
    for order, digits in RESOLUTIONS:
        with mp.workdps(digits):
            data = {s:direct(order,digits,rows,Y,W) for s,(Y,W) in centers.items()}
            gaps = {a:data["positive"][a][0]-data["negative"][a][0] for a in ("sharp","mix","coherent")}
            gaps["primary"] = gaps["coherent"]-gaps["mix"]
            gaps["mix_minus_sharp"] = gaps["mix"]-gaps["sharp"]
            if previous:
                p_old, gap_old = previous
                assert all(abs(gap_old[k]-v)<mp.mpf("1e-48") for k,v in gaps.items())
                assert all(abs(p_old[s][a][0]-u[0])<mp.mpf("1e-43") and
                           abs(p_old[s][a][1]-u[1])<mp.mpf("1e-30")
                           for s,arms in data.items() for a,u in arms.items())
            previous = (data,gaps)
            out["resolutions"][str(digits)] = {
                "gauss_order":order,
                "probabilities":{s:{a:{"p_upper":mp.nstr(p,60),"dust_norm":mp.nstr(norm,45)}
                                     for a,(p,norm) in arms.items()} for s,arms in data.items()},
                "positive_minus_negative":{k:mp.nstr(v,35) for k,v in gaps.items()}}
    return out


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, ensure_ascii=False))
