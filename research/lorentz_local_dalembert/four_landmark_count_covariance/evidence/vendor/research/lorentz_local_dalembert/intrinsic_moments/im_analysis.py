"""Frozen all-cloud gates and independent verification of stored witnesses."""
import argparse
from collections import Counter
import json
from pathlib import Path
import numpy as np
from im_common import config
from volume_analysis import load,rms
from moment_analysis import stats
import intrinsic

def validate_record(row,c):
    s=row['selection'];f=row['inference']['frame'];cal=row['inference'].get('calibration');oracle=row['coordinate_oracle']
    valid=True
    if f['status']=='ok':
        counts={tuple(sorted(p)):n for p,n in zip(f['interval_pairs'],f['interval_counts'])}
        q=lambda a,b:(counts[tuple(sorted((a,b)))]/(row['rho']*intrinsic.VOLUME))**(2/3)
        h,v=intrinsic.gram_and_vectors(q,f['landmarks'],s['root'],s['support'],s['tau_m'])
        np.testing.assert_allclose(h,f['gram'],atol=1e-10,rtol=1e-9);np.testing.assert_allclose(v,f['vectors'],atol=1e-10,rtol=1e-9)
        t=np.array(f['transform']);z=np.array(f['features']);ev=np.linalg.eigvalsh(h)
        np.testing.assert_allclose(t@h@t.T,intrinsic.ETA,atol=1e-9,rtol=1e-9)
        np.testing.assert_allclose(t@t.T,np.diag(1/np.abs(ev)),atol=1e-9,rtol=1e-9)
        np.testing.assert_allclose(z,(t@v).T,atol=1e-10,rtol=1e-9)
        np.testing.assert_allclose(z@z.T,f['feature_gram'],atol=1e-10,rtol=1e-9)
        np.testing.assert_allclose(z@intrinsic.ETA@z.T,f['lorentz_feature_gram'],atol=1e-10,rtol=1e-9)
        np.testing.assert_allclose(intrinsic.design(z),cal['design'],atol=1e-10,rtol=1e-9)
        np.testing.assert_allclose(ev,f['eigenvalues'],atol=1e-10,rtol=1e-9)
        condition=float(np.max(np.abs(ev))/np.min(np.abs(ev)))
        np.testing.assert_allclose(condition,f['condition'],atol=1e-10,rtol=1e-9)
        assert condition<=c['raw_max_condition'] and ev[0]<0<ev[1]
        halves=[]
        for i in [0,1]:
            hc={tuple(sorted(p)):n for p,n in zip(f['interval_pairs'],f['half_interval_counts'][i])}
            qh=lambda a,b:(2*hc[tuple(sorted((a,b)))]/(row['rho']*intrinsic.VOLUME))**(2/3)
            hh,vh=intrinsic.gram_and_vectors(qh,f['landmarks'],s['root'],s['support'],s['tau_m']);halves.append((hh,vh))
            np.testing.assert_allclose(hh,f['half_grams'][i],atol=1e-10,rtol=1e-9)
            np.testing.assert_allclose(vh,f['half_vectors'][i],atol=1e-10,rtol=1e-9)
        assert all(a+b==n for a,b,n in zip(*f['half_interval_counts'],f['interval_counts']))
        guard=intrinsic.noise_guard(h,v,t,halves,f['interval_counts'],f['half_interval_counts'],condition,c)
        assert guard['checks']==f['guard']['checks'] and guard['passed']==f['guard']['passed']
        assert guard['reasons']==f['guard']['reasons']
    if s['status']=='ok':
        a0=np.array(s['weights'])*s['tau_m']**2;mask=[b in s['temporal'] for b in s['support']]
        for q in [cal,oracle]:
            if q is not None:
                valid=intrinsic.validate_calibration(q,c) and valid
                np.testing.assert_allclose(a0,q['baseline'],atol=1e-10,rtol=1e-9)
                assert mask==list(q['temporal_mask'])
        for name in ['intrinsic_raw','intrinsic_guarded']:
            raw=cal is not None and cal['status']=='VERIFIED';adopted=raw and (name=='intrinsic_raw' or f['guard']['passed'])
            assert row['arms'][name]['adopted']==adopted
            wanted=np.array(cal['weights'])/s['tau_m']**2 if adopted else s['weights']
            np.testing.assert_allclose(row['arms'][name]['weights'],wanted,atol=1e-10,rtol=1e-9)
            np.testing.assert_allclose(row['inference'][name]['weights'],wanted,atol=1e-10,rtol=1e-9)
    return valid

def summarize(directory):
    c,_=config();e,rows=load(directory);mode=e['mode']
    expected=[(rho,seed) for i,rho in enumerate(c['densities']) for seed in
        (c['development_seeds'] if mode=='development' else [c['test_seed_base']+100*i+j for j in range(c['test_replicates_per_density'])])]
    complete=e['status']=='COMPLETE' and [(r['rho'],r['seed']) for r in rows]==expected
    budget=e['seconds']<=c['wall_budget_seconds'] and e['peak_mib']<=c['memory_budget_mib']
    certificates=all(validate_record(r,c) for r in rows)
    controls=e['controls']['status']=='PASS_SOFTWARE_CONTROLS' and all(
        (r['cloud_controls'] is None or r['cloud_controls']['status']=='PASS') and
        all(a['status']!='ok' or a['evaluation']['algebra_pass'] for a in r['arms'].values()) for r in rows)
    cells=[]
    for rho in c['densities']:
        group=[r for r in rows if r['rho']==rho];arms={}
        for name in c['methods']:
            available=[r for r in group if r['arms'][name]['status']=='ok'];ev=[r['arms'][name]['evaluation'] for r in available]
            base=[r['arms']['volume_shell']['evaluation'] for r in available];paired={}
            for key in ['independent_field_rms','metric_error','affine_drift']:
                a=rms([x[key] for x in base]);b=rms([x[key] for x in ev])
                paired[key]=dict(baseline_rms=a,candidate_rms=b,ratio=b/a if a else None,
                    squared_reduction=stats([x[key]**2-y[key]**2 for x,y in zip(base,ev)]))
            adopted=sum(r['arms'][name]['adopted'] for r in group)
            arms[name]=dict(available=len(ev),total=len(group),availability=len(ev)/len(group) if group else 0,
                adopted=adopted,adoption_fraction=adopted/len(group) if group else 0,paired=paired,
                fallback_reasons=dict(Counter(reason for r in group for reason in r['arms'][name]['fallback_reasons'])),
                lorentz_signatures=sum(x['lorentz_signature'] for x in ev),
                absolute_mass=stats([x['absolute_mass'] for x in ev]),iid_noise_variance_factor=stats([x['iid_noise_variance_factor'] for x in ev]),
                independent_fields={key:dict(target=ev[0]['independent_fields'][key]['target'],
                    normalized_error=stats([x['independent_fields'][key]['normalized_error'] for x in ev]),
                    normalized_error_rms=rms([x['independent_fields'][key]['normalized_error'] for x in ev]))
                    for key in ev[0]['independent_fields']} if ev else {})
        frames=[r['inference']['frame'] for r in group if r['inference']['frame']['status']=='ok']
        cells.append(dict(rho=rho,arms=arms,frame_status=dict(Counter(r['inference']['frame']['status'] for r in group)),
            frames=dict(available=len(frames),condition=stats([f['condition'] for f in frames]),
                minimum_interval=stats([min(f['interval_counts']) for f in frames]),
                worst_half_gram_error=stats([max(x['gram_error'] for x in f['guard']['halves']) for f in frames]),
                worst_half_feature_error=stats([max(x['feature_error'] for x in f['guard']['halves']) for f in frames]),
                guard_failures=dict(Counter(reason for f in frames for reason in f['guard']['reasons'])))))
    primary=next(x for x in cells if x['rho']==c['primary_density'])['arms'][c['primary_method']]
    gates=dict(availability=primary['availability']>=c['minimum_availability'],guarded_adoption=primary['adoption_fraction']>=c['minimum_guarded_adoption'])
    for key in ['independent_field_rms','metric_error','affine_drift']:
        ratio=primary['paired'][key]['ratio'];gates[key]=ratio is not None and ratio<=c['maximum_primary_rms_ratio']
    passed=complete and budget and certificates and controls and all(gates.values())
    return dict(schema='x6.bk-intrinsic-moments-summary/1',mode=mode,complete=complete,budget_pass=budget,
        certificates_pass=certificates,controls_pass=controls,clouds=len(rows),cells=cells,primary_gates=gates,
        decision=('INTRINSIC_MOMENT_IMPROVEMENT' if passed else 'INTRINSIC_MOMENT_HOLD') if mode=='test' else 'DEVELOPMENT_ONLY',
        phase3='HOLD_PHASE3',note='Fixed intrinsic candidate with conditional count-thinning guard. Independent-field response is not a locality, convergence, metric or curvature qualification.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();s=summarize(a.directory)
    (a.directory/'summary.json').write_text(json.dumps(s,indent=2)+'\n');print(json.dumps(s,indent=2))
