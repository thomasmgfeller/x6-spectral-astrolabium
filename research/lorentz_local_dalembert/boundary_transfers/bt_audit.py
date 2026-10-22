"""Independent scalar checks of boundary enclosures and transfer accounting.
SPDX-License-Identifier: Apache-2.0
"""
from bt_run import *
from itertools import product

def membership(p,z,ends):
    def cone(a,b):
        d=[y-x for x,y in zip(a,b)]
        return d[0]>0 and d[0]*d[0]>d[1]*d[1]+d[2]*d[2]
    return [cone(z[a],p) and cone(p,z[b]) for a,b in ends]

def audit():
    w,zz=inputs();old=read(HERE.parent/'shape_coupling'/'summary.json')['selected']
    z=boosted(zz);alt=boosted(deform(zz,old['node'],1,1,F(old['step'])))
    v=z[old['node']];h=F(old['step']);unit=read(HERE/'contract.json')['coordinate_unit']
    box=setup(0);ranges=[(F(int(box['low'][j]),OLDUNIT),F(int(box['high'][j]),OLDUNIT)) for j in [1,2]]
    edges=[[a+(b-a)*i/16 for i in range(17)] for a,b in ranges]
    cut=v[1]+h/2;edges[0]=sorted(set(edges[0]+[cut]))
    rects=[((a,b),(c,d)) for a,b in zip(edges[0],edges[0][1:]) for c,d in zip(edges[1],edges[1][1:])]
    area=sum((b-a)*(d-c) for (a,b),(c,d) in rects)
    assert area==(ranges[0][1]-ranges[0][0])*(ranges[1][1]-ranges[1][0])
    checks=0;excluded_checks=0
    for side in [1,-1]:
        for rect in rects:
            sign,(dl,du),r=strip(rect,v[1:],h)
            times=(v[0]+r[0],v[0]+r[1]) if side==1 else (v[0]-r[1],v[0]-r[0])
            lower=np.array([[floor(times[0]*unit),floor(rect[0][0]*unit),floor(rect[1][0]*unit)]],dtype=np.int64)
            upper=np.array([[ceil(times[1]*unit),ceil(rect[0][1]*unit),ceil(rect[1][1]*unit)]],dtype=np.int64)
            _,_,outer=labels(lower,upper,z,[(3,0)],old['node'],side,np.array([sign>0]),unit)
            for fx,fy in product([F(1,4),F(1,2),F(3,4)],repeat=2):
                x=rect[0][0]+fx*(rect[0][1]-rect[0][0]);y=rect[1][0]+fy*(rect[1][1]-rect[1][0])
                a=sqrt_bounds((x-v[1])**2+(y-v[2])**2)
                b=sqrt_bounds((x-v[1]-h)**2+(y-v[2])**2)
                dlo,dhi=(b[0]-a[1],b[1]-a[0]) if sign>0 else (a[0]-b[1],a[1]-b[0])
                # Exact rational sqrt enclosures cross-check the correlated formula.
                assert dl<=dhi and dlo<=du
                t=v[0]+side*(sum(a)+sum(b))/4;p=[t,x,y]
                assert int(lower[0,0])<=t*unit<=int(upper[0,0])
                # Away from bisector and measure-zero boundaries, the strip flips the active cone.
                def active(q):
                    dt=side*(p[0]-q[0]);return dt>0 and dt*dt>(x-q[1])**2+(y-q[2])**2
                assert active(z[old['node']])==(sign>0)
                assert active(alt[old['node']])==(sign<0)
                if not outer[0]:assert not membership(p,z,[(3,0)])[0];excluded_checks+=1
                checks+=1
    # Both directions have fully certifiable labels in a separated synthetic geometry.
    synthetic=[[F(4),F(0),F(0)],[F(0),F(0),F(0)],[F(0),F(0),F(3)],[F(-4),F(0),F(0)]]
    changed=[row[:] for row in synthetic];changed[1][1]=F(1,100)
    ends=[(3,0),(1,0),(3,1)];rect=((F(1),F(5,4)),(F(0),F(1,4)))
    sign,_,r=strip(rect,synthetic[1][1:],F(1,100));synthetic_checks=0
    for side in [1,-1]:
        times=(r[0],r[1]) if side==1 else (-r[1],-r[0])
        lo=np.array([[floor(times[0]*unit),unit,0]],dtype=np.int64)
        hi=np.array([[ceil(times[1]*unit),5*unit//4,unit//4]],dtype=np.int64)
        k0,b0,_=labels(lo,hi,synthetic,ends,1,side,np.array([sign>0]),unit)
        k1,b1,_=labels(lo,hi,changed,ends,1,side,np.array([sign<0]),unit)
        assert k0[0] and k1[0] and bytes(b0[0])!=bytes(b1[0]);synthetic_checks+=1
    cycle=balance({'a>b':(F(1),F(1)),'b>a':(F(1),F(1))},F(0),F(2));assert cycle==(2,0,2)
    uncertain=balance({'a>b':(F(0),F(1)),'b>a':(F(0),F(1))},F(0),F(2))
    assert uncertain[2]==0 and uncertain[1]>=1  # uncertain upper masses are not proven cancellation
    missing=balance({},F(1,4),F(1,4));assert missing==(F(1,4),F(1,4),0)
    records=read(HERE/'transfers.json.gz')
    for rec in records:
        table={k:tuple(map(F,x)) for k,x in rec['transfers'].items()}
        result=balance(table,F(rec['exact_unknown_upper']),constant(w)*h/2)
        assert outward(result[1])[1]==rec['balanced_residual_mean_upper']
        assert sum(rec['classification'].values())==rec['surface_rectangles']
    assert all(F(b['balanced_tv_upper'])<F(a['balanced_tv_upper']) for a,b in zip(records,records[1:]))
    return dict(status='PASS',exact_scalar_strip_checks=checks,excluded_domain_checks=excluded_checks,
        synthetic_known_transfer_directions=synthetic_checks,spatial_area_exact=True,
        exact_cycle_cancellation=True,uncertain_cycle_not_claimed=True,unknown_mass_retained=True,
        scope='Finite point checks audit implementation; whole-cell interval inequalities and spatial partition proof supply coverage. No actual-pair cancellation is asserted by controls.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
