"""Continuous cover of the inherited node-15/node-5 coupled spatial line.
SPDX-License-Identifier: Apache-2.0
"""
from pc_common import *
from collections import Counter

def run():
    frozen();c=read(HERE/'contract.json');b=setup(c);lo,hi=map(F,c['interval'])
    # A separate whole-neighborhood certificate, not a grid approximation.
    a,d=map(F,c['focus_interval']);focus=joint_bounds(b,a,d,c)
    focus=dict(interval=c['focus_interval'],base_probability=outward(*b['joint_base'],digits=60),
               base_records=b['joint_base_records'],**focus)
    rows=[];active={};splits=[]
    def add(path,a,d):
        row=dict(path=path,lo=str(a),hi=str(d),**classify(b,a,d,c));rows.append(row);active[path]=row
    n=c['uniform_cells']
    for j in range(n):
        add(str(j),lo+(hi-lo)*j/n,lo+(hi-lo)*(j+1)/n)
        if j%16==15:print(json.dumps(dict(initial=j+1,states=dict(Counter(v['status'] for v in active.values())))),flush=True)
    for _ in range(c['refinement_rounds']):
        pending=sorted((v for v in active.values() if v['status']=='HOLD'),key=lambda v:(-(F(v['hi'])-F(v['lo'])),tuple(map(int,v['path'].split('/')))))[:c['maximum_parents_per_round']]
        splits.append([v['path'] for v in pending])
        for row in pending:
            a,d=F(row['lo']),F(row['hi']);m=(a+d)/2;del active[row['path']]
            add(row['path']+'/0',a,m);add(row['path']+'/1',m,d)
        print(json.dumps(dict(round=len(splits),split=len(pending),evaluated=len(rows),states=dict(Counter(v['status'] for v in active.values())))),flush=True)
        if not pending:break
    terminal=sorted(active.values(),key=lambda v:F(v['lo']))
    assert F(terminal[0]['lo'])==lo and F(terminal[-1]['hi'])==hi
    assert all(F(a['hi'])==F(d['lo']) for a,d in zip(terminal,terminal[1:]))
    unresolved=[]
    for row in terminal:
        if row['status']!='HOLD':continue
        if unresolved and unresolved[-1][1]==row['lo']:unresolved[-1][1]=row['hi']
        else:unresolved.append([row['lo'],row['hi']])
    summary=dict(status='CONTINUOUS_PAIRED_LINE_EXCLUDED' if not unresolved else 'HOLD_PAIRED_INTERVALS',
        interval=c['interval'],nodes=c['nodes'],velocities=c['velocities'],
        sampled_rays_from_PR111_covered=[0,1],evaluated_cells=len(rows),terminal_cells=len(terminal),
        states=dict(Counter(v['status'] for v in terminal)),unresolved_intervals=unresolved,
        focus_interval=c['focus_interval'],focus_uniform_full_law_tv_lower=focus['tv_lower'],
        focus_excluded=F(focus['tv_lower'])>F(c['tv_gate']),
        scope='Every h on this one coupled line, both signs, is covered by explicit cells. Exclusions apply to the unchanged-order, weight-gap >20%, full conditional count/overlap-law TV<=1/4 conjunction. HOLD cells are not counterexamples. Other 58 paired rays, arbitrary deformations and general stability remain open.')
    return focus,dict(splits=splits,cells=rows),summary

if __name__=='__main__':
    for name,result in zip(('focus.json','cells.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps(read(HERE/'summary.json')))
