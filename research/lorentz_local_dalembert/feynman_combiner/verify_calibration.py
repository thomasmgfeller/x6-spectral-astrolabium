"""Verify archived certificates and independently regenerate evaluation fields.
Does not repeat the expensive full frame search; that limit is explicit.
"""
import hashlib,json,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'moment_feasibility'))
from feasibility import checked_feasible,checked_infeasible,design
from variance_weights import certify
from fusion import causal_check
from run_calibration import coordinates_only,config,digest


def main():
    c=json.loads((HERE/'calibration_contract.json').read_text())
    lpcontract=json.loads((HERE.parent/'moment_feasibility/contract.json').read_text())
    _,oc,_,_=config();checked=0;lpcount=0;qpcount=0;intervals=0;complete=0;causal_rows=[]
    for split in ['calibration','test']:
        folder=HERE/('independent_'+split);execution=json.loads((folder/'execution.json').read_text())
        assert execution['status']=='COMPLETE'
        assert len(execution['records'])==32
        for path,expected in execution['source_sha256'].items():
            assert hashlib.sha256((HERE.parents[2]/path).read_bytes()).hexdigest()==expected,path
        for item in execution['records']:
            raw=(folder/item['file']).read_bytes();assert hashlib.sha256(raw).hexdigest()==item['sha256']
            row=json.loads(raw);checked+=1
            z=coordinates_only(row['rho'],row['seed'],oc)
            assert digest(z)==row['coordinates_sha256']
            o=row['operator'];w=row['selection']['selected']
            if w is None:
                assert o['status']=='NO_GUARDED_SUPPORT';continue
            # All counted intervals must be causal according to simulator geometry.
            for a,b in w['certificate']['interval_pairs']:
                dz=z[a]-z[b];assert dz[0]**2>dz[1:]@dz[1:];intervals+=1
            # Supplemental diagnostic, not a retroactively added primary gate.
            ids=[w['root']]+w['support'];actual=z[ids]
            dt=actual[None,:,0]-actual[:,None,0]
            dx=actual[None,:,1:]-actual[:,None,1:]
            rel=(dt>0)&(dt*dt>np.sum(dx*dx,axis=2))
            reconstructed=np.vstack((np.zeros(3),w['certificate']['features']))
            future_index=ids.index(w['temporal'][1])
            if reconstructed[future_index,0]<0:reconstructed[:,0]*=-1
            causal_rows.append(dict(split=split,seed=row['seed'],ordered_pairs_evaluated=len(ids)*(len(ids)-1),true_relations=int(rel.sum()),**causal_check(reconstructed,rel)))
            if o['status']!='COMPLETE':continue
            complete+=1;d=design(np.array(w['certificate']['features'])/w['scale'])
            np.testing.assert_allclose(d,o['design'],atol=1e-12,rtol=1e-12)
            for policy,name in [('unrestricted','lp'),('free_time','signed_lp')]:
                v=o[name]
                if v['status']=='FEASIBLE':
                    a,_=checked_feasible(d,o['baseline'],o['temporal_mask'],policy,v['primal'],v['dual'],lpcontract)
                    np.testing.assert_allclose(a,v['weights']);lpcount+=1
                elif v['status']=='INFEASIBLE':
                    checked_infeasible(d,o['baseline'],o['temporal_mask'],policy,v['separating_dual'],lpcontract);lpcount+=1
                else:raise AssertionError('unresolved LP')
            for name,sign in [('qp',None),('signed_qp',np.where(o['temporal_mask'],-1.,1.))]:
                v=o[name]
                if v is None:continue
                if v['status']=='VERIFIED':assert certify(d,v['weights'],sign,v['dual'])['passed'];qpcount+=1
            weights=np.array(o['weights']);np.testing.assert_allclose(weights[0],o['baseline']);np.testing.assert_allclose(weights[1],o['lp']['weights']);np.testing.assert_allclose(weights[2],o['qp']['weights'])
            assert hashlib.sha256(weights.tobytes()).hexdigest()==o['weights_seal']
            delta=z[w['support']]-z[w['root']]
            field=np.exp(delta[:,0]/2)*np.cos(delta[:,1]/2)*np.cos(delta[:,2]/2)
            noise=np.random.default_rng(np.random.SeedSequence([row['seed'],823731])).normal(scale=c['field_noise_sigma'],size=len(field)+1)
            scale=w['scale']**2
            np.testing.assert_allclose(weights@(field-1)/scale,o['clean'],atol=1e-10,rtol=1e-10)
            np.testing.assert_allclose(weights@(field-1+noise[1:]-noise[0])/scale,o['observed'],atol=1e-10,rtol=1e-10)
            full=np.column_stack((-weights.sum(axis=1),weights))/scale
            np.testing.assert_allclose(c['field_noise_sigma']**2*full@full.T,o['conditional_field_covariance'],atol=1e-10,rtol=1e-10)
    result=dict(status='PASS_CERTIFICATES_AND_FIELD_REPLAY',clouds=checked,complete=complete,lp_certificates=lpcount,qp_certificates=qpcount,
                causal_intervals=intervals,reconstructed_relation_diagnostic=causal_rows,scope='Source hashes, archive hashes, sampler coordinates, LP/QP certificates and field/noise replay. Not a full search replay or external validation.')
    (HERE/'CALIBRATION_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
