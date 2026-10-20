"""Independent physical clouds. Operator inference precedes truth/field evaluation."""
import argparse,gc,hashlib,json,resource,signal,sys,time
from pathlib import Path
import numpy as np
import scipy
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sys.path.insert(0,str(BASE/'joint_feasibility'))
from jf_common import config,sources,encode,digest
from run_joint import run_cloud
from od_simulation import shell
sys.path.insert(0,str(BASE/'moment_feasibility'))
from feasibility import design,solve
from variance_weights import minimum_variance


def coordinates_only(rho,seed,oc):
    # Exact sampler replay without constructing a second relation matrix.
    rng=np.random.default_rng(seed);size=rng.poisson(rho*np.pi/12)
    hw=.5*rng.random(size)**(1/3)
    t=(.5-hw)*rng.choice([-1,1],size)
    radius=hw*np.sqrt(rng.random(size));angle=2*np.pi*rng.random(size)
    z=np.vstack(([-.5,0,0],np.column_stack((t,radius*np.cos(angle),radius*np.sin(angle))),[.5,0,0]))
    for index,(lo,hi) in enumerate(zip(oc['outer_durations'][:-1],oc['outer_durations'][1:]),1):
        zz,_,_,_=shell(rho,seed,index,lo,hi,oc);z=np.vstack((z,zz))
    return z


def evaluate(row,z,c,lpcontract,coefficient):
    if not row['joint_pass']: return dict(status='NO_GUARDED_SUPPORT')
    w=row['selection']['selected'];cert=w['certificate'];s=w['scale'];root=w['root']
    counts={tuple(sorted(p)):n for p,n in zip(cert['interval_pairs'],cert['interval_counts'])}
    mask=np.array([b in w['temporal'] for b in w['support']]);a0=[]
    for b,temp in zip(w['support'],mask):
        q=(counts[tuple(sorted((root,b)))]/(row['rho']*np.pi/12))**(2/3)
        population=next((len(side) for side in w['support_sides'] if b in side),None)
        a0.append((-(coefficient+3) if temp else coefficient/population)*s*s/q)
    a0=np.array(a0);d=design(np.array(cert['features'])/s)
    lp=solve(d,a0,mask,'unrestricted',lpcontract)
    signed_lp=solve(d,a0,mask,'free_time',lpcontract)
    qp=minimum_variance(d)
    signed_qp=minimum_variance(d,signed_lp['weights'],mask) if signed_lp['status']=='FEASIBLE' else None
    out=dict(status='WEIGHTS_UNRESOLVED',design=d,baseline=a0,temporal_mask=mask,
             lp=lp,qp=qp,signed_lp=signed_lp,signed_qp=signed_qp)
    if lp['status']!='FEASIBLE' or qp['status']!='VERIFIED':return out
    # No true coordinates/field values are read until all weights are sealed.
    weights=np.array([a0,lp['weights'],qp['weights']]);seal=hashlib.sha256(weights.tobytes()).hexdigest()
    delta=z[w['support']]-z[root]
    field=np.exp(delta[:,0]/2)*np.cos(delta[:,1]/2)*np.cos(delta[:,2]/2)
    clean=weights@(field-1)/(s*s)
    rng=np.random.default_rng(np.random.SeedSequence([row['seed'],823731]))
    noise=rng.normal(scale=c['field_noise_sigma'],size=len(field)+1)
    noisy=weights@(field-1+noise[1:]-noise[0])/(s*s)
    full=np.column_stack((-weights.sum(axis=1),weights))/(s*s)
    out.update(status='COMPLETE',scale=s,weights=weights,weights_seal=seal,truth=-.75,
               clean=clean,observed=noisy,conditional_field_covariance=c['field_noise_sigma']**2*(full@full.T),
               actual_support_extent=[float(np.max(np.abs(delta[:,0]))),float(np.max(np.linalg.norm(delta[:,1:],axis=1)))])
    assert hashlib.sha256(weights.tobytes()).hexdigest()==seal
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('--split',choices=['calibration','test'],required=True)
    args=p.parse_args();c=json.loads((HERE/'calibration_contract.json').read_text())
    destination=HERE/('independent_'+args.split)
    if destination.exists():raise SystemExit('Refusing to overwrite evidence')
    jf,oc,guards,cfg=config();lpcontract=json.loads((BASE/'moment_feasibility/contract.json').read_text())
    bound=sources()
    for f in ['run_calibration.py','variance_weights.py','calibration_contract.json','CALIBRATION_PROTOCOL.md']:
        bound[str((HERE/f).relative_to(HERE.parents[2]))]=hashlib.sha256((HERE/f).read_bytes()).hexdigest()
    for f in ['feasibility.py','contract.json']:
        path=BASE/'moment_feasibility'/f;bound[str(path.relative_to(HERE.parents[2]))]=hashlib.sha256(path.read_bytes()).hexdigest()
    destination.mkdir();run=dict(split=args.split,contract=c,source_sha256=bound,numpy=np.__version__,scipy=scipy.__version__,status='RUNNING',records=[])
    def save(): (destination/'execution.json').write_text(json.dumps(run,indent=2)+'\n')
    save();start=time.monotonic()
    def timeout(*args):raise TimeoutError('declared time budget')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(c['wall_budget_seconds_per_split'])
    try:
        lo,hi=c[args.split+'_seeds']
        for seed in range(lo,hi+1):
            row=run_cloud(c['rho'],seed,jf,oc,guards,cfg)
            z=coordinates_only(c['rho'],seed,oc)
            assert digest(z)==row['coordinates_sha256'],'sampler replay mismatch'
            row['operator']=evaluate(row,z,c,lpcontract,cfg['coefficient_C'])
            name=f'seed-{seed}.json';data=encode(row);(destination/name).write_text(data)
            run['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()))
            save();print(json.dumps(dict(seed=seed,status=row['operator']['status'],seconds=round(row['seconds'],2))),flush=True)
            del row,z;gc.collect()
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024>c['memory_budget_mib']:raise MemoryError('declared RSS budget')
        run['status']='COMPLETE'
    except Exception as error:
        run.update(status='HOLD',reason=repr(error));raise
    finally:
        signal.alarm(0);run.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024);save()

if __name__=='__main__':main()
