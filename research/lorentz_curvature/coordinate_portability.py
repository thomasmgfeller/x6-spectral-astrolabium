"""Supplementary CPU-dispatch check; never changes the frozen experiment.

Reconstruct original coordinates and require every archived byte hash. Then
disable AVX512F in a separate interpreter, compare every coordinate to that
reference, require the complete archived relation, and retain explicit hashes.
This is an after-run portability diagnostic, not new scientific evidence.
"""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
from geometry import sample, relation, require
from core import pack
from run import seed_for, source_hashes

HERE = Path(__file__).resolve().parent
TOLERANCE = 1e-14


def clouds():
    contract = json.loads((HERE/'contract.json').read_text())
    records = json.loads(gzip.decompress((HERE/'results/records.json.gz').read_bytes()))
    families = {f['id']: f for f in contract['families']}
    provenance = json.loads((HERE/'results/provenance.json').read_text())
    require(source_hashes(provenance['source_commit']) == provenance['source_sha256'], 'source pin')
    for row in records:
        seed = seed_for(row['id'], contract)
        x, proposed = sample(np.random.Generator(np.random.PCG64(seed)), row['N'], families[row['family']])
        require(proposed == row['proposed'], 'proposal count '+row['id'])
        require(pack(relation(x)) == row['relation'], 'relation '+row['id'])
        yield row, x


def variant(reference, output):
    original = np.load(reference, allow_pickle=False)
    hashes = {}
    offset = changed = 0
    max_abs = 0.
    for row, x in clouds():
        old = original[offset:offset+row['N']]
        require(hashlib.sha256(old.astype('<f8').tobytes()).hexdigest() == row['points_sha256'], 'reference hash')
        delta = float(np.max(np.abs(old-x)))
        require(delta <= TOLERANCE, 'coordinate tolerance '+row['id'])
        digest = hashlib.sha256(x.astype('<f8').tobytes()).hexdigest()
        if digest != row['points_sha256']:
            hashes[row['id']] = digest
            changed += 1
        max_abs = max(max_abs, delta)
        offset += row['N']
    require(offset == len(original), 'coordinate roster')
    data = dict(schema='X6-CURVATURE-COORDINATE-VARIANT-1',
                source_commit=json.loads((HERE/'results/provenance.json').read_text())['source_commit'],
                records_sha256=hashlib.sha256((HERE/'results/records.json.gz').read_bytes()).hexdigest(),
                variant_environment={'NPY_DISABLE_CPU_FEATURES':os.environ.get('NPY_DISABLE_CPU_FEATURES')},
                coordinate_absolute_tolerance=TOLERANCE, observed_max_absolute_difference=max_abs,
                clouds=offset//96, points=offset, changed_hashes=changed,
                full_relations_identical=True, hashes=hashes,
                scope='Supplementary post-run CPU-dispatch diagnostic; original sources and records unchanged')
    # Count clouds independently; N=64 and 128 each have the same case count.
    data['clouds'] = len(json.loads(gzip.decompress((HERE/'results/records.json.gz').read_bytes())))
    output.write_bytes(gzip.compress(json.dumps(data,sort_keys=True,separators=(',',':')).encode(),mtime=0))
    print(json.dumps({k:v for k,v in data.items() if k!='hashes'},indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output',type=Path)
    ap.add_argument('--reference',type=Path)
    args = ap.parse_args()
    require(not args.output.exists(), 'output must be new')
    if args.reference:
        variant(args.reference,args.output)
        return
    with tempfile.TemporaryDirectory(prefix='x6-coordinate-portability-') as tmp:
        points=[]
        for row,x in clouds():
            require(hashlib.sha256(x.astype('<f8').tobytes()).hexdigest()==row['points_sha256'],
                    'original coordinate bytes unavailable on this CPU; cannot mint a variant')
            points.append(x)
        reference=Path(tmp)/'original.npy'
        np.save(reference,np.concatenate(points),allow_pickle=False)
        subprocess.run([sys.executable,'-B',str(Path(__file__).resolve()),str(args.output),'--reference',str(reference)],
                       env=dict(os.environ,NPY_DISABLE_CPU_FEATURES='AVX512F',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1'),check=True)


if __name__=='__main__':main()
