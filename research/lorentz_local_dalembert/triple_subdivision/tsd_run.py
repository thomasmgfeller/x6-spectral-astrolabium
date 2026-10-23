"""All448 children, joint operator bounds, then bounded marginal/overlap tests.
SPDX-License-Identifier: Apache-2.0
"""
from tsd_common import *

def run():
    frozen();c=read(HERE/'contract.json');old,previous,source,pending=inputs();b=setup(c)
    invs,strips=transport_inventory();rows=[];pcache={}
    assert len(pending)==c['parent_cells']
    for parent in pending:
        for r in children(parent):
            r.update(classify(b,list(map(F,r['box'])),c,invs,strips,pcache));rows.append(r)
        if len(rows)%32==0:print(json.dumps(dict(geometric_cells=len(rows),states=dict(Counter(r['status'] for r in rows)))),flush=True)
    assert len(rows)==c['child_cells'];events=[];mcache={};marginals=[]
    left=sorted((r for r in rows if r['status']=='HOLD'),key=path_key);assert len(left)<=c['maximum_marginal_cells']
    for index,r in enumerate(left):
        marginals.append(marginal(b,r,c,events,mcache))
        if (index+1)%16==0:print(json.dumps(dict(marginal_cells=index+1,states=dict(Counter(r['status'] for r in marginals)),distinct_events=len(events))),flush=True)
    left=[r for r in marginals if r['status']=='HOLD'];assert len(left)<=c['maximum_overlap_cells'];overlaps=[];laws=[];ocache={}
    for r in left:
        v=cached_overlap(b,r,c,laws,ocache);overlaps.append(v)
        print(json.dumps(dict(overlap_cells=len(overlaps),total=len(left),path=v['path'],status=v['status'],tv_lower=v.get('tv_lower'),distinct_laws=len(laws))),flush=True)
    ar=dict(splits=[r['path'] for r in pending],cells=rows,marginal_events=events,marginal=marginals,overlap_laws=laws,overlap=overlaps)
    final=combined(ar);states=Counter(r['status'] for r in final);volumes=Counter()
    for r in final:volumes[r['status']]+=volume(r)
    total=F(previous['total_volume']);held=volumes['HOLD'];assert sum(volumes.values())==total
    child_paths={r['path'] for r in rows};new=[r for r in final if r['path'] in child_paths];new_states=Counter(r['status'] for r in new)
    holds=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD'];marg,ov=event_coverage(ar)
    active={r['path']:r for r in new}
    closed=[p['path'] for p in pending if all(active[p['path']+'/'+str(j)]['status']!='HOLD' for j in range(8))]
    mins=[events[r['attempts'][-1]['event_id']]['certificate']['full_law_tv_lower'] for r in marginals if r['status']=='MARGINAL_TAIL_EXCLUDED']
    ovs=[r['tv_lower'] for r in overlaps if r['status']=='OVERLAP_TAIL_EXCLUDED']
    summary=dict(status='THREE_PARAMETER_CUBE_EXCLUDED' if not held else 'HOLD_THREE_PARAMETER_CUBE',nodes=c['nodes'],axis=c['axis'],domain=c['domain'],
        source_hold_cells=len(pending),evaluated_child_cells=len(rows),geometric_child_states=dict(Counter(r['status'] for r in rows)),new_terminal_states=dict(new_states),
        fully_closed_source_parents=closed,source_exclusions_preserved=len(source)-len(pending),terminal_cells=len(final),states=dict(states),volumes={k:str(v) for k,v in volumes.items()},
        total_volume=str(total),hold_volume=str(held),newly_excluded_volume=str(F(previous['hold_volume'])-held),previous_excluded_volume_fraction=previous['excluded_volume_fraction'],
        excluded_volume_fraction=str(1-held/total),excluded_volume_percent=outward(100*(1-held/total)),unresolved_cells=holds,
        marginal_input_cells=len(marginals),marginal_attempts=sum(len(r['attempts']) for r in marginals),distinct_marginal_events=len(events),marginal_inputs_with_enclosed_event=len(marg),
        marginal_skipped_reasons=dict(Counter(a['reason'] for r in marginals for a in r['attempts'] if 'reason' in a)),overlap_input_cells=len(overlaps),overlap_inputs_with_both_laws_enclosed=len(ov),
        distinct_overlap_laws=len(laws),overlap_law_states=dict(Counter(r['law']['status'] for r in laws)),remaining_without_enclosed_new_event=sum(r['path'] not in marg|ov for r in holds),
        minimum_new_marginal_tv_lower=min(mins,key=F,default=None),minimum_new_overlap_tv_lower=min(ovs,key=F,default=None),
        finite_child_operator_enclosures=sum('gap_upper' in r.get('operator',{}) for r in rows),operator_enclosure_failures=sum(r.get('operator',{}).get('status')=='HOLD_RANK_OR_ENCLOSURE' for r in rows),
        inherited_zero_third_slice_fully_excluded=True,
        scope='Fixed reference in 2+1 Minkowski; independent boosted-x moves of nodes15/17/5 in [-0.1,0.1]^3. Excludes unchanged order AND inherited admissibility AND symmetric physical weight gap>1/5 AND full conditional labelled count/overlap-law TV<=1/4. Parameter volume is not probability; HOLD is unresolved and general stability remains open.')
    return ar,summary

if __name__=='__main__':
    for name,result in zip(('certificates.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('unresolved_cells','fully_closed_source_parents')}),flush=True)
    print('TRIPLE_SUBDIVISION_REPLAY_COMPLETE',flush=True)
