"""Direct action/current checks on the source code and two exact comparison histories."""
from fractions import Fraction as F
import json
from pruefung import ROOT, I, P, FUT, DENSITY, model, support, variation, encode
from intervall import Box, SCALE, box


def read_geometry(code):
    rel,edges=model(code)
    mask=encode(rel,15)
    reference={(i,j):b for i,j,b in variation.edges(mask,15) if b}
    assert edges==reference
    return rel,edges,mask


def original_normalized_action(mask, y, w):
    g = variation.gamma(mask,15,y)
    return -sum(w[j]*(1 + F(2,19)*g[j]) for j in range(15))/2


def source_pair(mask,y,w):
    z=(29,23,16,8)
    l=(F(47,1856),F(3,184),F(1,128),F(0))
    duration=y[7]-y[3]
    amps={}
    for side in (-1,1):
        source=y[:]
        for i in P:
            source[i]=y[3]-120*l[i]+side*F(3,16)*z[i]/duration
        assert max(source[i] for i in P)<min(source[i] for i in I)
        assert all(source[i]<source[i+1] for i in P[:-1])
        past_only=[w[i] if i in P else 0 for i in range(15)]
        amps[side]=original_normalized_action(mask,source,w)-original_normalized_action(mask,source,past_only)
    return amps[-1]-amps[1]


def flat_control(code):
    rel,edges,mask=read_geometry(code)
    # Affine clock on each chain, independently found by the depth.
    y=[F(0)]*15
    for i in P: y[i]=F(i-5)
    for i in FUT: y[i]=F(i-5)
    for i in I: y[i]=F(-1+sum((j,i) in rel for j in I))
    assert all(y[a]<y[b] for a,b in rel)
    w=[DENSITY]*15
    for j in reversed(I):
        h=sum(b*(y[i]-y[j]) for (i,v),b in edges.items() if v==j)
        out=sum(b*w[v]*(y[v]-y[j]) for (i,v),b in edges.items() if i==j)
        w[j]=-out/h
        assert 0<w[j]<1
    g=variation.gamma_from_operator(mask,15,y)
    assert g==variation.gamma(mask,15,y)
    assert all(1+F(2,19)*g[i]==0 for i in I)
    current,grad=variation.current_and_gradient(mask,15,y,w)
    assert all(grad[i]==0 for i in I)
    cut_values=[]
    for n in range(1<<len(I)):
        region=set(P)|{i for j,i in enumerate(I) if n & (1<<j)}
        if any(i not in region and j in region for i,j in rel):
            continue
        cut_values.append(2*sum(v for i,j,v in current if i in region and j not in region))
    assert min(cut_values)==max(cut_values)>0
    phase=source_pair(mask,y,w)
    dose=sum(w[j] for j in I)/(y[7]-y[3])
    assert phase==F(45,19)*dose
    return {'Y':list(map(str,y)), 'w':list(map(str,w)), 'ideals_checked':len(cut_values),
            'current_19Delta_Q':str(cut_values[0]), 'dose_times_Delta':str(dose),
            'phase_rad':str(phase)}


def neighborhood(code, radius):
    """Validate existence by an explicit rational triangular parametrization on a real interval."""
    rel,edges,_=read_geometry(code)
    e=Box.hull(-radius,radius)
    y={0:box(-5),1:box(-4),2:box(-3),3:e-2,**{v:box(v-5) for v in FUT}}
    w=dict.fromkeys(FUT,box(DENSITY))
    moments={}
    for j in I:
        terms=[(i,b) for (i,v),b in edges.items() if v==j]
        assert sum(b for _,b in terms)==0
        h=sum(b*y[i] for i,b in terms)
        assert h.lo>0
        moments[j]=h
        y[j]=(19+sum(b*y[i].square() for i,b in terms))/(2*h)
    assert all(y[i].hi<y[j].lo for i,j in rel)
    for j in reversed(I):
        out=sum(b*w[v]*(y[v]-y[j]) for (i,v),b in edges.items() if i==j)
        w[j]=-out/moments[j]
        assert 0<w[j].lo<=w[j].hi<SCALE
    # Discrete conservation makes every ideal cut equivalent. Use the simpler future cut.
    charge=sum(b*w[j]*(y[j]-y[i]) for (i,j),b in edges.items() if i not in FUT and j in FUT)
    dose=sum(w[j] for j in I)/(4-e)
    assert charge.lo>0 and dose.lo>0
    return charge,dose


def ends(x):
    return list(map(str,(F(x.lo,SCALE),F(x.hi,SCALE))))


def run():
    for code in support.catalogue():
        read_geometry(code)
    # Compare the local polynomial expressions with unreduced coefficients away from singularities.
    for e in map(F,('-3/8','-1/4','-1/8','0','1/8','1/4','3/8')):
        y=[F(-5),F(-4),F(-3),-2+e]
        a=(e**2-4*e-2)/(2*(1+e))
        assert 19+sum(b*(a-i)**2 for b,i in zip((-8,16,-9,1),y))==0
        for k,row in ((1,(0,-8,16,-9)),(2,(0,0,-8,16))):
            vals=[*y,*([a]*k)]
            b=[*row,*([1]*k)]
            d=sum(b)
            h=sum(c*x for c,x in zip(b,vals))
            q=19+sum(c*x*x for c,x in zip(b,vals))
            if k==1:
                assert not d and q/(2*h)-a==(e**4+36*e**3-44*e**2-96*e-8)/(4*(1+e)*(17*e**2+18*e-2))
            else:
                assert d==10 and 4*(h*h-d*q)==8*(62*e**4+248*e**3+313*e**2+130*e-15)/(1+e)**2
                assert d*a*a-2*h*a+q==(2*e**4+8*e**3-5*e**2-26*e+3)/(1+e)**2
    a,b=39441,39456
    exact={str(c):flat_control(c) for c in (a,b)}
    radius=F(1,2**20)
    qa,da=neighborhood(a,radius)
    qb,db=neighborhood(b,radius)
    qr,dr=qb/qa,db/da
    assert qr.hi<SCALE and dr.lo>SCALE
    return {'exact':exact,'open_control_halfwidth_e':str(radius),'current_ratio_interval':ends(qr),
            'dose_ratio_interval':ends(dr),'current_ratio_at_zero':'1/5','dose_ratio_at_zero':'9/7'}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
