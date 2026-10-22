"""Synthetic mathematical/derivative controls, separate from campaign seeds.
SPDX-License-Identifier: Apache-2.0
"""
import json
from pathlib import Path
import numpy as np
from fit import Model, canonical, estimate, input_mask
from inference import ETA, design, solve
from selection import pairs_for

HERE=Path(__file__).resolve().parent
c=json.loads((HERE/'contract.json').read_text());cfg=c['fit'];checks=[]
def check(name, ok, value=None):
    checks.append(dict(name=name, passed=bool(ok), value=value))
    assert ok, name

rng=np.random.default_rng(782063)
anchors=np.array([[-8,0,0],[-10,1,0],[-12,0,1],[-15,.2,.3]])
support=np.column_stack((np.r_[-2.,2.,rng.uniform(-4,-1,9),rng.uniform(1,4,9)], rng.uniform(-.4,.4,(20,2))))
points=np.vstack((anchors,np.zeros(3),support));ids=list(range(len(points)))
delta=points[None]-points[:,None];s2=np.sum(delta**2*ETA,axis=2)
order=(delta[:,:,0]>0)&(s2<0)
p=dict(root=4,support=ids[5:],temporal=[5,6],landmarks=[0,1,2,3],scale=1.,pairs=pairs_for([0,1,2,3],4,ids[5:]),full_order=order.tolist())
q=np.array([-s2[a,b] for a,b in p['pairs']]);rho=20.;counts=rho*np.pi/12*q**1.5
z=canonical(points);dz=z[None]-z[:,None]
check('canonical_gauge_preserves_all_intervals',np.max(abs(np.sum(dz**2*ETA,axis=2)-s2))<1e-10)
model=Model(p,counts,rho,cfg);x=model.pack(z)
check('full_true_order_satisfies_all_constraints',model.constraints(x)[0].min()>0)
flipped=z.copy();flipped[:,0]*=-1
check('time_orientation_negative_control',model.constraints(model.pack(flipped))[0].min()<-1)
perturbed=x+rng.normal(size=len(x))*.003;v=rng.normal(size=len(x));v/=np.linalg.norm(v);step=1e-6
f,g=model.objective(perturbed);fd=(model.objective(perturbed+step*v)[0]-model.objective(perturbed-step*v)[0])/(2*step)
err=abs(fd-g@v)/(1+abs(g@v));check('raw_count_gradient_independent_difference',err<2e-5,float(err))
cv,cj=model.constraints(perturbed);cd=(model.constraints(perturbed+step*v)[0]-model.constraints(perturbed-step*v)[0])/(2*step)
err=np.max(abs(cd-cj@v)/(1+abs(cj@v)));check('complete_constraint_jacobian_independent_difference',err<2e-6,float(err))
ref,*_=solve(design(support),np.array([0,0,0,-2,2,2,0,0,0.]),1.)
fit=estimate(p,counts,rho,cfg)
check('exact_mean_fixture_is_qualified',fit.get('qualified'),fit.get('reason'))
err=np.max(abs(np.array(fit['weights'])-ref));check('exact_mean_operator_matches_oracle',err<1e-7,float(err))
check('minimum_count_hold',estimate(p,np.zeros_like(counts),rho,cfg)['status']=='COUNT_HOLD')
unused=counts.copy();unused[~input_mask(p)]=0.
fit_unused=estimate(p,unused,rho,cfg)
check('same_four_inputs_no_extra_root_support_information',fit_unused.get('qualified') and np.max(abs(np.array(fit_unused['weights'])-fit['weights']))<1e-10)
# Node relabeling changes ids and sorted pair ordering, never hidden geometry.
perm=rng.permutation(len(points));mapping={i:int(perm[i]) for i in ids}
pp={**p,'root':mapping[4],'landmarks':[mapping[i] for i in p['landmarks']],
    'support':[mapping[i] for i in p['support']],'temporal':[mapping[i] for i in p['temporal']],
    'pairs':[[min(mapping[a],mapping[b]),max(mapping[a],mapping[b])] for a,b in p['pairs']]}
fp=estimate(pp,counts,rho,cfg)
check('inference_relabel_invariance',fp.get('qualified') and np.max(abs(np.array(fp['weights'])-fit['weights']))<1e-8)
out=dict(status='PASS',checks=checks,scope='Synthetic controls, not fresh-cloud results. Expected real-valued counts in exact fixture, not a Poisson draw.')
with (HERE/'controls.json').open('x') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2))
