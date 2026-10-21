"""Inference from order, marks, density and auxiliary colours only.

No simulator, coordinate evaluator or validation-field import is permitted.
The mathematical flat 2+1 model is an explicit assumption, not inferred here.
"""
import itertools
import math
import numpy as np

ETA=np.diag([-1.,1.,1.])
TARGET=np.array([0.,0.,0.,-2.,2.,2.,0.,0.,0.])
VOLUME=math.pi/12

def design(z):
    z=np.asarray(z,float)
    return np.array([*z.T,*(z*z).T,*[np.sqrt(2)*z[:,i]*z[:,j] for i,j in [(0,1),(0,2),(1,2)]]])

def normalize(h,maximum):
    ev,u=np.linalg.eigh(h)
    if not (ev[0]<0 and ev[1]>0 and ev[2]>0):return None
    condition=float(np.max(np.abs(ev))/np.min(np.abs(ev)))
    if not np.isfinite(condition) or condition>maximum:return None
    return (u/np.sqrt(np.abs(ev))[None,:]).T,ev,condition

def gram_and_vectors(q,landmarks,root,support,tm):
    qr=np.array([q(a,root) for a in landmarks]);qb=np.array([q(root,b) for b in support])
    h=np.array([[(-qr[i]-qr[j]+(0. if i==j else q(a,b)))/(2*tm**2)
                 for j,b in enumerate(landmarks)] for i,a in enumerate(landmarks)])
    v=np.array([[(-qr[i]-qb[j]+q(a,b))/(2*tm**2) for j,b in enumerate(support)] for i,a in enumerate(landmarks)])
    return h,v

def noise_guard(h,v,t,half_data,counts,half_counts,condition,c):
    rows=[]
    for hh,vh in half_data:
        ev=np.linalg.eigvalsh(hh)
        rows.append(dict(lorentz_signature=bool(ev[0]<0<ev[1]),
            gram_error=float(np.linalg.norm(t@hh@t.T-ETA)/np.sqrt(3)),
            feature_error=float(np.linalg.norm(t@(vh-v))/max(np.linalg.norm(t@v),1e-12))))
    checks=dict(condition=condition<=c['guard_max_condition'],
                interval_count=min(counts)>=c['guard_min_interval'],
                half_interval_count=min(min(x) for x in half_counts)>=c['guard_min_half_interval'],
                half_signature=all(x['lorentz_signature'] for x in rows),
                gram_stability=all(x['gram_error']<=c['guard_max_gram_error'] for x in rows),
                feature_stability=all(x['feature_error']<=c['guard_max_feature_error'] for x in rows))
    return dict(passed=all(checks.values()),checks=checks,halves=rows,
                reasons=[k for k,v in checks.items() if not v])

def frame(g,s,rho,boundary,colours,c):
    if s['status']!='ok':return dict(status='unavailable_stencil')
    root=s['root'];support=s['support'];points=[root]+support;tm=s['tau_m']
    colours=np.asarray(colours,dtype=np.uint8)
    if len(colours)!=g.size or np.any(colours>1):raise ValueError('binary event colours required')
    bits=[int.from_bytes(np.packbits(colours==i,bitorder='little').tobytes(),'little') for i in [0,1]]
    cache={}
    def counted(a,b):
        if a==b:return (0,0,0)
        if g.r[b,a]:a,b=b,a
        if not g.r[a,b]:raise ValueError('noncausal interval')
        key=(int(a),int(b))
        if key not in cache:
            interval=g.succ[a]&g.pred[b]
            cache[key]=(interval.bit_count(),(interval&bits[0]).bit_count(),(interval&bits[1]).bit_count())
        return cache[key]
    def q(a,b):return (counted(a,b)[0]/(rho*VOLUME))**(2/3)
    candidate_counts=[];eligible_triples=0;best=None
    for direction,cones in [('past',g.pred),('future',g.succ)]:
        common=(1<<g.size)-1
        for b in points:common&=cones[b]
        candidates=[]
        while common:
            low=common&-common;a=low.bit_length()-1;common^=low
            if a not in boundary and min(counted(a,b)[0] for b in points)>=c['landmark_min_interval']:candidates.append(a)
        candidates.sort(key=lambda a:g.marks[a]);candidates=candidates[:c['landmark_candidates_per_side']]
        candidate_counts.append(dict(side=direction,count=len(candidates)))
        qr={a:q(a,root) for a in candidates};pairs={}
        for a,b in itertools.combinations(candidates,2):
            if (g.r[a,b] or g.r[b,a]) and counted(a,b)[0]>=c['landmark_min_interval']:pairs[(a,b)]=q(a,b)
        for triple in itertools.combinations(candidates,3):
            if any((a,b) not in pairs for a,b in itertools.combinations(triple,2)):continue
            eligible_triples+=1
            h=np.diag([-qr[a]/tm**2 for a in triple])
            for i,j in [(0,1),(0,2),(1,2)]:
                a,b=triple[i],triple[j];h[i,j]=h[j,i]=(-qr[a]-qr[b]+pairs[(a,b)])/(2*tm**2)
            normalized=normalize(h,c['raw_max_condition'])
            if normalized is None:continue
            score=float(abs(np.linalg.det(h))/np.prod(-np.diag(h)))
            key=(score,tuple(-float(g.marks[a]) for a in triple))
            if best is None or key>best[0]:best=(key,triple,direction,normalized)
    if best is None:return dict(status='no_admissible_frame',candidates=candidate_counts,eligible_triples=eligible_triples)
    key,landmarks,direction,(t,ev,condition)=best
    h,v=gram_and_vectors(q,landmarks,root,support,tm);z=(t@v).T
    used=set()
    for a in landmarks:
        used.add(tuple(sorted((a,root))))
        for b in support:used.add(tuple(sorted((a,b))))
    used.update(tuple(sorted((root,b))) for b in support)
    used.update(tuple(sorted(pair)) for pair in itertools.combinations(landmarks,2))
    ordered=sorted(used,key=lambda p:tuple(sorted(float(g.marks[a]) for a in p)))
    counts=[counted(a,b)[0] for a,b in ordered]
    half_counts=[[counted(a,b)[i+1] for a,b in ordered] for i in [0,1]]
    halves=[]
    for i in [0,1]:
        qh=lambda a,b:(2*counted(a,b)[i+1]/(rho*VOLUME))**(2/3)
        halves.append(gram_and_vectors(qh,landmarks,root,support,tm))
    guard=noise_guard(h,v,t,halves,counts,half_counts,condition,c)
    return dict(status='ok',landmarks=list(landmarks),side=direction,score=key[0],
                candidates=candidate_counts,eligible_triples=eligible_triples,gram=h,vectors=v,transform=t,
                eigenvalues=ev,condition=condition,features=z,feature_gram=z@z.T,
                lorentz_feature_gram=z@ETA@z.T,interval_pairs=ordered,interval_counts=counts,
                half_interval_counts=half_counts,half_grams=[a for a,b in halves],
                half_vectors=[b for a,b in halves],guard=guard)

def project(a,cap):
    a=np.asarray(a,float);positive=np.maximum(a,0.)
    if positive.sum()<=cap:return positive
    u=np.sort(a)[::-1];s=np.cumsum(u);j=np.arange(1,len(a)+1)
    index=np.flatnonzero(u-(s-cap)/j>0)[-1]
    return np.maximum(a-(s[index]-cap)/(index+1),0.)

def qp_certificate(d,b,a0,ridge,cap,a,c):
    d=np.asarray(d,float);b=np.asarray(b,float);a0=np.asarray(a0,float);a=np.asarray(a,float)
    assert np.isfinite(a).all() and ridge>0 and cap>0
    assert min(a)>=-c['solver_feasibility_tolerance']
    assert float(a.sum())<=cap+c['solver_feasibility_tolerance']*(1+cap)
    residual=d@a-b;delta=a-a0
    objective=float((residual@residual+ridge*(delta@delta))/2)
    grad=d.T@residual+ridge*delta
    gap=float(grad@a-cap*min(0.,float(grad.min())))
    assert gap>=-1e-8*(1+objective)
    assert gap<=c['solver_gap_tolerance']*(1+abs(objective))
    return dict(objective=objective,gap=gap,residual_norm=float(np.linalg.norm(residual)),
                coefficient_sum=float(a.sum()),minimum_coefficient=float(a.min()))

def quadratic(d,b,a0,ridge,cap,c):
    d=np.asarray(d,float);b=np.asarray(b,float);a0=np.asarray(a0,float)
    h=d.T@d+ridge*np.eye(len(a0));linear=-d.T@b-ridge*a0
    lipschitz=float(np.linalg.eigvalsh(h)[-1]);momentum=(math.sqrt(lipschitz)-math.sqrt(ridge))/(math.sqrt(lipschitz)+math.sqrt(ridge))
    a=project(a0,cap);y=a.copy();best=a.copy();best_value=float('inf');cert=None
    for iteration in range(1,c['solver_max_iterations']+1):
        previous=a;a=project(y-(h@y+linear)/lipschitz,cap);y=a+momentum*(a-previous)
        if iteration%10==0 or iteration==c['solver_max_iterations']:
            residual=d@a-b;delta=a-a0;value=float((residual@residual+ridge*(delta@delta))/2)
            if value<best_value:best=a.copy();best_value=value
            try:cert=qp_certificate(d,b,a0,ridge,cap,a,c)
            except AssertionError:continue
            break
    if cert is None:return dict(status='UNRESOLVED',iterations=iteration,coefficients=best)
    return dict(status='VERIFIED',iterations=iteration,coefficients=a,certificate=cert)

def calibrate(z,a0,temporal,c):
    d=design(z);a0=np.asarray(a0,float);mask=np.asarray(temporal,bool)
    assert mask.sum()==2 and np.all(a0[mask]<0) and np.all(a0[~mask]>=0)
    ds=d[:,~mask];b=TARGET-d[:,mask]@a0[mask]
    ridge=c['ridge_relative']*max(c['ridge_floor'],float(np.sum(ds*ds)/ds.shape[1]))
    cap=c['maximum_mass_ratio']*float(np.abs(a0).sum())-float(np.abs(a0[mask]).sum())
    solved=quadratic(ds,b,a0[~mask],ridge,cap,c)
    out=dict(design=d,baseline=a0,temporal_mask=mask,ridge=ridge,cap=cap,**solved)
    if solved['status']=='VERIFIED':
        a=a0.copy();a[~mask]=solved['coefficients'];mass=float(np.abs(a).sum())
        out.update(weights=a,mass=mass,mass_ratio=mass/float(np.abs(a0).sum()),
                   fitted_residual_norm=float(np.linalg.norm(d@a-TARGET)))
        validate_calibration(out,c)
    return out

def validate_calibration(row,c):
    if row['status']!='VERIFIED':return False
    d=np.array(row['design']);a0=np.array(row['baseline']);mask=np.array(row['temporal_mask'],bool);a=np.array(row['weights'])
    np.testing.assert_allclose(a[mask],a0[mask],atol=0,rtol=0)
    np.testing.assert_allclose(a[~mask],row['coefficients'],atol=0,rtol=0)
    expected_ridge=c['ridge_relative']*max(c['ridge_floor'],float(np.sum(d[:,~mask]**2)/(~mask).sum()))
    expected_cap=c['maximum_mass_ratio']*np.abs(a0).sum()-np.abs(a0[mask]).sum()
    np.testing.assert_allclose([row['ridge'],row['cap']],[expected_ridge,expected_cap],atol=1e-12,rtol=1e-12)
    cert=qp_certificate(d[:,~mask],TARGET-d[:,mask]@a0[mask],a0[~mask],row['ridge'],row['cap'],a[~mask],c)
    for k,v in cert.items():np.testing.assert_allclose(v,row['certificate'][k],atol=1e-10,rtol=1e-9)
    mass=float(np.abs(a).sum());assert mass<=c['maximum_mass_ratio']*np.abs(a0).sum()+1e-8
    np.testing.assert_allclose([mass,mass/np.abs(a0).sum(),np.linalg.norm(d@a-TARGET)],
        [row['mass'],row['mass_ratio'],row['fitted_residual_norm']],atol=1e-10,rtol=1e-9)
    return True

def infer(g,s,rho,boundary,colours,c):
    f=frame(g,s,rho,boundary,colours,c);out=dict(frame=f)
    if s['status']!='ok':return out
    a0=np.asarray(s['weights'])*s['tau_m']**2;mask=[b in s['temporal'] for b in s['support']]
    calibration=calibrate(f['features'],a0,mask,c) if f['status']=='ok' else None
    raw=calibration is not None and calibration['status']=='VERIFIED'
    guarded=raw and f['guard']['passed'];out['calibration']=calibration
    for name,adopted in [('intrinsic_raw',raw),('intrinsic_guarded',guarded)]:
        reason=[] if adopted else ([f['status']] if f['status']!='ok' else
            ['unresolved_calibration'] if not raw else f['guard']['reasons'])
        out[name]=dict(adopted=bool(adopted),fallback_reasons=reason,
            weights=np.asarray(calibration['weights'])/s['tau_m']**2 if adopted else np.asarray(s['weights']))
    return out
