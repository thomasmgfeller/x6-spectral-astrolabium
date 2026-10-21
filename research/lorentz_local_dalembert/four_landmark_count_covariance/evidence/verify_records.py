import gzip,hashlib,json
from pathlib import Path
import numpy as np
from inference import measurement
HERE=Path(__file__).resolve().parent
c=json.loads((HERE/'contract.json').read_text())
freeze=json.loads((HERE/'freeze.json').read_text())
for name,digest in freeze['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
vendor=json.loads((HERE/'vendor_sources.json').read_text())
for name,digest in vendor['files'].items():assert hashlib.sha256((HERE/'vendor'/name).read_bytes()).hexdigest()==digest,name
indices=[];replayed=0;qualified=0;selected=0
for worker in range(c['workers']):
    execution=json.loads((HERE/f'results/worker-{worker}.json').read_text());assert execution['status']=='COMPLETE'
    for item in execution['records']:
        assert item['status']!='ERROR',item
        path=HERE/'results'/item['file'];assert hashlib.sha256(path.read_bytes()).hexdigest()==item['sha256']
        row=json.loads(gzip.decompress(path.read_bytes()));indices.append(row['index'])
        if not row['replicates']:continue
        selected+=1;packet=row['selection']['fourth']['packet']
        assert len(row['replicates'])==c['count_replicates']
        for rep in row['replicates']:
            observed=rep['observed'];saved=rep['inference']
            out=measurement(packet,observed['counts'],observed['overlaps'],c['count_density'],c['minimum_measurement_count'])
            for arm in ['four','baseline']:
                assert out[arm]['status']==saved[arm]['status']
                if out[arm]['status']!='WEIGHTS_VALID':continue
                np.testing.assert_allclose(out[arm]['weights'],saved[arm]['weights'],rtol=1e-10,atol=1e-9)
                assert out[arm]['order']==saved[arm]['order']
            if rep['replicate']==0 and out['four']['status']=='WEIGHTS_VALID':
                np.testing.assert_allclose(out['four']['weight_covariance'],saved['four']['weight_covariance'],rtol=1e-10,atol=1e-8)
                qualified+=int(out['four']['qualified'])
            assert all(observed['intersection_replay'])
            replayed+=1
assert sorted(indices)==list(range(c['clouds'])),indices
result=dict(status='PASS',scheduled_records=len(indices),selected=selected,replayed_count_replicates=replayed,
            qualified_primary=qualified,frozen_source_files=len(freeze['files']),vendor_files=len(vendor['files']))
(HERE/'record_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
