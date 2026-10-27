"""Frozen fresh-count joint-region experiment, with validated issue decisions."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import collections,datetime,hashlib,json,math,sys,time
import numpy as np
import scipy
from scipy.special import xlog1py
from scipy.stats import beta
import joint,controls
from intervals import precision

ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'poisson_v0_2'
SOURCES=['PROTOCOL.json','THEORY.md','joint.py','intervals.py','controls.py','run.py']

def freeze():
    d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'stage':'before new target draws','baseline_publication_commit':'0c62d3a5af6b25bb942b2078f817d6ef7d461be8',
       'sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in SOURCES},
       'baseline_sha256':{n:hashlib.sha256((BASE/n).read_bytes()).hexdigest() for n in ['model.py','exact_start.py','geometries.json']}}
    (ROOT/'FREEZE.json').write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps(d,indent=2))

def cp(k,n):return 0. if k==0 else float(beta.ppf(.05/20,k,n-k+1))

def main():
    start=time.monotonic();f=json.loads((ROOT/'FREEZE.json').read_text())
    for name,h in f['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
    for name,h in f['baseline_sha256'].items():assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==h
    control=controls.main();print(json.dumps(control),flush=True)
    p=json.loads((ROOT/'PROTOCOL.json').read_text());gs=json.loads((BASE/'geometries.json').read_text())
    reps=p['replicates_per_geometry_per_density'];records=[];certificates=[];allcells=[];allmetrics=[]
    rechecks=0
    for level,M in enumerate(p['density_expected_outer_counts']):
        for gi,g in enumerate(gs):
            mu=M*joint.means_from_geometry(g)
            rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi])))
            y=rng.poisson(mu,size=(reps,20));observed=y@joint.C.T
            full=np.zeros((reps,21),dtype=np.int64);full[:,joint.baseline.PRED]=observed
            assert np.array_equal(joint.cells_from_counts(full),y)
            rho=M/(np.pi/24*float(F(g['outer_W'])))
            oldrec=joint.baseline.reconstruct(full,rho);oldbounds=joint.baseline.uncertainty(full,rho,oldrec)
            outer_s=F(g['signed_intervals'][joint.baseline.INDEX[(0,6)]])
            assert math.isqrt(M)**2==M
            trueq=F(g['tau_squared'])*math.isqrt(M)/abs(outer_s)
            delta=y-mu;kl=np.zeros_like(delta,dtype=float)
            nz=mu>0;kl[:,nz]=xlog1py(y[:,nz],delta[:,nz]/mu[nz])-delta[:,nz]
            kl[y==0]=np.broadcast_to(mu,y.shape)[y==0]
            divergences=kl.sum(axis=1)
            cert=np.zeros(reps,dtype=bool);candidate=np.zeros(reps,dtype=bool)
            wrong=np.zeros(reps,dtype=bool);finite=np.zeros(reps,dtype=bool)
            qhat=np.full(reps,np.nan);ql=np.zeros(reps);qu=np.full(reps,np.inf)
            reasons=collections.Counter();local=[]
            for rep in range(reps):
                floating=joint.evaluate(y[rep]);candidate[rep]=floating['certified']
                if 'qhat' in floating:qhat[rep]=floating['qhat'];ql[rep]=floating['q_lower'];qu[rep]=floating['q_upper'];finite[rep]=True
                if candidate[rep]:
                    proof=joint.evaluate(y[rep],rigorous=True)
                    reasons[proof['reason']]+=1;cert[rep]=proof['certified']
                    if cert[rep]:
                        low=F(Decimal(proof['q_lower']));high=F(Decimal(proof['q_upper']))
                        qlo=F(Decimal(proof['qhat_lower']));qhi=F(Decimal(proof['qhat_upper']))
                        assert low*121>=qhi*100 and high*81<=qlo*100
                        # Known simulation target is used for evaluation only.
                        wrong[rep]=not (qlo>=F(81,100)*trueq and qhi<=F(121,100)*trueq)
                        if divergences[rep]<47.999999:assert low<=trueq<=high
                        local.append((rep,proof));certificates.append({'level':level,'geometry':g['id'],'repeat':rep,**proof})
                else:reasons[floating['reason']]+=1
            if local:
                precision(90)
                for rep,old in [local[0],local[-1]]:
                    new=joint.evaluate(y[rep],rigorous=True)
                    assert new['certified']
                    assert Decimal(old['qhat_lower'])<=Decimal(new['qhat_lower'])<=Decimal(new['qhat_upper'])<=Decimal(old['qhat_upper'])
                    rechecks+=1
                precision(60)
            records.append({'level':level,'outer_expected_count':M,'geometry':g['id'],'family':g['family'],'epsilon':g['epsilon'],
                            'replicates':reps,'float_candidates':int(candidate.sum()),'validated_certificates':int(cert.sum()),
                            'certificate_cp_lower':cp(int(cert.sum()),reps),'wrong_issued_certificates':int(wrong.sum()),
                            'old_10pct_certificates':int(oldbounds['certificate_10pct'].sum()),
                            'joint_region_coverage':int((divergences<=48).sum()),'max_joint_divergence':float(divergences.max()),
                            'reasons':dict(reasons)})
            allcells.append(y)
            allmetrics.append(np.column_stack([qhat,ql,qu,finite,candidate,cert,wrong,oldbounds['certificate_10pct'],divergences]))
            if gi%5==4:print(json.dumps({'level':level,'geometries_done':gi+1,'certificates':sum(r['validated_certificates'] for r in records if r['level']==level)}),flush=True)
    primary=[r for r in records if r['level']==p['primary_density_index']]
    result={'version':'0.3','status':'COMPLETED','date':'2026-10-27','controls':control,
            'fresh_observations':len(gs)*len(p['density_expected_outer_counts'])*reps,
            'certificate_availability_gate_pass':all(r['certificate_cp_lower']>=.9 for r in primary),
            'validated_certificates':sum(r['validated_certificates'] for r in records),
            'wrong_issued_certificates':sum(r['wrong_issued_certificates'] for r in records),
            'precision_90_rechecks':rechecks,'records':records,'runtime_seconds':time.monotonic()-start,
            'environment':{'numpy':np.__version__,'scipy':scipy.__version__},
            'freeze_sha256':hashlib.sha256((ROOT/'FREEZE.json').read_bytes()).hexdigest()}
    np.savez_compressed(ROOT/'fresh_counts.npz',cells=np.array(allcells),metrics=np.array(allmetrics))
    (ROOT/'CERTIFICATES.json').write_text(json.dumps(certificates,indent=2)+'\n')
    (ROOT/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['fresh_observations','validated_certificates','wrong_issued_certificates','certificate_availability_gate_pass','runtime_seconds']}),flush=True)

if __name__=='__main__':
    if '--freeze-only' in sys.argv:freeze()
    else:main()
