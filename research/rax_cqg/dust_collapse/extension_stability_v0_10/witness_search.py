"""Search feasible parent-simplex mixtures on all fully clocked v0.8 pilot states."""
import argparse,json
from pathlib import Path
import numpy as np
from scipy.optimize import minimize
from source import ROOT,CACHE,reference
from bounds import inputs
from teiltraeger import names_and_reach
def search(tag,d):
    names,reach,base,cols,known,mags,radii=inputs(tag)
    pn,_=names_and_reach()
    labels=[x for x in pn if known[names.index(x)] is not None]
    ix=[pn.index(s) for s in labels]; idx=[names.index(s) for s in labels]
    gram=np.load(reference.SOURCE/'gram.npy').sum(axis=0)[np.ix_(ix,ix)]
    amp=np.array([complex(*known[j][d]) for j in idx])
    metric=(amp.conj()[:,None]*gram*amp).real
    b=np.zeros(len(labels));b[:2]=.5
    p=b@metric@b
    sets=[[k for k,j in enumerate(idx) if j in r] for r in reach]
    active=[[sub[0]] for sub in sets]
    weights=[np.ones(1),np.ones(1)]
    for iteration in range(30):
        n0=len(active[0]);cols_ix=active[0]+active[1]
        start=np.concatenate(weights)
        def coord(w):
            return .95*b+.025*np.bincount(cols_ix,weights=w,minlength=len(b))
        def value(w):
            v=coord(w); return v@metric@v/p
        def jac(w):return .05*(metric@coord(w))[cols_ix]/p
        cons=[{'type':'eq','fun':lambda w: w[:n0].sum()-1,
               'jac':lambda w: np.r_[np.ones(n0),np.zeros(len(w)-n0)]},
              {'type':'eq','fun':lambda w: w[n0:].sum()-1,
               'jac':lambda w: np.r_[np.zeros(n0),np.ones(len(w)-n0)]}]
        res=minimize(value,start,jac=jac,method='SLSQP',bounds=[(0,1)]*len(start),
                     constraints=cons,options={'ftol':1e-14,'maxiter':300})
        if not res.success:raise ValueError(res.message)
        w=res.x;v=coord(w);grad=.05*metric@v/p;new=False
        weights=[w[:n0],w[n0:]]
        for r,allowed in enumerate(sets):
            j=min(allowed,key=lambda k:grad[k])
            if j not in active[r] and weights[r]@grad[active[r]]-grad[j]>1e-12:
                active[r].append(j);weights[r]=np.r_[weights[r],0.];new=True
        if not new:break
    else:raise ValueError('active set iterations')
    den=10**8
    used=[];x=.95*b
    for r in range(2):
        a=np.maximum(weights[r],0);a/=a.sum()
        coeff=np.floor(a*den).astype(np.int64)
        coeff[np.argmax(a)]+=den-int(sum(coeff))
        if min(coeff)<0 or sum(coeff)!=den:raise ValueError('unphysical transfer')
        mix={labels[j]:int(k) for j,k in zip(active[r],coeff) if k}
        for name,k in mix.items():x[labels.index(name)]+=.025*k/den
        used.append(mix)
    val=x@metric@x;radius=sum(x[k]*float(radii[j])*np.sqrt(gram[k,k].real) for k,j in enumerate(idx))
    if any(radii[j] for j in idx[:2]):raise ValueError('base has uncertainty')
    return {'iterations':iteration+1,'parent_candidates':[len(a) for a in sets],
            'relative_transfer':.05,'denominator_per_parent':den,'weights':used,'central_ratio':val/p,
            'radius_envelope':[max(0.,np.sqrt(val)-radius)**2/p,(np.sqrt(val)+radius)**2/p]}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    a.out.write_text(json.dumps({f'{s}_{d}':search(s,d) for s in ('coarse','fine') for d in (0,1)},indent=2)+'\n')
