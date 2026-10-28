"""Analytic time integration, enclosed equal-volume ball coordinates.

All arrival and coefficient intervals are outward dyadic integer intervals.
Sorting lower and upper arrival endpoints encloses every order statistic,
including crossing/tied arrivals. Signed differences are never made positive.
"""
import hashlib
import itertools
import json
import time
from common10 import arb, ctx, check, endpoints, ball

ARRIVAL_BITS = 80
WEIGHT_BITS = 100
GEOMETRY_BITS = 256


def sector(n, i, j, k):
    """A Cartesian enclosure of one equal-volume spherical sector.

    u in [0,1], v in [-1,1], w in [0,1]; r=u^(1/3)/2,
    z=3/2+r*v, x+i*y=r*sqrt(1-v^2)*exp(2*pi*i*w).
    Its normalized spatial measure is exactly 1/n^3.
    """
    with ctx.workprec(GEOMETRY_BITS):
        rlo, rhi = (arb(i) / n).root(3) / 2, (arb(i + 1) / n).root(3) / 2
        r = rlo.union(rhi)
        v = (arb(2*j) / n - 1).union(arb(2*(j+1)) / n - 1)
        # Explicit nonnegative bounds avoid interval sqrt at a polar endpoint.
        amin = arb(0) if v.contains(0) else abs(v).lower()
        amax = abs(v).upper().min(arb(1))
        slo = (1 - amax**2).nonnegative_part().sqrt()
        shi = (1 - amin**2).nonnegative_part().sqrt()
        s = slo.union(shi)
        angle = (2*arb.pi()*k/n).union(2*arb.pi()*(k+1)/n)
        xyz = [r*s*angle.cos(), r*s*angle.sin(), arb('3/2')+r*v]
        return [endpoints(z, ARRIVAL_BITS) for z in xyz]


def arrivals(x, box):
    """Enclose t_y+distance(x,y) for every spatial point in a sector."""
    with ctx.workprec(GEOMETRY_BITS):
        out = []
        for row in x:
            dmin = arb(0); dmax = arb(0)
            for value, (lo, hi) in zip(row[1:], box):
                a, b, p = arb(lo)/(1<<ARRIVAL_BITS), arb(hi)/(1<<ARRIVAL_BITS), arb(float(value))
                near = a-p if p<a else p-b if p>b else arb(0)
                far = abs(a-p).max(abs(b-p))
                dmin += near**2; dmax += far**2
            low = endpoints(arb(float(row[0]))+dmin.nonnegative_part().sqrt(), ARRIVAL_BITS)[0]
            high = endpoints(arb(float(row[0]))+dmax.nonnegative_part().sqrt(), ARRIVAL_BITS)[1]
            out.append((low,high))
        return out


def product(a, b):
    values = [x*y for x in a for y in b]
    return min(values), max(values)


def prepare(table, counts):
    weights = [endpoints(z, WEIGHT_BITS) for z in table]
    # Differences are evaluated before integer quantization.
    differences = [endpoints(table[k]-table[k-1], WEIGHT_BITS) for k in range(1,len(table))]
    successors = [[int(i) for i in range(len(counts)) if counts[i,j] >= 0] for j in range(len(counts))]
    return weights[0], differences, successors


def time_coefficients(arrival, prepared, window):
    """Unnormalized integral for each query coefficient, exponent 180."""
    first, differences, successors = prepared
    scale = 1 << ARRIVAL_BITS
    a, b = [int((arb(v)*scale).unique_fmpz()) for v in window]
    duration = b-a
    def remaining(t):
        return max(0, min(duration,b-t))
    out=[]
    for y, future in enumerate(successors):
        low = sorted(arrival[z][0] for z in future)
        high = sorted(arrival[z][1] for z in future)
        lo, hi = product(first, (remaining(arrival[y][1]), remaining(arrival[y][0])))
        for k, (l, h) in enumerate(zip(low,high)):
            if l >= b:
                break
            dl, dh = product(differences[k], (remaining(h),remaining(l)))
            lo += dl; hi += dh
        out.append((lo,hi))
    return out


def integrate(x, counts, table, windows, grids, progress=None, deadline=None):
    prepared = prepare(table,counts)
    previous = None
    levels=[]
    for n in grids:
        totals = [[[0,0] for _ in x] for _ in windows]
        identity=hashlib.sha256()
        for i,j,k in itertools.product(range(n),repeat=3):
            if deadline is not None and time.monotonic()>deadline:
                raise TimeoutError('predeclared integration process budget')
            box = sector(n,i,j,k)
            arrival = arrivals(x,box)
            identity.update(json.dumps([i,j,k,box,arrival],separators=(',',':')).encode())
            for w,window in enumerate(windows):
                for dest,(lo,hi) in zip(totals[w],time_coefficients(arrival,prepared,window)):
                    dest[0]+=lo;dest[1]+=hi
        q=[]
        for w,window in enumerate(windows):
            duration=arb(window[1])-arb(window[0])
            q.append([ball(lo,hi,ARRIVAL_BITS+WEIGHT_BITS)/(n**3*duration) for lo,hi in totals[w]])
            if previous is not None:
                q[w]=[a.intersection(b) for a,b in zip(q[w],previous[w])]
        levels.append({'n':n,'sectors':n**3,'geometry_sha256':identity.hexdigest(),'q':q})
        previous=q
        if progress: progress(n)
    return levels
