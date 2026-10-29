"""Source freeze, full interval benchmark and two CPU relation audits."""
import argparse,json,os,platform,resource,signal,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
import numpy as np,scipy,flint
from flint import arb,ctx
from common import HERE,sha,check,write,protocol,balls
import benchmark,audit

SOURCES=['PROTOCOL.json','requirements.txt','common.py','geometry.cpp','geometry.py','initial_data.py','propagation.py','benchmark.py','audit.py','cpu.py','run.py','verify_publication.py']
DEPENDENCIES=['../scalar_pilot_v0_1/scalar.py','../scalar_pilot_v0_1/counts.cpp','../scalar_pilot_v0_1/PROTOCOL.json',
 '../scalar_pilot_v0_1/results/RUNS.json','../scalar_pilot_v0_1/results/clouds.npz','../scalar_pilot_portability_v0_1/STREAMS.json',
 '../certified_budget_v0_3/balls.py','../certified_budget_v0_3/source.py','../certified_budget_v0_3/PROTOCOL.json','../certified_budget_v0_3/results/SOURCE.json',
 '../massive_reference_v0_5/reference.py','../massive_reference_v0_5/results/SOURCE.json','../massive_reference_v0_5/results/SOURCE_192bit.json',
 '../e4_v0_1/contract.json','../joint_budget_v0_6/results/DECISION.json']
def inventory():return {p:sha(HERE/p) for p in SOURCES+DEPENDENCIES}
def frozen():check(inventory()==json.loads((HERE/'FREEZE.json').read_text())['files'],'frozen sources and inherited evidence')

def summary(record):
    groups={};counts={'WITHIN':0,'EXCEEDS':0,'UNDECIDED':0};maxrad=arb(0);maxsolve=arb(0);maxinput=arb(0);gains=[]
    for r in record['rows']:
        for f in r['fields']:
            counts[f['relative_10pct_screen']]+=1
            key=(r['kind'],r['nu'],r['epsilon'],f['field'],f['adapter_order'])
            groups.setdefault(key,[]).append(f)
            maxsolve=max(maxsolve,balls.decode(f['component_RMS']['linear_solve_and_coefficient_rounding']['upper']).real)
            maxinput=max(maxinput,balls.decode(f['component_RMS']['initial_evaluation_rounding']['upper']).real)
            for v in f['probe_values']:
                z=balls.decode(v);maxrad=max(maxrad,z.real.rad(),z.imag.rad())
            gains+= [balls.decode(z).real for z in f['history_linf_to_each_probe_upper']]
    rows=[]
    for key,vals in groups.items():
        def pooled(field):
            return {end:balls.encode((sum(balls.decode(v[field][end]).real**2 for v in vals)/len(vals)).sqrt()) for end in ['lower','upper']}
        components={}
        for component in protocol()['error_components']:
            components[component]={end:balls.encode((sum(balls.decode(v['component_RMS'][component][end]).real**2 for v in vals)/len(vals)).sqrt()) for end in ['lower','upper']}
        rows.append({'kind':key[0],'nu':key[1],'epsilon':key[2],'field':key[3],'adapter_order':key[4],
                     'archived_clouds':len(vals),'pooled_absolute_RMS':pooled('total_RMS'),'component_pooled_absolute_RMS':components})
    return {'schema':'cspp.scalar-propagation/0.7','field_adapter_cases':sum(counts.values()),'wave_clouds':64,'compact_source_clouds':1,
            'diagnostic_relative_10pct_counts':counts,'maximum_solution_component_radius':balls.encode(maxrad),
            'maximum_solver_rounding_RMS_upper':balls.encode(maxsolve),'maximum_initial_evaluation_rounding_RMS_upper':balls.encode(maxinput),
            'largest_history_linf_gain_upper':balls.encode(max(gains)),'rows':rows,
            'pooled_RMS_scope':'descriptive on the fixed archive, not independent statistical confirmation; signed error terms must not be combined as independent variances',
            'scientific_status':protocol()['scientific_status'],'new_random_realizations':0,'confirmation_seed_used':False,
            'spatial_detector_integration_status':'NOT_QUALIFIED_BY_SEVEN_POINT_DIAGNOSTIC',
            'general_nonlocal_Cauchy_wellposedness':'NOT_PROVED'}

def production(out,cpu=True):
    frozen();check((np.__version__,scipy.__version__,flint.__version__,flint.__FLINT_VERSION__)==('2.3.5','1.17.0','0.8.0','3.3.1'),'pinned numerical environment')
    check(os.getenv('OPENBLAS_NUM_THREADS')=='1' and os.getenv('OMP_NUM_THREADS')=='1','single-thread resource contract')
    resource.setrlimit(resource.RLIMIT_AS,(4*1024**3,4*1024**3));signal.alarm(protocol()['resources']['wall_seconds_max'])
    out.mkdir(parents=True,exist_ok=True);start=time.monotonic();ctx.prec=128;checks=audit.controls();records={}
    for bits in [128,192]:
        records[bits]=benchmark.compute(bits,out);audit.validate(records[bits])
    checks['replay']=audit.compare(records[128],records[192]);checks['reference_node_overlaps']=0
    a=benchmark.gzread(out/'SOURCE_NODES_128.json.gz');b=benchmark.gzread(out/'SOURCE_NODES_192.json.gz')
    check(a['coordinates_sha256']==b['coordinates_sha256'] and a['active_nodes']==b['active_nodes'],'source identity replay')
    for x,y in zip(a['values'],b['values']):
        for u,v in zip(x,y):check(balls.decode(u).overlaps(balls.decode(v)),'source node enclosure overlap');checks['reference_node_overlaps']+=1
    checks['status']='PASS';write(out/'AUDIT.json',checks);write(out/'SUMMARY.json',summary(records[128]))
    if cpu:
        for label,features in [('DEFAULT',None),('BASELINE','AVX512F,AVX512_SKX,AVX512_CLX,AVX512_CNL,AVX512_ICL')]:
            env=dict(os.environ)
            if features:env['NPY_DISABLE_CPU_FEATURES']=features
            else:env.pop('NPY_DISABLE_CPU_FEATURES',None)
            subprocess.run([sys.executable,'-B',str(HERE/'cpu.py'),'--source',str(out),'--out',str(out/f'CPU_{label}.json')],check=True,env=env)
    write(out/'COMPUTE.json',{'elapsed_seconds':time.monotonic()-start,'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
      'python_flint':flint.__version__,'FLINT':flint.__FLINT_VERSION__,'peak_RSS_MiB':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
      'new_random_realizations':0,'CPU_audits_run':cpu,'scientific_status':protocol()['scientific_status']})

def main():
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['freeze','all']);p.add_argument('--out',type=Path,default=HERE/'results');p.add_argument('--skip-cpu',action='store_true');a=p.parse_args()
    if a.phase=='freeze':
        check(not (HERE/'FREEZE.json').exists(),'refuse replacing freeze')
        write(HERE/'FREEZE.json',{'UTC':datetime.now(timezone.utc).isoformat(),'scope':'deterministic development freeze after exploratory runtime/control tests, before saved production; no new random data','files':inventory()})
    else:production(a.out,not a.skip_cpu)
if __name__=='__main__':main()
