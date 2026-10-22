"""Exact shared geometry and rank-two operator enclosure.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'poisson_tail_obstruction'))
from pto_run import F,read,save,outward,event_certificate
from ss_run import geometry,boosted,deform,exact_weights
from ss_marginal import lower_bound,pi_bounds
from st_certificate import solve,sqrt_bounds,interval,certify_order
sys.path.insert(0,str(HERE.parent/'coordinated_budget'))
from cb_run import matrices
from cs_interval import I,T

def frozen():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def mv(A,v):return [dot(row,v) for row in A]
def inv(A):return list(map(list,zip(*[solve(A,[F(int(i==j)) for i in range(len(A))]) for j in range(len(A))])))
def ibounds(x):return [F(x.lo,T),F(x.hi,T)]
def ivec(v):return [I(x) for x in v]

def setup():
    w,z,ends=geometry();M,S=matrices(z);Q=inv(S);rhs=list(map(F,[0,0,0,-2,2,2,0,0,0]));lam=solve(S,rhs)
    assert all(dot(Q[i],col)==int(i==j) for i in range(9) for j,col in enumerate(zip(*S)))
    weights=exact_weights(z,F(w['scale']))
    return dict(w=w,z=z,boost=boosted(z),ends=ends,M=M,Q=Q,lam=lam,weights=weights,
        norm=sqrt_bounds(dot(weights,weights)),pi=pi_bounds())

def ray_data(base,node,axis,sign):
    d=([F(-15,8),F(17,8),F(0)] if axis==1 else [F(0),F(0),F(1)])
    d=[sign*x for x in d];t,x,y=[a-b for a,b in zip(base['z'][node],base['z'][4])];a,b,c=d
    p1=[a,b,c,2*t*a,2*x*b,2*y*c,t*b+x*a,t*c+y*a,x*c+y*b]
    p2=[F(0),F(0),F(0),a*a,b*b,c*c,a*b,a*c,b*c]
    v=[row[node-5]-sum(row)/17 for row in base['M']];qv=mv(base['Q'],v)
    qp1,qp2=mv(base['Q'],p1),mv(base['Q'],p2)
    center=[-sum(row)/17 for row in base['M']]
    columns=[center]+[[a+b for a,b in zip(col,center)] for col in zip(*base['M'])]
    return dict(node=node,axis=axis,sign=sign,direction=d,p1=p1,p2=p2,v=v,qv=qv,
                b11=dot(v,qv)-F(16,17),tau1=dot(v,base['lam']),
                b12=[F(1),dot(v,qp1),dot(v,qp2)],
                b22=[F(0),F(0),dot(p1,qp1),2*dot(p1,qp2),dot(p2,qp2)],
                tau2=[F(0),dot(p1,base['lam']),dot(p2,base['lam'])],
                alpha_coeff=[dot(col,qv) for col in columns],
                beta_coeff=[[F(0),dot(col,qp1),dot(col,qp2)] for col in columns])

def delta_weights(base,ray,h):
    """Woodbury with U=[v,d], C=[[0,1],[1,16/17]]. Works for F or I."""
    convert=I if isinstance(h,I) else F
    # Multiply and cancel exact polynomial coefficients BEFORE interval evaluation.
    # Raw Q*d intervals would lose large algebraic cancellations in this geometry.
    def poly(coefficients):
        value=convert(0)
        for coefficient in reversed(coefficients):value=value*h+convert(coefficient)
        return value
    b11=convert(ray['b11']);b12=poly(ray['b12']);b22=poly(ray['b22'])
    det=b11*b22-b12*b12
    if isinstance(det,I):assert not det.lo<=0<=det.hi,'unresolved determinant'
    else:assert det!=0
    t1=convert(ray['tau1']);t2=poly(ray['tau2'])
    alpha=(b22*t1-b12*t2)/det;beta=(b11*t2-b12*t1)/det
    dlam=t2-(b12-1)*alpha-b22*beta
    shifts=[-convert(a)*alpha-poly(b)*beta+convert(F(int(j==ray['node']-4))-F(1,17))*dlam
            for j,(a,b) in enumerate(zip(ray['alpha_coeff'],ray['beta_coeff']))]
    scale=convert(F(base['w']['scale'])**2)
    return [x/scale for x in shifts],det

def gap_upper(base,ray,lo,hi):
    delta,det=delta_weights(base,ray,I(lo,hi))
    n=sqrt_bounds(sum(F(x.mag(),T)**2 for x in delta))[1]
    alt=[I(w)+d for w,d in zip(base['weights'],delta)]
    amin=[F(0) if x.lo<=0<=x.hi else min(abs(F(x.lo,T)),abs(F(x.hi,T))) for x in alt]
    na=sqrt_bounds(sum(x*x for x in amin))[0]
    return min(F(2),2*n/(base['norm'][0]+na)),delta,det

def q_bounds(base,ray,i,j,lo,hi):
    q=interval(base['z'],i,j);node=ray['node']
    if node not in (i,j):return q,q
    other=j if i==node else i
    linear=2*ray['sign']*(base['boost'][other][ray['axis']]-base['boost'][node][ray['axis']])
    points=[lo,hi];vertex=linear/2
    if lo<vertex<hi:points.append(vertex)
    vals=[q+linear*h-h*h for h in points]
    return min(vals),max(vals)

def invalid_order_pair(base,ray,lo,hi):
    node=ray['node']
    for other in range(21):
        if other==node:continue
        q=interval(base['z'],node,other);a,b=q_bounds(base,ray,node,other,lo,hi)
        if (q>0 and b<=0) or (q<0 and a>=0):return [node,other]
    return None

def mean_bounds(base,q):
    a,b=q;assert 0<a<=b
    factor=F(base['w']['rho'],12)*F(base['w']['scale'])**3
    return tuple(map(F,outward(factor*base['pi'][0]*a*sqrt_bounds(a)[0],factor*base['pi'][1]*b*sqrt_bounds(b)[1],digits=30)))

def law_lower(base,ray,lo,hi,c):
    candidates=[]
    for k,(i,j) in enumerate(base['ends']):
        if ray['node'] not in (i,j):continue
        q=q_bounds(base,ray,i,j,lo,hi)
        if q[0]<=0:continue
        a=mean_bounds(base,(interval(base['z'],i,j),)*2);b=mean_bounds(base,q)
        if not (a[1]<b[0] or b[1]<a[0]):continue
        _,h=lower_bound(a,b)
        candidates.append((h,k,a,b))
    candidates.sort(key=lambda x:(-x[0],x[1]));best=dict(tv_lower='0',method='NONE')
    for h,k,a,b in candidates:
        if h>F(c['tv_gate']):return dict(tv_lower=outward(h)[0],method='HELLINGER',interval_index=k,mean_intervals=[[str(v) for v in pair] for pair in (a,b)])
    for h,k,a,b in candidates[:2]:
        if max(a+b)>c['poisson']['maximum_mean']:continue
        cert=event_certificate(a,b,c['poisson'])
        if F(cert['full_law_tv_lower'])>F(best['tv_lower']):
            best=dict(tv_lower=cert['full_law_tv_lower'],method='POISSON_EVENT',interval_index=k,threshold=cert['threshold'],
                      mean_intervals=[[str(v) for v in pair] for pair in (a,b)])
        if F(best['tv_lower'])>F(c['tv_gate']):break
    return best

def classify(base,ray,lo,hi,c):
    bad=invalid_order_pair(base,ray,lo,hi)
    if bad:return dict(status='ORDER_EXCLUDED',pair=bad)
    try:g,_,det=gap_upper(base,ray,lo,hi)
    except AssertionError:g=F(2);det=None
    record=dict(gap_upper=outward(g)[1])
    if det is not None:record['determinant']=list(map(str,ibounds(det)))
    if g<=F(c['gap_gate']):return dict(status='GAP_EXCLUDED',**record)
    law=law_lower(base,ray,lo,hi,c)
    return dict(status='LAW_EXCLUDED' if F(law['tv_lower'])>F(c['tv_gate']) else 'HOLD',law=law,**record)
