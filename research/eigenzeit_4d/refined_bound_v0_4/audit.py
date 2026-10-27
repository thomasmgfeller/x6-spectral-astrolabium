"""Independent point solves, exact issue checks, seed replay and stress audit."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import json,math,time
import numpy as np
import refined,witnesses,run
from intervals import precision

ROOT=Path(__file__).resolve().parent
assert Path(run.__file__).resolve()==ROOT/'run.py'
assert Path(witnesses.__file__).resolve()==ROOT/'witnesses.py'


def main():
    start=time.monotonic();run.check_freeze();precision(60)
    p=json.loads((ROOT/'PROTOCOL.json').read_text());r=json.loads((ROOT/'RESULTS.json').read_text())
    cs=json.loads((ROOT/'CERTIFICATES.json').read_text());data=np.load(ROOT/'fresh_counts.npz')
    gs=json.loads((ROOT.parent/'poisson_v0_2/geometries.json').read_text())
    lookup={(c['level'],c['geometry'],c['repeat']):c for c in cs}
    rng=np.random.Generator(np.random.PCG64(2026102711))
    checked=0;rechecks=0;directions=0;mask_checks=0;wrong=0
    for row,record in enumerate(r['records']):
        level=record['level'];gi=row%20;g=gs[gi];M=p['density_expected_outer_counts'][level]
        gen=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi])))
        replay=gen.poisson(M*refined.previous.means_from_geometry(g),size=data['cells'][row].shape)
        assert np.array_equal(replay,data['cells'][row])
        full=np.zeros((len(replay),21),dtype=np.int64)
        full[:,refined.previous.baseline.PRED]=replay@refined.C.T
        full[:,refined.previous.baseline.INDEX[(5,6)]]=123456789
        assert np.array_equal(refined.previous.cells_from_counts(full),replay);mask_checks+=1
        assert record['new_validated_certificates']==int(data['metrics'][row,:,5].sum())
        assert record['previous_validated_certificates']==int(data['metrics'][row,:,7].sum())
        target=F(g['tau_squared'])*math.isqrt(M)/abs(F(g['signed_intervals'][refined.previous.baseline.INDEX[(0,6)]]))
        local=[]
        for rep,y in enumerate(replay):
            key=(level,g['id'],rep)
            assert (key in lookup)==bool(data['metrics'][row,rep,5])
            if key not in lookup:continue
            c=lookup[key];ql=F(Decimal(c['q_lower']));qu=F(Decimal(c['q_upper']))
            pl=F(Decimal(c['qhat_lower']));pu=F(Decimal(c['qhat_upper']))
            assert ql>0 and 121*ql>=100*pu and 81*qu<=100*pl
            point=witnesses.point_interval(y)
            assert point.lo<=Decimal(c['qhat_upper']) and point.hi>=Decimal(c['qhat_lower'])
            bad=not (pl>=F(81,100)*target and pu<=F(121,100)*target)
            assert bad==bool(data['metrics'][row,rep,8]);wrong+=bad
            if data['metrics'][row,rep,9]<47.999999:assert ql<=target<=qu
            checked+=1;local.append((rep,c))
        for rep,c in ([local[0],local[-1]] if local else []):
            precision(90);new=refined.evaluate(replay[rep],True);precision(60)
            assert new['certified']
            assert Decimal(c['qhat_lower'])<=Decimal(new['qhat_lower'])<=Decimal(new['qhat_upper'])<=Decimal(c['qhat_upper'])
            rechecks+=1
            y=replay[rep];u=np.array([int(v)+48+refined.ceil_sqrt(48**2+96*int(v)) for v in y],float)
            z=rng.standard_normal((256,20));z/=np.linalg.norm(z,axis=1)[:,None]
            means=(y+np.sqrt(96*u)*z)@refined.C.T
            assert np.all(means>0)
            s=np.zeros((len(z),21));s[:,refined.previous.baseline.PRED]=-np.sqrt(means)
            G,d=refined.previous.baseline.build_system(s);w=np.linalg.solve(G,d[...,None])[...,0]
            q=-np.einsum('ni,ni->n',d,w)
            assert np.all(q>=float(c['q_lower'])-1e-8) and np.all(q<=float(c['q_upper'])+1e-8)
            directions+=len(z)
    assert checked==len(cs)==r['new_validated_certificates']
    assert wrong==r['wrong_new_certificates']
    out={'status':'PASS_INTERNAL_AUDIT','vectors_replayed':int(np.prod(data['cells'].shape[:2])),
         'issued_certificates_checked_with_independent_point_solve':checked,'wrong_issued_certificates':wrong,
         'precision_90_rechecks':rechecks,'ellipsoid_boundary_direction_checks':directions,
         'withheld_count_mask_checks':mask_checks,'frozen_sources_unchanged':True,
         'runtime_seconds':time.monotonic()-start,
         'limits':'Internal audit; not external review or proof-assistant verification. The publication replay separately recomputes every 60-digit certificate of both methods.'}
    (ROOT/'AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':main()
