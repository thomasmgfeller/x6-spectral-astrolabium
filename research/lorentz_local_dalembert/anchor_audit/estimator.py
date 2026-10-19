"""Coordinate-blind balanced-first search; original pilot remains immutable."""
import math
import numpy as np
from common import core
from core import indices, invert_overlap


def eligible(g, a, b, cfg, reverse=False):
    succ, pred = g.bits(reverse)
    rows = []
    for c in indices(pred[a] & pred[b]):
        ac = succ[c] & pred[a]; bc = succ[c] & pred[b]
        na, nb, nc = ac.bit_count(), bc.bit_count(), (ac & bc).bit_count()
        if min(na, nb) >= cfg['overlap_min_interval']:
            rows.append((c, na, nb, nc))
    rows.sort(key=lambda q: (-min(q[1], q[2]), g.marks[q[0]]))
    return rows


def spatial_distance(g, a, b, rho, cfg, reverse=False):
    if a == b:
        return 0., {'status':'reference','anchors':0}
    succ, _ = g.bits(reverse)
    if (succ[a] >> b) & 1 or (succ[b] >> a) & 1:
        return None, {'status':'comparable','anchors':0}
    rows = eligible(g, a, b, cfg, reverse)
    valid = []; zero = one = outside = 0
    for rank, (c, na, nb, nc) in enumerate(rows):
        o = nc/min(na, nb)
        if o == 0: zero += 1; continue
        if o == 1: one += 1; continue
        if abs(na-nb) >= cfg['overlap_balance_prefactor']*math.sqrt((na+nb)*(1-o)):
            continue
        x = invert_overlap(o)
        if x is None: outside += 1; continue
        valid.append((rank, c, x))
    chosen = valid[:cfg['overlap_max_anchors']]
    distances = []
    if chosen:
        ta, tb = g.to(a, reverse), g.to(b, reverse)
        for rank, c, x in chosen:
            tau = cfg['alpha2']*rho**(-1/3)*(ta[c]+tb[c])/2
            distances.append(float(2*tau*x))
    return (float(np.median(distances)) if distances else None), {
        'status':'ok' if distances else 'no_balanced_anchor','anchors':len(chosen),
        'searched':len(rows),'balanced_total':len(valid),
        'eligible_beyond_original_cap':sum(rank>=cfg['overlap_max_anchors'] for rank,_,_ in valid),
        'first_valid_rank':valid[0][0]+1 if valid else None,
        'overlap_zero':zero,'overlap_one':one,'overlap_outside_table':outside}


# The original assembly is copied verbatim, except for dependency injection of
# the distance function. Controls compare this wrapper against the frozen core.
def neighborhood(g, rho, bottom, top, cfg, distance_function=spatial_distance):
    path = g.chain(bottom,top); middle = len(path)//2; root = path[middle]
    m = max(1,round(cfg['m_prefactor']*rho**cfg['m_exponent']))
    n = max(m+1,round(cfg['n_prefactor']*rho**cfg['n_exponent']))
    tn = cfg['alpha2']*rho**(-1/3)*n
    tm = cfg['alpha2']*rho**(-1/3)*m
    out = dict(root=root, chain=path, n=n, m=m, tau_n=tn, tau_m=tm, status='ok')
    if middle < n or len(path)-1-middle < n:
        return dict(out, status='short_chain')
    out['temporal'] = [path[middle-n],path[middle+n]]
    sides = []
    for reverse, shift in [(False,m),(True,-m)]:
        reference = path[middle+shift]
        levels = g.to(root, not reverse)
        shell = sorted(np.flatnonzero(levels==m).tolist(), key=lambda b:g.marks[b])
        estimates = []; diagnostics = []; selected = []
        for b in shell:
            distance, info = distance_function(g,reference,b,rho,cfg,reverse)
            estimates.append(distance); diagnostics.append(info)
            if distance is not None and distance <= cfg['radius_over_tau_m']*tm:
                selected.append(b)
        sides.append(dict(reference=reference,shell=shell,distances=estimates,
                          diagnostics=diagnostics,selected=selected))
    out['sides'] = sides
    if min(len(s['selected']) for s in sides) < cfg['minimum_neighborhood_population']:
        out['status'] = 'insufficient_neighborhood'
        return out
    c = cfg['coefficient_C']
    weights = {}
    for b in out['temporal']: weights[b] = weights.get(b,0.)-(c+3)/tn**2
    for side in sides:
        for b in side['selected']:
            weights[b] = weights.get(b,0.)+c/(len(side['selected'])*tm**2)
    out['support'] = sorted(weights, key=lambda b:g.marks[b])
    out['weights'] = [weights[b] for b in out['support']]
    return out

