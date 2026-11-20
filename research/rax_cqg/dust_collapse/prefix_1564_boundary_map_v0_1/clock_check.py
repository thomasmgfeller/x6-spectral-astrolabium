"""Compare marked event removal with an independently ordered quadrature on each end type."""
from functools import lru_cache
from unittest.mock import patch
import numpy as np

I = (4,5,6,11,12,13)
P, F = tuple(range(4)), tuple(range(7,11))
BETA = 4/np.sqrt(6.)
STEP = np.sqrt(2/(19*BETA))


@lru_cache(None)
def gauss(n):
    nodes,weights = np.polynomial.legendre.leggauss(n)
    return nodes,weights/2


def row(k,b,t):
    return 1+BETA/2*sum(w*(t[k]-t[i])**2 for (i,j),w in b.items() if k==j and w)


def D(c):
    # 1/2 delta_0 + 1/2 uniform[0,1], integrated with exp(-i rho C/2).
    return (1+np.exp(-.25j*c)*np.sinc(c/(4*np.pi)))/2


def collar_times(t):
    return {**{i:(i-5)*STEP for i in (*P,*F)},3:t}


def marked_sample(b,gravity,outer,n):
    x,w = gauss(n)
    times = collar_times(outer)
    for a,i in enumerate(I[:-1]):
        shape = [1]*5
        shape[a] = n
        times[i] = (1.5*x).reshape(shape)
    past = sum(row(i,b,times) for i in P)
    accumulated = np.zeros([n]*5,dtype=complex)
    for s,ws in zip(1.5*x,w):
        times[13] = s
        fine = np.exp(-1j*sum(row(i,b,times) for i in F)/16)*D(row(13,b,times))
        for i in I[:-1]:
            fine = fine*D(row(i,b,times))
        accumulated += ws*fine
    for _ in I[:-1]:
        accumulated = np.tensordot(w,accumulated,axes=(0,0))
    return past,np.exp(1j*gravity)*accumulated


def marked_lobes(b,gravity,n,m):
    x,w = gauss(m)
    answer = np.zeros((2,2),dtype=complex)
    for col,side in enumerate((-1,1)):
        points = -2*STEP + side/16 + x/32
        past,values = zip(*(marked_sample(b,gravity,t,n) for t in points))
        past = np.asarray(past)
        for d,r in enumerate((1/8,1/4)):
            initial = np.exp(-.5j*r*past)*np.sinc(past/(64*np.pi))
            answer[d,col] = np.sqrt(1/48/32)*np.dot(w,initial*values)
    return answer


def fixed_old_fields(b,bp,fg,pg,n):
    # Compare at a point of the support, before averaging over the old densities.
    s,ws = gauss(n)
    r,wr = gauss(96)
    r = (1+r)/2
    old = collar_times(-2*STEP+1/16)
    old.update(dict(zip(I[:-1],[-.7,.4,-.1,1.15,-1.2])))
    rho = dict.fromkeys(P,1/8)
    rho.update(dict.fromkeys(F,1/8))
    rho.update(dict(zip(I[:-1],[0.,.3,.7,0.,.5])))
    parent_sum = sum(rho[k]*row(k,bp,old) for k in rho)
    fine = {**old,13:1.5*s}
    new_row = row(13,b,fine)
    retained_sum = sum(rho[k]*row(k,b,fine) for k in rho)
    raw_density = (1+np.exp(-.5j*np.outer(new_row,r))@wr)/2
    fine_direct = np.dot(ws, np.exp(1j*fg-.5j*retained_sum)*raw_density)
    influence = np.exp(1j*(fg-pg))*np.dot(ws,D(new_row)*np.exp(-.5j*(retained_sum-parent_sum)))
    return influence,abs(np.exp(1j*pg-.5j*parent_sum)*influence-fine_direct)


def check_clocks(cases,make,scalar):
    import clock_network as reference
    _,bp,gp = make(1564,5)
    refs = {}
    maxima = []
    bulk_error = 0.
    sample = {}
    for n,m in ((3,3),(5,4)):
        largest = 0.
        with patch.object(reference,'layout',scalar.layout):
            for end,code,_ in cases:
                _,b,gravity = make(code,6)
                key = (end,n,m)
                if key not in refs:
                    refs[key] = reference.packet((6,end),n,m)[0]
                obs = marked_lobes(b,gravity,n,m)
                largest = max(largest,float(np.max(np.abs(obs-refs[key]))))
                if n==5:
                    value,err = fixed_old_fields(b,bp,gravity,gp,64)
                    bulk_error = max(bulk_error,float(err))
                    if end in (1790,5374):
                        sample[str(end)] = [float(value.real),float(value.imag)]
        assert largest < 1e-13
        maxima.append(dict(inner_points=n,outer_points=m,max_complex_lobe_difference=largest))
    assert bulk_error < 1e-13
    return dict(marked_paths=16,comparison_grids=maxima,outer_density_centres=['1/8','1/4'],
                preparations='both original lobes separately; coherent equal-weight packet follows by linearity',
                fixed_old_fields_max_complex_difference=bulk_error,example_influence_at_fixed_fields=sample,
                scope='same-grid reordering checks; no continuum error bound inferred')
