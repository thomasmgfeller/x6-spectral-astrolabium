"""Finite Poisson overlap relaxation; exact integer shortest paths.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib,math
from pathlib import Path
from functools import lru_cache
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'finite_poisson_bounds'))
from fp_common import F,read,save,input_record,count_box,confidence_bound,outward,pi_bounds,cube_bounds,OLD,interval,sqrt_bounds
from fp_bound import Bound
UNIT=10**6
@lru_cache(None)
def box(n,c):
    lo,hi=count_box(int(n),c)
    return lo.numerator*UNIT//lo.denominator,-((-hi.numerator*UNIT)//hi.denominator)
def close(D):
    D=D.copy()
    assert np.max(abs(D))<10**12
    for k in range(len(D)):D=np.minimum(D,D[:,k,None]+D[None,k,:])
    assert np.all(D.diagonal()>=0),'EMPTY_RELAXATION: no accuracy claim'
    return D

def compute(index):
    p,obs,mask=input_record(index);m=len(mask)
    ns=[obs['counts'][i] for i in mask]
    C=np.array(obs['overlaps'],dtype=np.int64)[np.ix_(mask,mask)]
    assert np.array_equal(C,C.T) and np.array_equal(C.diagonal(),ns)
    nodes=p['landmarks']+[p['root']]+p['support'];lookup={n:i for i,n in enumerate(nodes)}
    order=p['full_order'];pairs=[p['pairs'][i] for i in mask]
    def before(a,b):return bool(order[lookup[a]][lookup[b]])
    def le(a,b):return a==b or before(a,b)
    ends=[]
    for a,b in pairs:
        if before(b,a):a,b=b,a
        assert before(a,b);ends.append((a,b))
    where={v:i for i,v in enumerate(ends)}
    raw=[count_box(n,12) for n in ns]
    D=np.full((m+1,m+1),10**12,dtype=np.int64);np.fill_diagonal(D,0)
    for i,n in enumerate(ns):lo,hi=box(n,12);D[0,i+1]=hi;D[i+1,0]=-lo
    def edge(i,j,upper):D[i+1,j+1]=min(D[i+1,j+1],upper)
    def interval_bound(i,lo,hi):D[0,i+1]=min(D[0,i+1],hi);D[i+1,0]=min(D[i+1,0],-lo)
    nesting=known=empty=0
    for i in range(m):
      for j in range(i+1,m):
        overlap=int(C[i,j]);a=ns[i]-overlap;b=ns[j]-overlap
        assert min(overlap,a,b)>=0
        lc,uc=box(overlap,20);la,ua=box(a,20);lb,ub=box(b,20)
        edge(j,i,ua-lb);edge(i,j,ub-la)
        interval_bound(i,lc+la,uc+ua);interval_bound(j,lc+lb,uc+ub)
        ai,bi=ends[i];aj,bj=ends[j]
        if le(aj,ai) and le(bi,bj):
            assert overlap==ns[i];edge(j,i,0);edge(i,j,ub);edge(j,i,-lb);nesting+=1
        if le(ai,aj) and le(bj,bi):
            assert overlap==ns[j];edge(i,j,0);edge(j,i,ua);edge(i,j,-la);nesting+=1
        lower=aj if le(ai,aj) else ai if le(aj,ai) else None
        upper=bi if le(bi,bj) else bj if le(bj,bi) else None
        if lower is not None and upper is not None:
            if not before(lower,upper):assert overlap==0;empty+=1
            elif (lower,upper) in where:
                k=where[lower,upper];assert overlap==ns[k];known+=1
                interval_bound(k,lc,uc)
                edge(k,i,ua);edge(i,k,-la);edge(k,j,ub);edge(j,k,-lb)
    initial=D.copy();D=close(D)
    tightened=[(max(lo,F(-int(D[i+1,0]),UNIT)),min(hi,F(int(D[0,i+1]),UNIT))) for i,(lo,hi) in enumerate(raw)]
    assert all(lo<=hi for lo,hi in tightened)
    ratios=[(b-a)/(d-c) for (a,b),(c,d) in zip(tightened,raw)]
    pi0,pi1=pi_bounds();factor=F(32768,12)*F(str(p['scale']))**3
    qb=[(cube_bounds((lo/(factor*pi1))**2)[0],cube_bounds((hi/(factor*pi0))**2)[1]) for lo,hi in tightened]
    prior=read(OLD/f'results/cloud-{index:02d}.json.gz')
    result=dict(index=index,intervals=m,extra_counts=3*m*(m-1)//2,nesting_pairs=nesting,known_intersections=known,empty_intersections=empty,
        tightened_marginals=sum(r<1 for r in ratios),minimum_width_ratio=outward(min(ratios)),median_width_ratio=outward(sorted(ratios)[m//2]),
        mean_box=[[str(v) for v in row] for row in tightened],difference_upper_microcounts=D.tolist(),
        tightened_difference_edges=int(np.sum(D[1:,1:]<initial[1:,1:])),status='BASE_HOLD')
    if prior['base'].get('qualified'):
        old=read(HERE.parent/f'finite_poisson_bounds/results/cloud-{index:02d}.json.gz')
        bound=Bound(p,mask,prior['base']['coordinates'],qb,pivots=old['constants']['pivots'])
        result.update(status='COMPLETE',full_bound=bound.evaluate(0))
    if index==9:
        witness=read(OLD/'witness.json');rows=[]
        for z in witness['coordinates']:
            z=[[F(v) for v in row] for row in z];means=[(F(0),F(0))]
            for a,b in witness['pairs']:
                q=interval(z,a,b);sl,su=sqrt_bounds(q);f=factor*q
                means.append((f*pi0*sl,f*pi1*su))
            violated=[];uncertain=0
            for i in range(m+1):
              for j in range(m+1):
                if i==j:continue
                u=F(int(D[i,j]),UNIT)
                if means[j][0]-means[i][1]>u:violated.append([i,j])
                elif means[j][1]-means[i][0]>u:uncertain+=1
            rows.append(dict(violated_edges=violated,unresolved_edges=uncertain,
                status='EXCLUDED' if violated else 'INSIDE_RELAXATION' if not uncertain else 'UNRESOLVED'))
        result['witness_relaxation_checks']=rows
    return result

def controls():
    D=np.array([[0,10,20],[0,0,3],[0,20,0]],dtype=np.int64)
    assert close(D)[0,2]==13
    assert box(0,20)==(0,20*UNIT)
    D=np.array([[0,-1],[-1,0]],dtype=np.int64)
    try:close(D)
    except AssertionError:pass
    else:raise AssertionError('negative cycle accepted')
    # A single synthetic nested pair with common count 100 and exclusive 0.
    # Its difference upper bound is 20, whereas independent boxes allow more.
    assert box(100,12)[1]-box(100,12)[0]>20*UNIT
    return ['shortest_path_transitivity','zero_count_exact_tail','empty_set_rejected','nested_zero_difference_gain']

def main():
    verify='--verify' in sys.argv
    freeze=read(HERE/'freeze.json')
    for name,h in freeze['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    contract=read(HERE/'contract.json');rows=[]
    for i in contract['indices']:
        r=compute(i);path=HERE/f'results/cloud-{i:02d}.json.gz'
        if verify:assert r==read(path),i
        else:save(path,r)
        row={k:r[k] for k in ['index','intervals','extra_counts','tightened_marginals','minimum_width_ratio','median_width_ratio','status']}
        row['ten_percent_certified']=r.get('full_bound',{}).get('ten_percent_certified',False)
        if 'witness_relaxation_checks' in r:row['witness_relaxation_checks']=r['witness_relaxation_checks']
        rows.append(row);print(json.dumps(row),flush=True)
    total=sum(r['intervals'] for r in rows);extra=sum(r['extra_counts'] for r in rows)
    fail=confidence_bound(total,12)+confidence_bound(extra,20)
    result=dict(status='PASS',controls=controls(),interval_total=total,extra_counts=extra,
      coverage_lower=outward(1-fail)[0],failure_upper=outward(fail)[1],
      tightened_marginals=sum(r['tightened_marginals'] for r in rows),
      full_box_ten_percent=sum(r['ten_percent_certified'] for r in rows),records=rows)
    if verify:assert result==read(HERE/'summary.json')
    else:save(HERE/'summary.json',result)
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
