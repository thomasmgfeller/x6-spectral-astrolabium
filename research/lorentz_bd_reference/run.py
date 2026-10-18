"""Fixed-budget runner; requires a clean, committed source contract before data."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import time
import numpy as np
import scipy
from core import HERE, ROOT, contract, seed, sprinkle, counts, curvature, compile_kernel, forward_grid, physical_volume, truth
from analyze import group_result, gate
from continuum import mean_curvature

def dump(p, data):
    p.write_text(json.dumps(data, indent=2, allow_nan=False)+'\n')

def frozen(ref):
    result = {}
    for name in contract()['frozen_paths']:
        raw = (ROOT/name).read_bytes()
        if raw != subprocess.check_output(['git','show',ref+':'+name],cwd=ROOT):
            raise ValueError('source changed since freeze: '+name)
        result[name] = hashlib.sha256(raw).hexdigest()
    return result

def cell(out, split, lam, h, number, rho, start):
    c = contract()
    data = {k:[] for k in ['n','c2','bd','sample_seconds','count_seconds','c2_seconds','bd_seconds','coordinate_hash','interval_hash','proposed']}
    all_counts=[]
    for i in range(number):
        if time.perf_counter()-start > c['limits']['wall_seconds']:
            raise RuntimeError('wall budget exhausted')
        rng = np.random.default_rng(seed(f'{split}/{lam}/{h:.8f}/{i}'))
        a=time.perf_counter(); x, proposed=sprinkle(rng,rho,h); b=time.perf_counter()
        ns=counts(x); d=time.perf_counter()
        c2=int(ns.sum()); e=time.perf_counter()
        vals=[curvature(ns,rho,eps) for eps in c['epsilon_candidates']]; f=time.perf_counter()
        if len(x)<2:
            raise RuntimeError('N<2: no silent removal')
        record=dict(n=len(x),c2=c2,bd=vals,sample_seconds=b-a,count_seconds=d-b,c2_seconds=e-d,
            bd_seconds=f-e,coordinate_hash=hashlib.sha256(x.tobytes()).hexdigest(),
            interval_hash=hashlib.sha256(ns.tobytes()).hexdigest(),proposed=proposed)
        for key,value in record.items(): data[key].append(value)
        all_counts.append(ns)
    data={k:np.asarray(v) for k,v in data.items()}
    data['interval_counts']=np.concatenate(all_counts)
    data['offsets']=np.r_[0,np.cumsum(data['n'])]
    name=f'{split}-{lam}-{h:.2f}.npz'
    np.savez_compressed(out/name, **data)
    print(name, 'complete', flush=True)
    return data,name

def main():
    p=argparse.ArgumentParser(); p.add_argument('--source-ref',required=True); p.add_argument('--output',type=Path,required=True)
    args=p.parse_args(); c=contract(); sources=frozen(args.source_ref)
    args.output.mkdir(parents=True,exist_ok=False)
    resource.setrlimit(resource.RLIMIT_AS,(2*1024**3,2*1024**3))
    resource.setrlimit(resource.RLIMIT_CPU,(600,600))
    start=time.perf_counter(); cpu=time.process_time()
    dump(args.output/'execution.json',dict(status='RUNNING',source_ref=args.source_ref,source_hashes=sources,
        python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform(),
        compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],threads={k:os.environ.get(k) for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']}))
    compile_kernel(); forward_grid()
    setup=time.perf_counter()-start
    selected={}; dev=[]
    for lam in c['flat_expected_counts']:
        rho=lam/(np.pi/24)
        a,name=cell(args.output,'development',lam,0.,c['development_flat_clouds_per_density'],rho,start)
        mse=np.mean(a['bd'].reshape(-1,c['group_size'],len(c['epsilon_candidates'])).mean(axis=1)**2,axis=0)
        j=int(np.argmin(mse)); selected[str(lam)]=j
        dev.append(dict(flat_expected_count=lam,group_mse=mse.tolist(),chosen_epsilon=c['epsilon_candidates'][j],file=name))
    # Written before any test cloud; test selection cannot change this file.
    dump(args.output/'selection.json',dict(selected=selected,development=dev))
    rows=[]; controls=True
    for lam in c['flat_expected_counts']:
        rho=lam/(np.pi/24); j=selected[str(lam)]; eps=c['epsilon_candidates'][j]
        for h in c['test_h']:
            a,name=cell(args.output,'test',lam,h,c['test_clouds_per_cell'],rho,start)
            begun=time.perf_counter(); metrics=group_result(a['n'],a['c2'],a['bd'][:,j],h); analysis_seconds=time.perf_counter()-begun
            continuum=mean_curvature(h,rho,eps,64); higher=mean_curvature(h,rho,eps,96)
            se=a['bd'][:,j].std(ddof=1)/np.sqrt(len(a['n']))
            delta=abs(higher-continuum)
            mu=rho*physical_volume(h)
            poisson_ok=abs(a['n'].mean()-mu)<=5*np.sqrt(mu/len(a['n'])) and .6<a['n'].var(ddof=1)/mu<1.4
            continuum_ok=delta<1e-6 and abs(a['bd'][:,j].mean()-higher)<=5*se+delta
            controls &= bool(poisson_ok and continuum_ok)
            shared=float(np.sum(a['sample_seconds']+a['count_seconds']))
            # Charge BD all four candidate evaluations, a conservative upper bound;
            # C2 group inversion/interval analysis is reported separately below.
            c2time=shared+float(a['c2_seconds'].sum()); bdtime=shared+float(a['bd_seconds'].sum())
            row=dict(flat_expected_count=lam,h=h,rho=rho,expected_count=mu,truth=truth(h),epsilon=eps,file=name,
                n_mean=float(a['n'].mean()),n_variance=float(a['n'].var(ddof=1)),
                l=rho**(-.25),l_k=(eps*rho)**(-.25),metrics=metrics,
                continuum_mean=higher,continuum_order_difference=delta,continuum_bias=higher-truth(h),
                poisson_control=bool(poisson_ok),continuum_control=bool(continuum_ok),
                shared_seconds=shared,c2_total_seconds=c2time,bd_total_upper_seconds=bdtime,
                method_cost_ratio=bdtime/c2time,analysis_seconds=analysis_seconds)
            rows.append(row)
            dump(args.output/'partial-summary.json',rows)
    decision=gate(rows,controls)
    dump(args.output/'summary.json',dict(rows=rows,decision=decision))
    ex=json.loads((args.output/'execution.json').read_text())
    ex.update(status='COMPLETE',wall_seconds=time.perf_counter()-start,cpu_seconds=time.process_time()-cpu,
        setup_seconds=setup,peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
        development_clouds=len(c['flat_expected_counts'])*c['development_flat_clouds_per_density'],
        test_clouds=len(c['flat_expected_counts'])*len(c['test_h'])*c['test_clouds_per_cell'])
    dump(args.output/'execution.json',ex)
    dump(args.output/'hashes.json',{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.output.iterdir()) if p.is_file()})
    print(json.dumps(decision),flush=True)

if __name__=='__main__': main()
