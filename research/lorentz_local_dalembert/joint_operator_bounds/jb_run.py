"""Certified joint support bounds for the finite operator perturbation.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
from functools import lru_cache
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'finite_poisson_bounds'))
from fp_common import *
from fp_bound import Bound
# fp_common exports HERE; restore this package's directory.
HERE=Path(__file__).resolve().parent
UNIT=10**12

def maximizing_pair(lx,ux,ly,uy,d):
    left=max(lx,ly-d);right=ux
    assert left<=right and ly<=uy and lx<=ux
    x=left if d>=0 else max(left,min(ux,uy-d))
    assert left<=x<=right
    y=min(uy,x+d)
    assert ly<=y<=uy and lx<=x<=ux and y-x<=d
    return x,y

class Support:
    def __init__(self,D,q0,radius):
        self.D=D;self.q0=[F(0)]+list(q0);self.radius=radius;self.cache={}
        self.edges=sorted(((int(D[i,j]-D[i,0]-D[0,j]),i,j) for i in range(len(D)) for j in range(len(D)) if i!=j))
        self.improved=0;self.forms=0
    def upper(self,c):
        c=[-sum(c)]+list(c);supply=[max(F(0),-v) for v in c];demand=[max(F(0),v) for v in c]
        value=F(0);balance=[F(0)]*len(c)
        for _,i,j in self.edges:
            if supply[i] and demand[j]:
                flow=min(supply[i],demand[j]);supply[i]-=flow;demand[j]-=flow
                balance[i]-=flow;balance[j]+=flow
                value+=flow*F(int(self.D[i,j]),UNIT)
        assert not any(supply) and not any(demand) and balance==c
        return value-sum(a*b for a,b in zip(c,self.q0))
    def absolute(self,c):
        key=tuple(c)
        if key not in self.cache:
            independent=sum(abs(a)*r for a,r in zip(c,self.radius))
            bound=max(self.upper(c),self.upper([-a for a in c]),F(0))
            self.cache[key]=min(independent,bound)
            self.forms+=1;self.improved+=self.cache[key]<independent
        return self.cache[key]

def graph(means,meanD,scale,use_joint):
    pi0,pi1=pi_bounds();factor=F(32768,12)*scale**3
    @lru_cache(None)
    def f(x):return cube_bounds((x/(factor*pi1))**2)[0],cube_bounds((x/(factor*pi0))**2)[1]
    def ceiling(x):return -((-x.numerator*UNIT)//x.denominator)
    qbox=[(f(lo)[0],f(hi)[1]) for lo,hi in means]
    m=len(means);D=np.zeros((m+1,m+1),dtype=np.int64)
    for i,(lo,hi) in enumerate(qbox):D[0,i+1]=ceiling(hi);D[i+1,0]=ceiling(-lo)
    for i in range(m):
      for j in range(m):
        if i==j:continue
        upper=qbox[j][1]-qbox[i][0]
        if use_joint:
            x,y=maximizing_pair(*means[i],*means[j],F(meanD[i+1][j+1],10**6))
            upper=min(upper,f(y)[1]-f(x)[0])
        D[i+1,j+1]=ceiling(upper)
    assert np.max(abs(D))<10**16
    for k in range(m+1):D=np.minimum(D,D[:,k,None]+D[None,k,:])
    assert np.all(D.diagonal()>=0),'empty q relaxation'
    return D,qbox

def coefficients(packet,mask,q0,pivots):
    pairs=[packet['pairs'][i] for i in mask];m=len(pairs)
    where={tuple(sorted(pair)):k for k,pair in enumerate(pairs)}
    def coeff(a,b):
        v=np.full(m,F(0),dtype=object)
        if a!=b:v[where[tuple(sorted((a,b)))]]=F(1)
        return v
    anchors=packet['landmarks'];root=packet['root']
    hm=np.array([[(coeff(a,b)-coeff(a,anchors[0])-coeff(anchors[0],b))/2 for b in anchors[1:]] for a in anchors[1:]],dtype=object)
    Z=np.array([[(coeff(a,s)-coeff(anchors[0],s)-coeff(a,root)+coeff(anchors[0],root))/2 for a in anchors[1:]] for s in packet['support']],dtype=object)
    v=Z@q0;D=np.array([[t,x,y,t*t,x*x,y*y,t*x,t*y,x*y] for t,x,y in v],dtype=object).T
    bm=np.vstack((np.full((3,m),F(0),dtype=object),2*hm[0,0],2*hm[1,1],2*hm[2,2],2*hm[0,1],2*hm[0,2],2*hm[1,2]))
    return Z,v,inverse(D[:,pivots]),bm

def refine(base,packet,mask,D):
    support=Support(D,base.q0,base.radius);Z,v,S,bm=coefficients(packet,mask,base.q0,base.pivots)
    L=np.full((9,base.n),F(0),dtype=object);Q=L.copy()
    for j in range(base.n):
        ev=np.array([support.absolute(row) for row in Z[j]],dtype=object)
        J=np.vstack((Z[j],*[2*v[j,i]*Z[j,i] for i in range(3)],
                     v[j,0]*Z[j,1]+v[j,1]*Z[j,0],v[j,0]*Z[j,2]+v[j,2]*Z[j,0],v[j,1]*Z[j,2]+v[j,2]*Z[j,1]))
        remainder=np.r_[np.full(3,F(0),dtype=object),ev*ev,ev[0]*ev[1],ev[0]*ev[2],ev[1]*ev[2]]
        L[:,j]=[support.absolute(row) for row in S@J];Q[:,j]=abs(S)@remainder
    B=normup([support.absolute(row) for row in S@bm])
    old=base.L,base.Q,base.B
    base.L,base.Q,base.B=normup(L),normup(Q),B
    assert all(a<=b for a,b in zip((base.L,base.Q,base.B),old))
    result=dict(linear=outward(base.L)[1],quadratic=outward(base.Q)[1],target=outward(base.B)[1],
                forms=support.forms,forms_improved_vs_symmetric_box=support.improved,bound=base.evaluate(0))
    result['bound']['confidence_scope']='FULL_JOINT_OUTER_RELAXATION'
    base.L,base.Q,base.B=old
    return result

def compute(index):
    prior=read(OLD/f'results/cloud-{index:02d}.json.gz')
    if not prior['base'].get('qualified'):return dict(index=index,status='BASE_HOLD')
    p,obs,mask=input_record(index)
    jo=read(HERE.parent/f'joint_overlap_bounds/results/cloud-{index:02d}.json.gz')
    means=[[F(v) for v in row] for row in jo['mean_box']]
    D,qb=graph(means,jo['difference_upper_microcounts'],F(str(p['scale'])),True)
    independent,_=graph(means,jo['difference_upper_microcounts'],F(str(p['scale'])),False)
    old=read(HERE.parent/f'finite_poisson_bounds/results/cloud-{index:02d}.json.gz')
    base=Bound(p,mask,prior['base']['coordinates'],qb,pivots=old['constants']['pivots'])
    symmetric=base.evaluate(0);box=refine(base,p,mask,independent);joint=refine(base,p,mask,D)
    # Greedy feasible flows are not optimal; joint and box are separately valid.
    # Take their smaller component bounds to guarantee no regression.
    best=[min(F(box[k]),F(joint[k])) for k in ['linear','quadratic','target']]
    base.L,base.Q,base.B=best
    combined=base.evaluate(0);combined['confidence_scope']='FULL_JOINT_OUTER_RELAXATION'
    return dict(index=index,status='COMPLETE',q_difference_upper_units=D.tolist(),unit=UNIT,
        symmetric_box=symmetric,box_transport=box,joint_transport=joint,combined=combined,
        contraction_ratio_vs_box_transport=outward(F(combined['contraction_upper'])/F(box['bound']['contraction_upper'])),
        contraction_ratio_vs_old_symmetric=outward(F(combined['contraction_upper'])/F(symmetric['contraction_upper'])))

def controls():
    # Positive and negative difference branches, including a capped y endpoint.
    for d in [F(-2),F(0),F(2)]:
        x,y=maximizing_pair(F(2),F(8),F(1),F(6),d)
        ref=float(y)**(2/3)-float(x)**(2/3)
        for a in range(20,81):
            xx=F(a,10);yy=min(F(6),xx+d)
            if yy>=1:assert float(yy)**(2/3)-float(xx)**(2/3)<=ref+1e-12
    D=np.array([[0,UNIT,UNIT],[0,0,UNIT//10],[0,UNIT//10,0]],dtype=np.int64)
    s=Support(D,[F(1,2),F(1,2)],[F(1,2),F(1,2)])
    assert s.absolute([F(1),F(-1)])==F(1,10)
    assert s.absolute([F(0),F(0)])==0
    # An explicit feasible perturbation must be covered by the exact flow bound.
    assert abs(F(3,5)-F(11,20))<=s.absolute([F(1),F(-1)])
    return ['concave_difference_both_signs_grid_sanity','exact_flow_difference_gain','zero_form','feasible_point_below_bound']

def main():
    verify='--verify' in sys.argv
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    rows=[]
    for i in read(HERE/'contract.json')['indices']:
        r=compute(i);path=HERE/f'results/cloud-{i:02d}.json.gz'
        if verify:assert r==read(path),i
        else:save(path,r)
        row={k:v for k,v in r.items() if k not in ['q_difference_upper_units','box_transport','joint_transport','symmetric_box']}
        rows.append(row);print(json.dumps(row),flush=True)
    result=dict(status='PASS',controls=controls(),records=rows,full_ten_percent=sum(r.get('combined',{}).get('ten_percent_certified',False) for r in rows),
        coverage_lower=read(HERE.parent/'joint_overlap_bounds/summary.json')['coverage_lower'])
    if verify:assert result==read(HERE/'summary.json')
    else:save(HERE/'summary.json',result)
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
