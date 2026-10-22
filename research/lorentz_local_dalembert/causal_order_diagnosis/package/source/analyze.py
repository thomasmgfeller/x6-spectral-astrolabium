"""Post-seal evaluation; outcomes never fed back to selection or inference."""
import gzip,hashlib,json,math
from pathlib import Path
import numpy as np
from inference import solve,design

HERE=Path(__file__).resolve().parent

def main():
    c=json.loads((HERE/'contract.json').read_text());rows=[];evaluated=[]
    for index in range(c['clouds']):
        path=HERE/f'results/cloud-{index:02d}.json.gz'
        if not path.exists():
            rows.append(dict(index=index,status='NO_COMPLETED_RECORD'));continue
        raw=path.read_bytes();row=json.loads(gzip.decompress(raw));entry=dict(index=index,status=row['selection']['status'])
        if not row['replicates']:rows.append(entry);continue
        truth=json.loads((HERE/f'results/truth/cloud-{index:02d}.json').read_text())
        assert truth['inference_sha256']==hashlib.sha256(raw).hexdigest()
        points=np.array(truth['points']);x=points[4:]-points[4]
        packet=row['selection']['fourth']['packet'];scale=packet['scale']
        oracle,*_=solve(design(x[1:]/scale),np.array([0,0,0,-2,2,2,0,0,0.]),scale)
        original_z=np.array(row['selection']['baseline_selected']['certificate']['features'])/scale
        original,*_=solve(design(original_z),np.array([0,0,0,-2,2,2,0,0,0.]),scale)
        primary=row['replicates'][0]['inference'];f=primary['four'];b=primary['baseline']
        entry.update(primary_four=f['status'],primary_three=b['status'],qualified=f.get('qualified',False),
                     order=f.get('order'),four_valid_replicates=sum(r['inference']['four']['status']=='WEIGHTS_VALID' for r in row['replicates']))
        weights=dict(oracle=oracle,original_A=original)
        if f['status']=='WEIGHTS_VALID':weights['four_B']=np.array(f['weights'])
        if b['status']=='WEIGHTS_VALID':weights['three_B']=np.array(b['weights'])
        fields=[]
        variance_complete=all(r['inference']['four']['status']=='WEIGHTS_VALID' for r in row['replicates'])
        for spec in c['fields']:
            k=np.array(spec['k']);phase=spec['phase'];u=x@k
            func=np.cos if spec['kind']=='cos' else np.sin
            y=func(u+phase)-func(phase)
            linear=(-np.sin(phase) if spec['kind']=='cos' else np.cos(phase))*u
            exact=(k[0]**2-k[1]**2-k[2]**2)*func(phase)
            values={a:float(w@y) for a,w in weights.items()}
            field=dict(name=spec['name'],truth=float(exact),errors={a:v-exact for a,v in values.items()},
                       linear_response={a:float(w@linear) for a,w in weights.items()})
            if variance_complete:
                replicas=[np.array(r['inference']['four']['weights'])@y for r in row['replicates'][1:]]
                pred=float(y@np.array(f['weight_covariance'])@y)
                diag=float(y@np.array(f['independent_counts_negative_control'])@y)
                field['count_uncertainty']=dict(predicted_full=max(0.,pred),predicted_diagonal=max(0.,diag),
                    empirical=float(np.var(replicas,ddof=1)),replicate_mean=float(np.mean(replicas)),
                    primary_response=values['four_B'])
            fields.append(field)
        entry.update(fields=fields,variance_complete=variance_complete,
                     iid_noise_variance={a:float(c['field_noise_sigma']**2*(w@w)) for a,w in weights.items()})
        rows.append(entry);evaluated.append(entry)
    common=[r for r in evaluated if r.get('primary_four')=='WEIGHTS_VALID' and r.get('primary_three')=='WEIGHTS_VALID']
    def stats(population):
        if not population:return None
        fields=[f for r in population for f in r['fields']];arms=['original_A','three_B','four_B','oracle']
        rmse={a:float(np.sqrt(np.mean([f['errors'][a]**2 for f in fields]))) for a in arms}
        linear={a:float(np.sqrt(np.mean([f['linear_response'][a]**2 for f in fields]))) for a in arms}
        noise={a:float(np.mean([r['iid_noise_variance'][a] for r in population])) for a in arms}
        return dict(clouds=len(population),rmse=rmse,linear_rmse=linear,mean_iid_noise_variance=noise,
                    rmse_ratio=rmse['four_B']/rmse['three_B'],linear_ratio=linear['four_B']/linear['three_B'],
                    noise_ratio=noise['four_B']/noise['three_B'])
    primary=stats(common);qualified=stats([r for r in common if r['qualified']])
    calibration=[r for r in evaluated if r.get('variance_complete')]
    fs=[f['count_uncertainty'] for r in calibration for f in r['fields']]
    uncertainty=None
    if fs:
        empirical=float(np.mean([f['empirical'] for f in fs]));pred=float(np.mean([f['predicted_full'] for f in fs]));diag=float(np.mean([f['predicted_diagonal'] for f in fs]))
        uncertainty=dict(clouds=len(calibration),replicates_per_cloud=8,mean_empirical_variance=empirical,
                         mean_predicted_full=pred,mean_predicted_diagonal=diag,
                         empirical_over_full=empirical/pred,empirical_over_diagonal=empirical/diag,
                         scope='conditional on A, first-order count uncertainty; no interval for unbiased continuum truth')
    boot=None
    if len(common)>=2:
        rng=np.random.default_rng(c['bootstrap_seed']);sq=np.array([[np.mean([f['errors'][a]**2 for f in r['fields']]) for a in ['three_B','four_B']] for r in common])
        ix=rng.integers(0,len(common),size=(c['bootstrap_draws'],len(common)));means=sq[ix].mean(axis=1)
        boot=np.quantile(np.sqrt(means[:,1]/means[:,0]),[.025,.975]).tolist()
    g=c['primary_gates'];qualified_count=sum(r.get('qualified',False) for r in rows)
    gates=dict(all_scheduled_recorded=len(rows)==c['clouds'] and all(r['status']!='NO_COMPLETED_RECORD' for r in rows),
               qualified_availability=qualified_count>=g['minimum_qualified_primary_clouds'],
               common_availability=len(common)>=g['minimum_common_primary_weight_cases'],
               rmse=primary is not None and primary['rmse_ratio']<=g['maximum_rmse_ratio_four_to_three_B'],
               linear_response=primary is not None and primary['linear_ratio']<=g['maximum_linear_response_rmse_ratio'],
               noise_cost=primary is not None and primary['noise_ratio']<=g['maximum_mean_iid_noise_variance_ratio'],
               variance_calibration=uncertainty is not None and len(calibration)>=g['minimum_variance_calibration_clouds'] and .5<=uncertainty['empirical_over_full']<=2.)
    out=dict(status='PILOT_SUPPORTED' if all(gates.values()) else 'HOLD',scheduled=c['clouds'],
             selected_four=sum(r['status']=='SELECTED' for r in rows),qualified_primary=qualified_count,
             raw_common=primary,qualified_common=qualified,rmse_ratio_cloud_bootstrap_95=boot,
             uncertainty=uncertainty,gates=gates,records=rows,
             holds=c['holds'],note='Fresh bounded pilot, fixed rules; fields and B repeats do not multiply independent A clouds.')
    (HERE/'analysis.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'},indent=2))

if __name__=='__main__':main()
