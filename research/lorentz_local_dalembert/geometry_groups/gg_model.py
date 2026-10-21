"""SPDX-License-Identifier: Apache-2.0
Grouped invariant uncertainty; every prediction uses inference-only inputs.
"""
import numpy as np
from scipy.optimize import nnls
from gg_common import cfg,old,design
from gu_model import matrices as old_matrices,intervals,development_rows as older_rows

def matrices(features,order):
    M=old_matrices(features,order);i,j=M['pairs'].T;o=np.asarray(order,bool)
    causal=o[i,j]|o[j,i]
    masks=[i==0,(i!=0)&~causal,(i!=0)&causal]
    M['groups']={name:mask for name,mask in zip(cfg()['groups'],masks)}
    for name,mask in M['groups'].items():
        if mask.any():M['blocks'][name]=mask.astype(float)/mask.sum()
    # Each cloud and each nonempty group have equal total fitting weight.
    present=sum(mask.any() for mask in masks)
    M['fit_weight']=sum(mask.astype(float)/mask.sum()/present for mask in masks if mask.any())
    M['group_X']=np.column_stack([v for mask in masks for v in [mask.astype(float),mask*M['q']]])
    return M

def basis(M,which):
    if which=='pooled':return M['R'],['independent','shared_endpoint','shared_cloud'],[0]
    masks=list(M['groups'].values());P=M['R'][1]
    B=[np.diag(mask.astype(float)) for mask in masks]
    names=[name+'_independent' for name in cfg()['groups']]
    B.append(P);names.append('cross_group_endpoint')
    # Root-only endpoint kernel equals (I_root + 1_root 1_root.T)/2:
    # omit that redundant component to preserve identifiability.
    for k in [1,2]:
        B.append(P*masks[k][:,None]*masks[k][None,:]);names.append(cfg()['groups'][k]+'_endpoint')
    for name,mask in M['groups'].items():
        B.append(np.outer(mask,mask).astype(float));names.append(name+'_cloud')
    u=M['q']/M['D'];B.append(np.outer(u,u));names.append('signed_common_scale')
    return B,names,[0,1,2]

def covariance(M,parameters,which):
    B,_,_=basis(M,which);R=sum(v*b for v,b in zip(parameters,B))
    return M['D'][:,None]*R*M['D'][None,:]

def development_rows():
    out=[]
    for r in older_rows():
        out.append((r['cloud']['intrinsic'],r['cloud']['observed_order'],r['evaluation']['true_support_points']))
    for phase in ['calibration','test']:
        _,rows=old.load_phase(phase)
        for r in rows:
            if r['evaluation']['status']=='COMPLETE':
                out.append((r['cloud']['intrinsic'],r['cloud']['observed_order'],r['true_support_points']))
    return out

def ridge(xx,xy):
    penalty=cfg()['bias_ridge_relative']*np.trace(xx)/len(xx)
    return np.linalg.solve(xx+penalty*np.eye(len(xx)),xy)

def fit_one(data,which):
    terms=[]
    for features,order,truth in data:
        M=matrices(features,order);X=M['X'] if which=='pooled' else M['group_X']
        e=M['q']-truth;w=M['fit_weight']
        terms.append((X.T@(w[:,None]*X),X.T@(w*e),X,e,w))
    xx=sum(t[0] for t in terms);xy=sum(t[1] for t in terms)
    beta=ridge(xx,xy);grid=cfg()['bias_shrinkage_grid'];risk=np.zeros(len(grid))
    for tx,ty,X,e,w in terms:
        loo=ridge(xx-tx,xy-ty);b=X@loo
        risk+=np.array([np.sum(w*(e-g*b)**2) for g in grid])/len(terms)
    candidates=np.where(risk<=risk.min()+1e-12*max(1.,float(risk.min())))[0]
    shrink=grid[int(candidates[0])]
    G=None;rhs=None;raw=[];adjusted=[]
    for (features,order,truth),term in zip(data,terms):
        M=matrices(features,order);X=term[2];e=term[3];w=term[4]
        residual=e-shrink*(X@beta);z=residual/M['D'];B,names,floors=basis(M,which)
        # sqrt(w) on both axes weights every group-pair block equally.
        sw=np.sqrt(w);C=np.array([sw[:,None]*b*sw[None,:] for b in B]);v=sw*z
        if G is None:G=np.zeros((len(B),len(B)));rhs=np.zeros(len(B))
        flat=C.reshape(len(B),-1);G+=flat@flat.T
        rhs+=np.einsum('i,kij,j->k',v,C,v)
        raw.append(float(np.sum(w*e*e)));adjusted.append(float(np.sum(w*residual*residual)))
    floor=np.zeros(len(names));floor[floors]=cfg()['independent_variance_floor']
    scales=np.sqrt(np.diag(G));assert np.min(scales)>0
    Gn=G/scales[:,None]/scales[None,:];bn=(rhs-G@floor)/scales
    L=np.linalg.cholesky(Gn)
    vn,residual=nnls(L.T,np.linalg.solve(L,bn),maxiter=10000);parameters=vn/scales+floor
    return dict(bias_coefficients=beta.tolist(),bias_shrinkage=shrink,loo_risk_by_shrinkage=risk.tolist(),
        variance_components=parameters.tolist(),component_names=names,
        component_gram_condition=float(np.linalg.cond(Gn)),moment_fit_residual=float(residual),
        raw_group_balanced_mse=float(np.mean(raw)),adjusted_group_balanced_mse=float(np.mean(adjusted)))

def fit():
    rows=development_rows();out={which:{} for which in cfg()['models']};metadata=[]
    for arm in cfg()['arms']:
        data=[]
        for intrinsic,order,points in rows:
            x=intrinsic['original_features'] if arm=='original' else intrinsic['projection']['features']
            data.append((x,order,intervals(np.asarray(points)/intrinsic['scale'])))
            if arm=='original':metadata.append([len(x),float(np.linalg.cond(design(np.asarray(x))))])
        for which in cfg()['models']:out[which][arm]=fit_one(data,which)
    meta=np.array(metadata)
    return dict(status='FROZEN_DEVELOPMENT_MODEL',development_attempts=128,development_complete=len(rows),
        interpretation='PR74 and PR76 clouds reused for development. No independent claim on those data.',
        models=out,support_cut=float(np.median(meta[:,0])),condition_cut=float(np.median(meta[:,1])),
        metadata_min=meta.min(axis=0).tolist(),metadata_max=meta.max(axis=0).tolist())

def predict(intrinsic,order,frozen):
    if intrinsic['status']!='COMPLETE':return dict(status=intrinsic['status'])
    models={which:{} for which in cfg()['models']}
    for arm in cfg()['arms']:
        x=intrinsic['original_features'] if arm=='original' else intrinsic['projection']['features']
        M=matrices(x,order);H=M['H']
        for which in cfg()['models']:
            params=frozen['models'][which][arm];X=M['X'] if which=='pooled' else M['group_X']
            bias=params['bias_shrinkage']*(X@np.asarray(params['bias_coefficients']));centre=M['q']-bias
            K=covariance(M,params['variance_components'],which)
            sd=np.sqrt(np.diag(K));gsd=np.sqrt(np.einsum('ij,ij->i',H@K,H))
            assert min(sd)>0 and min(gsd)>0
            blocks={}
            for name,w in M['blocks'].items():
                var=float(w@K@w);diagonal=float(np.sum(w*w*np.diag(K)))
                blocks[name]=dict(centre=float(w@centre),sd=float(np.sqrt(var)),shared_to_diagonal_variance_ratio=var/diagonal)
            models[which][arm]=dict(interval_centre=centre.tolist(),interval_sd=sd.tolist(),bias=bias.tolist(),
                gram_centre=(H@centre).tolist(),gram_sd=gsd.tolist(),blocks=blocks,
                covariance_condition=float(np.linalg.cond(K)),pair_count=len(centre),
                group_median_sd={name:float(np.median(sd[mask])) for name,mask in M['groups'].items() if mask.any()})
    x=np.asarray(intrinsic['original_features']);meta=np.array([len(x),np.linalg.cond(design(x))])
    return dict(status='COMPLETE',models=models,scale=intrinsic['scale'],support_count=len(x),
        design_condition=float(meta[1]),support_stratum='low' if meta[0]<=frozen['support_cut'] else 'high',
        condition_stratum='low' if meta[1]<=frozen['condition_cut'] else 'high',
        outside_development_range=bool(np.any(meta<frozen['metadata_min']) or np.any(meta>frozen['metadata_max'])))

def evaluate(intrinsic,order,prediction,true_points):
    if prediction['status']!='COMPLETE':return dict(status=prediction['status'])
    truth=intervals(np.asarray(true_points)/prediction['scale']);models={}
    for which,arms in prediction['models'].items():
        results={};score=0.
        for arm,p in arms.items():
            x=intrinsic['original_features'] if arm=='original' else intrinsic['projection']['features']
            M=matrices(x,order);e=np.asarray(p['interval_centre'])-truth;iz=e/np.asarray(p['interval_sd'])
            gz=(np.asarray(p['gram_centre'])-M['H']@truth)/p['gram_sd']
            blocks={name:float((p['blocks'][name]['centre']-w@truth)/p['blocks'][name]['sd']) for name,w in M['blocks'].items()}
            family=dict(interval=float(np.max(abs(iz))),gram=float(np.max(abs(gz))),block=float(max(abs(v) for v in blocks.values())))
            groups={name:dict(n=int(mask.sum()),max_abs_z=float(np.max(abs(iz[mask]))),
                mean_z=float(np.mean(iz[mask])),second_moment=float(np.mean(iz[mask]**2)),
                raw_mse=float(np.mean((M['q'][mask]-truth[mask])**2)),adjusted_mse=float(np.mean(e[mask]**2)))
                for name,mask in M['groups'].items() if mask.any()}
            arm_score=max(family.values());score=max(score,arm_score)
            results[arm]=dict(score=arm_score,family_scores=family,standardized_blocks=blocks,groups=groups,
                raw_mse=float(np.mean((M['q']-truth)**2)),adjusted_mse=float(np.mean(e*e)),
                standardized_pointwise_second_moment=float(np.mean(iz*iz)))
        models[which]=dict(score=score,arms=results)
    return dict(status='COMPLETE',models=models,true_intervals=truth.tolist())
