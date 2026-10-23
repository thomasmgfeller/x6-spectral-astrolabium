"""Exact finite-count tests on the inherited paired-family HOLD cells.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'paired_family'))
from pf_common import (F,read,save,outward,base_setup,means,mean_bounds,qpoly,qrange,interval,
    sqrt_bounds,cm,cover,boosted)
from pto_run import event_certificate
import jr_run as jr
HERE=Path(__file__).resolve().parent

def frozen():
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def setup(base,ray):
    b=dict(base,ray=ray,velocities=[F(0)]*21)
    for n,v in zip(ray['nodes'],ray['velocities']):b['velocities'][n]=F(v)
    return b

def inputs():
    old=read(HERE.parent/'paired_family/combined_summary.json')
    archive=read(HERE.parent/'paired_family/transfer_cells.json.gz');rows=[]
    for line in archive['lines']:
        for r in sorted(line['cells'],key=lambda x:F(x['lo'])):
            if r['status']=='HOLD':rows.append(dict(index=len(rows),ray=line['ray'],parent=r['parent'],lo=r['lo'],hi=r['hi']))
    assert len(rows)==old['final_states']['HOLD']==574
    return old,rows

def require_disjoint(b,node,xpair,ypair):
    assert node>=5 and {tuple(xpair),tuple(ypair)}=={(2,node),(node,1)}
    assert tuple(xpair) in b['ends'] and tuple(ypair) in b['ends']
    assert b['boost'][2][0]<b['boost'][node][0]<b['boost'][1][0]
    assert b['ray']['axis'] in (1,2)

def joint_certificate(b,lo,hi,node,xpair,ypair,coefficient,threshold,c):
    require_disjoint(b,node,xpair,ypair)
    pairs=[xpair,ypair];qs=[qrange(b,*p,lo,hi) for p in pairs]
    if any(q[0]<=0 for q in qs):return dict(tv_lower='0',reason='NONPOSITIVE_WHOLE_CELL_Q')
    base=[b['basemeans'][b['ends'].index(tuple(p))] for p in pairs]
    alt=[mean_bounds(b,q) for q in qs]
    if max(base[0]+alt[0])>F(c['maximum_short_mean']):return dict(tv_lower='0',reason='SHORT_MEAN_BUDGET')
    jc=dict(c['joint_probability'],event=dict(x_coefficient=coefficient,threshold=threshold))
    cache=b['joint_base_cache'];key=(node,tuple(xpair),coefficient,threshold)
    try:
        if key not in cache:cache[key]=jr.enclose_event(*base,jc)
        p,pr=cache[key];q,qr=jr.enclose_event(*alt,jc)
    except AssertionError:
        return dict(tv_lower='0',reason='FIXED_PROBABILITY_BUDGET_UNRESOLVED')
    tv=max(F(0),p[0]-q[1],q[0]-p[1])
    return dict(tv_lower=outward(tv)[0],node=node,X=list(xpair),Y=list(ypair),coefficient=coefficient,threshold=threshold,
        base_mean_intervals=[[str(x) for x in m] for m in base],moved_mean_intervals=[[str(x) for x in m] for m in alt],
        q_ranges=[[str(x) for x in q] for q in qs],base_probability=outward(*p,digits=60),moved_probability=outward(*q,digits=60),
        records=dict(base=pr,moved=qr))

def strip_certificate(base,c):
    d=c['strip'];b=setup(base,dict(nodes=[15],axis=1,velocities=['-1']))
    cert=joint_certificate(b,*map(F,d['step_interval']),15,[2,15],[15,1],d['coefficient'],d['threshold'],c)
    return dict(domain=d,**cert)

def marginal_candidates(b,lo,hi):
    rows=[]
    for index,pair in enumerate(b['ends']):
        if not set(pair)&set(b['ray']['nodes']):continue
        q=qrange(b,*pair,lo,hi)
        if q[0]<=0:continue
        a=b['basemeans'][index];d=mean_bounds(b,q)
        if not(a[1]<d[0] or d[1]<a[0]):continue
        ra=(sqrt_bounds(a[0])[0],sqrt_bounds(a[1])[1]);rd=(sqrt_bounds(d[0])[0],sqrt_bounds(d[1])[1])
        distance=max(F(0),ra[0]-rd[1],rd[0]-ra[1]);score=distance*distance/2
        rows.append(dict(index=index,pair=list(pair),base=a,moved=d,score=score))
    return sorted(rows,key=lambda r:(-r['score'],r['index']))

def joint_candidates(b,lo,hi,c):
    rows=[]
    for node in b['ray']['nodes']:
        pairs=[(2,node),(node,1)]
        if not all(p in b['ends'] for p in pairs):continue
        # X is the shorter base interval, which keeps the frozen PMF tail budget useful.
        pairs.sort(key=lambda p:(sum(b['basemeans'][b['ends'].index(p)]),p))
        xpair,ypair=pairs;require_disjoint(b,node,xpair,ypair)
        qs=[qrange(b,*p,lo,hi) for p in pairs]
        if any(q[0]<=0 for q in qs):continue
        base=[b['basemeans'][b['ends'].index(p)] for p in pairs];alt=[mean_bounds(b,q) for q in qs]
        if max(base[0]+alt[0])>F(c['maximum_short_mean']):continue
        for a in c['joint_coefficients']:
            mean0=(base[1][0]-a*base[0][1],base[1][1]-a*base[0][0])
            mean1=(alt[1][0]-a*alt[0][1],alt[1][1]-a*alt[0][0])
            separation=max(F(0),mean0[0]-mean1[1],mean1[0]-mean0[1])
            variance=base[1][1]+a*a*base[0][1]+alt[1][1]+a*a*alt[0][1]
            score=separation*separation/variance
            midpoint=(sum(mean0)+sum(mean1))/4;threshold=midpoint.__floor__()
            rows.append(dict(node=node,X=list(xpair),Y=list(ypair),coefficient=a,threshold=threshold,score=score))
    return sorted(rows,key=lambda r:(-r['score'],r['node'],r['coefficient']))

def classify(b,lo,hi,strip,c):
    if b['ray']['axis']==1 and F(strip['tv_lower'])>F(c['tv_gate']):
        steps=sorted(-b['velocities'][15]*h for h in (lo,hi));a,d=map(F,c['strip']['step_interval'])
        if a<=steps[0]<=steps[1]<=d:
            return dict(status='STRIP_JOINT_EXCLUDED',tv_lower=strip['tv_lower'],strip_steps=list(map(str,steps)))
    marginal=[];joint=[]
    for candidate in marginal_candidates(b,lo,hi)[:c['maximum_marginal_tests_per_cell']]:
        if max(candidate['base']+candidate['moved'])>c['poisson']['maximum_mean']:continue
        cert=event_certificate(candidate['base'],candidate['moved'],c['poisson'])
        marginal.append(dict(index=candidate['index'],pair=candidate['pair'],score=str(candidate['score']),
            base_mean=[str(x) for x in candidate['base']],moved_mean=[str(x) for x in candidate['moved']],certificate=cert))
        if F(cert['full_law_tv_lower'])>F(c['tv_gate']):
            return dict(status='MARGINAL_TAIL_EXCLUDED',tv_lower=cert['full_law_tv_lower'],marginal=marginal,joint=joint)
    for candidate in joint_candidates(b,lo,hi,c)[:c['maximum_joint_tests_per_cell']]:
        cert=joint_certificate(b,lo,hi,candidate['node'],candidate['X'],candidate['Y'],candidate['coefficient'],candidate['threshold'],c)
        joint.append(dict(candidate={k:str(v) if k=='score' else v for k,v in candidate.items()},certificate=cert))
        if F(cert['tv_lower'])>F(c['tv_gate']):
            return dict(status='DISJOINT_JOINT_EXCLUDED',tv_lower=cert['tv_lower'],marginal=marginal,joint=joint)
    best=max([F(0)]+[F(r['certificate']['full_law_tv_lower']) for r in marginal]+[F(r['certificate']['tv_lower']) for r in joint])
    return dict(status='HOLD',tv_lower=outward(best)[0],marginal=marginal,joint=joint)
