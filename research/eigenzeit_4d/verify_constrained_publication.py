"""Full paired v0.5 replay without changing the archived evidence."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,tempfile
import numpy as np
from verify_joint_publication import compare

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'constrained_region_v0_5'


def main():
    for line in (SOURCE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()==digest,name
    with tempfile.TemporaryDirectory(prefix='eigenzeit-constrained-replay-') as tmp:
        base=Path(tmp)
        for name in ['poisson_v0_2','joint_region_v0_3','refined_bound_v0_4','constrained_region_v0_5']:
            shutil.copytree(ROOT/name,base/name,ignore=shutil.ignore_patterns('__pycache__'))
        work=base/'constrained_region_v0_5'
        env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
        for script in ['experiment.py','audit_v05.py','development.py']:
            subprocess.run([sys.executable,'-B',str(work/script)],check=True,env=env)
        for name in ['RESULTS.json','CERTIFICATES.json','AUDIT.json','DEVELOPMENT.json']:
            compare(json.loads((SOURCE/name).read_text()),json.loads((work/name).read_text()),name)
        old=np.load(SOURCE/'fresh_counts.npz');new=np.load(work/'fresh_counts.npz')
        assert old.files==new.files
        assert np.array_equal(old['cells'],new['cells'])
        np.testing.assert_allclose(old['metrics'],new['metrics'],rtol=1e-8,atol=1e-11,equal_nan=True)
    print('PASS: v0.5 paired observations, geometric certificates, fallback, audits and gates reproduced.')


if __name__=='__main__':main()
