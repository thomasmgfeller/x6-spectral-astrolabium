"""Finite differences of the native matter equations, preserving specified input data."""
from fractions import Fraction as Q
import json
from basisdaten import SCALE,box,hull,dot,read
from antwort import U,Z,H,R,FUTURE

JOBS=(Z,R,*FUTURE)
PAST=(0,1,2,3)


def layer(b,i,targets):
    return [b.get((i,j),0) for j in targets]


def incoming(y,b,j):
    return sum((v*(y[j]-y[i]) for (i,k),v in b.items() if k==j),box(0))


def ranks(table):
    # Each chosen interval pivot excludes zero over the entire input box.
    a=[r[:] for r in table]; pos=0; cols=[]
    upper=sum(any(v.lo or v.hi for v in row) for row in table)
    for c in range(len(a[0])):
        k=next((i for i in range(pos,len(a)) if not a[i][c].contains_zero()),None)
        if k is None:continue
        a[k],a[pos]=a[pos],a[k]
        for i in range(pos+1,len(a)):
            if a[i][c].lo or a[i][c].hi:
                scale=a[i][c]/a[pos][c]
                for j in range(c+1,len(a[i])):
                    a[i][j]=a[i][j]-scale*a[pos][j]
                a[i][c]=box(0)
        pos+=1;cols.append(c)
        if pos==upper:break
    assert pos==upper
    return {'rank':pos,'unknowns':len(a[0]),'nullity':len(a[0])-pos,'pivot_columns':cols}


def proof(y,b):
    other=sorted(set(y)-set(JOBS))
    def moments(i):
        return [v for k in layer(b,i,JOBS) for v in (-k*y[i],box(k))]
    upstream=[moments(i) for i in other]
    rows={i:layer(b,i,JOBS) for i in other}
    assert rows[0]==[-8,0,0,0,0,0] and rows[1]==[16,-8,0,0,0,0]
    assert rows[2]==[-9,16,0,0,0,0] and rows[3]==[0]*6
    assert rows[12]==rows[13]==[0,0,-9,16,-8,0]
    assert rows[H]==[0,1,-9,16,-8,0]
    assert (y[12]-y[13]).lo>0 and not (y[H]+Q(12,7)).contains_zero()
    assert layer(b,Z,FUTURE)==rows[H][2:]
    a=ranks(upstream);c=ranks([moments(i) for i in other if i not in PAST])
    # Once endpoints are fixed: seven independent future-moment conditions.
    levels=[layer(b,i,FUTURE) for i in (6,11,12,14)]
    assert levels==[[-8,0,0,0],[16,-8,0,0],[-9,16,-8,0],[1,-9,16,-8]]
    for i,j in ((11,U),(12,13),(14,R)):
        assert layer(b,i,FUTURE)==layer(b,j,FUTURE) and not (y[i]-y[j]).contains_zero()
    direction=[Q(1),Q(2),Q(23,8),Q(29,8)]
    assert all(sum(v*k for v,k in zip(row,direction))==0 for row in levels[1:])
    return {'with_four_past_momenta':a,'without_past_momenta':c,
            'nonzero_rows':{str(i):v for i,v in rows.items() if any(v)},
            'h_plus_12_over_7':(y[H]+Q(12,7)).data(),
            'homogeneous_future_direction':list(map(str,direction)),
            'nullity_with_passive_receiver_and_matched_past':1}


def end_values(y,w,b,e,windows,dw,dm):
    yy=y.copy();ww=w.copy();dx={}
    for j,d in dw.items():
        ww[j]=w[j]+d
        assert ww[j].lo>0 and ww[j].hi<SCALE
        dy=(dm[j]-y[j]*d)/ww[j]
        yy[j]=y[j]+dy;dx[j]=dy
    assert all(yy[j].lo>yy[i].hi for i,j in b)
    for j,window in zip((Z,R),windows):
        xt=(yy[j]+2-e)/(4-e)
        assert window[0]*SCALE<xt.lo<=xt.hi<window[1]*SCALE
    return {str(j):{'dw':dw[j].data(),'dM':dm[j].data(),'dY':dx[j].data()} for j in sorted(dw)}


def finite(y,w,b,e,windows,source,match_sum):
    # Branch continuously connected to the reference; stable formula for small dt.
    s,t,u,h=y[Z],y[R],y[U],y[H]
    mz,mr=incoming(y,b,Z),incoming(y,b,R)
    assert sum(v for (i,j),v in b.items() if j==Z)==0
    assert sum(v for (i,j),v in b.items() if j==R)==1
    d=box(source)/(2*mz); gap=t-s
    B=mr-d; C=d*(d-2*gap)
    radical=B*B-C
    assert radical.lo>0 and B.hi<0
    q=C/(-B+radical.sqrt())
    dw_r=-w[R]*q/(t+q-h);dm_r=h*dw_r
    l1,l2,l3=(layer(b,i,FUTURE) for i in (11,12,14))
    f=[w[i] for i in FUTURE]
    l2w,l3w=dot(l2,f),dot(l3,f)
    if match_sum:
        dw_z=(8*(h+2)*dw_r-w[Z]*d)/(s+d+3)
    else:
        dw_z=(-d*l2w+dw_r*gap+(w[R]+dw_r)*(q-d))/mz
    dm_z=(s+d)*dw_z+w[Z]*d
    j_clock=-2*(-d*l2w+dw_r*gap+(w[R]+dw_r)*(q-d)-mz*dw_z)
    if not match_sum:assert j_clock.contains_zero()
    target1=-(dm_z-u*dw_z)+9*(dm_r-u*dw_r)
    target3=q*l3w+dw_r*mr+(w[R]+dw_r)*(q-d)
    W1=target1/(y[11]-u);W3=target3/(y[14]-t-q)
    def future(a,c):
        v8=-a/8;v9=2*v8;v10=(-9*v8+16*v9-c)/8
        return [box(0),v8,v9,v10]
    dw={Z:dw_z,R:dw_r,**dict(zip(FUTURE,future(W1,W3)))}
    dm={Z:dm_z,R:dm_r,**dict(zip(FUTURE,future(y[11]*W1,y[14]*W3)))}
    # Past boundary momenta in these units are G_i=-1/2 dA/dY_i.
    dp=[sum((b.get((i,j),0)*(dm[j]-y[i]*dw[j]) for j in JOBS),box(0)) for i in PAST]
    total=sum(dp,box(0))
    if match_sum:assert total.contains_zero() and not j_clock.contains_zero()
    else:assert not total.contains_zero()
    assert not q.contains_zero() and not dw_r.contains_zero() and any(not p.contains_zero() for p in dp)
    return {'source_w':str(source),'source_Y':j_clock.data(),'construction':'matched_sum' if match_sum else 'pure',
            'delta_Y_z':d.data(),'delta_Y_r':q.data(),'delta_w_r':dw_r.data(),
            'delta_boundary_momenta':[v.data() for v in dp],'delta_sum':total.data(),
            'future_and_endpoints':end_values(y,w,b,e,windows,dw,dm)}


def homogeneous(y,w,b,e,windows,a):
    direction=[Q(1),Q(2),Q(23,8),Q(29,8)]
    dw={k:box(a*v) for k,v in zip(FUTURE,direction)}
    dm={j:y[6]*v for j,v in dw.items()}
    for k in set(y)-set(FUTURE):
        flux=sum((b.get((k,j),0)*(dm[j]-y[k]*dw[j]) for j in FUTURE),box(0))
        assert flux.contains_zero()
    return end_values(y,w,b,e,windows,dw,dm)


def run():
    y,w,rel,b,e,windows=read()
    return {'initial':proof(y,b),
            'finite':[finite(y,w,b,e,windows,q,match) for q in map(Q,('1/100000','-1/100000')) for match in (False,True)],
            'zero_source_free_future':{str(a):homogeneous(y,w,b,e,windows,a) for a in map(Q,('1/1000000','-1/1000000'))}}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
