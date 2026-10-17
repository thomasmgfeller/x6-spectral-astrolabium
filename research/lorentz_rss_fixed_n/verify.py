"""Archive verification and complete fresh-seed replay; no scientific reclassification."""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import numpy as np
from analysis import summarize
from run import HERE, source_hashes
from selftest import execute as selftest


def close(a,b,path='root'):
    if isinstance(a,dict):
        assert set(a)==set(b),path
        for key in a: close(a[key],b[key],path+'/'+key)
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)): close(x,y,path+'/'+str(i))
    elif isinstance(a,float):
        assert np.isclose(a,b,rtol=1e-9,atol=1e-11), (path,a,b)
    else: assert a==b,(path,a,b)


def execute(replay=False):
    selftest()
    archive=HERE/'results'
    hashes=json.loads((archive/'hashes.json').read_text())
    for name,digest in hashes.items():
        assert hashlib.sha256((archive/name).read_bytes()).hexdigest()==digest,name
    provenance=json.loads((archive/'provenance.json').read_text())
    assert source_hashes(provenance['source_commit'])==provenance['source_sha256']
    contract=json.loads((HERE/'contract.json').read_text())
    refs=json.loads((archive/'reference.json').read_text())
    data=np.load(archive/'raw.npz',allow_pickle=False)
    assert data['importance_slopes'].shape==(8192,7,3)
    assert data['direct_counts'].shape==(8,2048,3)
    assert np.isfinite(data['importance_slopes']).all()
    summary=summarize(data,contract,refs['geometry'],refs['quadrature'])
    close(summary,json.loads((archive/'summary.json').read_text()))
    if replay:
        with tempfile.TemporaryDirectory(prefix='rss-fixed-n-') as temp:
            out=Path(temp)/'replay'
            subprocess.run([sys.executable,'-B',str(HERE/'run.py'),str(out),'--source-commit',provenance['source_commit']],check=True)
            fresh=np.load(out/'raw.npz',allow_pickle=False)
            for name in data.files:
                if data[name].dtype.kind=='f':
                    assert np.allclose(data[name],fresh[name],rtol=1e-9,atol=1e-11),name
                else: assert np.array_equal(data[name],fresh[name]),name
            close(summary,json.loads((out/'summary.json').read_text()))
            close(refs,json.loads((out/'reference.json').read_text()))
    print(json.dumps(dict(status='PASS_FULL_RSS_FIXED_N_REPLAY' if replay else 'PASS_ARCHIVED_RSS_FIXED_N',
                          independent_clouds=summary['total_independent_clouds'],scientific_status=summary['primary_slope_status'],
                          external_replication=False)))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--replay',action='store_true')
    execute(parser.parse_args().replay)
