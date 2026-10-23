"""Read-only signed-half-ray accounting of the frozen continuous cover.
SPDX-License-Identifier: Apache-2.0
"""
from pf_common import *
from collections import Counter

def summarize():
    frozen();archive=read(HERE/'cells.json.gz');summary=read(HERE/'summary.json')
    rays=[]
    for line in archive['lines']:
        parents={p for level in line['splits'] for p in level}
        leaves=[r for r in line['cells'] if r['path'] not in parents]
        cover(leaves,F(-1,10),F(1,10))
        for sign,index,lo,hi in ((-1,line['ray']-1,F(-1,10),F(0)),(1,line['ray'],F(0),F(1,10))):
            cells=[]
            for r in leaves:
                a=max(lo,F(r['lo']));d=min(hi,F(r['hi']))
                if a<d:cells.append(dict(r,lo=str(a),hi=str(d)))
            cover(cells,lo,hi)
            pending=[]
            for r in sorted(cells,key=lambda v:F(v['lo'])):
                if r['status']!='HOLD':continue
                if pending and pending[-1][1]==r['lo']:pending[-1][1]=r['hi']
                else:pending.append([r['lo'],r['hi']])
            # Report magnitude s>=0 in that signed ray's original convention.
            if sign<0:pending=[[str(-F(b)),str(-F(a))] for a,b in reversed(pending)]
            rays.append(dict(ray=index,status='CONTINUOUS_SIGNED_RAY_EXCLUDED' if not pending else 'HOLD_SIGNED_RAY',
                unresolved_step_intervals=pending,states=dict(Counter(r['status'] for r in cells))))
    closed=[r['ray'] for r in rays if not r['unresolved_step_intervals']]
    pending=[r['ray'] for r in rays if r['unresolved_step_intervals']]
    assert sorted(closed+pending)==list(range(2,60))
    assert {v for index in summary['completely_excluded_new_lines'] for v in (index-1,index)}<=set(closed)
    result=dict(status='PAIRED_SIGNED_FAMILY_EXCLUDED' if not pending else 'HOLD_SIGNED_FAMILY',
        all_signed_rays=60,inherited_excluded_signed_rays=[0,1],new_excluded_signed_rays=closed,
        total_excluded_signed_ray_count=len(closed)+2,unresolved_signed_rays=pending,
        unresolved_signed_ray_count=len(pending),new_complete_lines=summary['completely_excluded_new_lines'],rays=rays,
        scope='Each signed ray has magnitude s in [0,0.1]; unresolved intervals are in that signed convention. The original line summary counts only rays inherited from fully closed lines; this report also recognizes individually closed half-lines. No additional classifier or adaptive evaluation.')
    return result

if __name__=='__main__':
    result=summarize()
    if '--verify' in sys.argv:assert result==read(HERE/'direction_summary.json')
    else:save(HERE/'direction_summary.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='rays'}),flush=True)
