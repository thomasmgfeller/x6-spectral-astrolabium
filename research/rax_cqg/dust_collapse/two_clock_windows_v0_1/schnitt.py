"""Zwei Uhrfenster der reduzierten AA-Auslese und des offenen Präfixmodells."""
import argparse
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
sys.path.insert(0, str(ROOT.parent))

from zero_one_pairing_v0_1 import schranken as bounds
from m1_pilot_clock_v0_1.uhrtest import exp_minus_interval

ZERO = (F(0), F(0))
ONE = (F(1), F(1))


def check_sources():
    manifest = json.loads((ROOT/'quellen.json').read_text())
    for source in manifest['files'].values():
        name = source['path']
        data = (REPO / name).read_bytes()
        git = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if git != source['git_blob']:
            raise ValueError(name)
    return manifest['commit']


def subtract(x, y):
    return bounds.plus(x, bounds.scale(-1, y))


def divide(x, y):
    if y[0] <= 0:
        raise ArithmeticError('Nenner ohne positive Untergrenze')
    return bounds.times(x, (1/y[1], 1/y[0]))


def clock_vector(a, b):
    def integral(p, t):
        return [bounds.scale(t, z) for z in bounds.dust_mean(p, t)]
    return [[subtract(x, y) for x, y in zip(integral(p, b), integral(p, a))] for p in (1, 2)]


def length_weights(t):
    common = bounds.scale(F(2,81), bounds.times(bounds.PI, bounds.root(1+bounds.B2)))
    oblique = bounds.root(F(1370,841*t*t+529))
    return (bounds.times(common, bounds.scale(4, bounds.root(F(9,12871)))),
            bounds.times(common, bounds.plus(bounds.root(F(9,1423450)),
                              bounds.scale(2,bounds.times(oblique,bounds.root(F(9,69185)))))))


def pairing(left, right, weights):
    real = imag = ZERO
    for (x,y),(u,v),w in zip(left,right,weights):
        real = bounds.plus(real, bounds.times(w, bounds.plus(bounds.times(x,u),bounds.times(y,v))))
        imag = bounds.plus(imag, bounds.times(w, subtract(bounds.times(x,v),bounds.times(y,u))))
    return real, imag


def fmt(x):
    return bounds.decimal_bounds(x, places=14)


def cut(a, c, b, t):
    left, right = clock_vector(a,c), clock_vector(c,b)
    w = length_weights(t)
    ll = pairing(left,left,w)[0]
    rr = pairing(right,right,w)[0]
    re, im = pairing(left,right,w)
    both = pairing(clock_vector(a,b),clock_vector(a,b),w)[0]
    residual = subtract(both, bounds.plus(bounds.plus(ll,rr),bounds.scale(2,re)))
    if not residual[0]<=0<=residual[1] or re[0]<=0:
        raise ArithmeticError('Zusammensetzung')
    mod2 = bounds.plus(bounds.square(re),bounds.square(im))
    denom = bounds.times(ll,rr)
    eta2 = divide(mod2,denom)
    determinant = subtract(denom,mod2)
    if determinant[0]<=0:
        raise ArithmeticError('Zwei zeitlich unabhängige Antworten nicht zertifiziert')
    return dict(left=fmt(ll),right=fmt(rr),real_cross=fmt(re),imag_cross=fmt(im),
                total=fmt(both),interference_share=fmt(divide(bounds.scale(2,re),both)),
                normalized_overlap_squared=fmt(eta2),
                gram_determinant=bounds.decimal_bounds(determinant,places=25))


def reference_clock():
    d=F(1,8)
    output={}
    for beta in (F(5,4),F(4,3)):
        def h0(t): return bounds.plus(exp_minus_interval(t),bounds.scale((1-beta)*t,ONE))
        def h1(t): return bounds.plus(exp_minus_interval(t),bounds.scale(beta-1,ONE))
        checks=0
        for k in range(1,16):
            c=d*k/16
            # Telescope empty -> one -> one; empty -> empty -> one.
            early=bounds.times(bounds.scale(c,h1(c)),divide(h1(d),h1(c)))
            late=bounds.times(h0(c),divide(bounds.scale(d-c,h1(d)),h0(c)))
            for actual, exact in ((early,bounds.scale(c,h1(d))), (late,bounds.scale(d-c,h1(d)))):
                diff=subtract(actual,exact)
                if not diff[0]<=0<=diff[1]:
                    raise ArithmeticError('Präfixverklebung')
                checks+=1
        output[str(beta)]=dict(P0=fmt(h0(d)), P1=fmt(bounds.scale(d,h1(d))),
                               P_early_and_one=fmt(bounds.scale(d/2,h1(d))),
                               P_late_and_one=fmt(bounds.scale(d/2,h1(d))),
                               conditional_half='1/2',initial_hazard=str(beta),checked_branches=checks)
    return output


def calculate():
    commit=check_sources()
    d=F(1,8)
    cuts={str(t):{str(frac):cut(F(0),frac*d,d,t) for frac in (F(1,3),F(1,2),F(2,3))}
          for t in (1,4)}
    prior=json.loads((ROOT.parent/'zero_one_pairing_v0_1/ergebnis.json').read_text())
    for t,rows in cuts.items():
        lo,hi=map(F,rows['1/2']['total'])
        l,h=map(F,prior['certified']['1/8'][t]['ratio'])
        if max(lo,l)>min(hi,h):
            raise ArithmeticError('Quotient aus PR 309')
    return dict(commit=commit,window='1/8',length_products=cuts,
                open_clock=reference_clock(),rank_complex_at_most=2,rank_real_at_most=4,
                three_bin_complex_coherence_bound='1/2',five_bin_real_coherence_bound='1/4',
                physical_birth_rate='HOLD',P3_new_physical_histories=0)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    args.out.write_text(json.dumps(calculate(),sort_keys=True,indent=2)+'\n')
