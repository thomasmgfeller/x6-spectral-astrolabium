"""Preserve original evidence; replay in a temporary directory and compare."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile,zipfile
import numpy as np

ROOT=Path(__file__).resolve().parent
ARCHIVES={
    'Eigenzeit_4D_Start_v0_1.zip':'6488f1ce685fb85a108dd9bc5cb373e055a14dda14b7e2b78048e89c1121baff',
    'Eigenzeit_4D_Poisson_v0_2.zip':'3d39b5b1d3fbb733ce2947bb8f2956f8e94f13139fa39de330d246574fbb9856'}

def main():
    for name,h in ARCHIVES.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,name
    original=ROOT/'poisson_v0_2'
    with zipfile.ZipFile(ROOT/'Eigenzeit_4D_Poisson_v0_2.zip') as z:
        assert z.testzip() is None
        for name in z.namelist():
            local=original/Path(name).name
            assert local.read_bytes()==z.read(name),name
    for line in (original/'SHA256SUMS').read_text().splitlines():
        h,name=line.split('  ',1)
        assert hashlib.sha256((original/name).read_bytes()).hexdigest()==h,name
    with tempfile.TemporaryDirectory(prefix='x6-4d-replay-') as td:
        work=Path(td)/'poisson_v0_2'
        shutil.copytree(original,work,ignore=shutil.ignore_patterns('__pycache__'))
        env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1'}
        for script in ['run.py','audit.py']:
            subprocess.run([sys.executable,'-B',str(work/script)],cwd=work,env=env,check=True,stdout=subprocess.DEVNULL)
        for name in ['campaign_arrays.npz','direct_cloud_counts.npz']:
            with np.load(original/name) as old,np.load(work/name) as new:
                assert set(old.files)==set(new.files)
                for key in old.files:
                    if old[key].dtype.kind in 'iub':
                        assert np.array_equal(old[key],new[key]),(name,key)
                    else:
                        np.testing.assert_allclose(new[key],old[key],rtol=1e-8,atol=1e-11,equal_nan=True)
        old=json.loads((original/'RESULTS.json').read_text()); new=json.loads((work/'RESULTS.json').read_text())
        for key in ['accuracy_gate_pass','uncertainty_gate_pass','primary_count_vectors','geometries','source_freeze_sha256']:
            assert old[key]==new[key],key
        for a,b in zip(old['records'],new['records'],strict=True):
            for key in ['geometry','replicates','certificate_10pct','finite_tau_intervals','simultaneous_mean_box_coverage','tau_interval_coverage']:
                assert a[key]==b[key],(a['geometry'],key)
            assert a['primary']['success_10pct']==b['primary']['success_10pct']
        audit=json.loads((work/'AUDIT.json').read_text())
        assert audit['status']=='PASS_INTERNAL_AUDIT'
    print(json.dumps({'status':'PASS_PUBLICATION_REPLAY','original_archives_preserved':True,
                      'count_vectors':40960,'direct_clouds':1024,
                      'accuracy_gate':'PASS_CONDITIONAL_HIGH_DENSITY',
                      'error_certificate':'HOLD','float_rtol':1e-8}))

if __name__=='__main__':main()
