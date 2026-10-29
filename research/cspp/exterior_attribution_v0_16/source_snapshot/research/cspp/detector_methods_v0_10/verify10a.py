"""Corrected post-run verifier; see VERIFICATION_AMENDMENT.json.
Scientific production sources and the original verifier remain frozen.
"""
import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from common10 import HERE, arb, ctx, check, plan, unpack, gzread, write, sha, freeze_check
import run10
import audit10


def compare(a,b):
    check(a['protocol_sha256']==b['protocol_sha256'] and a['new_random_clouds']==b['new_random_clouds']==0,'same deterministic development data')
    check(len(a['rows'])==len(b['rows']),'same complete slot inventory');count=0
    for r,s in zip(a['rows'],b['rows']):
        check(r['key']==s['key'] and r['status']==s['status'],'same slot and availability')
        if r['status']!='COMPLETE':continue
        for key in ['N','active_nodes','history_nodes','coordinates_sha256','counts_sha256','relations_sha256',
                    'query_counts_sha256','query_relations_sha256','source_support_hits','numeric_pass']:
            check(r[key]==s[key],'same geometry and decision: '+key)
        for l,m in zip(r['levels'],s['levels']):
            for key in ['n','sectors','geometry_sha256']:check(l[key]==m[key],'same certified sector geometry')
            for w,v in zip(l['windows'],m['windows']):
                check(w['field_pass']==v['field_pass'] and w['adapter_bound_pass']==v['adapter_bound_pass'],'same budget decisions')
                for key in ['values','oracle_waves','continuum_waves','history_transfer','query_coefficients']:
                    check(len(w[key])==len(v[key]),'same enclosed vector size')
                    for x,y in zip(w[key],v[key]):check(unpack(x).overlaps(unpack(y)),'enclosed comparison '+key);count+=1
    return count


def verify(directory):
    freeze_check();p=plan();ctx.prec=256
    registration=json.loads((HERE/'REGISTRATION.json').read_text())
    docs=[gzread(directory/f'BENCHMARK_{b}.json.gz') for b in p['precision_bits']]
    for bits,doc in zip(p['precision_bits'],docs):
        check(doc['precision_bits']==bits and doc['new_random_clouds']==0,'precision and no new random data')
        check(doc['protocol_sha256']==sha(HERE/'PROTOCOL.json'),'same frozen protocol')
        check([r['key'] for r in doc['rows']]==p['clouds'],'every fixed archive slot')
        compute=json.loads((directory/f'COMPUTE_{bits}.json').read_text())
        check(datetime.datetime.fromisoformat(compute['started_UTC'])>datetime.datetime.fromisoformat(registration['published_UTC'].replace('Z','+00:00')),'archive integration after public method freeze')
        check(compute['maximum_RSS_MiB']<4096,'memory cap')
        for row in doc['rows']:
            if row['status']!='COMPLETE':continue
            check([l['n'] for l in row['levels']]==p['spatial_grids'],'all fixed refinement levels')
            check(row['N']<=p['resources']['max_points_per_cloud'],'cloud resource bound')
            scales=[arb(1)]*4+[unpack(doc['normalization_A']).real/arb(1).exp()]*2
            for level in row['levels']:
                check(level['sectors']==level['n']**3 and len(level['windows'])==2,'full ball and both windows')
                for w in level['windows']:
                    check(len(w['values'])==6 and len(w['oracle_waves'])==4,'all physical fields and wave controls')
                    check(len(w['query_coefficients'])==row['active_nodes'] and len(w['history_transfer'])==row['history_nodes'],'full query and history transfer')
                    for f,(z,s) in enumerate(zip(w['values'],scales)):
                        z=unpack(z);ratio=max(z.real.rad(),z.imag.rad())/s
                        # Serialization can enlarge a ball by tiny endpoint rounding.
                        # Success requires the serialized upper bound too; no false PASS.
                        if w['field_pass'][f]:check(ratio<=arb(p['integration_tolerance']),'reported integration pass enclosed')
                        else:check(ratio>arb(p['integration_tolerance']),'reported integration hold reproduced')
                    for v,passed in zip(w['adapter_normalized_error_upper'],w['adapter_bound_pass']):
                        check(unpack(v).real>=0,'nonnegative initial-data error upper bound')
                        check(bool(unpack(v).real<=arb(p['adapter_tolerance']))==passed,'derived initial-data upper-bound decision')
                    for k in range(4):
                        total=unpack(w['values'][k])-unpack(w['continuum_waves'][k])
                        split=unpack(w['wave_history_effect'][k])+unpack(w['wave_operator_domain_effect'][k])
                        check(total.overlaps(split),'separate wave errors telescope')
                    if row['source_support_hits']==0:
                        check(all(unpack(w['values'][f]).is_zero() for f in [4,5]),'both local adapters miss the compact source exactly')
            derived_numeric=all(unpack(e['node_radius']).real<=arb('1e-18') and unpack(e['input_rounding']).real+unpack(e['float_nodal_solve']).real<=arb('1e-8') for e in row['numeric_controls'])
            check(row['numeric_pass']==bool(derived_numeric),'derived nodal numerical decision')
        derived=run10.summarize(doc['rows'])
        check(derived==json.loads((directory/f'DECISION_{bits}.json').read_text()),'all public decisions recomputed')
        if derived['decision']!='RESOURCE_HOLD':check(compute['wall_seconds']<=p['resources']['wall_seconds_per_process'],'completed process time budget')
    cpu=json.loads((directory/'CPU_BASELINE_COMPUTE.json').read_text())
    check(cpu['cpu_features_disabled']==p['cpu_modes'][1],'declared baseline CPU mask')
    check(cpu['maximum_RSS_MiB']<4096,'baseline memory cap')
    for order in ['1','3']:
        check(unpack(docs[0]['remainder_constants'][order]).overlaps(unpack(docs[1]['remainder_constants'][order])),'common analytic norm expression agrees')
    checks=compare(*docs)+compare(docs[0],gzread(directory/'BASELINE_128.json.gz'))
    control=audit10.compute();check(control['status']=='PASS','analytic controls')
    return {'status':'PASS','enclosed_comparisons':checks,'analytic_controls':control['count'],'decision':run10.summarize(docs[0]['rows'])}


def replay():
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='cspp-v10-replay-') as temp:
        p=Path(temp)
        for bits in [128,192]:subprocess.run([sys.executable,'-B',str(HERE/'run10.py'),'--bits',str(bits),'--out',str(p)],check=True,env=env)
        baseline=p/'baseline'
        subprocess.run([sys.executable,'-B',str(HERE/'run10.py'),'--bits','128','--out',str(baseline)],check=True,
                       env=dict(env,NPY_DISABLE_CPU_FEATURES=plan()['cpu_modes'][1]))
        (p/'BASELINE_128.json.gz').write_bytes((baseline/'BENCHMARK_128.json.gz').read_bytes())
        (p/'CPU_BASELINE_COMPUTE.json').write_bytes((baseline/'COMPUTE_128.json').read_bytes())
        out=verify(p)
        for bits in [128,192]:compare(gzread(p/f'BENCHMARK_{bits}.json.gz'),gzread(HERE/'results'/f'BENCHMARK_{bits}.json.gz'))
        return out


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--preflight',action='store_true');a.add_argument('--replay',action='store_true');a.add_argument('--out',type=Path);args=a.parse_args()
    if (HERE/'SHA256SUMS').exists():
        for line in (HERE/'SHA256SUMS').read_text().splitlines():
            expected,name=line.split('  ',1);check(sha(HERE/name)==expected,'package digest '+name)
    if args.preflight:freeze_check();result=audit10.compute()
    else:result=replay() if args.replay else verify(HERE/'results')
    if args.out:write(args.out,result)
    print(json.dumps(result,indent=2))
