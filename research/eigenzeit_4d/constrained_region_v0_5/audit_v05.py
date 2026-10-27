"""Audit the corrected center and F with fixed coefficients, never refit k."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import json,math,time
import numpy as np
import constrained as c
import experiment
import validation_controls as controls
from intervals import precision

ROOT=Path(__file__).resolve().parent
assert Path(experiment.__file__).resolve()==ROOT/'experiment.py'
assert Path(controls.__file__).resolve()==ROOT/'validation_controls.py'


def main():
    start=time.monotonic();experiment.check_freeze();precision(60)
    p=json.loads((ROOT/'PROTOCOL.json').read_text());r=json.loads((ROOT/'RESULTS.json').read_text())
    cs=json.loads((ROOT/'CERTIFICATES.json').read_text());data=np.load(ROOT/'fresh_counts.npz')
    gs=json.loads((ROOT.parent/'poisson_v0_2/geometries.json').read_text())
    lookup={(x['level'],x['geometry'],x['repeat']):x for x in cs}
    rng=np.random.Generator(np.random.PCG64(2026102715));checked=wrong=rechecks=directions=mask_checks=0
    for row,record in enumerate(r['records']):
        level=record['level'];gi=row%20;g=gs[gi];M=p['density_expected_outer_counts'][level]
        gen=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi])))
        y=gen.poisson(M*c.baseline.previous.means_from_geometry(g),size=data['cells'][row].shape)
        assert np.array_equal(y,data['cells'][row])
        full=np.zeros((len(y),21),dtype=np.int64);full[:,c.baseline.previous.baseline.PRED]=y@c.C.T
        full[:,c.baseline.previous.baseline.INDEX[(5,6)]]=987654321
        assert np.array_equal(c.baseline.previous.cells_from_counts(full),y);mask_checks+=1
        assert record['selected_validated_certificates']==int(data['metrics'][row,:,9].sum())
        assert record['geometric_validated_certificates']==int(data['metrics'][row,:,6].sum())
        assert record['previous_validated_certificates']==int(data['metrics'][row,:,8].sum())
        target=F(g['tau_squared'])*math.isqrt(M)/abs(F(g['signed_intervals'][c.baseline.previous.baseline.INDEX[(0,6)]]))
        local=[]
        for rep,counts in enumerate(y):
            key=(level,g['id'],rep)
            assert (key in lookup)==bool(data['metrics'][row,rep,9])
            assert not data['metrics'][row,rep,8] or data['metrics'][row,rep,9]
            if key not in lookup:continue
            cert=lookup[key];ql=F(Decimal(cert['q_lower']));qu=F(Decimal(cert['q_upper']))
            pl=F(Decimal(cert['qhat_lower']));pu=F(Decimal(cert['qhat_upper']))
            assert ql>0 and 121*ql>=100*pu and 81*qu<=100*pl
            point=controls.corrected_point(counts,cert['coefficients'])
            assert point.lo<=Decimal(cert['qhat_upper']) and point.hi>=Decimal(cert['qhat_lower'])
            bad=not (pl>=F(81,100)*target and pu<=F(121,100)*target)
            assert bad==bool(data['metrics'][row,rep,10]);wrong+=bad
            if data['metrics'][row,rep,11]<47.999999:assert ql<=target<=qu
            checked+=1;local.append((rep,cert))
        selected=[] if not local else [local[0]] if len(local)==1 else [local[0],local[-1]]
        for rep,cert in selected:
            precision(90)
            proof=c.evaluate(y[rep],True,cert['coefficients']) if cert['method']=='geometric_constraints' else c.baseline.evaluate(y[rep],True)
            precision(60)
            assert proof['certified']
            assert Decimal(cert['qhat_lower'])<=Decimal(proof['qhat_lower'])<=Decimal(proof['qhat_upper'])<=Decimal(cert['qhat_upper'])
            rechecks+=1
            counts=y[rep];u=np.array([int(v)+48+c.ceil_sqrt(48**2+96*int(v)) for v in counts],float)
            z=rng.standard_normal((256,20));z/=np.linalg.norm(z,axis=1)[:,None]
            means=(counts+np.sqrt(96*u)*z)@c.C.T;assert np.all(means>0)
            s=-np.sqrt(means);G=np.einsum('nk,kij->nij',s,c.GS2/2);P=np.einsum('nk,kia->nia',s,c.BP2/2)
            X=np.linalg.solve(G,P);d=P[:,:,0]-P[:,:,1]
            q=-np.einsum('ni,ni->n',d,X[:,:,0]-X[:,:,1])
            residual=np.einsum('nia,nia->na',P,X)-s@c.SP
            # The ambient-region bound is for F_k; k is fixed by the observation.
            corrected=q+residual@(np.array(cert['coefficients'])/c.SCALE)
            assert np.all(corrected>=float(cert['q_lower'])-1e-8) and np.all(corrected<=float(cert['q_upper'])+1e-8)
            directions+=len(z)
    assert checked==len(cs)==r['selected_validated_certificates']
    assert wrong==r['wrong_selected_certificates']
    out={'status':'PASS_INTERNAL_AUDIT','vectors_replayed':int(np.prod(data['cells'].shape[:2])),
         'selected_certificates_checked_with_independent_point_solve':checked,'wrong_selected_certificates':wrong,
         'distinct_precision_90_rechecks':rechecks,'fixed_coefficient_boundary_checks':directions,
         'withheld_count_mask_checks':mask_checks,'frozen_sources_unchanged':True,
         'runtime_seconds':time.monotonic()-start,
         'limits':'Internal audit. The full publication replay recomputes all candidate certificates of both methods. No external review or proof-assistant verification.'}
    (ROOT/'AUDIT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))


if __name__=='__main__':main()
