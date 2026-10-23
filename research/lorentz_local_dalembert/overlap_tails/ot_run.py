"""Frozen overlap-intensity slicing on the last 38 paired subcells.
SPDX-License-Identifier: Apache-2.0
"""
from ot_common import *
from collections import Counter

def run():
    frozen();c=read(HERE/'contract.json');old,pending=inputs();base=base_setup()
    rays=read(HERE.parent/'coordinated_motions/directions.json');cache={};bases={};rows=[]
    for r in pending:
        if r['ray'] not in bases:bases[r['ray']]=setup(base,rays[r['ray']])
        b=bases[r['ray']]
        rows.append(dict(r,**classify(b,F(r['lo']),F(r['hi']),c,cache)))
        if len(rows)%5==0:print(json.dumps(dict(completed=len(rows),states=dict(Counter(v['status'] for v in rows)))),flush=True)
    lines=[];closed=[]
    for line in old['lines']:
        current=[r for r in rows if r['ray']==line['ray']];pending=[]
        for lo,hi in line['unresolved_intervals']:
            cover([r for r in current if F(lo)<=F(r['lo'])<F(r['hi'])<=F(hi)],F(lo),F(hi))
        for r in current:
            if r['status']!='HOLD':continue
            if pending and pending[-1][1]==r['lo']:pending[-1][1]=r['hi']
            else:pending.append([r['lo'],r['hi']])
        for sign,index in ((-1,line['ray']-1),(1,line['ray'])):
            if index not in old['unresolved_signed_rays']:continue
            if not any((sign<0 and F(a)<0) or (sign>0 and F(d)>0) for a,d in pending):closed.append(index)
        if current:lines.append(dict(ray=line['ray'],unresolved_intervals=pending,states=dict(Counter(r['status'] for r in current))))
    pending=sorted(set(old['unresolved_signed_rays'])-set(closed));states=Counter(r['status'] for r in rows)
    final=Counter(old['combined_states']);del final['HOLD'];final.update(states)
    summary=dict(status='FROZEN_60_SIGNED_PAIRED_RAYS_EXCLUDED' if not pending else 'HOLD_OVERLAP_DIFFERENCE',
        inherited_excluded_signed_rays=58,newly_excluded_signed_rays=sorted(closed),total_excluded_signed_rays=58+len(closed),
        unresolved_signed_rays=pending,source_hold_cells=len(rows),new_states=dict(states),combined_states=dict(final),
        overlap_slices_per_law=c['overlap_slices'],event_attempts=sum(len(r['attempts']) for r in rows),
        distinct_base_law_enclosures=len(cache),minimum_new_excluded_full_law_tv_lower=min((r['tv_lower'] for r in rows if r['status']!='HOLD'),key=F,default=None),
        lines=lines,scope='The 60 frozen fixed-base signed paired rays, step magnitudes [0,0.1], only. Excludes unchanged-order, weight-gap >20%, full conditional count/overlap-law TV<=1/4 conjunction. Not arbitrary two-support motion or general stability.')
    return rows,summary

if __name__=='__main__':
    for name,result in zip(('certificates.json.gz','summary.json'),run()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps(result),flush=True);print('OVERLAP_TAIL_REPLAY_COMPLETE',flush=True)
