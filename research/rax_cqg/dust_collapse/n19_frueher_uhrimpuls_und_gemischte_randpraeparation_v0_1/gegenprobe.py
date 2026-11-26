"""Independent finite differences of the rational action, and nodal equilibrium."""
from fractions import Fraction as F
from itertools import combinations
import json

from algebra import gauss_box
from quelle import box, hull, DATA, SCALE
from frueh import CLOCK, WEIGHT, PAST, FUT, LIVE, Z, R
from gemischt import Action, N

Y, W, ORDER, _, _, _ = DATA
NODES = list(range(19))
LAYERS = (1, -9, 16, -8)
EDGES = []
for i,j in sorted(ORDER):
    layer = sum((i,k) in ORDER and (k,j) in ORDER for k in NODES)
    if layer < 4:
        EDGES.append((i, j, LAYERS[layer]))


def fields(x):
    y = {i:v for i,v in zip(CLOCK, x[:11])}
    w = {i:v for i,v in zip(WEIGHT, x[11:20])}
    for i in PAST+FUT:
        y[i] = x[20] + (x[21] if i == 0 else 0) if i in PAST else 0
        y[i] += F(-11,6) if i == 3 else F(Y[i].lo,SCALE)
        w[i] = F(W[i].lo,SCALE)
    w[15] = w[17] = 0
    return y, w


def value(x):
    y, w = fields(x)
    return 19*sum(w.values()) + sum(c*w[j]*(y[j]-y[i])**2 for i,j,c in EDGES)


def gradients(y, w):
    G = [0]*19
    d_w = [19]*19
    for i,j,c in EDGES:
        gap = y[j]-y[i]
        flow = c*w[j]*gap
        G[i] += flow
        G[j] -= flow
        d_w[j] += c*gap*gap
    return G, d_w


def contains(interval, x):
    return interval.lo <= x*SCALE <= interval.hi


def shifted(x, changes):
    result = list(x)
    for k, delta in changes:
        result[k] += delta
    return result


def check_action(centre):
    step = F(1,8192)
    model = Action(True)
    g,H = model.evaluate([box(v) for v in centre])
    original = value(centre)
    for i in range(22):
        hi = value(shifted(centre, [(i, step)]))
        lo = value(shifted(centre, [(i, -step)]))
        assert contains(g[i], (hi-lo)/(2*step))
        assert contains(H[i][i], (hi-2*original+lo)/step**2)
    for i,j in combinations(range(22),2):
        derivative = sum(a*b*value(shifted(centre, [(i,a*step),(j,b*step)]))
                         for a in (-1,1) for b in (-1,1))/(4*step**2)
        assert contains(H[i][j], derivative) and contains(H[j][i], derivative)
    y,w = fields(centre)
    local_G0 = (w[1]*(y[1]-y[0])-9*w[2]*(y[2]-y[0])+16*w[3]*(y[3]-y[0])
                -8*sum(w[j]*(y[j]-y[0]) for j in (4,5,6,Z)))
    changing_0 = (value(shifted(centre, [(21,step)]))-value(shifted(centre, [(21,-step)])))
    assert local_G0 == -changing_0/(4*step)


def proof_box(proof):
    radius = F(proof['radius'])
    return [hull(F(v)-radius,F(v)+radius) for v in proof['solution_centres']]


def audit(early, mixed):
    cert = mixed['reference']
    base = proof_box(cert) + [box(0),box(0)]
    centre = list(map(F,cert['solution_centres']))+[F(0),F(0)]
    check_action(centre)
    y,w = fields(base)
    y = {i:box(v) for i,v in y.items()}
    w = {i:box(v) for i,v in w.items()}
    initial_G,_ = gradients(y,w)
    momentum = [sum(initial_G[i] for i in PAST),initial_G[0]]

    # A unit weight at each node gives an entire column without using 'currents'.
    columns = []
    for j in LIVE:
        masses = [int(i==j) for i in NODES]
        G,_ = gradients(y,masses)
        columns.append([G[i] for i in CLOCK]+[sum(G[i] for i in PAST),box(j==7)])
    v = gauss_box(list(zip(*columns)), [box(0)]*12+[box(1)])
    broad = early['fixed_clocks_and_sum']['dw_per_dw7']
    for i,a in zip(LIVE,v):
        lo,hi = map(F,broad[str(i)])
        assert lo <= F(a.lo,SCALE) <= F(a.hi,SCALE) <= hi
    changes = []
    for amp in (-F(1,10**6),F(1,10**6)):
        masses = w.copy()
        for i,di in zip(LIVE,v):
            masses[i] += amp*di
        G,d_w = gradients(y,masses)
        assert all(G[i].contains_zero() for i in CLOCK)
        assert all(d_w[i].contains_zero() for i in WEIGHT)
        assert (sum(G[i] for i in PAST)-momentum[0]).contains_zero()
        changes.append(G[0])
    gap = changes[0]-changes[1]
    assert gap.lo>0
    broad_gap = early['fixed_clocks_and_sum']['G0_plus_minus_separation']
    assert F(broad_gap[0]) <= F(gap.lo,SCALE) <= F(gap.hi,SCALE) <= F(broad_gap[1])

    for result in mixed['mixed_cases']:
        x = proof_box(result['proof'])
        y,w = fields(x)
        G,d_w = gradients(y,w)
        assert all(G[i].contains_zero() for i in CLOCK)
        assert all(d_w[i].contains_zero() for i in WEIGHT)
        assert (sum(G[i] for i in PAST)-momentum[0]).contains_zero()
        assert (G[0]-momentum[1]-F(result['delta_G0'])).contains_zero()
    return {'exact_rational_action_differences': {'gradients':22,'hessian_entries_with_symmetry':484,
            'explicit_G0_formula':True}, 'second_elimination_nominal_gap':gap.data(),
            'nodal_equilibria_checked': {'interior_equations_per_state':20,
            'source_free_density_witnesses':2, 'mixed_targets':3}}


if __name__ == '__main__':
    from quelle import ROOT
    a,b = [json.loads((ROOT/name).read_text()) for name in ('Frueher_Zugriff.json','Randpraeparation.json')]
    print(json.dumps(audit(a,b), indent=2, sort_keys=True))
