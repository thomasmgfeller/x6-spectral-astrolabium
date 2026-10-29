"""Frozen-plan development pilot. All outputs remain diagnostics, including on success."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import signal
import sys
import time
import numpy as np
import scipy
from fields import fields, rms, NAMES
from scalar import HERE, protocol, digest, sprinkle, extend, probes, counts, apply, propagate, volume
from reference import evaluate, source_norm

SOURCES=['PROTOCOL.json','counts.cpp','fields.py','scalar.py','reference.py','run.py']
def write_json(path,value):
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def frozen():
    expected=json.loads((HERE/'FREEZE.json').read_text())['sha256']
    actual={n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in SOURCES}
    if expected!=actual: raise RuntimeError('HOLD: frozen pilot source mismatch')
def generate(out):
    c=protocol();clouds={};runs=[]
    for d,nu in enumerate(c['nu']):
        for i in range(c['realizations']):
            key=f'd{d}_r{i:02d}'
            record={'key':key,'density_index':d,'realization_index':i,'nu':nu,
                    'seed_entropy':[1,1,d,i,1,c['master_seed']]}
            try:
                x=sprinkle(d,i);clouds[key]=x
                record.update(N=len(x),coordinates_sha256=digest(x),status='GENERATED')
                if d in [0,3] and i<4:
                    y=extend(x,d,i);clouds[key+'_outer']=y
                    record.update(outer_N=len(y),outer_sha256=digest(y),outer_seed_entropy=[1,2,d,i,1,c['master_seed']])
            except RuntimeError as exc:record.update(status=str(exc))
            runs.append(record)
    np.savez_compressed(out/'clouds.npz',**clouds)
    write_json(out/'RUNS.json',runs)
    print(f'Generated {len(runs)} planned runs, {sum(len(v) for k,v in clouds.items() if not k.endswith("outer"))} inner points',flush=True)
def reference(out):
    clouds=np.load(out/'clouds.npz');pp=probes()[:28]
    keys=[k for k in clouds.files if not k.endswith('outer')]
    ns=[int(np.searchsorted(clouds[k][:,0],1,side='left')) for k in keys]
    query=np.concatenate([clouds[k][:n] for k,n in zip(keys,ns)]+[pp])
    results={};info=[]
    start=time.monotonic()
    for label,(n,dt) in zip(['coarse','fine'],protocol()['reference']['resolutions']):
        values,meta=evaluate(query,n,dt,progress=lambda s:print(s,flush=True))
        info.append(meta);offset=0
        for key,count in zip(keys,ns):
            v=np.full((len(clouds[key]),3),complex(np.nan,np.nan))
            v[:count]=values[offset:offset+count];offset+=count
            results[key+'_'+label]=v
        results['probes_'+label]=values[offset:]
    results['query']=query
    np.savez_compressed(out/'reference.npz',**results)
    write_json(out/'REFERENCE.json',{'method':'uncertified Fourier resolution comparison','resolutions':info,
        'source_normalization_A':source_norm()[0],'quad_reported_error_not_certified':source_norm()[1],
        'query_count':len(query),'elapsed_seconds':time.monotonic()-start,
        'probe_fine_minus_coarse_RMS_by_mass':rms(results['probes_fine']-results['probes_coarse']).tolist(),
        'reference_status':'REFERENCE_HOLD_NO_CERTIFIED_REMAINDER'})
def execute(out):
    cfg=protocol();clouds=np.load(out/'clouds.npz');ref=np.load(out/'reference.npz')
    runs=json.loads((out/'RUNS.json').read_text());p=probes();pp=p[:28]
    fp,bp=fields(p);shape=(4,16,3)
    operators=np.full(shape+(32,10),complex(np.nan,np.nan));prop=np.full(shape+(28,8),complex(np.nan,np.nan))
    residual=np.full(shape,np.nan);outer=np.full((8,3,32,10),complex(np.nan,np.nan))
    # Column meanings: 4 manufactured waves, 3 compact-source masses, unit-history response.
    masses=[1,1,1,1,0,1,2,1]
    started=time.monotonic();outer_index=0
    for rec in runs:
        d,i,key=rec['density_index'],rec['realization_index'],rec['key']
        if rec['status']!='GENERATED':continue
        start=time.monotonic()
        try:
            if time.monotonic()-started>cfg['wall_seconds_max']:raise RuntimeError('RESOURCE_HOLD: wall cap')
            x=clouds[key];rho=cfg['nu'][d]/volume(4)
            cc,pc=counts(x,p)
            rec.update(interval_counts_sha256=digest(cc),probe_counts_sha256=digest(pc))
            f,b=fields(x)
            history=np.column_stack([f[:,6:],ref[key+'_fine'],np.ones(len(x))])
            J=np.column_stack([b[:,6:]-f[:,6:],np.zeros((len(x),4))])
            Jp=np.column_stack([bp[:28,6:]-fp[:28,6:],np.zeros((28,4))])
            for ei,e in enumerate(cfg['epsilon']):
                operators[d,i,ei]=apply(pc,rho,e,f,fp)
                prop[d,i,ei],residual[d,i,ei]=propagate(cc,pc[:28],x,pp,rho,e,history,J,Jp,masses)
            if key+'_outer' in clouds:
                y=clouds[key+'_outer'];_,oc=counts(y,p,full=False);fy,_=fields(y)
                for ei,e in enumerate(cfg['epsilon']):outer[outer_index,ei]=apply(oc,rho,e,fy,fp)
                rec.update(outer_metric_index=outer_index,outer_probe_counts_sha256=digest(oc));outer_index+=1
            rec['status']='COMPUTED_DIAGNOSTIC'
        except (RuntimeError,ValueError,np.linalg.LinAlgError) as exc:
            rec['status']=str(exc)
        rec['elapsed_seconds']=time.monotonic()-start
        print(key,rec['status'],f"{rec['elapsed_seconds']:.2f}s",flush=True)
        write_json(out/'RUNS.json',runs)
    np.savez_compressed(out/'metrics.npz',operator=operators,propagation=prop,residual=residual,outer_operator=outer,probes=p,exact_phi=fp,exact_box=bp)
    write_json(out/'COMPUTE.json',{'elapsed_seconds':time.monotonic()-started,'peak_RSS_MiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'threads':{k:os.getenv(k) for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS']},'platform':platform.platform()})
    summarize(out)
def summarize(out):
    z=np.load(out/'metrics.npz');ref=np.load(out/'reference.npz');cfg=protocol()
    f,b=z['exact_phi'][:21],z['exact_box'][:21]
    denom=np.maximum(rms(f),rms(b));runs=json.loads((out/'RUNS.json').read_text())
    complete=all(r['status']=='COMPUTED_DIAGNOSTIC' for r in runs)
    cells=[]
    for d,nu in enumerate(cfg['nu']):
        for ei,e in enumerate(cfg['epsilon']):
            actual=z['operator'][d,:,ei,:21]
            err=(actual-b[None,:,:])/denom
            valid=bool(np.isfinite(err).all())
            row={'nu':nu,'epsilon':e,'ell_k_L0':float((e*nu/volume(4))**(-.25)),
                 'all_planned_runs_finite':valid}
            if valid:
                row['operator_normalized_RMSE_by_field']=rms(err.reshape(-1,10)).tolist()
                row['operator_normalized_mean_bias_RMS_by_field']=rms(np.mean(err,axis=0)).tolist()
                row['operator_normalized_sample_SD_RMS_by_field']=np.sqrt(np.mean(np.var(err,axis=0,ddof=1),axis=0)).tolist()
                row['maximum_field_RMSE']=max(row['operator_normalized_RMSE_by_field'])
                row['draft_tolerance_screen']='WITHIN_0.1' if row['maximum_field_RMSE']<=.1 else 'FAIL_TOLERANCE'
                target=z['exact_phi'][:28,6:]
                row['manufactured_propagation_relative_RMSE_by_k']=(rms((z['propagation'][d,:,ei,:,:4]-target).reshape(-1,4))/rms(target)).tolist()
                target=ref['probes_fine']
                row['compact_source_probe_relative_RMSE_by_mass']=(rms((z['propagation'][d,:,ei,:,4:7]-target).reshape(-1,3))/rms(target)).tolist()
                row['unit_history_response_max']=float(np.max(np.abs(z['propagation'][d,:,ei,:,7])))
                row['algebraic_backward_residual_max']=float(np.max(z['residual'][d,:,ei]))
            cells.append(row)
    boundary=[]
    for rec in runs:
        if 'outer_metric_index' not in rec:continue
        d,i,j=rec['density_index'],rec['realization_index'],rec['outer_metric_index']
        delta=z['outer_operator'][j]-z['operator'][d,i]
        boundary.append({'key':rec['key'],'normalized_inner_change_RMS_by_epsilon_and_field':(rms(delta[:,:21],axis=1)/denom).tolist()})
    write_json(out/'RESULTS.json',{'schema':'cspp.scalar-pilot.results/0.1','status':'HOLD',
        'reason':'development pilot; G1 independent qualification, continuum reference certificate and Cauchy adapter remain open',
        'planned_runs':64,'computed_runs':sum(r['status']=='COMPUTED_DIAGNOSTIC' for r in runs),
        'all_runs_computed':complete,'field_order':NAMES,'cells':cells,'paired_boundary':boundary,
        'confirmation_seed_used':False,'Dirac_run':False,'flavor_run':False})
def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['freeze','generate','reference','run','summarize','all']);ap.add_argument('--out',type=Path,default=HERE/'results');a=ap.parse_args()
    if a.phase=='freeze':
        path=HERE/'FREEZE.json'
        if path.exists():raise SystemExit('Refuse to replace existing pilot freeze')
        write_json(path,{'scope':'development pilot source lock; NOT E4 confirmation freeze','UTC':datetime.now(timezone.utc).isoformat(),
            'sha256':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in SOURCES}})
        return
    frozen();a.out.mkdir(parents=True,exist_ok=True)
    if np.__version__!='2.3.5' or scipy.__version__!='1.17.0':
        raise RuntimeError('Use the declared numpy 2.3.5 and scipy 1.17.0 environment')
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
    signal.alarm(protocol()['wall_seconds_max'])
    if a.phase in ['generate','all']:generate(a.out)
    if a.phase in ['reference','all']:reference(a.out)
    if a.phase in ['run','all']:execute(a.out)
    if a.phase=='summarize':summarize(a.out)
if __name__=='__main__':main()
