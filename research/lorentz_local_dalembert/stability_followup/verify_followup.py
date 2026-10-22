"""Post-run independent numerical audit and descriptive diagnostic summary.
SPDX-License-Identifier: Apache-2.0
"""
import gzip,hashlib,json
from collections import Counter
from pathlib import Path
import numpy as np
from models import PRIOR,estimate
from inference import ETA,four_geometry,normalize,design
from fit import input_mask
from run import encode,save
from runner import verify_freeze

HERE=Path(__file__).resolve().parent
def main():
    verify_freeze();c=json.loads((HERE/'contract.json').read_text());oldc=json.loads((PRIOR/'contract.json').read_text())
    source_checks=0;fit_checks=0;max_moment=0.;max_weights=0.;max_loss=0.;new_hashes=set()
    for mode in ['development','conditional']:
        for index in c['selected_indices']:
            oldraw=(PRIOR/f'results/cloud-{index:02d}.json.gz').read_bytes();old=json.loads(gzip.decompress(oldraw));p=old['selection']['fourth']['packet'];nodes=p['landmarks']+[p['root']]+p['support'];lookup={a:i for i,a in enumerate(nodes)}
            raw=(HERE/f'{mode}/cloud-{index:02d}.json.gz').read_bytes();r=json.loads(gzip.decompress(raw));truth=json.loads((HERE/f'{mode}/truth/cloud-{index:02d}.json').read_text())
            assert r['source_sha256']==hashlib.sha256(oldraw).hexdigest()
            assert truth['inference_sha256']==hashlib.sha256(raw).hexdigest();source_checks+=1
            for rr in r['replicates']:
                rep=rr['replicate'];obs=rr['observed'] if mode=='conditional' else old['replicates'][rep]['observed']
                counts=np.array(obs['counts']);C=np.array(obs['overlaps'],float)
                assert np.array_equal(C,C.T) and np.array_equal(C.diagonal(),counts) and all(obs['intersection_replay'])
                if mode=='conditional':
                    assert obs['coordinates_sha256']!=old['replicates'][rep]['observed']['coordinates_sha256']
                    new_hashes.add(obs['coordinates_sha256'])
                for arm in (c['development_arms'] if mode=='development' else ['full_gls']):
                    f=rr['arms'][arm]
                    if f['status']!='WEIGHTS_VALID':continue
                    fit_checks+=1;z=np.array(f['coordinates']);w=np.array(f['weights']);scale=p['scale']
                    d=z[None]-z[:,None];s2=d[:,:,1]**2+d[:,:,2]**2-d[:,:,0]**2;observed=np.array(p['full_order'],bool);order=(d[:,:,0]>0)&(s2<0)
                    matches=bool(np.array_equal(order,observed));assert f['qualified']==matches
                    if arm!='no_support_order':assert matches
                    t,x,y=(z[5:]-z[4]).T;D=np.array([t,x,y,t*t,x*x,y*y,t*x,t*y,x*y]);target=np.array([0,0,0,-2,2,2,0,0,0.])
                    err=float(np.max(abs(D@(w[1:]*scale**2)-target)));max_moment=max(max_moment,err);assert err<1e-6
                    H=np.eye(len(t))+np.ones((len(t),len(t)));Q=np.linalg.solve(H,D.T);a=Q@np.linalg.solve(D@Q,target);direct=np.r_[-a.sum(),a]/scale**2
                    err=float(np.max(abs(direct-w)/(1+abs(w))));max_weights=max(max_weights,err);assert err<1e-5
                    mask=input_mask(p);pairs=np.array([[lookup[a],lookup[b]] for a,b in p['pairs']])[mask];delta=z[pairs[:,1]]-z[pairs[:,0]];q=delta[:,0]**2-delta[:,1]**2-delta[:,2]**2;assert np.all(q>0)
                    lam=c['count_density']*np.pi/12*scale**3*q**1.5;n=counts[mask];residual=lam-n
                    if arm=='no_support_order':loss=2*np.mean(lam-n+n*np.log(n/lam))
                    else:
                        cov=C[np.ix_(mask,mask)];alpha=c['fit']['correlation_shrinkage'];cov=(1-alpha)*cov+alpha*np.diag(n) if arm=='full_gls' else np.diag(n)
                        loss=residual@np.linalg.solve(cov,residual)/len(n)
                    err=abs(float(loss)-f['objective']);max_loss=max(max_loss,err);assert err<1e-7
    # Selection witness inventory; no further full A simulation is needed because
    # selection_audit already checked byte-identical regeneration on every seed.
    funnel=Counter();selection=[];eligible_checked=0
    for index in c['selection_failure_indices']:
        raw=(HERE/f'selection/cloud-{index:02d}.json.gz').read_bytes();r=json.loads(gzip.decompress(raw));assert r['selection_identical'] and r['exhausted']
        oldraw=(PRIOR/f'results/cloud-{index:02d}.json.gz').read_bytes();assert hashlib.sha256(oldraw).hexdigest()==r['source_sha256']
        records=r['records'];assert len(records)==r['funnel']['pool'];funnel.update(r['funnel'])
        for side in ['past','future']:
            ranks=[x['rank'] for x in records if x['side']==side];assert ranks==list(range(len(ranks)))
        assert len({x['candidate'] for x in records})==len(records)
        eligible=[x for x in records if x['status']=='ELIGIBLE'];assert len(eligible)==r['funnel'].get('eligible',0)
        assert not any(x['in_original_cap'] for x in eligible)
        count_eligible=[x for x in records if x['status'] in ['ELIGIBLE','GEOMETRY_HOLD']]
        assert len(count_eligible)==r['funnel'].get('count_eligible',0)
        # Replaying eligibility-before-cap retains all count-eligible candidates
        # in these failed cases: none has 128 on either side.
        assert all(sum(x['side']==side for x in count_eligible)<128 for side in ['past','future'])
        for x in eligible:
            p=x['packet'];values=np.array(x['counts']);q=(values[:,0]/(c['count_density']*np.pi/12))**(2/3)/p['scale']**2
            h,z,_,_=four_geometry(q,p);_,cond=normalize(h);assert cond<=oldc['selection']['maximum_landmark_condition']
            D=design(z[5:]);assert np.linalg.matrix_rank(D)==9 and np.linalg.cond(D)<=oldc['selection']['maximum_design_condition']
            assert np.isclose(cond,x['landmark_condition'],atol=1e-9,rtol=1e-9);eligible_checked+=1
        selection.append(dict(index=index,pool=len(records),count_eligible=len(count_eligible),eligible=len(eligible),original_cap_missed=bool(eligible)))
    assert len(new_hashes)==171
    from simulation import counting_cloud
    oldc['count_seed_tag']=c['conditional_count_seed_tag'];replay=[]
    for index in [c['selected_indices'][0],c['selected_indices'][-1]]:
        old=json.loads(gzip.decompress((PRIOR/f'results/cloud-{index:02d}.json.gz').read_bytes()));p=old['selection']['fourth']['packet']
        truth=json.loads((HERE/f'conditional/truth/cloud-{index:02d}.json').read_text());r=json.loads(gzip.decompress((HERE/f'conditional/cloud-{index:02d}.json.gz').read_bytes()));stored=r['replicates'][0]
        obs=counting_cloud(dict(points=np.array(truth['points']),ids=truth['ids']),p,old['seed'],0,oldc);assert encode(obs)==encode(stored['observed'])
        fit=estimate(p,obs['counts'],obs['overlaps'],c['count_density'],c['fit'],'full_gls');assert fit['status']==stored['arms']['full_gls']['status']
        assert max(abs(np.array(fit['weights'])-stored['arms']['full_gls']['weights']))<1e-8;replay.append(index)
    verification=dict(status='PASS',bound_records=source_checks,new_unique_B_coordinate_hashes=len(new_hashes),valid_new_variant_fits_checked=fit_checks,max_direct_moment_residual=max_moment,max_relative_direct_weight_difference=max_weights,max_independent_loss_difference=max_loss,exhaustive_A_replays=13,selection_candidates_accounted=funnel['pool'],eligible_Gram_moment_rechecks=eligible_checked,count_and_fit_replay_indices=replay,scope='Internal audit with alternate linear solves and loss calculation; no external replication or global optimizer certificate. Added post-freeze without changing fitting/criteria.')
    if not (HERE/'verification.json').exists():save(HERE/'verification.json',verification)
    dev=json.loads((HERE/'analysis-development.json').read_text());paired=[r for r in dev['records'] if all(k in r['variance'] for k in ['four','old_poisson'])];cloud4=next(r for r in paired if r['index']==4)
    total=sum(r['variance']['old_poisson'] for r in paired);excess=sum(r['variance']['old_poisson']-r['variance']['four'] for r in paired)
    summary=dict(status='DIAGNOSIS_COMPLETE_CANDIDATE_HOLD',selection=selection,funnel=dict(funnel),capped_failures_with_feasible_uncapped_candidates=sum(r['original_cap_missed'] for r in selection),fixed_family_exhausted_without_candidate=[r['index'] for r in selection if not r['eligible']],counterfactual_selection_availability=(19+sum(r['original_cap_missed'] for r in selection)),counterfactual_scope='Feasibility only on 32 known A clouds, not weights, new-A validation or original qualification. Count-eligibility before cap would retain all feasible candidates in the nine rescued cases.',variance_cloud04=dict(values=cloud4['variance'],share_original_fit_variance=cloud4['variance']['old_poisson']/total,share_net_variance_excess=(cloud4['variance']['old_poisson']-cloud4['variance']['four'])/excess,leave04out_ratio=sum(r['variance']['old_poisson'] for r in paired if r['index']!=4)/sum(r['variance']['four'] for r in paired if r['index']!=4),scope='Posthoc concentration diagnostic only; cloud04 retained in every gate. Share of net excess can exceed 100% because other clouds offset it.'),conditional_gate_status=json.loads((HERE/'analysis-conditional.json').read_text())['status'])
    if not (HERE/'diagnostic-summary.json').exists():save(HERE/'diagnostic-summary.json',summary)
    print(json.dumps(verification,indent=2));print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
