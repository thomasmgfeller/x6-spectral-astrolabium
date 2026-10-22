"""Replay frozen diagnostics and independently certify the finite witness.
SPDX-License-Identifier: Apache-2.0
"""
import argparse
from collections import Counter
import hashlib
import numpy as np
from st_common import HERE, read, save, frozen
from st_model import Stability
from st_certificate import build_witness, certify
import st_controls


def audit():
    frozen();cfg=read(HERE/'contract.json');execution=read(HERE/'execution.json')
    assert execution['status']=='COMPLETE'
    paths=sorted((HERE/'results').glob('cloud-*.json.gz'))
    records=[read(p) for p in paths]
    assert [r['index'] for r in records]==cfg['indices']
    statuses=Counter();messages=Counter();pairs=0;with_pairs=0;local=[];rows=[]
    for r,e in zip(records,execution['records']):
        assert r['index']==e['index'] and r['status']==e['status']
        found=[]
        if r['base'].get('qualified'):
            assert len(r['trials'])==4
            p,obs=r['packet'],r['observed'];m=Stability(p,obs['counts'],obs['overlaps'],cfg['rho'],cfg['fit'])
            x=m.pack(np.array(r['base']['coordinates']));mu,J=m.means(x);w,W=m.weights(x)
            A=np.linalg.solve(m.L,J);U,s,V=np.linalg.svd(A,full_matrices=False)
            gain=np.linalg.svd(W@((V.T/s)@U.T),compute_uv=False)[0]/np.linalg.norm(w)
            assert np.allclose(s,r['local']['singular_values'],atol=1e-7,rtol=1e-7)
            assert abs(gain-r['local']['relative_leading_gain'])<1e-7
            assert r['local']['rank']==r['local']['columns']
            local.append(gain)
            for trial in r['trials']:
                statuses[trial['status']]+=1;messages[str(trial['optimizer_message'])]+=1
                if 'best' not in trial:continue
                best=trial['best'];weights=[];means=[];residuals=[]
                for z in best['coordinates']:
                    xx=m.pack(np.array(z));gate=m.gate(xx);mm,_=m.means(xx);ww=m.weights(xx,False)
                    assert np.allclose(ww,gate['weights'],atol=1e-5,rtol=1e-5)
                    weights.append(ww);means.append(mm)
                    residuals.append(float((mm-m.counts)@m.precision@(mm-m.counts)))
                delta=means[1]-means[0];q=float(delta@m.precision@delta)
                rel=np.linalg.norm(weights[1]-weights[0])/(sum(map(np.linalg.norm,weights))/2)
                assert q<4 and max(residuals)<len(mu)
                assert abs(q-best['squared_pair_discrepancy'])<1e-6
                assert abs(rel-best['relative_weight_separation'])<1e-6
                assert rel<cfg['minimum_relative_weight_separation']
                pairs+=1;found.append(float(rel))
        if found:with_pairs+=1
        rows.append(dict(index=r['index'],status=r['status'],base_status=r['base']['status'],
                         maximum_relative_separation=max(found,default=None),
                         local_relative_gain=r.get('local',{}).get('relative_leading_gain')))
    # Re-run the six frozen, independent synthetic controls without overwriting.
    controls=[];original_save=st_controls.save
    try:
        st_controls.save=lambda path,obj: controls.append(obj)
        st_controls.main()
    finally:st_controls.save=original_save
    assert len(controls)==1 and all(v['passed'] for v in controls[0]['checks'])
    witness=build_witness();assert witness==read(HERE/'witness.json');certificate=certify(witness)
    assert certificate['relative_weight_separation']==read(HERE/'certificate.json')['relative_weight_separation']
    return dict(status='PASS',sources=len(records),qualified_bases=len(local),
                count_hold_indices=[r['index'] for r in records if r['base']['status']=='COUNT_HOLD'],
                trials=sum(len(r['trials']) for r in records),
                optimizer_successes=sum(t['optimizer_success'] for r in records for t in r['trials']),
                trial_statuses=dict(statuses),optimizer_messages=dict(messages),
                verified_numerical_pairs=pairs,clouds_with_numerical_pairs=with_pairs,strong_pairs=0,
                relative_local_gain=dict(minimum=float(min(local)),median=float(np.median(local)),maximum=float(max(local))),
                synthetic_controls=len(controls[0]['checks']),exact_witness_status=certificate['status'],
                results=rows,decision='No strong witness; certified smaller bounded-error ambiguity; no global stability or Poisson impossibility conclusion. All scientific HOLDs remain.')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    if (HERE/'SHA256SUMS').exists():
        for line in (HERE/'SHA256SUMS').read_text().splitlines():
            h,name=line.split('  ',1);assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    result=audit()
    if args.write:save(HERE/'audit.json',result)
    else:
        old=read(HERE/'audit.json')
        for k in ['sources','qualified_bases','trials','optimizer_successes','trial_statuses','verified_numerical_pairs','strong_pairs','exact_witness_status']:
            assert result[k]==old[k],k
    print({k:v for k,v in result.items() if k!='results'})


if __name__=='__main__':main()
