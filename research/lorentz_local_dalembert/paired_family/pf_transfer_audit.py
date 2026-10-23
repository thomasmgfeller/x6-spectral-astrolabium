"""Provenance, exact displacement pullbacks and fixed-endpoint mean invariance.
SPDX-License-Identifier: Apache-2.0
"""
from pf_transfer import *

def audit_transfer():
    cert,summary=run_transfer()
    assert cert==read(HERE/'transfer_cells.json.gz') and summary==read(HERE/'combined_summary.json')
    original=read(HERE/'cells.json.gz');source=read(HERE.parent/'continuous_energy/cells.json.gz')
    source_rows={(r['ray'],r['path']):r for r in source['cells']}
    base=base_setup();rays=read(HERE.parent/'coordinated_motions/directions.json')
    marginal_count=0;joint_count=0;polynomial_count=0;partitions=0;used=set()
    for line,trans in zip(original['lines'],cert['lines']):
        assert line['ray']==trans['ray'];b=setup(base,rays[line['ray']])
        parents={p for level in line['splits'] for p in level}
        leaves=[r for r in line['cells'] if r['path'] not in parents]
        holds={r['path']:r for r in leaves if r['status']=='HOLD'}
        groups={k:[] for k in holds}
        for r in trans['cells']:groups[r['parent']].append(r)
        for parent,rows in groups.items():
            cover(rows,F(holds[parent]['lo']),F(holds[parent]['hi']));partitions+=1
        final=[r for r in leaves if r['status']!='HOLD']+trans['cells'];cover(final,F(-1,10),F(1,10))
        for row in trans['cells']:
            if row['status']=='HOLD':continue
            assert row['status']=='TRANSFERRED_LAW_EXCLUDED';r=row['source'];node=r['node'];sign=r['sign']
            velocity=b['velocities'][node];assert velocity!=0
            lo,hi=map(F,(row['lo'],row['hi']))
            mapped=sorted(velocity*h/sign for h in (lo,hi))
            assert list(map(str,mapped))==row['source_step_range']
            assert F(r['lo'])<=mapped[0]<=mapped[1]<=F(r['hi'])
            if r['source']=='continuous_energy':
                s=source_rows[(r['source_ray'],r['source_path'])];assert s['status']=='LAW_EXCLUDED'
                assert source['rays'][s['ray']]==[node,r['axis'],sign]
                assert [r['lo'],r['hi'],r['tv_lower']]==[s['lo'],s['hi'],s['law']['tv_lower']]
                pairs=[list(base['ends'][s['law']['interval_index']])]
                old_alt=[tuple(map(F,s['law']['mean_intervals'][1]))]
                marginal_count+=1;used.add((s['ray'],s['path']))
            else:
                assert r['source']=='joint_ray_obstruction'
                s=read(HERE.parent/'joint_ray_obstruction/certificate.json')
                assert [node,r['axis'],sign]==[15,1,-1]
                assert [r['lo'],r['hi']]==s['domain']['h'] and r['tv_lower']==s['full_law_tv_lower']
                pairs=[[2,15],[15,1]];old_alt=[tuple(map(F,v)) for v in s['moved_mean_intervals']]
                assert b['boost'][2][0]<b['boost'][15][0]<b['boost'][1][0]
                joint_count+=1
            assert pairs==r['intervals'] and F(r['tv_lower'])>F(1,4)
            single=dict(base,ray=dict(axis=r['axis']),velocities=[F(sign) if k==node else F(0) for k in range(21)])
            for pair,enclosure in zip(pairs,old_alt):
                assert node in pair and len(set(pair)&set(range(5)))==1
                # Full-polynomial identity, not just endpoint samples.
                new=qpoly(b,*pair);old=qpoly(single,*pair);factor=velocity/sign
                assert new==[old[k]*factor**k for k in range(3)];polynomial_count+=1
                new_mean=mean_bounds(b,qrange(b,*pair,lo,hi))
                assert enclosure[0]<=new_mean[0]<=new_mean[1]<=enclosure[1]
    assert marginal_count+joint_count==summary['transferred_subcells']
    # An operator certificate is never admitted as a transferable law certificate.
    admitted={(r['source_ray'],r['source_path']) for r in source_regions() if r['source']=='continuous_energy'}
    assert all(source_rows[key]['status']=='LAW_EXCLUDED' for key in admitted)
    assert not any(key in admitted for key,r in source_rows.items() if r['status']=='GAP_EXCLUDED')
    return dict(status='PASS',original_hold_cells_partitioned=partitions,transferred_marginal_subcells=marginal_count,
        transferred_joint_subcells=joint_count,unique_inherited_marginal_certificates=len(used),
        exact_full_polynomial_identities=polynomial_count,whole_cell_mean_inclusions=polynomial_count,
        complete_refined_cover_checked=True,no_operator_gap_transferred=True,
        source_probability_validation='Pinned historical source certificates and audits; probability arithmetic is inherited, not relabelled as a fresh independent probability replay.')

if __name__=='__main__':
    result=audit_transfer()
    if '--verify' in sys.argv:assert result==read(HERE/'transfer_audit.json')
    else:save(HERE/'transfer_audit.json',result)
    print(json.dumps(result),flush=True)
