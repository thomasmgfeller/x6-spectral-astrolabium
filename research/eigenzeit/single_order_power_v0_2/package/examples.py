"""Four fixed engineering runs. Redraws and an estimate of population power are excluded."""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import subprocess
import sys
import numpy as np
from scipy.spatial.distance import cdist
from apply_order import observed_count, matched_count, apply_packed
from decision import DESIGN, classify

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'source/research/lorentz_curvature'))
from geometry import flat_points

def seed(method,model,role):
    name=f"{DESIGN['seed_namespace']}/{method}/{model}/{role}"
    return int.from_bytes(hashlib.sha256(name.encode()).digest()[:16],'big')

def generate(n,h,rng):
    result=[];size=proposals=0
    while size<n:
        batch=max(128,2*(n-size))
        cloud=flat_points(rng,batch)
        if h:
            cloud=cloud[rng.random(batch)<=((1-h/2)/(1-h*cloud[:,0]))**4]
        take=cloud[:n-size];result.append(take);size+=len(take);proposals+=batch
    return np.concatenate(result),proposals

def crosscheck_all(cloud):
    # Each unordered pair counted once. SciPy Euclidean distance and linear delta-t
    # as an independent predicate, with no matrix reused from the C++ path.
    total=0;block=256
    for start in range(0,len(cloud),block):
        stop=min(start+block,len(cloud))
        left=cloud[start:stop];right=cloud[start:]
        distances=cdist(left[:,1:],right[:,1:],metric='euclidean')
        comparable=abs(left[:,None,0]-right[None,:,0])>distances
        nleft=len(left);total+=int(comparable[:,nleft:].sum())+int(np.triu(comparable[:,:nleft],1).sum())
    return total

def verify_matching_synthetic(path):
    # Sparse on-disk order. Selected links exercise both orientations of the query interface.
    n=DESIGN['matching']['n'];stride=n//8;fixed_seed=714514
    pairs=np.random.Generator(np.random.PCG64(fixed_seed)).permutation(n).reshape(-1,2)
    with path.open('wb') as f:f.truncate(n*stride)
    # For this control only the selected links are present. They form a disjoint union of
    # two-element chains and isolated nodes, itself a valid strict transitive closure.
    order=np.memmap(path,mode='r+',dtype=np.uint8,shape=(n,stride))
    forwards=np.arange(n//2)<128
    edges=pairs[forwards].copy();edges[::2]=edges[::2,::-1]
    a,b=edges.T;order[a,b//8]|=(1<<(b%8)).astype(np.uint8);order.flush();del order
    result=apply_packed(path,'matching',fixed_seed)
    if result['count']!=int(sum(forwards)):raise AssertionError('matching matrix entry point')
    path.unlink()

def main():
    out=[]
    with TemporaryDirectory() as directory:
        temp=Path(directory);exe=temp/'pack_relations'
        subprocess.run(['c++','-std=c++17','-O3','-ffp-contract=off',str(ROOT/'pack_relations.cpp'),'-o',str(exe)],check=True)
        verify_matching_synthetic(temp/'sparse.bin')
        for method in ('full_order','matching'):
            n=DESIGN[method]['n']
            for model in DESIGN['model_h']:
                h=0. if model=='0' else .5
                rng=np.random.Generator(np.random.PCG64(seed(method,model,'sample')))
                cloud,proposals=generate(n,h,rng)
                rng=np.random.Generator(np.random.PCG64(seed(method,model,'labels')))
                cloud=np.asarray(cloud[rng.permutation(n)],dtype='<f8')
                metadata={}
                if method=='full_order':
                    binary=temp/'relations.bin'
                    with binary.open('wb') as f:subprocess.run([str(exe),str(n)],input=cloud.tobytes(),stdout=f,check=True)
                    res=apply_packed(binary,method);count=res['count'];metadata['order_sha256']=res['order_sha256']
                    if count!=crosscheck_all(cloud):raise AssertionError('full-order independent recount')
                    binary.unlink()
                else:
                    pair_seed=seed(method,model,'matching')
                    def query(i,j):
                        delta=cloud[i]-cloud[j]
                        return delta[:,0]**2>np.einsum('ij,ij->i',delta[:,1:],delta[:,1:])
                    count,metadata['pairing_sha256']=matched_count(n,query,np.random.Generator(np.random.PCG64(pair_seed)))
                    pairs=np.random.Generator(np.random.PCG64(pair_seed)).permutation(n).reshape(-1,2)
                    delta=cloud[pairs[:,0]]-cloud[pairs[:,1]]
                    check=np.count_nonzero(abs(delta[:,0])>np.linalg.norm(delta[:,1:],axis=1))
                    if count!=check:raise AssertionError('matching independent recount')
                out.append(dict(method=method,h=model,n=n,count=count,compatible=classify(method,n,count),
                                proposals=proposals,coordinates_sha256=hashlib.sha256(cloud.tobytes()).hexdigest(),**metadata))
    return out

if __name__=='__main__':print(json.dumps(main(),indent=2))
