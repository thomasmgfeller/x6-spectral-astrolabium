"""Verify the archived complete orders, independent counts, ranks, gates and source pins."""
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys
import numpy as np
from geometry import require
from core import unpack, validate, fit, score, summarize, assess
from run import source_hashes, seed_for

HERE=Path(__file__).resolve().parent


def compare(a,b,path='root'):
    if isinstance(a,dict):
        require(isinstance(b,dict) and a.keys()==b.keys(),path+' keys')
        for key in a: compare(a[key],b[key],path+'/'+key)
    elif isinstance(a,list):
        require(isinstance(b,list) and len(a)==len(b),path+' length')
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i))
    elif isinstance(a,float):
        require(isinstance(b,(float,int)) and math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-13),path+' float')
    else:require(a==b,path+' value')


def verify(output):
    hashes=json.loads((output/'hashes.json').read_text())
    require(set(hashes)=={'models.json','provenance.json','records.json.gz','resources.json','summary.json'},'archive inventory')
    for name,digest in hashes.items():
        require(hashlib.sha256((output/name).read_bytes()).hexdigest()==digest,'archive hash '+name)
    provenance=json.loads((output/'provenance.json').read_text())
    require(source_hashes(provenance['source_commit'])==provenance['source_sha256'],'source pin')
    contract=json.loads((HERE/'contract.json').read_text())
    records=json.loads(gzip.decompress((output/'records.json.gz').read_bytes()))
    expected=set()
    for n in contract['sizes']:
        for phase,total,families in [('train',contract['training_per_size'],contract['families'][:1]),('calibration',contract['calibration_per_size'],contract['families'][:1]),('test',contract['test_per_cell'],contract['families'])]:
            for family in families:
                expected.update(f'{phase}/N{n}/{family["id"]}/{i:04}' for i in range(total))
    ids=[r['id'] for r in records]
    require(len(ids)==len(set(ids)) and set(ids)==expected,'complete unique case roster')
    twins=corruptions=0
    for r in records:
        n=r['N'];c=unpack(r['relation'],n);validate(c)
        require(not np.any(np.tril(c)), 'archive must use increasing coordinate-time labels')
        inc,out=c.sum(axis=0,dtype=np.int64),c.sum(axis=1,dtype=np.int64)
        # Every 3-chain has one middle vertex; every 4-chain has one middle relation.
        counts=[int(inc.sum()),int(inc@out),int(np.sum(c*(inc[:,None]*out[None,:])))]
        f=r['features']
        require(counts==[f['C2'],f['C3'],f['C4']],'independent chain abundance identity')
        h=[1]*n
        for i in range(n):
            for j in np.flatnonzero(c[i]): h[int(j)]=max(h[int(j)],h[i]+1)
        require(max(h)==f['H'],'independent outgoing height DP')
        require([counts[k-2]/math.comb(n,k) for k in range(2,5)]==f['normalized'],'feature normalization')
        require(str(seed_for(r['id'],contract))==r['seed'],'seed binding')
        require(r['id'].split('/')[0]==r['phase'] and r['id'].split('/')[1]=='N'+str(n) and r['id'].split('/')[2]==r['family'],'metadata binding')
        if 'flat_density_twin' in r:
            require(r['family'].startswith('de_sitter_'),'unexpected twin')
            require(all(r['flat_density_twin'][key] for key in ['identical_full_relation','identical_features','identical_scores_and_decisions']),'twin failure')
            compare(r['flat_density_twin']['features'],r['features'],'twin features')
            compare(r['flat_density_twin']['assessment'],r['assessment'],'twin assessment')
            twins+=1
        control=r.get('relation_error_control')
        if control and control['witness'] is not None:
            i,j,k=control['witness'];require(c[i,j] and c[j,k] and c[i,k],'corruption witness')
            bad=c.copy();bad[i,k]=False
            try:validate(bad)
            except ValueError:corruptions+=1
            else:raise ValueError('corruption accepted')
    models=json.loads((output/'models.json').read_text())
    ranks=0
    for n in contract['sizes']:
        train=[r for r in records if r['N']==n and r['phase']=='train']
        cal=[r for r in records if r['N']==n and r['phase']=='calibration']
        model=fit(train)
        bank=dict(scores=[score(r['features'],model) for r in cal],heights=[r['features']['H'] for r in cal])
        compare(models[str(n)],dict(training=model,calibration=bank),'fitted model')
        for r in records:
            if r['N']!=n or r['phase']!='test':continue
            a=r['assessment'];q=score(r['features'],model);h=r['features']['H'];b=len(cal)
            require(a['joint_p']==(1+sum(v>=q for v in bank['scores']))/(b+1),'independent upper rank')
            require(a['height_p']==min(1.,2*(1+min(sum(v<=h for v in bank['heights']),sum(v>=h for v in bank['heights'])))/(b+1)),'independent height rank')
            compare(a,assess(r['features'],model,bank),'assessment');ranks+=2
    summary=json.loads((output/'summary.json').read_text())
    for key,value in summarize(records,contract).items():compare(summary[key],value,'summary/'+key)
    require(summary['unique_orders']==len(records) and summary['conformal_twin_checks']==twins and summary['relation_error_checks']==corruptions,'totals')
    resources=json.loads((output/'resources.json').read_text())
    require(resources['elapsed_seconds']<contract['resource_limit']['seconds'],'elapsed budget')
    require(resources['peak_rss_kib']*1024<=contract['resource_limit']['address_space_bytes'],'memory budget')
    return dict(status='PASS_ARCHIVED_EVIDENCE',orders=len(records),independent_chain_counts=3*len(records),rank_checks=ranks,
                conformal_twins=twins,relation_error_controls=corruptions,source_commit=provenance['source_commit'],external_replication=False)


if __name__=='__main__':
    print(json.dumps(verify(Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'results'),indent=2))
