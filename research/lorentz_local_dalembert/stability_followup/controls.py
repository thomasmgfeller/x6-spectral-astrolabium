"""Synthetic covariance/forward-model controls before campaign freeze.
SPDX-License-Identifier: Apache-2.0
"""
import json
from pathlib import Path
import numpy as np
from models import Alternative,canonical,estimate
from inference import ETA,design,solve
from selection import pairs_for
from run import save

HERE=Path(__file__).resolve().parent;c=json.loads((HERE/'contract.json').read_text());cfg=c['fit'];rng=np.random.default_rng(782073)
anchors=np.array([[-8,0,0],[-10,1,0],[-12,0,1],[-15,.2,.3]])
support=np.column_stack((np.r_[-2.,2.,rng.uniform(-4,-1,9),rng.uniform(1,4,9)],rng.uniform(-.4,.4,(20,2))))
points=np.vstack((anchors,np.zeros(3),support));d=points[None]-points[:,None];s2=np.sum(d*d*ETA,axis=2);order=(d[:,:,0]>0)&(s2<0);ids=list(range(len(points)))
p=dict(root=4,support=ids[5:],temporal=[5,6],landmarks=ids[:4],scale=1.,pairs=pairs_for(ids[:4],4,ids[5:]),full_order=order.tolist())
counts=20*np.pi/12*np.array([-s2[a,b] for a,b in p['pairs']])**1.5
shared=.25*counts.min();C=np.diag(counts-shared)+shared*np.ones((len(counts),len(counts)));checks=[]
def check(name,ok,value=None):
    checks.append(dict(name=name,passed=bool(ok),value=value));assert ok,name
m=Alternative(p,counts,C,20,cfg,'full_gls');x=m.pack(canonical(points))+rng.normal(size=len(m.indices))*.003;v=rng.normal(size=len(x));v/=np.linalg.norm(v);h=1e-6
value,g=m.objective(x);fd=(m.objective(x+h*v)[0]-m.objective(x-h*v)[0])/(2*h);err=abs(fd-g@v)/(1+abs(g@v));check('full_covariance_gradient_finite_difference',err<2e-5,float(err))
md=Alternative(p,counts,C,20,cfg,'diagonal_gls');check('correlation_negative_control_changes_loss',abs(md.objective(x)[0]-value)>1e-7)
mi=Alternative(p,counts,np.diag(counts),20,cfg,'full_gls');check('diagonal_limit_matches_diagonal_control',abs(mi.objective(x)[0]-md.objective(x)[0])<1e-10)
f=estimate(p,counts,C,20,cfg,'full_gls');ref,*_=solve(design(support),np.array([0,0,0,-2,2,2,0,0,0.]),1.)
err=max(abs(np.array(f.get('weights',[1e10]))-ref));check('exact_mean_full_covariance_operator_oracle',f.get('qualified') and err<1e-7,float(err))
check('minimum_count_abstention_preserved',estimate(p,np.zeros_like(counts),np.zeros_like(C),20,cfg,'full_gls')['status']=='COUNT_HOLD')
bad=C.copy();bad[0,0]+=1
check('inconsistent_covariance_rejected',estimate(p,counts,bad,20,cfg,'full_gls')['status']=='UNRESOLVED')
save(HERE/'controls.json',dict(status='PASS',checks=checks,scope='Synthetic common-plus-independent Poisson-component covariance; real-valued expected-count fixture, not random physical data.'))
print(json.dumps(checks,indent=2))
