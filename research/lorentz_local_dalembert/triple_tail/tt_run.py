"""Complete the frozen missing-event pass; never extend after results.
SPDX-License-Identifier: Apache-2.0
"""
from tt_common import *

def run():
    frozen();c=read(HERE/'contract.json');b=setup(c);old,previous,source,pending=inputs()
    assert len(pending)==c['maximum_marginal_cells']==c['expected_inputs']
    rows=[];events=[];mcache={}
    for index,row in enumerate(pending):
        rows.append(marginal(b,row,c,events,mcache))
        if (index+1)%32==0:print(json.dumps(dict(marginal_cells=index+1,states=dict(Counter(r['status'] for r in rows)),distinct_events=len(events))),flush=True)
    left=[r for r in rows if r['status']=='HOLD'];assert len(left)<=c['maximum_overlap_cells']
    overlaps=[];laws=[];ocache={}
    for index,row in enumerate(left):
        r=cached_overlap(b,row,c,laws,ocache);overlaps.append(r)
        print(json.dumps(dict(overlap_cells=index+1,path=r['path'],status=r['status'],tv_lower=r.get('tv_lower'),distinct_laws=len(laws))),flush=True)
    ar=dict(marginal_events=events,marginal=rows,overlap_laws=laws,overlap=overlaps)
    final=combined(ar);states=Counter(r['status'] for r in final);volumes=Counter()
    for r in final:volumes[r['status']]+=volume(r)
    total=F(1,125);held=volumes['HOLD'];assert sum(volumes.values())==total
    marg,ov=event_coverage(ar);valid=marg|ov;input_paths={r['path'] for r in pending}
    holds=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    marginal_min=[F(events[r['attempts'][-1]['event_id']]['certificate']['full_law_tv_lower']) for r in rows if r['status']=='MARGINAL_TAIL_EXCLUDED']
    overlap_min=[F(r['tv_lower']) for r in overlaps if r['status']=='OVERLAP_TAIL_EXCLUDED']
    summary=dict(status='THREE_PARAMETER_CUBE_EXCLUDED' if not held else 'HOLD_THREE_PARAMETER_CUBE',
        nodes=c['nodes'],axis=c['axis'],domain=c['domain'],terminal_cells=len(final),states=dict(states),volumes={k:str(v) for k,v in volumes.items()},
        total_volume=str(total),hold_volume=str(held),excluded_volume_fraction=str(1-held/total),excluded_volume_percent=outward(100*(1-held/total)),
        previous_excluded_volume_fraction=previous['excluded_volume_fraction'],new_excluded_volume=str(F(previous['hold_volume'])-held),
        new_marginal_exclusions=len(marginal_min),new_overlap_exclusions=len(overlap_min),
        minimum_new_marginal_tv_lower=str(min(marginal_min)) if marginal_min else None,minimum_new_overlap_tv_lower=str(min(overlap_min)) if overlap_min else None,
        marginal_input_cells=len(rows),marginal_attempts=sum(len(r['attempts']) for r in rows),distinct_marginal_events=len(events),
        marginal_inputs_with_enclosed_event=len(marg),marginal_skipped_reasons=dict(Counter(a['reason'] for r in rows for a in r['attempts'] if 'reason' in a)),
        overlap_input_cells=len(overlaps),overlap_inputs_with_both_laws_enclosed=len(ov),distinct_overlap_laws=len(laws),overlap_law_states=dict(Counter(r['law']['status'] for r in laws)),
        inputs_with_enclosed_event=len(valid),inputs_without_enclosed_event=len(input_paths-valid),
        preserved_previous_tested_holds=421-len(pending),remaining_new_inputs=sum(r['path'] in input_paths for r in holds),
        remaining_new_inputs_without_enclosed_event=sum(r['path'] in input_paths-valid for r in holds),unresolved_cells=holds,
        inherited_zero_third_slice_fully_excluded=True,
        scope='Fixed reference in 2+1 Minkowski, nodes15/17/5 independent boosted-x displacements in [-0.1,0.1]^3. Excludes unchanged order AND symmetric physical weight gap>20% AND full conditional labelled count/overlap-law TV<=1/4. Parameter volume is not probability. HOLD is unresolved; no general stability theorem.')
    return ar,summary

if __name__=='__main__':
    for name,result in zip(('certificates.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps({k:v for k,v in result.items() if k!='unresolved_cells'}),flush=True)
    print('TRIPLE_TAIL_REPLAY_COMPLETE',flush=True)
