#!/usr/bin/env python3
"""Retrospective localization only: all original observations are unblinded."""
import gzip, hashlib, json, math, subprocess, sys
from decimal import Decimal, localcontext
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import kstest

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OUT=HERE/'results'
SEEDS=[0,1,20261017,4294967295]
DTYPE=np.dtype([('u','<u4'),('w','<f8')])
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def ks(x):
    t=kstest(x,'uniform',method='exact')
    v=np.sort(x);n=len(v)
    direct=max(np.max(np.arange(1,n+1)/n-v),np.max(v-np.arange(n)/n))
    assert abs(direct-t.statistic)<1e-15
    return dict(n=n,D=float(t.statistic),p=float(t.pvalue),location=float(t.statistic_location),sign=int(t.statistic_sign),direct_D=float(direct))
def load_trace(path):return np.frombuffer(gzip.decompress(path.read_bytes()),dtype=DTYPE)
def main():
    OUT.mkdir(exist_ok=True)
    archive=HERE.parent/'v1b_boundary/results'
    for line in (archive/'SHA256SUMS').read_text().splitlines():
        h,name=line.split(maxsplit=1)
        assert digest(archive/name)==h, name
    config=dict(output=str(OUT),historical=True,m=16384,summary_file='historical_trace.json',groups=[dict(id='historical_d4',streams=[dict(id=f's{s}',seed=s) for s in SEEDS])])
    temp=OUT/'historical_config.json';temp.write_text(json.dumps(config))
    subprocess.run(['node',str(HERE/'trace.cjs'),str(temp)],check=True);temp.unlink()
    raw=json.loads(gzip.decompress((archive/'native_raw.json.gz').read_bytes()))
    trace=load_trace(OUT/'historical_d4.bin.gz');u=trace['u']/2**32
    pts=np.concatenate([np.asarray(next(c['points'] for c in raw['clouds'] if c['d']==4 and c['parameters']['seed']==s)) for s in SEEDS])
    a=.5-np.abs(pts[:,0]);w=(np.linalg.norm(pts[:,1:],axis=1)/a)**3
    summary=json.loads((OUT/'historical_trace.json').read_text())
    details=[]
    for i,s in enumerate(SEEDS):
        sl=slice(i*16384,(i+1)*16384)
        details.append(dict(seed=s,radial_input=ks(u[sl]),reconstructed=ks(w[sl]),mean=float(u[sl].mean())))
    # Decimal re-evaluation of worst errors and KS location, plus fixed first/last.
    delta=np.abs(w-u);indices=set([0,len(u)-1,int(np.argmin(abs(w-ks(w)['location'])))])
    indices.update(map(int,np.argsort(delta)[-32:]))
    decimal_errors=[]
    with localcontext() as ctx:
        ctx.prec=80
        for i in sorted(indices):
            p=list(map(lambda x:Decimal.from_float(float(x)),pts[i]));aa=Decimal('.5')-abs(p[0])
            rr=sum(x*x for x in p[1:]).sqrt();ww=(rr/aa)**3
            decimal_errors.append(dict(index=i,error=float(abs(ww-Decimal(int(trace['u'][i]))/Decimal(2**32)))))
    report=dict(schema='x6.v1b-radial-diagnosis/1',kind='RETROSPECTIVE_UNBLINDED',base_commit='305a882d7c307a0f8e17ce3e18c23609376bd202',
        archive_sha256=digest(archive/'native_raw.json.gz'),all_18_archived_hashes_verified=True,
        runtime=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__),
        input_radial=ks(u),reconstructed_numpy=ks(w),reconstructed_native=ks(trace['w']),per_seed=details,
        max_numpy_transform_error=float(delta.max()),max_native_transform_error=float(np.max(abs(trace['w']-u))),
        decimal_checks=decimal_errors,trace=summary,
        original_gate='FAIL',overall_V1b='NOT_PASSED',
        conclusion='The old discrepancy is already present in the sampled radial PRNG inputs. Geometry, normal-direction normalization, and rounding do not create it. This does not establish a systematic PRNG defect; fresh controls are required.')
    (OUT/'diagnosis.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['input_radial','reconstructed_numpy','per_seed','max_numpy_transform_error','max_native_transform_error']},indent=2))
if __name__=='__main__':main()
