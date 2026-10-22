"""Certified membership-atom lower volumes and unresolved-mass TV bound.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'conformal_transport'))
from ct_run import inputs,bounds,F,read,save,boosted,sqrt_bounds,outward
from pt_common import setup,UNIT as OLDUNIT,input_record
from sc_run import deform

def floor(q):return q.numerator//q.denominator
def ceil(q):return -((-q.numerator)//q.denominator)

def classify(lower,upper,lo,hi,ends):
    # Each coordinate magnitude <1e7: squared differences fit signed int64.
    assert max(np.max(abs(x)) for x in [lower,upper,lo,hi])<10**7
    fi=[];fo=[];pi=[];po=[]
    for a,b in zip(lo,hi):
        mind=np.maximum(0,np.maximum(a[1:]-upper[:,1:],lower[:,1:]-b[1:]))
        maxd=np.maximum(abs(lower[:,1:]-b[1:]),abs(upper[:,1:]-a[1:]))
        rmin=np.sum(mind*mind,axis=1);rmax=np.sum(maxd*maxd,axis=1)
        for dmin,dmax,inside,outside in [(lower[:,0]-b[0],upper[:,0]-a[0],fi,fo),
                                        (a[0]-upper[:,0],b[0]-lower[:,0],pi,po)]:
            inside.append((dmin>0)&(dmin*dmin>rmax))
            outside.append((dmax>0)&(dmax*dmax>=rmin))
    inner=np.array([fi[a]&pi[b] for a,b in ends]);outer=np.array([fo[a]&po[b] for a,b in ends])
    assert np.all(~inner|outer)
    known=np.all(inner==outer,axis=0)
    return known,np.packbits(inner.T,axis=1,bitorder='little')

def partition(z,ends,low,high,n,unit,chunk):
    lo=np.array([[floor(v*unit) for v in row] for row in z],dtype=np.int64)
    hi=np.array([[ceil(v*unit) for v in row] for row in z],dtype=np.int64)
    edges=[np.array([l+(h-l)*i//n for i in range(n+1)],dtype=np.int64) for l,h in zip(low,high)]
    assert all(np.all(np.diff(e)>0) for e in edges)
    atoms={};known_cells=0;total=0
    for start in range(0,n**3,chunk):
        ids=np.arange(start,min(start+chunk,n**3));idx=[ids//(n*n),(ids//n)%n,ids%n]
        lower=np.stack([e[i] for e,i in zip(edges,idx)],axis=1);upper=np.stack([e[i+1] for e,i in zip(edges,idx)],axis=1)
        volumes=np.prod(upper-lower,axis=1);total+=int(volumes.sum())
        known,labels=classify(lower,upper,lo,hi,ends);known_cells+=int(known.sum())
        keep=known&np.any(labels!=0,axis=1)
        if not np.any(keep):continue
        keys,inverse=np.unique(labels[keep],axis=0,return_inverse=True)
        weights=np.zeros(len(keys),dtype=np.int64);np.add.at(weights,inverse,volumes[keep])
        for key,volume in zip(keys,weights):
            label=bytes(key).hex();atoms[label]=atoms.get(label,0)+int(volume)
    assert total==math.prod(h-l for l,h in zip(low,high))<2**63
    return dict(cells=n**3,fully_classified_cells=known_cells,atom_integer_volumes=dict(sorted(atoms.items())),covered_nonzero_integer_volume=sum(atoms.values()))

def distance_upper(a,b):
    total=F(0)
    for key in a.keys()|b.keys():
        x=sqrt_bounds(a.get(key,F(0)));y=sqrt_bounds(b.get(key,F(0)))
        total+=max(abs(x[0]-y[1]),abs(x[1]-y[0]))**2
    return sqrt_bounds(total)[1]

def law_bound(a,b,total_upper):
    assert all(v>=0 for v in [*a.values(),*b.values()])
    residual=[total_upper-sum(v.values()) for v in [a,b]]
    assert min(residual)>=0
    delta=distance_upper(a,b);root=delta+sum(sqrt_bounds(v)[1] for v in residual)
    return dict(known_root_distance_upper=outward(delta)[1],unresolved_mean_upper=[outward(v)[1] for v in residual],
                root_hellinger_exponent_upper=outward(root)[1],tv_upper=outward(min(F(1),root))[1])

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z=inputs();old=read(HERE.parent/'shape_coupling'/'summary.json')['selected']
    zz=deform(z,old['node'],old['axis'],old['sign'],F(old['step']))
    packet,_,_=input_record(w['index']);lookup={v:i for i,v in enumerate(w['nodes'])}
    pairs=[(lookup[a],lookup[b]) for a,b in packet['pairs']];R=w['full_order'];ends=[(a,b) if R[a][b] else (b,a) for a,b in pairs]
    assert len(ends)==c['intervals'] and (3,0) in ends
    unit=c['coordinate_unit'];box=setup(0)
    low=[floor(F(int(v),OLDUNIT)*unit) for v in box['low']];high=[ceil(F(int(v),OLDUNIT)*unit) for v in box['high']]
    assert math.prod(h-l for l,h in zip(low,high))<2**63
    _,U,_=bounds(w,z);factor=F(w['rho'])*F(w['scale'])**3/unit**3
    records=[]
    for n in c['partition_levels']:
        volumes=[partition(boosted(g),ends,low,high,n,unit,c['chunk_size']) for g in [z,zz]]
        masses=[{k:factor*v for k,v in item['atom_integer_volumes'].items()} for item in volumes]
        certificate=law_bound(*masses,U[1])
        record=dict(level=n,geometries=volumes,bound=certificate);records.append(record)
        print(json.dumps(dict(level=n,known_atoms=[len(x) for x in masses],**certificate)),flush=True)
    best=min(F(r['bound']['tv_upper']) for r in records)
    summary=dict(status='ATOM_BOUND_CERTIFIED' if best<=F(c['tv_gate']) else 'HOLD_VOLUME_RESOLUTION',
       pair_unchanged=True,partition_levels=c['partition_levels'],cells_per_geometry=sum(n**3 for n in c['partition_levels']),
       best_atom_tv_upper=outward(best)[1],previous_coupling_tv_upper=old['tv_upper'],
       combined_best_tv_upper=outward(min(best,F(old['tv_upper'])))[1],
       final=records[-1]['bound'],expected_outer_population=outward(*U),
       equal_residual_requirement_at_zero_known_distance='each unresolved mean <=1/64 suffices for this TV <=1/4 bound',
       scope='Deterministic numerical feasibility bound for the unchanged PR95 pair, not a new geometry or an actual-TV lower bound. Unknown and unobserved membership patterns are retained via residual mass.')
    return records,summary

if __name__=='__main__':
    for name,data in zip(['partitions.json.gz','summary.json'],run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
