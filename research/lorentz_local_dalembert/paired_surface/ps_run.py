"""Frozen quadtree cover of two independently displaced supports.
SPDX-License-Identifier: Apache-2.0
"""
from ps_common import *
from collections import Counter
from pc_common import event_certificate

def marginal_candidates(b,box):
    candidates=[]
    for index,pair in enumerate(b['ends']):
        if not any(n in b['nodes'] for n in pair):continue
        q=qrange(b,*pair,box)
        if q[0]<=0:continue
        a=b['basemeans'][index];d=mean_bounds(b,q);sep=max(F(0),a[0]-d[1],d[0]-a[1]);score=sep*sep/(a[1]+d[1])
        candidates.append(dict(index=index,base=a,moved=d,score=score))
    return sorted(candidates,key=lambda x:(-x['score'],x['index']))

def marginal(b,r,c):
    attempts=[]
    for v in marginal_candidates(b,list(map(F,r['box'])))[:c['maximum_marginal_events_per_cell']]:
        if max(v['base']+v['moved'])>c['poisson']['maximum_mean']:
            attempts.append(dict(index=v['index'],reason='HOLD_RATE_BUDGET'));continue
        cert=event_certificate(v['base'],v['moved'],c['poisson'])
        attempts.append(dict(index=v['index'],score=str(v['score']),base=list(map(str,v['base'])),moved=list(map(str,v['moved'])),certificate=cert))
        if F(cert['full_law_tv_lower'])>F(c['tv_gate']):return dict(path=r['path'],box=r['box'],status='MARGINAL_TAIL_EXCLUDED',attempts=attempts)
    return dict(path=r['path'],box=r['box'],status='HOLD',attempts=attempts)

def overlap_candidates(b,box):
    rows=[]
    for k,side in b['common_anchors']:
        alt=statistics(b,box,k,side)
        if alt is None:continue
        base=b['base_statistics'][k];a,d=[tuple(map(F,v['mean'])) for v in (base,alt)]
        sep=max(F(0),a[0]-d[1],d[0]-a[1]);variance=F(base['variance_upper'])+F(alt['variance_upper'])
        rows.append(dict(anchor=k,side=side,base=base,moved=alt,score=sep*sep/variance if variance else F(0),threshold=((sum(a)+sum(d))/4).__floor__()))
    return sorted(rows,key=lambda r:(-r['score'],r['anchor']))

def overlap(b,r,c,cache):
    choices=overlap_candidates(b,list(map(F,r['box'])))
    if not choices:return dict(path=r['path'],box=r['box'],status='HOLD',reason='NO_TIMELIKE_ANCHOR')
    v=choices[0];key=(v['anchor'],v['threshold'])
    if key not in cache:cache[key]=enclose_difference(v['base'],v['threshold'],c['overlap'])
    base=cache[key];alt=enclose_difference(v['moved'],v['threshold'],c['overlap']);p,q=[tuple(map(F,x['probability'])) for x in (base,alt)]
    tv=max(F(0),p[0]-q[1],q[0]-p[1])
    return dict(path=r['path'],box=r['box'],status='OVERLAP_TAIL_EXCLUDED' if tv>F(c['tv_gate']) else 'HOLD',anchor=v['anchor'],side=v['side'],threshold=v['threshold'],score=str(v['score']),base_statistics=v['base'],moved_statistics=v['moved'],base_law=base,moved_law=alt,tv_lower=outward(tv)[0])

def final_cells(archive):
    parents={p for level in archive['splits'] for p in level};active={r['path']:r for r in archive['cells'] if r['path'] not in parents}
    for stage in ('marginal','overlap'):
        for r in archive[stage]:assert active[r['path']]['status']=='HOLD';active[r['path']]=r
    return sorted(active.values(),key=lambda r:tuple(map(int,r['path'].split('/'))))

def run():
    frozen();c=read(HERE/'contract.json');b=setup(c);inventory=strips(b);n=c['grid_per_axis'];lo,hi=map(F,c['domain']);active={};rows=[];splits=[]
    for i in range(n):
        for j in range(n):
            box=[lo+(hi-lo)*i/n,lo+(hi-lo)*(i+1)/n,lo+(hi-lo)*j/n,lo+(hi-lo)*(j+1)/n]
            r=dict(path=str(i*n+j),box=list(map(str,box)),**classify(b,box,c,inventory));rows.append(r);active[r['path']]=r
        if (i+1)%4==0:print(json.dumps(dict(grid_rows=i+1,states=dict(Counter(r['status'] for r in active.values())))),flush=True)
    for level in range(c['refinement_rounds']):
        selected=sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:c['maximum_parents_per_round']]
        if not selected:break
        splits.append([r['path'] for r in selected])
        for r in selected:
            del active[r['path']]
            for child in children(r):
                child.update(classify(b,list(map(F,child['box'])),c,inventory));rows.append(child);active[child['path']]=child
        print(json.dumps(dict(refinement=level+1,states=dict(Counter(r['status'] for r in active.values())))),flush=True)
    ms=[];os=[];cache={}
    for r in sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:c['maximum_marginal_cells']]:
        result=marginal(b,r,c);ms.append(result);active[r['path']]=result
    print(json.dumps(dict(marginal_cells=len(ms),states=dict(Counter(r['status'] for r in active.values())))),flush=True)
    for r in sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:c['maximum_overlap_cells']]:
        result=overlap(b,r,c,cache);os.append(result);active[r['path']]=result
        if len(os)%4==0:print(json.dumps(dict(overlap_cells=len(os),states=dict(Counter(r['status'] for r in active.values())))),flush=True)
    archive=dict(strips=inventory,cells=rows,splits=splits,marginal=ms,overlap=os)
    final=final_cells(archive);areas=Counter();counts=Counter(r['status'] for r in final);total=(hi-lo)**2
    for r in final:areas[r['status']]+=area(r)
    assert sum(areas.values())==total
    held=areas['HOLD'];pending=[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    summary=dict(status='TWO_PARAMETER_SQUARE_EXCLUDED' if not pending else 'HOLD_TWO_PARAMETER_SQUARE',nodes=c['nodes'],axis=c['axis'],domain=c['domain'],initial_cells=n*n,evaluated_geometric_cells=len(rows),terminal_cells=len(final),states=dict(counts),areas={k:str(v) for k,v in areas.items()},total_area=str(total),hold_area=str(held),excluded_area_fraction=str(1-held/total),excluded_area_percent=outward(100*(1-held/total)),unresolved_cells=pending,marginal_cells_tested=len(ms),marginal_events=sum(len(r['attempts']) for r in ms),overlap_cells_tested=len(os),distinct_overlap_base_laws=len(cache),scope='Fixed reference; nodes15/17 independent boosted-x displacements in [-0.1,0.1]^2. Exclusions rule out unchanged order AND symmetric weight gap>20% AND full conditional count/overlap-law TV<=1/4. HOLD is not a counterexample; area is parameter-space area, not probability. No general stability claim.')
    return archive,summary

if __name__=='__main__':
    for name,data in zip(('certificates.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
    print(json.dumps({k:v for k,v in data.items() if k!='unresolved_cells'}),flush=True);print('PAIRED_SURFACE_REPLAY_COMPLETE',flush=True)
