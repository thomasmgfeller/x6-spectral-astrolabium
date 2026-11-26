"""A conditional stationary send/receive witness and fixed-source existence proof."""
from fractions import Fraction as F
import json
from leer import (U,Z,H,R,FREE,FUTURE,PAST,INNER,DOSE,E,WINDOWS,SCALE,UNIVERSE,
                  MID_E,MID_S,MID_R,Box,box,coordinates,relation,kernel,currents)
from positiv import serial
from kegel import coefficients

CASE=(frozenset((0,1,2,U,Z)),frozenset((0,)),0,0)


def bounds(x):
    return F(x.lo,SCALE),F(x.hi,SCALE)


def modulus(x):
    return max(abs(k) for k in bounds(x))


class Jet:
    """Value and both first partial derivatives on a rectangular domain."""
    def __init__(self,v,ds=0,dr=0):
        self.v,self.ds,self.dr=box(v),box(ds),box(dr)

    def __add__(self,other):
        b=jet(other)
        return Jet(self.v+b.v,self.ds+b.ds,self.dr+b.dr)
    __radd__=__add__

    def __neg__(self):return Jet(-self.v,-self.ds,-self.dr)

    def __sub__(self,other):return self+-jet(other)
    def __rsub__(self,other):return jet(other)+-self

    def __mul__(self,other):
        b=jet(other)
        return Jet(self.v*b.v,self.ds*b.v+self.v*b.ds,self.dr*b.v+self.v*b.dr)
    __rmul__=__mul__

    def __truediv__(self,other):
        b=jet(other)
        q=self.v/b.v
        return Jet(q,(self.ds-q*b.ds)/b.v,(self.dr-q*b.dr)/b.v)

    def square(self):
        return Jet(self.v.square(),2*self.v*self.ds,2*self.v*self.dr)

    def sqrt(self):
        assert self.v.lo>0
        v=self.v.sqrt_nonnegative_part()
        return Jet(v,self.ds/(2*v),self.dr/(2*v))


def jet(v):return v if isinstance(v,Jet) else Jet(v)


def response(s,r,future):
    """Local equations written explicitly, independently of the order solver."""
    s,r=Jet(s,ds=1),Jet(r,dr=1)
    f7,f8,f9,f10=map(jet,future)
    u=s-(s.square()+6*s+6).sqrt()
    vacancy_rad=8*(r+4).square()-16*(r+3).square()+9*(r-u).square()-(r-s).square()-19
    h=r-vacancy_rad.sqrt()
    mr=-8*(r+4)+16*(r+3)-9*(r-u)+(r-s)+(r-h)
    wr=(f7*(2-r)-9*f8*(3-r)+16*f9*(4-r)-8*f10*(5-r))/mr
    wz=(-9*f7*(2-s)+16*f8*(3-s)-8*f9*(4-s)+wr*(r-s))/(-u-3)
    gu=16*f7*(2-u)-8*f8*(3-u)+wz*(s-u)-9*wr*(r-u)
    gh=-9*f7*(2-h)+16*f8*(3-h)-8*f9*(4-h)+wr*(r-h)
    return gu,gh


def invert(case,e,s,r):
    reason,data=kernel(case,e,s,r,'pairwise')
    assert data is not None,reason
    rows=[]
    for k in range(4):
        result,branch=currents(data,[box(int(k==j)) for j in range(4)])
        assert result=='complete'
        rows.append(branch[1:])
    f=[box((1+DOSE)/64),None,None,box(F(1,64))]
    a,b=rows[1];c,d=rows[2]
    det=a*d-b*c
    assert det.hi<0 or det.lo>0
    right_u=-(f[0]*rows[0][0]+f[3]*rows[3][0])
    right_h=-(f[0]*rows[0][1]+f[3]*rows[3][1])
    f[1]=(d*right_u-c*right_h)/det
    f[2]=(a*right_h-b*right_u)/det
    return f,det


def decimal_shape(interval,denominator):
    low,high=bounds(64*interval)
    n=round((low+high)*denominator/2)
    assert F(n,denominator)-F(1,2*denominator)<low<=high<F(n,denominator)+F(1,2*denominator)
    return F(n,denominator)


def fixed_source(f,half):
    centre=(MID_E-2+(4-MID_E)*MID_S,MID_E-2+(4-MID_E)*MID_R)
    local=response(*map(box,centre),f)
    whole=response(*(Box.hull(v-half,v+half) for v in centre),f)
    derivatives=[[item.ds,item.dr] for item in local]
    (a,b),(c,d)=[[sum(bounds(v))/2 for v in row] for row in derivatives]
    det=a*d-b*c
    assert det!=0
    inverse=((d/det,-b/det),(-c/det,a/det))
    J=((whole[0].ds,whole[0].dr),(whole[1].ds,whole[1].dr))
    lipschitz=max(sum(modulus(box(int(i==j))-sum((inverse[i][k]*J[k][j] for k in range(2)),box(0)))
                        for j in range(2)) for i in range(2))
    offset=max(modulus(sum((inverse[i][k]*local[k].v for k in range(2)),box(0))) for i in range(2))
    assert lipschitz<1 and offset+lipschitz*half<half,(float(lipschitz),float(offset))
    error=offset/(1-lipschitz)
    return [Box.hull(v-error,v+error) for v in centre],{
        'centre_Y':list(map(str,centre)),'test_halfwidth':str(half),'lipschitz_upper':str(lipschitz),
        'centre_step_upper':str(offset),'error_upper':str(error),'jacobian_determinant_at_centre':serial(local[0].ds*local[1].dr-local[0].dr*local[1].ds)}


def normalized(t):
    # Both partial derivatives have fixed signs for the two observed clocks.
    lo,hi=bounds(t)
    return Box.hull((lo+2-E[1])/(4-E[1]),(hi+2-E[0])/(4-E[0]))


def validate_all(e,s,r,f):
    why,data=kernel(CASE,e,s,r,'shift')
    assert data is not None,why
    rel,y,_,_,_,rad=data
    assert rad.lo>0 and all(y[i].hi<y[j].lo for i,j in rel)
    ok,result=currents(data,f)
    assert ok=='complete'
    w,gu,gh=result
    assert all(0<w[i].lo<=w[i].hi<SCALE for i in (*FREE,*FUTURE))
    assert gu.lo<=0<=gu.hi and gh.lo<=0<=gh.hi
    for v in response(s,r,f):
        assert v.v.lo<=0<=v.v.hi
    w.update({i:box(F(1,8)) for i in PAST})
    # Symmetric differences of the whole matter action, including regraded old edges.
    pred,terms=coefficients(rel,UNIVERSE,'pairwise')
    weights={(i,j):b for j in terms for i,b in terms[j]}
    assert not {k for k in UNIVERSE if (Z,k) in rel and (k,R) in rel}
    def action(yy,ww):
        return 19*sum(ww.values(),box(0))+sum((b*ww[j]*(yy[j]-yy[i]).square()
                                              for (i,j),b in weights.items()),box(0))
    delta=F(1,10000)
    for j in (*FREE,U,H):
        assert all(y[k].lo-y[i].hi>delta*SCALE for i,k in rel if j in (i,k))
        g=(action({**y,j:y[j]-delta},w)-action({**y,j:y[j]+delta},w))/(4*delta)
        assert g.lo<=0<=g.hi
    delta=F(1,10**7)
    for j in FREE:
        assert delta*SCALE<w[j].lo<=w[j].hi<(1-delta)*SCALE
        d=(action(y,{**w,j:w[j]+delta})-action(y,{**w,j:w[j]-delta}))/(2*delta)
        assert d.lo<=0<=d.hi
    # A unique surviving interval alone does not give existence. Confirm that
    # each old branch is constructed from a strict radicand or nonsingular linear root.
    from positiv import roots
    old=set(range(15))
    op,ot=coefficients(frozenset((i,j) for i,j in rel if i in old and j in old),old,'shift')
    for j in INNER:
        terms_j=ot[j]
        assert terms[j]==terms_j
        a=sum(b for i,b in terms_j)
        origin=box(F(-11,6))
        m=sum((b*(y[i]-origin) for i,b in terms_j),box(0))
        c=19+sum((b*(y[i]-origin).square() for i,b in terms_j),box(0))
        if a: assert (m.square()-a*c).lo>0
        else: assert m.hi<0 or m.lo>0
        choices,singular=roots(terms_j,y,'shift')
        assert not singular and sum(v.intersection(y[j]) is not None for v in choices)==1
    return {'Y':{str(k):serial(v) for k,v in sorted(y.items())},
            'w':{str(k):serial(v) for k,v in sorted(w.items())},
            'w_free_positive_min':str(min(F(w[k].lo,SCALE) for k in FREE)),
            'w_free_positive_max':str(max(F(w[k].hi,SCALE) for k in FREE)),
            'min_clock_gap':str(min(F(y[j].lo-y[i].hi,SCALE) for i,j in rel)),
            'free_clock_equations':len(FREE)+2,'positive_density_equations':len(FREE)}


def read_pair(fields,rel):
    # The reader sees clock/density intervals and the transitive relation, without
    # designated sender/receiver labels. Require full containment for each hit.
    xs=fields['x']
    selected=[]
    for window in WINDOWS:
        definite=[];possible=[]
        for n,weight in fields['w'].items():
            if weight.hi<=0:continue
            lo,hi=bounds(xs[n])
            if not (lo>window[1] or hi<window[0]):
                possible.append(n)
                if weight.lo>0 and window[0]<=lo<=hi<=window[1]:definite.append(n)
        if len(definite)!=1 or possible!=definite:return None
        selected.append(definite[0])
    a,b=selected
    if (a,b) not in rel:return None
    return a,b,not any((a,k) in rel and (k,b) in rel for k in xs)


def record_check(forward,clocks):
    r=relation(CASE)
    y={int(k):Box.hull(*map(F,v)) for k,v in forward['Y'].items()}
    w={int(k):Box.hull(*map(F,v)) for k,v in forward['w'].items()}
    def xclock(v):
        # Cover all endpoint combinations, including times above Y7=2.
        ends=[(t+2-e)/(4-e) for t in bounds(v) for e in E]
        return Box.hull(min(ends),max(ends))
    x={k:xclock(v) for k,v in y.items()}
    read={'w':w,'x':x}
    assert read_pair(read,r)==(Z,R,True)
    assert read_pair({'w':{**w,R:box(0)},'x':x},r) is None
    assert read_pair({'w':w,'x':{**x,H:x[R]}},r)==(Z,R,True)
    assert read_pair({'w':w,'x':{**x,14:x[R]}},r) is None
    assert read_pair(read,r-{(Z,R)}) is None
    # Verify relabel-covariance for every single transposition. The rule itself
    # uses only membership, set cardinality, order and clock/density values.
    for i in UNIVERSE:
        for j in UNIVERSE:
            if i>=j:continue
            swap=lambda k:j if k==i else i if k==j else k
            changed={key:{swap(k):v for k,v in data.items()} for key,data in read.items()}
            assert read_pair(changed,{(swap(k),swap(l)) for k,l in r})==(swap(Z),swap(R),True)
    dt=(clocks[1]-clocks[0])/(4-Box.hull(*E))
    return {'send':Z,'receive':R,'link':True,'all_transpositions':171,
            'delta_x':serial(dt),'input':'ideal fine-history clock, density and order'}
    

def run():
    e,s,r=coordinates(True)
    f,det=invert(CASE,e,s,r)
    inverse=validate_all(e,s,r,f)
    # The rounded boundary profile is one fixed preparation for both times.
    shape=[1+DOSE,decimal_shape(f[1],10**8),decimal_shape(f[2],10**8),F(1)]
    fixed=[box(value/64) for value in shape]
    clocks,certificate=fixed_source(fixed,F(1,10**6))
    forward=validate_all(Box.hull(*E),*clocks,fixed)
    x=[normalized(t) for t in clocks]
    for iv,(lo,hi) in zip(x,WINDOWS,strict=True):
        assert lo<F(iv.lo,SCALE)<=F(iv.hi,SCALE)<hi
    return {'case':{'old_past_of_r':sorted(CASE[0]),'old_past_of_h':sorted(CASE[1]),
                    'old_future_of_h_and_r':list(FUTURE),'h_before_r':True},
            'inverse':{'x_centre':list(map(str,(MID_S,MID_R))),'e':str(MID_E),
                       'normalized_future_64w':[serial(64*v) for v in f],'det':serial(det),**inverse},
            'fixed_rounded':{'normalized_future_64w':list(map(str,shape)),'x_over_e':[serial(v) for v in x],
                             'proof':certificate,**forward},
            'clock_record':record_check(forward,clocks),
            'post_hoc_source':True,'causal_link_z_r':True,'measured_light_response':None,
            'operational_radius':None,'physical_P3':'HOLD_NOT_ELIGIBLE','physical_checkpoints_not_run':60}


if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
