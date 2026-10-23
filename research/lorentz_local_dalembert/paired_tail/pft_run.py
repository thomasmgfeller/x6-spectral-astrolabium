"""One frozen finite-count pass over all 574 inherited unresolved cells.
SPDX-License-Identifier: Apache-2.0
"""
from pft_common import *
from collections import Counter

def run():
    frozen();c=read(HERE/'contract.json');old,source=inputs();base=base_setup()
    base['basemeans']=means(base['w'],base['z'],base['ends'],base['pi']);base['joint_base_cache']={}
    rays=read(HERE.parent/'coordinated_motions/directions.json');strip=strip_certificate(base,c)
    rows=[];last=None
    for r in source:
        if r['ray']!=last:b=setup(base,rays[r['ray']]);last=r['ray']
        rows.append(dict(r,**classify(b,F(r['lo']),F(r['hi']),strip,c)))
        if len(rows)%50==0:print(json.dumps(dict(completed=len(rows),states=dict(Counter(v['status'] for v in rows)))),flush=True)
    lines=[];newly_closed=[]
    for line in old['lines']:
        current=[r for r in rows if r['ray']==line['ray']];pending=[]
        for lo,hi in line['unresolved_intervals']:
            cells=[r for r in current if F(lo)<=F(r['lo'])<F(r['hi'])<=F(hi)];cover(cells,F(lo),F(hi))
        for r in current:
            if r['status']!='HOLD':continue
            if pending and pending[-1][1]==r['lo']:pending[-1][1]=r['hi']
            else:pending.append([r['lo'],r['hi']])
        for sign,index in ((-1,line['ray']-1),(1,line['ray'])):
            if index not in old['unresolved_signed_rays']:continue
            if not any((sign<0 and F(a)<0) or (sign>0 and F(d)>0) for a,d in pending):newly_closed.append(index)
        lines.append(dict(ray=line['ray'],unresolved_intervals=pending,new_states=dict(Counter(r['status'] for r in current))))
    pending=sorted(set(old['unresolved_signed_rays'])-set(newly_closed));states=Counter(r['status'] for r in rows)
    final=Counter(old['final_states']);del final['HOLD'];final.update(states)
    summary=dict(status='FROZEN_60_SIGNED_PAIRED_RAYS_EXCLUDED' if not pending else 'HOLD_PAIRED_TAILS',
        inherited_excluded_signed_rays=old['total_excluded_signed_rays'],newly_excluded_signed_rays=sorted(newly_closed),
        total_excluded_signed_rays=old['total_excluded_signed_rays']+len(newly_closed),unresolved_signed_rays=pending,
        source_hold_cells=len(source),new_states=dict(states),combined_states=dict(final),
        strip_uniform_full_law_tv_lower=strip['tv_lower'],
        minimum_new_excluded_full_law_tv_lower=min((r['tv_lower'] for r in rows if r['status']!='HOLD'),key=F,default=None),
        marginal_events=sum(len(r.get('marginal',[])) for r in rows),joint_events=sum(len(r.get('joint',[])) for r in rows),lines=lines,
        scope='Only the 60 predeclared fixed-base paired rays for magnitudes [0,0.1]. Excludes unchanged-order, symmetric weight gap >20%, full conditional count-law TV<=1/4 conjunction. No arbitrary coordinated-motion or general stability theorem.')
    return strip,rows,summary

if __name__=='__main__':
    for name,result in zip(('strip_certificate.json','certificates.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps({k:v for k,v in result.items() if k!='lines'}),flush=True)
    print('PAIRED_TAIL_REPLAY_COMPLETE',flush=True)
