"""Transport previously certified labelled sub-observation tests to paired lines.
SPDX-License-Identifier: Apache-2.0
"""
from pf_common import *
from collections import Counter

def source_regions():
    source=read(HERE.parent/'continuous_energy/cells.json.gz');out=[]
    base=base_setup()
    for row in source['cells']:
        if row['status']!='LAW_EXCLUDED':continue
        node,axis,sign=source['rays'][row['ray']];law=row['law']
        pair=base['ends'][law['interval_index']]
        assert node in pair and len(set(pair)&set(range(5)))==1
        assert F(law['tv_lower'])>F(1,4)
        out.append(dict(source='continuous_energy',source_ray=row['ray'],source_path=row['path'],
            node=node,axis=axis,sign=sign,lo=row['lo'],hi=row['hi'],tv_lower=law['tv_lower'],intervals=[list(pair)]))
    joint=read(HERE.parent/'joint_ray_obstruction/certificate.json');domain=joint['domain']
    assert F(joint['full_law_tv_lower'])>F(1,4)
    assert [joint['statistics'][s]['interval'] for s in ('X','Y')]==[[2,15],[15,1]]
    out.append(dict(source='joint_ray_obstruction',node=domain['node'],axis=domain['axis'],sign=domain['sign'],
        lo=domain['h'][0],hi=domain['h'][1],tv_lower=joint['full_law_tv_lower'],intervals=[[2,15],[15,1]]))
    return out

def mapped_regions(ray,regions):
    out=[]
    for region in regions:
        if region['node'] not in ray['nodes'] or region['axis']!=ray['axis']:continue
        v=F(ray['velocities'][ray['nodes'].index(region['node'])]);assert v!=0
        lo,hi=sorted(F(region[k])*region['sign']/v for k in ('lo','hi'))
        lo=max(F(-1,10),lo);hi=min(F(1,10),hi)
        if lo<hi:out.append(dict(region,line_lo=str(lo),line_hi=str(hi)))
    return out

def run_transfer():
    frozen()
    for name,digest in read(HERE/'transfer_freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
    original=read(HERE/'cells.json.gz');rays=read(HERE.parent/'coordinated_motions/directions.json');regions=source_regions()
    all_records=[];line_summaries=[];signed=[];states=Counter();checks=0
    for line in original['lines']:
        ray=rays[line['ray']];available=mapped_regions(ray,regions)
        parents={p for level in line['splits'] for p in level};leaves=sorted((r for r in line['cells'] if r['path'] not in parents),key=lambda r:F(r['lo']))
        final=[];records=[]
        for old in leaves:
            if old['status']!='HOLD':final.append(old);continue
            lo,hi=F(old['lo']),F(old['hi']);points={lo,hi}
            for region in available:
                for k in ('line_lo','line_hi'):
                    value=F(region[k])
                    if lo<value<hi:points.add(value)
            points=sorted(points)
            for a,d in zip(points,points[1:]):
                eligible=[r for r in available if F(r['line_lo'])<=a<d<=F(r['line_hi'])]
                r=dict(parent=old['path'],lo=str(a),hi=str(d),status='HOLD')
                if eligible:
                    proof=eligible[0]
                    v=F(ray['velocities'][ray['nodes'].index(proof['node'])])
                    steps=sorted(v*h/proof['sign'] for h in (a,d))
                    assert F(proof['lo'])<=steps[0]<=steps[1]<=F(proof['hi'])
                    r.update(status='TRANSFERRED_LAW_EXCLUDED',source=proof,source_step_range=list(map(str,steps)));checks+=1
                final.append(r);records.append(r)
        cover(final,F(-1,10),F(1,10));counts=Counter(r['status'] for r in final);states.update(counts)
        pending=[]
        for r in final:
            if r['status']!='HOLD':continue
            if pending and pending[-1][1]==r['lo']:pending[-1][1]=r['hi']
            else:pending.append([r['lo'],r['hi']])
        for sign,index in ((-1,line['ray']-1),(1,line['ray'])):
            hold=any(r['status']=='HOLD' and ((sign<0 and F(r['lo'])<0) or (sign>0 and F(r['hi'])>0)) for r in final)
            signed.append(dict(ray=index,status='HOLD' if hold else 'EXCLUDED'))
        line_summaries.append(dict(ray=line['ray'],states=dict(counts),unresolved_intervals=pending))
        all_records.append(dict(ray=line['ray'],cells=records))
    excluded=[r['ray'] for r in signed if r['status']=='EXCLUDED'];pending=[r['ray'] for r in signed if r['status']=='HOLD']
    return dict(lines=all_records),dict(status='PAIRED_FAMILY_EXCLUDED' if not pending else 'HOLD_PAIRED_FAMILY',
        inherited_excluded_signed_rays=[0,1],new_excluded_signed_rays=excluded,
        total_excluded_signed_rays=2+len(excluded),unresolved_signed_rays=pending,
        complete_new_lines=[r['ray'] for r in line_summaries if not r['unresolved_intervals']],
        source_marginal_regions=len(regions)-1,source_joint_regions=1,
        transferred_subcells=checks,final_states=dict(states),lines=line_summaries,
        scope='Probability tests only are transported. No single-support operator-gap or support-support order certificate is transported. All unresolved intervals retained; no arbitrary coordinated-motion stability claim.')

if __name__=='__main__':
    for name,result in zip(('transfer_cells.json.gz','combined_summary.json'),run_transfer()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps({k:v for k,v in result.items() if k!='lines'}),flush=True)
