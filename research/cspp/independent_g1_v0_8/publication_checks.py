"""Publication verifier, with Amendment01 for precision-dependent report floors."""
import argparse,datetime,json,os,subprocess,sys,tempfile
from pathlib import Path
import numpy as np
from flint import arb,ctx
from support import HERE,check,sha,write,plan,freeze_check,gzread,unpack,old,digest,norm,load
import inference,scalar_operator as op
# support exposes predecessor geometry through sys.path; resolve this audit
# by its frozen package path, never by the ambiguous bare module name.
audit=load('v08_frozen_audit',HERE/'audit.py')

def exact_decision(d):
    """Compare exact rational endpoints/counts/decisions, not rounded floors."""
    copy=json.loads(json.dumps(d))
    for cell in copy['cells']:
        for test in cell['tests']:del test['population_RMS_lower']
    return copy

def validate_reported_lower_bounds(d):
    previous=ctx.prec
    try:
        ctx.prec=256
        for cell in d['cells']:
            for test in cell['tests']:
                lo=arb(test['exceedance_probability_lower_endpoint_bracket'][0])
                exact=(lo/25).sqrt()
                raw=unpack(test['population_RMS_lower'])
                check(raw.imag.is_zero() and raw.real.lower()>=0,'real nonnegative RMS lower report')
                check(raw.real.lower()<=exact.lower(),'reported endpoint is a valid downward RMS bound')
                check((exact-raw.real.lower()).upper()<=arb('1e-35'),'precision-specific floor near exact expression')
    finally:ctx.prec=previous

def verify(source):
    ctx.prec=128;p=plan();freeze_check()
    pre=json.loads((HERE/'REGISTRATION.json').read_text())
    start=json.loads((source/'COMPUTE_128.json').read_text())['started_UTC']
    check(datetime.datetime.fromisoformat(start)>datetime.datetime.fromisoformat(pre['published_UTC'].replace('Z','+00:00')),'sampling after public registration')
    a=gzread(source/'BENCHMARK_128.json.gz');b=gzread(source/'BENCHMARK_192.json.gz')
    check(a['preregistration_commit']==b['preregistration_commit']==pre['commit_sha'],'pre-data commit identity')
    check(a['protocol_sha256']==b['protocol_sha256']==sha(HERE/'PROTOCOL.json'),'protocol identity')
    check(len(a['rows'])==len(b['rows'])==768,'all 768 planned paired cell-realizations')
    check(a['graphs']==b['graphs'],'exact graph replay across precision')
    count=0;maxinput=0.;maxnum=0.;maxradius=0.
    pv,bp=op.values(old.probes()[:21],True)
    for r,s in zip(a['rows'],b['rows']):
        check([r[k] for k in ['density_index','realization_index','epsilon','status']]==[s[k] for k in ['density_index','realization_index','epsilon','status']],'fixed row identity and availability')
        if r['status']!='COMPLETE':continue
        check([f['field'] for f in r['fields']]==p['fields'],'complete fixed field family')
        for j,(f,g) in enumerate(zip(r['fields'],s['fields'])):
            for x,y in zip(f['operator_values'],g['operator_values']):
                check(unpack(x).overlaps(unpack(y)),'128/192 operator-value overlap');count+=1
            denominator=max(norm([v[j] for v in pv])[1],norm([v[j] for v in bp])[1])
            local_lower=norm([unpack(z)-v[j] for z,v in zip(f['operator_values'],bp)])[0]/denominator
            # Stored decimal balls widen the original result, so a certified
            # success must remain certified after serialization as well.
            if f['certified_exceedance']:check(local_lower>arb('1/5'),'stored evidence really exceeds frozen threshold')
            check(f['certified_exceedance']==g['certified_exceedance'],'same exceedance decision at both precisions')
            check(f['certified_exceedance']==bool(unpack(f['relative_operator_RMS'][0]).real>arb('1/5')),'derived, not asserted, success flag')
            for field in ['normalized_input_rounding_RMS_upper','normalized_coefficient_sum_RMS_upper']:
                check(unpack(f[field]).real<=arb('1e-8'),'separate numeric budget')
            maxinput=max(maxinput,float(unpack(f['normalized_input_rounding_RMS_upper']).real.upper()))
            maxnum=max(maxnum,float(unpack(f['normalized_coefficient_sum_RMS_upper']).real.upper()))
            maxradius=max(maxradius,float(unpack(f['maximum_component_radius']).real.upper()))
    check(maxradius<=1e-12,'reference/enclosure radius budget')
    decision=inference.summarize(a['rows'])
    for bits in [128,192]:
        saved=json.loads((source/f'DECISION_{bits}.json').read_text())
        check(exact_decision(decision)==exact_decision(saved),'identical exact counts, CP rational endpoints and decisions')
        validate_reported_lower_bounds(saved)
    hashes=[];entropy=[];points=0
    prior=np.load(HERE.parent/'scalar_pilot_v0_1/results/clouds.npz')
    prior_hashes={digest(prior[k]) for k in prior.files}
    for d in range(4):
        archive=np.load(source/f'clouds_d{d}.npz')
        for g in a['graphs'][d*64:(d+1)*64]:
            if g['status']!='COMPLETE':continue
            x=archive[g['key']];h=digest(x);check(h==g['coordinates_sha256'],'canonical cloud integrity')
            check(h not in prior_hashes,'fresh cloud differs from every development archive')
            check(g['entropy']==[2,8,1,d,g['realization_index'],1,p['rng']['master_seed']],'fixed method-validation stream')
            hashes.append(h);entropy.append(tuple(g['entropy']));points+=len(x)
    check(len(set(hashes))==len(hashes) and len(set(entropy))==len(entropy),'no duplicate data or stream identities')
    for mode in ['DEFAULT','BASELINE']:
        cpu=json.loads((source/f'CPU_{mode}.json').read_text())
        check(cpu['status']=='PASS' and cpu['clouds_checked']==len(hashes),'complete required CPU graph scope')
    check(json.loads((source/'AUDIT.json').read_text())['status']=='PASS','pre-data controls')
    return {'status':'PASS','independent_clouds':len(hashes),'total_points':points,'operator_value_overlaps':count,
            'field_cell_realizations':sum(len(r['fields']) for r in a['rows']),
            'maximum_normalized_input_rounding_RMS':maxinput,'maximum_normalized_coefficient_sum_RMS':maxnum,
            'maximum_Arb_component_radius':maxradius,'rejected_cells':decision['rejected_cells'],
            'scientific_status':decision['scientific_status'],'Dirac_decision':decision['Dirac_decision']}

def replay():
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
    with tempfile.TemporaryDirectory(prefix='cspp-g1-replay-') as t:
        out=Path(t);write(out/'AUDIT.json',audit.compute())
        for d in range(4):(out/f'clouds_d{d}.npz').symlink_to((HERE/'results'/f'clouds_d{d}.npz').resolve())
        for bits in [128,192]:
            subprocess.run([sys.executable,'-B',str(HERE/'run.py'),'--out',t,'--bits',str(bits),'--replay-source',str(HERE/'results')],check=True,env=env)
        for name,features in zip(['DEFAULT','BASELINE'],plan()['cpu']['modes']):
            cpuenv=dict(env)
            if features!='default':cpuenv['NPY_DISABLE_CPU_FEATURES']=features
            subprocess.run([sys.executable,'-B',str(HERE/'cpu.py'),'--source',t,'--out',str(out/f'CPU_{name}.json')],check=True,env=cpuenv)
        result=verify(out)
        for bits in [128,192]:
            check(json.loads((out/f'DECISION_{bits}.json').read_text())==json.loads((HERE/'results'/f'DECISION_{bits}.json').read_text()),'full replay conclusion')
            actual=gzread(out/f'BENCHMARK_{bits}.json.gz');saved=gzread(HERE/'results'/f'BENCHMARK_{bits}.json.gz')
            check(actual['graphs']==saved['graphs'],'replay all graph identities')
            for row,prior in zip(actual['rows'],saved['rows']):
                check(row['status']==prior['status'],'replay availability')
                for field,earlier in zip(row['fields'],prior['fields']):
                    for v,w in zip(field['operator_values'],earlier['operator_values']):
                        check(unpack(v).overlaps(unpack(w)),'every replay value overlaps archived enclosure')
                    check(np.allclose(field['numeric_values'],earlier['numeric_values'],atol=1e-10,rtol=1e-11),'replay archived numerical action')
        return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');p.add_argument('--out',type=Path);z=p.parse_args()
    if (HERE/'SHA256SUMS').exists():
        for line in (HERE/'SHA256SUMS').read_text().splitlines():
            h,name=line.split('  ',1);check(sha(HERE/name)==h,'package file '+name)
    result=replay() if z.replay else verify(HERE/'results')
    if z.out:write(z.out,result)
    print(json.dumps(result,indent=2))
