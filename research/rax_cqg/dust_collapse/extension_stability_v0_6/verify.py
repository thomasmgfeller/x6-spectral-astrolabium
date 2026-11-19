"""Check the published v0.6 study and optionally rebuild its numerical tables."""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
STUDY=ROOT/'study'
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS'):
    os.environ[key]='1'

def main():
    if not __debug__:raise RuntimeError('Run without -O.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rebuild',action='store_true')
    args=parser.parse_args()
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        expected,rel=line.split('  ',1)
        path=ROOT/rel
        if hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise ValueError(rel)
    sys.path.insert(0,str(STUDY))
    import positive,exact,audit
    positive.verify(); controls=audit.run()
    for tag in ('coarse','fine'):
        assert controls['checks'][tag]['archived_40x40_max_error']<5e-14
        for t in [Fraction(1,20),Fraction(5021,100000)]:
            result=exact.verify(tag,t)
            frozen=json.loads((STUDY/'result.json').read_text())[tag][str(t)]
            assert max(abs(a-b) for a,b in zip(result['support_success_lower'],frozen['support_success_lower']))<1e-12
    import analytic
    analytic.run()
    refined=json.loads((STUDY/'refined.json').read_text())
    direct=json.loads((STUDY/'direct.json').read_text())
    eligible={name for name,r in direct.items() if max(abs(complex(*a)-complex(*b)) for a,b in
                zip(r['rows']['coarse'],r['rows']['fine']))>2e-12}
    assert set(refined)==eligible|{'N14_734','N14_760','N14_8191'}
    assert max(r['change_from_48_8'] for r in refined.values())<1e-7
    print('PASS: both finite grids; universal 0.050210, failing witness 0.050211.',flush=True)
    if not args.rebuild:return
    import numpy as np
    with tempfile.TemporaryDirectory() as tmp:
        work=Path(tmp)
        shutil.copytree(ROOT.parent/'extension_stability_v0_5',work/'reference'); local=work/'study';local.mkdir()
        for src in STUDY.glob('*.py'):shutil.copy2(src,local/src.name)
        def run(name,*more):
            subprocess.run([sys.executable,'-B',str(local/name),*more],cwd=work,check=True)
        masks=[s.split('_')[1] for s in direct]
        run('scalar.py'); run('amplitude_caps.py'); run('five_factors.py');run('tails.py',*masks)
        run('refine.py');run('positive.py');run('audit.py');run('exact.py')
        assert abs(np.load(local/'gram.npy')-np.load(STUDY/'gram.npy')).max()<5e-13
        for name,original in direct.items():
            regenerated=json.loads((local/'direct.json').read_text())[name]
            for tag in ('coarse','fine'):
                assert max(abs(complex(*a)-complex(*b)) for a,b in zip(
                    original['rows'][tag],regenerated['rows'][tag]))<1e-10
        for f in ('caps.json','extra_cap.json'):
            original=json.loads((STUDY/f).read_text());new=json.loads((local/f).read_text())
            assert set(original)==set(new)
            assert max(abs(x-new[k][s]) for k,row in original.items() for s,x in row.items())<1e-10
        assert max(r['change_from_48_8'] for r in json.loads((local/'refined.json').read_text()).values())<1e-7
        print('PASS: numerical inputs rebuilt in a temporary directory.')
if __name__=='__main__':main()
