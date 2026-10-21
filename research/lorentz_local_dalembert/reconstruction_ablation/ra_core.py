"""SPDX-License-Identifier: Apache-2.0
Truth-assisted reference only; no changes to deployed/frozen inference.
"""
import math
import numpy as np
from ra_common import cfg,close,ec,design,TARGET,minimum_variance,field_values


def reference(points,scale):
    x=np.asarray(points,float);d=design(x/scale)
    sv=np.linalg.svd(d,compute_uv=False)
    rank=int(np.count_nonzero(sv>cfg()['relative_rank_cutoff']*sv[0])) if len(sv) and sv[0]>0 else 0
    condition=float(sv[0]/sv[-1]) if len(sv)==9 and sv[-1]>0 else None
    if rank!=9 or condition is None or condition>cfg()['maximum_oracle_design_condition']:
        return dict(status='ORACLE_UNAVAILABLE',reason='rank or condition',rank=rank,condition=condition)
    q=minimum_variance(d)
    if q['status']!='VERIFIED':return dict(status='ORACLE_UNAVAILABLE',reason='uncertified QP',rank=rank,condition=condition)
    a=np.asarray(q['weights']);h=np.eye(len(x))+np.ones((len(x),len(x)))
    l=np.linalg.cholesky(h)
    c=np.linalg.solve(l,d.T).T
    u,s,vt=np.linalg.svd(c,full_matrices=False)
    alternative=np.linalg.solve(l.T,vt.T@((u.T@TARGET)/s))
    close(a,alternative);close(d@alternative,TARGET)
    full=np.r_[-a.sum(),a]/scale**2
    physical=design(x)@full[1:]-TARGET
    close(physical,0);close(full.sum(),0)
    return dict(status='COMPLETE',rank=rank,condition=condition,scale=scale,
                full_coefficients=full.tolist(),dimensionless_weights=a.tolist(),
                physical_moment_residuals=physical.tolist(),certificate=q['certificate'],
                independent_svd_max_weight_difference=float(np.max(np.abs(a-alternative))))


def taylor_parts(points,spec,weights):
    x=np.asarray(points);b=np.asarray(weights)
    contrast,truth=field_values(x,spec)
    phase=spec['phase'];u=x@np.asarray(spec['k'])
    root=math.cos(phase) if spec['kind']=='cos' else math.sin(phase)
    derivative=-math.sin(phase) if spec['kind']=='cos' else math.cos(phase)
    linear=derivative*u;quadratic=-.5*root*u*u
    remainder=contrast-linear-quadratic
    values=np.array([b[:,1:]@linear,b[:,1:]@quadratic-truth,b[:,1:]@remainder]).T
    total=b[:,1:]@contrast-truth
    close(values.sum(axis=1),total)
    scalar=np.array([math.fsum(float(a)*float(v) for a,v in zip(row[1:],contrast))-truth for row in b])
    close(total,scalar)
    return dict(name=spec['name'],truth=truth,errors=total.tolist(),taylor=values.tolist())


def evaluate(row):
    base=dict(phase=row['phase'],index=row['index'],seed=row['seed'],input_status=row['evaluation']['status'])
    if base['input_status']!='COMPLETE':return dict(base,status='INPUT_UNAVAILABLE',reason=base['input_status'])
    v=row['evaluation'];p=row['prepared'];points=np.asarray(v['true_support_points'])
    close(points[0],0);scale=p['scale']
    # Recompute both geometry-only policies on their stored reconstructed features.
    old=np.asarray(v['full_coefficients'])
    for arm,features in [(0,row['cloud']['intrinsic']['original_features']),
                         (2,row['cloud']['intrinsic']['projection']['features'])]:
        q=minimum_variance(design(features));assert q['status']=='VERIFIED'
        a=np.asarray(q['weights']);close(np.r_[-a.sum(),a]/scale**2,old[arm])
    oracle=reference(points[1:],scale)
    if oracle['status']!='COMPLETE':return dict(base,status='ORACLE_UNAVAILABLE',oracle=oracle)
    weights=np.vstack((old,np.asarray(oracle['full_coefficients'])))
    moments=weights[:,1:]@design(points[1:]).T-TARGET
    close(moments[4],0);close(weights.sum(axis=1),0)
    fields=[]
    for spec,saved in zip(ec.cfg()['fields'],v['fields']):
        f=taylor_parts(points[1:],spec,weights)
        error=np.asarray(f['errors']);close(error[:4],saved['error'])
        close(np.asarray(f['taylor'])[4,:2],0)
        d=error[4];r=error[[0,2]]-d;c=error[[1,3]]-error[[0,2]]
        close(d+r,error[[0,2]]);close(d+r+c,error[[1,3]])
        f.update(discretization=float(d),reconstruction=r.tolist(),metadata_increment=c.tolist())
        fields.append(f)
    return dict(base,status='COMPLETE',support_count=len(points)-1,oracle=oracle,
                arm_order=['original','metadata','projected','projected_metadata','oracle'],
                hypothetical_iid_variance=(ec.cfg()['field_noise_sigma']**2*np.sum(weights*weights,axis=1)).tolist(),
                physical_moment_residuals=moments.tolist(),fields=fields)
