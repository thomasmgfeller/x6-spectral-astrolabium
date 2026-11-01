"""Apply either certified procedure to the strict, bit-packed relation of one order."""
import argparse
import hashlib
import json
import secrets
from pathlib import Path
import numpy as np
from decision import DESIGN, classify

def observed_count(stream,n):
    stride=(n+7)//8;count=0;digest=hashlib.sha256()
    for i in range(n):
        row=stream.read(stride)
        if len(row)!=stride or row[i//8]&(1<<(i%8)):
            raise ValueError('missing row or nonzero diagonal')
        if n%8 and row[-1]>>(n%8):
            raise ValueError('nonzero padding bits')
        digest.update(row)
        count+=int.from_bytes(row,'little').bit_count()
    if stream.read(1):raise ValueError('trailing bytes')
    return count,digest.hexdigest()

def matched_count(n,relation_query,rng):
    pairs=rng.permutation(n).reshape(-1,2)
    values=np.asarray(relation_query(pairs[:,0],pairs[:,1]))
    if values.shape!=(n//2,) or values.dtype!=bool:raise ValueError('bad pair-query results')
    return int(values.sum()),hashlib.sha256(pairs.astype('<i8').tobytes()).hexdigest()

def apply_packed(path,method,seed=None):
    n=DESIGN[method]['n'];stride=(n+7)//8
    if path.stat().st_size!=n*stride:raise ValueError('packed-order size differs from design')
    if method=='full_order':
        with path.open('rb') as stream:count,sha=observed_count(stream,n)
        metadata={'order_sha256':sha}
    else:
        if seed is None:seed=secrets.randbits(128)
        order=np.memmap(path,dtype=np.uint8,mode='r',shape=(n,stride))
        def relation_query(i,j):
            ij=(order[i,j//8]>>(j%8))&1
            ji=(order[j,i//8]>>(i%8))&1
            if np.any(ij & ji):raise ValueError('queried pair violates asymmetry')
            return (ij|ji).astype(bool)
        count,sha=matched_count(n,relation_query,np.random.Generator(np.random.PCG64(seed)))
        metadata={'matching_seed':str(seed),'pairing_sha256':sha}
    return dict(method=method,n=n,count=count,compatible=classify(method,n,count),**metadata)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('method',choices=['full_order','matching'])
    p.add_argument('path',type=Path)
    p.add_argument('--seed',type=int,help='For independent replay of the randomized matching only')
    a=p.parse_args();print(json.dumps(apply_packed(a.path,a.method,a.seed),indent=2))
