"""Complete fixed ensemble; resource failures retain their original slots."""
import argparse,datetime,json,resource,signal,time
from pathlib import Path
import numpy as np
from flint import ctx
from support import HERE,old,check,sha,digest,write,plan,draw,freeze_check,gzwrite,gzread,geometry
import scalar_operator as op
from inference import summarize

def unavailable(d,i,e,reason):
    return {'density_index':d,'realization_index':i,'epsilon':e,'status':reason,'fields':[]}

def compute(out,bits,replay_source=None):
    freeze_check();p=plan();ctx.prec=bits;out.mkdir(parents=True,exist_ok=True)
    registration=json.loads((HERE/'REGISTRATION.json').read_text())
    check(len(registration['commit_sha'])==40 and registration['published_before_sampling'],'public preregistration receipt')
    started=datetime.datetime.now(datetime.timezone.utc).isoformat();t0=time.monotonic()
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3))
    stop=False;rows=[];graphs=[];total_points=0
    for d,nu in enumerate(p['nu']):
        clouds={};source=np.load(replay_source/f'clouds_d{d}.npz') if replay_source else None
        oldgraphs={g['key']:g for g in gzread(replay_source/'BENCHMARK_128.json.gz')['graphs']} if replay_source else {}
        for i in range(p['realizations_per_density']):
            key=f'd{d}_r{i:02d}'
            if stop or time.monotonic()-t0>p['resources']['campaign_wall_seconds']:
                stop=True;rows.extend(unavailable(d,i,e,'RESOURCE_HOLD_NOT_ATTEMPTED') for e in p['epsilon'])
                graphs.append({'key':key,'status':'RESOURCE_HOLD_NOT_ATTEMPTED'});continue
            x=None;meta={}
            try:
                if source is None:x,meta=draw(d,i)
                else:
                    prior=oldgraphs[key];meta={k:prior[k] for k in ['entropy','N','rng_draw_output_sha256']} if 'entropy' in prior else {}
                    x=source[key] if key in source.files else None
                check(x is not None,'RESOURCE_HOLD Poisson point cap')
                clouds[key]=x;total_points+=len(x)
                _,pc,rr,rp,stats=geometry.inventory(x,old.probes()[:21],full=False)
                domain,ds=geometry.region(x,4);check(np.all(domain),'exact Omega4 membership')
                graph={'key':key,'status':'COMPLETE','density_index':d,'realization_index':i,**meta,
                       'coordinates_sha256':digest(x),'relations_sha256':digest(rr),
                       'probe_relations_sha256':digest(rp),'probe_counts_sha256':digest(pc),
                       'domain_mask_sha256':digest(domain),'geometry_stats':stats,'domain_stats':ds}
                graphs.append(graph)
                check(len(x)>0,'NUMERICAL_HOLD empty cloud requires full zero-trial handling')
                field_values=op.values(x)[0]
                for e in p['epsilon']:
                    try:
                        fields=op.compute(x,pc,nu,e,field_values)
                        rows.append({'density_index':d,'realization_index':i,'epsilon':e,'status':'COMPLETE','fields':fields})
                    except (RuntimeError,ArithmeticError,MemoryError,ValueError) as exc:
                        rows.append(unavailable(d,i,e,'NUMERICAL_HOLD: '+str(exc)))
                print(bits,key,len(x),'complete',flush=True)
            except (RuntimeError,ArithmeticError,MemoryError,ValueError) as exc:
                if not any(g['key']==key for g in graphs):graphs.append({'key':key,'status':str(exc),**(meta if 'meta' in locals() else {})})
                rows.extend(unavailable(d,i,e,'UNAVAILABLE: '+str(exc)) for e in p['epsilon'])
                print(bits,key,'UNAVAILABLE',str(exc),flush=True)
        if source is None:np.savez_compressed(out/f'clouds_d{d}.npz',**clouds)
    check(len(rows)==768 and len(graphs)==256,'fixed planned ensemble')
    result={'precision_bits':bits,'protocol_sha256':sha(HERE/'PROTOCOL.json'),
            'preregistration_commit':registration['commit_sha'],'rows':rows,'graphs':graphs}
    gzwrite(out/f'BENCHMARK_{bits}.json.gz',result)
    write(out/f'DECISION_{bits}.json',summarize(rows))
    write(out/f'COMPUTE_{bits}.json',{'started_UTC':started,'completed_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'wall_seconds':time.monotonic()-t0,'max_rss_MiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
            'total_points':total_points,'complete_cells':sum(r['status']=='COMPLETE' for r in rows),
            'planned_cell_realizations':768,'new_clouds':256 if source is None else 0})
    return result

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--bits',type=int,choices=[128,192],required=True);a.add_argument('--replay-source',type=Path)
    z=a.parse_args();compute(z.out,z.bits,z.replay_source)
