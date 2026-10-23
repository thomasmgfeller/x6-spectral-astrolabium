"""Independent direct moments, geometry, moment inequalities and cover checks.
SPDX-License-Identifier: Apache-2.0
"""
from pf_common import *
from collections import Counter

def direct_q(a,b):
    t,x,y=[v-u for u,v in zip(a,b)]
    return t*t-x*x-y*y

def check_virtual(b,lo,hi,v):
    i,j=b['ray']['nodes'];k=v['anchor'];tip=v['tip'];sgn=v['time_sign']
    delay=F(v['delay_upper']);duration=F(v['duration']);qsub=F(v['common_q_lower'])
    dt=abs(b['boost'][i][0]-b['boost'][j][0]);qmin=F(v['pair_q_range'][0])
    assert delay>=0 and (dt+delay)**2>=dt*dt-qmin
    assert qsub==qrange(b,tip,k,lo,hi)[0]-2*duration*delay+delay*delay
    mu=[list(map(F,m)) for m in v['count_mean_intervals']];common=F(v['common_mean_lower'])
    assert F(v['variance_upper'])==mu[0][1]+mu[1][1]-2*common>=0
    assert list(map(F,v['mean']))==[mu[0][0]-mu[1][1],mu[0][1]-mu[1][0]]
    for h in (lo,(lo+hi)/2,hi):
        zz=boosted(cm.moved(b['z'],b['ray'],h));virtual=list(zz[tip]);virtual[0]+=sgn*delay
        for n in (i,j):
            assert sgn*(virtual[0]-zz[n][0])>=0 and direct_q(zz[n],virtual)>=0
        if common:
            assert delay<duration and qsub>0
            assert sgn*(zz[k][0]-virtual[0])>0
            q=direct_q(virtual,zz[k]);assert q>=qsub
            intensity=F(b['w']['rho'],12)*F(b['w']['scale'])**3*b['pi'][0]*q*sqrt_bounds(q)[0]
            assert 0<common<=intensity
        else:assert not(delay<duration and qsub>0)
    return v['side']

def check_event(base,alt,e):
    mb,ma=map(lambda r:tuple(map(F,r['mean'])),(base,alt))
    vb,va=F(base['variance_upper']),F(alt['variance_upper']);k=e['threshold']
    assert k==((sum(mb)+sum(ma))/4).__floor__()
    if ma[1]<mb[0]:small,big,vs,vh=ma,mb,va,vb
    elif mb[1]<ma[0]:small,big,vs,vh=mb,ma,vb,va
    else:assert F(e['tv_lower'])==0;return
    a=F(k+1)-small[1];d=big[0]-k
    if min(a,d)<=0:assert F(e['tv_lower'])==0;return
    direct=max(F(0),1-vs/(vs+a*a)-vh/(vh+d*d))
    assert F(e['tv_lower'])<=direct
    assert list(map(F,e['cantelli_tail_upper']))==[vs/(vs+a*a),vh/(vh+d*d)]

def audit():
    from pf_fast import install
    install()
    frozen();c=read(HERE/'contract.json');archive=read(HERE/'cells.json.gz');summary=read(HERE/'summary.json')
    amendment=read(HERE/'execution_amendment.json');initial=read(HERE/'freeze_initial.json')
    current=(HERE/'pf_run.py').read_text()
    original=current.replace("assert json.loads(json.dumps(result))==read(HERE/name)","assert result==read(HERE/name)")
    assert hashlib.sha256(original.encode()).hexdigest()==initial['files']['pf_run.py']==amendment['original_run_sha256']
    for name,digest in initial['files'].items():
        if name!='pf_run.py':assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest
    for known in amendment['known_partial_results']:
        observed=next(r for r in summary['lines'] if r['ray']==known['ray'])
        assert all(observed[k]==v for k,v in known.items())
    base=base_setup();base['basemeans']=means(base['w'],base['z'],base['ends'],base['pi'])
    rays=read(HERE.parent/'coordinated_motions/directions.json');start,end=map(F,c['interval'])
    assert [a['ray'] for a in archive['lines']]==c['positive_ray_indices']
    assert [s['ray'] for s in summary['lines']]==c['positive_ray_indices']
    assert set(c['positive_ray_indices'])==set(range(3,60,2))
    totals=Counter();checks=Counter();sides=Counter();closed=[]
    for line,line_summary in zip(archive['lines'],summary['lines']):
        b=setup(base,rays[line['ray']]);rows={r['path']:r for r in line['cells']};n=c['uniform_cells']
        assert len(rows)==len(line['cells']);active={str(k):rows[str(k)] for k in range(n)}
        assert {str(k):v for k,v in b['base_statistics'].items()}==line['base_statistics']
        for k in range(n):
            assert F(active[str(k)]['lo'])==start+(end-start)*k/n
            assert F(active[str(k)]['hi'])==start+(end-start)*(k+1)/n
        assert len(line['splits'])<=c['refinement_rounds']
        for level in line['splits']:
            expected=sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:c['maximum_parents_per_round']]
            assert level==[r['path'] for r in expected]
            for path in level:
                old=active.pop(path);lo,hi=F(old['lo']),F(old['hi']);mid=(lo+hi)/2
                for child,a,d in ((path+'/0',lo,mid),(path+'/1',mid,hi)):
                    assert [rows[child]['lo'],rows[child]['hi']]==list(map(str,(a,d)));active[child]=rows[child]
        assert len(rows)==n+2*sum(map(len,line['splits']))
        leaves=sorted(active.values(),key=lambda r:F(r['lo']));cover(leaves,start,end)
        assert len(line['splits'])==c['refinement_rounds'] or not any(r['status']=='HOLD' for r in leaves)
        try:cover(leaves[1:],start,end)
        except AssertionError:checks['gapped_cover_rejected']+=1
        else:raise AssertionError('missing cell accepted')
        counts=Counter(r['status'] for r in leaves);totals.update(counts)
        assert counts==line_summary['states']
        unresolved=[]
        for r in leaves:
            if r['status']=='HOLD':
                if unresolved and unresolved[-1][1]==r['lo']:unresolved[-1][1]=r['hi']
                else:unresolved.append([r['lo'],r['hi']])
        assert unresolved==line_summary['unresolved_intervals']
        if not unresolved:closed.append(line['ray'])
        checks['terminal_cells']+=len(leaves);checks['evaluated_cells']+=len(rows)
        i,j=b['ray']['nodes'];pairs=[(i,j)]+[(node,k) for node in (i,j) for k in (0,2)]
        for h in (start,F(-1,20),F(0),F(1,20),end):
            zz=cm.moved(b['z'],b['ray'],h);truth=exact_weights(zz,F(b['w']['scale']))
            _,change,eta=solve_cell(b,h,h,c)
            assert eta==0 and all(v.contains(a-old) for v,a,old in zip(change,truth,b['weights']))
            checks['direct_nine_moment_comparisons']+=1
            for a,d in pairs:
                assert sum(x*h**power for power,x in enumerate(qpoly(b,a,d)))==direct_q(zz[a],zz[d])
                checks['direct_quadratic_comparisons']+=1
        # Nonzero motion audits every available future and past construction.
        for k,side in b['common_anchors']:
            for lo,hi in ((F(0),F(0)),(F(-1,100),F(-9,1000)),(F(9,1000),F(1,100))):
                v=variance_enclosure(b,lo,hi,k,side)
                if v:sides[check_virtual(b,lo,hi,v)]+=1
        # Whole-cell gap bounds checked against a separate direct solve at three points.
        gap_cells=sorted((r for r in leaves if r['status']=='GAP_EXCLUDED'),key=priority)
        for r in gap_cells[:2]:
            bounds=[tuple(map(F,v)) for v in r['weight_change_bounds']]
            lo,hi=F(r['lo']),F(r['hi'])
            for h in (lo,(lo+hi)/2,hi):
                truth=exact_weights(cm.moved(b['z'],b['ray'],h),F(b['w']['scale']))
                assert all(a<=v-old<=d for (a,d),v,old in zip(bounds,truth,b['weights']))
                checks['direct_nine_moment_comparisons']+=1
        for r in leaves:
            lo,hi=F(r['lo']),F(r['hi']);status=r['status']
            if status=='ORDER_EXCLUDED':
                a,d=qrange(b,*r['pair'],lo,hi);q0=interval(b['z'],*r['pair'])
                assert (q0>0 and d<=0) or (q0<0 and a>=0)
            elif status=='GAP_EXCLUDED':assert F(r['gap_upper'])<=F(1,5) and F(r['neumann_norm_upper'])<1
            elif status=='DIFFERENCE_LAW_EXCLUDED':
                o=r['overlap'];v=o['variance'];e=o['event'];k=o['anchor']
                assert F(o['tv_lower'])==F(e['tv_lower'])>F(1,4)
                sides[check_virtual(b,lo,hi,v)]+=1;check_event(b['base_statistics'][k],v,e)
                checks['cantelli_events']+=1
            elif status=='MARGINAL_LAW_EXCLUDED':
                m=r['marginal'];a,d=[tuple(map(F,v)) for v in m['mean_intervals']]
                assert a==b['basemeans'][m['index']]
                assert d==mean_bounds(b,qrange(b,*b['ends'][m['index']],lo,hi))
                assert F(1,4)<F(m['tv_lower'])<=lower_bound(a,d)[1]
                checks['marginal_bounds']+=1
            else:assert status=='HOLD'
            for h in (lo,(lo+hi)/2,hi):
                zz=cm.moved(b['z'],b['ray'],h)
                for a,d in pairs:
                    lower,upper=qrange(b,a,d,lo,hi)
                    assert lower<=direct_q(zz[a],zz[d])<=upper
                    checks['direct_quadratic_comparisons']+=1
        vi,vj=b['velocities'][i],b['velocities'][j]
        assert qpoly(b,i,j)[2]!=-(vi*vi+vj*vj);checks['cross_terms_retained']+=1
        print(json.dumps(dict(audited_ray=line['ray'],checks=dict(checks))),flush=True)
    assert totals==summary['states']
    assert checks['terminal_cells']==summary['terminal_cells'] and checks['evaluated_cells']==summary['evaluated_cells']
    assert closed==summary['completely_excluded_new_lines']
    assert summary['total_completely_excluded_signed_rays']==2+2*len(closed)
    assert len(archive['lines'])==summary['new_lines']==29 and summary['new_signed_rays']==58
    # Synthetic Poisson exclusive atoms independently check the moment event.
    import jr_run as jr
    jc=read(HERE.parent/'paired_continuous/contract.json')['joint_probability']
    stats=[dict(mean=['30','30'],variance_upper='50'),dict(mean=['60','60'],variance_upper='80')]
    e=difference_event(*stats);k=e['threshold']
    p,_=jr.event(F(10),F(40),1,k,jc);q,_=jr.event(F(10),F(70),1,k,jc)
    assert F(e['tv_lower'])<=p[0]-q[1]<1
    assert difference_event(stats[0],stats[0])['tv_lower']=='0'
    assert difference_event(*stats)['tv_lower']==difference_event(*reversed(stats))['tv_lower']
    unsafe=[dict(s,variance_upper='0') for s in stats]
    assert F(difference_event(*unsafe)['tv_lower'])>p[1]-q[0]
    # Equal-time virtual tips and time reversal, independent synthetic geometry.
    for sign in (-1,1):
        a=[F(0),F(-1),F(0)];d=[F(0),F(1),F(0)];v=[F(2*sign),F(1),F(0)]
        assert sign*(v[0]-a[0])>=0 and direct_q(a,v)>=0 and direct_q(d,v)>=0
    inherited=read(HERE.parent/'paired_continuous/combined_summary.json')
    assert inherited['status']=='CONTINUOUS_PAIRED_LINE_EXCLUDED' and not inherited['unresolved_intervals']
    return dict(status='PASS',**dict(checks),whole_cell_virtual_tip_checks=dict(sides),rational_virtual_tip_checks=3*sum(sides.values()),
        deterministic_refinement_and_complete_cover=True,synthetic_product_poisson_comparison=True,
        controls=['missing coverage rejected on every line','moving-endpoint cross terms retained on both axes',
                  'equal means produce zero','law swap symmetry','underestimated variance fails Poisson control',
                  'equal tip times and time reversal'],scope='Direct tests audit implementations; whole-cell validity follows from the written exact inequalities.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
