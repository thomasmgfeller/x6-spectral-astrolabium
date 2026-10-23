"""Exact paired-support screen; scalar cancellation is not vector cancellation.
SPDX-License-Identifier: Apache-2.0
"""
import sys, json, hashlib
from pathlib import Path
from collections import Counter
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent/'continuous_energy'))
from ce_common import F, read, save, outward, inv, dot
from ss_run import geometry, boosted, deform, exact_weights, certify_order, intrinsic_gates, gap
from ss_marginal import means, lower_bound, pi_bounds
from st_certificate import interval, sqrt_bounds
from pto_run import event_certificate

def frozen():
    for name, digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest() == digest, name

def mul(a,b):
    v=[x*y for x in a for y in b]
    return min(v),max(v)

def determinant(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
           -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
           +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))

def structure(z,ends):
    fixed=set(range(5)); blocks={i:[] for i in range(5,21)}; constants=[]
    for k,(i,j) in enumerate(ends):
        supports=set((i,j))-fixed
        assert len(supports)<=1
        if not supports:constants.append(k)
        else:blocks[next(iter(supports))].append(k)
    assert len(constants)==10
    for node,rows in blocks.items():
        assert len(rows)==5
        assert {v for k in rows for v in ends[k] if v in fixed}==fixed
    # Exact finite difference inverse; G=diag(1,-1,-1).
    A=[[-2*g*(z[a][j]-z[0][j]) for j,g in enumerate((1,-1,-1))] for a in (1,2,3)]
    Q=inv(A);det=determinant(A)
    assert det!=0
    return dict(constant_intervals=constants,blocks={str(k):v for k,v in blocks.items()},
                difference_matrix=[[str(v) for v in row] for row in A],
                inverse=[[str(v) for v in row] for row in Q],determinant=str(det),
                inverse_infinity_norm=str(max(sum(map(abs,row)) for row in Q)),
                exact_jacobian_rank=48,coordinate_dimensions=48,
                exact_mean_preserving_motion='ONLY_ZERO_WITH_FIXED_LANDMARKS',
                claim='Mean map injective with fixed nondegenerate landmarks; no numerical stability constant for operator weights is asserted.')

def directions(z,c):
    zz=boosted(z);p=c['pivot_node'];a=c['balance_anchor'];out=[]
    for j in c['partners']:
      for axis in c['axes']:
        g=[]
        for node in (p,j):
            q=interval(z,a,node);assert q>0
            v=zz[a][axis]-zz[node][axis]
            g.append(mul((v,v),sqrt_bounds(q)))
        assert not g[1][0]<=0<=g[1][1]
        ratios=[-x/y for x in g[0] for y in g[1]]
        midpoint=(min(ratios)+max(ratios))/2
        rounded=midpoint*c['coefficient_unit']+F(1,2)
        coefficient=F(rounded.numerator//rounded.denominator,c['coefficient_unit'])
        norm=max(F(1),abs(coefficient));v=(1/norm,coefficient/norm)
        assert all(v) and max(map(abs,v))==1
        terms=[mul(gi,(vi,vi)) for gi,vi in zip(g,v)]
        residual=tuple(sum(t[k] for t in terms) for k in (0,1))
        magnitude=sum(min(map(abs,t)) for t in terms)
        relative=max(map(abs,residual))/magnitude
        assert relative<F(1,10**10)
        for sign in c['signs']:
            out.append(dict(index=len(out),nodes=[p,j],axis=axis,sign=sign,
                velocities=[str(sign*x) for x in v],
                aggregate_derivative_relative_residual_upper=outward(relative)[1]))
    assert len(out)==c['rays']
    return out

def moved(z,ray,h):
    zz=z
    for node,v in zip(ray['nodes'],map(F,ray['velocities'])):
        zz=deform(zz,node,ray['axis'],1,h*v)
    return zz

def law_screen(base,alt,ends,c):
    ranked=sorted([(*lower_bound(a,b),k) for k,(a,b) in enumerate(zip(base,alt))],
                  key=lambda x:(-x[0],x[2]))
    exponent,tv,k=ranked[0]
    result=dict(tv_lower=outward(tv)[0],method='HELLINGER',interval_index=k,endpoints=list(ends[k]),
                mean_intervals=[[str(x) for x in v] for v in (base[k],alt[k])])
    if tv>F(c['tv_gate']):return result
    events=[]
    for _,_,k in ranked[:2]:
        a,b=base[k],alt[k]
        if not (a[1]<b[0] or b[1]<a[0]):continue
        if max(a+b)>c['poisson']['maximum_mean']:continue
        cert=event_certificate(a,b,c['poisson'])
        events.append(dict(interval_index=k,endpoints=list(ends[k]),
                           mean_intervals=[[str(x) for x in v] for v in (a,b)],certificate=cert))
        if F(cert['full_law_tv_lower'])>F(result['tv_lower']):
            result.update(tv_lower=cert['full_law_tv_lower'],method='POISSON_EVENT',
                          interval_index=k,endpoints=list(ends[k]),
                          mean_intervals=[[str(x) for x in v] for v in (a,b)])
        if F(result['tv_lower'])>F(c['tv_gate']):break
    result['event_checks']=events
    return result

def run():
    frozen();c=read(HERE/'contract.json');w,z,ends=geometry();scale=F(w['scale'])
    proof=structure(z,ends);rays=directions(z,c);weights=exact_weights(z,scale)
    pi=pi_bounds();base=means(w,z,ends,pi);rows=[]
    for ray in rays:
      for step in c['steps']:
        zz=moved(z,ray,F(step));row=dict(index=len(rows),ray=ray['index'],step=step);rows.append(row)
        try:row['order']=certify_order(zz,w['full_order'])
        except AssertionError:row['status']='ORDER_OR_MARGIN_REJECTED';continue
        try:altw=exact_weights(zz,scale)
        except (StopIteration,ZeroDivisionError):row['status']='RANK_REJECTED';continue
        row.update(gap(weights,altw))
        assert not F(row['relative'][0])<=F(c['gap_gate'])<F(row['relative'][1])
        if F(row['relative'][1])<=F(c['gap_gate']):row['status']='GAP_BELOW_GATE';continue
        try:row['intrinsic_gates']=intrinsic_gates(zz,altw,scale)
        except (AssertionError,StopIteration,ZeroDivisionError):row['status']='CONDITIONING_REJECTED';continue
        alt=means(w,zz,ends,pi);row['law']=law_screen(base,alt,ends,c)
        # The cancellation target is only one sum. Archive its finite nonlinear residual.
        idx=[next(k for k,pair in enumerate(ends) if set(pair)=={c['balance_anchor'],node}) for node in ray['nodes']]
        shifts=[(alt[k][0]-base[k][1],alt[k][1]-base[k][0]) for k in idx]
        row['balanced_sum_mean_change']=outward(sum(a for a,b in shifts),sum(b for a,b in shifts))
        row['component_mean_changes']=[outward(*v) for v in shifts]
        row['status']='LAW_EXCLUDED' if F(row['law']['tv_lower'])>F(c['tv_gate']) else 'HOLD'
      if ray['index']%10==9:print(json.dumps(dict(rays=ray['index']+1,states=dict(Counter(v['status'] for v in rows)))),flush=True)
    assert len(rows)==c['candidate_count']
    strong=[r for r in rows if 'law' in r];holds=[r for r in strong if r['status']=='HOLD']
    summary=dict(status='FINITE_PAIRED_GRID_EXCLUDED' if not holds else 'HOLD_COORDINATED_LAW',
        candidates=len(rows),rays=len(rays),states=dict(Counter(r['status'] for r in rows)),
        strong_conditioned_candidates=len(strong),unresolved_indices=[r['index'] for r in holds],
        strongest_order_rank_candidate=max((dict(index=r['index'],ray=r['ray'],step=r['step'],relative=r['relative'],status=r['status']) for r in rows if 'relative' in r),key=lambda r:F(r['relative'][0])),
        maximum_aggregate_tangent_relative_residual_upper=max((r['aggregate_derivative_relative_residual_upper'] for r in rays),key=F),
        minimum_excluded_full_law_tv_lower=min((r['law']['tv_lower'] for r in strong if r['status']=='LAW_EXCLUDED'),key=F,default=None),
        exact_mean_map_rank=proof['exact_jacobian_rank'],
        scope='420 paired candidates at one fixed reference. Exact noncancellation theorem is wider but does not prove finite-error operator stability. No joint-law upper bound, continuous pair-ray exclusion or physical accuracy claim.')
    return proof,rays,rows,summary

if __name__=='__main__':
    for name,data in zip(('structure.json','directions.json','candidates.json','summary.json'),run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
    print(json.dumps(read(HERE/'summary.json')))
