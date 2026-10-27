"""Post-run internal audit: replay, direct-cloud atoms, and Decimal elimination.
This audit is not independent external replication and does not change gates.
"""
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
import hashlib,json
import numpy as np
from scipy.stats import poisson
import model as m

ROOT=Path(__file__).resolve().parent

def decimal_tau(counts,outerW,budget):
    """Separate solver: two point coordinates, Decimal Gaussian elimination."""
    with localcontext() as ctx:
        ctx.prec=80
        ow=F(outerW); factor=D(ow.numerator)/D(ow.denominator)/D(budget)
        S=[[D(0) for _ in range(7)] for _ in range(7)]
        for k,(i,j) in enumerate(m.PAIRS):
            S[i][j]=S[j][i]=-(D(int(counts[k]))*factor).sqrt()
        G=[[(S[0][i]+S[0][j]-S[i][j])/2 for j in range(1,5)] for i in range(1,5)]
        def solve(rhs):
            a=[row[:]+[y] for row,y in zip(G,rhs)]
            for k in range(4):
                pivot=max(range(k,4),key=lambda j:abs(a[j][k]))
                a[k],a[pivot]=a[pivot],a[k]
                divisor=a[k][k]
                if divisor==0:raise ValueError('singular')
                a[k]=[x/divisor for x in a[k]]
                for j in range(4):
                    if j!=k:
                        mul=a[j][k]; a[j]=[x-mul*y for x,y in zip(a[j],a[k])]
            return [row[-1] for row in a]
        cp=solve([(S[0][i]+S[0][5]-S[i][5])/2 for i in range(1,5)])
        cq=solve([(S[0][i]+S[0][6]-S[i][6])/2 for i in range(1,5)])
        dc=[x-y for x,y in zip(cp,cq)]
        tau2=-sum(dc[i]*G[i][j]*dc[j] for i in range(4) for j in range(4))
        return float(tau2.sqrt()) if tau2>0 else None

def main():
    p=json.loads((ROOT/'PROTOCOL.json').read_text()); gs=json.loads((ROOT/'geometries.json').read_text())
    r=json.loads((ROOT/'RESULTS.json').read_text()); f=json.loads((ROOT/'FREEZE.json').read_text())
    for name,h in f['sha256'].items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
    data=np.load(ROOT/'campaign_arrays.npz'); direct=np.load(ROOT/'direct_cloud_counts.npz')['counts']
    maxrel=0.; decimal_checks=0; replay_vectors=0; selected=[]
    summaries=[]
    for row,record in enumerate(r['records']):
        level=record['level']; gi=row%len(gs); g=gs[gi]
        a=m.arrays(g); budget=p['outer_expected_counts'][level]; reps=record['replicates']
        rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi,0])))
        replay=rng.poisson(budget*a['atom_ratios'],size=(reps,21))@m.B.T
        assert np.array_equal(replay,data['counts'][row])
        rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['count_seed'],level,gi,1])))
        assert np.array_equal(rng.poisson(budget*a['volume_ratios'],size=(reps,21)),data['iid_negative'][row])
        replay_vectors+=reps
        values=data['metrics'][row,:,0]; valid=np.flatnonzero(np.isfinite(values))
        if len(valid):
            worst=valid[np.argmax(abs(values[valid]/record['true_tau']-1))]
            for i in sorted(set([int(valid[0]),int(worst)])):
                ref=decimal_tau(data['counts'][row,i],g['outer_W'],budget)
                assert ref is not None
                rel=abs(values[i]/ref-1); maxrel=max(maxrel,rel); decimal_checks+=1
                assert rel<1e-7,(row,i,rel)
                selected.append({'cell':row,'repeat':i,'relative_difference':rel})
    # Mobius inversion of independently sprinkled clouds: realized atom counts.
    atom_ps=[]; direct_replay=0
    for gi,g in enumerate(gs[:4]):
        cc=direct[gi]; atoms=[]
        def read(i,j):return cc[:,m.INDEX[(i,j)]] if i<j else np.zeros(len(cc),dtype=np.int64)
        for i,j in m.PAIRS:
            atoms.append(read(i,j)-read(i+1,j)-read(i,j-1)+read(i+1,j-1))
        atoms=np.array(atoms).T
        assert np.all(atoms>=0)
        assert np.array_equal(atoms@m.B.T,cc)
        mu=p['direct_cloud_check']['outer_expected_count']*m.arrays(g)['atom_ratios']*len(cc)
        total=atoms.sum(axis=0)
        ps=np.minimum(1,2*np.minimum(poisson.cdf(total,mu),poisson.sf(total-1,mu)))
        atom_ps.extend(ps.tolist())
        # Repeat the separate spatial point sampler, not the atom simulator.
        rng=np.random.Generator(np.random.PCG64(np.random.SeedSequence([p['direct_cloud_seed'],gi])))
        points=np.array([[float(F(x)) for x in pt] for pt in g['points']])
        for i in range(len(cc)):
            n=rng.poisson(p['direct_cloud_check']['outer_expected_count'])
            cloud=m.sample_diamond(rng,n,points[0],points[-1])
            assert np.array_equal(m.cloud_counts(cloud,points),cc[i]); direct_replay+=1
    # Atom goodness check is post-run diagnostic, not a replacement primary gate.
    atom_pass=min(atom_ps)>=.01/len(atom_ps)
    for level,budget in enumerate(p['outer_expected_counts']):
        cells=[x for x in r['records'] if x['level']==level]
        ids=[i for i,x in enumerate(r['records']) if x['level']==level]
        met=data['metrics'][ids]; bound=data['bounds'][ids]
        true=np.array([x['true_tau'] for x in cells])[:,None]
        raw=np.isfinite(met[:,:,0])&(abs(met[:,:,0]/true-1)<=.1)
        summary={'outer_expected_count':budget,'replicates':sum(x['replicates'] for x in cells),
                 'valid':sum(x['primary']['valid'] for x in cells),
                 'count_eligible':sum(x['primary']['count_eligible'] for x in cells),
                 'valid_and_error_le_10pct_without_count_guard':int(raw.sum()),
                 'full_success':sum(x['primary']['success_10pct'] for x in cells),
                 'finite_intervals':sum(x['finite_tau_intervals'] for x in cells),
                 'certificate_10pct':sum(x['certificate_10pct'] for x in cells),
                 'mean_box_coverage':sum(x['simultaneous_mean_box_coverage'] for x in cells),
                 'direct_count_success':sum(x['direct_count_success_10pct'] for x in cells),
                 'oracle_anchor_success':sum(x['oracle_anchor_diagnostic']['success_10pct'] for x in cells),
                 'iid_negative_control_success':sum(x['iid_negative_control']['success_10pct'] for x in cells)}
        summaries.append(summary)
    audit={'status':'PASS_INTERNAL_AUDIT','frozen_files_unchanged':True,
           'joint_count_vectors_replayed':replay_vectors,'iid_count_vectors_replayed':replay_vectors,
           'direct_cloud_vectors_replayed':direct_replay,'direct_atom_inversion_nonnegative':True,
           'posthoc_direct_atom_p_min':min(atom_ps),'posthoc_direct_atom_bonferroni_threshold':.01/len(atom_ps),
           'posthoc_direct_atom_check_pass':atom_pass,
           'decimal_precision_digits':80,'decimal_checks':decimal_checks,'decimal_max_relative_difference':maxrel,
           'decimal_selected':selected,'summaries':summaries,
           'limits':'Internal replay and separate numerical method; not independent external validation. No new scientific gates.'}
    assert atom_pass
    (ROOT/'AUDIT.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(json.dumps({k:v for k,v in audit.items() if k not in ['decimal_selected','summaries']},indent=2))
    print(json.dumps(summaries,indent=2))

if __name__=='__main__':main()
