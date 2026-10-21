"""SPDX-License-Identifier: Apache-2.0"""
import inspect
import json
from copy import deepcopy
import numpy as np
from ca_common import cfg,close,matrices,covariance,basis
from ca_model import intervention,loss,predict
from ca_analyze import select
from gc_controls import order_of,check as old_check

def check():
    p=np.array([[0.,0.,0.],[2.,.2,.1],[-1.,.1,-.1],[.2,1.,.3],[.4,-.5,1.1],[1.,1.5,-.3]])
    M=matrices(p[1:],order_of(p));B,names,_=basis(M,'grouped')
    v=np.linspace(.01,.1,len(B));v[names.index('root_cloud')]=0;v[names.index('support_causal_endpoint')]=0
    K=covariance(M,v,'grouped');sd=np.sqrt(np.diag(K));R=K/sd[:,None]/sd[None,:]
    for name in cfg()['candidates']+['diagonal','full','drop_root_cloud','drop_support_causal_endpoint']:
        A=intervention(M,v,name);close(np.diag(A),np.diag(K));close(A,A.T)
        assert np.linalg.eigvalsh(A).min()>0
    close(intervention(M,v,'drop_root_cloud'),K);close(intervention(M,v,'drop_support_causal_endpoint'),K)
    blocks=intervention(M,v,'within_groups')
    for a,ma in M['groups'].items():
        for b,mb in M['groups'].items():close(blocks[np.ix_(ma,mb)],K[np.ix_(ma,mb)] if a==b else 0)
    conditions=[1.]
    for name,strength in cfg()['shrinkage'].items():
        A=intervention(M,v,name)/sd[:,None]/sd[None,:]
        close(np.linalg.eigvalsh(A),1+strength*(np.linalg.eigvalsh(R)-1));conditions.append(np.linalg.cond(A))
    conditions.append(np.linalg.cond(R));assert np.all(np.diff(conditions)>=-1e-10)
    for name in [n for n in cfg()['candidates'] if n.startswith('drop_')]:
        k=names.index(name[5:]);C=M['D'][:,None]*(v[k]*B[k])*M['D'][None,:]
        close(intervention(M,v,name),K-C+np.diag(np.diag(C)))
    e=np.linspace(-.3,.4,len(M['q']));d=np.linspace(.1,-.2,len(e));w=M['fit_weight'];L=loss(e,d,w)
    close(L['mse_change'],L['cross_term']+L['step_squared']);close(loss(e,-e,w)['mse'],0.)
    assert loss(e,e,w)['mse_change']>0
    for d in [M['q'],e,np.zeros_like(e)]:
        denom=(w*M['q'])@M['q'];a=(w*M['q'])@d/denom;energy=(w*d)@d
        fraction=a*a*denom/energy if energy>1e-24 else 0.;assert -1e-12<=fraction<=1+1e-12
    k=names.index('signed_common_scale');K0=K-v[k]*np.outer(M['q'],M['q']);b=M['q']@np.linalg.solve(K0,M['q'])
    close((M['q']@np.linalg.solve(K,M['q']))/b,1/(1+v[k]*b))
    close((M['q']@np.linalg.solve(K0,M['q']))/b,1.)
    assert list(inspect.signature(predict).parameters)==['intrinsic','order','frozen']
    variants={n:dict(rmse=.98,ratio_to_baseline=.98,ratio_to_diagonal=.98,groups={g:dict(rmse=.98) for g in M['groups']},order_violations=0,fallbacks=0) for n in cfg()['candidates']}
    variants['baseline']=dict(groups={g:dict(rmse=1.) for g in M['groups']})
    blocks={s:dict(complete=64,variants=deepcopy(variants)) for s in ['calibration','test']};pooled=dict(variants=deepcopy(variants))
    result=select(blocks,pooled);assert result['selected']==cfg()['candidates'][0]
    name=cfg()['candidates'][0]
    mutations=[lambda b:b.update(complete=47),lambda b:b['variants'][name].update(ratio_to_baseline=.991),
        lambda b:b['variants'][name].update(ratio_to_diagonal=1.001),lambda b:b['variants'][name]['groups']['root'].update(rmse=1.051),
        lambda b:b['variants'][name].update(order_violations=1),lambda b:b['variants'][name].update(fallbacks=7)]
    for phase in blocks:
        for mutate in mutations:
            b=deepcopy(blocks);mutate(b[phase]);assert name not in select(b,pooled)['eligible']
    b=deepcopy(blocks)
    for n in cfg()['candidates']:b['test']['variants'][n]['ratio_to_baseline']=1.
    assert select(b,pooled)['decision']=='STOP_CORRELATION_CORRECTION_SCREEN'
    pooled['variants'][cfg()['candidates'][1]]['rmse']=.97;assert select(blocks,pooled)['selected']==cfg()['candidates'][1]
    return dict(status='PASS',groups=['positive_definiteness','fixed_marginal_variances','group_blocks','shrinkage_spectrum',
        'isolated_component_correlations','zero_component_noop','exact_loss_decomposition','scale_energy_bounds',
        'rank_one_identity','inference_only_signature','both_block_gate_negative_controls','ranking_and_ties'],inherited=old_check())
if __name__=='__main__':print(json.dumps(check()))
