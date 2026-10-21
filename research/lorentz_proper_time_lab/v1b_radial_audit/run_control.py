#!/usr/bin/env python3
"""Run the frozen fresh-data radial control once, without changing core.js."""
import argparse, gzip, hashlib, json, platform, subprocess, sys, tempfile
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import binomtest, ks_2samp
from diagnose import HERE, ROOT, digest, ks, load_trace

def split_interval(start,length):
    end=start+length
    return [(start,min(end,2**32))]+([(0,end-2**32)] if end>2**32 else [])
def overlaps(a,b):return any(max(x,u)<min(y,v) for x,y in a for u,v in b)
def schedule(q):
    C=0x6D2B79F5;inv=pow(C,-1,2**32);length=q['reserved_uniforms_per_stream']
    used=[split_interval(((s*inv)+1)%2**32,length) for s in q['historical_seeds']]
    accepted=[];skipped=[];i=0
    while len(accepted)<q['batches']*q['streams_per_batch']:
        h=hashlib.sha256((q['seed_namespace']+f'/mulberry32/{i}').encode()).digest()
        seed=int.from_bytes(h[:4],'little');phase=(seed*inv+1)%2**32
        interval=split_interval(phase,length)
        if any(overlaps(interval,x) for x in used):skipped.append(dict(candidate=i,seed=seed,reason='reserved-state-window-overlap'))
        else:accepted.append(dict(candidate=i,seed=seed,first_state_phase=phase));used.append(interval)
        i+=1
    return accepted,skipped
def analyze(out,q):
    arms={};all_values={};historical=json.loads((HERE/'results/diagnosis.json').read_text())
    x0=historical['input_radial']['location']
    for arm in ['mulberry32','philox32']:
        summary=json.loads((out/f'{arm}_trace.json').read_text())
        batch=[];traces=[]
        for g in summary['groups']:
            path=out/g['file'];assert digest(path)==g['file_sha256']
            z=gzip.decompress(path.read_bytes());assert hashlib.sha256(z).hexdigest()==g['raw_sha256']
            t=load_trace(path);assert len(t)==q['m']*q['streams_per_batch'];traces.append(t)
            batch.append(dict(id=g['id'],reconstructed=ks(t['w']),radial_input=ks(t['u']/2**32)))
        t=np.concatenate(traces);u=t['u']/2**32;w=t['w'];all_values[arm]=u
        failures=sum(b['reconstructed']['p']<.05 for b in batch)
        tail=binomtest(failures,q['batches'],.05,alternative='greater')
        rate=binomtest(failures,q['batches']).proportion_ci(confidence_level=.95,method='exact')
        pooled=ks(w);input_ks=ks(u)
        delta=float(np.max(abs(w-u)))
        records=[r for g in summary['groups'] for r in g['streams']]
        rejects={k:sum(r['rejected'][k] for r in records) for k in records[0]['rejected']}
        engineering=delta<=q['transform_tolerance'] and all(r['max_support']<.5 and r['draws']<=q['reserved_uniforms_per_stream'] for r in records)
        # Diagnostic confidence radius assumes iid observations; not a PRNG proof.
        iid_radius=float(pooled['D']+np.sqrt(np.log(2/.025)/(2*len(w))))
        fixed_count=int(np.count_nonzero(u<=x0))
        arms[arm]=dict(n=len(w),pooled_reconstructed=pooled,pooled_radial_input=input_ks,batches=batch,
            batch_rejections_at_005=failures,batch_rejection_upper_tail_p=float(tail.pvalue),
            batch_rejection_rate_95ci=[float(rate.low),float(rate.high)],
            primary_pooled_pass=pooled['p']>=q['primary_alpha_per_test'],
            primary_excess_rejection_pass=tail.pvalue>=q['primary_alpha_per_test'],
            max_transform_error=delta,rejections=rejects,engineering_pass=engineering,
            nominal_iid_CDF_distance_upper_975=iid_radius,
            historical_location_probe=dict(x=x0,count=fixed_count,cdf_excess=fixed_count/len(u)-x0,
                one_sided_p=float(binomtest(fixed_count,len(u),x0,alternative='greater').pvalue),role='SECONDARY_DESCRIPTIVE'))
    control=ks(all_values['philox32'][:q['m']*q['streams_per_batch']]**3)
    assert control['p']<q['wrong_exponent_control_max_p']
    two=ks_2samp(all_values['mulberry32'],all_values['philox32'],method='asymp')
    statistical=all(a['primary_pooled_pass'] and a['primary_excess_rejection_pass'] for a in arms.values())
    engineering=all(a['engineering_pass'] for a in arms.values())
    report=dict(schema=q['schema'],status='NO_DISCREPANCY_DETECTED_IN_FIXED_FOLLOWUP' if statistical and engineering else 'FOLLOWUP_HOLD',
        original_V1b='NOT_PASSED',original_radial_gate='FAIL_UNCHANGED',primary_family_alpha=.05,primary_alpha_per_test=q['primary_alpha_per_test'],
        arms=arms,wrong_exponent_positive_control=control,
        secondary_two_sample_KS=dict(D=float(two.statistic),p=float(two.pvalue),role='SECONDARY_DESCRIPTIVE'),
        statistical_screens_pass=statistical,engineering_pass=engineering,
        limitations=q['interpretation_limits'])
    return report

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--freeze-commit',required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    q=json.loads((HERE/'protocol.json').read_text());out=args.output.resolve()
    if out.exists():raise SystemExit('Use a new output directory; no overwrite or automatic retry.')
    frozen=['protocol.json','run_control.py','trace.cjs','diagnose.py']
    for name in frozen:
        archived=subprocess.check_output(['git','show',f'{args.freeze_commit}:{(HERE/ name).relative_to(ROOT)}'],cwd=ROOT)
        if archived!=(HERE/name).read_bytes():raise SystemExit('Frozen source mismatch: '+name)
    assert digest(HERE.parent/'core.js')==q['core_sha256']
    assert np.__version__==q['versions']['numpy'] and scipy.__version__==q['versions']['scipy']
    out.mkdir(parents=True)
    seeds,skipped=schedule(q)
    keys=[int.from_bytes(hashlib.sha256((q['seed_namespace']+f'/philox32/{i}').encode()).digest()[:16],'little') for i in range(len(seeds))]
    assert len(set(keys))==len(keys)
    schedule_record=dict(mulberry32=seeds,skipped_without_generating_outputs=skipped,philox_keys=[str(k) for k in keys])
    (out/'schedule.json').write_text(json.dumps(schedule_record,indent=2)+'\n')
    with tempfile.TemporaryDirectory(prefix='radial-control-') as work:
        tmp=Path(work)
        for arm in ['mulberry32','philox32']:
            groups=[]
            for b in range(q['batches']):
                streams=[]
                for j in range(q['streams_per_batch']):
                    i=b*q['streams_per_batch']+j;rec=dict(id=f'{arm}-{i:03d}')
                    if arm=='mulberry32':rec['seed']=seeds[i]['seed']
                    else:
                        rec['key']=str(keys[i]);p=tmp/f'philox-{i:03d}.u32'
                        values=(np.random.Philox(key=keys[i]).random_raw(q['reserved_uniforms_per_stream'])>>np.uint64(32)).astype('<u4')
                        p.write_bytes(values.tobytes());rec['input_file']=str(p)
                    streams.append(rec)
                groups.append(dict(id=f'{arm}-{b:02d}',streams=streams))
            config=dict(output=str(out),historical=False,m=q['m'],summary_file=f'{arm}_trace.json',groups=groups)
            p=tmp/'config.json';p.write_text(json.dumps(config))
            subprocess.run(['node',str(HERE/'trace.cjs'),str(p)],check=True)
    report=analyze(out,q)
    report['provenance']=dict(base_commit=q['base_commit'],freeze_commit=args.freeze_commit,protocol_sha256=digest(HERE/'protocol.json'),
        source_sha256={name:digest(HERE/name) for name in frozen},core_sha256=digest(HERE.parent/'core.js'),
        runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,node=subprocess.check_output(['node','--version'],text=True).strip()),
        public_preregistration_required=True)
    (out/'control_report.json').write_text(json.dumps(report,indent=2)+'\n')
    (out/'SHA256SUMS').write_text(''.join(f'{digest(p)}  {p.name}\n' for p in sorted(out.iterdir()) if p.is_file() and p.name!='SHA256SUMS'))
    print(json.dumps(dict(status=report['status'],arms={k:{f:a[f] for f in ['n','pooled_reconstructed','batch_rejections_at_005','batch_rejection_upper_tail_p','max_transform_error','historical_location_probe']} for k,a in report['arms'].items()}),indent=2))
if __name__=='__main__':main()
