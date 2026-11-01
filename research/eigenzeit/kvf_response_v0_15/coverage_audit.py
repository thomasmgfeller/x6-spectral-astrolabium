"""Fresh, fixed-budget coverage audit; uses scipy's independent t sampler."""
import argparse,hashlib,json
from pathlib import Path
import numpy as np
from scipy.stats import multivariate_t,beta
from gum import cp
from reproduce import compare


def audit():
    for line in Path('AUDIT_FREEZE.sha256').read_text().splitlines():
        h,p=line.split(None,1);assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,p
    plan=json.loads(Path('AUDIT_PLAN.json').read_text());c=json.loads(Path('CONTRACT.json').read_text())
    result={}
    for name in c['models']:
        blocks=np.load('raw/'+name+'_blocks.npy');n,d=blocks.shape;nu=n-d
        mu=blocks.mean(0);S=np.cov(blocks,rowvar=False);scale=(n-1)/(nu*n)*S
        rec=json.loads(Path('records/'+name+'.json').read_text());ell=rec['joint_ellipsoid']
        center=np.array(rec['exact_pdf_mean']);cov=np.array(rec['exact_pdf_covariance']);inv=np.linalg.inv(cov)
        rng=np.random.default_rng(plan['seeds'][name]);hits=0;N=plan['draws_each_model'];step=plan['chunk_size']
        for start in range(0,N,step):
            size=min(step,N-start)
            x=multivariate_t.rvs(mu,scale,df=nu,size=size,random_state=rng)
            common=rng.uniform(-c['gum_common_bias_halfwidth'],c['gum_common_bias_halfwidth'],(size,1))
            local=rng.uniform(-c['gum_local_bias_halfwidth'],c['gum_local_bias_halfwidth'],(size,d))
            K=rng.uniform(.99,1.01,(size,1))
            y=(x-common-local)/K-center
            hits+=int(np.sum(np.einsum('ij,jk,ik->i',y,inv,y)<=ell['radius_squared']))
        ci=cp(hits,N,plan['interval_alpha_each'])
        M=ell['radius_draws'];k=int(np.ceil(.95*M))
        cal=[float(beta.ppf(.005,k,M+1-k)),float(beta.ppf(.995,k,M+1-k))]
        delta=np.array(rec['nominal_response'])-center
        q=float(delta@inv@delta)
        result[name]=dict(draws=N,hits=hits,estimated_pdf_coverage=hits/N,coverage_probability_99_5pct_interval=ci,
            target_in_interval=ci[0]<=.95<=ci[1],original_radius_squared=ell['radius_squared'],
            calibration_order_statistic_99pct_probability_interval=cal,
            single_raw_dataset_nominal_radius_squared=q,single_raw_dataset_nominal_vector_inside=q<=ell['radius_squared'])
    return dict(status='FIXED_RADIUS_COVERAGE_AUDIT_REPORTED',results=result,
        original_data_and_radius_unchanged=True,physical_release='HOLD_FIELD_TRANSFER')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--verify',action='store_true');args=p.parse_args()
    out=audit();target=Path('records/coverage_audit.json')
    if args.verify:compare(json.loads(target.read_text()),out,'coverage_audit');print('COVERAGE_AUDIT_REPLAY_PASS')
    else:target.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
