"""Independent coverage, exact-operator, energy and compatibility controls.
SPDX-License-Identifier: Apache-2.0
"""
from ce_common import *
from ce_energy import laplacian,dual_squared
from ce_compat import path_trace
from collections import Counter

def check_cover(leaves,rays,start,end):
    for ray in range(rays):
        intervals=sorted((F(v['lo']),F(v['hi'])) for v in leaves if v['ray']==ray)
        assert intervals and intervals[0][0]==start and intervals[-1][1]==end
        assert all(lo<hi for lo,hi in intervals)
        assert all(a[1]==b[0] for a,b in zip(intervals,intervals[1:]))

def audit():
    frozen();c=read(HERE/'contract.json');archive=read(HERE/'cells.json.gz');summary=read(HERE/'summary.json');base=setup()
    cells={(v['ray'],v['path']):v for v in archive['cells']};assert len(cells)==len(archive['cells'])
    n=c['uniform_cells_per_ray'];start,end=map(F,c['rays']['interval']);active={}
    for ray in range(64):
        for j in range(n):
            v=cells[(ray,str(j))];assert F(v['lo'])==start+(end-start)*j/n and F(v['hi'])==start+(end-start)*(j+1)/n
            active[(ray,str(j))]=v
    for split in archive['splits']:
        expected=sorted((v for v in active.values() if v['status']=='HOLD'),key=lambda v:(-(F(v['hi'])-F(v['lo'])),v['ray'],tuple(map(int,v['path'].split('/')))))[:c['maximum_parents_per_round']]
        assert split==[[v['ray'],v['path']] for v in expected]
        for key in map(tuple,split):
            parent=active.pop(key);lo,hi=F(parent['lo']),F(parent['hi']);mid=(lo+hi)/2
            for suffix,a,b in [('0',lo,mid),('1',mid,hi)]:
                new=(key[0],key[1]+'/'+suffix);v=cells[new];assert (F(v['lo']),F(v['hi']))==(a,b);active[new]=v
    check_cover(list(active.values()),64,start,end)
    assert dict(Counter(v['status'] for v in active.values()))==summary['states']
    assert len(active)==summary['active_cells'] and len(cells)==summary['evaluated_cells']
    references=interval_points=quadratic_points=0;selected=[]
    for j,params in enumerate(archive['rays']):
        ray=ray_data(base,*params)
        for h in (F(3,100),F(1,10)):
            dw,_=delta_weights(base,ray,h);zz=deform(base['z'],*params,h)
            assert [a+b for a,b in zip(base['weights'],dw)]==exact_weights(zz,F(base['w']['scale']));references+=1
            for other in range(21):
                if other==ray['node']:continue
                q=q_bounds(base,ray,ray['node'],other,h,h)
                assert q==(interval(zz,ray['node'],other),)*2;quadratic_points+=1
        seen=set()
        for v in sorted((v for v in active.values() if v['ray']==j),key=lambda v:F(v['lo'])):
            if v['status'] in seen:continue
            selected.append(v);seen.add(v['status'])
    for v in active.values():
        if v['status']=='GAP_EXCLUDED':assert F(v['gap_upper'])<=F(c['gap_gate'])
        elif v['status']=='LAW_EXCLUDED':assert F(v['law']['tv_lower'])>F(c['tv_gate'])
        elif v['status']=='HOLD':assert F(v['gap_upper'])>F(c['gap_gate']) and F(v['law']['tv_lower'])<=F(c['tv_gate'])
        else:assert v['status']=='ORDER_EXCLUDED'
    for v in selected:
        ray=ray_data(base,*archive['rays'][v['ray']]);lo,hi=F(v['lo']),F(v['hi'])
        if v['status']=='ORDER_EXCLUDED':
            i,j=v['pair'];q=q_bounds(base,ray,i,j,lo,hi);original=interval(base['z'],i,j)
            assert (original>0 and q[1]<=0) or (original<0 and q[0]>=0)
            continue
        if 'determinant' in v:
            g,deltas,_=gap_upper(base,ray,lo,hi);assert outward(g)[1]==v['gap_upper']
            for h in (lo,(lo+hi)/2,hi):
                exact,_=delta_weights(base,ray,h);assert all(a.contains(b) for a,b in zip(deltas,exact));interval_points+=1
        if 'law' in v and v['law']['method']!='NONE':
            law=v['law'];i,j=base['ends'][law['interval_index']]
            a,b=[tuple(map(F,x)) for x in law['mean_intervals']]
            assert a==mean_bounds(base,(interval(base['z'],i,j),)*2)
            assert b==mean_bounds(base,q_bounds(base,ray,i,j,lo,hi))
            if law['method']=='HELLINGER':assert lower_bound(a,b)[1]>=F(law['tv_lower'])
            else:assert event_certificate(a,b,c['poisson'])['full_law_tv_lower']==law['tv_lower']
    graph=read(HERE/'energy_graph.json');edges=graph['directed_hasse_edges'];L=laplacian(21,edges);Q=[[F(v) for v in row] for row in graph['grounded_inverse']]
    assert all(sum(row)==0 for row in L)
    assert all(dot(Q[i],col)==int(i==j) for i in range(20) for j,col in enumerate(zip(*[r[1:] for r in L[1:]])))
    witness=graph['witness'];v=list(map(F,witness['delta']));x=list(map(F,witness['grounded_potential']));sq=F(witness['squared_dual_norm'])
    assert mv(L,x)==v and dot(v,x)==dot(x,mv(L,x))==sq
    assert dual_squared(v,[[a/2 for a in row] for row in Q])==sq/2
    permutation=list(reversed(range(21)));P=[[L[i][j] for j in permutation] for i in permutation]
    Qp=inv([r[1:] for r in P[1:]])
    assert dual_squared([v[i] for i in permutation],Qp)==sq
    comp=read(HERE/'compatibility.json');polynomial_checks=0
    for level in comp['levels']:
        n=level['subdivision'];ell=F(1,n)
        # Integrate independently expanded polynomials, not stored closed forms.
        integral=sum(a*ell**(j+1)/(j+1) for j,a in enumerate([F(0),ell,F(-1)]))
        energy=sum(a*ell**(j+1)/(j+1) for j,a in enumerate([ell*ell,-4*ell,F(4)]))
        assert n*integral==F(level['saturating_bubble_error'])
        assert len(edges)*n*energy==F(level['saturating_bubble_energy'])
        assert (n*integral)**2==F(level['quadrature_constant_squared'])*len(edges)*n*energy
        assert path_trace(n,F(n))==[[F(1),F(-1)],[F(-1),F(1)]];polynomial_checks+=1
    invalid=0
    broken=list(active.values())[1:]
    for call in [lambda:check_cover(broken,64,start,end),lambda:laplacian(3,[(0,1)]),
                 lambda:laplacian(2,[(0,1)],F(-1)),lambda:dual_squared([F(1)]*21,Q),lambda:I(-1,1).inv()]:
        try:call()
        except AssertionError:invalid+=1;continue
        raise AssertionError('invalid control accepted')
    assert invalid==5
    return dict(status='PASS',complete_continuous_covers=64,active_cells_checked=len(active),exact_independent_weight_solves=references,
        exact_moving_interval_identities=quadratic_points,sampled_interval_weight_enclosures=interval_points,
        sampled_certificate_cells=len(selected),fixed_refinement_selection_verified=True,
        energy_duality=True,permutation_invariance=True,conductance_scale_control=True,
        trace_and_saturating_polynomial_levels=polynomial_checks,invalid_controls_rejected=invalid,
        scope='Exact identities and independent source solves validate the implementation; whole-interval coverage follows from directed intervals and the proofs in THEOREMS.md. Auxiliary energy results do not establish a Lorentzian continuum limit.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
