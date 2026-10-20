"""Minimum conditional IID field-noise variance; includes the shared root value."""
import numpy as np
from scipy.optimize import minimize

TARGET=np.array([0.,0.,0.,-2.,2.,2.,0.,0.,0.])


def certify(d,a,signs,dual,tol=2e-6):
    d,a,dual=np.asarray(d,float),np.asarray(a,float),np.asarray(dual,float)
    h=np.eye(len(a))+np.ones((len(a),len(a)))
    grad=h@a+d.T@dual
    residual=float(np.max(np.abs(d@a-TARGET)))
    if signs is None:
        station=float(np.max(np.abs(grad))); negative=0.;gap=0.
    else:
        u=np.asarray(signs)*a;mu=np.asarray(signs)*grad
        negative=max(0.,float(-u.min()),float(-mu.min()))
        station=float(np.max(np.abs(mu[u>tol]))) if np.any(u>tol) else 0.
        gap=float(mu@u)
    bound=tol*(1+float(np.linalg.norm(a)))
    passed=residual<=tol and station<=bound and negative<=bound and abs(gap)<=tol*(1+float(a@h@a))
    return dict(passed=bool(passed),moment_residual=residual,stationarity=station,
                dual_or_primal_violation=negative,complementarity=gap,
                iid_gain=float(a@h@a),full_mass=float(np.abs(a).sum()+abs(a.sum())))


def minimum_variance(d, start=None, temporal=None):
    d=np.asarray(d,float);n=d.shape[1]
    h=np.eye(n)+np.ones((n,n))
    signs=None if temporal is None else np.where(temporal,-1.,1.)
    if signs is None:
        hdt=np.linalg.solve(h,d.T)
        lam=np.linalg.solve(d@hdt,TARGET)
        a=hdt@lam; dual=-lam
    else:
        if start is None: raise ValueError('certified feasible initial point required')
        q=h*signs[:,None]*signs[None,:];mat=d*signs
        scale=max(1.,float(np.linalg.norm(start)))
        res=minimize(lambda u:.5*u@q@u/scale**2,np.asarray(start)*signs,
                     jac=lambda u:q@u/scale**2,method='SLSQP',bounds=[(0,None)]*n,
                     constraints=[dict(type='eq',fun=lambda u:mat@u-TARGET,jac=lambda u:mat)],
                     options=dict(ftol=1e-12,maxiter=2000))
        # Polish the selected face using an equality-constrained linear solve.
        free=np.flatnonzero(res.x>1e-7)
        qf=q[np.ix_(free,free)];df=mat[:,free]
        kkt=np.block([[qf,df.T],[df,np.zeros((9,9))]])
        solution=np.linalg.lstsq(kkt,np.r_[np.zeros(len(free)),TARGET],rcond=1e-12)[0]
        u=np.zeros(n);u[free]=solution[:len(free)];a=signs*u;dual=solution[len(free):]
    cert=certify(d,a,signs,dual)
    return dict(status='VERIFIED' if cert['passed'] else 'UNRESOLVED',weights=a.tolist(),dual=dual.tolist(),certificate=cert)


def audit_archived():
    import json
    from pathlib import Path
    root=Path(__file__).parent
    old=json.loads((root/'weight_audit.json').read_text())
    records=[]
    for row in old['records']:
        if row['status']!='AUDITED': continue
        entry=dict(seed=row['seed'],rho=row['rho'],arms={})
        for policy in ['free_time','unrestricted']:
            lp=row['policies'][policy]
            if lp['status']!='FEASIBLE':
                entry['arms'][policy]=dict(status='INFEASIBLE_LP');continue
            qp=minimum_variance(row['design'],lp['weights'],row['temporal_mask'] if policy=='free_time' else None)
            qp['gain_ratio_to_l1']=qp['certificate']['iid_gain']/lp['iid_field_noise_gain']
            qp['gain_ratio_to_baseline']=qp['certificate']['iid_gain']/row['baseline_noise']['iid_field_noise_gain']
            if qp['status']=='VERIFIED': assert qp['gain_ratio_to_l1']<=1+1e-6
            entry['arms'][policy]=qp
        records.append(entry)
    output=dict(scope='Retrospective development; conditional field-noise variance only',records=records)
    (root/'variance_development.json').write_text(json.dumps(output,indent=2)+'\n')
    for p in ['free_time','unrestricted']:
        rows=[r['arms'][p] for r in records if r['rho']==32768 and r['arms'][p]['status']=='VERIFIED']
        print(p,len(rows),'gain/L1 range',min(r['gain_ratio_to_l1'] for r in rows),max(r['gain_ratio_to_l1'] for r in rows))

if __name__=='__main__': audit_archived()
