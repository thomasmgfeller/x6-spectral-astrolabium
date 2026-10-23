"""Rank-four polynomial certificate for a simultaneous two-column motion.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'coordinated_motions'))
import cm_run as cm
from cm_run import F,read,save,outward,inv,dot,geometry,boosted,exact_weights,interval,sqrt_bounds,means,pi_bounds,lower_bound,event_certificate
from ce_common import setup as base_setup,mean_bounds
from cs_interval import I,T,ceildiv
sys.path.insert(0,str(HERE.parent/'joint_ray_obstruction'))
import jr_run as jr

def frozen():
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def add(a,b):return [x+y for x,y in zip(a,b)]
def neg(a):return [-x for x in a]
def scale(a,v):return [x*v for x in a]
def constant(v):return [F(v),F(0),F(0),F(0),F(0)]
def product(a,b):
    assert all(a[i]*b[j]==0 for i in range(5) for j in range(5) if i+j>4)
    return [sum((a[i]*b[k-i] for i in range(k+1)),F(0)) for k in range(5)]
def value(p,h):
    result=I(0) if isinstance(h,I) else F(0)
    for v in reversed(p):result=result*h+v
    return result
def shift(p,m):
    return [sum((p[k]*math.comb(k,j)*m**(k-j) for k in range(j,5)),F(0)) for j in range(5)]
def polynomial_dot(a,b):
    out=constant(0)
    for x,y in zip(a,b):out=add(out,product(x,y))
    return out
def matrix_vector(A,x):return [dot(row,x) for row in A]
def ibounds(x):return [str(F(x.lo,T)),str(F(x.hi,T))]

def setup(c):
    b=base_setup();z=b['z'];ray=read(HERE.parent/'coordinated_motions'/'directions.json')[c['ray_index']]
    assert ray['nodes']==c['nodes'] and ray['axis']==c['axis'] and ray['velocities']==c['velocities']
    velocities=[F(0)]*21
    for node,v in zip(ray['nodes'],map(F,ray['velocities'])):velocities[node]=v
    # U contains the two changed moment columns: u_i(h)=h*p1+h^2*p2.
    U=[]
    for node,v in zip(ray['nodes'],map(F,ray['velocities'])):
        direction=[-F(15,8)*v,F(17,8)*v,F(0)]
        t,x,y=[a-d for a,d in zip(z[node],z[4])];a,d,e=direction
        p1=[a,d,e,2*t*a,2*x*d,2*y*e,t*d+x*a,t*e+y*a,x*e+y*d]
        p2=[F(0),F(0),F(0),a*a,d*d,e*e,a*d,a*e,d*e]
        U.append([[F(0),p,q,F(0),F(0)] for p,q in zip(p1,p2)])
    V=[[row[node-5]-sum(row)/17 for row in b['M']] for node in ray['nodes']]
    QV=[matrix_vector(b['Q'],v) for v in V]
    QU=[[[sum((b['Q'][i][j]*u[j][k] for j in range(9)),F(0)) for k in range(5)] for i in range(9)] for u in U]
    K=[[F(int(i==j))-F(1,17) for j in range(2)] for i in range(2)]
    A=[[constant(0) for j in range(4)] for i in range(4)]
    rhs=[constant(dot(v,b['lam'])) for v in V]
    for u in U:rhs.append([sum((u[i][k]*b['lam'][i] for i in range(9)),F(0)) for k in range(5)])
    for i in range(2):
      for j in range(2):
        A[i][j]=constant(dot(V[i],QV[j])-K[i][j])
        A[i][j+2]=add(constant(int(i==j)),[sum((V[i][r]*QU[j][r][k] for r in range(9)),F(0)) for k in range(5)])
        A[j+2][i]=A[i][j+2]
        A[i+2][j+2]=polynomial_dot(U[i],QU[j])
    center=[-sum(row)/17 for row in b['M']]
    R=[center]+[[a+d for a,d in zip(col,center)] for col in zip(*b['M'])]
    # delta w = (R_E-R_D Q V)*eta_V - R_D Q U*eta_U.
    W=[]
    for n,row in enumerate(R):
        W.append([constant(F(int(n==node-4))-F(1,17)-dot(row,qv)) for node,qv in zip(ray['nodes'],QV)]
                 +[[-sum((row[r]*qu[r][k] for r in range(9)),F(0)) for k in range(5)] for qu in QU])
    b.update(ray=ray,velocities=velocities,A=A,rhs=rhs,W=W)
    pair=c['joint_event'];indices=[b['ends'].index(tuple(pair[k])) for k in ('X','Y')]
    basemeans=means(b['w'],z,b['ends'],b['pi']);b['basemeans']=basemeans
    b['joint_base'],b['joint_base_records']=jr.enclose_event(*(basemeans[k] for k in indices),c['joint_probability'])
    return b

def solve_cell(b,lo,hi,c):
    m=(lo+hi)/2;s=I(lo-m,hi-m)
    A=[[shift(p,m) for p in row] for row in b['A']];rhs=[shift(p,m) for p in b['rhs']]
    R=inv([[p[0] for p in row] for row in A]);eta0=matrix_vector(R,[p[0] for p in rhs])
    # Exact polynomial cancellation precedes interval rounding.
    residual=[add(p,neg([sum((A[i][j][k]*eta0[j] for j in range(4)),F(0)) for k in range(5)])) for i,p in enumerate(rhs)]
    assert all(p[0]==0 for p in residual)
    tau=[value([sum((R[i][j]*residual[j][k] for j in range(4)),F(0)) for k in range(5)],s) for i in range(4)]
    E=[[value([F(0)]+[-sum((R[i][r]*A[r][j][k] for r in range(4)),F(0)) for k in range(1,5)],s) for j in range(4)] for i in range(4)]
    mags=[[e.mag() for e in row] for row in E];norm=max(sum(row) for row in mags)
    assert norm<T,'rank-four contraction unresolved'
    tauabs=[x.mag() for x in tau]
    radius=ceildiv(max(tauabs)*T,T-norm);r=[radius]*4
    for _ in range(c['neumann_refinements']):
        r=[min(old,ai+ceildiv(sum(a*v for a,v in zip(row,r)),T)) for old,ai,row in zip(r,tauabs,mags)]
    delta=[I(-v,v,raw=True) for v in r]
    weight_change=[]
    for row in b['W']:
        p=[shift(x,m) for x in row]
        nominal=value([sum((p[j][k]*eta0[j] for j in range(4)),F(0)) for k in range(5)],s)
        variation=sum((value(x,s)*v for x,v in zip(p,delta)),I(0))
        weight_change.append((nominal+variation)/F(b['w']['scale'])**2)
    n=sqrt_bounds(sum(F(x.mag(),T)**2 for x in weight_change))[1]
    alt=[I(w)+d for w,d in zip(b['weights'],weight_change)]
    amin=[F(0) if x.lo<=0<=x.hi else min(abs(F(x.lo,T)),abs(F(x.hi,T))) for x in alt]
    na=sqrt_bounds(sum(x*x for x in amin))[0]
    bound=min(F(2),2*n/(b['norm'][0]+na))
    return bound,weight_change,F(norm,T)

def qpoly(b,i,j):
    dv=b['velocities'][j]-b['velocities'][i]
    dx=b['boost'][j][1]-b['boost'][i][1]
    return [interval(b['z'],i,j),-2*dx*dv,-dv*dv]

def qrange(b,i,j,lo,hi):
    a,d,e=qpoly(b,i,j);points=[lo,hi]
    if e and lo<-d/(2*e)<hi:points.append(-d/(2*e))
    vals=[a+d*h+e*h*h for h in points]
    return min(vals),max(vals)

def invalid_order(b,lo,hi):
    for i in range(21):
      for j in range(i+1,21):
        q=interval(b['z'],i,j);a,d=qrange(b,i,j,lo,hi)
        if (q>0 and d<=0) or (q<0 and a>=0):return [i,j]
    return None

def joint_bounds(b,lo,hi,c):
    pairs=[c['joint_event'][name] for name in ('X','Y')];qs=[qrange(b,*pair,lo,hi) for pair in pairs]
    if any(q[0]<=0 for q in qs):return None
    # Boosted tip times are constant along the simultaneous spatial motion.
    assert b['boost'][2][0]<b['boost'][5][0]<b['boost'][1][0]
    mus=[mean_bounds(b,q) for q in qs]
    p,records=jr.enclose_event(*mus,c['joint_probability']);base=b['joint_base']
    tv=max(F(0),base[0]-p[1],p[0]-base[1])
    return dict(tv_lower=outward(tv)[0],mean_intervals=[[str(v) for v in p] for p in mus],
                probability=outward(*p,digits=60),q_ranges=[[str(v) for v in q] for q in qs],records=records)

def marginal_bounds(b,lo,hi,c):
    candidates=[]
    for k,(i,j) in enumerate(b['ends']):
        if i not in c['nodes'] and j not in c['nodes']:continue
        q=qrange(b,i,j,lo,hi)
        if q[0]<=0:continue
        a=b['basemeans'][k];d=mean_bounds(b,q)
        if not (a[1]<d[0] or d[1]<a[0]):continue
        exponent,tv=lower_bound(a,d);candidates.append((exponent,tv,k,a,d))
    candidates.sort(key=lambda x:(-x[0],x[2]));best=dict(tv_lower='0',method='NONE')
    for exponent,tv,k,a,d in candidates:
        if tv>F(c['tv_gate']):return dict(tv_lower=outward(tv)[0],method='HELLINGER',index=k,means=[[str(x) for x in v] for v in (a,d)])
    for exponent,tv,k,a,d in candidates[:2]:
        if max(a+d)>c['poisson']['maximum_mean']:continue
        cert=event_certificate(a,d,c['poisson'])
        if F(cert['full_law_tv_lower'])>F(best['tv_lower']):
            best=dict(tv_lower=cert['full_law_tv_lower'],method='POISSON_EVENT',index=k,means=[[str(x) for x in v] for v in (a,d)],certificate=cert)
        if F(best['tv_lower'])>F(c['tv_gate']):break
    return best

def classify(b,lo,hi,c):
    pair=invalid_order(b,lo,hi)
    if pair:return dict(status='ORDER_EXCLUDED',pair=pair)
    record={}
    try:
        g,d,eta=solve_cell(b,lo,hi,c)
        record.update(gap_upper=outward(g)[1],neumann_norm_upper=outward(eta)[1],weight_change_bounds=[ibounds(x) for x in d])
        if g<=F(c['gap_gate']):return dict(status='GAP_EXCLUDED',**record)
    except (AssertionError,StopIteration,ZeroDivisionError):record['operator']='HOLD_RANK_OR_ENCLOSURE'
    joint=joint_bounds(b,lo,hi,c)
    if joint and F(joint['tv_lower'])>F(c['tv_gate']):return dict(status='JOINT_LAW_EXCLUDED',joint=joint,**record)
    marginal=marginal_bounds(b,lo,hi,c)
    return dict(status='MARGINAL_LAW_EXCLUDED' if F(marginal['tv_lower'])>F(c['tv_gate']) else 'HOLD',joint=joint,marginal=marginal,**record)
