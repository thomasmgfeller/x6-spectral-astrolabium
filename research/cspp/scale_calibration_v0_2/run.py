"""Execute predeclared calibration; old pilot data and conclusions remain immutable."""
import argparse
from datetime import datetime,timezone
import json
from pathlib import Path
import platform
import resource
import signal
import time
import numpy as np
import scipy
from common import HERE,OLD,old,load,plan,sha,digest,write,cloud,gaussian_fields,exact_box
from mean_operator import integral,tail_bounds
from green_reference import evaluate as green
from fourier_nodes import evaluate as fourier

SOURCES=['PROTOCOL.json','common.py','mean_operator.py','green_reference.py','fourier_nodes.py','run.py']
DEPENDENCIES=['scalar.py','counts.cpp','reference.py','prepare_reference.py','results/REFERENCE_ARCHIVE.json']
def frozen():
    lock=json.loads((HERE/'FREEZE.json').read_text())
    if lock['sources']!={f:sha(HERE/f) for f in SOURCES}:raise RuntimeError('HOLD: changed calibration sources')
    if lock['dependencies']!={f:sha(OLD/f) for f in DEPENDENCIES}:raise RuntimeError('HOLD: changed frozen dependency')
def mean_scan(out):
    cfg=plan()['mean_scan'];rows=[];values=[];start=time.monotonic()
    for L in cfg['L']:
        for H in cfg['H']:
            for ell in cfg['ell_k']:
                vals=np.array([integral(ell,H,L,n,cfg['y_cutoff']) for n in cfg['quadrature_orders']])
                diff=float(np.max(np.abs(vals[-1]-vals[-2])/np.abs(exact_box(L))))
                rows.append({'L':L,'H':H,'ell_k':ell,'last_resolution_relative_max':diff,
                    'resolution_screen':'WITHIN_GOAL' if diff<=cfg['relative_last_resolution_goal'] else 'QUADRATURE_HOLD',
                    **tail_bounds(ell,H,L,cfg['y_cutoff'])})
                values.append(vals)
    np.savez_compressed(out/'mean.npz',values=np.array(values))
    write(out/'MEAN.json',{'rows':rows,'orders':cfg['quadrature_orders'],'elapsed_seconds':time.monotonic()-start,
                         'claim':'exact expectation formula; resolution checks and analytic truncation bounds do not certify numerical quadrature'})
    print('mean scan complete',flush=True)
def sprinklings(out):
    cfg=plan();records=[];estimates=np.full((3,16,3,3,4),complex(np.nan,np.nan))
    started=time.monotonic();p=np.zeros((1,4))
    for d,nu in enumerate(cfg['nu_equivalent_Omega4']):
        for batch in range(2):
            archive={}
            for i in range(batch*8,(batch+1)*8):
                key=f'd{d}_r{i:02d}';start=time.monotonic()
                rec={'key':key,'density_index':d,'realization_index':i,'nu_equivalent_Omega4':nu,
                     'seed_entropy':[1,3,d,i,1,cfg['master_seed']]}
                try:
                    x=cloud(d,i);archive[key]=x
                    _,pc=old.counts(x,p,full=False);n=pc[0]
                    if np.any(n<0):raise RuntimeError('GEOMETRY_HOLD: sampled point not in probe past')
                    rho=nu/old.volume(4);f=gaussian_fields(x,cfg['field_L_for_sprinkling'])
                    nested=[]
                    for hi,H in enumerate(cfg['nested_domains_H']):
                        keep=-x[:,0]+np.linalg.norm(x[:,1:],axis=1)<H;nested.append(int(np.sum(keep)))
                        for ei,ell in enumerate(cfg['fixed_ell_k']):
                            e=ell**-4/rho
                            estimates[d,i,hi,ei]=old.apply(n[keep][None,:],rho,e,f[keep],np.ones((1,4)))[0]
                    rec.update(status='COMPUTED_DIAGNOSTIC',N=len(x),nested_N=nested,cloud_sha256=digest(x),counts_sha256=digest(n))
                except (RuntimeError,ValueError,MemoryError) as exc:rec.update(status=str(exc))
                rec['elapsed_seconds']=time.monotonic()-start;records.append(rec)
                write(out/'RUNS.json',records);print(key,rec['status'],flush=True)
            np.savez_compressed(out/f'clouds_d{d}_b{batch}.npz',**archive)
    np.savez_compressed(out/'sprinklings.npz',values=estimates)
    write(out/'SPRINKLING_COMPUTE.json',{'elapsed_seconds':time.monotonic()-started})
def source_reference(out):
    cfg=plan()['source_reference'];load('cspp_prepare_v01',OLD/'prepare_reference.py').prepare()
    ref=np.load(OLD/'results/reference.npz');pp=old.probes()[:28]
    indices=np.linspace(0,len(ref['query'])-1,256,dtype=int)
    query=np.concatenate([pp,ref['query'][indices]])
    start=time.monotonic();values=[]
    for n in cfg['Gauss_orders']:
        values.append(green(query,n));print('Green reference order',n,'complete',flush=True)
    ff=[];meta=[]
    for n in cfg['Fourier_N']:
        v,m=fourier(pp,n,cfg['Fourier_box_length']);ff.append(v);meta.append(m)
        print('exact-node Fourier N',n,'complete',flush=True)
    oldqueries=[]
    for label in ['coarse','fine']:
        array=np.concatenate([ref[f'd{d}_r{i:02d}_{label}'][np.isfinite(ref[f'd{d}_r{i:02d}_{label}'][:,0])] for d in range(4) for i in range(16)]+[ref['probes_'+label]])
        oldqueries.append(np.concatenate([ref['probes_'+label],array[indices]]))
    np.savez_compressed(out/'source.npz',query=query,old_query_indices=indices,green=np.array(values),fourier=np.array(ff),old_reference=np.array(oldqueries))
    write(out/'SOURCE.json',{'elapsed_seconds':time.monotonic()-start,'Gauss_orders':cfg['Gauss_orders'],'Fourier':meta,
        'query_count':len(query),'primary_count':28,'reference_status':'HOLD_NO_VALIDATED_REMAINDER'})
def summary(out):
    cfg=plan();means=np.load(out/'mean.npz')['values'][:,-1]
    mrows=json.loads((out/'MEAN.json').read_text())['rows']
    lookup={(r['L'],r['H'],r['ell_k']):i for i,r in enumerate(mrows)}
    raw=np.load(out/'sprinklings.npz')['values'];records=json.loads((out/'RUNS.json').read_text())
    cells=[];truth=exact_box(2.);denom=np.abs(truth)
    for d,nu in enumerate(cfg['nu_equivalent_Omega4']):
        for hi,H in enumerate(cfg['nested_domains_H']):
            for ei,ell in enumerate(cfg['fixed_ell_k']):
                v=raw[d,:,hi,ei];mu=means[lookup[(2,H,ell)]];mu64=means[lookup[(2,64,ell)]]
                r={'nu_equivalent_Omega4':nu,'H':H,'ell_k':ell,'epsilon':ell**-4/(nu/old.volume(4)),
                   'all_16_finite':bool(np.isfinite(v).all())}
                if r['all_16_finite']:
                    empirical=np.mean(v,axis=0);sd=np.std(v,axis=0,ddof=1)
                    r.update(relative_RMSE=(np.sqrt(np.mean(np.abs(v-truth)**2,axis=0))/denom).tolist(),
                        relative_sample_SD=(sd/denom).tolist(),relative_mean_minus_exact_expectation=(np.abs(empirical-mu)/denom).tolist(),
                        relative_mean_standard_error_descriptive=(sd/4/denom).tolist(),
                        relative_nonlocal_bias_at_H64=(np.abs(mu64-truth)/denom).tolist(),
                        relative_finite_domain_shift=(np.abs(mu-mu64)/denom).tolist(),
                        relative_exact_mean_bias=(np.abs(mu-truth)/denom).tolist())
                cells.append(r)
    src=np.load(out/'source.npz');gg=src['green'];ff=src['fourier'];oldv=src['old_reference'];target=gg[-1,:28]
    rms=lambda a:np.sqrt(np.mean(np.abs(a)**2,axis=0))
    source={'primary_green_last_order_relative_RMS':(rms(gg[-1,:28]-gg[-2,:28])/rms(target)).tolist(),
            'all_query_green_last_order_relative_RMS':(rms(gg[-1]-gg[-2])/rms(gg[-1])).tolist(),
            'old_Fourier_relative_RMS_vs_Green_by_resolution':[(rms(v[:28]-target)/rms(target)).tolist() for v in oldv],
            'new_Fourier_relative_RMS_vs_Green_by_resolution':[(rms(v-target)/rms(target)).tolist() for v in ff],
            'local_amplitude_check_not_detector_trace_budget':True,'reference_status':'HOLD_NO_VALIDATED_REMAINDER'}
    write(out/'RESULTS.json',{'schema':'cspp.scale-calibration.results/0.2','scientific_status':'HOLD',
          'planned_runs':48,'computed_runs':sum(r['status']=='COMPUTED_DIAGNOSTIC' for r in records),'cells':cells,'source_reference':source,
          'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN','confirmation_seed_used':False})
def main():
    ap=argparse.ArgumentParser();ap.add_argument('phase',choices=['freeze','mean','sprinklings','source','summary','all']);ap.add_argument('--out',type=Path,default=HERE/'results');a=ap.parse_args()
    if a.phase=='freeze':
        if (HERE/'FREEZE.json').exists():raise SystemExit('Do not replace source lock')
        write(HERE/'FREEZE.json',{'UTC':datetime.now(timezone.utc).isoformat(),'scope':'development calibration source lock, not E4 confirmation',
            'sources':{f:sha(HERE/f) for f in SOURCES},'dependencies':{f:sha(OLD/f) for f in DEPENDENCIES}});return
    frozen();a.out.mkdir(parents=True,exist_ok=True)
    if np.__version__!='2.3.5' or scipy.__version__!='1.17.0':raise RuntimeError('pinned numpy/scipy versions required')
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3));signal.alarm(plan()['wall_seconds_max']);start=time.monotonic()
    if a.phase in ['mean','all']:mean_scan(a.out)
    if a.phase in ['sprinklings','all']:sprinklings(a.out)
    if a.phase in ['source','all']:source_reference(a.out)
    if a.phase in ['summary','all']:summary(a.out)
    write(a.out/'COMPUTE.json',{'phase':a.phase,'elapsed_seconds':time.monotonic()-start,'peak_RSS_MiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'workers':1})
if __name__=='__main__':main()
