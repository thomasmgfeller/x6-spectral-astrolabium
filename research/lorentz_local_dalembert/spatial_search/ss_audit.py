"""Exact isometry, coverage, exclusion and finite-selection audit.
SPDX-License-Identifier: Apache-2.0
"""
from ss_run import *
from bt_run import radial_bounds
from sc_run import sqrt_bounds,interval
from itertools import product

def bits(p,z,ends):
    future=[];past=[]
    for v in z:
        dt=p[0]-v[0];q=dt*dt-sum((a-b)**2 for a,b in zip(p[1:],v[1:]))
        future.append(dt>0 and q>0);past.append(dt<0 and q>0)
    return [future[a] and past[b] for a,b in ends]

def audit_cells(w,z,zz,ends,row):
    axis,sign,node,h=row['axis'],row['sign'],row['node'],F(row['step'])
    a=frame(boosted(z),axis,sign);b=frame(boosted(zz),axis,sign)
    unit=262144;v=a[node];rects=rectangles(v,h,axis,sign,16)
    box=setup(0)
    area=F((box['high'][1]-box['low'][1])*(box['high'][2]-box['low'][2]),OLDUNIT**2)
    assert sum((r[0][1]-r[0][0])*(r[1][1]-r[1][0]) for r in rects)==area
    checks=excluded=radial=0
    for side in (1,-1):
        for rect in rects:
            s,delta,r=strip(rect,v[1:],h)
            times=(v[0]+r[0],v[0]+r[1]) if side==1 else (v[0]-r[1],v[0]-r[0])
            lo=np.array([[floor(times[0]*unit),floor(rect[0][0]*unit),floor(rect[1][0]*unit)]],dtype=np.int64)
            hi=np.array([[ceil(times[1]*unit),ceil(rect[0][1]*unit),ceil(rect[1][1]*unit)]],dtype=np.int64)
            known0,label0,outer0,possible0,_=labels(lo,hi,a,ends,node,side,np.array([s>0]),unit,True)
            known1,label1,outer1,possible1,_=labels(lo,hi,b,ends,node,side,np.array([s<0]),unit,True)
            for f in [F(1,4),F(1,2),F(3,4)]:
                X=[low+f*(high-low) for low,high in rect]
                roots=[sqrt_bounds(sum((x-y)**2 for x,y in zip(X,tip[1:]))) for tip in (v,b[node])]
                dlo,dhi=(roots[1][0]-roots[0][1],roots[1][1]-roots[0][0]) if s>0 else (roots[0][0]-roots[1][1],roots[0][1]-roots[1][0])
                # The independent root enclosures must overlap the strip enclosure.
                assert dhi>=delta[0] and dlo<=delta[1];radial+=1
                inner,outer=(roots[0],roots[1]) if s>0 else (roots[1],roots[0])
                if inner[1]>=outer[0]:continue  # zero-width bisector or root uncertainty
                radius=(inner[1]+outer[0])/2
                p=[v[0]+side*radius,*X]
                assert all(F(int(low),unit)<=x<=F(int(high),unit) for x,low,high in zip(p,lo[0],hi[0]))
                bb0,bb1=bits(p,a,ends),bits(p,b,ends)
                if known0[0]:assert bytes(label0[0])==np.packbits(bb0,bitorder='little').tobytes()
                if known1[0]:assert bytes(label1[0])==np.packbits(bb1,bitorder='little').tobytes()
                oi=ends.index((3,0))
                if not outer0[0]:assert not bb0[oi]
                if not outer1[0]:assert not bb1[oi]
                affected=[i for i,(aa,bb) in enumerate(ends) if (aa==node if side==1 else bb==node)]
                if not possible0[0]:assert not any(bb0[i] for i in affected)
                if not possible1[0]:assert not any(bb1[i] for i in affected)
                excluded_cell=not(outer0[0] and outer1[0]) or not(possible0[0] or possible1[0]) or (known0[0] and known1[0] and np.array_equal(label0[0],label1[0]))
                if excluded_cell:
                    assert not bb0[oi] or bb0==bb1
                    excluded+=1
                # Back-transform each rational point and independently compare all bits.
                original=[p[0],F(0),F(0)];original[axis]=sign*p[1];original[3-axis]=p[2]
                assert bb0==bits(original,boosted(z),ends)
                assert bb1==bits(original,boosted(zz),ends)
                checks+=1
    return dict(points=checks,excluded_points=excluded,radial_checks=radial)

def audit():
    c=read(HERE/'contract.json');rows=read(HERE/'candidates.json.gz');summary=read(HERE/'summary.json');w,z,ends=geometry()
    expected=list(product(c['moved_nodes'],c['axes'],c['signs'],c['steps']))
    assert [(r['node'],r['axis'],r['sign'],r['step']) for r in rows]==expected
    causal_rejected=margin_rejected=0
    for r in rows:
        zz=deform(z,r['node'],r['axis'],r['sign'],F(r['step']))
        assert zz[:5]==z[:5]
        exact_order=all((interval(zz,i,j)>0 and zz[j][0]>zz[i][0])==w['full_order'][i][j] for i in range(21) for j in range(21) if i!=j)
        if r['status']=='ORDER_OR_MARGIN_REJECTED':
            if exact_order:margin_rejected+=1
            else:causal_rejected+=1
            continue
        assert exact_order
        for key in ('coarse','refined'):
            if key not in r:continue
            level=r[key]
            assert sum(level['classification'].values())==level['surface_rectangles']
            m=min(F(level['exact_global_mean_upper']),F(level['exact_localized_mean_upper']))
            assert F(level['exact_changed_mean_upper'])==m
            assert F(level['tv_upper'])==tv_upper(m)
        if 'refined' in r:assert F(r['tv_upper'])==min(F(r['coarse']['tv_upper']),F(r['refined']['tv_upper']))
        if r['status']=='ALL_GATES_CERTIFIED':
            assert F(r['tv_upper'])<=F(c['tv_gate'])
            assert all(F(r['intrinsic_gates'][k])<100000 for k in ('landmark_condition_upper','moment_condition_upper'))
    ranked=sorted([r for r in rows if 'coarse' in r and F(1,4)<F(r['coarse']['tv_upper'])<=F(1,2)],key=lambda r:(-F(r['relative'][0]),r['index']))[:8]
    assert [r['index'] for r in ranked]==summary['refined_indices']
    eligible=[r for r in rows if r['status']=='ALL_GATES_CERTIFIED']
    best=max(eligible,key=lambda r:(F(r['relative'][0]),-r['index']))
    assert best==summary['selected'] and len(eligible)==summary['all_gates_pass']
    # Compare the unchanged +x reference against the previously archived integrator.
    reference=next(r for r in rows if (r['node'],r['axis'],r['sign'],r['step'])==(15,1,1,c['steps'][0]))
    previous=read(HERE.parent/'boundary_transfers'/'transfers.json.gz')[0]
    assert outward(F(reference['coarse']['exact_changed_mean_upper']))[1]==previous['localized_changed_mean_upper']
    assert reference['coarse']['surface_rectangles']==previous['surface_rectangles']
    # Audit the winning candidate plus one largest admissible move in every signed frame.
    selected={best['index']:best}
    for axis,sign in product((1,2),(-1,1)):
        r=max((r for r in rows if 'coarse' in r and (r['axis'],r['sign'])==(axis,sign)),key=lambda r:(F(r['step']),-r['index']))
        selected[r['index']]=r
    checks=[]
    for r in selected.values():
        zz=deform(z,r['node'],r['axis'],r['sign'],F(r['step']))
        checks.append(dict(index=r['index'],**audit_cells(w,z,zz,ends,r)))
    # Upper-bound failure remains inconclusive; unresolved mass cannot be dropped.
    assert tv_upper(F(2))==1 and tv_upper(F(1,4))>F(22,100)
    assert any(r.get('status')=='LAW_BOUND_ABOVE_GATE' for r in rows)
    invalid=0
    for args in [(z,0,1),(z,1,0)]:
        try:frame(*args)
        except AssertionError:invalid+=1
    try:tv_upper(F(-1))
    except AssertionError:invalid+=1
    assert invalid==3
    return dict(status='PASS',candidates_checked=len(rows),causal_order_rejections=causal_rejected,margin_only_rejections=margin_rejected,
      fixed_refinement_priority_verified=True,reference_localization_reproduced=True,all_four_spatial_frames=True,
      cell_audits=checks,scalar_points=sum(r['points'] for r in checks),excluded_points=sum(r['excluded_points'] for r in checks),
      unknown_mass_retained=True,invalid_inputs_rejected=invalid,
      scope='Exact isometry/coverage/selection checks and scalar audits support the generalized localization. Whole-cell validity follows from inherited rational interval bounds, not from sampling.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
