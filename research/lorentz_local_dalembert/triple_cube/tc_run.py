"""Frozen 8x8x8 cube, two bounded octree rounds and bounded exact events.
SPDX-License-Identifier: Apache-2.0
"""
from tc_common import *

def run():
    frozen();c=read(HERE/'contract.json');b=setup(c);inventory=source_inventory(b);strips=node5_strips(b)
    lo,hi=map(F,c['domain']);n=c['grid_per_axis'];rows=[];active={};splits=[];pcache={}
    for i,j,k in itertools.product(range(n),repeat=3):
        box=[]
        for pos in (i,j,k):box.extend((lo+(hi-lo)*pos/n,lo+(hi-lo)*(pos+1)/n))
        r=dict(path=str((i*n+j)*n+k),box=list(map(str,box)),**classify(b,box,c,inventory,strips,pcache));rows.append(r);active[r['path']]=r
        if len(rows)%64==0:print(json.dumps(dict(initial_cells=len(rows),states=dict(Counter(v['status'] for v in active.values())))),flush=True)
    for level in range(c['refinement_rounds']):
        chosen=sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:c['maximum_parents_per_round']]
        if not chosen:break
        splits.append([r['path'] for r in chosen])
        for parent in chosen:
            del active[parent['path']]
            for child in children(parent):
                child.update(classify(b,list(map(F,child['box'])),c,inventory,strips,pcache));rows.append(child);active[child['path']]=child
        print(json.dumps(dict(refinement=level+1,states=dict(Counter(v['status'] for v in active.values())))),flush=True)
    marginal_rows=[];events=[];mcache={};overlap_rows=[];bases=[];ocache={}
    for row in sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:c['maximum_marginal_cells']]:
        r=marginal(b,row,c,events,mcache);marginal_rows.append(r);active[r['path']]=r
    print(json.dumps(dict(marginal_cells=len(marginal_rows),states=dict(Counter(v['status'] for v in active.values())))),flush=True)
    for row in sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:c['maximum_overlap_cells']]:
        r=overlap(b,row,c,bases,ocache);overlap_rows.append(r);active[r['path']]=r
        print(json.dumps(dict(overlap_cells=len(overlap_rows),path=r['path'],status=r['status'],tv_lower=r.get('tv_lower'))),flush=True)
    ar=dict(projection_sources=inventory,node5_strips=strips,cells=rows,splits=splits,marginal_events=events,marginal=marginal_rows,overlap_base_laws=bases,overlap=overlap_rows)
    final=final_cells(ar);volumes=Counter();states=Counter(r['status'] for r in final)
    for r in final:volumes[r['status']]+=volume(r)
    total=(hi-lo)**3;held=volumes['HOLD'];assert sum(volumes.values())==total
    holds=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    tested={r['path'] for r in marginal_rows}|{r['path'] for r in overlap_rows}
    summary=dict(status='THREE_PARAMETER_CUBE_EXCLUDED' if not holds else 'HOLD_THREE_PARAMETER_CUBE',nodes=c['nodes'],axis=c['axis'],domain=c['domain'],initial_cells=n**3,evaluated_geometric_cells=len(rows),terminal_cells=len(final),states=dict(states),volumes={k:str(v) for k,v in volumes.items()},total_volume=str(total),hold_volume=str(held),excluded_volume_fraction=str(1-held/total),excluded_volume_percent=outward(100*(1-held/total)),unresolved_cells=holds,marginal_cells_tested=len(marginal_rows),marginal_attempts=sum(len(r['attempts']) for r in marginal_rows),distinct_marginal_events=len(events),overlap_cells_tested=len(overlap_rows),distinct_overlap_base_laws=len(bases),remaining_without_new_exact_event=sum(r['path'] not in tested for r in holds),inherited_zero_third_slice_fully_excluded=True,operator_enclosure_failures=sum(r.get('operator',{}).get('status')=='HOLD_RANK_OR_ENCLOSURE' for r in rows),scope='One fixed reference in 2+1 Minkowski, nodes15/17/5 independent boosted-x displacements in [-0.1,0.1]^3. Strong target: unchanged order AND symmetric physical weight gap>20% AND full conditional count/overlap-law TV<=1/4. Parameter volume is not probability. HOLD is unresolved, not a counterexample; no general stability theorem.')
    return ar,summary

if __name__=='__main__':
    for name,result in zip(('certificates.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps({k:v for k,v in result.items() if k!='unresolved_cells'}),flush=True);print('TRIPLE_CUBE_REPLAY_COMPLETE',flush=True)
