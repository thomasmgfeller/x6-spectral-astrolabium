"""Finite implementation controls on declared exact-distance fixtures."""
import json
from pathlib import Path
import numpy as np
from four_landmark_operator import operator
from intrinsic_correction import weights, ETA

a=np.array([[-8,0,0],[-10,1,0],[-12,0,1],[-15,0,0]],float)
p=np.array([[-1,0,0],[-2,0,0],[-2,1,0],[-2,-1,0],[-2,0,1],[-2,0,-1],[-3,1,1],[-3,1,0],[-3,0,1],[-4,1,2],[-4,-2,1]],float)
qa=-np.sum((a[:,None]-a[None])**2*ETA,axis=2)
qr=-np.sum(a*a*ETA,axis=1)
qx=-np.sum((a[:,None]-p[None])**2*ETA,axis=2)
reference,_=weights(p,1.)
checks=[]
for name,perm,scale in [('base',[0,1,2,3],1.),('anchor_permutation',[2,0,3,1],1.),('scale',[0,1,2,3],7.)]:
    result=operator(qa[np.ix_(perm,perm)],qr[perm],qx[perm],scale)
    error=float(np.max(abs(np.array(result['weights'])-reference)))
    checks.append(dict(name=name,passed=error<1e-7,maximum_weight_error=error))
    assert checks[-1]['passed']
bad=np.arange(4,dtype=float)[:,None]*np.array([[2,0,0]])+np.array([[-10,0,0]])
bq=-np.sum((bad[:,None]-bad[None])**2*ETA,axis=2)
try:
    operator(bq,-np.sum(bad*bad*ETA,axis=1),-np.sum((bad[:,None]-p[None])**2*ETA,axis=2),1.)
    rejected=False
except ValueError:rejected=True
checks.append(dict(name='rank_deficient_anchor_frame_rejected',passed=rejected))
assert rejected
out=dict(status='PASS',checks=checks,noisy_cloud_validation='NOT_RUN')
(Path(__file__).parent/'four_landmark_numerical_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
