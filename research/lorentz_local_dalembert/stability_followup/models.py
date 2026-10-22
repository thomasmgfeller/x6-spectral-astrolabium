"""Fixed diagnostic ablations and covariance-aware nonlinear count GLS.
SPDX-License-Identifier: Apache-2.0
"""
import sys,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize

HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'causal_count_fit'
sys.path.insert(0,str(PRIOR))
from fit import Model,canonical,input_mask
from inference import ETA,four,four_geometry,normalize,strict_order_check

class Alternative(Model):
    def __init__(self,packet,counts,overlaps,rho,cfg,arm):
        super().__init__(packet,counts,rho,cfg)
        self.arm=arm
        overlap=np.asarray(overlaps,float);counts=np.asarray(counts,float)
        if overlap.shape!=(len(counts),len(counts)) or not np.array_equal(overlap,overlap.T) or not np.array_equal(overlap.diagonal(),counts):
            raise ValueError('invalid overlap covariance')
        self.precision=None
        if arm in ['full_gls','diagonal_gls']:
            C=overlap[np.ix_(self.mask,self.mask)]
            alpha=cfg['correlation_shrinkage']
            C=(1-alpha)*C+alpha*np.diag(self.counts) if arm=='full_gls' else np.diag(self.counts)
            chol=np.linalg.cholesky(C)
            inv=np.linalg.solve(chol,np.eye(len(C)))
            self.precision=inv.T@inv
            self.covariance_condition=float(np.linalg.cond(C))
        keep=~((self.i>=5)&(self.j>=5))
        self.constraint_mask=np.r_[keep,keep[self.causal]] if arm=='no_support_order' else None

    def objective(self,x):
        if self.precision is None:return super().objective(x)
        s,ds,_=self.interval(x,self.a,self.b);q=np.maximum(-s,1e-12)
        mean=self.factor*q**1.5;r=mean-self.counts
        dm=-1.5*self.factor*np.sqrt(q)[:,None]*ds;dm[-s<=1e-12]=0
        pr=self.precision@r
        return float(r@pr/len(r)),2/len(r)*pr@dm

    def constraints(self,x):
        c,j=super().constraints(x)
        if self.constraint_mask is not None:return c[self.constraint_mask],j[self.constraint_mask]
        return c,j

def estimate(packet,counts,overlaps,rho,cfg,arm):
    start=time.monotonic();out=dict(status='UNRESOLVED',qualified=False,arm=arm)
    counts=np.asarray(counts,float)
    if np.min(counts[input_mask(packet)])<cfg['minimum_count']:
        return dict(status='COUNT_HOLD',qualified=False,arm=arm,seconds=time.monotonic()-start)
    try:
        q=(counts/(rho*np.pi/12))**(2/3)/packet['scale']**2
        h,z,_,_=four_geometry(q,packet);tr,_=normalize(h);initial=(tr@z.T).T
        future=packet['support'].index(packet['temporal'][1])+5
        if initial[future,0]<0:initial[:,0]*=-1
        m=Alternative(packet,counts,overlaps,rho,cfg,arm);x=m.pack(canonical(initial))
        if max(abs(x))>=cfg['coordinate_bound']:raise ValueError('initial coordinate budget')
        def guard(_):
            if time.monotonic()-start>cfg['fit_seconds']:raise TimeoutError('fit time budget')
        r=minimize(m.objective,x,jac=True,method='SLSQP',bounds=[(-cfg['coordinate_bound'],cfg['coordinate_bound'])]*len(x),
            constraints=[dict(type='ineq',fun=lambda x:m.constraints(x)[0],jac=lambda x:m.constraints(x)[1])],callback=guard,
            options=dict(maxiter=cfg['max_iterations'],ftol=cfg['ftol']))
        z=m.unpack(r.x);c,_=m.constraints(r.x);order=strict_order_check(z,packet['full_order'])
        out.update(optimizer_success=bool(r.success),optimizer_message=str(r.message),iterations=int(r.nit),objective=float(r.fun),minimum_constraint=float(c.min()),order=order,coordinates=z,
                   active_constraints=int(np.sum(c<1e-6)),covariance_condition=getattr(m,'covariance_condition',None))
        if not r.success or c.min() < -cfg['constraint_tolerance']:raise ValueError('optimizer or feasibility failed')
        pairs=np.array([[m.lookup[a],m.lookup[b]] for a,b in packet['pairs']])
        qfit=-np.sum((z[pairs[:,1]]-z[pairs[:,0]])**2*ETA,axis=1)
        f=four(qfit,packet)
        out.update(status='WEIGHTS_VALID',weights=f['weights'],certificate=f['certificate'],landmark_condition=f['landmark_condition'],qualified=bool(order['passed'] and f['qualified']))
        if arm!='no_support_order' and not out['qualified']:
            out.pop('weights',None);out['status']='ORDER_HOLD'
    except (ValueError,np.linalg.LinAlgError,TimeoutError) as exc:out['reason']=str(exc)
    out['seconds']=time.monotonic()-start
    return out
