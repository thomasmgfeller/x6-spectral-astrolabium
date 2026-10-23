"""Covariance-aware difference-count obstruction on inherited HOLD cells.
SPDX-License-Identifier: Apache-2.0
"""
from pc_common import *

def terminal_cells(archive):
    parents={p for level in archive['splits'] for p in level}
    return sorted((r for r in archive['cells'] if r['path'] not in parents),key=lambda r:F(r['lo']))

def variance_enclosure(b,lo,hi):
    # A=I(5,1), B=I(15,1); the later boosted tip is node 15.
    a,j,k=5,15,1
    dt=b['boost'][j][0]-b['boost'][a][0]
    Ttip=b['boost'][k][0]-b['boost'][j][0]
    assert dt>0 and Ttip>0
    pair=qrange(b,a,j,lo,hi)
    assert dt*dt-pair[0]>=0
    rhi=sqrt_bounds(dt*dt-pair[0])[1]
    delay=max(F(0),rhi-dt)
    qa=qrange(b,a,k,lo,hi);qb=qrange(b,j,k,lo,hi)
    assert qa[0]>0 and qb[0]>0
    ma,mb=mean_bounds(b,qa),mean_bounds(b,qb)
    # v(h)=(t15+max(0,|s15-s5|-dt),s15). I(v,1) lies in A intersect B.
    qsub=qb[0]-2*Ttip*delay+delay*delay
    submean=F(0)
    if delay<Ttip and qsub>0:submean=mean_bounds(b,(qsub,qsub))[0]
    variance=ma[1]+mb[1]-2*submean
    assert variance>=0
    return dict(mean=[str(ma[0]-mb[1]),str(ma[1]-mb[0])],variance_upper=str(variance),
        count_mean_intervals=[[str(x) for x in m] for m in (ma,mb)],
        common_future_tip_delay_upper=str(delay),common_interval_q_lower=str(qsub),
        common_interval_mean_lower=str(submean),pair_q_range=[str(x) for x in pair])

def difference_event(base,alt):
    a=tuple(map(F,base['mean']));d=tuple(map(F,alt['mean']))
    va=F(base['variance_upper']);vd=F(alt['variance_upper'])
    # Deterministic midpoint threshold, no search over thresholds.
    midpoint=(sum(a)+sum(d))/4;k=midpoint.numerator//midpoint.denominator
    if a[1]<d[0]:low,high=a,d;vl,vh=va,vd
    elif d[1]<a[0]:low,high=d,a;vl,vh=vd,va
    else:return dict(tv_lower='0',threshold=k,reason='OVERLAPPING_MEAN_ENCLOSURES')
    left=F(k+1)-low[1];right=high[0]-k
    if left<=0 or right<=0:return dict(tv_lower='0',threshold=k,reason='THRESHOLD_NOT_BETWEEN_MEANS')
    # For E={D<=k}, low law has P(E)>=1-vl/(vl+left^2),
    # high law has P(E)<=vh/(vh+right^2). D is integer valued.
    eleft=vl/(vl+left*left);eright=vh/(vh+right*right)
    tv=max(F(0),1-eleft-eright)
    return dict(tv_lower=outward(tv)[0],threshold=k,
        low_law_event_probability_lower=outward(1-eleft)[0],
        high_law_event_probability_upper=outward(eright)[1],
        cantelli_tail_upper=[str(eleft),str(eright)])

def run_overlap():
    for name,digest in read(HERE/'overlap_freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
    c=read(HERE/'contract.json');oc=read(HERE/'overlap_contract.json');b=setup(c)
    old=read(HERE/'summary.json');archive=read(HERE/'cells.json.gz');leaves=terminal_cells(archive)
    pending=[r for r in leaves if r['status']=='HOLD'];assert len(pending)==old['states'].get('HOLD',0)
    base=variance_enclosure(b,F(0),F(0));rows=[]
    for row in pending:
        lo,hi=F(row['lo']),F(row['hi'])
        try:
            alt=variance_enclosure(b,lo,hi);event=difference_event(base,alt)
        except AssertionError:
            rows.append(dict(path=row['path'],lo=row['lo'],hi=row['hi'],status='HOLD',reason='GEOMETRIC_ENCLOSURE_UNRESOLVED'));continue
        rows.append(dict(path=row['path'],lo=row['lo'],hi=row['hi'],
            status='DIFFERENCE_LAW_EXCLUDED' if F(event['tv_lower'])>F(oc['tv_gate']) else 'HOLD',
            variance=alt,event=event))
    lookup={r['path']:r for r in rows};unresolved=[];counts={}
    for leaf in leaves:
        r=lookup.get(leaf['path'],leaf);counts[r['status']]=counts.get(r['status'],0)+1
        if r['status']!='HOLD':continue
        if unresolved and unresolved[-1][1]==r['lo']:unresolved[-1][1]=r['hi']
        else:unresolved.append([r['lo'],r['hi']])
    excluded=[r for r in rows if r['status']=='DIFFERENCE_LAW_EXCLUDED']
    summary=dict(status='CONTINUOUS_PAIRED_LINE_EXCLUDED' if not unresolved else 'HOLD_PAIRED_INTERVALS',
        interval=c['interval'],paired_rays_from_PR111_covered=[0,1],terminal_cells=len(leaves),states=counts,
        original_unresolved_cells=len(pending),newly_excluded_cells=len(excluded),
        unresolved_intervals=unresolved,
        minimum_difference_full_law_tv_lower=min((r['event']['tv_lower'] for r in excluded),key=F,default=None),
        focus_interval=old['focus_interval'],focus_uniform_full_law_tv_lower=old['focus_uniform_full_law_tv_lower'],
        scope='Complete domain coverage of the one fixed node-15/node-5 coupled x line; every cell either excluded or explicitly HOLD. Other 58 paired rays and general stability remain open.')
    return dict(base=base,rows=rows),summary

if __name__=='__main__':
    for name,result in zip(('overlap_certificates.json','combined_summary.json'),run_overlap()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps(read(HERE/'combined_summary.json')))
