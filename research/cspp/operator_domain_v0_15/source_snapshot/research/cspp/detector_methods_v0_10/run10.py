"""Fixed archived-data method comparison. No new sampling, no population claim."""
import argparse
import datetime
import json
import os
import resource
import time
import numpy as np
from common10 import HERE, PREVIOUS, previous, arb, acb, ctx, check, plan, pack, unpack, gzwrite, gzread, write, sha, digest, freeze_check
from time_integral import integrate
from adapter import constants, history_bounds, support_hits, transfer_bound
from detector import wave_reference


def forward(x,counts,A):
    data=previous.initial_data;prop=previous.propagation;p=plan()
    nh=int(np.searchsorted(x[:,0],-1,side='right'))
    check(nh>0,'original history exists')
    hf=np.column_stack([data.float_wave_history(x[:nh],k,1) for k in [0,2,4,8]]+
                       [data.float_bump_history(x[:nh],1,o,float(A.mid())) for o in [1,3]])
    history=[]
    for i,point in enumerate(x[:nh]):
        waves=[data.wave(point,k) for k in [0,2,4,8]]
        jets=data.bump_jets(point,1,A)
        h=[data.extension(point,w[1:],1) for w in waves]+[data.extension(point,jets,o) for o in [1,3]]
        history.append(h+[acb(complex(z)) for z in hf[i]]+[w[0] for w in waves])
    _,values,_,edges,_=prop.solve(counts,np.empty((0,len(x)),dtype=np.int32),512,'1/16',1,history,nh)
    table=prop.coefficient_table(len(x),512,'1/16',1)
    numeric=np.empty((len(x),6),dtype=complex);numeric[:nh]=hf
    for i in range(nh,len(x)):
        js=np.array([j for j,w in edges[i]],dtype=int);ws=np.array([float(w.mid()) for j,w in edges[i]])
        numeric[i]=ws@numeric[js] if len(js) else 0
    check(np.isfinite(numeric).all(),'finite float comparison')
    scales=[arb(1)]*4+[A/arb(1).exp()]*2
    maximum=max(w.abs_upper() for w in table);errors=[]
    for f in range(6):
        er=maximum*sum((v[f+6]-v[f]).abs_upper() for v in values)/scales[f]
        es=maximum*sum((acb(complex(z[f]))-v[f+6]).abs_upper() for z,v in zip(numeric,values))/scales[f]
        nr=max(max(v[f].real.rad(),v[f].imag.rad()) for v in values)/scales[f]
        errors.append({'input_rounding':pack(er),'float_nodal_solve':pack(es),'node_radius':pack(nr)})
    return history,values,edges,table,scales,errors


def evaluate(q,history,values,edges):
    t=list(q)
    for i in range(len(t)-1,len(history)-1,-1):
        for j,w in edges[i]:t[j]+=t[i]*w
    t=t[:len(history)]
    output=[]
    for f in list(range(6))+list(range(12,16)):
        a=sum(w*v[f] for w,v in zip(q,values));b=sum(w*h[f] for w,h in zip(t,history))
        check(a.overlaps(b),'forward/adjoint agreement')
        output.append(acb(a.real.intersection(b.real),a.imag.intersection(b.imag)))
    return output,t


def summarize(rows):
    p=plan();complete=[r for r in rows if r['status']=='COMPLETE']
    passed=sum(sum(w['field_pass']) for r in complete for w in r['levels'][-1]['windows'])
    hpassed=sum(sum(w['adapter_bound_pass']) for r in complete for w in r['levels'][-1]['windows'])
    decision='RESOURCE_HOLD' if len(complete)!=8 else 'NUMERIC_HOLD' if not all(r['numeric_pass'] for r in complete) else 'METHOD_HOLD' if passed!=96 or hpassed!=32 else 'DEVELOPMENT_BUDGETS_ONLY'
    return {'decision':decision,'completed_clouds':len(complete),'planned_clouds':8,
            'integration_pass':passed,'integration_total':96,'original_H1_integration_pass':sum(sum(w['field_pass'][:5]) for r in complete for w in r['levels'][-1]['windows']),
            'original_H1_total':80,'adapter_upper_bound_pass':hpassed,'adapter_upper_bound_total':32,
            'source_empty_clouds':[r['key'] for r in complete if r['source_support_hits']==0],
            'fresh_confirmation':'NOT_RUN','G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN',
            'physical_noise':'NOT_ESTABLISHED','predictive_covariance':'NOT_QUALIFIED'}


def compute(bits,out):
    freeze_check();p=plan();ctx.prec=bits
    start=time.monotonic();stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
    archive=np.load(HERE.parent/'scalar_pilot_v0_1/results/clouds.npz')
    A=previous.initial_data.source.normalization(bits)[0];cs=constants();rows=[]
    old=gzread(PREVIOUS/'results'/f'BENCHMARK_{bits}.json.gz')
    for key in p['clouds']:
        if time.monotonic()-start>p['resources']['wall_seconds_per_process']:
            rows.append({'key':key,'status':'RESOURCE_HOLD'});continue
        original=archive[key]
        if len(original)>p['resources']['max_points_per_cloud']:
            rows.append({'key':key,'status':'RESOURCE_HOLD'});continue
        cc,pc,relations,qr,stats=previous.geometry.inventory(original,np.array([[.875,0,0,1.5],[1.125,0,0,1.5]]))
        membership,_=previous.geometry.region(original,4);check(np.all(membership),'exact original Omega4 membership')
        n=int(np.searchsorted(original[:,0],1.25,side='left'));x=original[:n];counts=cc[:n,:n]
        history,values,edges,table,scales,errors=forward(x,counts,A);nh=len(history)
        hb={o:history_bounds(x[:nh],o,cs[o]) for o in [1,3]}
        try:
            levels=integrate(x,counts,table,p['time_windows'],p['spatial_grids'],lambda g:print(key,bits,'grid',g,flush=True),
                             deadline=start+p['resources']['wall_seconds_per_process'])
        except (TimeoutError,MemoryError) as e:
            rows.append({'key':key,'status':'RESOURCE_HOLD','reason':type(e).__name__});continue
        saved=[];last=None
        oldrow=next(r for r in old['rows'] if r['key']==key)
        for level in levels:
            windows=[]
            for wi,q in enumerate(level['q']):
                z,t=evaluate(q,history,values,edges)
                if last is not None:
                    z=[acb(v.real.intersection(u.real),v.imag.intersection(u.imag)) for v,u in zip(z,last[wi])]
                radii=[max(v.real.rad(),v.imag.rad())/s for v,s in zip(z[:6],scales)]
                bounds=[transfer_bound(t,hb[o]) for o in [1,3]]
                refs=[wave_reference(k,p['time_windows'][wi]) for k in [0,2,4,8]]
                for f in range(5):check(z[f].overlaps(unpack(oldrow['windows'][wi]['values'][f])),'independent v0.9 integral overlap')
                windows.append({'values':[pack(v) for v in z[:6]],'oracle_waves':[pack(v) for v in z[6:]],
                    'continuum_waves':[pack(v) for v in refs],
                    'wave_history_effect':[pack(z[k]-z[6+k]) for k in range(4)],
                    'wave_operator_domain_effect':[pack(z[6+k]-refs[k]) for k in range(4)],
                    'normalized_radii_upper':[float(v.upper()) for v in radii],
                    'field_pass':[bool(v<=arb(p['integration_tolerance'])) for v in radii],
                    'history_transfer':[pack(v) for v in t],
                    'adapter_normalized_error_upper':[pack(v) for v in bounds],
                    'adapter_bound_pass':[bool(v<=arb(p['adapter_tolerance'])) for v in bounds],
                    'query_coefficients':[pack(v) for v in q]})
            last=[[unpack(v) for v in w['values']+w['oracle_waves']] for w in windows]
            saved.append({k:v for k,v in level.items() if k!='q'}|{'windows':windows})
        numeric=all(unpack(e['node_radius']).real<=arb('1e-18') and unpack(e['input_rounding']).real+unpack(e['float_nodal_solve']).real<=arb('1e-8') for e in errors)
        rows.append({'key':key,'status':'COMPLETE','N':len(original),'active_nodes':n,'history_nodes':nh,
             'coordinates_sha256':digest(original),'counts_sha256':digest(cc),'relations_sha256':digest(relations),
             'query_counts_sha256':digest(pc),'query_relations_sha256':digest(qr),
             'source_support_hits':support_hits(x[:nh]),'numeric_pass':bool(numeric),'numeric_controls':errors,'levels':saved})
        gzwrite(out/f'BENCHMARK_{bits}.json.gz',{'precision_bits':bits,'rows':rows})
    result={'schema':p['schema'],'precision_bits':bits,'new_random_clouds':0,'protocol_sha256':sha(HERE/'PROTOCOL.json'),
            'normalization_A':pack(A),'remainder_constants':{str(o):pack(v) for o,v in cs.items()},'rows':rows}
    gzwrite(out/f'BENCHMARK_{bits}.json.gz',result);write(out/f'DECISION_{bits}.json',summarize(rows))
    write(out/f'COMPUTE_{bits}.json',{'started_UTC':stamp,'wall_seconds':time.monotonic()-start,
          'maximum_RSS_MiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
          'cpu_features_disabled':os.getenv('NPY_DISABLE_CPU_FEATURES','default')})
    return summarize(rows)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--bits',type=int,choices=[128,192],required=True);parser.add_argument('--out',type=__import__('pathlib').Path,required=True)
    a=parser.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
    print(json.dumps(compute(a.bits,a.out),indent=2))
