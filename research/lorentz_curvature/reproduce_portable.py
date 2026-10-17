"""Strict scientific replay plus an explicitly verified coordinate hash variant.

The original reproduce.py stays frozen and demands original coordinate bytes.
This supplementary checker accepts ONLY the archived original hash or the
per-case hash from the independently bounded AVX512F-disabled diagnostic.
Unknown hashes, changed relations, seeds, proposals or decisions still fail.
"""
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from geometry import require
from verify import verify, compare

HERE=Path(__file__).resolve().parent


def coordinate_match(old,new,variants):
    require(old['id']==new['id'],'coordinate case identity')
    if old['points_sha256']==new['points_sha256']:
        return False
    require(variants.get(old['id'])==new['points_sha256'],'unrecognized coordinate hash '+old['id'])
    return True


def selftest():
    old={'id':'case','points_sha256':'original'}
    require(not coordinate_match(old,dict(old),{}),'original rejected')
    require(coordinate_match(old,{'id':'case','points_sha256':'bounded'},{'case':'bounded'}),'variant rejected')
    for new in [{'id':'case','points_sha256':'unknown'},{'id':'other','points_sha256':'original'}]:
        try:coordinate_match(old,new,{'case':'bounded'})
        except ValueError:pass
        else:raise ValueError('coordinate negative control accepted')
    try:compare({'relation':'AA=='},{'relation':'AQ=='},'relation negative control')
    except ValueError:pass
    else:raise ValueError('relation mutation accepted')


def main():
    selftest()
    original=HERE/'results'
    print(json.dumps(verify(original),indent=2),flush=True)
    v=json.loads(gzip.decompress((original/'coordinate-variant.json.gz').read_bytes()))
    require(v['schema']=='X6-CURVATURE-COORDINATE-VARIANT-1','variant schema')
    require(v['records_sha256']==hashlib.sha256((original/'records.json.gz').read_bytes()).hexdigest(),'variant archive binding')
    require(v['coordinate_absolute_tolerance']==1e-14 and v['observed_max_absolute_difference']<=1e-14,'variant coordinate bound')
    require(v['full_relations_identical'] is True,'variant relation certificate')
    provenance=json.loads((original/'provenance.json').read_text())
    require(v['source_commit']==provenance['source_commit'],'variant source pin')
    before=json.loads(gzip.decompress((original/'records.json.gz').read_bytes()))
    require(v['clouds']==len(before) and v['changed_hashes']==len(v['hashes']),'variant count')
    require(set(v['hashes'])<=set(row['id'] for row in before),'unknown variant case')
    with tempfile.TemporaryDirectory(prefix='x6-portable-curvature-') as tmp:
        fresh=Path(tmp)/'results'
        subprocess.run([sys.executable,'-B',str(HERE/'run.py'),str(fresh),'--source-commit',provenance['source_commit']],
                       env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),check=True)
        print(json.dumps(verify(fresh),indent=2),flush=True)
        for name in ['models.json','summary.json']:
            compare(json.loads((original/name).read_text()),json.loads((fresh/name).read_text()),name)
        after=json.loads(gzip.decompress((fresh/'records.json.gz').read_bytes()))
        require(len(before)==len(after),'record count')
        variant_count=0
        for old,new in zip(before,after):
            variant_count+=coordinate_match(old,new,v['hashes'])
            checked=copy.deepcopy(new)
            checked['points_sha256']=old['points_sha256']
            compare(old,checked,'all records/'+old['id'])
        compare(provenance['source_sha256'],json.loads((fresh/'provenance.json').read_text())['source_sha256'],'frozen sources')
    print(json.dumps(dict(status='PASS_PORTABLE_CURVATURE_REPLAY',records=len(before),
          original_coordinate_hashes=len(before)-variant_count,verified_variant_hashes=variant_count,
          variant_max_absolute_difference=v['observed_max_absolute_difference'],
          unknown_coordinate_hashes_accepted=0,negative_controls=3,
          scope='All original scientific checks retained; only explicitly bounded per-case coordinate hash variants accepted',
          strict_original_coordinate_replay=(variant_count==0),external_replication=False),indent=2))


if __name__=='__main__':main()
