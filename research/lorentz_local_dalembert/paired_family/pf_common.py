"""Continuous certificates for the remaining frozen two-support spatial lines.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'paired_continuous'))
from pc_common import (F,read,save,outward,inv,dot,interval,sqrt_bounds,means,base_setup,mean_bounds,
    I,T,ceildiv,add,neg,scale,constant,product,value,shift,polynomial_dot,matrix_vector,
    solve_cell,ibounds,lower_bound,cm,exact_weights,boosted)
from pc_overlap import difference_event
HERE=Path(__file__).resolve().parent

def frozen():
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def setup(base,ray):
    b=dict(base);z=b['z'];assert ray['axis'] in (1,2)
    velocities=[F(0)]*21
    for node,v in zip(ray['nodes'],map(F,ray['velocities'])):velocities[node]=v
    # U contains the two changed moment columns: u_i(h)=h*p1+h^2*p2.
    U=[]
    for node,v in zip(ray['nodes'],map(F,ray['velocities'])):
        direction=([-F(15,8)*v,F(17,8)*v,F(0)] if ray['axis']==1 else [F(0),F(0),v])
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
    b['common_anchors']=[]
    i,j=ray['nodes']
    for k in range(5):
        if (i,k) in b['ends'] and (j,k) in b['ends']:b['common_anchors'].append((k,'future'))
        elif (k,i) in b['ends'] and (k,j) in b['ends']:b['common_anchors'].append((k,'past'))
    b['base_statistics']={k:variance_enclosure(b,F(0),F(0),k,side) for k,side in b['common_anchors']}
    return b

def qpoly(b,i,j):
    dv=b['velocities'][j]-b['velocities'][i]
    dx=b['boost'][j][b['ray']['axis']]-b['boost'][i][b['ray']['axis']]
    return [interval(b['z'],i,j),-2*dx*dv,-dv*dv]

def qrange(b,i,j,lo,hi):
    a,d,e=qpoly(b,i,j);points=[lo,hi]
    if e and lo<-d/(2*e)<hi:points.append(-d/(2*e))
    vals=[a+d*h+e*h*h for h in points]
    return min(vals),max(vals)

def invalid_order(b,lo,hi):
    # Only pairs incident to a moved point can change. Include their cross term.
    for i in range(21):
      for j in range(i+1,21):
        if i not in b['ray']['nodes'] and j not in b['ray']['nodes']:continue
        q=interval(b['z'],i,j);a,d=qrange(b,i,j,lo,hi)
        if (q>0 and d<=0) or (q<0 and a>=0):return [i,j]
    return None

def variance_enclosure(b,lo,hi,k,side):
    i,j=b['ray']['nodes'];ti,tj=(b['boost'][n][0] for n in (i,j))
    earlier,later=sorted((i,j),key=lambda n:(b['boost'][n][0],n))
    dt=abs(ti-tj);pair=qrange(b,i,j,lo,hi)
    delay=max(F(0),sqrt_bounds(dt*dt-pair[0])[1]-dt)
    if side=='future':
        assert (i,k) in b['ends'] and (j,k) in b['ends']
        tip=later;duration=b['boost'][k][0]-b['boost'][tip][0];time_sign=1
    else:
        assert side=='past' and (k,i) in b['ends'] and (k,j) in b['ends']
        tip=earlier;duration=b['boost'][tip][0]-b['boost'][k][0];time_sign=-1
    assert duration>0
    qi,qj=qrange(b,i,k,lo,hi),qrange(b,j,k,lo,hi)
    if qi[0]<=0 or qj[0]<=0:return None
    mi,mj=mean_bounds(b,qi),mean_bounds(b,qj)
    qsub=qrange(b,tip,k,lo,hi)[0]-2*duration*delay+delay*delay
    common=mean_bounds(b,(qsub,qsub))[0] if delay<duration and qsub>0 else F(0)
    variance=mi[1]+mj[1]-2*common;assert variance>=0
    return dict(anchor=k,side=side,tip=tip,time_sign=time_sign,duration=str(duration),
        mean=[str(mi[0]-mj[1]),str(mi[1]-mj[0])],variance_upper=str(variance),
        count_mean_intervals=[[str(x) for x in m] for m in (mi,mj)],delay_upper=str(delay),
        common_q_lower=str(qsub),common_mean_lower=str(common),pair_q_range=[str(x) for x in pair])

def overlap_bound(b,lo,hi):
    best=dict(tv_lower='0')
    for k,side in b['common_anchors']:
        alt=variance_enclosure(b,lo,hi,k,side)
        if alt is None:continue
        event=difference_event(b['base_statistics'][k],alt)
        if F(event['tv_lower'])>F(best['tv_lower']):best=dict(tv_lower=event['tv_lower'],anchor=k,variance=alt,event=event)
    return best

def marginal_bound(b,lo,hi):
    best=dict(tv_lower='0')
    for index,(i,j) in enumerate(b['ends']):
        if i not in b['ray']['nodes'] and j not in b['ray']['nodes']:continue
        q=qrange(b,i,j,lo,hi)
        if q[0]<=0:continue
        a=b['basemeans'][index];d=mean_bounds(b,q);_,tv=lower_bound(a,d)
        if tv>F(best['tv_lower']):best=dict(tv_lower=outward(tv)[0],index=index,mean_intervals=[[str(x) for x in m] for m in (a,d)])
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
    overlap=overlap_bound(b,lo,hi)
    if F(overlap['tv_lower'])>F(c['tv_gate']):return dict(status='DIFFERENCE_LAW_EXCLUDED',overlap=overlap,**record)
    marginal=marginal_bound(b,lo,hi)
    return dict(status='MARGINAL_LAW_EXCLUDED' if F(marginal['tv_lower'])>F(c['tv_gate']) else 'HOLD',
                overlap=overlap,marginal=marginal,**record)

def priority(row):return (-(F(row['hi'])-F(row['lo'])),tuple(map(int,row['path'].split('/'))))

def cover(leaves,lo,hi):
    rows=sorted(leaves,key=lambda r:F(r['lo']))
    assert rows and F(rows[0]['lo'])==lo and F(rows[-1]['hi'])==hi
    assert all(F(r['lo'])<F(r['hi']) for r in rows)
    assert all(F(a['hi'])==F(d['lo']) for a,d in zip(rows,rows[1:]))
