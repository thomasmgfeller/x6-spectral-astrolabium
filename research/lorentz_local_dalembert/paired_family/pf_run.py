"""Frozen bounded campaign; preserve every unresolved parameter interval.
SPDX-License-Identifier: Apache-2.0
"""
from pf_common import *
from collections import Counter

def run():
    frozen();c=read(HERE/'contract.json');base=base_setup()
    base['basemeans']=means(base['w'],base['z'],base['ends'],base['pi'])
    rays=read(HERE.parent/'coordinated_motions/directions.json')
    start,end=map(F,c['interval']);archives=[];summaries=[]
    for index in c['positive_ray_indices']:
        ray=rays[index];assert ray['index']==index and ray['sign']==1
        negative=rays[index-1]
        assert negative['nodes']==ray['nodes'] and negative['axis']==ray['axis']
        assert list(map(F,negative['velocities']))==[-F(v) for v in ray['velocities']]
        b=setup(base,ray);rows=[];active={};splits=[]
        def append(path,lo,hi):
            row=dict(path=path,lo=str(lo),hi=str(hi),**classify(b,lo,hi,c))
            rows.append(row);active[path]=row
        n=c['uniform_cells']
        for j in range(n):append(str(j),start+(end-start)*j/n,start+(end-start)*(j+1)/n)
        for _ in range(c['refinement_rounds']):
            pending=sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:c['maximum_parents_per_round']]
            splits.append([r['path'] for r in pending])
            for row in pending:
                a,d=F(row['lo']),F(row['hi']);m=(a+d)/2;del active[row['path']]
                append(row['path']+'/0',a,m);append(row['path']+'/1',m,d)
            if not pending:break
        leaves=sorted(active.values(),key=lambda r:F(r['lo']));cover(leaves,start,end)
        unresolved=[]
        for row in leaves:
            if row['status']!='HOLD':continue
            if unresolved and unresolved[-1][1]==row['lo']:unresolved[-1][1]=row['hi']
            else:unresolved.append([row['lo'],row['hi']])
        summary=dict(ray=index,nodes=ray['nodes'],axis=ray['axis'],evaluated_cells=len(rows),terminal_cells=len(leaves),
                     states=dict(Counter(r['status'] for r in leaves)),unresolved_intervals=unresolved)
        summaries.append(summary);archives.append(dict(ray=index,base_statistics=b['base_statistics'],splits=splits,cells=rows))
        print(json.dumps(summary),flush=True)
    states=Counter()
    for s in summaries:states.update(s['states'])
    closed=[s['ray'] for s in summaries if not s['unresolved_intervals']]
    summary=dict(status='CONTINUOUS_REMAINING_PAIRED_FAMILY_EXCLUDED' if len(closed)==len(summaries) else 'HOLD_PAIRED_FAMILY',
        interval=c['interval'],new_lines=len(summaries),new_signed_rays=2*len(summaries),
        completely_excluded_new_lines=closed,completely_excluded_new_signed_rays=2*len(closed),
        inherited_excluded_signed_rays=[0,1],total_completely_excluded_signed_rays=2+2*len(closed),
        total_declared_signed_rays=60,states=dict(states),evaluated_cells=sum(s['evaluated_cells'] for s in summaries),
        terminal_cells=sum(s['terminal_cells'] for s in summaries),lines=summaries,
        scope='Fixed base geometry and 30 frozen lines only. HOLD is not a counterexample. No arbitrary coordinated-motion or general stability theorem.')
    return dict(lines=archives),summary

if __name__=='__main__':
    for name,result in zip(('cells.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert json.loads(json.dumps(result))==read(HERE/name),name
        else:save(HERE/name,result)
    print('PAIRED_FAMILY_REPLAY_COMPLETE',flush=True)
