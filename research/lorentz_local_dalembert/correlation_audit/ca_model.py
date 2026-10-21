"""SPDX-License-Identifier: Apache-2.0
All covariance interventions preserve the diagonal and positive definiteness.
"""
import numpy as np
from scipy.linalg import cho_factor,cho_solve
from ca_common import cfg,matrices,covariance,basis,canonical,correct,intervals,order_check

def intervention(M,parameters,name):
    K=covariance(M,parameters,'grouped');diagonal=np.diag(np.diag(K))
    if name=='diagonal':return diagonal
    if name=='full':return K
    if name in cfg()['shrinkage']:
        strength=cfg()['shrinkage'][name];return diagonal+strength*(K-diagonal)
    if name=='within_groups':
        mask=sum(np.outer(g,g) for g in M['groups'].values());return K*mask
    if name.startswith('drop_'):
        B,names,_=basis(M,'grouped');k=names.index(name[5:])
        component=M['D'][:,None]*(parameters[k]*B[k])*M['D'][None,:]
        return K-component+np.diag(np.diag(component))
    raise ValueError(name)

def predict(intrinsic,order,frozen):
    if intrinsic['status']!='COMPLETE':return dict(status=intrinsic['status'])
    features=np.asarray(intrinsic['projection']['features']);M=matrices(features,order)
    params=frozen['models']['grouped']['projected'];target=M['q']-params['bias_shrinkage']*(M['group_X']@params['bias_coefficients'])
    initial=None;reason=None
    try:initial=canonical(features,order)
    except (ValueError,AssertionError,np.linalg.LinAlgError) as exc:reason=str(exc)
    variants={}
    for name in cfg()['candidates']:
        K=intervention(M,params['variance_components'],name);condition=float(np.linalg.cond(K))
        if reason or condition>cfg()['maximum_covariance_condition']:
            result=dict(status='FALLBACK',reason=reason or 'covariance condition limit',features=features.tolist())
        else:result=correct(initial,order,target,K,'full')
        p=np.vstack((np.zeros(3),result['features']));result['order']=order_check(p,order)
        result['covariance_condition']=condition;variants[name]=result
    return dict(status='COMPLETE',variants=variants)

def loss(error,delta,weights):
    initial=float(weights@(error*error));cross=float(2*weights@(error*delta));step=float(weights@(delta*delta))
    final=float(weights@((error+delta)**2))
    return dict(initial_mse=initial,mse=final,cross_term=cross,step_squared=step,mse_change=final-initial)

def evaluate(old_row,prediction,frozen):
    if prediction['status']!='COMPLETE':return dict(status=prediction['status'])
    intrinsic=old_row['cloud']['intrinsic'];order=old_row['cloud']['observed_order']
    M=matrices(intrinsic['projection']['features'],order)
    truth=intervals(np.asarray(old_row['true_support_points'])/intrinsic['scale']);e=M['q']-truth;w=M['fit_weight']
    ps={**old_row['prediction']['variants'],**prediction['variants']};variants={}
    params=frozen['models']['grouped']['projected'];K=covariance(M,params['variance_components'],'grouped')
    reference_conditions={'baseline':1.,'unweighted':1.,'diagonal':float(np.max(np.diag(K))/np.min(np.diag(K))), 'full':float(np.linalg.cond(K))}
    for name,p in ps.items():
        points=np.vstack((np.zeros(3),p['features']));q=intervals(points);delta=q-M['q'];L=loss(e,delta,w)
        denom=float((w*M['q'])@M['q']);amplitude=float((w*M['q'])@delta/denom)
        fraction=amplitude**2*denom/L['step_squared'] if L['step_squared']>1e-24 else 0.
        groups={g:loss(e[mask],delta[mask],np.full(mask.sum(),1/mask.sum())) for g,mask in M['groups'].items() if mask.any()}
        variants[name]=dict(**L,groups=groups,scale_step_amplitude=amplitude,scale_step_energy_fraction=float(fraction),
            fallback=p['status']=='FALLBACK',order=order_check(points,order),
            covariance_condition=p['covariance_condition'] if 'covariance_condition' in p else reference_conditions[name])
    sd=np.sqrt(np.diag(K));R=K/sd[:,None]/sd[None,:];values,vectors=np.linalg.eigh(R)
    bias=params['bias_shrinkage']*(M['group_X']@params['bias_coefficients']);residual=(e-bias)/sd
    z=(vectors.T@residual)/np.sqrt(values);m=len(values);edges=[0,m//4,3*m//4,m]
    spectral={name:dict(modes=edges[j+1]-edges[j],eigenvalue_min=float(values[edges[j]]),eigenvalue_max=float(values[edges[j+1]-1]),
        mean_standardized_square=float(np.mean(z[edges[j]:edges[j+1]]**2))) for j,name in enumerate(['lowest_quarter','middle_half','highest_quarter'])}
    # Rank-one identity before any irrelevant common precision normalization.
    k=params['component_names'].index('signed_common_scale');v=params['variance_components'][k]
    K0=K-v*np.outer(M['q'],M['q']);b=float(M['q']@cho_solve(cho_factor(K0,lower=True),M['q']))
    attenuation=1/(1+v*b);actual=float(M['q']@cho_solve(cho_factor(K,lower=True),M['q']))/b
    return dict(status='COMPLETE',variants=variants,spectral=spectral,correlation_condition=float(values[-1]/values[0]),
        signed_scale_precision_attenuation=attenuation,rank_one_identity_error=abs(actual-attenuation))
