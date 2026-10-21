"""Sampler and independent coordinate-based evaluation; never used by core."""
import hashlib
import math
import time
import numpy as np
from scipy.stats import spearmanr
import core

ETA = np.diag([-1.,1.,1.])


def sprinkle(rho, seed):
    rng = np.random.default_rng(seed)
    size = rng.poisson(rho*core.VOLUME)
    # Exact uniform physical-volume sampling of |t|+r<1/2.
    halfwidth = .5*rng.random(size)**(1/3)
    t = (.5-halfwidth)*rng.choice([-1,1],size)
    radius = halfwidth*np.sqrt(rng.random(size)); angle = 2*np.pi*rng.random(size)
    coordinates = np.vstack(([-.5,0,0],np.column_stack((t,radius*np.cos(angle),radius*np.sin(angle))),[.5,0,0]))
    marks = np.random.default_rng(seed ^ 0x5A8D39).random(size+2)
    relation = np.zeros((size+2,size+2),bool)
    for start in range(0,size+2,128):
        delta = coordinates[None,:,:]-coordinates[start:start+128,None,:]
        relation[start:start+128] = (delta[:,:,0]>0)&(delta[:,:,0]**2>np.sum(delta[:,:,1:]**2,axis=2))
    return coordinates,relation,marks,0,size+1


def proper(delta, spacelike=False):
    square = -delta[...,0]**2+np.sum(delta[...,1:]**2,axis=-1)
    return np.sqrt(np.maximum(0,square if spacelike else -square))


def signature(g):
    eig = np.linalg.eigvalsh(g)
    threshold = 1e-10*max(1,np.max(np.abs(eig)))
    return bool(np.sum(eig < -threshold)==1 and np.sum(eig>threshold)==2)


def relative_error(g,target):
    return float(np.linalg.norm(g-target)/np.linalg.norm(target))


def boundary_witness(z,stencil):
    """Sample the ideal cap in the selected reference's rest frame, after inference.

    A positive result witnesses truncation. Zero is not a proof of full containment.
    """
    root = z[stencil['root']]; tm = stencil['tau_m']; bad=total=0
    for side,sgn in zip(stencil['sides'],[1,-1]):
        u = sgn*(z[side['reference']]-root)
        tau = proper(u)
        if tau<=0: return 1.
        u = u/tau; gamma=u[0]; velocity=u[1:]/gamma
        for chi in np.linspace(0,math.acosh(11/9),9):
            angles = np.arange(64)*2*np.pi/64
            spatial = tm*math.sinh(chi)*np.column_stack((np.cos(angles),np.sin(angles)))
            times = np.full(64,tm*math.cosh(chi))
            dot = spatial@velocity
            transformed_t = gamma*(times+dot)
            v2 = float(velocity@velocity)
            transformed_x = spatial+((gamma-1)*dot/max(v2,1e-30)+gamma*times)[:,None]*velocity
            points = root+sgn*np.column_stack((transformed_t,transformed_x))
            bad += np.sum(np.abs(points[:,0])+np.linalg.norm(points[:,1:],axis=1)>.5+1e-12)
            total += len(points)
    return float(bad/total)


def evaluate(g,z,stencil,rho,bottom,cfg):
    root=stencil['root']; result={'status':stencil['status']}
    if stencil['status']=='short_chain': return result
    middle=len(stencil['chain'])//2
    time_rows=[]
    for k in [-stencil['n'],-stencil['m'],stencil['m'],stencil['n']]:
        b=stencil['chain'][middle+k]; actual=float(proper(z[b]-z[root]))
        a,c=(b,root) if k<0 else (root,b)
        count=g.interval(a,c); estimate=cfg['alpha2']*rho**(-1/3)*abs(k)
        volume=(count/(rho*core.VOLUME))**(1/3)
        time_rows.append(dict(chain_edges=abs(k),actual=actual,estimate=estimate,volume_estimate=volume,
                              interval_count=count,alpha_volume=(count/core.VOLUME)**(1/3)/abs(k)))
    result['time']=time_rows
    result['time_relative_rmse']=float(np.sqrt(np.mean([(q['estimate']/q['actual']-1)**2 for q in time_rows])))
    errors=[]; ranks=[]; missing=total=ties=0; distance_rows=[]; cap_hits=cap_total=selected_total=0
    for side in stencil['sides']:
        true=[]; estimated=[]; rows=[]
        for b,estimate,info in zip(side['shell'],side['distances'],side['diagnostics']):
            if b==side['reference']: continue
            actual=float(proper(z[b]-z[side['reference']],True)); total+=1
            in_true_cap=actual<=cfg['radius_over_tau_m']*stencil['tau_m']
            is_selected=b in side['selected']
            cap_total+=int(in_true_cap); selected_total+=int(is_selected)
            cap_hits+=int(in_true_cap and is_selected)
            rows.append(dict(event=b,actual=actual,estimate=estimate,**info))
            if estimate is None: missing+=1; continue
            true.append(actual); estimated.append(estimate)
            errors.append((estimate/actual-1)**2)
        if len(true)>2 and np.std(estimated)>0:
            ranks.append(float(spearmanr(true,estimated).statistic))
        ties+=len(estimated)-len(set(estimated))
        distance_rows.append(rows)
    result.update(space_relative_rmse=float(np.sqrt(np.mean(errors))) if errors else None,
                  space_spearman=float(np.mean(ranks)) if ranks else None,
                  missing_distances=missing,total_distances=total,distance_ties=ties,
                  spatial_distances=distance_rows,populations=[len(s['selected']) for s in stencil['sides']],
                  true_cap_events=cap_total,true_cap_recovered=cap_hits,selected_nonreference=selected_total,
                  boundary_witness_fraction=boundary_witness(z,stencil))
    if stencil['status']!='ok': return result
    xyz=z-z[root]
    fields=[np.ones(len(z))]+[xyz[:,i] for i in range(3)]+[xyz[:,i]**2 for i in range(3)]
    fields += [xyz[:,i]*xyz[:,j] for i,j in [(0,1),(0,2),(1,2)]]
    fields += [np.exp((xyz[:,0]**2-np.sum(xyz[:,1:]**2,axis=1))*(-.5))]
    names=['constant','t','x','y','t2','x2','y2','tx','ty','xy','exp']
    target=np.array([0,0,0,0,-2,2,2,0,0,0,3.])
    response=np.array([core.apply(stencil,f) for f in fields])
    result['operator']={name:dict(value=float(v),target=float(t)) for name,v,t in zip(names,response,target)}
    result['operator_normalized_rmse']=float(np.sqrt(np.mean(((response[1:]-target[1:])/np.maximum(1,np.abs(target[1:])))**2)))
    oracle=core.metric(stencil,xyz)
    result['oracle_metric']=oracle.tolist()
    result['oracle_metric_error']=relative_error(oracle,ETA)
    result['oracle_signature']=signature(oracle)
    result['product_residual']=float(np.max(np.abs(oracle-core.metric_outer(stencil,xyz))))
    transform=np.array([[1.2,.2,-.1],[.1,.9,.3],[-.2,.15,1.1]])
    transformed=xyz@transform.T+np.array([.3,-.2,.1])
    mg=core.metric(stencil,transformed)
    result['affine_transform_residual']=float(np.max(np.abs(mg-transform@oracle@transform.T)))
    result['transformed_oracle_error']=relative_error(mg,transform@ETA@transform.T)
    # Nonlinear coordinate control; derivative is identity at the reference.
    curved_chart=xyz.copy(); curved_chart[:,1]+=.3*xyz[:,0]**2
    result['nonlinear_flat_chart_metric_error']=relative_error(core.metric(stencil,curved_chart),ETA)
    chart=core.intrinsic_chart(g,stencil,rho,bottom,cfg)
    result['chart']={'status':chart['status']}
    if chart['status']=='ok':
        anchors=z[chart['landmarks']]
        jacobian=(anchors[0]-anchors[1:])@ETA/stencil['tau_n']
        condition=float(np.linalg.cond(jacobian))
        target=jacobian@ETA@jacobian.T
        exact=xyz@jacobian.T
        measured=core.metric(stencil,chart['fields'])
        support=stencil['support']
        denom=np.linalg.norm(exact[support])
        result['chart']=dict(status='ok' if condition<=cfg['chart_max_condition'] else 'ill_conditioned_target',
                            landmarks=chart['landmarks'],jacobian=jacobian.tolist(),condition=condition,
                            metric=measured.tolist(),target=target.tolist(),
                            metric_error=relative_error(measured,target),signature=signature(measured),
                            field_error=float(np.linalg.norm(chart['fields'][support]-exact[support])/denom) if denom>0 else None,
                            smooth_field_metric_error=relative_error(core.metric(stencil,exact),target),
                            fields_on_support=chart['fields'][support].tolist(),
                            product_residual=float(np.max(np.abs(measured-core.metric_outer(stencil,chart['fields'])))))
    return result


def check_relabel(relation,marks,bottom,top,rho,cfg,original,original_chart,seed):
    permutation=np.random.default_rng(seed+917).permutation(len(marks))
    inverse=np.argsort(permutation)
    h=core.Poset(relation[np.ix_(permutation,permutation)],marks[permutation])
    s=core.neighborhood(h,rho,int(inverse[bottom]),int(inverse[top]),cfg)
    assert s['status']==original['status']
    assert [int(permutation[a]) for a in s['chain']]==original['chain']
    if 'sides' in original:
        for a,b in zip(s['sides'],original['sides']):
            assert [int(permutation[i]) for i in a['selected']]==b['selected']
            np.testing.assert_allclose([v or 0 for v in a['distances']],[v or 0 for v in b['distances']],rtol=1e-10,atol=1e-12)
            assert [v is None for v in a['distances']]==[v is None for v in b['distances']]
    if s['status']=='ok':
        np.testing.assert_allclose(s['weights'],original['weights'],rtol=1e-10,atol=1e-12)
        chart=core.intrinsic_chart(h,s,rho,int(inverse[bottom]),cfg)
        assert chart['status']==original_chart['status']
        if chart['status']=='ok':
            assert [int(permutation[i]) for i in chart['landmarks']]==original_chart['landmarks']
            np.testing.assert_allclose(chart['fields'][inverse],original_chart['fields'],rtol=1e-10,atol=1e-12)
    return True


def run_cloud(rho,seed,cfg,relabel=False):
    start=time.monotonic()
    z,relation,marks,bottom,top=sprinkle(rho,seed)
    g=core.Poset(relation,marks)
    s=core.neighborhood(g,rho,bottom,top,cfg)
    result=evaluate(g,z,s,rho,bottom,cfg)
    if relabel:
        chart=core.intrinsic_chart(g,s,rho,bottom,cfg) if s['status']=='ok' else None
        result['relabel_pass']=check_relabel(relation,marks,bottom,top,rho,cfg,s,chart,seed)
    return dict(rho=rho,seed=seed,poisson_count=len(z)-2,coordinates_sha256=hashlib.sha256(z.tobytes()).hexdigest(),
                relation_sha256=hashlib.sha256(relation.tobytes()).hexdigest(),marks_sha256=hashlib.sha256(marks.tobytes()).hexdigest(),
                seconds=time.monotonic()-start,stencil=s,evaluation=result)
