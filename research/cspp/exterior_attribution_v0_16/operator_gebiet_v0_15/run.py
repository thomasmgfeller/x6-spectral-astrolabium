"""Deterministic, interval-certified operator/domain diagnosis on archived data."""
import argparse, gzip, hashlib, json, sys, time
from pathlib import Path
import numpy as np
from flint import arb, acb, ctx

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'source_snapshot/research/cspp'
sys.path.insert(0,str(ROOT/'joint_budget_v0_6'))
import model
sys.path.insert(0,str(ROOT/'scalar_propagation_v0_7'))
import geometry

def require(ok,label):
    if not bool(ok): raise RuntimeError('HOLD: '+label)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest(x): return hashlib.sha256(np.ascontiguousarray(x).tobytes()).hexdigest()
def pack(x):
    x=acb(x); require(x.is_finite(),'finite interval')
    v=[x.real.str(45,more=True),x.imag.str(45,more=True)]
    require(arb(v[0]).contains(x.real) and arb(v[1]).contains(x.imag),'outward serialization')
    return v
def unpack(x): return acb(arb(x[0]),arb(x[1]))
def dump(p,x): Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def loadgz(p):
    with gzip.open(p,'rt') as f: return json.load(f)
def weights(n,e):
    from math import comb
    if e==1:return [arb([1,-9,16,-8][i] if i<4 else 0) for i in range(n+1)]
    return [sum(arb(c)*comb(i,k)*e**k*(1-e)**(i-k) for k,c in enumerate([1,-9,16,-8]) if k<=i) for i in range(n+1)]

def compute(bits):
    ctx.prec=bits; start=time.monotonic(); p=json.loads((HERE/'PROTOCOL.json').read_text())
    for name,h in json.loads((HERE/'FREEZE.json').read_text())['sha256'].items():
        require(sha(HERE/name)==h,'frozen file '+name)
    rho=3/arb.pi(); target=-arb(1)/2; controls=[]; means={}
    for e0 in p['epsilon']:
        e=arb(e0);q=e*rho;ell=q**(-arb(1)/4)
        mu,meta=model.previous_mean.mean_witness(ell)
        require(mu.rad()<arb('1e-15'),'infinite witness enclosure')
        rows=[]
        for H in p['H']:
            # Both routes are established predecessor methods with explicit rests.
            if H<=8:finite=model.finite_mean_direct(ell,H);method='validated compact double integral'
            else:finite=mu-model.outside_boundary(ell,H)[0];method='Gamma series plus explicit Taylor and wedge rests'
            require(finite.rad()<arb('1e-12'),'finite witness enclosure')
            boundary=finite-mu; bias=mu-target
            require((finite-target-bias-boundary).contains(0),'signed mean split')
            rows.append({'H':H,'finite_mean':pack(finite),'boundary_signed':pack(boundary),'total_bias':pack(finite-target),
                         'relative_total_bias':pack(abs(finite-target)/abs(target)),'method':method})
            means[(e0,H)]=finite
        tail=model.previous_mean.gaussian_tail(ell,12,2)
        bound=(mu-target).abs_lower()-tail.abs_upper()
        controls.append({'epsilon':e0,'q':pack(q),'ell':pack(ell),'infinite_mean':pack(mu),'operator_bias':pack(mu-target),
            'relative_infinite_bias':pack(abs(mu-target)/abs(target)),'finite_domains':rows,
            'all_H_ge_12_absolute_tail_bound':pack(tail),'all_H_ge_12_relative_bias_lower':pack(bound/abs(target)),
            'mean_integral_rests':meta,'necessary_10pct_bias_test':'REJECT' if abs(mu-target)>arb('0.05') else 'UNRESOLVED'})
    archive=np.load(ROOT/'scalar_pilot_v0_1/results/clouds.npz')
    oldruns=json.loads((ROOT/'scalar_pilot_v0_1/results/RUNS.json').read_text())
    pairs=[];e=arb('1/16');q=e*rho;a=4*(q/6).sqrt();mu=unpack(controls[-1]['infinite_mean']).real
    for key in p['paired_existing_clouds']:
        x=archive[key];y=archive[key+'_outer']; rec=next(z for z in oldruns if z['key']==key)
        require(digest(x)==rec['coordinates_sha256'] and digest(y)==rec['outer_sha256'],'archived pair identity')
        index={tuple(row):i for i,row in enumerate(y)};inner=[index[tuple(row)] for row in x]
        outer=[i for i in range(len(y)) if i not in set(inner)]
        _,c4,_,_,s4=geometry.inventory(x,np.zeros((1,4)),full=False)
        _,c5,_,_,s5=geometry.inventory(y,np.zeros((1,4)),full=False)
        require(np.array_equal(c4[0],c5[0,inner]),'convex-domain count invariance')
        w=weights(len(y),e)
        def field(row):return (-sum(arb(float(z))**2 for z in row)/8).exp()
        def summation(z,counts,indices):return sum(w[int(counts[i])]*field(z[i]) for i in indices if counts[i]>=0)
        f4=a*(-1+e*summation(x,c4[0],range(len(x))))
        f5=a*(-1+e*summation(y,c5[0],range(len(y))))
        shell=a*e*summation(y,c5[0],outer)
        require((f5-f4-shell).contains(0),'shell-only paired difference')
        srows=[]
        for H,f in [(4,f4),(5,f5)]:
            b=means[('1/16',H)]-mu;noise=f-means[('1/16',H)];op=mu-target
            require((f-target-op-b-noise).contains(0),'sample operator-boundary-fluctuation split')
            srows.append({'H':H,'operator_value':pack(f),'operator_bias':pack(op),'boundary_bias':pack(b),
                          'realization_deviation':pack(noise),'total_error':pack(f-target)})
        pairs.append({'key':key,'N4':len(x),'N5':len(y),'coordinates_sha256':digest(x),'outer_sha256':digest(y),
            'count_invariance':True,'paired_change':pack(f5-f4),'direct_shell':pack(shell),
            'shell_mean':pack(means[('1/16',5)]-means[('1/16',4)]),
            'shell_realization_deviation':pack(shell-(means[('1/16',5)]-means[('1/16',4)])),
            'geometry_checks':[s4,s5],'splits':srows})
    v12=loadgz(ROOT/f'full_continuum_v0_12/results/BENCHMARK_{bits}.json.gz')
    v10=loadgz(ROOT/f'detector_methods_v0_10/results/BENCHMARK_{bits}.json.gz')
    history=[]
    for key in p['history_clouds']:
        old=next(r for r in v12['rows'] if r['key']==key); prev=next(r for r in v10['rows'] if r['key']==key)
        x=archive[key];require(digest(x)==old['coordinates_sha256']==prev['coordinates_sha256'],'source cloud unchanged')
        nh=old['history_nodes'];require(nh==int(np.searchsorted(x[:,0],-1,side='right')),'history identity')
        h=list(map(unpack,old['oracle_history']));wins=[]
        for wi,w in enumerate(prev['levels'][-1]['windows']):
            T=list(map(unpack,w['history_transfer']));require(len(T)==nh,'history transfer dimension')
            A=sum(t*z for t,z in zip(T,h)); ref=unpack(v12['reference']['windows'][wi]['normalized_value'])
            require(A.overlaps(unpack(old['windows'][wi]['models'][0]['continuum_oracle_discrete_response'])),'archived forward-adjoint response')
            cuts=[]
            for cutoff in p['history_zero_cutoffs']:
                from fractions import Fraction
                cut=float(Fraction(cutoff));mask=x[:nh,0]<=cut
                removed=sum((T[j]*h[j] for j in range(nh) if mask[j]),acb(0))
                changed=sum((T[j]*h[j] for j in range(nh) if not mask[j]),acb(0))
                gain=sum((T[j].abs_upper() for j in range(nh) if mask[j]),arb(0))
                lowergain=sum((T[j].abs_lower() for j in range(nh) if mask[j]),arb(0))
                require((changed-A+removed).contains(0),'exact history-policy response split')
                cuts.append({'cutoff':cutoff,'removed_nodes':int(mask.sum()),'response_change':pack(-removed),
                             'changed_response':pack(changed),'changed_error':pack(changed-ref),
                             'history_sup_gain_lower':pack(lowergain),'history_sup_gain_upper':pack(gain),
                             'interpretation':'zero early prescribed history; NOT omitted exterior tail'})
            wins.append({'window':old['windows'][wi]['time_window'],'baseline_oracle_response':pack(A),'reference':pack(ref),
                'baseline_operator_domain_error':pack(A-ref),'history_gain_lower':pack(sum(t.abs_lower() for t in T)),
                'history_gain_upper':pack(sum(t.abs_upper() for t in T)),'cuts':cuts})
        history.append({'key':key,'history_nodes':nh,'windows':wins})
    out={'schema':p['schema'],'precision_bits':bits,'controls':controls,'paired_archive_diagnosis':pairs,
         'original_detector_history_diagnosis':history,'new_random_calls':0,'new_clouds':0,
         'status':{'fixed_cell_boundary_only_repair':'REJECTED_BY_NECESSARY_OPERATOR_WITNESS',
                   'three_declared_smoothing_choices':'NO_CANDIDATE_QUALIFIED','whole_operator_family':'NOT_REJECTED',
                   'original_detector_operator_vs_exterior_tail':'UNRESOLVED','G1':'HOLD','independent_transfer':'NOT_RUN'},
         'elapsed_seconds':time.monotonic()-start}
    dump(HERE/f'results/DIAGNOSIS_{bits}.json',out)
    print('Completed',bits,'seconds',out['elapsed_seconds'],flush=True)
    return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,choices=[128,192],required=True);args=ap.parse_args();compute(args.bits)
