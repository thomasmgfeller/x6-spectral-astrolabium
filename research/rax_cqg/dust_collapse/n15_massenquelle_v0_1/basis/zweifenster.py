"""Exact finite-model controls for a two-lobe mass reading on type 2324.

Uses Python 3.9+ standard library. Fractions bound the one algebraic scale.
Run with python3 -B massentest.py. No input files or network access.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import combinations, product
import json


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __add__(self, other):
        other = interval(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -interval(other)

    def __rsub__(self, other):
        return interval(other) - self

    def __mul__(self, other):
        other = interval(other)
        endpoints = [x*y for x,y in product((self.lo,self.hi),(other.lo,other.hi))]
        return Interval(min(endpoints), max(endpoints))

    __rmul__ = __mul__

    def __truediv__(self, other):
        divisor = interval(other)
        assert divisor.lo * divisor.hi > 0
        return self * Interval(1/divisor.hi, 1/divisor.lo)

    def __rtruediv__(self, other):
        return interval(other)/self


def interval(x):
    return x if isinstance(x, Interval) else Interval(Q(x), Q(x))


def decimal_bracket(x, digits=12):
    scale = 10**digits
    lower = x.lo*scale
    upper = x.hi*scale
    return [str(Q(lower.__floor__(),scale)), str(Q(upper.__ceil__(),scale))]


def delta_enclosure():
    # Delta^4=3/722. Strict bracketing is certified by integer powers.
    lo, hi = Q(1,4), Q(13,50)
    for _ in range(128):
        mid = (lo+hi)/2
        if mid**4 < Q(3,722):
            lo = mid
        else:
            hi = mid
    assert lo**4 < Q(3,722) <= hi**4
    return Interval(lo,hi)


PAST = (0,1,2,3)
INSIDE = (4,5,6,11,12,13,14)
FUTURE = (7,8,9,10)
ROUTE = (3,4,13,7)
LAYERS = (1,-9,16,-8)


def order_and_layers():
    inner = ((a,b) for j,(a,b) in enumerate(combinations(INSIDE,2)) if 2324 & (1<<j))
    rel = set(combinations(PAST,2)) | set(combinations(FUTURE,2)) | set(inner)
    rel.update(product(PAST,INSIDE+FUTURE))
    rel.update(product(INSIDE,FUTURE))
    assert all((a,c) in rel for a,b in rel for v,c in rel if b==v)
    counts = {(a,b):sum((a,v) in rel and (v,b) in rel for v in range(15)) for a,b in rel}
    assert all(counts[a,b]==0 for a,b in zip(ROUTE,ROUTE[1:]))
    coeff = {pair:LAYERS[n] if n<4 else 0 for pair,n in counts.items()}
    assert all(coeff[i,j]==0 for i,j in product(PAST,FUTURE))
    return rel,coeff


def read_action(rel,coeff,k,mass,e,empty_collar=False):
    # Clocks in units Delta, weights in units Delta. Keep weights fixed for shifts.
    assert Q(1,4)<k<Q(1,2)
    clocks = {i:Q(i-5) for i in PAST+FUTURE}
    clocks[3] += e
    u = {4:Q(1,2)-k,13:k}
    rest = [i for i in INSIDE if i not in u]
    u.update({i:Q(1,2)+Q(j,2*(len(rest)+1)) for j,i in enumerate(rest,1)})
    clocks.update({i:-2+e+(4-e)*u[i] for i in INSIDE})
    if abs(e) < 1:
        assert all(clocks[a]<clocks[b] for a,b in rel)
    fractions = (u[4]+u[13])/2, 1-(u[4]+u[13])/2
    assert fractions == (Q(1,4),Q(3,4))
    weights = dict.fromkeys(range(15),Q(0))
    if not empty_collar:
        weights.update(dict.fromkeys(PAST+FUTURE,Q(1,8)))
    weights[4],weights[13] = (mass*(4-e)*v for v in fractions)

    def action(shift):
        y = {i:v+shift if i in PAST else v for i,v in clocks.items()}
        return -sum(weights.values())/2-sum(
            b*weights[j]*(y[j]-y[i])**2 for (i,j),b in coeff.items()
        )/38

    shift = Q(2,13)
    return (action(-shift/2)-action(shift/2))/shift


def action_polynomial(rel,coeff,k,mass):
    h = Q(1,4)
    def at(e):
        return read_action(rel,coeff,k,mass,e)
    central, left, right = at(0), at(-h), at(h)
    a,b,c = central,(right-left)/(2*h),(right+left-2*central)/(2*h**2)
    # Independent of direct full-action evaluations: two occupied BD layer rows.
    assert (a,b,c)==tuple(mass*x/76 for x in (4*(1+12*k),-(93+24*k),23+3*k))
    for e in (Q(-2,7),Q(5,17)):
        assert a+b*e+c*e**2==at(e)
    return a,b,c


def moments(delta):
    lo,hi = Q(1,32),Q(3,32)
    def average(n):
        return (hi**(n+1)-lo**(n+1))/((n+1)*(hi-lo))
    assert average(1)==Q(1,16) and average(2)==Q(13,3072)
    return average(1)/delta, average(2)/(delta*delta)


def means(poly,mu,nu):
    a,b,c = poly
    return a-b*mu+c*nu, a+b*mu+c*nu


def evaluated():
    rel,coeff=order_and_layers()
    delta=delta_enclosure()
    mu,nu=moments(delta)
    assert [[coeff[i,j] for i in PAST] for j in (4,13)]==[[-8,16,-9,1],[0,-8,16,-9]]
    det=273*(16-nu)
    assert det.lo>0
    left_weight=76*((48+3*nu)/mu-24)/(2*det)
    right_weight=76*(-(48+3*nu)/mu-24)/(2*det)
    def infer(left,right):
        return left_weight*left + right_weight*right
    cases=[]
    for mass,k in product((Q(0),Q(1,4),Q(1,2),Q(19,20),Q(1)),(Q(1,3),Q(3,8),Q(2,5),Q(11,24))):
        left,right=means(action_polynomial(rel,coeff,k,mass),mu,nu)
        value=infer(left,right)
        assert value.lo<=mass<=value.hi and value.hi-value.lo<Q(1,10**34)
        cases.append({'M':str(mass),'k':str(k),'left':decimal_bracket(left),'right':decimal_bracket(right)})
    for empty in (False,True):
        assert read_action(rel,coeff,Q(1,3),Q(0),Q(1,4),empty)==0
    upper_weight = Q(3,4)*(4*delta+Q(3,32))
    lower_weight_at_four=3*(4*delta-Q(3,32))
    assert upper_weight.hi<1 and lower_weight_at_four.lo>1
    # Unequal profiles can defeat the readout with identical masses and channels.
    L,_=means(action_polynomial(rel,coeff,Q(1,3),Q(1)),mu,nu)
    _,R=means(action_polynomial(rel,coeff,Q(11,24),Q(1)),mu,nu)
    biased=infer(L,R)
    assert biased.hi<Q(98,100)
    # Stronger: solve exactly, side by side, for equal observable channel means
    # at different masses. Interval arithmetic proves admissibility of the solution.
    M2=Q(19,20)
    counter={}
    for sign,name in ((1,'left'),(-1,'right')):
        a=4+23*nu+sign*93*mu
        b=48+3*nu+sign*24*mu
        assert b.lo>0
        k2=((a+b*Q(3,8))/M2-a)/b
        assert Q(1,4)<k2.lo<=k2.hi<Q(1,2)
        counter[name]=decimal_bracket(k2)
    assert M2*Q(102,100)<Q(98,100)
    return {
      'source_commit':'83b8a71bb96f2d794ecc35909f8102c20901f7f6',
      'type':2324,'route':list(ROUTE),'cases_checked':cases,
      'coefficients_on_p_left_right':[decimal_bracket(left_weight),decimal_bracket(right_weight)],
      'max_abs_error_gain_if_equal_lobe_error_bounds':decimal_bracket(left_weight-right_weight),
      'same_k_across_lobes':'EXACT_TAGGED_MODEL_IDENTITY',
      'density_cap_max_at_M1':decimal_bracket(upper_weight),
      'density_cap_min_on_vertex_13_at_M4':decimal_bracket(lower_weight_at_four),
      'M1_different_k_mass_readout':decimal_bracket(biased),
      'identical_two_channel_counterexample':{'first_mass':'1','first_k_both':'3/8',
          'second_mass':'19/20','second_k_bounds':counter,'two_2pct_bands_disjoint':True},
      'vacuum':'PASS_ALGEBRAIC_ONLY','physical_P3':'HOLD_NOT_ELIGIBLE / NOT_RUN'}


if __name__=='__main__':
    if not __debug__:
        raise RuntimeError('Please run without -O.')
    print(json.dumps(evaluated(),indent=2,ensure_ascii=False))
