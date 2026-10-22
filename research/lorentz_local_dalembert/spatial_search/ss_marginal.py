"""Post-search exact single-count distinguishability diagnostics.
SPDX-License-Identifier: Apache-2.0
"""
from ss_run import *
from sc_run import sqrt_bounds,interval
from st_certificate import pi_bounds

def means(w,z,ends,pi):
    result=[]
    for i,j in ends:
        q=interval(z,i,j);assert q>0
        a,b=sqrt_bounds(q);factor=F(w['rho'],12)*F(w['scale'])**3*q
        result.append(tuple(map(F,outward(factor*pi[0]*a,factor*pi[1]*b,digits=30))))
    return result

def lower_bound(a,b):
    ra=(sqrt_bounds(a[0])[0],sqrt_bounds(a[1])[1])
    rb=(sqrt_bounds(b[0])[0],sqrt_bounds(b[1])[1])
    distance=max(F(0),ra[0]-rb[1],rb[0]-ra[1])
    exponent=distance*distance/2
    return exponent,F(outward(void_bounds(min(exponent,F(1)))[0])[0])

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    w,z,ends=geometry();pi=pi_bounds();base=means(w,z,ends,pi)
    rows=read(HERE/'candidates.json.gz');selected=[r for r in rows if 'relative' in r and F(r['relative'][0])>F(1,5)]
    results=[]
    for row in selected:
        zz=deform(z,row['node'],row['axis'],row['sign'],F(row['step']))
        r=dict(index=row['index'],symmetric_gap=row['relative'])
        try:r['intrinsic_gates']=intrinsic_gates(zz,exact_weights(zz,F(w['scale'])),F(w['scale']))
        except (AssertionError,StopIteration,ZeroDivisionError):
            r['status']='CONDITIONING_REJECTED';results.append(r);continue
        alt=means(w,zz,ends,pi)
        candidates=[(*lower_bound(a,b),k) for k,(a,b) in enumerate(zip(base,alt))]
        exponent,tv,k=max(candidates,key=lambda a:(a[0],-a[2]))
        r.update(status='DISTINGUISHABLE_AT_TV_GATE' if tv>F(1,4) else 'MARGINAL_INCONCLUSIVE',
                 interval_index=k,endpoints=list(ends[k]),
                 mean_intervals=[[str(x) for x in a] for a in (base[k],alt[k])],
                 exponent_lower=outward(exponent)[0],tv_lower=outward(tv)[0])
        results.append(r)
    unresolved=[r['index'] for r in results if r['status']=='MARGINAL_INCONCLUSIVE']
    # Analytic controls: identical marginals give zero; swapping the pair preserves the bound.
    assert lower_bound((F(100),)*2,(F(100),)*2)[1]==0
    a,b=(F(100),)*2,(F(121),)*2
    assert lower_bound(a,b)==lower_bound(b,a)
    assert F(39,100)<lower_bound(a,b)[1]<F(4,10)
    assert lower_bound((F(0),)*2,(F(100),)*2)[1]>F(63,100)
    return dict(status='NO_STRONG_CLOSE_PAIR_IN_FINITE_GRID' if not unresolved else 'HOLD_STRONG_CANDIDATE_LAW',
        post_search_diagnostic=True,strong_gap_candidates=len(selected),
        conditioning_rejected=sum(r['status']=='CONDITIONING_REJECTED' for r in results),
        distinguishable_at_tv_gate=sum(r['status']=='DISTINGUISHABLE_AT_TV_GATE' for r in results),
        unresolved_indices=unresolved,results=results,
        analytic_controls='PASS: equal means, symmetry, known exponent 1/2, conservative exponent cap',
        scope='Only the 512 frozen sampled geometries. A marginal TV lower bound also lower-bounds the full joint law, without an independence assumption among counts. No continuous-family or global exclusion.')

if __name__=='__main__':
    result=run()
    if '--verify' in sys.argv:assert result==read(HERE/'marginal_diagnostic.json')
    else:save(HERE/'marginal_diagnostic.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='results'}))
