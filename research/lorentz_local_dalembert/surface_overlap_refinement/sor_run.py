"""Complete missing overlap tests, then one fixed eightfold slice refinement.
SPDX-License-Identifier: Apache-2.0
"""
from sor_common import *

def run():
    frozen();c=read(HERE/'contract.json');previous,old,pending,missing,prior=inputs();b=setup(c);bases=[]
    assert len(missing)==c['missing_overlap_cells'] and len(prior)==c['prior_overlap_holds']
    first=evaluate_stage(b,missing,c,'missing',bases)
    remaining=pending_refinement(first);assert len(remaining)<=c['maximum_refined_cells']
    second=evaluate_stage(b,remaining,c,'refined',bases)
    archive=dict(missing=first,refined=second,base_laws=bases)
    final=combined(archive);states=Counter(r['status'] for r in final);areas=Counter()
    for r in final:areas[r['status']]+=area(r)
    total=F(previous['total_area']);held=areas['HOLD'];assert sum(areas.values())==total
    paths={r['path'] for r in pending};new=[r for r in final if r['path'] in paths];excluded=[r for r in new if r['status']!='HOLD']
    unresolved=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    prior_map={r['path']:r for r in prior}
    improvements=[dict(path=r['path'],old_tv_lower=prior_map[r['path']]['tv_lower'],new_tv_lower=r['tv_lower'],status=r['status']) for r in second if r['path'] in prior_map and 'tv_lower' in r]
    summary=dict(status='TWO_PARAMETER_SQUARE_EXCLUDED' if not unresolved else 'HOLD_SURFACE_OVERLAP_REFINEMENT',source_hold_cells=len(pending),missing_overlap_cells_tested=len(first),refined_cells_tested=len(second),stage_states={stage:dict(Counter(r['status'] for r in rows)) for stage,rows in (('missing',first),('refined',second))},new_states=dict(Counter(r['status'] for r in new)),newly_excluded_cells=len(excluded),newly_excluded_area=str(sum((area(r) for r in excluded),F(0))),minimum_new_full_law_tv_lower=min((r['tv_lower'] for r in excluded),key=F,default=None),terminal_cells=len(final),states=dict(states),areas={k:str(v) for k,v in areas.items()},total_area=str(total),hold_area=str(held),excluded_area_fraction=str(1-held/total),excluded_area_percent=outward(100*(1-held/total)),unresolved_cells=unresolved,distinct_base_laws=len(bases),moved_laws=len(first)+len(second),prior_overlap_improvements=improvements,scope='Fixed reference, nodes15/17 independently displaced in boosted x over [-0.1,0.1]^2; unchanged 2104 rectangles. Exclusions rule out unchanged selected-node order AND symmetric physical weight gap>1/5 AND full conditional labelled count/overlap-law TV<=1/4. No general stability theorem; area is not probability.')
    return archive,summary

if __name__=='__main__':
    for name,result in zip(('certificates.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('unresolved_cells','prior_overlap_improvements')}),flush=True)
    print('SURFACE_OVERLAP_REFINEMENT_REPLAY_COMPLETE',flush=True)
