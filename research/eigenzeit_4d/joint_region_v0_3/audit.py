"""Internal audit, full seed replay and every issued interval certificate."""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal
import hashlib,json,math,time
import numpy as np
import joint
from intervals import precision

ROOT=Path(__file__).resolve().parent

def main():
    start=time.monotonic();p=json.loads((ROOT/'PROTOCOL.json').read_text())
    r=json.loads((ROOT/'RESULTS.json').read_text());cs=json.loads((ROOT/'CERTIFICATES.json').read_text())
    gs=json.loads((ROOT.parent/'poisson_v0_2/geometries.json').read_text());a=np.load(ROOT/'fresh_counts.npz')
    f=json.loads((ROOT/'FREEZE.json').read_text())
    for n,h in f['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h
    for n,h in f['baseline_sha256'].items():assert hashlib.sha256((ROOT.parent/'poisson_v0_2'/n).read_bytes()).hexdigest()==h
    rng=np.random.Generator(np.random.PCG64(2026102707));precision(60)
    checked=0;directions=0;point_error=0.;mask_checks=0
    cert_lookup={(x['level'],x['geometry'],x['repeat']):x for x in cs}
    for row,record in enumerate(r['records']):
        level=record['level'];gi=row%20;M=p['density_expected_outer_counts'][level];g=gs[gi]
        gen=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi])))
        replay=gen.poisson(M*joint.means_from_geometry(g),size=a['cells'][row].shape)
        assert np.array_equal(replay,a['cells'][row])
        full=np.zeros((len(replay),21),dtype=np.int64);full[:,joint.baseline.PRED]=replay@joint.C.T
        full[:,joint.baseline.INDEX[(5,6)]]=987654321
        assert np.array_equal(joint.cells_from_counts(full),replay);mask_checks+=1
        existing=[]
        for rep in range(len(replay)):
            cand=joint.evaluate(replay[rep])
            assert bool(cand['certified'])==bool(a['metrics'][row,rep,4])
            key=(level,g['id'],rep)
            if key in cert_lookup:
                ref=cert_lookup[key]; proof=joint.evaluate(replay[rep],True)
                assert proof['certified']
                assert all(proof[k]==ref[k] for k in proof),key
                qlo=F(Decimal(proof['q_lower']));qhi=F(Decimal(proof['q_upper']))
                assert qlo*121>=F(Decimal(proof['qhat_upper']))*100
                assert qhi*81<=F(Decimal(proof['qhat_lower']))*100
                checked+=1;existing.append((rep,proof))
        # Additional stress diagnosis; not a substitute for the analytic bound.
        for rep,proof in ([existing[0],existing[-1]] if existing else []):
            y=replay[rep];u=np.array([int(v)+48+joint.ceil_sqrt(48**2+96*int(v)) for v in y],float)
            z=rng.standard_normal((512,20));z/=np.linalg.norm(z,axis=1)[:,None]
            alternatives=y+np.sqrt(96*u)*z
            intervals=alternatives@joint.C.T
            assert np.all(intervals>0)
            s=np.zeros((len(z),21));s[:,joint.baseline.PRED]=-np.sqrt(intervals)
            G,d=joint.baseline.build_system(s);w=np.linalg.solve(G,d[...,None])[...,0]
            q=-np.einsum('ni,ni->n',d,w)
            lo=float(proof['q_lower']);hi=float(proof['q_upper'])
            assert np.all(q>=lo-1e-8) and np.all(q<=hi+1e-8)
            directions+=len(z)
            # Separate unwhitened solve at the observed count center.
            s[:]=0;s[:,joint.baseline.PRED]=-np.sqrt(y@joint.C.T)
            G,d=joint.baseline.build_system(s[:1]);qp=-d[0]@np.linalg.solve(G[0],d[0])
            reference=(float(proof['qhat_lower'])+float(proof['qhat_upper']))/2
            point_error=max(point_error,abs(qp/reference-1))
    assert checked==r['validated_certificates']==len(cs)
    assert point_error<1e-7
    out={'status':'PASS_INTERNAL_AUDIT','fresh_vectors_replayed':int(a['cells'].shape[0]*a['cells'].shape[1]),
         'all_issued_certificates_recomputed':checked,'withheld_count_mask_checks':mask_checks,
         'ellipsoid_boundary_direction_checks':directions,'separate_point_solve_max_relative_error':point_error,
         'frozen_sources_unchanged':True,'runtime_seconds':time.monotonic()-start,
         'limits':'Internal verified arithmetic and computational checks; not independent external review or proof-assistant verification.'}
    (ROOT/'AUDIT.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
