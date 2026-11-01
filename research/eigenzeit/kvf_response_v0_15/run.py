"""Generate frozen synthetic ABBA data, paired-reference controls and GUM records."""
import hashlib,json,platform
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import norm
from model import spectral
from gum import evaluate,cp
from certificate import certificate


def dump(name,obj):
    Path(name).write_text(json.dumps(obj,indent=2,allow_nan=False)+'\n')


def verify_freeze():
    for line in Path('FREEZE.sha256').read_text().splitlines():
        sha,p=line.split(None,1)
        assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha,p


def run():
    verify_freeze();c=json.loads(Path('CONTRACT.json').read_text());cert=certificate()
    dump('records/certificate.json',cert)
    n=c['primary_blocks'];times=np.array(c['shot_times']);sign=np.array(c['signs']);w=sign/4
    corr=np.full((4,4),.2);np.fill_diagonal(corr,1)
    channels=np.array([[1.,.4],[.4,1.]])
    raw_cov=np.kron(corr,channels)*(.05**2/.3);L=np.linalg.cholesky(raw_cov)
    results={}
    for name,mass in c['models'].items():
        R=np.array([spectral(mass,T)['R'] for T in c['delays']])
        # Exact support results replace floating point cancellation residues.
        R[[0,3]]=0
        if mass==0:R[2]=0
        rng=np.random.default_rng(c['seeds']['raw_'+name])
        data=(rng.standard_normal((n,4,8))@L.T).reshape(n,4,4,2)
        offset=np.array([[.3,-.4],[.7,.2],[-.2,.8],[.1,-.6]])
        slope=np.array([[.01,-.02],[.03,.015],[-.02,.04],[.05,-.01]])
        data+=offset[None,None,:,:]+times[None,:,None,None]*slope[None,None,:,:]
        # A shared odd feedthrough is present in both channels and cancels.
        data+=sign[None,:,None,None]*.02
        data[:,:,:,0]+=sign[None,:,None]*(c['synthetic_gain_true']*R+np.array(c['synthetic_odd_bias_true']))[None,None,:]
        np.save('raw/'+name+'.npy',data)
        blocks=np.einsum('t,nts->ns',w,data[:,:,:,0]-data[:,:,:,1])
        np.save('raw/'+name+'_blocks.npy',blocks)
        result=evaluate(blocks,c,c['seeds']['gum_'+name])
        result['nominal_response']=R.tolist();result['primary_raw_contrast']=float(blocks[:,2].mean())
        result['decision']='M1' if result['primary_raw_contrast']<c['decision_threshold'] else 'M0'
        dump('records/'+name+'.json',result);results[name]=dict(decision=result['decision'],primary_raw_contrast=result['primary_raw_contrast'],
            response_estimate=result['exact_pdf_mean'][2],standard_uncertainty=result['standard_uncertainty'][2],joint_ellipsoid=result['joint_ellipsoid'])
    rng=np.random.default_rng(c['seeds']['campaign']);M=c['endpoint_campaign_repeats']
    endpoint={}
    for name,mean in [('M0',-.0005),('M1',-.00742)]:
        sample=rng.normal(mean,.05/np.sqrt(n),M);np.save('raw/endpoint_'+name+'.npy',sample)
        errors=int(np.sum(sample<c['decision_threshold'])) if name=='M0' else int(np.sum(sample>=c['decision_threshold']))
        endpoint[name]=dict(repeats=M,errors=errors,error_probability_99pct_interval=cp(errors,M))
    endpoint['exact_Gaussian_endpoint_error']=float(norm.cdf(-cert['separation_gap']*np.sqrt(n)/(.1)))
    dump('records/campaign.json',endpoint)
    dump('records/summary.json',dict(status='SYNTHETIC_RESPONSE_CONTROL_COMPLETE',field_status='HOLD_FIELD_TRANSFER',
        results=results,conditional_error_bound_each=cert['error_bound_each'],physical_measurements=False,source_state='driven coherent control, not an undisturbed vacuum measurement',quantum_witness=False))
    dump('records/environment.json',dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
    print(json.dumps(dict(results=results,campaign=endpoint),indent=2))


if __name__=='__main__':run()
