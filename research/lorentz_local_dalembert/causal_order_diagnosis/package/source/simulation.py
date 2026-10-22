"""Only this boundary sees simulator coordinates; inference receives relations."""
import gc
import hashlib
import sys
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent
BASE=HERE/'vendor/research/lorentz_local_dalembert'
sys.path.insert(0,str(BASE/'joint_feasibility'))
from jf_common import config,core,estimator,experiment,weighting,PhysicalPoset,shell,relation,digest
from joint import select,audit,Counts
from od_simulation import uniform_diamond
from selection import select_four

def selection_cloud(seed,contract):
    rho=contract['selection_density'];c,oc,guards,cfg=config()
    z,r,marks,bottom,top=experiment.sprinkle(rho,seed)
    ni=len(z);probes=[bottom,top]
    gi=core.Poset(r,marks)
    baseline=weighting.reweight(gi,estimator.neighborhood(gi,rho,bottom,top,cfg),rho,cfg['coefficient_C'])
    root,chain=baseline['root'],baseline['chain'];scale=baseline['tau_m']
    del gi,r
    colours=np.random.default_rng(seed^guards['colour_seed_xor']).integers(0,2,size=ni,dtype=np.uint8)
    for index,(lo,hi) in enumerate(zip(oc['outer_durations'][:-1],oc['outer_durations'][1:]),1):
        zz,mm,cc,_=shell(rho,seed,index,lo,hi,oc)
        z=np.vstack((z,zz));marks=np.r_[marks,mm];colours=np.r_[colours,cc]
    if len(z)>c['maximum_points']:raise MemoryError('A point budget')
    g=PhysicalPoset(relation(z,c['relation_block_rows']),marks,probes);g.probes_for_check=probes
    inner=[i for i in range(ni) if i not in probes]
    selected=select(g,root,chain,inner,probes,colours,rho,c,guards,scale)
    hidden=np.random.default_rng(np.random.SeedSequence([seed,c['audit_colour_seed_tag']])).integers(0,2,size=g.size,dtype=np.uint8)
    audited=audit(g,selected['selected'],hidden,rho,guards)
    fourth=select_four(g,Counts(g,colours,rho,guards),selected['selected'],contract['selection']) if audited['passed'] else dict(status='BASE_AUDIT_HOLD')
    record=dict(status=fourth['status'],fourth=fourth,base_audit=audited['passed'],
                physical_count=len(z)-2,coordinates_sha256=digest(z),relation_sha256=digest(g.r),
                baseline_selected=selected['selected'],
                base_selection_funnel=[{k:v for k,v in shell.items() if k!='trials'} for shell in selected['shells']])
    private=None
    if fourth['status']=='SELECTED':
        packet=fourth['packet'];ids=packet['landmarks']+[packet['root']]+packet['support']
        private=dict(ids=ids,points=z[ids].copy())
    del g;gc.collect()
    return record,private

def counting_cloud(private,packet,seed,replicate,contract):
    rng=np.random.default_rng(np.random.SeedSequence([seed,contract['count_seed_tag'],replicate]))
    rho=contract['count_density'];duration=contract['duration']
    n=int(rng.poisson(rho*np.pi/12*duration**3))
    if n>contract['maximum_count_points']:raise MemoryError('B point budget')
    z=uniform_diamond(n,duration,rng)
    p=private['points']
    dt=z[None,:,0]-p[:,None,0];dx=z[None,:,1]-p[:,None,1];dy=z[None,:,2]-p[:,None,2]
    future=(dt>0)&(dt*dt>dx*dx+dy*dy)
    past=(dt<0)&(dt*dt>dx*dx+dy*dy)
    lookup={a:i for i,a in enumerate(private['ids'])}
    order=np.asarray(packet['full_order'],bool)
    bits=[]
    for a,b in packet['pairs']:
        i,j=lookup[a],lookup[b]
        if order[j,i]:i,j=j,i
        if not order[i,j]:raise ValueError('noncausal counted interval')
        mask=future[i]&past[j]
        bits.append(int.from_bytes(np.packbits(mask,bitorder='little').tobytes(),'little'))
    counts=[b.bit_count() for b in bits];m=len(bits);overlap=np.empty((m,m),dtype=np.int64)
    for i in range(m):
        for j in range(i+1):overlap[i,j]=overlap[j,i]=(bits[i]&bits[j]).bit_count()
    # Independent sparse-set intersection replay for fixed positions.
    checks=[]
    for i,j in [(0,m-1),(m//3,m//2),(m//2,m//2)]:
        def indices(b):
            out=set()
            while b:
                low=b&-b;out.add(low.bit_length()-1);b^=low
            return out
        checks.append(len(indices(bits[i])&indices(bits[j]))==overlap[i,j])
    assert all(checks)
    return dict(counts=counts,overlaps=overlap,physical_count=n,coordinates_sha256=digest(z),
                interval_bits_sha256=hashlib.sha256(b''.join(b.to_bytes((n+7)//8,'little') for b in bits)).hexdigest(),
                intersection_replay=checks)
