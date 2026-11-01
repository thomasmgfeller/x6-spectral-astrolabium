"""Explicit cross-platform replay; never changes the original archive or freezes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import numpy as np


def compare_raw(reference,actual):
    if reference.dtype!=actual.dtype or reference.shape!=actual.shape:
        raise ValueError('raw dtype or shape mismatch')
    if reference.dtype!=np.dtype('float64'):
        raise ValueError('expected float64 raw data')
    if not np.all(np.isfinite(reference)) or not np.all(np.isfinite(actual)):
        raise ValueError('non-finite raw data')
    scale=max(1.,float(np.max(np.abs(reference))))
    limit=8*np.finfo(np.float64).eps*scale
    error=float(np.max(np.abs(actual-reference)))
    if error>limit:raise ValueError(f'raw numerical difference {error} exceeds {limit}')
    return dict(max_absolute_difference=error,absolute_tolerance=limit,array_equal=bool(np.array_equal(reference,actual)))


def comparator_controls():
    a=np.array([0.,.25,-.5,1.])
    b=a.copy();b[1]=np.nextafter(b[1],np.inf);compare_raw(a,b)
    for b in [a+1e-9,a[::-1],a.astype(np.float32),a[:3],np.array([0.,.25,np.nan,1.])]:
        try:compare_raw(a,b)
        except ValueError:continue
        raise AssertionError('comparator accepted corrupted data')


def replay(reference):
    comparator_controls()
    with tempfile.TemporaryDirectory() as temp:
        work=Path(temp)
        for folder in ['raw','records']:(work/folder).mkdir()
        files=['CONTRACT.json','FREEZE.sha256','model.py','certificate.py','gum.py','run.py',
               'check.py','reproduce.py','requirements.txt','AUDIT_PLAN.json','AUDIT_FREEZE.sha256',
               'coverage_audit.py','audit_reproduce.py','records/coverage_audit.json']
        for name in files:shutil.copyfile(reference/name,work/name)
        env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
        for name in ['run.py','check.py']:
            subprocess.run([sys.executable,'-B',name],cwd=work,env=env,check=True,stdout=subprocess.DEVNULL)
        sys.path.insert(0,str(work))
        from reproduce import compare
        records=['certificate','M0','M1','campaign','summary','check']
        equal=0
        for name in records:
            a=reference/'records'/f'{name}.json';b=work/'records'/f'{name}.json'
            compare(json.loads(a.read_text()),json.loads(b.read_text()),name)
            equal+=a.read_bytes()==b.read_bytes()
        originals=sorted((reference/'raw').glob('*.npy'))
        if {p.name for p in originals}!={p.name for p in (work/'raw').glob('*.npy')}:
            raise ValueError('raw inventory mismatch')
        raw={}
        for path in originals:
            target=work/'raw'/path.name
            row=compare_raw(np.load(path,allow_pickle=False),np.load(target,allow_pickle=False))
            row['byte_identical']=path.read_bytes()==target.read_bytes();raw[path.name]=row
        # Re-evaluate the original, frozen audit on regenerated block data,
        # keeping its original ellipse radii and input records for comparison.
        for name in ['M0','M1']:
            shutil.copyfile(reference/'records'/f'{name}.json',work/'records'/f'{name}.json')
        subprocess.run([sys.executable,'-B','coverage_audit.py','--verify'],cwd=work,env=env,check=True)
        print(json.dumps(dict(status='PORTABLE_NUMERICAL_REPLAY_PASS',records_compared=len(records),
            records_byte_identical=equal,raw_comparisons=raw,original_archive_unchanged=True,
            comparator_negative_controls='PASS',scope='Float64 roundoff tolerance; byte identity is reported separately'),indent=2))
