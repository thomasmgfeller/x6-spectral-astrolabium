"""Post-run audit, not part of fitting or success-threshold selection.
SPDX-License-Identifier: Apache-2.0
"""
import gzip,hashlib,json
from pathlib import Path
import numpy as np
from fit import estimate, input_mask, SOURCE
from run import frozen,encode,save

HERE=Path(__file__).resolve().parent
def main():
    frozen();c=json.loads((HERE/'contract.json').read_text());checks={};nrecords=0;nfits=0
    max_moment=0.;max_weights=0.;max_objective=0.;replay=[]
    # Verify all inherited archive files against the previously published manifest.
    nsource=0
    for line in (SOURCE/'SHA256SUMS.txt').read_text().splitlines():
        if not line.strip():continue
        digest,name=line.split(maxsplit=1);name=name.lstrip('* ')
        assert hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()==digest,name
        nsource+=1
    for mode in ['archive','results']:
        root=HERE/mode;records=[]
        for index in range(c['clouds']):
            path=root/f'cloud-{index:02d}.json.gz';raw=path.read_bytes();row=json.loads(gzip.decompress(raw));nrecords+=1
            assert row['selection_seal']==hashlib.sha256(encode(row['selection'])).hexdigest()
            if not row['replicates']:continue
            truth=json.loads((root/f'truth/cloud-{index:02d}.json').read_text())
            assert truth['inference_sha256']==hashlib.sha256(raw).hexdigest()
            p=row['selection']['fourth']['packet'];ids=p['landmarks']+[p['root']]+p['support'];lookup={a:i for i,a in enumerate(ids)}
            assert truth['ids']==ids
            true=np.array(truth['points']);d=true[None]-true[:,None]
            true_order=(d[:,:,0]>0)&(d[:,:,0]**2>d[:,:,1]**2+d[:,:,2]**2)
            assert np.array_equal(true_order,p['full_order'])
            for rr in row['replicates']:
                fit=rr['fit'];obs=rr['observed'];counts=np.array(obs['counts']);overlap=np.array(obs['overlaps'])
                assert np.array_equal(overlap,overlap.T) and np.array_equal(np.diag(overlap),counts)
                assert all(obs['intersection_replay'])
                if not fit.get('qualified'):continue
                nfits+=1;z=np.array(fit['coordinates']);w=np.array(fit['weights']);scale=p['scale']
                assert fit['optimizer_success'] and fit['status']=='WEIGHTS_VALID'
                # Independently write the scalar interval and full directed-order checks.
                observed=np.array(p['full_order'],bool)
                for a in range(len(z)):
                    for b in range(a+1,len(z)):
                        dt,dx,dy=z[b]-z[a];interval=dx*dx+dy*dy-dt*dt
                        assert bool(dt>0 and interval<0)==observed[a,b]
                        assert bool(dt<0 and interval<0)==observed[b,a]
                        signed=-interval if observed[a,b] or observed[b,a] else interval
                        assert signed>=c['fit']['interval_margin']-c['fit']['constraint_tolerance']
                u=z[5:]-z[4];t,x,y=u.T
                D=np.array([t,x,y,t*t,x*x,y*y,t*x,t*y,x*y])
                target=np.array([0,0,0,-2,2,2,0,0,0.])
                err=float(np.max(abs(D@(w[1:]*scale**2)-target)))
                max_moment=max(max_moment,err);assert err<1e-6
                assert abs(w.sum())<1e-7*(1+max(abs(w)))
                # Independent direct coordinate moment solve, without Gram inversion.
                H=np.eye(len(u))+np.ones((len(u),len(u)))
                HinvDt=np.linalg.solve(H,D.T)
                direct=HinvDt@np.linalg.solve(D@HinvDt,target)
                full=np.r_[-direct.sum(),direct]/scale**2
                error=float(np.max(abs(full-w)/(1+abs(w))))
                max_weights=max(max_weights,error);assert error<1e-5
                mask=input_mask(p);lam=[]
                for a,b in np.array(p['pairs'])[mask]:
                    dt,dx,dy=z[lookup[b]]-z[lookup[a]]
                    q=dt*dt-dx*dx-dy*dy;assert q>0
                    lam.append(c['count_density']*np.pi/12*scale**3*q**1.5)
                lam=np.array(lam);n=counts[mask]
                dev=float(2*np.mean(lam-n+n*np.log(n/lam)))
                error=abs(dev-fit['objective']);max_objective=max(max_objective,error);assert error<1e-7
            records.append((row,truth))
        if mode=='results' and records:
            # Fixed endpoint samples of successful selection, no favorable-case search.
            from simulation import counting_cloud
            for row,truth in [records[0],records[-1]]:
                p=row['selection']['fourth']['packet'];rr=row['replicates'][0]
                observed=counting_cloud(dict(points=np.array(truth['points']),ids=truth['ids']),p,row['seed'],0,c)
                assert encode(observed)==encode(rr['observed'])
                fitted=estimate(p,observed['counts'],c['count_density'],c['fit'])
                assert fitted['status']==rr['fit']['status']
                if fitted.get('qualified'):
                    assert np.max(abs(np.array(fitted['weights'])-rr['fit']['weights']))<1e-8
                replay.append(dict(index=row['index'],count_cloud_identical=True,inference_status_identical=True,weights_equal_within_1e_minus_8=True))
    out=dict(status='PASS',source_manifest_entries=nsource,records=nrecords,qualified_fits_checked=nfits,max_direct_moment_residual=max_moment,max_relative_direct_weight_difference=max_weights,max_deviance_difference=max_objective,deterministic_replays=replay,scope='Internal numerical and integrity audit, not external replication or global optimality certificate. Audit added after freeze; no fitting or criteria changed.')
    if not (HERE/'verification.json').exists():save(HERE/'verification.json',out)
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
