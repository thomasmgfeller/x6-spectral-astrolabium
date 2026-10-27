"""Frozen paired comparison of geometric correction and v0.4."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import collections,datetime,hashlib,json,math,sys,time
import numpy as np
import scipy
from scipy.special import xlog1py
from scipy.stats import beta
import constrained as c
import validation_controls as controls

ROOT=Path(__file__).resolve().parent
assert Path(c.__file__).resolve()==ROOT/'constrained.py'
assert Path(controls.__file__).resolve()==ROOT/'validation_controls.py'
SOURCES=['PROTOCOL.json','THEORY.md','constrained.py','validation_controls.py','experiment.py','audit_v05.py','development.py','DEVELOPMENT.json']
BASE_FILES=['refined_bound_v0_4/refined.py','refined_bound_v0_4/witnesses.py','refined_bound_v0_4/realizability.py',
            'refined_bound_v0_4/fresh_counts.npz','refined_bound_v0_4/RESULTS.json',
            'joint_region_v0_3/joint.py','joint_region_v0_3/intervals.py',
            'poisson_v0_2/model.py','poisson_v0_2/exact_start.py','poisson_v0_2/geometries.json']


def freeze():
    d={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':'before fresh v0.5 draws',
       'baseline_commit':'5507bf0b1664778877d7582ebb8f30095d6745d9',
       'sha256':{n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in SOURCES},
       'baseline_sha256':{n:hashlib.sha256((ROOT.parent/n).read_bytes()).hexdigest() for n in BASE_FILES}}
    (ROOT/'FREEZE.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))


def check_freeze():
    f=json.loads((ROOT/'FREEZE.json').read_text())
    for n,h in f['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    for n,h in f['baseline_sha256'].items():assert hashlib.sha256((ROOT.parent/n).read_bytes()).hexdigest()==h,n


def main():
    start=time.monotonic();check_freeze();control=controls.main();print(json.dumps(control),flush=True)
    p=json.loads((ROOT/'PROTOCOL.json').read_text());gs=json.loads((ROOT.parent/'poisson_v0_2/geometries.json').read_text())
    reps=p['replicates_per_geometry_per_density'];records=[];certificates=[];cells_all=[];metrics_all=[]
    for level,M in enumerate(p['density_expected_outer_counts']):
        for gi,g in enumerate(gs):
            mu=M*c.baseline.previous.means_from_geometry(g)
            gen=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi])))
            cells=gen.poisson(mu,size=(reps,20))
            target=F(g['tau_squared'])*math.isqrt(M)/abs(F(g['signed_intervals'][c.baseline.previous.baseline.INDEX[(0,6)]]))
            assert math.isqrt(M)**2==M
            metrics=[];reasons=collections.Counter()
            for rep,y in enumerate(cells):
                geometric=c.evaluate(y,diagnostics=True);old=c.baseline.evaluate(y)
                gp=op=None;wrong=False;selected=None
                if geometric['certified']:gp=c.evaluate(y,True,geometric['coefficients'])
                if old['certified']:op=c.baseline.evaluate(y,True)
                gc=bool(gp and gp['certified']);oc=bool(op and op['certified'])
                if gc:selected=gp
                elif oc:selected={**op,'method':'v0.4_fallback','coefficients':[0,0],'coefficient_denominator':c.SCALE}
                if selected:
                    pl=F(Decimal(selected['qhat_lower']));pu=F(Decimal(selected['qhat_upper']))
                    wrong=not (pl>=F(81,100)*target and pu<=F(121,100)*target)
                    certificates.append({'level':level,'geometry':g['id'],'repeat':rep,**selected})
                    reasons[selected['method']]+=1
                else:reasons[gp['reason'] if gp else geometric['reason']]+=1
                diff=y-mu;nz=mu>0
                div=float(np.sum(xlog1py(y[nz],diff[nz]/mu[nz])-diff[nz]))
                metrics.append([geometric.get('qhat',np.nan),geometric.get('raw_qhat',np.nan),
                                float(geometric.get('epsilon_upper',np.nan)),geometric.get('first_bound',np.nan),
                                geometric.get('nonlinear_bound',np.nan),geometric['certified'],gc,
                                old['certified'],oc,selected is not None,wrong,div])
            metrics=np.array(metrics);nc=int(metrics[:,9].sum());oc=int(metrics[:,8].sum());gc=int(metrics[:,6].sum())
            cp=0. if nc==0 else float(beta.ppf(.05/20,nc,reps-nc+1))
            records.append({'level':level,'outer_expected_count':M,'budget_multiplier':M//268435456,
                            'geometry':g['id'],'family':g['family'],'replicates':reps,
                            'geometric_float_candidates':int(metrics[:,5].sum()),'geometric_validated_certificates':gc,
                            'previous_float_candidates':int(metrics[:,7].sum()),'previous_validated_certificates':oc,
                            'selected_validated_certificates':nc,'fallback_certificates':nc-gc,
                            'availability_cp_lower':cp,'wrong_selected_certificates':int(metrics[:,10].sum()),
                            'joint_region_coverage':int((metrics[:,11]<=48).sum()),'reasons':dict(reasons)})
            cells_all.append(cells);metrics_all.append(metrics)
            if gi%5==4:print(json.dumps({'level':level,'geometries_done':gi+1,
                'selected_certificates':sum(x['selected_validated_certificates'] for x in records if x['level']==level)}),flush=True)
    primary=[x for x in records if x['level']==p['primary_density_index']]
    out={'version':'0.5','status':'COMPLETED','date':'2026-10-27','controls':control,
         'fresh_observations':len(gs)*len(p['density_expected_outer_counts'])*reps,
         'selected_validated_certificates':sum(x['selected_validated_certificates'] for x in records),
         'geometric_validated_certificates':sum(x['geometric_validated_certificates'] for x in records),
         'previous_validated_certificates':sum(x['previous_validated_certificates'] for x in records),
         'wrong_selected_certificates':sum(x['wrong_selected_certificates'] for x in records),
         'primary_fixed_geometry_gate_pass':all(x['availability_cp_lower']>=.9 for x in primary),
         'records':records,'runtime_seconds':time.monotonic()-start,
         'environment':{'numpy':np.__version__,'scipy':scipy.__version__},
         'freeze_sha256':hashlib.sha256((ROOT/'FREEZE.json').read_bytes()).hexdigest()}
    np.savez_compressed(ROOT/'fresh_counts.npz',cells=np.array(cells_all),metrics=np.array(metrics_all))
    (ROOT/'CERTIFICATES.json').write_text(json.dumps(certificates,indent=2)+'\n')
    (ROOT/'RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['records','environment','controls']}),flush=True)


if __name__=='__main__':
    if '--freeze-only' in sys.argv:freeze()
    else:main()
