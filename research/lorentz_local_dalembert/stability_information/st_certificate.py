"""Exact rational/interval certificate for the strongest archived SMALL_PAIR.

Post-search diagnostic selection; the frozen 25% success threshold is unchanged.
No optimizer or floating-point equality is trusted as a mathematical certificate.
SPDX-License-Identifier: Apache-2.0
"""
import argparse
import hashlib
import math
from fractions import Fraction as F
import numpy as np
from st_common import HERE, read, save, frozen, input_mask
from st_model import Stability


def outward(lo, hi=None, digits=20):
    """Decimal rational strings enclosing an interval, with directed rounding."""
    hi = lo if hi is None else hi
    t = 10**digits
    a = lo.numerator*t//lo.denominator
    b = -((-hi.numerator*t)//hi.denominator)
    def decimal(k):
        sign = '-' if k < 0 else ''
        k = abs(k)
        return f'{sign}{k//t}.{k%t:0{digits}d}'
    return [decimal(a), decimal(b)]


def sqrt_bounds(q, digits=65):
    assert q >= 0
    t = 10**digits
    a = math.isqrt(q.numerator*t*t//q.denominator)
    return F(a, t), F(a+1, t)


def pi_bounds():
    # Alternating Taylor series, then the exact Machin identity.
    def atan_reciprocal(n):
        total = F(0)
        for k in range(200):
            term = F((-1)**k, (2*k+1)*n**(2*k+1))
            total += term
            nxt = F((-1)**(k+1), (2*k+3)*n**(2*k+3))
            if abs(nxt) < F(1, 10**75):
                return min(total, total+nxt), max(total, total+nxt)
        raise AssertionError('atan series budget')
    a, b = atan_reciprocal(5)
    c, d = atan_reciprocal(239)
    return tuple(map(F, outward(16*a-4*d, 16*b-4*c, 70)))


def solve(matrix, rhs):
    a = [[F(v) for v in row]+[F(b)] for row, b in zip(matrix, rhs)]
    n = len(a)
    for k in range(n):
        pivot = next(i for i in range(k, n) if a[i][k])
        a[k], a[pivot] = a[pivot], a[k]
        p = a[k][k]
        a[k] = [v/p for v in a[k]]
        for i in range(n):
            if i != k:
                p = a[i][k]
                a[i] = [v-p*w for v, w in zip(a[i], a[k])]
    return [row[-1] for row in a]


def exact_weights(z, scale):
    y = [[a-b for a, b in zip(row, z[4])] for row in z[5:]]
    D = list(map(list, zip(*[[t,x,y,t*t,x*x,y*y,t*x,t*y,x*y] for t,x,y in y])))
    n = len(z)-5
    sums = [sum(row) for row in D]
    S = [[sum(a*b for a,b in zip(ri,rj))-si*sj/(n+1)
          for rj,sj in zip(D,sums)] for ri,si in zip(D,sums)]
    b = [0,0,0,-2,2,2,0,0,0]
    lam = solve(S,b)  # Invertibility proves full moment rank.
    a = [sum(D[i][j]*lam[i] for i in range(9)) for j in range(n)]
    correction = sum(a)/(n+1)
    a = [v-correction for v in a]
    assert [sum(x*y for x,y in zip(row,a)) for row in D] == b
    assert all(a[j]+sum(a)==sum(D[i][j]*lam[i] for i in range(9)) for j in range(n))
    w = [-sum(a),*a]
    assert sum(w)==0
    return [v/scale**2 for v in w]


def interval(z, i, j):
    t,x,y = [b-a for a,b in zip(z[i],z[j])]
    return t*t-x*x-y*y


def condition_bound(matrix):
    n=len(matrix)
    inverse_columns=[solve(matrix,[int(i==j) for i in range(n)]) for j in range(n)]
    inverse=list(zip(*inverse_columns))
    return max(sum(map(abs,row)) for row in matrix)*max(sum(map(abs,row)) for row in inverse)


def intrinsic_gates(z,weights,scale):
    # The original inference uses landmark inner products, not normalized y.
    anchors=z[1:4]  # z[0] is exactly zero in the fixed gauge.
    dot=lambda a,b: -a[0]*b[0]+a[1]*b[1]+a[2]*b[2]
    H=[[dot(a,b) for b in anchors] for a in anchors]
    y=[[a-b for a,b in zip(row,z[4])] for row in z[5:]]
    v=[[dot(anchor,row) for anchor in anchors] for row in y]
    D=list(map(list,zip(*[[t,x,y,t*t,x*x,y*y,t*x,t*y,x*y] for t,x,y in v])))
    b=[0,0,0,2*H[0][0],2*H[1][1],2*H[2][2],2*H[0][1],2*H[0][2],2*H[1][2]]
    a=[w*scale**2 for w in weights[1:]]
    assert [sum(x*y for x,y in zip(row,a)) for row in D]==b
    Gram=[[sum(a*b for a,b in zip(row,col)) for col in D] for row in D]
    hbound=condition_bound(H)
    dbound=sqrt_bounds(condition_bound(Gram))[1]
    assert hbound<10**5 and dbound<10**5
    return dict(exact_intrinsic_moments=True,
                landmark_condition_upper=outward(hbound)[1],
                moment_condition_upper=outward(dbound)[1])


def certify_order(z, order):
    minimum = None
    times = []
    for i in range(len(z)):
        for j in range(i+1,len(z)):
            q = interval(z,i,j)
            assert q != 0
            dt = z[j][0]-z[i][0]
            assert (q>0 and dt>0) == order[i][j]
            assert (q>0 and dt<0) == order[j][i]
            minimum = min(minimum,abs(q)) if minimum is not None else abs(q)
            if q>0: times.append(abs(dt))
    # Frozen numerical gate permits constraint residual >= -1e-10.
    assert minimum >= F(1,10**8)-F(1,10**10)
    assert min(times) >= F(1,10**8)-F(1,10**10)
    # Canonical triangular landmark basis: nonzero determinant proves signature.
    determinant = z[1][0]*z[2][1]*z[3][2]
    assert determinant != 0
    return dict(unordered_pairs=len(z)*(len(z)-1)//2,
                minimum_absolute_interval=outward(minimum),
                minimum_causal_time_separation=outward(min(times)),
                landmark_determinant=outward(determinant),
                exact_order=True, exact_moment_rank=9)


def spd_minors(K):
    """Bareiss elimination; positive leading principal minors certify SPD."""
    a = [row[:] for row in K]
    prior = 1
    pivots = []
    for k in range(len(a)):
        p = a[k][k]
        assert p>0
        pivots.append(str(p))
        for i in range(k+1,len(a)):
            for j in range(k+1,len(a)):
                numerator = a[i][j]*p-a[i][k]*a[k][j]
                assert numerator % prior == 0
                a[i][j] = numerator//prior
        prior = p
    return pivots


def precision_certificate(K):
    """Rational approximate inverse, certified via a Neumann residual bound."""
    t = 10**18
    inverse = np.linalg.inv(np.array(K,dtype=float)/20)
    inverse = (inverse+inverse.T)/2
    Q = [[round(float(v)*t) for v in row] for row in inverse]
    n = len(K)
    assert all(Q[i][j]==Q[j][i] for i in range(n) for j in range(n))
    residual = [[20*t*(i==j)-sum(K[i][k]*Q[k][j] for k in range(n))
                 for j in range(n)] for i in range(n)]
    eta = F(max(sum(map(abs,row)) for row in residual),20*t)
    norm = F(max(sum(map(abs,row)) for row in Q),t)
    assert eta<1
    error = norm*eta/(1-eta)
    return Q,t,norm,error,dict(residual_infinity_norm=outward(eta),
                             inverse_error_infinity_bound=outward(error))


def quadratic_bounds(intervals,Q,t,norm,error):
    # All means are first rounded outwards on the common 10^-30 grid.
    v = [(a+b)/2 for a,b in intervals]
    delta = max((b-a)/2 for a,b in intervals)
    n = len(v)
    nominal = sum(v[i]*sum(F(Q[i][j],t)*v[j] for j in range(n)) for i in range(n))
    v1, vi = sum(map(abs,v)),max(map(abs,v))
    rounding = norm*(2*v1*delta+n*delta*delta)
    inverse = (v1+n*delta)*(vi+delta)*error
    return nominal-rounding-inverse, nominal+rounding+inverse


def select_pair():
    candidates=[]
    for path in sorted((HERE/'results').glob('cloud-*.json.gz')):
        r=read(path)
        for j,t in enumerate(r['trials']):
            if 'best' in t: candidates.append((t['best']['relative_weight_separation'],r,j))
    _,r,j=max(candidates,key=lambda x:x[0])
    assert not any(v[0]>=.25 for v in candidates)
    return r,j


def build_witness():
    r,j=select_pair();p=r['packet'];obs=r['observed'];best=r['trials'][j]['best']
    anchors=set(p['landmarks'])
    mask=[i for i,(a,b) in enumerate(p['pairs']) if a in anchors or b in anchors]
    assert mask==list(np.flatnonzero(input_mask(p)))
    nodes=p['landmarks']+[p['root']]+p['support'];lookup={a:i for i,a in enumerate(nodes)}
    return dict(schema='x6.stability.rational-witness/1',
                selection='POSTHOC strongest SMALL_PAIR; no frozen strong success',
                index=r['index'],trial=j,coordinates=[[[f'{v:.12f}' for v in row] for row in z] for z in best['coordinates']],
                scale=str(p['scale']),rho=32768,nodes=nodes,full_order=p['full_order'],
                input_mask_indices=mask,pairs=[[lookup[a],lookup[b]] for i,(a,b) in enumerate(p['pairs']) if i in mask],
                counts=[obs['counts'][i] for i in mask],
                overlaps=[[obs['overlaps'][i][j] for j in mask] for i in mask])


def certify(witness):
    z=[[[F(v) for v in row] for row in geometry] for geometry in witness['coordinates']]
    scale=F(witness['scale']);m=len(witness['counts'])
    order=[certify_order(geometry,witness['full_order']) for geometry in z]
    weights=[exact_weights(geometry,scale) for geometry in z]
    gates=[intrinsic_gates(geometry,w,scale) for geometry,w in zip(z,weights)]
    delta=[b-a for a,b in zip(*weights)]
    sq=sum(v*v for v in delta)
    norm_delta=sqrt_bounds(sq)
    norm_weights=[sqrt_bounds(sum(v*v for v in w)) for w in weights]
    relative=(2*norm_delta[0]/sum(x[1] for x in norm_weights),2*norm_delta[1]/sum(x[0] for x in norm_weights))
    sign_field=[1 if v>0 else -1 if v<0 else 0 for v in delta]
    scalar_gap=sum(abs(v) for v in delta)
    K=[[19*int(c)+(int(witness['counts'][i]) if i==j else 0) for j,c in enumerate(row)] for i,row in enumerate(witness['overlaps'])]
    assert all(K[i][j]==K[j][i] for i in range(m) for j in range(m))
    minors=spd_minors(K)
    Q,t,norm,error,precision=precision_certificate(K)
    pi_lo,pi_hi=pi_bounds();means=[]
    for geometry in z:
        mu=[]
        for i,j in witness['pairs']:
            q=interval(geometry,i,j);assert q>0
            a,b=sqrt_bounds(q)
            factor=F(witness['rho'],12)*scale**3*q
            mu.append(tuple(map(F,outward(factor*pi_lo*a,factor*pi_hi*b,30))))
        means.append(mu)
    pair=[(b[0]-a[1],b[1]-a[0]) for a,b in zip(*means)]
    residuals=[[(a-n,b-n) for (a,b),n in zip(mu,witness['counts'])] for mu in means]
    pair_q=quadratic_bounds(pair,Q,t,norm,error)
    observed=[quadratic_bounds(v,Q,t,norm,error) for v in residuals]
    assert pair_q[0]>0 and pair_q[1]<4
    assert all(0<lo<hi<m for lo,hi in observed)
    assert F(1482,10000)<relative[0]<relative[1]<F(1483,10000)<F(1,4)
    marginal=max(max(abs(a),abs(b))/sqrt_bounds(F(n))[0] for (a,b),n in zip(pair,witness['counts']))
    assert marginal<F(2,5)
    return dict(status='CERTIFIED_SMALL_PAIR',index=witness['index'],trial=witness['trial'],
        nodes=len(z[0]),measured_intervals=m,exact_geometry=order,exact_intrinsic_gates=gates,
        scale_interpretation='Exact decimal rational from archived JSON; coordinates exact 12-place decimals.',
        covariance=dict(definition='(19*C+diag(N))/20',dimension=m,
                        positive_leading_principal_minors=len(minors),
                        leading_minors_sha256=hashlib.sha256('\n'.join(minors).encode()).hexdigest(),**precision),
        squared_pair_discrepancy=outward(*pair_q),
        squared_observed_discrepancies=[outward(*v) for v in observed],
        relative_weight_separation=outward(*relative),
        absolute_weight_separation=outward(*norm_delta),
        half_separation_lower_bound=outward(norm_delta[0]/2,norm_delta[1]/2),
        normalized_minimax_lower_bound=outward(relative[0]/2,relative[1]/2),
        maximum_marginal_mean_shift_upper=outward(marginal)[1],
        weights_intervals=[[outward(v) for v in w] for w in weights],
        adversarial_bounded_field=sign_field,
        scalar_response_separation=outward(scalar_gap),
        scalar_half_separation_lower_bound=outward(scalar_gap/2),
        strong_threshold_met=False,
        scope='Deterministic selected-node bounded-error model and discrete moment weights; not full Poisson indistinguishability, smooth-field accuracy, or global instability.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    frozen();witness=build_witness()
    if args.write:save(HERE/'witness.json',witness)
    else:assert witness==read(HERE/'witness.json')
    cert=certify(witness)
    if args.write:save(HERE/'certificate.json',cert)
    else:
        archived=read(HERE/'certificate.json')
        # Inverse proposals may differ by BLAS; every fresh proposal is certified.
        assert cert['relative_weight_separation']==archived['relative_weight_separation']
        for key in ['squared_pair_discrepancy','squared_observed_discrepancies']:
            assert np.allclose(np.array(cert[key],float),np.array(archived[key],float),rtol=0,atol=1e-7)
    print({k:cert[k] for k in ['status','index','trial','measured_intervals','relative_weight_separation','half_separation_lower_bound','squared_pair_discrepancy','squared_observed_discrepancies']})


if __name__=='__main__':main()
