"""Exact finite-grid certificates for the total transferred fraction and fixed marginals."""
from fractions import Fraction as Q
from itertools import product
from math import ceil, lcm
import json
import numpy as np
from readout import ROOT, label, branch_splits, corner_data

def exact_effects(m):
    a=np.vectorize(Q.from_float,otypes=[object])(m[:,:3])
    a=(a+a.swapaxes(-1,-2))/2
    # The inherited failure outcome is exactly one minus the success.
    return np.concatenate((a,(1-a.sum(axis=1))[:,None]),axis=1)


def certify(m,names,parents,mids,ends,laws):
    M=exact_effects(m)
    b=np.array([Q(1,2) if k in parents else Q(0) for k in names])
    S=M[:,:3].sum(axis=1)
    P=b@M@b
    gram_lower=[min(s[i,i]-sum(abs(s[i,j]) for j in range(len(s)) if i!=j)
                    for i in range(len(s))) for s in S]
    assert min(gram_lower)>0
    pairs,_=corner_data(names,parents,mids,ends)
    indices=[(names.index(a),names.index(c)) for a,c in pairs]
    def corner_values(row):
        return [(row[i]+row[j])/2 for i,j in indices]
    # On [0,.06] every accepted bin decreases for each allowed endpoint
    # mixture. Bound the derivative at both interval endpoints.
    T=Q(6,100)
    derivative=[]
    for j in range(2):
        row=[]
        for k in range(3):
            cross=corner_values(b@M[j,k])
            start=max(cross)-P[j,k]
            end=(1-T)*start+T*(max(M[j,k].ravel())-min(cross))
            upper=2*max(start,end)
            assert upper<0
            row.append(float(upper))
        derivative.append(row)
    D=M[1]-M[0]; old=b@D@b
    a=[max(abs(b@d-u)) for d,u in zip(D,old)]
    c=[max(abs(d-u).ravel()) for d,u in zip(D,old)]
    contrast=(2*T*(1-T)*sum(a)+T*T*sum(c))/(sum(abs(old))/4)
    assert contrast<1
    ds=D[:3].sum(axis=0)
    sign_upper=max(ds[i,i]+sum(abs(ds[i,j]) for j in range(len(ds)) if i!=j) for i in range(len(ds)))
    assert sign_upper<0
    data=json.loads((ROOT/'tangent_points.json').read_text())
    lo,hi=Q(data['lower_fraction']),Q(data['upper_fraction'])
    assert 0<lo<hi<T
    tangent=[];upper_ratios=[]
    for j,point in enumerate(data['points_by_density_then_root']):
        rows=[np.array([Q(r.get(label(k),0),data['denominator']) for k in names]) for r in point]
        for side,row in enumerate(rows):
            allowed={pair[side] for pair in pairs}
            assert sum(row)==1 and min(row)>=0 and all(names[i] in allowed for i,x in enumerate(row) if x)
        v=(rows[0]+rows[1])/2
        x=(1-lo)*b+lo*v
        z=x@S[j]
        tangent_value=(z@x+2*lo*(min(corner_values(z))-z@v))/(b@S[j]@b)
        y=(1-hi)*b+hi*v
        actual=(y@S[j]@y)/(b@S[j]@b)
        tangent.append(tangent_value);upper_ratios.append(actual)
    assert min(tangent)>Q(9,10) and min(upper_ratios)<Q(9,10)
    # Convexity gives the maximal success for a fixed N12 marginal at one of
    # its 77,000 deterministic daughter assignments. An integer upper sum
    # eliminates non-maximizers, then exact rationals rank all surviving ties.
    all_fixed={}
    for law in ('marked','shapes'):
        marginal=laws[law][0];weights=[marginal[k] for k in mids]
        denom=lcm(*(v.denominator for v in weights)); nums=[int(denom*v) for v in weights]
        choices=[sorted(names.index(k) for k in branch_splits(h,set(ends),law)) for h in mids]
        arr=np.array(list(product(*choices)),dtype=np.int64);ratios=[];winners=[]
        for j,s in enumerate(S):
            scale=2**52
            up=np.vectorize(lambda q:ceil(q*scale),otypes=[np.int64])(s)
            assert int(np.abs(up).max())*denom**2 < 2**62
            bound=np.zeros(len(arr),dtype=np.int64)
            for u,nu in enumerate(nums):
                for v,nv in enumerate(nums):
                    bound+=nu*nv*up[arr[:,u],arr[:,v]]
            def candidate(row):
                return sum(wu*wv*s[i,k] for i,wu in zip(row,weights) for k,wv in zip(row,weights))
            best=int(bound.argmax())
            threshold=ceil(candidate(arr[best])*scale*denom**2)
            possibles=np.flatnonzero(bound>=threshold)
            val,winner=max((candidate(arr[ix]),int(ix)) for ix in possibles)
            ratios.append(float(val/(b@s@b)))
            winners.append([label(names[i]) for i in arr[winner]])
            assert val<Q(9,10)*(b@s@b)
        all_fixed[law]={'N12_parent_order':[label(k) for k in mids],'assignments_per_density':len(arr),
                        'maximum_success_over_N11_success':ratios,'maximizing_assignments':winners}
    return {'success_PSD_row_lower_bounds':list(map(float,gram_lower)),
            'sign_matrix_row_upper_bound':float(sign_upper),'all_bin_derivative_upper_bounds_to_006':derivative,
            'contrast_over_tolerance_bound_to_006':float(contrast),'breakpoint_fraction_bracket':[float(lo),float(hi)],
            'minimum_success_ratio_lower_bound_at_lo':list(map(float,tangent)),
            'witness_success_ratio_at_hi':list(map(float,upper_ratios)),
            'fixed_intermediate_full_replacement':all_fixed}


