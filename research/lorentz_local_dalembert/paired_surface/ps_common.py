"""Exact bivariate geometry, rank-four update and conditional-law obstructions.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'overlap_tails'))
from ot_common import F,read,save,outward,base_setup,mean_bounds,interval,sqrt_bounds,boosted,jr,enclose_difference
from pf_common import I,T,ceildiv,inv,dot,matrix_vector,ibounds,lower_bound,means,exact_weights
from pf_fast import install
install() # Algebraically identical common-denominator exponential sum; no approximation.
HERE=Path(__file__).resolve().parent

def frozen():
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def const(v):return {(0,0):F(v)} if v else {}
def padd(*ps):
    r={}
    for p in ps:
        for k,v in p.items():r[k]=r.get(k,F(0))+v
    return {k:v for k,v in r.items() if v}
def pscale(p,v):return {k:a*v for k,a in p.items() if a*v}
def pmul(p,q):
    r={}
    for (i,j),a in p.items():
        for (k,l),b in q.items():r[(i+k,j+l)]=r.get((i+k,j+l),F(0))+a*b
    assert all(sum(k)<=4 for k in r)
    return {k:v for k,v in r.items() if v}
def pdot(p,q):return padd(*(pmul(a,b) for a,b in zip(p,q)))
def pshift(p,u,v):
    r={}
    for (i,j),a in p.items():
        for k in range(i+1):
            for l in range(j+1):r[(k,l)]=r.get((k,l),F(0))+a*math.comb(i,k)*math.comb(j,l)*u**(i-k)*v**(j-l)
    return {k:a for k,a in r.items() if a}
def pval(p,u,v):
    zero=I(0) if isinstance(u,I) else F(0)
    # Horner in each variable; no interval '**' operation is required.
    out=zero
    for i in range(4,-1,-1):
        row=zero
        for j in range(4,-1,-1):row=row*v+p.get((i,j),F(0))
        out=out*u+row
    return out

def setup(c):
    b=base_setup();nodes=c['nodes'];assert nodes==[15,17] and c['axis']==1
    b['nodes']=nodes;b['basemeans']=means(b['w'],b['z'],b['ends'],b['pi'])
    U=[]
    for n,node in enumerate(nodes):
        t,x,y=[a-d for a,d in zip(b['z'][node],b['z'][4])];a,d,e=-F(15,8),F(17,8),F(0)
        p1=[a,d,e,2*t*a,2*x*d,2*y*e,t*d+x*a,t*e+y*a,x*e+y*d]
        p2=[F(0),F(0),F(0),a*a,d*d,e*e,a*d,a*e,d*e]
        U.append([{((1,0) if n==0 else (0,1)):p,((2,0) if n==0 else (0,2)):q} for p,q in zip(p1,p2)])
    V=[[row[node-5]-sum(row)/17 for row in b['M']] for node in nodes]
    QV=[matrix_vector(b['Q'],v) for v in V]
    QU=[[padd(*(pscale(u[j],b['Q'][i][j]) for j in range(9))) for i in range(9)] for u in U]
    A=[[{} for _ in range(4)] for _ in range(4)]
    rhs=[const(dot(v,b['lam'])) for v in V]+[padd(*(pscale(u[i],b['lam'][i]) for i in range(9))) for u in U]
    for i in range(2):
        for j in range(2):
            A[i][j]=const(dot(V[i],QV[j])-F(int(i==j))+F(1,17))
            A[i][j+2]=padd(const(int(i==j)),*(pscale(QU[j][r],V[i][r]) for r in range(9)))
            A[j+2][i]=A[i][j+2];A[i+2][j+2]=pdot(U[i],QU[j])
    center=[-sum(row)/17 for row in b['M']];R=[center]+[[a+d for a,d in zip(col,center)] for col in zip(*b['M'])]
    W=[[const(F(int(n==node-4))-F(1,17)-dot(row,qv)) for node,qv in zip(nodes,QV)]
        +[padd(*(pscale(qu[r],-row[r]) for r in range(9))) for qu in QU] for n,row in enumerate(R)]
    b.update(A=A,rhs=rhs,W=W)
    b['common_anchors']=[(k,'future') if (nodes[0],k) in b['ends'] and (nodes[1],k) in b['ends'] else (k,'past') for k in range(5)]
    assert all(((i,k) if side=='future' else (k,i)) in b['ends'] for k,side in b['common_anchors'] for i in nodes)
    zero=[F(0)]*4;b['base_statistics']={k:statistics(b,zero,k,side) for k,side in b['common_anchors']}
    return b

def moved(b,u,v):
    z=[row.copy() for row in b['z']]
    for node,s in zip(b['nodes'],(u,v)):
        z[node][0]-=F(15,8)*s;z[node][1]+=F(17,8)*s
    return z

def displacement(b,node,box):
    return tuple(box[:2]) if node==b['nodes'][0] else tuple(box[2:]) if node==b['nodes'][1] else (F(0),F(0))

def qrange(b,i,j,box):
    ai,bi=displacement(b,i,box);aj,bj=displacement(b,j,box)
    lo,hi=aj-bi,bj-ai;dx=b['boost'][j][1]-b['boost'][i][1];q0=interval(b['z'],i,j)
    points=[lo,hi]
    if lo<-dx<hi:points.append(-dx)
    values=[q0-2*dx*s-s*s for s in points]
    return min(values),max(values)

def invalid_order(b,box):
    for i in range(21):
        for j in range(i+1,21):
            if i not in b['nodes'] and j not in b['nodes']:continue
            q=interval(b['z'],i,j);lo,hi=qrange(b,i,j,box)
            if (q>0 and hi<=0) or (q<0 and lo>=0):return dict(pair=[i,j],base_q=str(q),range=list(map(str,(lo,hi))))
    return None

def solve_box(b,box,c):
    a,d,e,f=box;u=(a+d)/2;v=(e+f)/2;x=I(a-u,d-u);y=I(e-v,f-v)
    A=[[pshift(p,u,v) for p in row] for row in b['A']];rhs=[pshift(p,u,v) for p in b['rhs']]
    R=inv([[p.get((0,0),F(0)) for p in row] for row in A]);eta0=matrix_vector(R,[p.get((0,0),F(0)) for p in rhs])
    residual=[padd(p,*(pscale(A[i][j],-eta0[j]) for j in range(4))) for i,p in enumerate(rhs)]
    assert all(not p.get((0,0),0) for p in residual)
    tau=[pval(padd(*(pscale(residual[j],R[i][j]) for j in range(4))),x,y) for i in range(4)]
    E=[]
    for i in range(4):
        row=[]
        for j in range(4):
            p=padd(*(pscale(A[r][j],-R[i][r]) for r in range(4)));p.pop((0,0),None);row.append(pval(p,x,y))
        E.append(row)
    mags=[[z.mag() for z in row] for row in E];norm=max(sum(row) for row in mags);assert norm<T
    tauabs=[z.mag() for z in tau];radius=ceildiv(max(tauabs)*T,T-norm);r=[radius]*4
    for _ in range(c['neumann_refinements']):r=[min(old,ai+ceildiv(sum(a*v for a,v in zip(row,r)),T)) for old,ai,row in zip(r,tauabs,mags)]
    delta=[I(-v,v,raw=True) for v in r];change=[]
    for row in b['W']:
        ps=[pshift(p,u,v) for p in row];nominal=pval(padd(*(pscale(ps[j],eta0[j]) for j in range(4))),x,y)
        variation=sum((pval(p,x,y)*d for p,d in zip(ps,delta)),I(0));change.append((nominal+variation)/F(b['w']['scale'])**2)
    n=sqrt_bounds(sum(F(d.mag(),T)**2 for d in change))[1];alt=[I(w)+d for w,d in zip(b['weights'],change)]
    amin=[F(0) if z.lo<=0<=z.hi else min(abs(F(z.lo,T)),abs(F(z.hi,T))) for z in alt]
    bound=min(F(2),2*n/(b['norm'][0]+sqrt_bounds(sum(v*v for v in amin))[0]))
    return dict(gap_upper=outward(bound)[1],neumann_norm_upper=outward(F(norm,T))[1],weight_change_bounds=[ibounds(z) for z in change])

def statistics(b,box,k,side):
    i,j=b['nodes'];earlier,later=sorted((i,j),key=lambda n:(b['boost'][n][0],n));dt=abs(b['boost'][i][0]-b['boost'][j][0]);pair=qrange(b,i,j,box)
    delay=max(F(0),sqrt_bounds(dt*dt-pair[0])[1]-dt);tip=later if side=='future' else earlier;sgn=1 if side=='future' else -1
    duration=sgn*(b['boost'][k][0]-b['boost'][tip][0]);assert duration>0
    qi,qj=qrange(b,i,k,box),qrange(b,j,k,box)
    if min(qi[0],qj[0])<=0:return None
    mi,mj=mean_bounds(b,qi),mean_bounds(b,qj);qsub=qrange(b,tip,k,box)[0]-2*duration*delay+delay*delay
    common=mean_bounds(b,(qsub,qsub))[0] if delay<duration and qsub>0 else F(0)
    return dict(anchor=k,side=side,tip=tip,time_sign=sgn,duration=str(duration),mean=[str(mi[0]-mj[1]),str(mi[1]-mj[0])],
        variance_upper=str(mi[1]+mj[1]-2*common),count_mean_intervals=[list(map(str,mi)),list(map(str,mj))],
        delay_upper=str(delay),common_q_lower=str(qsub),common_mean_lower=str(common),pair_q_range=list(map(str,pair)))

def strips(b):
    source=read(HERE.parent/'continuous_energy/cells.json.gz');rows=[]
    for r in source['cells']:
        node,axis,sign=source['rays'][r['ray']]
        if node not in b['nodes'] or axis!=1 or r['status']!='LAW_EXCLUDED':continue
        pair=list(b['ends'][r['law']['interval_index']]);assert node in pair and all(n==node or n<5 for n in pair)
        lo,hi=sorted(sign*F(r[k]) for k in ('lo','hi'));assert F(r['law']['tv_lower'])>F(1,4)
        rows.append(dict(node=node,lo=str(lo),hi=str(hi),tv_lower=r['law']['tv_lower'],source='continuous_energy',ray=r['ray'],path=r['path'],pairs=[pair]))
    for directory,name in (('joint_ray_obstruction','certificate.json'),('paired_tail','strip_certificate.json')):
        r=read(HERE.parent/directory/name)
        if directory=='joint_ray_obstruction':
            lo,hi=sorted(-F(v) for v in r['domain']['h']);tv=r['full_law_tv_lower'];pairs=[r['statistics'][k]['interval'] for k in ('X','Y')]
        else:lo,hi=sorted(-F(v) for v in r['domain']['step_interval']);tv=r['tv_lower'];pairs=[r['X'],r['Y']]
        assert F(tv)>F(1,4) and all(17 not in pair for pair in pairs)
        rows.append(dict(node=15,lo=str(lo),hi=str(hi),tv_lower=tv,source=directory,pairs=pairs))
    return rows

def transfer(box,inventory):
    for node,lo,hi in ((15,*box[:2]),(17,*box[2:])):
        selected=[];end=lo
        for index,r in sorted(enumerate(inventory),key=lambda v:(F(v[1]['lo']),F(v[1]['hi']),v[0])):
            if r['node']!=node or F(r['hi'])<=end or F(r['lo'])>end:continue
            selected.append(index);end=max(end,F(r['hi']))
            if end>=hi:return dict(node=node,strips=selected,tv_lower=min((inventory[i]['tv_lower'] for i in selected),key=F))
    return None

def cheap_laws(b,box,c):
    from pc_overlap import difference_event
    best=dict(tv_lower='0')
    for k,side in b['common_anchors']:
        alt=statistics(b,box,k,side)
        if alt is None:continue
        event=difference_event(b['base_statistics'][k],alt)
        if F(event['tv_lower'])>F(best['tv_lower']):best=dict(tv_lower=event['tv_lower'],anchor=k,statistics=alt,event=event)
        if F(best['tv_lower'])>F(c['tv_gate']):return dict(status='DIFFERENCE_LAW_EXCLUDED',law=best)
    for index,pair in enumerate(b['ends']):
        if not any(n in b['nodes'] for n in pair):continue
        q=qrange(b,*pair,box)
        if q[0]<=0:continue
        a=b['basemeans'][index];d=mean_bounds(b,q);_,tv=lower_bound(a,d)
        if tv>F(c['tv_gate']):return dict(status='MARGINAL_LAW_EXCLUDED',law=dict(index=index,base=list(map(str,a)),moved=list(map(str,d)),tv_lower=outward(tv)[0]))
    return dict(status='HOLD',best_difference=best)

def classify(b,box,c,inventory):
    bad=invalid_order(b,box)
    if bad:return dict(status='ORDER_EXCLUDED',order=bad)
    transferred=transfer(box,inventory)
    if transferred:return dict(status='TRANSFERRED_LAW_EXCLUDED',transfer=transferred)
    try:
        record=solve_box(b,box,c)
        if F(record['gap_upper'])<=F(c['gap_gate']):return dict(status='GAP_EXCLUDED',operator=record)
    except (AssertionError,StopIteration,ZeroDivisionError):record=dict(status='HOLD_RANK_OR_ENCLOSURE')
    return dict(cheap_laws(b,box,c),operator=record)

def area(r):
    a,d,e,f=map(F,r['box']);return (d-a)*(f-e)
def priority(r):return (-area(r),tuple(map(int,r['path'].split('/'))))
def children(r):
    a,d,e,f=map(F,r['box']);u=(a+d)/2;v=(e+f)/2
    return [dict(path=r['path']+'/'+str(i),box=list(map(str,z))) for i,z in enumerate(((a,u,e,v),(a,u,v,f),(u,d,e,v),(u,d,v,f)))]
