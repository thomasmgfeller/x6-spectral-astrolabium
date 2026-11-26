"""Exact canonical local memories, initial conditions, probe readout and endpoint constraint."""
from fractions import Fraction as F
from math import erf, sqrt
from itertools import combinations
import json
from vorstudie import inputs, ROOT

SOURCE, POINTER = 'A', 'D'


def labels(bg):
    return [*sorted(set(bg.nodes)-bg.past), SOURCE, POINTER]


def topological(bg, backwards_ties=False):
    return sorted(set(bg.nodes)-bg.past, key=lambda j: (
        sum(k == j for _, k in bg.relation), -j if backwards_ties else j))


def eye(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def add_row(target, control, strength):
    return [v + strength * w for v, w in zip(target, control, strict=True)]


def apply_gate(q, p, ids, gate):
    control, target, strength = gate
    i, j = ids[control], ids[target]
    assert i != j
    q[j] = add_row(q[j], q[i], strength)
    p[i] = add_row(p[i], p[j], -strength)


def blocks(bg, b, source, receiver, transmit, listen):
    dynamical = sorted(set(bg.nodes)-bg.past)
    out = {}
    for j in dynamical:
        row = [(i, j, b[j][i]) for i in dynamical if (i,j) in bg.relation and b[j][i]]
        if j == source and transmit:
            row.append((SOURCE, j, -1))
        if j == receiver and listen:
            row.append((j, POINTER, 1))
        out[j] = row
    return out


def circuit(bg, gates, receiver, order):
    modes = labels(bg)
    ids = {key: i for i, key in enumerate(modes)}
    q, p = eye(len(modes)), eye(len(modes))
    for j in order:
        for gate in gates[j]:
            apply_gate(q, p, ids, gate)
        if j == receiver:
            at_read = q[ids[POINTER]].copy()
    assert q[ids[POINTER]] == at_read
    return q, p


def dot(a, b):
    return sum(x*y for x,y in zip(a,b,strict=True))


def symplectic(q, p):
    return [[dot(r, s) for s in p] for r in q] == eye(len(q))


def bands(mu, var):
    def cdf(x):
        return (1 + erf((x-float(mu)) / sqrt(2*float(var)))) / 2
    left, upto = cdf(-1), cdf(1)
    return [format(v,'.10f') for v in (left, upto-left, 1-upto)]


def sparse(modes, row):
    return {str(key): v for key, v in zip(modes, row) if v}


def moments(bg, q, centre):
    modes = labels(bg)
    row = q[modes.index(POINTER)]
    mu = F(centre * row[modes.index(SOURCE)])
    var = sum(coef*coef*(F(1) if mode in (SOURCE, POINTER) else F(1,2))
              for mode, coef in zip(modes, row))
    return {'mean': str(mu), 'variance': str(var), 'record_row': sparse(modes,row),
            'p_left_middle_right': bands(mu,var)}


def endpoint(bg, h, z, r):
    future = {i for a,i in bg.relation if a == z}
    assert (future | {z}) - bg.future == {r,z}
    h0, = [i for i in bg.inner if bg.weights[i] == (0,0) and
           (i,r) in bg.relation and (i,z) not in bg.relation and (z,i) not in bg.relation]
    u, = [i for i in bg.inner if bg.weights[i] == (0,0) and (i,z) in bg.relation]
    cols = [z, r]
    unchanged = sorted(set(bg.inner)-set(cols))
    response = [[h[i][j] for j in cols] for i in (u,h0)]
    (a,b),(c,d) = response
    minor = a*d-b*c
    assert minor and all(not any(h[i][j] for j in cols) for i in unchanged if i not in (u,h0))
    extended = [*cols,*sorted(bg.future)]
    assert [h[z][j] for j in extended] == [h[h0][j] for j in extended]
    # Force j_z=1. With a free receiver reaction, minimise non-endpoint sources.
    phi_r = F(1)/h[z][r]
    assert h[z][z] == 0 and h[h0][z] == 0
    def source_for(phi_z):
        return {str(i):str(val) for i in bg.inner if (val := h[i][z]*phi_z+h[i][r]*phi_r)}
    cancel_u = -b*phi_r/a
    cancel_r = -h[r][r]*phi_r/h[r][z]
    return {'unforced_rows':[u,h0], 'support':cols,
            'two_rows':[[str(v) for v in row] for row in response],
            'minor':str(minor), 'null_dimension_on_two_endpoints':0,
            'columns_future_free':extended,'twin_rows':[z,h0],
            'common_row':[str(h[z][j]) for j in extended],
            'with_receiver_reaction':{'field':[str(cancel_u),str(phi_r)],'source':source_for(cancel_u)},
            'without_receiver_reaction':{'field':[str(cancel_r),str(phi_r)],'source':source_for(cancel_r)}}


def arms(bg, z, r):
    later, = [j for j in bg.future if (r,j) in bg.relation and
              not any((k,j) in bg.relation for k in bg.future)]
    return {'off':(z,r,False,True,1), 'on':(z,r,True,True,1),
            'negative':(z,r,True,True,-1),'active_zero':(z,r,True,True,0),
            'late':(later,r,True,True,1),'reversed':(r,z,True,True,1),
            'reversed_off':(r,z,False,True,1),'disconnected':(z,r,True,False,1)}


def analyse(bg, select, matrices):
    z,r = select(bg)
    b,h=matrices
    modes=labels(bg); ids={k:i for i,k in enumerate(modes)}
    spec=json.loads((ROOT/'basis/Zeigervertrag.json').read_bytes())['selected_candidate']['reference_apparatus']
    assert spec == {'g':1,'sigma':1,'middle_bin':[-1,1]}
    results={}
    for key,(src,rec,transmit,listen,centre) in arms(bg,z,r).items():
        gates=blocks(bg,b,src,rec,transmit,listen)
        q,p=circuit(bg,gates,rec,topological(bg))
        assert symplectic(q,p)
        assert (q,p)==circuit(bg,gates,rec,topological(bg,True))
        results[key]=moments(bg,q,centre)
        results[key]['source_event']=src;results[key]['read_event']=rec
        if key=='on':
            kick=sparse(modes,p[ids[SOURCE]])
            receiver_kick=p[ids[rec]][ids[POINTER]]
            late_transfer={str(j):q[ids[j]][ids[SOURCE]] for j in sorted(bg.future)}
            # Incomparable blocks commute gate by gate, including probe kicks.
            pairs=[(i,j) for i,j in combinations(topological(bg),2)
                   if (i,j) not in bg.relation and (j,i) not in bg.relation]
            for i,j in pairs:
                assert all(a != d and c != t for a,t,_ in gates[i] for c,d,_ in gates[j])
    for key in ('mean','variance','record_row','p_left_middle_right'):
        assert results['late'][key] == results['off'][key]
        assert results['reversed'][key] == results['reversed_off'][key]
    return {'source':z,'receiver':r,'past_inputs_zero':sorted(bg.past),'canonical_modes':len(modes),
            'endpoint':endpoint(bg,h,z,r),'arms':results,'on_future_mean_changes':late_transfer,
            'source_final_momentum_row':kick,'receiver_momentum_pointer_coefficient':receiver_kick,
            'incomparable_event_blocks':len(pairs),'P3':{'NOT_RUN':60}}


if __name__ == '__main__':
    with inputs() as (bg,sel,mat,ref):
        print(json.dumps(analyse(bg,sel,mat),sort_keys=True,indent=2))
