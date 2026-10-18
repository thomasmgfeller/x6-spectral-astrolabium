"""Coordinate-blind marked-poset inference. No simulator import is permitted."""
import ctypes
import functools
import hashlib
import math
from pathlib import Path
import subprocess
import tempfile

import numpy as np
from numpy.polynomial.legendre import leggauss

HERE = Path(__file__).resolve().parent
VOLUME = math.pi / 12


@functools.lru_cache(None)
def kernel():
    src = HERE / 'longest.cpp'
    digest = hashlib.sha256(src.read_bytes()).hexdigest()[:16]
    lib = Path(tempfile.gettempdir()) / ('x6-bk-longest-' + digest + '.so')
    if not lib.exists():
        subprocess.run(['g++', '-O2', '-std=c++17', '-shared', '-fPIC', str(src), '-o', str(lib)], check=True)
    fn = ctypes.CDLL(str(lib)).longest_to
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int,
                   ctypes.c_int, ctypes.c_void_p]
    fn.restype = None
    return fn


def indices(bits):
    while bits:
        low = bits & -bits
        yield low.bit_length() - 1
        bits ^= low


class Poset:
    def __init__(self, relation, marks):
        self.r = np.ascontiguousarray(relation, dtype=np.uint8)
        self.marks = np.asarray(marks, dtype=float)
        self.size = len(self.r)
        if self.r.shape != (self.size, self.size) or len(self.marks) != self.size:
            raise ValueError('relation/mark shape')
        if np.any(np.diag(self.r)) or not np.isfinite(self.marks).all() or len(set(self.marks)) != self.size:
            raise ValueError('strict relation and distinct finite marks required')
        self.order = np.ascontiguousarray(np.lexsort((self.marks, self.r.sum(axis=0))), dtype=np.int32)
        rank = np.empty(self.size, int); rank[self.order] = np.arange(self.size)
        # Check acyclicity/topological ordering, not a cubic transitivity test.
        for i in range(self.size):
            if np.any(rank[np.flatnonzero(self.r[i])] <= rank[i]):
                raise ValueError('not a topologically ordered strict partial order')
        self.succ = [int.from_bytes(x.tobytes(), 'little') for x in np.packbits(self.r, axis=1, bitorder='little')]
        self.pred = [int.from_bytes(x.tobytes(), 'little') for x in np.packbits(self.r.T, axis=1, bitorder='little')]
        self.cache = {}

    def to(self, target, reverse=False):
        key = (int(target), bool(reverse))
        if key not in self.cache:
            out = np.empty(self.size, np.int32)
            kernel()(self.r.ctypes.data, self.order.ctypes.data, self.size, int(target), int(reverse), out.ctypes.data)
            self.cache[key] = out
        return self.cache[key]

    def bits(self, reverse=False):
        return (self.pred, self.succ) if reverse else (self.succ, self.pred)

    def chain(self, bottom, top):
        d = self.to(top)
        if d[bottom] < 0:
            raise ValueError('unrelated endpoints')
        path = [int(bottom)]
        while path[-1] != top:
            a = path[-1]
            candidates = [b for b in indices(self.succ[a]) if d[b] == d[a]-1]
            path.append(min(candidates, key=lambda b: self.marks[b]))
        return path

    def interval(self, a, b):
        return (self.succ[a] & self.pred[b]).bit_count()


def overlap_function(x, quadrature=64):
    """2+1 overlap, x=l/(2*tau); deterministic Gauss quadrature of Eq.49."""
    x = np.atleast_1d(np.asarray(x, float))[:, None, None]
    u, w = leggauss(quadrature)
    theta = (u+1)*math.pi/4
    radial = (u+1)/2
    t = np.sqrt(1+x*x)
    bound = 1/(2*(t+x*np.cos(theta)[None, :, None]))
    r = bound*radial[None, None, :]
    integrand = r*(t-r-np.sqrt(r*r+x*x+2*x*r*np.cos(theta)[None, :, None]))
    return (48/math.pi*np.sum(integrand*bound*w[None, :, None]*math.pi/4*w[None, None, :]/2, axis=(1,2)))


@functools.lru_cache(None)
def overlap_table():
    x = np.r_[np.linspace(0, 1, 1001), np.geomspace(1.002, 16, 1000)]
    y = np.concatenate([overlap_function(c) for c in np.array_split(x, 32)])
    if not np.all(np.diff(y) < 0) or abs(y[0]-1)>1e-10:
        raise ArithmeticError('overlap quadrature invalid')
    return x, y


def invert_overlap(o):
    x, y = overlap_table()
    if not y[-1] <= o < 1:
        return None
    return float(np.interp(o, y[::-1], x[::-1]))


def spatial_distance(g, a, b, rho, cfg, reverse=False):
    if a == b:
        return 0., {'status':'reference', 'anchors':0}
    succ, pred = g.bits(reverse)
    if (succ[a] >> b) & 1 or (succ[b] >> a) & 1:
        return None, {'status':'comparable', 'anchors':0}
    candidates = []
    for c in indices(pred[a] & pred[b]):
        ac = succ[c] & pred[a]; bc = succ[c] & pred[b]
        na, nb, nc = ac.bit_count(), bc.bit_count(), (ac & bc).bit_count()
        if min(na,nb) >= cfg['overlap_min_interval']:
            candidates.append((c, na, nb, nc))
    candidates.sort(key=lambda q: (-min(q[1],q[2]), g.marks[q[0]]))
    candidates = candidates[:cfg['overlap_max_anchors']]
    distances = []; zero = one = 0
    for c,na,nb,nc in candidates:
        o = nc/min(na,nb)
        if o == 0: zero += 1; continue
        if o == 1: one += 1; continue
        if abs(na-nb) >= cfg['overlap_balance_prefactor']*math.sqrt((na+nb)*(1-o)):
            continue
        x = invert_overlap(o)
        if x is None: continue
        tau = cfg['alpha2']*rho**(-1/3)*(g.to(a,reverse)[c]+g.to(b,reverse)[c])/2
        distances.append(float(2*tau*x))
    return (float(np.median(distances)) if distances else None), {
        'status':'ok' if distances else 'no_balanced_anchor', 'anchors':len(distances),
        'searched':len(candidates), 'overlap_zero':zero, 'overlap_one':one}


def neighborhood(g, rho, bottom, top, cfg):
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
            distance, info = spatial_distance(g,reference,b,rho,cfg,reverse)
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


def apply(stencil, values):
    f = np.asarray(values)
    return np.tensordot(stencil['weights'], f[stencil['support']]-f[stencil['root']], axes=(0,0))


def metric(stencil, fields):
    x = np.asarray(fields); origin = x[stencil['root']]
    bx = apply(stencil,x)
    result = np.empty((x.shape[1],x.shape[1]))
    for i in range(x.shape[1]):
        for j in range(x.shape[1]):
            result[i,j] = (apply(stencil,x[:,i]*x[:,j])-origin[i]*bx[j]-origin[j]*bx[i])/2
    return result


def metric_outer(stencil,fields):
    dx = fields[stencil['support']]-fields[stencil['root']]
    return np.einsum('n,ni,nj->ij',stencil['weights'],dx,dx)/2


def independent_columns(matrix, marks, count=3):
    residual = np.asarray(matrix,float).copy(); chosen = []
    for _ in range(count):
        norms = np.sum(residual**2,axis=0)
        if chosen: norms[chosen] = -1
        j = max(range(len(norms)),key=lambda i:(norms[i],-marks[i]))
        if norms[j] < 1e-20: return None
        chosen.append(j)
        direction = residual[:,j]/math.sqrt(norms[j])
        residual -= np.outer(direction,direction@residual)
    return chosen


def intrinsic_chart(g, stencil, rho, bottom, cfg):
    support = [stencil['root']]+stencil['support']
    common = (1<<g.size)-1
    for b in support: common &= g.pred[b]
    candidates = [a for a in indices(common) if a != bottom and
                  min(g.interval(a,b) for b in support)>=cfg['chart_min_interval']]
    candidates.sort(key=lambda a:g.marks[a])
    candidates = candidates[:cfg['chart_max_candidates']]
    if len(candidates)<3: return dict(status='insufficient_landmarks')
    scale = 2*stencil['tau_n']
    base = np.array([(g.interval(bottom,b)/(rho*VOLUME))**(2/3) for b in support])
    columns = np.array([[(g.interval(a,b)/(rho*VOLUME))**(2/3) for b in support] for a in candidates]).T
    columns = (base[:,None]-columns)/scale
    columns -= columns[0].copy()
    pivot = independent_columns(columns,np.array([g.marks[a] for a in candidates]))
    if pivot is None: return dict(status='rank_deficient_fields')
    fields = np.zeros((g.size,3))
    fields[support] = columns[:,pivot]
    return dict(status='ok',landmarks=[bottom]+[candidates[j] for j in pivot],fields=fields)
