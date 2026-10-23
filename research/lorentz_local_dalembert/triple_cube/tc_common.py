"""Exact three-variable geometry and a joint rank-at-most-six weight update.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib,math,itertools
from pathlib import Path
from collections import Counter
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'surface_overlap_refinement'))
from sor_common import combined as parent_combined, frozen as parent_frozen
from ps_common import (F,read,save,outward,base_setup,mean_bounds,interval,sqrt_bounds,
    boosted,jr,enclose_difference,I,T,ceildiv,inv,dot,matrix_vector,ibounds,means,exact_weights)
from pc_common import event_certificate
HERE=Path(__file__).resolve().parent
ZERO=(0,0,0)

def frozen():
    parent_frozen()
    for name,h in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name

def const(v):return {ZERO:F(v)} if v else {}
def padd(*ps):
    r={}
    for p in ps:
        for k,v in p.items():r[k]=r.get(k,F(0))+v
    return {k:v for k,v in r.items() if v}
def pscale(p,v):return {k:a*v for k,a in p.items() if a*v}
def pmul(p,q):
    r={}
    for i,a in p.items():
        for j,b in q.items():
            k=tuple(x+y for x,y in zip(i,j));r[k]=r.get(k,F(0))+a*b
    assert all(sum(k)<=4 for k in r)
    return {k:v for k,v in r.items() if v}
def pdot(p,q):return padd(*(pmul(a,b) for a,b in zip(p,q)))
def pshift(p,*m):
    r={}
    for powers,a in p.items():
        for k in itertools.product(*(range(i+1) for i in powers)):
            v=a
            for i,j,x in zip(powers,k,m):v*=math.comb(i,j)*x**(i-j)
            r[k]=r.get(k,F(0))+v
    return {k:v for k,v in r.items() if v}
def pval(p,*x):
    zero=I(0) if any(isinstance(v,I) for v in x) else F(0)
    def rec(poly,axis):
        if not poly:return zero
        if axis==3:return poly.get((),F(0))
        groups={}
        for k,v in poly.items():groups.setdefault(k[0],{})[k[1:]]=v
        ans=zero
        for i in range(max(groups),-1,-1):ans=ans*x[axis]+rec(groups.get(i,{}),axis+1)
        return ans
    return rec(p,0)
def setup(c):
    b=base_setup();nodes=c['nodes'];assert nodes==[15,17,5] and c['axis']==1
    b['nodes']=nodes;b['basemeans']=means(b['w'],b['z'],b['ends'],b['pi'])
    U=[]
    for n,node in enumerate(nodes):
        t,x,y=[a-d for a,d in zip(b['z'][node],b['z'][4])];a,d,e=-F(15,8),F(17,8),F(0)
        p1=[a,d,e,2*t*a,2*x*d,2*y*e,t*d+x*a,t*e+y*a,x*e+y*d]
        p2=[F(0),F(0),F(0),a*a,d*d,e*e,a*d,a*e,d*e]
        U.append([{tuple(int(i==n) for i in range(3)):p,tuple(2*int(i==n) for i in range(3)):q} for p,q in zip(p1,p2)])
    V=[[row[node-5]-sum(row)/17 for row in b['M']] for node in nodes]
    QV=[matrix_vector(b['Q'],v) for v in V]
    QU=[[padd(*(pscale(u[j],b['Q'][i][j]) for j in range(9))) for i in range(9)] for u in U]
    A=[[{} for _ in range(6)] for _ in range(6)]
    rhs=[const(dot(v,b['lam'])) for v in V]+[padd(*(pscale(u[i],b['lam'][i]) for i in range(9))) for u in U]
    for i in range(3):
        for j in range(3):
            A[i][j]=const(dot(V[i],QV[j])-F(int(i==j))+F(1,17))
            A[i][j+3]=padd(const(int(i==j)),*(pscale(QU[j][r],V[i][r]) for r in range(9)))
            A[j+3][i]=A[i][j+3];A[i+3][j+3]=pdot(U[i],QU[j])
    center=[-sum(row)/17 for row in b['M']];R=[center]+[[a+d for a,d in zip(col,center)] for col in zip(*b['M'])]
    W=[[const(F(int(n==node-4))-F(1,17)-dot(row,qv)) for node,qv in zip(nodes,QV)]
        +[padd(*(pscale(qu[r],-row[r]) for r in range(9))) for qu in QU] for n,row in enumerate(R)]
    b.update(A=A,rhs=rhs,W=W)
    b['common_anchors']=[]
    for pair in itertools.combinations(nodes,2):
        for k in range(5):
            if all((i,k) in b['ends'] for i in pair):b['common_anchors'].append((pair,k,'future'))
            elif all((k,i) in b['ends'] for i in pair):b['common_anchors'].append((pair,k,'past'))
    b['base_statistics']={(pair,k):statistics(b,[F(0)]*6,pair,k,side) for pair,k,side in b['common_anchors']}
    return b

def moved(b,*s):
    z=[row.copy() for row in b['z']]
    for node,h in zip(b['nodes'],s):z[node][0]-=F(15,8)*h;z[node][1]+=F(17,8)*h
    return z

def displacement(b,node,box):
    if node not in b['nodes']:return F(0),F(0)
    i=b['nodes'].index(node);return tuple(box[2*i:2*i+2])

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
    center=[(box[2*i]+box[2*i+1])/2 for i in range(3)]
    x=[I(box[2*i]-center[i],box[2*i+1]-center[i]) for i in range(3)]
    A=[[pshift(p,*center) for p in row] for row in b['A']];rhs=[pshift(p,*center) for p in b['rhs']]
    R=inv([[p.get(ZERO,F(0)) for p in row] for row in A]);eta0=matrix_vector(R,[p.get(ZERO,F(0)) for p in rhs])
    residual=[padd(p,*(pscale(A[i][j],-eta0[j]) for j in range(6))) for i,p in enumerate(rhs)]
    assert all(not p.get(ZERO,0) for p in residual)
    tau=[pval(padd(*(pscale(residual[j],R[i][j]) for j in range(6))),*x) for i in range(6)]
    E=[]
    for i in range(6):
        row=[]
        for j in range(6):
            poly=padd(*(pscale(A[r][j],-R[i][r]) for r in range(6)));poly.pop(ZERO,None);row.append(pval(poly,*x))
        E.append(row)
    mags=[[z.mag() for z in row] for row in E];norm=max(sum(row) for row in mags);assert norm<T
    tauabs=[z.mag() for z in tau];radius=ceildiv(max(tauabs)*T,T-norm);r=[radius]*6
    for _ in range(c['neumann_refinements']):r=[min(old,ai+ceildiv(sum(a*v for a,v in zip(row,r)),T)) for old,ai,row in zip(r,tauabs,mags)]
    delta=[I(-v,v,raw=True) for v in r];change=[]
    for row in b['W']:
        polys=[pshift(p,*center) for p in row]
        nominal=pval(padd(*(pscale(polys[j],eta0[j]) for j in range(6))),*x)
        variation=sum((pval(p,*x)*d for p,d in zip(polys,delta)),I(0))
        change.append((nominal+variation)/F(b['w']['scale'])**2)
    n=sqrt_bounds(sum(F(d.mag(),T)**2 for d in change))[1];alt=[I(w)+d for w,d in zip(b['weights'],change)]
    amin=[F(0) if z.lo<=0<=z.hi else min(abs(F(z.lo,T)),abs(F(z.hi,T))) for z in alt]
    bound=min(F(2),2*n/(b['norm'][0]+sqrt_bounds(sum(v*v for v in amin))[0]))
    return dict(gap_upper=outward(bound)[1],neumann_norm_upper=outward(F(norm,T))[1],weight_change_bounds=[ibounds(z) for z in change])

def statistics(b,box,pair_nodes,k,side):
    i,j=pair_nodes;earlier,later=sorted((i,j),key=lambda n:(b['boost'][n][0],n));dt=abs(b['boost'][i][0]-b['boost'][j][0]);pair=qrange(b,i,j,box)
    delay=max(F(0),sqrt_bounds(dt*dt-pair[0])[1]-dt);tip=later if side=='future' else earlier;sgn=1 if side=='future' else -1
    duration=sgn*(b['boost'][k][0]-b['boost'][tip][0]);assert duration>0
    qi,qj=qrange(b,i,k,box),qrange(b,j,k,box)
    if min(qi[0],qj[0])<=0:return None
    mi,mj=mean_bounds(b,qi),mean_bounds(b,qj);qsub=qrange(b,tip,k,box)[0]-2*duration*delay+delay*delay
    common=mean_bounds(b,(qsub,qsub))[0] if delay<duration and qsub>0 else F(0)
    return dict(anchor=k,side=side,tip=tip,time_sign=sgn,duration=str(duration),mean=[str(mi[0]-mj[1]),str(mi[1]-mj[0])],
        variance_upper=str(mi[1]+mj[1]-2*common),count_mean_intervals=[list(map(str,mi)),list(map(str,mj))],
        delay_upper=str(delay),common_q_lower=str(qsub),common_mean_lower=str(common),pair_q_range=list(map(str,pair)))

def source_inventory(b):
    old=parent_combined(read(HERE.parent/'surface_overlap_refinement/certificates.json.gz'))
    ps=read(HERE.parent/'paired_surface/certificates.json.gz');st=read(HERE.parent/'surface_tail/certificates.json.gz')
    records=[]
    for r in old:
        status=r['status'];pairs=[];tv=None
        if status=='GAP_EXCLUDED':continue
        if status=='ORDER_EXCLUDED':pairs=[r['order']['pair']]
        elif status=='TRANSFERRED_LAW_EXCLUDED':
            pairs=[pair for j in r['transfer']['strips'] for pair in ps['strips'][j]['pairs']];tv=r['transfer']['tv_lower']
        elif status=='MARGINAL_TAIL_EXCLUDED':
            a=r['attempts'][-1];e=st['marginal_events'][a['event_id']] if 'event_id' in a else a
            pairs=[list(b['ends'][e['index']])];tv=e['certificate']['full_law_tv_lower']
        elif status=='OVERLAP_TAIL_EXCLUDED':
            pairs=[[n,r['anchor']] if r['side']=='future' else [r['anchor'],n] for n in (15,17)];tv=r['tv_lower']
        else:raise AssertionError(status)
        if any(5 in pair for pair in pairs):continue
        if tv is not None:assert F(tv)>F(1,4)
        records.append(dict(path=r['path'],box=r['box'],status=status,pairs=pairs,tv_lower=tv))
    return records

def projection(box,inventory):
    a,d,e,f=box[:4];selected=[];covered=F(0)
    for index,r in enumerate(inventory):
        aa,dd,ee,ff=map(F,r['box']);w=min(d,dd)-max(a,aa);h=min(f,ff)-max(e,ee)
        if w>0 and h>0:selected.append(index);covered+=w*h
    if covered==(d-a)*(f-e):return dict(source_cells=selected)
    assert covered<(d-a)*(f-e)
    return None

def node5_strips(b):
    old=read(HERE.parent/'continuous_energy/cells.json.gz');result=[]
    for r in old['cells']:
        node,axis,sign=old['rays'][r['ray']]
        if node!=5 or axis!=1 or r['status']!='LAW_EXCLUDED':continue
        pair=list(b['ends'][r['law']['interval_index']]);assert all(n==5 or n<5 for n in pair)
        lo,hi=sorted(sign*F(r[k]) for k in ('lo','hi'));assert F(r['law']['tv_lower'])>F(1,4)
        result.append(dict(ray=r['ray'],path=r['path'],lo=str(lo),hi=str(hi),pairs=[pair],tv_lower=r['law']['tv_lower']))
    return result

def strip_cover(lo,hi,inventory):
    end=lo;selected=[]
    for index,r in sorted(enumerate(inventory),key=lambda a:(F(a[1]['lo']),F(a[1]['hi']),a[0])):
        if F(r['hi'])<=end or F(r['lo'])>end:continue
        selected.append(index);end=max(end,F(r['hi']))
        if end>=hi:return dict(source_strips=selected,tv_lower=min((inventory[i]['tv_lower'] for i in selected),key=F))
    return None

def marginal_candidates(b,box):
    result=[]
    for k,pair in enumerate(b['ends']):
        if not any(n in b['nodes'] for n in pair):continue
        q=qrange(b,*pair,box)
        if q[0]<=0:continue
        a=b['basemeans'][k];d=mean_bounds(b,q);sep=max(F(0),a[0]-d[1],d[0]-a[1])
        result.append(dict(index=k,base=a,moved=d,score=sep*sep/(a[1]+d[1])))
    return sorted(result,key=lambda r:(-r['score'],r['index']))

def overlap_candidates(b,box):
    result=[]
    for pair,k,side in b['common_anchors']:
        alt=statistics(b,box,pair,k,side)
        if alt is None:continue
        base=b['base_statistics'][(pair,k)];a,d=[tuple(map(F,r['mean'])) for r in (base,alt)]
        sep=max(F(0),a[0]-d[1],d[0]-a[1]);variance=F(base['variance_upper'])+F(alt['variance_upper'])
        result.append(dict(pair=list(pair),anchor=k,side=side,base=base,moved=alt,score=sep*sep/variance if variance else F(0),threshold=((sum(a)+sum(d))/4).__floor__()))
    return sorted(result,key=lambda r:(-r['score'],tuple(r['pair']),r['anchor']))

def classify(b,box,c,inventory,strips,cache):
    key=tuple(box[:4])
    if key not in cache:cache[key]=projection(box,inventory)
    if cache[key]:return dict(status='PROJECTION_EXCLUDED',projection=cache[key])
    tr=strip_cover(*box[4:],strips)
    if tr:return dict(status='AXIS_LAW_EXCLUDED',transfer=tr)
    bad=invalid_order(b,box)
    if bad:return dict(status='ORDER_EXCLUDED',order=bad)
    try:
        op=solve_box(b,box,c)
        if F(op['gap_upper'])<=F(c['gap_gate']):return dict(status='GAP_EXCLUDED',operator=op)
    except (AssertionError,StopIteration,ZeroDivisionError):op=dict(status='HOLD_RANK_OR_ENCLOSURE')
    return dict(status='HOLD',operator=op)

def marginal(b,row,c,events,cache):
    attempts=[]
    for e in marginal_candidates(b,list(map(F,row['box'])))[:c['maximum_marginal_events_per_cell']]:
        a,d=e['base'],e['moved'];reason=None
        if max(a+d)>c['poisson']['maximum_mean']:reason='HOLD_RATE_BUDGET'
        elif not (a[1]<d[0] or d[1]<a[0]):reason='HOLD_OVERLAPPING_MEAN_BOUNDS'
        if reason:attempts.append(dict(index=e['index'],score=str(e['score']),reason=reason));continue
        key=(e['index'],a,d)
        if key not in cache:
            try:cert=event_certificate(a,d,c['poisson'])
            except AssertionError:attempts.append(dict(index=e['index'],score=str(e['score']),reason='HOLD_EVENT_BUDGET'));continue
            cache[key]=len(events);events.append(dict(index=e['index'],base=list(map(str,a)),moved=list(map(str,d)),certificate=cert))
        event_id=cache[key];attempts.append(dict(event_id=event_id,score=str(e['score'])))
        if F(events[event_id]['certificate']['full_law_tv_lower'])>F(c['tv_gate']):return dict(path=row['path'],box=row['box'],status='MARGINAL_TAIL_EXCLUDED',attempts=attempts)
    return dict(path=row['path'],box=row['box'],status='HOLD',attempts=attempts)

def overlap(b,row,c,bases,cache):
    choices=overlap_candidates(b,list(map(F,row['box'])))
    if not choices:return dict(path=row['path'],box=row['box'],status='HOLD',reason='NO_TIMELIKE_PAIR_ANCHOR')
    e=choices[0];key=(tuple(e['pair']),e['anchor'],e['threshold'])
    if key not in cache:
        cache[key]=len(bases);bases.append(dict(pair=e['pair'],anchor=e['anchor'],threshold=e['threshold'],law=enclose_difference(e['base'],e['threshold'],c['overlap'])))
    ref=cache[key];base=bases[ref]['law'];alt=enclose_difference(e['moved'],e['threshold'],c['overlap'])
    a,d=[tuple(map(F,r['probability'])) for r in (base,alt)];tv=max(F(0),a[0]-d[1],d[0]-a[1])
    return dict(path=row['path'],box=row['box'],status='OVERLAP_TAIL_EXCLUDED' if tv>F(c['tv_gate']) else 'HOLD',pair=e['pair'],anchor=e['anchor'],side=e['side'],threshold=e['threshold'],score=str(e['score']),base_statistics=e['base'],moved_statistics=e['moved'],base_law_id=ref,moved_law=alt,tv_lower=outward(tv)[0])

def volume(row):
    box=list(map(F,row['box']));return math.prod(box[2*i+1]-box[2*i] for i in range(3))
def path_key(row):return tuple(map(int,row['path'].split('/')))
def priority(row):return (-volume(row),path_key(row))
def children(row):
    box=list(map(F,row['box']));mid=[(box[2*i]+box[2*i+1])/2 for i in range(3)];result=[]
    for j,bits in enumerate(itertools.product((0,1),repeat=3)):
        child=[]
        for i,bit in enumerate(bits):child.extend((mid[i],box[2*i+1]) if bit else (box[2*i],mid[i]))
        result.append(dict(path=row['path']+'/'+str(j),box=list(map(str,child))))
    return result

def final_cells(ar):
    parents={p for level in ar['splits'] for p in level};active={r['path']:r for r in ar['cells'] if r['path'] not in parents}
    for stage in ('marginal','overlap'):
        for r in ar[stage]:
            assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box'];active[r['path']]=r
    return sorted(active.values(),key=path_key)
