"""Exhaustive interval cover of 64 fixed-base single-node spatial rays.
SPDX-License-Identifier: Apache-2.0
"""
from ce_common import *
from itertools import product
from collections import Counter

def run():
    frozen();c=read(HERE/'contract.json');base=setup();r=c['rays'];rays=[list(v) for v in product(r['nodes'],r['axes'],r['signs'])]
    raycache=[ray_data(base,*v) for v in rays];start,end=map(F,r['interval']);n=c['uniform_cells_per_ray']
    rows=[];active={}
    def add(ray,path,lo,hi):
        result=classify(base,raycache[ray],lo,hi,c)
        row=dict(ray=ray,path=path,lo=str(lo),hi=str(hi),**result)
        rows.append(row);active[(ray,path)]=row
    for j,ray in enumerate(rays):
        for k in range(n):add(j,str(k),start+(end-start)*k/n,start+(end-start)*(k+1)/n)
        print(json.dumps(dict(ray=j,completed=len(rows),states=dict(Counter(x['status'] for x in rows)))),flush=True)
    splits=[]
    for _ in range(c['refinement_rounds']):
        pending=sorted((v for v in active.values() if v['status']=='HOLD'),key=lambda x:(-(F(x['hi'])-F(x['lo'])),x['ray'],tuple(map(int,x['path'].split('/')))))[:c['maximum_parents_per_round']]
        splits.append([[x['ray'],x['path']] for x in pending])
        for old in pending:
            lo,hi=F(old['lo']),F(old['hi']);mid=(lo+hi)/2;del active[(old['ray'],old['path'])]
            add(old['ray'],old['path']+'/0',lo,mid);add(old['ray'],old['path']+'/1',mid,hi)
        print(json.dumps(dict(refinement=len(splits),split=len(pending),evaluated=len(rows),states=dict(Counter(x['status'] for x in active.values())))),flush=True)
    holds=[]
    for j,ray in enumerate(rays):
        items=sorted((v for v in active.values() if v['ray']==j),key=lambda x:F(x['lo']))
        assert F(items[0]['lo'])==start and F(items[-1]['hi'])==end
        assert all(F(a['hi'])==F(b['lo']) for a,b in zip(items,items[1:]))
        merged=[]
        for v in items:
            if v['status']!='HOLD':continue
            if merged and merged[-1][1]==v['lo']:merged[-1][1]=v['hi']
            else:merged.append([v['lo'],v['hi']])
        if merged:holds.append(dict(ray=j,node=ray[0],axis=ray[1],sign=ray[2],intervals=merged))
    states=dict(Counter(x['status'] for x in active.values()))
    summary=dict(status='CONTINUOUS_FAMILY_EXCLUDED' if not holds else 'HOLD_CONTINUOUS_INTERVALS',rays=len(rays),interval=r['interval'],
        evaluated_cells=len(rows),active_cells=len(active),states=states,unresolved_rays=len(holds),unresolved_intervals=holds,
        original_grid_gap_addressed=True,scope='All h in [0,0.1] covered on 64 single-node rays from one fixed base. Excluded cells cannot satisfy the unchanged-order, >20% gap and TV<=1/4 conjunction. HOLD cells are unresolved, not witnesses or close-law certificates. No coordinated-motion, arbitrary-pair or global stability claim.')
    return dict(rays=rays,splits=splits,cells=rows),summary

if __name__=='__main__':
    for name,data in zip(('cells.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
