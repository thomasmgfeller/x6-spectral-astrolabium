"""Frozen comparison with the published KL design rule."""
from fractions import Fraction as Q
from common import kl,reference
from bounds import sufficient,design_interval,confidence
from support import contract,value,interval_record

def planning():
    rows=[]
    for text in contract()['planning_h']:
        h=Q(text);maximum=contract()['maximum_planning_clouds']
        old=kl.first_sufficient(h,128,'KL',maximum);new=sufficient(h,128,maximum)
        gain=Q(old,new) if old and new else None
        for method,m in [('KL',old),('Bennett',new)]:
            fn=(lambda m:kl.design_interval(h,128,m,'KL')) if method=='KL' else (lambda m:design_interval(h,128,m))
            rows.append(dict(h=text,method=method,sufficient_clouds=m,gain=None if gain is None else value(gain),
                interval=None if m is None else interval_record(fn(m)),
                adjacent_interval=None if m is None or m==1 else interval_record(fn(m-1))))
    factors=[Q(r['gain']['exact']) for r in rows if r['method']=='Bennett' and r['gain'] is not None]
    passed=len(factors)==3 and min(factors)>=2
    return dict(status='TWO_FOLD_VARIANCE_GAIN_CERTIFIED' if passed else 'TWO_FOLD_VARIANCE_GAIN_NOT_ESTABLISHED',
                fresh_gate=passed,rows=rows,claim='Sufficient procedure boundaries; not optimal minima or executed cloud counts')

def analyze(counts,cell):
    h=Q(cell['h']);rows=[];groups=[]
    for m in cell['group_sizes']:
        totals=counts.reshape(-1,m).sum(axis=1)
        stats={k:dict(covered=0,qualified=0,incompatible=0,qualified_noncovering=0) for k in ['KL','Bennett']}
        narrower=0
        for index,total in enumerate(totals):
            intervals={'KL':kl.confidence(int(total),128,m),'Bennett':confidence(int(total),128,m)}
            records={}
            for method,interval in intervals.items():
                covered=interval is not None and interval[0]<=h<=interval[1]
                r=reference.relative_radius(interval);qualified=r is not None and r<=Q(1,5)
                for key,flag in [('covered',covered),('qualified',qualified),('incompatible',interval is None),('qualified_noncovering',qualified and not covered)]:stats[method][key]+=int(flag)
                records[method]=dict(**interval_record(interval),contains_true_h=covered)
            old,new=intervals['KL'],intervals['Bennett']
            narrower+=int(old is not None and new is not None and old[0]<=new[0]<=new[1]<=old[1])
            groups.append(dict(group_size=m,group_index=index,total_c2=int(total),intervals=records))
        for method in stats:rows.append(dict(h=cell['h'],clouds_per_group=m,groups=len(totals),method=method,**stats[method],bennett_subset_count=narrower))
    full=confidence(int(counts.sum()),128,len(counts))
    return dict(h=cell['h'],rows=rows,groups=groups,density_twin=dict(status='OUTSIDE_UNIFORM_DENSITY_ASSUMPTION',
                same_relations=True,flat_q=0,restricted_interval_contains_zero=full is not None and full[0]==0),
                claim='Paired descriptive checks; nested budgets reuse clouds; no unadjusted intersection')
