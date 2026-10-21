import json
from pathlib import Path
import numpy as np
from scipy.optimize._numdiff import approx_derivative
from intrinsic_correction import ETA, geometry, loss_functions, order_constraints, order_check, correct

HERE = Path(__file__).resolve().parent
cfg = json.loads((HERE/'contract.json').read_text())['solver']
checks = []
def check(name, passed, value=None):
    checks.append(dict(name=name, passed=bool(passed), value=value))
    assert passed, name

rng = np.random.default_rng(810021)
x = np.column_stack((rng.uniform(1, 3, 16), rng.uniform(-.4, .4, (16, 2))))
x[:8, 0] *= -1
lm = np.array([[-8., 0, 0], [-9, 1, 0], [-10, 0, 1]])
z = np.vstack((np.zeros(3), x))
delta = z[None]-z[:, None]
order = (delta[:, :, 0]>0) & (np.sum(delta*delta*ETA, axis=2)<0)
anchors = np.vstack((np.zeros(3), lm))
q = -np.sum((x[:, None]-anchors[None])**2*ETA, axis=2)
sigma = np.ones_like(q)
fun, jac, _ = loss_functions(anchors, q, sigma)
check('compatible_metric_zero_loss', fun(x.ravel()) < 1e-20)
v = x.ravel()+rng.normal(0, .01, x.size)
error = float(np.max(np.abs(jac(v)-approx_derivative(lambda w: np.array([fun(w)]), v).ravel())))
check('objective_gradient_independent_difference', error<1e-5, error)
c, cj = order_constraints(order, cfg['margin'])
error = float(np.max(np.abs(cj(v)-approx_derivative(c, v))))
check('order_jacobian_independent_difference', error<1e-7, error)
check('strict_order_exactly_reproduced', order_check(x, order)['passed'])
lor = np.array([[1.25, -.75, 0],[-.75, 1.25,0],[0,0,1]])
boostfun, _, _ = loss_functions(anchors@lor.T, q, sigma)
check('distance_loss_lorentz_invariant', abs(fun(v)-boostfun((v.reshape(-1,3)@lor.T).ravel()))<1e-9)
bad = order.copy();bad[0,0]=True
try:
    order_constraints(bad, cfg['margin']); rejected=False
except ValueError:
    rejected=True
check('invalid_order_rejected', rejected)
# Continuous exact-volume fixture. These counts are positive real volumes,
# deliberately NOT represented as a random Poisson-sprinkled cloud.
h = (lm*ETA)@lm.T
ev,u = np.linalg.eigh(h)
t = (u/np.sqrt(abs(ev))).T
vv = (lm*ETA)@x.T
features = (t@vv).T
future = int(np.flatnonzero(x[:,0]>0)[0]); past = int(np.flatnonzero(x[:,0]<0)[0])
if features[future,0]<0:features[:,0]*=-1
ids = list(range(1,17));lids=[17,18,19]
pairs=[];counts=[];rho=10000
for j,b in enumerate(ids):
    for k,a in enumerate([0]+lids):
        pairs.append([a,b]);counts.append(rho*np.pi/12*q[j,k]**1.5)
row=dict(scale=1.,rho=rho,root=0,support=ids,landmarks=lids,temporal=[ids[past],ids[future]],
         certificate=dict(gram=h.tolist(),vectors=vv.tolist(),transform=t.tolist(),interval_pairs=pairs,interval_counts=counts),
         observed_order=order.tolist(),initial_features=features.tolist(),feasible_features=features.tolist())
fit=correct(row,cfg)
check('exact_volume_fixed_point', fit['status']=='ACCEPTED' and np.max(abs(np.array(fit['features'])-features))<1e-7, fit['status'])
perturbed=features.copy();perturbed[0,1]+=.01
row['initial_features']=perturbed.tolist();row['feasible_features']=perturbed.tolist()
fit=correct(row,cfg)
check('controlled_distortion_repaired', fit['status']=='ACCEPTED' and np.max(abs(np.array(fit['features'])-features))<1e-5, fit['status'])
out=dict(status='PASS',checks=checks,continuous_fixture=True)
(HERE/'numerical_control_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
