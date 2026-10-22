"""Independent exact identities and scalar membership replay of surface certificates.
SPDX-License-Identifier: Apache-2.0
"""
from sf_run import *
from itertools import product

def point_bits(p,z,ends):
    future=[];past=[]
    for w in z:
        dt=p[0]-w[0];q=dt*dt-sum((x-y)**2 for x,y in zip(p[1:],w[1:]))
        future.append(dt>0 and q>0);past.append(dt<0 and q>0)
    return np.packbits(np.array([future[a] and past[b] for a,b in ends],dtype=bool),bitorder='little').tobytes().hex()

def audit():
    identities=0
    # Pythagorean coordinates give exact rational r, so the identity is checked
    # independently against the original Minkowski quadratic without root error.
    v=[F(2,3),F(-1,4),F(3,5)]
    for x,y,r in [(3,4,5),(-3,4,5),(5,-12,13),(8,15,17)]:
        X=[v[1]+x,v[2]+y];rect=tuple((q,q) for q in X)
        for side,e,w in product([1,-1],[F(-1,100),F(0),F(1,100)],[[F(1),F(2),F(3)],[F(-3),F(1,7),F(-4)]]):
            p=[v[0]+side*(r+e),*X]
            states,q,time=surface_cones(rect,v,w,side,(F(r),F(r)),(e,e))
            exact=(p[0]-w[0])**2-sum((a-b)**2 for a,b in zip(X,w[1:]))
            assert q==(exact,exact) and time==(p[0]-w[0],)*2
            for kind,state in zip([1,-1],states):assert state==((kind*(p[0]-w[0])>0 and exact>0),)*2
            identities+=1
    w,z,ends,selected=geometry();node=selected['node'];h=F(selected['step']);v=z[node]
    changed=[row[:] for row in z];changed[node][1]+=h
    records=read(HERE/'transfers.json.gz');checks=0;qchecks=0
    final=records[-1]
    for witness in final['known_cell_witnesses']:
        rect=[tuple(map(F,row)) for row in witness['rect']];side=witness['side']
        sign,thickness,_=strip(rect,v[1:],h);r=radial_bounds(rect,v[1:]);e=(F(0),thickness[1]) if sign>0 else (-thickness[1],F(0))
        qbounds=[surface_cones(rect,v,tip,side,r,e)[1] for tip in z]
        for fx,fy,u in product([F(1,4),F(1,2),F(3,4)],repeat=3):
            X=[a+f*(b-a) for (a,b),f in zip(rect,[fx,fy])]
            roots=[sqrt_bounds(sum((a-b)**2 for a,b in zip(X,tip[1:]))) for tip in [v,changed[node]]]
            radius=(1-u)*sum(roots[0])/2+u*sum(roots[1])/2
            p=[v[0]+side*radius,*X]
            assert point_bits(p,z,ends)==witness['labels'][0]
            assert point_bits(p,changed,ends)==witness['labels'][1]
            for tip,(lo,hi) in zip(z,qbounds):
                exact=(p[0]-tip[0])**2-sum((a-b)**2 for a,b in zip(X,tip[1:]))
                assert lo<=exact<=hi;qchecks+=1
            checks+=1
    # Reconstruct the cancellation lower bound independently from the archived table.
    cancellation=[]
    for record in records:
        low_in={};low_out={}
        for edge,(lo,hi) in record['transfers'].items():
            a,b=edge.split('>');lo,hi=F(lo),F(hi);assert a!=b and 0<=lo<=hi
            low_out[a]=low_out.get(a,F(0))+lo;low_in[b]=low_in.get(b,F(0))+lo
        C=sum(min(low_in.get(k,F(0)),low_out.get(k,F(0))) for k in low_in.keys()|low_out.keys())
        assert outward(C)[0]==record['certified_cancellation_lower'];cancellation.append(C)
        assert sum(record['classification'].values())==record['surface_rectangles']
    baseline=read(HERE.parent/'boundary_transfers'/'transfers.json.gz')
    for a,b in zip(baseline,records):
        assert a['surface_rectangles']==b['surface_rectangles']
        assert F(b['localization_tv_upper'])<=F(a['localized_void_tv_upper'])
    assert cancellation[-1]>0 and F(final['tv_upper'])<F(baseline[-1]['balanced_tv_upper'])
    assert final['classification']['transfer']>0 and F(final['exact_unknown_upper'])>0
    # Do not fabricate cancellation from upper bounds alone.
    assert balance({'a>b':(F(0),F(1)),'b>a':(F(0),F(1))},F(0),F(2))[2]==0
    return dict(status='PASS',exact_quadratic_identity_cases=identities,
        complete_pattern_witness_cells=len(final['known_cell_witnesses']),scalar_membership_points=checks,
        scalar_quadratic_enclosure_checks=qchecks,cancellation_lower_independently_reconstructed=True,
        matched_spatial_rectangles=True,unknown_mass_retained=True,
        scope='Exact polynomial checks and scalar audits support the implementation; rational interval algebra supplies whole-cell coverage. Positive cancellation is for the unchanged repository pair, not only a toy.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
