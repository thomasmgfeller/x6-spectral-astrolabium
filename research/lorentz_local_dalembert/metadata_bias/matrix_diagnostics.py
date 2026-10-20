"""Read-only diagnostics. No new selection or acceptance rules."""
import numpy as np
from mb_common import contract
from feasibility import design, TARGET
from cg_relations import constraints
from cg_common import contract as geometry_contract


def spectrum(a,tol):
    a=np.asarray(a,float)
    sv=np.linalg.svd(a,compute_uv=False) if min(a.shape)>0 else np.array([])
    rank=int(np.sum(sv>tol*sv[0])) if len(sv) else 0
    cond=float(sv[0]/sv[-1]) if len(sv) and sv[-1]>0 else None
    return dict(shape=list(a.shape),singular_values=sv.tolist(),rank=rank,
                relative_rank_threshold=tol,condition=cond)


def diagnose(rows):
    records=[]
    for r in rows:
        intr=r['intrinsic']; entry=dict(seed=r['seed'],status=intr['status'])
        if intr['status']!='COMPLETE':
            records.append(entry);continue
        initial=np.vstack(([0.,0.,0.],intr['original_features']))
        repaired=np.vstack(([0.,0.,0.],intr['projection']['features']))
        weights=np.asarray(r['metadata_inference']['weights'])
        entry['moments']=[]
        for arm,x in enumerate([initial[1:],repaired[1:]]):
            d=design(x); n=d.shape[1]
            hi=np.eye(n)+(1/np.sqrt(n+1)-1)/n*np.ones((n,n))
            spec=spectrum(d,1e-12)
            ids=[0,1,4] if arm==0 else [2,3,5]
            entry['moments'].append(dict(arm=arm,matrix=spec,
                full_row_rank=spec['rank']==9,expected_weight_nullity=n-9,
                noise_weighted_moment_matrix=spectrum(d@hi,1e-12),
                maximum_moment_residual=max(float(np.max(np.abs(d@weights[j]-TARGET))) for j in ids),
                existing_condition_guard=geometry_contract()['maximum_design_condition']))
        fun,jac,_=constraints(initial,np.asarray(r['observed_order'],bool),geometry_contract()['projection']['margin'])
        v=repaired[1:].ravel(); slack=fun(v); active=slack<=1e-7
        entry['projection']=dict(solver_success=intr['projection']['solver_success'],
            iterations=intr['projection']['iterations'],minimum_constraint_slack=float(slack.min()),
            active_threshold=1e-7,active_constraints=int(active.sum()),
            active_constraint_jacobian=spectrum(jac(v)[active],1e-10),
            meaning='Constraint Jacobian only. Redundancy is possible; not a stochastic measurement Jacobian.')
        records.append(entry)
    good=[r for r in records if 'moments' in r]
    conditions=np.array([[v['matrix']['condition'] for v in r['moments']] for r in good])
    return dict(scope='Passive diagnostics; no changed numerical decisions or inferred embedding covariance.',
        geometry_measurement_jacobian=None,
        geometry_measurement_jacobian_reason='No statistical full-embedding observation model has been defined.',
        clouds=len(rows),complete=len(good),
        full_row_rank_failures=sum(not m['full_row_rank'] for r in good for m in r['moments']),
        maximum_moment_residual=max(m['maximum_moment_residual'] for r in good for m in r['moments']),
        condition_by_arm=[dict(min=float(v.min()),median=float(np.median(v)),max=float(v.max())) for v in conditions.T],
        records=records)
