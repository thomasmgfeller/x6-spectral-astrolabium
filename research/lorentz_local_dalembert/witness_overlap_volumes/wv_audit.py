"""Independent controls and recorded numerical containment audit.
SPDX-License-Identifier: Apache-2.0
"""
from wv_run import *
def controls():
    # Integer interval classifier checked at exact rational points in cells.
    cells=np.array([[t,x,y] for t in range(-3,4) for x in range(-2,3) for y in range(-2,3)],dtype=np.int64)
    lo=np.array([[0,0,0]],dtype=np.int64);hi=lo.copy()
    fi,fo,pi,po=classify_cells(cells,lo,hi)
    for k,cell in enumerate(cells):
      for a in [F(0),F(1,2),F(1)]:
       for b in [F(0),F(1,2),F(1)]:
        for c in [F(0),F(1,2),F(1)]:
         t,x,y=[F(int(v))+u for v,u in zip(cell,[a,b,c])]
         future=t>0 and t*t>x*x+y*y;past=t<0 and t*t>x*x+y*y
         if fi[0,k]:assert future
         if not fo[0,k]:assert not future
         if pi[0,k]:assert past
         if not po[0,k]:assert not past
    # Exact finite binomial tail enumeration; scalar Chernoff interval also
    # covers binomial means by the log(1+u)<=u MGF proof.
    tailcases=0
    for n in [8,32]:
      for p in [F(1,10),F(1,2),F(9,10)]:
        failure=F(0)
        for k in range(n+1):
            l,u=cb(k,4)
            if not l<=n*p<=u:failure+=math.comb(n,k)*p**k*(1-p)**(n-k)
        assert failure<=confidence_bound(1,4);tailcases+=1
    assert outcome((F(2),F(3)),(F(1),F(4)))=='INSIDE'
    assert outcome((F(5),F(6)),(F(1),F(4)))=='EXCLUDED'
    assert outcome((F(3),F(5)),(F(1),F(4)))=='UNRESOLVED'
    return dict(exact_cell_point_checks=len(cells)*27,binomial_tail_cases=tailcases,
                decision_controls=3,rational_boost_determinant=str(F(17,8)**2-F(15,8)**2))
def audit():
    w,ends,items=setup();records=[];c=read(HERE/'contract.json')
    for g in range(2):
        r=read(HERE/f'geometry-{g}.json.gz');last=r['stages'][-1]
        coords=[[F(v) for v in row] for row in w['coordinates'][g]]
        assert F(w['scale'])**2*interval(coords,3,0)<F(3,2)**2
        assert r['status']=='COMPATIBLE_WITH_CHECKED_CONFIDENCE_SET'
        assert r['analytic_status_counts']==dict(INSIDE=6737,EXCLUDED=0,UNRESOLVED=0)
        assert last['status_counts']==dict(INSIDE=1440,EXCLUDED=0,UNRESOLVED=0)
        assert len(last['controls'])==74 and all(v['status']=='ENCLOSES_ANALYTIC' for v in last['controls'])
        lookup={(x['i'],x['j']):x for x in items}
        for row in last['rows']:
            targets=lookup[row['i'],row['j']]['targets']
            for value,t in zip(row['bounds'],targets):assert outcome(tuple(map(F,value)),t)=='INSIDE'
        records.append(dict(geometry=g,checked_constraints=8177,numerical_samples=last['samples'],stages=len(r['stages'])))
    cert=read(OLD/'certificate.json');summary=read(HERE/'summary.json')
    assert F(summary['numerical_failure_upper'])<F(14,10**7)
    return dict(status='PASS',controls=controls(),records=records,
                inherited_relative_weight_separation=cert['relative_weight_separation'],
                inherited_uniform_recovery_lower_bound=cert['normalized_minimax_lower_bound'],
                interpretation='The pair lies in the actual pairwise-overlap confidence set subject to the numerical integration risk and its iid sampling assumption. This is set diameter/uniform recovery, not statistical minimax risk; it does not rule out 10% accuracy.')
if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
