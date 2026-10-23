"""Independent exact geometry, direct nine-moment solves and cover audit.
SPDX-License-Identifier: Apache-2.0
"""
from pc_common import *
from pc_overlap import terminal_cells
from collections import Counter
from decimal import Decimal
from jr_audit import decimal_reference

def direct_q(a,b):
    t,x,y=[v-u for u,v in zip(a,b)]
    return t*t-x*x-y*y

def cover(leaves,lo,hi):
    items=sorted(leaves,key=lambda r:F(r['lo']))
    assert items and F(items[0]['lo'])==lo and F(items[-1]['hi'])==hi
    assert all(F(r['lo'])<F(r['hi']) for r in items)
    assert all(F(a['hi'])==F(d['lo']) for a,d in zip(items,items[1:]))

def audit():
    frozen();c=read(HERE/'contract.json');b=setup(c)
    archive=read(HERE/'cells.json.gz');summary=read(HERE/'summary.json');focus=read(HERE/'focus.json')
    rows={r['path']:r for r in archive['cells']};assert len(rows)==len(archive['cells'])
    start,end=map(F,c['interval']);n=c['uniform_cells']
    assert {str(k) for k in range(n)}.issubset(rows)
    active={str(k):rows[str(k)] for k in range(n)}
    for k in range(n):
        assert F(rows[str(k)]['lo'])==start+(end-start)*k/n
        assert F(rows[str(k)]['hi'])==start+(end-start)*(k+1)/n
    for level in archive['splits']:
        expected=sorted((r for r in active.values() if r['status']=='HOLD'),key=lambda v:(-(F(v['hi'])-F(v['lo'])),tuple(map(int,v['path'].split('/')))))[:c['maximum_parents_per_round']]
        assert level==[r['path'] for r in expected]
        for path in level:
            old=active.pop(path);a,d=F(old['lo']),F(old['hi']);m=(a+d)/2
            for child,lo,hi in ((path+'/0',a,m),(path+'/1',m,d)):
                assert F(rows[child]['lo'])==lo and F(rows[child]['hi'])==hi
                active[child]=rows[child]
    leaves=terminal_cells(archive);assert {r['path'] for r in leaves}==set(active)
    assert len(rows)==n+2*sum(map(len,archive['splits']))
    cover(leaves,start,end)
    assert Counter(r['status'] for r in leaves)==summary['states']
    # Missing a terminal cell must invalidate a claimed continuous cover.
    try:cover(leaves[1:],start,end)
    except AssertionError:pass
    else:raise AssertionError('gapped cover accepted')
    moment_checks=0;quadratic_checks=0
    # Direct 9x9 rational moments independently test the 4x4 update at all 64 coarse centers.
    for k in range(n):
        h=start+(end-start)*F(2*k+1,2*n);zz=cm.moved(b['z'],b['ray'],h)
        truth=exact_weights(zz,F(b['w']['scale']));g,d,eta=solve_cell(b,h,h,c)
        assert eta==0 and all(v.contains(a-old) for v,a,old in zip(d,truth,b['weights']));moment_checks+=1
        for i,j in ((5,15),(5,1),(15,1),(2,5),(2,15),(3,5),(5,4)):
            polynomial=qpoly(b,i,j)
            assert sum(coef*h**power for power,coef in enumerate(polynomial))==direct_q(zz[i],zz[j]);quadratic_checks+=1
    for r in leaves:
        lo,hi=F(r['lo']),F(r['hi'])
        if r['status']=='GAP_EXCLUDED':
            assert F(r['gap_upper'])<=F(1,5) and F(r['neumann_norm_upper'])<1
            bounds=[tuple(map(F,p)) for p in r['weight_change_bounds']]
            for h in (lo,(lo+hi)/2,hi):
                truth=exact_weights(cm.moved(b['z'],b['ray'],h),F(b['w']['scale']))
                assert all(a<=v-old<=d for (a,d),v,old in zip(bounds,truth,b['weights']));moment_checks+=1
        elif r['status']=='JOINT_LAW_EXCLUDED':assert F(r['joint']['tv_lower'])>F(1,4)
        elif r['status']=='MARGINAL_LAW_EXCLUDED':assert F(r['marginal']['tv_lower'])>F(1,4)
        elif r['status']=='ORDER_EXCLUDED':assert invalid_order(b,lo,hi)==r['pair']
        else:assert r['status']=='HOLD'
        for i,j in ((5,15),(5,1),(15,1),(2,5),(2,15)):
            a,d=qrange(b,i,j,lo,hi)
            for h in (lo,(lo+hi)/2,hi):
                zz=cm.moved(b['z'],b['ray'],h)
                assert a<=direct_q(zz[i],zz[j])<=d;quadratic_checks+=1
    # Cross term must not be dropped when both interval endpoints move.
    vi,vj=b['velocities'][5],b['velocities'][15]
    assert qpoly(b,5,15)[2]!=-(vi*vi+vj*vj)
    try:solve_cell(b,F(-10),F(10),c)
    except (AssertionError,StopIteration,ZeroDivisionError):pass
    else:raise AssertionError('uncontracted whole-domain solve accepted')
    probability_checks=0
    for record in focus['base_records']+focus['records']:
        p=decimal_reference(F(record['x_mean']),F(record['y_mean']),2,891)
        assert Decimal(record['probability'][0])<=p<=Decimal(record['probability'][1]);probability_checks+=1
        assert all(int(record['normalization'][v]['tail'])>0 for v in ('x','y'))
    joint=joint_bounds(b,*map(F,c['focus_interval']),c)
    assert joint['tv_lower']==focus['tv_lower']
    # The focus law is valid throughout this actual admissible neighborhood.
    # Boosted times do not change; q bounds preserve all 210 oriented relations.
    focus_order_checks=0
    for i in range(21):
      for j in range(i+1,21):
        a,d=qrange(b,i,j,*map(F,c['focus_interval']));q0=interval(b['z'],i,j)
        assert (q0>0 and a>=F(99,10**10)) or (q0<0 and d<=-F(99,10**10))
        focus_order_checks+=1
    p,q=map(lambda v:tuple(map(F,v)),(focus['base_probability'],focus['probability']))
    assert F(focus['tv_lower'])<=max(F(0),p[0]-q[1],q[0]-p[1])
    return dict(status='PASS',terminal_cover_cells=len(leaves),exact_nine_moment_comparisons=moment_checks,
        direct_quadratic_checks=quadratic_checks,independent_110_digit_focus_pmf_checks=probability_checks,
        whole_focus_order_pairs=focus_order_checks,
        deterministic_refinement_checked=True,
        negative_controls=['missing coverage cell rejected','two-endpoint cross term retained','uncontracted large interval rejected'],
        scope='Arithmetic and implementation checks; whole-cell validity comes from the written interval inequalities.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
