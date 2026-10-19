"""Coordinate-assisted LPs; every conclusion requires a checked witness."""
import numpy as np
from scipy.optimize import linprog

TARGET=np.array([0.,0.,0.,-2.,2.,2.,0.,0.,0.])

def design(z):
    z=np.asarray(z,float)
    return np.vstack([z.T,(z*z).T,np.sqrt(2)*z[:,0]*z[:,1],
                      np.sqrt(2)*z[:,0]*z[:,2],np.sqrt(2)*z[:,1]*z[:,2]])

def problem(d,a0,temporal,policy):
    d=np.asarray(d,float);a0=np.asarray(a0,float);n=len(a0)
    temporal=np.asarray(temporal,bool);fixed=np.zeros(n)
    if policy=='fixed_time':
        fixed[temporal]=a0[temporal];points=np.flatnonzero(~temporal);signs=np.ones(len(points))
    elif policy=='free_time':
        points=np.arange(n);signs=np.where(temporal,-1.,1.)
    elif policy=='unrestricted':
        points=np.tile(np.arange(n),2);signs=np.repeat([1.,-1.],n)
    else:raise ValueError('unknown policy')
    return d[:,points]*signs,TARGET-d@fixed,fixed,points,signs

def checked_feasible(d,a0,temporal,policy,x,y,contract):
    d=np.asarray(d,float);x=np.asarray(x,float);y=np.asarray(y,float)
    a,b,fixed,points,signs=problem(d,a0,temporal,policy)
    assert x.shape==(a.shape[1],) and y.shape==(len(b),)
    assert np.isfinite(x).all() and np.isfinite(y).all()
    tol=contract['certificate_tolerance'];scale=1+float(np.max(np.abs(b)))
    residual=float(np.max(np.abs(a@x-b)));negative=max(0.,float(-np.min(x)))
    slack=float(np.min(1-a.T@y));gap=float(np.sum(x)-b@y)
    assert residual<=tol*scale and negative<=tol and slack>=-tol
    assert abs(gap)<=contract['duality_gap_tolerance']*(1+abs(float(np.sum(x))))
    weights=fixed.copy();np.add.at(weights,points,signs*x)
    moment_residual=float(np.max(np.abs(d@weights-TARGET)))
    mass=float(np.abs(weights).sum());objective=float(np.sum(x)+np.abs(fixed).sum())
    assert moment_residual<=tol*scale
    assert abs(mass-objective)<=contract['duality_gap_tolerance']*(1+abs(objective))
    return weights,dict(primal_residual=residual,negative_variable_violation=negative,
        minimum_dual_slack=slack,duality_gap=gap,moment_residual=moment_residual,
        mass=mass,positive_mass=float(weights[weights>0].sum()),negative_mass=float(-weights[weights<0].sum()))

def checked_infeasible(d,a0,temporal,policy,y,contract):
    a,b,_,_,_=problem(d,a0,temporal,policy);y=np.asarray(y,float)
    assert y.shape==(len(b),) and np.isfinite(y).all()
    tol=contract['certificate_tolerance'];margin=float(-b@y)
    slack=float(np.min(a.T@y));norm=float(np.max(np.abs(y)))
    assert slack>=-tol and norm<=1+tol and margin>tol
    return dict(separation_margin=margin,minimum_cone_slack=slack,witness_infinity_norm=norm)

def solve(d,a0,temporal,policy,contract):
    a,b,_,_,_=problem(d,a0,temporal,policy)
    options={k:v for k,v in contract['solver'].items() if k!='method'}
    res=linprog(np.ones(a.shape[1]),A_eq=a,b_eq=b,bounds=(0,None),
                method=contract['solver']['method'],options=options)
    singular=np.linalg.svd(a,compute_uv=False);rank=int(np.sum(singular>contract['rank_relative_cutoff']*singular[0])) if len(singular) else 0
    out=dict(status='UNRESOLVED',solver_status=int(res.status),iterations=int(res.nit),solver_message=str(res.message),singular_values=singular.tolist(),rank=rank)
    if res.status==0:
        out.update(primal=res.x.tolist(),dual=res.eqlin.marginals.tolist())
        try:w,cert=checked_feasible(d,a0,temporal,policy,res.x,res.eqlin.marginals,contract)
        except AssertionError:return dict(out,reason='failed_optimality_certificate')
        out.update(status='FEASIBLE',certificate=cert,weights=w.tolist(),minimum_mass=cert['mass'],
                   mass_ratio=cert['mass']/float(np.abs(a0).sum()))
    elif res.status==2:
        sep=linprog(b,A_ub=-a.T,b_ub=np.zeros(a.shape[1]),bounds=[(-1,1)]*len(b),
                    method=contract['solver']['method'],options=options)
        out.update(separator_solver_status=int(sep.status),separator_iterations=int(sep.nit))
        if sep.status==0:
            out['separating_dual']=sep.x.tolist()
            try:cert=checked_infeasible(d,a0,temporal,policy,sep.x,contract)
            except AssertionError:return dict(out,reason='failed_infeasibility_certificate')
            out.update(status='INFEASIBLE',certificate=cert)
    return out

def validate_record(record,contract):
    for family in record['supports'].values():
        if family['status']!='ok':continue
        d=np.array(family['design']);a0=np.array(family['baseline_coefficients']);mask=family['temporal_mask']
        for policy,row in family['policies'].items():
            if row['status']=='FEASIBLE':
                weights,cert=checked_feasible(d,a0,mask,policy,row['primal'],row['dual'],contract)
                np.testing.assert_allclose(weights,row['weights'],atol=1e-10,rtol=1e-9)
                for k,v in cert.items():np.testing.assert_allclose(v,row['certificate'][k],atol=1e-10,rtol=1e-9)
                np.testing.assert_allclose(cert['mass'],row['minimum_mass'],atol=1e-10,rtol=1e-9)
                np.testing.assert_allclose(cert['mass']/np.abs(a0).sum(),row['mass_ratio'],atol=1e-10,rtol=1e-9)
            elif row['status']=='INFEASIBLE':
                cert=checked_infeasible(d,a0,mask,policy,row['separating_dual'],contract)
                for k,v in cert.items():np.testing.assert_allclose(v,row['certificate'][k],atol=1e-10,rtol=1e-9)
    return True
