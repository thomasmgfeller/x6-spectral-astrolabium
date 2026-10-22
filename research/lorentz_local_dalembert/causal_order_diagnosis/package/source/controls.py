"""Mathematical, derivative, correlation, and coordinate-free selection controls."""
import json
from pathlib import Path
import numpy as np
from inference import four,baseline_three,solve,design,ETA,four_geometry
from selection import pairs_for,select_four

HERE=Path(__file__).resolve().parent
checks=[]
def check(name,passed,value=None):
    checks.append(dict(name=name,passed=bool(passed),value=value));assert passed,name

anchors=np.array([[-8,0,0],[-10,1,0],[-12,0,1],[-15,0,0]],float)
p=np.array([[-1,0,0],[-2,0,0],[-2,1,0],[-2,-1,0],[-2,0,1],[-2,0,-1],[-3,1,1],[-3,1,0],[-3,0,1],[-4,1,2],[-4,-2,1]],float)
points=np.vstack((anchors,np.zeros(3),p));ids=list(range(len(points)))
delta=points[None]-points[:,None]
order=(delta[:,:,0]>0)&(np.sum(delta*delta*ETA,axis=2)<0)
packet=dict(root=4,support=ids[5:],temporal=[5,6],landmarks=[0,1,2,3],scale=1.,
            pairs=pairs_for([0,1,2,3],4,ids[5:]),full_order=order.tolist())
q=np.array([-np.sum((points[a]-points[b])**2*ETA) for a,b in packet['pairs']])
ref,*_=solve(design(p),np.array([0,0,0,-2,2,2,0,0,0.]),1.)
c=four(q,packet,np.eye(len(q)))
check('exact_distance_operator_matches_physical',np.max(abs(c['weights']-ref))<1e-9)
b=baseline_three(q,packet)
check('three_landmark_control_matches_same_oracle',np.max(abs(b['weights']-ref))<1e-9)
direction=np.random.default_rng(782044).normal(size=len(q))
step=1e-6
fd=(four(q+step*direction,packet)['weights']-four(q-step*direction,packet)['weights'])/(2*step)
analytic=c['weight_jacobian']@direction
error=float(np.max(abs(fd-analytic)/(1+abs(analytic))))
check('KKT_sensitivity_matches_independent_difference',error<1e-5,error)
check('root_weight_covariance_conserves_constants',np.max(abs(c['weight_covariance'].sum(axis=0)))<1e-7)
# Exact fixed-bin independent Poisson construction with overlapping counts.
incidence=np.array([[1,1,0],[1,0,1],[0,1,0]],float);means=np.array([50.,30.,40.])
expected=(incidence*means)@incidence.T
samples=np.random.default_rng(782045).poisson(means,size=(100000,3))@incidence.T
empirical=np.cov(samples,rowvar=False)
error=float(np.max(abs(empirical-expected)/np.sqrt(np.outer(np.diag(expected),np.diag(expected)))))
check('overlap_covariance_matches_Poisson_experiment',error<.03,error)
contrast=np.array([1.,-1.,0.]);correct=float(contrast@expected@contrast);wrong=float(contrast@np.diag(np.diag(expected))@contrast)
check('diagonal_only_negative_control_detected',correct==70 and wrong==170,dict(full=correct,diagonal=wrong))
check('intersection_covariance_PSD',np.linalg.eigvalsh(expected)[0]>=0)
# A coordinate-free object is all the selector receives. Distances below are
# exact-volume fixture measurements, not a claimed random physical cloud.
class Poset:
    def __init__(self,r,marks):
        self.r=r;self.size=len(r);self.marks=marks;self.probes_for_check=[]
        self.pred=[sum(1<<int(j) for j in np.flatnonzero(r[:,i])) for i in range(len(r))]
        self.succ=[sum(1<<int(j) for j in np.flatnonzero(r[i])) for i in range(len(r))]
class Counts:
    def __init__(self,qs):self.qs=qs
    def good(self,a,b):return self.qs[a,b]>0
    def q(self,a,b):return self.qs[a,b]
    def values(self,a,b):return [100*self.qs[a,b]**1.5,0,0]
allq=-np.sum(delta*delta*ETA,axis=2)
marks=np.random.default_rng(782046).random(len(points))
sel=dict(root=4,support=ids[5:],temporal=[5,6],landmarks=[0,1,2],scale=1.)
cfg=dict(candidate_cap_per_side=128,maximum_landmark_condition=1e5,maximum_design_condition=1e5)
selected=select_four(Poset(order,marks),Counts(allq),sel,cfg)
check('intrinsic_fourth_selection_on_fixture',selected['status']=='SELECTED' and selected['packet']['landmarks'][3]==3)
perm=np.random.default_rng(782047).permutation(len(points));inverse=np.argsort(perm)
changed={k:[int(inverse[a]) for a in sel[k]] if isinstance(sel[k],list) else int(inverse[sel[k]]) if k=='root' else sel[k] for k in sel}
relabeled=select_four(Poset(order[np.ix_(perm,perm)],marks[perm]),Counts(allq[np.ix_(perm,perm)]),changed,cfg)
check('landmark_selection_relabel_equivariant',relabeled['status']=='SELECTED' and int(perm[relabeled['packet']['landmarks'][3]])==3)
check('unused_root_support_counts_have_zero_sensitivity',
      max(float(np.max(abs(c['weight_jacobian'][:,i]))) for i,(a,b) in enumerate(packet['pairs']) if 4 in (a,b) and (b if a==4 else a) in packet['support'])<1e-12)
out=dict(status='PASS',checks=checks,checks_total=len(checks),scope='Synthetic controls only; no campaign seeds generated')
(HERE/'controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
