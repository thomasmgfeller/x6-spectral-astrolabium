"""Uniform difference-count laws with an interval-valued unknown overlap.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'paired_family'))
from pf_common import (F,read,save,outward,base_setup,setup,variance_enclosure,qrange,qpoly,
    mean_bounds,interval,sqrt_bounds,cm,boosted,cover)
import jr_run as jr
HERE=Path(__file__).resolve().parent

def frozen():
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def inputs():
    old=read(HERE.parent/'paired_tail/summary.json')
    records=read(HERE.parent/'paired_tail/certificates.json.gz')
    pending=[dict(index=r['index'],ray=r['ray'],parent=r['parent'],lo=r['lo'],hi=r['hi']) for r in records if r['status']=='HOLD']
    assert len(pending)==old['new_states']['HOLD']==38
    assert sorted({r['ray'] for r in pending})==[3,45]
    return old,pending

def rate_bounds(stats,lo,hi):
    a,b=[tuple(map(F,v)) for v in stats['count_mean_intervals']]
    assert 0<=lo<=hi<=min(a[1],b[1])
    # N(A)-N(B)=N(A\B)-N(B\A). Only the two exclusive atoms are independent.
    plus=(max(F(0),a[0]-hi),a[1]-lo)
    minus=(max(F(0),b[0]-hi),b[1]-lo)
    assert 0<=plus[0]<=plus[1] and 0<=minus[0]<=minus[1]
    return plus,minus

def enclose_difference(stats,threshold,c):
    a,b=[tuple(map(F,v)) for v in stats['count_mean_intervals']]
    lower=F(stats['common_mean_lower']);upper=min(a[1],b[1])
    assert 0<=lower<=upper
    n=c['overlap_slices'];rows=[];probabilities=[]
    jc=dict(c['probability'],event=dict(x_coefficient=1,threshold=threshold))
    # Every possible overlap intensity belongs to at least one closed slice.
    for j in range(n):
        lo=lower+(upper-lower)*j/n;hi=lower+(upper-lower)*(j+1)/n
        plus,minus=rate_bounds(stats,lo,hi)
        if max(plus+minus)>c['maximum_exclusive_mean']:
            return dict(status='HOLD_RATE_BUDGET',probability=['0','1'])
        try:p,records=jr.enclose_event(minus,plus,jc)
        except AssertionError:return dict(status='HOLD_PROBABILITY_BUDGET',probability=['0','1'])
        probabilities.append(p)
        rows.append(dict(overlap=[str(lo),str(hi)],plus=[str(x) for x in plus],minus=[str(x) for x in minus],
            probability=outward(*p,digits=60),records=records))
    probability=(min(p[0] for p in probabilities),max(p[1] for p in probabilities))
    return dict(status='ENCLOSED',threshold=threshold,overlap_range=[str(lower),str(upper)],
                probability=outward(*probability,digits=60),slices=rows)

def candidates(b,lo,hi):
    rows=[]
    for k,side in b['common_anchors']:
        alt=variance_enclosure(b,lo,hi,k,side)
        if alt is None:continue
        base=b['base_statistics'][k];a,d=[tuple(map(F,v['mean'])) for v in (base,alt)]
        separation=max(F(0),a[0]-d[1],d[0]-a[1])
        variance=F(base['variance_upper'])+F(alt['variance_upper'])
        score=separation*separation/variance if variance else F(0)
        threshold=((sum(a)+sum(d))/4).__floor__()
        rows.append(dict(anchor=k,side=side,score=score,threshold=threshold,base=base,moved=alt))
    return sorted(rows,key=lambda r:(-r['score'],r['anchor']))

def classify(b,lo,hi,c,base_cache):
    attempts=[]
    for v in candidates(b,lo,hi)[:c['maximum_anchor_events_per_cell']]:
        key=(b['ray']['index'],v['anchor'],v['threshold'])
        if key not in base_cache:base_cache[key]=enclose_difference(v['base'],v['threshold'],c)
        p=base_cache[key];q=enclose_difference(v['moved'],v['threshold'],c)
        a,d=[tuple(map(F,r['probability'])) for r in (p,q)]
        tv=max(F(0),a[0]-d[1],d[0]-a[1])
        attempt=dict(anchor=v['anchor'],side=v['side'],score=str(v['score']),threshold=v['threshold'],
            base_statistics=v['base'],moved_statistics=v['moved'],base_law=p,moved_law=q,tv_lower=outward(tv)[0])
        attempts.append(attempt)
        if tv>F(c['tv_gate']):return dict(status='OVERLAP_DIFFERENCE_EXCLUDED',tv_lower=attempt['tv_lower'],attempts=attempts)
    best=max([F(0)]+[F(a['tv_lower']) for a in attempts])
    return dict(status='HOLD',tv_lower=outward(best)[0],attempts=attempts)
