"""Frozen independent experiment: refined bound versus v0.3 at three budgets."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import collections,datetime,hashlib,json,math,sys,time
import numpy as np
import scipy
from scipy.special import xlog1py
from scipy.stats import beta
import refined,controls

ROOT=Path(__file__).resolve().parent
assert Path(controls.__file__).resolve()==ROOT/'controls.py'
SOURCES=['PROTOCOL.json','THEORY.md','refined.py','controls.py','witnesses.py','development.py','run.py','audit.py','REGION_WITNESSES.json','DEVELOPMENT.json','AMENDMENT.json','ABORT_LOG.txt']
BASE_FILES=['joint_region_v0_3/joint.py','joint_region_v0_3/intervals.py','joint_region_v0_3/fresh_counts.npz','poisson_v0_2/model.py','poisson_v0_2/exact_start.py','poisson_v0_2/geometries.json']


def freeze():
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':'before fresh v0.4 draws',
            'baseline_commit':'8605c9469fa455a07db663b4d533a7cb241dd97e',
            'sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in SOURCES},
            'baseline_sha256':{n:hashlib.sha256((ROOT.parent/n).read_bytes()).hexdigest() for n in BASE_FILES}}
    (ROOT/'FREEZE.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


def check_freeze():
    f=json.loads((ROOT/'FREEZE.json').read_text())
    for n,h in f['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    for n,h in f['baseline_sha256'].items():assert hashlib.sha256((ROOT.parent/n).read_bytes()).hexdigest()==h,n


def main():
    start=time.monotonic();check_freeze();control=controls.main();print(json.dumps(control),flush=True)
    p=json.loads((ROOT/'PROTOCOL.json').read_text())
    gs=json.loads((ROOT.parent/'poisson_v0_2/geometries.json').read_text())
    reps=p['replicates_per_geometry_per_density'];records=[];certificates=[];allcells=[];allmetrics=[]
    for level,M in enumerate(p['density_expected_outer_counts']):
        for gi,g in enumerate(gs):
            mu=M*refined.previous.means_from_geometry(g)
            gen=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi])))
            cells=gen.poisson(mu,size=(reps,20))
            target=F(g['tau_squared'])*math.isqrt(M)/abs(F(g['signed_intervals'][refined.previous.baseline.INDEX[(0,6)]]))
            assert math.isqrt(M)**2==M
            metrics=[];reasons=collections.Counter();oldreasons=collections.Counter()
            for rep,y in enumerate(cells):
                new=refined.evaluate(y,diagnostics=True);old=refined.previous.evaluate(y)
                newcert=oldcert=False;wrong=False
                if new['certified']:
                    proof=refined.evaluate(y,True);newcert=proof['certified'];reasons[proof['reason']]+=1
                    if newcert:
                        ql=F(Decimal(proof['qhat_lower']));qu=F(Decimal(proof['qhat_upper']))
                        wrong=not (ql>=F(81,100)*target and qu<=F(121,100)*target)
                        certificates.append({'level':level,'geometry':g['id'],'repeat':rep,**proof})
                else:reasons[new['reason']]+=1
                if old['certified']:
                    oldproof=refined.previous.evaluate(y,True);oldcert=oldproof['certified'];oldreasons[oldproof['reason']]+=1
                else:oldreasons[old['reason']]+=1
                # The sharper bounds preserve previous accepted observations.
                assert not oldcert or newcert
                if 'error_bound' in old:assert new['error_bound']<=old['error_bound']*(1+1e-10)
                diff=y-mu;nz=mu>0
                div=float(np.sum(xlog1py(y[nz],diff[nz]/mu[nz])-diff[nz]))
                metrics.append([new.get('qhat',np.nan),new.get('first_bound',np.nan),new.get('nonlinear_bound',np.nan),
                                float(new.get('epsilon_upper',np.nan)),new['certified'],newcert,old['certified'],oldcert,wrong,div])
            metrics=np.array(metrics);nc=int(metrics[:,5].sum());oc=int(metrics[:,7].sum())
            cp=0. if nc==0 else float(beta.ppf(.05/20,nc,reps-nc+1))
            records.append({'level':level,'outer_expected_count':M,'budget_multiplier':M//268435456,
                            'geometry':g['id'],'family':g['family'],'replicates':reps,
                            'new_float_candidates':int(metrics[:,4].sum()),'new_validated_certificates':nc,
                            'previous_float_candidates':int(metrics[:,6].sum()),'previous_validated_certificates':oc,
                            'availability_cp_lower':cp,'wrong_new_certificates':int(metrics[:,8].sum()),
                            'joint_region_coverage':int((metrics[:,9]<=48).sum()),
                            'new_reasons':dict(reasons),'previous_reasons':dict(oldreasons)})
            allcells.append(cells);allmetrics.append(metrics)
            if gi%5==4:print(json.dumps({'level':level,'geometries_done':gi+1,'new_certificates':sum(x['new_validated_certificates'] for x in records if x['level']==level)}),flush=True)
    primary=[x for x in records if x['level']==p['primary_density_index']]
    out={'version':'0.4','status':'COMPLETED','date':'2026-10-27','controls':control,
         'fresh_observations':len(gs)*len(p['density_expected_outer_counts'])*reps,
         'new_validated_certificates':sum(x['new_validated_certificates'] for x in records),
         'previous_validated_certificates':sum(x['previous_validated_certificates'] for x in records),
         'wrong_new_certificates':sum(x['wrong_new_certificates'] for x in records),
         'primary_expanded_budget_gate_pass':all(x['availability_cp_lower']>=.9 for x in primary),
         'records':records,'runtime_seconds':time.monotonic()-start,
         'environment':{'numpy':np.__version__,'scipy':scipy.__version__},
         'freeze_sha256':hashlib.sha256((ROOT/'FREEZE.json').read_bytes()).hexdigest()}
    np.savez_compressed(ROOT/'fresh_counts.npz',cells=np.array(allcells),metrics=np.array(allmetrics))
    (ROOT/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    (ROOT/'CERTIFICATES.json').write_text(json.dumps(certificates,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['records','environment','controls']}),flush=True)


if __name__=='__main__':
    if '--freeze-only' in sys.argv:freeze()
    else:main()
