"""Missing64-slice tests followed by one predeclared512-slice refinement.
SPDX-License-Identifier: Apache-2.0
"""
from tor_common import *

def run():
    frozen();c=read(HERE/'contract.json');old,previous,source,pending,missing,prior=inputs();b=setup(c);laws=[];cache={}
    assert len(missing)==c['missing_overlap_cells'] and len(prior)==c['prior_overlap_holds']
    first=evaluate_stage(b,missing,c,'missing',laws,cache)
    remaining=pending_refinement(first);assert len(remaining)<=c['maximum_refined_cells']
    second=evaluate_stage(b,remaining,c,'refined',laws,cache)
    ar=dict(missing=first,refined=second,laws=laws);final=combined(ar);states=Counter(r['status'] for r in final);volumes=Counter()
    for r in final:volumes[r['status']]+=volume(r)
    total=F(previous['total_volume']);held=volumes['HOLD'];assert sum(volumes.values())==total
    ids={r['path'] for r in pending};new=[r for r in final if r['path'] in ids];excluded=[r for r in new if r['status']!='HOLD']
    prior_map={r['path']:r for r in prior};prior_map.update({r['path']:r for r in first if r['status']=='HOLD'})
    comparisons=[dict(path=r['path'],old_tv_lower=prior_map[r['path']].get('tv_lower'),new_tv_lower=r.get('tv_lower'),status=r['status']) for r in second]
    valid={stage:sum('reason' not in r and all(laws[r[k]]['law']['status']=='ENCLOSED' for k in ('base_law_id','moved_law_id')) for r in rows) for stage,rows in (('missing',first),('refined',second))}
    summary=dict(status='THREE_PARAMETER_CUBE_EXCLUDED' if not held else 'HOLD_THREE_PARAMETER_CUBE',nodes=c['nodes'],axis=c['axis'],domain=c['domain'],
        source_hold_cells=len(pending),missing_overlap_cells_tested=len(first),refined_cells_tested=len(second),
        stage_states={stage:dict(Counter(r['status'] for r in rows)) for stage,rows in (('missing',first),('refined',second))},
        comparisons_with_both_laws_enclosed=valid,distinct_laws=len(laws),law_states=dict(Counter(r['law']['status'] for r in laws)),
        distinct_laws_by_stage=dict(Counter(r['stage'] for r in laws)),newly_excluded_cells=len(excluded),newly_excluded_volume=str(sum((volume(r) for r in excluded),F(0))),
        minimum_new_full_law_tv_lower=min((r['tv_lower'] for r in excluded),key=F,default=None),
        terminal_cells=len(final),states=dict(states),volumes={k:str(v) for k,v in volumes.items()},total_volume=str(total),hold_volume=str(held),
        previous_excluded_volume_fraction=previous['excluded_volume_fraction'],excluded_volume_fraction=str(1-held/total),excluded_volume_percent=outward(100*(1-held/total)),
        unresolved_cells=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD'],prior_overlap_comparisons=comparisons,
        inherited_zero_third_slice_fully_excluded=True,
        scope='Fixed reference in2+1 Minkowski; nodes15/17/5 independently displaced in boosted x over[-0.1,0.1]^3. Excludes unchanged order AND inherited admissibility AND symmetric physical weight gap>1/5 AND full conditional labelled count/overlap-law TV<=1/4 on certified boxes. Parameter volume is not probability. HOLD is unresolved; no general stability claim.')
    return ar,summary

if __name__=='__main__':
    for name,result in zip(('certificates.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('unresolved_cells','prior_overlap_comparisons')}),flush=True)
    print('TRIPLE_OVERLAP_REFINEMENT_REPLAY_COMPLETE',flush=True)
