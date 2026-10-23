"""Frozen full marginal pass, then bounded geometry-ranked overlap events.
SPDX-License-Identifier: Apache-2.0
"""
from sft_common import *

def run():
    frozen();c=read(HERE/'contract.json');old,previous,old_final,pending=inputs();b=setup(c)
    events=[];event_cache={};marginals=[];overlaps=[];base_cache={};base_ids={};base_laws=[]
    for row in pending:
        marginals.append(marginal(b,row,c,events,event_cache))
        if len(marginals)%100==0:print(json.dumps(dict(marginal_cells=len(marginals),states=dict(Counter(r['status'] for r in marginals)),distinct_events=len(events))),flush=True)
    chosen=sorted((r for r in marginals if r['status']=='HOLD'),key=lambda r:overlap_priority(b,r))[:c['maximum_overlap_cells']]
    for r in chosen:
        result=overlap(b,r,c,base_cache)
        if 'base_law' in result:
            key=(result['anchor'],result['threshold']);base=result.pop('base_law')
            if key not in base_ids:base_ids[key]=len(base_laws);base_laws.append(dict(anchor=key[0],threshold=key[1],law=base))
            result['base_law_id']=base_ids[key]
        overlaps.append(result)
        if len(overlaps)%16==0:print(json.dumps(dict(overlap_cells=len(overlaps),states=dict(Counter(v['status'] for v in overlaps)))),flush=True)
    archive=dict(marginal_events=events,marginal=marginals,overlap_base_laws=base_laws,overlap=overlaps)
    final=combined(archive);areas=Counter();states=Counter(r['status'] for r in final)
    for r in final:areas[r['status']]+=area(r)
    total=F(previous['total_area']);held=areas['HOLD'];assert sum(areas.values())==total
    selected={r['path'] for r in pending};new=[r for r in final if r['path'] in selected];unresolved=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    new_excluded=[r for r in new if r['status']!='HOLD'];lower=[]
    for r in new_excluded:
        if r['status']=='OVERLAP_TAIL_EXCLUDED':lower.append(r['tv_lower'])
        else:lower.append(events[r['attempts'][-1]['event_id']]['certificate']['full_law_tv_lower'])
    tested_overlap={r['path'] for r in old['overlap']}|{r['path'] for r in overlaps}
    summary=dict(status='TWO_PARAMETER_SQUARE_EXCLUDED' if not unresolved else 'HOLD_SURFACE_TAIL',source_hold_cells=775,source_untested_cells=len(pending),unchanged_previously_tested_holds=31,new_states=dict(Counter(r['status'] for r in new)),newly_excluded_cells=len(new_excluded),newly_excluded_area=str(sum((area(r) for r in new_excluded),F(0))),minimum_new_full_law_tv_lower=min(lower,key=F,default=None),terminal_cells=len(final),states=dict(states),areas={k:str(v) for k,v in areas.items()},total_area=str(total),hold_area=str(held),excluded_area_fraction=str(1-held/total),excluded_area_percent=outward(100*(1-held/total)),unresolved_cells=unresolved,marginal_cells_tested=len(marginals),marginal_attempts=sum(len(r['attempts']) for r in marginals),distinct_marginal_events=len(events),overlap_cells_tested=len(overlaps),distinct_overlap_base_laws=len(base_laws),remaining_without_new_exact_event=0,remaining_without_overlap_event=sum(r['status']=='HOLD' and r['path'] not in tested_overlap for r in final),scope='Same 2104 rectangles covering nodes15/17 independent boosted-x square [-0.1,0.1]^2 at one fixed reference. All 744 previously untested HOLD rectangles receive fixed-budget marginal attempts; up to128 new failures receive one geometry-ranked overlap event. HOLD is unresolved, area is not probability, no general stability claim.')
    return archive,summary

if __name__=='__main__':
    for name,result in zip(('certificates.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps({k:v for k,v in result.items() if k!='unresolved_cells'}),flush=True);print('SURFACE_TAIL_REPLAY_COMPLETE',flush=True)
