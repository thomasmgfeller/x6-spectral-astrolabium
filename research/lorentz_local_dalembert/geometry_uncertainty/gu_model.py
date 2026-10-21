"""SPDX-License-Identifier: Apache-2.0
Invariant geometry prediction. No true coordinates enter predict().
"""
import numpy as np
from scipy.optimize import nnls
from gu_common import cfg,ec,design

def intervals(points):
    p=np.asarray(points);i,j=np.triu_indices(len(p),1);d=p[i]-p[j]
    return np.sum(d*d*np.array([-1.,1.,1.]),axis=1)

def matrices(features,order):
    x=np.vstack((np.zeros(3),np.asarray(features)))
    n=len(x);i,j=np.triu_indices(n,1);m=len(i);q=intervals(x)
    X=np.column_stack((np.ones(m),q,(i==0).astype(float)))
    A=np.zeros((m,n));A[np.arange(m),i]=A[np.arange(m),j]=1/np.sqrt(2.)
    R=[np.eye(m),A@A.T,np.ones((m,m))]
    H=[];gram_pairs=[];lookup={(a,b):k for k,(a,b) in enumerate(zip(i,j))}
    for a in range(1,n):
        for b in range(a,n):
            v=np.zeros(m)
            if a==b:v[lookup[(0,a)]]=1.
            else:
                v[lookup[(0,a)]]=.5;v[lookup[(0,b)]]=.5;v[lookup[(a,b)]]=-.5
            H.append(v);gram_pairs.append([a,b])
    o=np.asarray(order,bool);causal=o[i,j]|o[j,i]
    masks=[np.ones(m,bool),i==0,i!=0,causal,~causal,
           np.abs(q)<=cfg()['near_threshold'],np.abs(q)>cfg()['near_threshold']]
    blocks={name:mask.astype(float)/mask.sum() for name,mask in zip(cfg()['blocks'],masks) if mask.any()}
    return dict(q=q,X=X,D=np.sqrt(1+q*q),R=R,H=np.array(H),blocks=blocks,
                pairs=np.column_stack((i,j)),gram_pairs=gram_pairs,n=n-1)

def covariance(M,parameters):
    R=sum(v*r for v,r in zip(parameters,M['R']))
    return M['D'][:,None]*R*M['D'][None,:]

def development_rows():
    rows=[]
    for phase in ['calibration','test']:
        _,batch=ec.load_phase(phase)
        rows.extend(r for r in batch if r['evaluation']['status']=='COMPLETE')
    return rows

def fit():
    rows=development_rows();out={};metadata=[]
    for arm in cfg()['arms']:
        data=[]
        for row in rows:
            intrinsic=row['cloud']['intrinsic'];scale=intrinsic['scale']
            x=intrinsic['original_features'] if arm=='original' else intrinsic['projection']['features']
            M=matrices(x,row['cloud']['observed_order'])
            truth=intervals(np.asarray(row['evaluation']['true_support_points'])/scale)
            data.append((M,M['q']-truth))
            if arm=='original':metadata.append([M['n'],float(np.linalg.cond(design(np.asarray(x))))])
        xx=sum(M['X'].T@M['X']/len(e) for M,e in data)
        xy=sum(M['X'].T@e/len(e) for M,e in data)
        beta=np.linalg.solve(xx,xy)
        G=np.zeros((3,3));b=np.zeros(3)
        for M,e in data:
            z=(e-M['X']@beta)/M['D'];m=len(z)
            for a in range(3):
                b[a]+=float(z@M['R'][a]@z)/(m*m)
                for k in range(3):G[a,k]+=np.sum(M['R'][a]*M['R'][k])/(m*m)
        floor=np.array([cfg()['independent_variance_floor'],0.,0.])
        L=np.linalg.cholesky(G)
        v,residual=nnls(L.T,np.linalg.solve(L,b-G@floor));v+=floor
        out[arm]=dict(bias_coefficients=beta.tolist(),variance_components=v.tolist(),
            component_names=['independent','shared_endpoint','shared_cloud'],moment_fit_residual=float(residual),
            raw_cloud_balanced_mse=float(np.mean([np.mean(e*e) for M,e in data])),
            adjusted_cloud_balanced_mse=float(np.mean([np.mean((e-M['X']@beta)**2) for M,e in data])))
    meta=np.array(metadata)
    return dict(status='FROZEN_DEVELOPMENT_MODEL',development_attempts=64,development_complete=len(rows),
        interpretation='Reused historical data; working invariant covariance, not a conditional embedding covariance.',
        arms=out,support_cut=float(np.median(meta[:,0])),condition_cut=float(np.median(meta[:,1])),
        metadata_min=meta.min(axis=0).tolist(),metadata_max=meta.max(axis=0).tolist())

def predict(intrinsic,order,frozen):
    if intrinsic['status']!='COMPLETE':return dict(status=intrinsic['status'])
    out={}
    for arm in cfg()['arms']:
        x=intrinsic['original_features'] if arm=='original' else intrinsic['projection']['features']
        M=matrices(x,order);params=frozen['arms'][arm]
        bias=M['X']@np.asarray(params['bias_coefficients']);centre=M['q']-bias
        K=covariance(M,params['variance_components']);H=M['H']
        sd=np.sqrt(np.diag(K));gsd=np.sqrt(np.einsum('ij,ij->i',H@K,H))
        assert np.min(sd)>0 and np.min(gsd)>0
        blocks={}
        for name,w in M['blocks'].items():
            var=float(w@K@w);diagonal=float(np.sum(w*w*np.diag(K)))
            blocks[name]=dict(centre=float(w@centre),sd=float(np.sqrt(var)),
                shared_to_diagonal_variance_ratio=var/diagonal)
        out[arm]=dict(interval_centre=centre.tolist(),interval_sd=sd.tolist(),bias=bias.tolist(),
            gram_centre=(H@centre).tolist(),gram_sd=gsd.tolist(),blocks=blocks,
            covariance_condition=float(np.linalg.cond(K)),pair_count=len(centre))
    x=np.asarray(intrinsic['original_features']);meta=np.array([len(x),np.linalg.cond(design(x))])
    return dict(status='COMPLETE',arms=out,scale=intrinsic['scale'],support_count=len(x),
        design_condition=float(meta[1]),support_stratum='low' if meta[0]<=frozen['support_cut'] else 'high',
        condition_stratum='low' if meta[1]<=frozen['condition_cut'] else 'high',
        outside_development_range=bool(np.any(meta<frozen['metadata_min']) or np.any(meta>frozen['metadata_max'])))

def evaluate(intrinsic,order,prediction,true_points):
    if prediction['status']!='COMPLETE':return dict(status=prediction['status'])
    truth=intervals(np.asarray(true_points)/prediction['scale']);arms={};score=0.
    for arm,p in prediction['arms'].items():
        x=intrinsic['original_features'] if arm=='original' else intrinsic['projection']['features']
        M=matrices(x,order);error=np.asarray(p['interval_centre'])-truth
        iz=error/np.asarray(p['interval_sd'])
        gz=(np.asarray(p['gram_centre'])-M['H']@truth)/np.asarray(p['gram_sd'])
        blocks={name:float((p['blocks'][name]['centre']-w@truth)/p['blocks'][name]['sd']) for name,w in M['blocks'].items()}
        family=dict(interval=float(np.max(np.abs(iz))),gram=float(np.max(np.abs(gz))),
                    block=float(max(abs(v) for v in blocks.values())))
        arm_score=max(family.values());score=max(score,arm_score)
        arms[arm]=dict(score=arm_score,family_scores=family,standardized_blocks=blocks,
            standardized_pointwise_second_moment=float(np.mean(iz*iz)),
            raw_mean_error=float(np.mean(M['q']-truth)),adjusted_mean_error=float(np.mean(error)),
            raw_mse=float(np.mean((M['q']-truth)**2)),adjusted_mse=float(np.mean(error*error)))
    return dict(status='COMPLETE',score=score,arms=arms,true_intervals=truth.tolist())
