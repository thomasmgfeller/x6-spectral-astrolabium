"""Verify before importing sources. Optional isolated reconstruction of the study."""
from argparse import ArgumentParser
from hashlib import sha256
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
for var in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS'):
    os.environ[var]='1'

def main():
    if not __debug__: raise RuntimeError('Run without -O.')
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('--rebuild',action='store_true')
    args=parser.parse_args()
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1)
        if sha256((ROOT/name).read_bytes()).hexdigest()!=expected: raise ValueError(name)
    import catalog
    import certificate
    import full
    import bottleneck
    from caps import calculator
    from control import brute_forest
    def archived(name):
        return json.loads((ROOT/name).read_text())
    def canonical(x):
        return json.loads(json.dumps(x))
    assert canonical(catalog.calculate())==archived('catalog.json')
    fresh=certificate.calculate();original=archived('certificate.json')
    assert canonical(fresh['grids'])==original['grids']
    assert max(fresh['positive_congruence_residuals'])<1e-7
    assert canonical(full.calculate())==archived('full.json')
    assert {t:bottleneck.calculate(t) for t in ('coarse','fine')}==archived('bottleneck.json')
    control=archived('controls.json');bound=calculator(4,3)
    assert max(abs(bound(m)-1e-12-brute_forest(m,4,3)) for m in control['forest_direct_masks'])<1e-14
    assert control['original_kernel_obstructions_rechecked']==archived('catalog.json')['counts']['excluded']
    print('PASS: catalogue, positive pilot, full-support fraction, independent forest checks.', flush=True)
    if args.rebuild:
        import numpy as np
        with tempfile.TemporaryDirectory() as temp:
            work=Path(temp)
            from model import ARCHIVE
            shutil.copy2(ARCHIVE, work/'input_v06.zip')
            for file in ROOT.glob('*.py'):
                shutil.copy2(file,work/file.name)
            for stem in ['catalog','pilot','matrices','caps','projections','control','certificate','full']:
                subprocess.run([sys.executable,'-B',str(work/(stem+'.py'))],cwd=work,check=True)
            read=lambda f:json.loads((work/f).read_text())
            assert read('catalog.json')==archived('catalog.json')
            original_clocks=archived('clocks.json')
            for k,v in read('clocks.json').items():
                for tag,a in v['rows'].items():
                    assert np.max(abs(np.array(a)-np.array(original_clocks[k]['rows'][tag])))<1e-11
            assert np.max(abs(np.load(work/'gram.npy')-np.load(ROOT/'gram.npy')))<1e-12
            for file in ['caps.json','anchor_rows.json']:
                a=read(file); b=archived(file); assert set(a)==set(b)
                for k,row in a.items():
                    if file=='caps.json': assert max(abs(x-b[k][tag]) for tag,x in row.items())<1e-12
                    else: assert np.max(abs(np.array(row)-np.array(b[k])))<1e-12
            assert read('full.json')['bound_fraction']==archived('full.json')['bound_fraction']
        print('PASS: isolated rebuild.',flush=True)
if __name__=='__main__':main()
