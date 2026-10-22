"""Post-freeze independent algebra/inventory/replay audit; no gate changes.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import json
import math
import numpy as np
from eb_common import HERE,SOURCE,read,save,encode,frozen

def compare_legacy(actual, expected):
    """Exact selection replay, except two recomputed condition diagnostics."""
    actual=json.loads(encode(actual)); expected=json.loads(encode(expected))
    for key in ['landmark_condition','design_condition']:
        if key not in expected:continue
        a=actual.pop(key); b=expected.pop(key)
        assert type(a) is type(b) is float,(key,a,b)
        assert math.isfinite(a) and math.isfinite(b),(key,a,b)
        assert math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12),(key,a,b)
        if a!=b:print('Legacy condition replay:',key,repr(a),repr(b))
    assert encode(actual)==encode(expected),'legacy selection payload changed'

def gram_vectors(q,p):
    lookup={tuple(pair):float(v) for pair,v in zip(p['pairs'],q)}
    def d(a,b):return 0. if a==b else lookup[tuple(sorted((a,b)))]
    anchors=p['landmarks']; root=p['root']; nodes=anchors+[root]+p['support']
    h=np.array([[(d(a,b)-d(a,anchors[0])-d(anchors[0],b))/2 for b in anchors[1:]] for a in anchors[1:]])
    z=np.array([[(d(a,b)-d(anchors[0],b)-d(a,root)+d(anchors[0],root))/2 for a in anchors[1:]] for b in nodes])
    return h,z

def monomials(z):
    t,x,y=np.asarray(z).T
    return np.array([t,x,y,t*t,x*x,y*y,t*x,t*y,x*y])

def main(write=True):
    frozen(); c=read(HERE/'contract.json'); totals=dict(A=0,B=0,arm_records=0,valid_weights=0,accepted_frames=0,candidates=0)
    maxima=dict(moment=0.,weight_relative=0.,covariance_relative=0.,order_mismatches=0)
    Ahash=set(); Bhash=set(); historical_A=set(); historical_B=set()
    for package in ['four_landmark_count_covariance/evidence','causal_count_fit']:
        for path in (HERE.parent/package/'results').glob('cloud-*.json.gz'):
            rr=read(path); historical_A.add(rr['selection']['coordinates_sha256'])
            for rep in rr['replicates']:historical_B.add(rep['observed']['coordinates_sha256'])
    for path in (HERE.parent/'stability_followup/conditional').glob('cloud-*.json.gz'):
        for rep in read(path)['replicates']: historical_B.add(rep['observed']['coordinates_sha256'])
    for index in range(c['clouds']):
        path=HERE/f'results/cloud-{index:02d}.json.gz'; r=read(path); s=r['selection']
        assert r['seed']==c['selection_seed_base']+index
        assert hashlib.sha256(encode(s)).hexdigest()==r['selection_seal']
        assert s['coordinates_sha256'] not in historical_A
        Ahash.add(s['coordinates_sha256']); totals['A']+=1
        old,new=s['arms']['legacy'],s['arms']['candidate']; inv=new.get('inventory',[])
        totals['candidates']+=len(inv); assert len({v['candidate'] for v in inv})==len(inv)
        for side in ['past','future']:
            rows=[v for v in inv if v['side']==side]
            assert [v['raw_rank'] for v in rows]==list(range(len(rows)))
            eligible=[v for v in rows if v['status']=='COUNT_ELIGIBLE']
            for rank,v in enumerate(eligible):
                assert v['eligible_rank']==rank
                assert v['within_geometry_cap']==(rank<c['selection']['candidate_cap_per_side'])
                n=np.array(v['endpoint_counts']); assert np.all(n[:,0]>=16) and np.all(n[:,1:]>=4)
                assert np.array_equal(n[:,0],n[:,1:].sum(axis=1))
                if v['in_old_cap']:assert v['within_geometry_cap']
            for v in rows:assert v['in_old_cap']==(v['raw_rank']<c['selection']['candidate_cap_per_side'])
        for v in inv:
            if v.get('geometry_status')!='ELIGIBLE':continue
            p=v['packet']; ns=np.array(v['pair_counts']); assert np.array_equal(ns[:,0],ns[:,1:].sum(axis=1))
            q=(ns[:,0]/(c['selection_density']*np.pi/12))**(2/3)/p['scale']**2
            h,z=gram_vectors(q,p); ev=np.linalg.eigvalsh(h); condition=float(np.linalg.cond(h)); D=monomials(z[5:])
            assert ev[0]<0<ev[1] and condition<=c['selection']['maximum_landmark_condition']
            assert np.linalg.matrix_rank(D)==9 and np.linalg.cond(D)<=c['selection']['maximum_design_condition']
            assert np.isclose(condition,v['landmark_condition'],rtol=1e-9,atol=1e-9)
            totals['accepted_frames']+=1
        if old['status']=='SELECTED':
            assert new['status']=='SELECTED'
            assert any(v['candidate']==old['packet']['landmarks'][3] and v.get('geometry_status')=='ELIGIBLE' for v in inv)
            assert new['landmark_condition']<=old['landmark_condition']*(1+1e-12)
        if new['status']=='SELECTED':
            choice=next(v for v in inv if v['candidate']==new['packet']['landmarks'][3])
            assert choice['geometry_status']=='ELIGIBLE'
            assert all(new['landmark_condition']<=v['landmark_condition']*(1+1e-12) for v in inv if v.get('geometry_status')=='ELIGIBLE')
        if not r['replicates']:continue
        tr=read(HERE/f'results/truth/cloud-{index:02d}.json'); assert tr['inference_sha256']==hashlib.sha256(path.read_bytes()).hexdigest()
        for rr in r['replicates']:
            hashes={v['observed']['coordinates_sha256'] for v in rr['arms'].values()}; assert len(hashes)==1
            b=hashes.pop(); assert b not in historical_B and b not in Bhash; Bhash.add(b); totals['B']+=1
            for arm,rrr in rr['arms'].items():
                totals['arm_records']+=1; p=s['arms'][arm]['packet']; obs=rrr['observed']; m=rrr['measurement']; f=m['four']
                C=np.array(obs['overlaps'],float); n=np.array(obs['counts']); assert np.array_equal(C,C.T) and np.array_equal(C.diagonal(),n)
                assert np.linalg.eigvalsh(C)[0]>=-1e-8 and all(obs['intersection_replay'])
                if f['status']!='WEIGHTS_VALID':continue
                totals['valid_weights']+=1; w=np.array(f['weights']); z=np.array(f['coordinates']); scale=p['scale']
                D=monomials(z[5:]-z[4]); target=np.array([0,0,0,-2,2,2,0,0,0.])
                residual=float(np.max(abs(D@(w[1:]*scale**2)-target))); maxima['moment']=max(maxima['moment'],residual); assert residual<1e-6
                H=np.eye(D.shape[1])+np.ones((D.shape[1],D.shape[1])); Q=np.linalg.solve(H,D.T)
                a=Q@np.linalg.solve(D@Q,target); direct=np.r_[-a.sum(),a]/scale**2
                error=float(np.max(abs(direct-w)/(1+abs(w)))); maxima['weight_relative']=max(maxima['weight_relative'],error); assert error<1e-5
                delta=z[None]-z[:,None]; order=(delta[:,:,0]>0)&(delta[:,:,0]**2>delta[:,:,1]**2+delta[:,:,2]**2)
                observed=np.array(p['full_order'],bool); mismatch=int(np.sum(order!=observed))
                assert f['qualified']==bool(mismatch==0) and mismatch==f['order']['missing']+f['order']['extra']
                maxima['order_mismatches']=max(maxima['order_mismatches'],mismatch)
                q=(n/(c['count_density']*np.pi/12))**(2/3)/scale**2; derivative=np.zeros(len(n)); mask=n>0; derivative[mask]=(2/3)*q[mask]/n[mask]
                J=np.array(f['weight_jacobian']); cov=J@(C*derivative[:,None]*derivative[None,:])@J.T
                stored=np.array(f['weight_covariance']); error=float(np.max(abs(cov-stored))/(1+np.max(abs(stored))))
                maxima['covariance_relative']=max(maxima['covariance_relative'],error); assert error<1e-10
                assert np.max(abs(w.sum()))<1e-7
    assert len(Ahash)==32
    # Independent legacy simulation path validates copied A construction and old selection.
    from replay_coordinates import selection_cloud,counting_cloud
    replays=[]
    for index in [0,c['clouds']-1]:
        r=read(HERE/f'results/cloud-{index:02d}.json.gz'); s=r['selection']; original,_=selection_cloud(r['seed'],c,s['coordinates_sha256'])
        compare_legacy(original['fourth'],s['arms']['legacy'])
        for key in ['base_audit','physical_count','coordinates_sha256','relation_sha256','baseline_selected','base_selection_funnel']:
            assert encode(original[key])==encode(s[key]),key
        trpath=HERE/f'results/truth/cloud-{index:02d}.json'
        if trpath.exists():
            tr=read(trpath)
            for arm,pp in tr['arms'].items():
                pp={**pp,'points':np.array(pp['points'])}; p=s['arms'][arm]['packet']
                obs=counting_cloud(pp,p,r['seed'],0,c,r['replicates'][0]['arms'][arm]['observed']['coordinates_sha256'])
                assert encode(obs)==encode(r['replicates'][0]['arms'][arm]['observed'])
        replays.append(index)
    out=dict(status='PASS',totals=totals,maxima=maxima,legacy_A_and_paired_B0_replays=replays,
        unique_A_hashes=len(Ahash),unique_B_hashes=len(Bhash),prior_A_hashes_excluded=len(historical_A),prior_B_hashes_excluded=len(historical_B),
        scope='Internal post-freeze algebra, inventory and replay audit; no external replication, full floating-point proof or uncertainty-coverage guarantee.')
    if write:
        save(HERE/'verification.json',out)
    else:
        published=read(HERE/'verification.json')
        assert published['status']=='PASS' and published['totals']==out['totals']
        for key in ['legacy_A_and_paired_B0_replays','unique_A_hashes','unique_B_hashes','prior_A_hashes_excluded','prior_B_hashes_excluded']:
            assert published[key]==out[key],key
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
