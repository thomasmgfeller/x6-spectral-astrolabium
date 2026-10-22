"""Retrospective, fixed-configuration intervention; original evidence is read-only.
SPDX-License-Identifier: Apache-2.0
"""
import collections
import datetime
from fractions import Fraction as F
import gzip
import hashlib
import itertools
import json
import platform
from pathlib import Path
import sys
import time

import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
SRC = HERE / 'source'
OUT = HERE / 'evidence'
sys.path.insert(0, str(SRC))
import inference as old

ETA = np.array([-1., 1., 1.])

def native(x):
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, np.generic): return x.item()
    raise TypeError(type(x).__name__)

def save(name, x):
    (OUT / name).write_text(json.dumps(x, default=native, indent=2, allow_nan=False) + '\n')

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def truth_order(p):
    d = p[None, :, :] - p[:, None, :]
    return (d[:, :, 0] > 0) & (d[:, :, 0]**2 > d[:, :, 1]**2+d[:, :, 2]**2)

def intervals(p):
    d=p[None,:,:]-p[:,None,:]
    return np.sum(d*d*ETA,axis=2)

def matrices(packet):
    """Independent coefficient assembly, indexed by exported local node order."""
    ids=packet['landmarks']+[packet['root']]+packet['support']
    lookup={a:i for i,a in enumerate(ids)}
    m=len(packet['pairs']);Q=np.zeros((len(ids),len(ids),m))
    for k,(a,b) in enumerate(packet['pairs']):
        i,j=lookup[a],lookup[b];Q[i,j,k]=Q[j,i,k]=1.
    H=np.array([[(Q[i,j]-Q[i,0]-Q[0,j])/2 for j in range(1,4)] for i in range(1,4)])
    Z=np.array([[(Q[i,x]-Q[0,x]-Q[i,4]+Q[0,4])/2 for i in range(1,4)] for x in range(len(ids))])
    groups=[]
    for a,b in packet['pairs']:
        i,j=lookup[a],lookup[b]
        groups.append('A' if i<4 and j<4 else 'R' if (i<4 and j==4) or (j<4 and i==4) else 'S' if i<4 or j<4 else 'unused')
    return H,Z,np.array(groups),ids

def reconstruct(q,packet,H,Z):
    h=H@q;z=Z@q
    eigen,u=np.linalg.eigh(h)
    if not eigen[0]<0<eigen[1]:return dict(status='SIGNATURE_FAIL',eigenvalues=eigen)
    if np.linalg.cond(h)>1e5:return dict(status='FRAME_CONDITION_FAIL',condition=float(np.linalg.cond(h)))
    coords=(z@u)/np.sqrt(abs(eigen))
    future=packet['support'].index(packet['temporal'][1])+5
    if coords[future,0]<0:coords[:,0]*=-1
    r=truth_order(coords);observed=np.asarray(packet['full_order'],bool)
    return dict(status='GEOMETRY_VALID',passed=bool(np.array_equal(r,observed)),
                missing=int(np.sum(observed&~r)),extra=int(np.sum(r&~observed)),
                condition=float(np.linalg.cond(h)),coordinates=coords,order=r,
                eigenvalues=eigen)

def summary_geometry(g): return {k:v for k,v in g.items() if k not in ('coordinates','order')}

def exact_rational_intervals(q,packet):
    """Independent exact rational inverse on the *binary64* input distances.
    This tests arithmetic signs, not exact Poisson-to-distance real arithmetic.
    """
    ids=packet['landmarks']+[packet['root']]+packet['support']
    lookup={tuple(sorted((a,b))):F(float(v)) for (a,b),v in zip(packet['pairs'],q)}
    def get(a,b):return F(0) if a==b else lookup[tuple(sorted((a,b)))]
    l=packet['landmarks'];root=packet['root']
    h=[[(get(l[i],l[j])-get(l[i],l[0])-get(l[0],l[j]))/2 for j in range(1,4)] for i in range(1,4)]
    a=[h[i]+[F(int(i==j)) for j in range(3)] for i in range(3)]
    for k in range(3):
        pivot=next(i for i in range(k,3) if a[i][k])
        a[k],a[pivot]=a[pivot],a[k];v=a[k][k];a[k]=[x/v for x in a[k]]
        for i in range(3):
            if i!=k:
                v=a[i][k];a[i]=[x-v*y for x,y in zip(a[i],a[k])]
    inv=[row[3:] for row in a]
    z=[[(get(l[i],x)-get(l[0],x)-get(l[i],root)+get(l[0],root))/2 for i in range(1,4)] for x in ids]
    out={}
    for i,j in itertools.combinations(range(len(ids)),2):
        d=[z[j][k]-z[i][k] for k in range(3)]
        val=sum(d[k]*inv[k][l]*d[l] for k in range(3) for l in range(3))
        out[(i,j)]=(int(val>0)-int(val<0),float(val))
    return out

def role(i):return 'landmark' if i<4 else 'root' if i==4 else 'support'

def diagnostic():
    start=time.monotonic();c=json.loads((SRC/'contract.json').read_text())
    manifest=0
    for line in (SRC/'SHA256SUMS.txt').read_text().splitlines():
        digest,name=line.split(maxsplit=1);name=name.lstrip('*')
        assert sha(SRC/name)==digest,name;manifest+=1
    for fname,prefix in [('freeze.json',SRC),('vendor_sources.json',SRC/'vendor')]:
        for name,digest in json.loads((SRC/fname).read_text())['files'].items():
            assert sha(prefix/name)==digest,name
    attempts=[];clouds=[];interventions=[];badpairs=[];replays=0;exact_sign_pairs=0
    masks=[''.join(x for bit,x in enumerate('ARS') if k&(1<<bit)) or 'none' for k in range(8)]
    for index in range(c['clouds']):
        path=SRC/f'results/cloud-{index:02d}.json.gz'
        row=json.loads(gzip.decompress(path.read_bytes()))
        attempts.append(dict(index=index,selection_status=row['selection']['status']))
        if not row['replicates']:continue
        truth=json.loads((SRC/f'results/truth/cloud-{index:02d}.json').read_text())
        assert truth['inference_sha256']==sha(path)
        packet=row['selection']['fourth']['packet'];p=np.array(truth['points'])
        H,Z,groups,ids=matrices(packet);assert ids==truth['ids']
        assert np.array_equal(truth_order(p),packet['full_order'])
        scale=packet['scale'];lookup={a:i for i,a in enumerate(ids)}
        exact=-intervals(p)/scale**2
        qtrue=np.array([exact[lookup[a],lookup[b]] for a,b in packet['pairs']])
        assert np.all(qtrue>0)
        B=(p[1:4]-p[0])/scale;X=(p-p[4])/scale
        np.testing.assert_allclose(H@qtrue,(B*ETA)@B.T,rtol=2e-12,atol=2e-12)
        np.testing.assert_allclose(Z@qtrue,(X*ETA)@B.T,rtol=2e-12,atol=2e-12)
        truegeo=reconstruct(qtrue,packet,H,Z);assert truegeo['passed']
        maxerr=float(np.max(abs(intervals(truegeo['coordinates'])-intervals(X))))
        assert maxerr<1e-8
        extents=2*(abs(p[:,0])+np.linalg.norm(p[:,1:],axis=1));assert np.max(extents)<c['duration']
        countmeans=c['count_density']*np.pi/12*(qtrue*scale**2)**1.5
        transformed=(countmeans/(c['count_density']*np.pi/12))**(2/3)/scale**2
        np.testing.assert_allclose(transformed,qtrue,rtol=2e-14,atol=2e-14)
        primary=row['replicates'][0];q0=np.array(primary['inference']['q'])
        anchor_errors=np.array([abs(v-t)/t for v,t,g in zip(q0,qtrue,groups) if g=='A'])
        cloud=dict(index=index,seed=row['seed'],nodes=len(p),support=len(packet['support']),pairs=len(qtrue),
                   exact_frame_condition=truegeo['condition'],original_frame_condition=primary['inference']['four'].get('landmark_condition'),
                   exact_pair_interval_max_abs_error=maxerr,maximum_diamond_extent=float(max(extents)),
                   minimum_diamond_slack=float((c['duration']-max(extents))/2),
                   expected_count_min=float(min(countmeans)),anchor_max_relative_q_error=float(max(anchor_errors)),
                   count_standardized_error_mean=float(np.mean((np.array(primary['observed']['counts'])-countmeans)/np.sqrt(countmeans))))
        clouds.append(cloud)
        for rep in row['replicates']:
            obs=rep['observed'];q=np.array(rep['inference']['q'])
            replay=old.measurement(packet,obs['counts'],obs['overlaps'],c['count_density'],c['minimum_measurement_count'])
            np.testing.assert_array_equal(replay['q'],q)
            for arm in ['four','baseline']:
                saved=rep['inference'][arm];out=replay[arm];assert saved['status']==out['status']
                if out['status']=='WEIGHTS_VALID':
                    assert out['order']==saved['order']
                    np.testing.assert_allclose(out['weights'],saved['weights'],rtol=1e-10,atol=1e-9)
            replays+=1
            for label in masks:
                replaced=np.isin(groups,list(label)) if label!='none' else np.zeros(len(q),bool)
                qi=np.where(replaced,qtrue,q)
                hg,zg,_,_=old.four_geometry(qi,packet)
                np.testing.assert_allclose(hg,H@qi,rtol=1e-12,atol=1e-12)
                np.testing.assert_allclose(zg,Z@qi,rtol=1e-12,atol=1e-12)
                geo=reconstruct(qi,packet,H,Z)
                try:
                    f=old.four(qi,packet)
                    full=dict(status=f['status'],qualified=f['qualified'],order=f['order'])
                except (ValueError,np.linalg.LinAlgError) as exc:full=dict(status='UNRESOLVED',reason=str(exc))
                interventions.append(dict(index=index,replicate=rep['replicate'],replace=label,
                                          geometry=summary_geometry(geo),solve=full))
                if label=='none' and replay['four']['status']=='WEIGHTS_VALID':
                    assert geo['passed']==replay['four']['qualified']
                    assert (geo['missing'],geo['extra'])==(replay['four']['order']['missing'],replay['four']['order']['extra'])
                if label=='ARS':assert geo['passed']
            if rep['replicate']!=0 or replay['four']['status']!='WEIGHTS_VALID':continue
            geo=reconstruct(q,packet,H,Z);h=H@q;z=Z@q;hi=np.linalg.inv(h)
            rational=exact_rational_intervals(q,packet)
            sr=intervals(geo['coordinates']);st=intervals(X);counts=np.array(obs['counts'])
            der=(2/3)*q/counts;cov=np.array(obs['overlaps'])*der[:,None]*der[None,:]
            for (i,j),(sgn,val) in rational.items():
                assert np.sign(sr[i,j])==sgn,(index,i,j,sr[i,j],sgn)
                exact_sign_pairs+=1
                observed=np.array(packet['full_order'],bool);r=geo['order']
                if r[i,j]==observed[i,j] and r[j,i]==observed[j,i]:continue
                v=z[j]-z[i];w=hi@v
                jac=2*w@(Z[j]-Z[i])-np.einsum('i,ijm,j->m',w,H,w)
                var=max(0.,float(jac@cov@jac));diag=float(np.sum(jac**2*np.diag(cov)))
                delta=X[j]-X[i];nullness=abs(st[i,j])/float(delta@delta)
                pair=dict(index=index,i=i,j=j,node_i=ids[i],node_j=ids[j],roles=role(i)+'-'+role(j),
                          true_order=[bool(observed[i,j]),bool(observed[j,i])],estimated_order=[bool(r[i,j]),bool(r[j,i])],
                          true_s2=float(st[i,j]),estimated_s2=float(sr[i,j]),exact_binary_input_s2=val,
                          physical_true_s2=float(st[i,j]*scale**2),physical_estimated_s2=float(sr[i,j]*scale**2),
                          lightcone_relative_margin=float(nullness),true_dt=float(delta[0]),
                          estimated_dt=float(geo['coordinates'][j,0]-geo['coordinates'][i,0]),
                          full_delta_sd=float(np.sqrt(var)),diagonal_delta_sd=float(np.sqrt(diag)),
                          true_margin_over_full_sd=float(abs(st[i,j])/np.sqrt(var)) if var>0 else None,
                          sign_flip=bool(np.sign(st[i,j])!=np.sign(sr[i,j])),
                          measured_pair=tuple(sorted((ids[i],ids[j]))) in {tuple(x) for x in packet['pairs']})
                badpairs.append(pair)
        print(json.dumps(dict(stage='archive',index=index,exact_geometry=truegeo['passed'])),flush=True)
    def aggregate(reps):
        out={}
        for label in masks:
            a=[x for x in interventions if x['replace']==label and x['replicate'] in reps]
            out[label]=dict(attempts=len(a),geometry_valid=sum(x['geometry']['status']=='GEOMETRY_VALID' for x in a),
                geometry_order_pass=sum(x['geometry'].get('passed',False) for x in a),
                total_missing=sum(x['geometry'].get('missing',0) for x in a),total_extra=sum(x['geometry'].get('extra',0) for x in a),
                full_solve_valid=sum(x['solve']['status']=='WEIGHTS_VALID' for x in a),
                full_solve_order_pass=sum(x['solve'].get('qualified',False) for x in a),
                unavailable_reasons=dict(collections.Counter(x['solve'].get('reason','') for x in a if x['solve']['status']!='WEIGHTS_VALID')))
        return out
    summary=dict(status='DIAGNOSIS_COMPLETED_NO_QUALIFICATION',scheduled_original_attempts=len(attempts),
        selection_statuses=dict(collections.Counter(x['selection_status'] for x in attempts)),
        selected_configurations=len(clouds),manifest_entries_verified=manifest,replayed_count_clouds=replays,
        exact_geometry_order_pass=len(clouds),exact_pair_interval_max_abs_error=max(x['exact_pair_interval_max_abs_error'] for x in clouds),
        interval_signs_checked_exact_rational=exact_sign_pairs,primary=aggregate([0]),all_replicates=aggregate(range(9)),
        primary_mismatched_unordered_pairs=len(badpairs),mismatch_roles=dict(collections.Counter(x['roles'] for x in badpairs)),
        mismatch_sign_flips=sum(x['sign_flip'] for x in badpairs),mismatches_measured_directly=sum(x['measured_pair'] for x in badpairs),
        mismatch_lightcone_margin_quantiles=np.quantile([x['lightcone_relative_margin'] for x in badpairs],[0,.25,.5,.75,1]),
        mismatch_true_margin_over_full_sd_quantiles=np.quantile([x['true_margin_over_full_sd'] for x in badpairs],[0,.25,.5,.75,1]),
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),seconds=time.monotonic()-start)
    save('attempts.json',attempts);save('clouds.json',clouds);save('interventions.json',interventions)
    save('violated_pairs.json',badpairs);save('summary.json',summary)
    print(json.dumps(summary,default=native,indent=2))

if __name__=='__main__':diagnostic()
