"""Independent subset geometry, Cantelli arithmetic and complete-cover checks.
SPDX-License-Identifier: Apache-2.0
"""
from pc_overlap import *
from pc_audit import direct_q,cover
from collections import Counter

def audit_overlap():
    cert,summary=run_overlap()
    assert cert==read(HERE/'overlap_certificates.json')
    assert summary==read(HERE/'combined_summary.json')
    c=read(HERE/'contract.json');oc=read(HERE/'overlap_contract.json');b=setup(c)
    old=read(HERE/'summary.json');archive=read(HERE/'cells.json.gz');leaves=terminal_cells(archive)
    assert old['states']['HOLD']==oc['source_hold_cells']==len(cert['rows'])
    assert old['unresolved_intervals']==[oc['source_hold_interval']]
    lookup={r['path']:r for r in cert['rows']}
    assert set(lookup)=={r['path'] for r in leaves if r['status']=='HOLD'}
    combined=[lookup.get(r['path'],r) for r in leaves]
    cover(combined,*map(F,c['interval']))
    assert Counter(r['status'] for r in combined)==summary['states']
    cases=[(F(0),F(0),cert['base'])]+[(F(r['lo']),F(r['hi']),r['variance']) for r in cert['rows'] if 'variance' in r]
    geometry_checks=0;variance_checks=0
    dt=b['boost'][15][0]-b['boost'][5][0];Ttip=b['boost'][1][0]-b['boost'][15][0]
    for lo,hi,v in cases:
        delay=F(v['common_future_tip_delay_upper']);qsub=F(v['common_interval_q_lower'])
        qlo=F(v['pair_q_range'][0])
        # Entire-cell inequality: delayed node 15 lies in the future of node 5.
        assert delay>=0 and (dt+delay)**2>=dt*dt-qlo
        mu=[[F(x) for x in pair] for pair in v['count_mean_intervals']]
        overlap=F(v['common_interval_mean_lower'])
        assert F(v['variance_upper'])==mu[0][1]+mu[1][1]-2*overlap
        for h in (lo,(lo+hi)/2,hi):
            zz=boosted(cm.moved(b['z'],b['ray'],h))
            virtual=[zz[15][0]+delay,zz[15][1],zz[15][2]]
            assert virtual[0]>=zz[5][0] and direct_q(zz[5],virtual)>=0
            assert virtual[0]>=zz[15][0] and direct_q(zz[15],virtual)>=0
            if overlap>0:
                assert delay<Ttip and qsub>0
                q=direct_q(virtual,zz[1]);assert virtual[0]<zz[1][0] and q>=qsub
                pl,pu=b['pi'];factor=F(b['w']['rho'],12)*F(b['w']['scale'])**3
                assert overlap<=factor*pl*q*sqrt_bounds(q)[0]
            geometry_checks+=1
        assert overlap>=0 and F(v['variance_upper'])>=0;variance_checks+=1
    # Independent formula for each event using fractions directly.
    base=cert['base'];mb=tuple(map(F,base['mean']));vb=F(base['variance_upper'])
    for row in cert['rows']:
        if 'event' not in row:continue
        alt=row['variance'];ma=tuple(map(F,alt['mean']));va=F(alt['variance_upper']);e=row['event'];k=e['threshold']
        assert k==((sum(mb)+sum(ma))/4).__floor__()
        if ma[1]<mb[0]:small,big,vs,vh=ma,mb,va,vb
        else:small,big,vs,vh=mb,ma,vb,va
        a=F(k+1)-small[1];d=big[0]-k;assert a>0 and d>0
        direct=max(F(0),1-vs/(vs+a*a)-vh/(vh+d*d))
        assert F(e['tv_lower'])<=direct
        assert (row['status']=='DIFFERENCE_LAW_EXCLUDED')==(F(e['tv_lower'])>F(1,4))
    # Synthetic independent exclusive regions, with nonzero shared intensity.
    # These provide exact product-Poisson event bounds to check Cantelli against.
    synthetic=[(F(40),F(10),F(60)),(F(70),F(10),F(40))]
    stats=[]
    for plus,minus,common in synthetic:
        muA=plus+common;muB=minus+common
        stats.append(dict(mean=[str(plus-minus)]*2,variance_upper=str(muA+muB-2*common)))
    bound=difference_event(*stats);k=bound['threshold'];jc=c['joint_probability']
    p,_=jr.event(synthetic[0][1],synthetic[0][0],1,k,jc)
    q,_=jr.event(synthetic[1][1],synthetic[1][0],1,k,jc)
    assert F(bound['tv_lower'])<=p[0]-q[1]<1
    assert difference_event(stats[0],stats[0])['tv_lower']=='0'
    assert difference_event(*stats)['tv_lower']==difference_event(*reversed(stats))['tv_lower']
    # Dropping shared covariance is conservative but less informative.
    inflated=[dict(v,variance_upper=str(F(v['variance_upper'])+2*common)) for v,(_,_,common) in zip(stats,synthetic)]
    assert F(difference_event(*inflated)['tv_lower'])<=F(bound['tv_lower'])
    # An invalid zero-variance shortcut would produce an impossible TV lower 1.
    unsafe=[dict(v,variance_upper='0') for v in stats]
    assert F(difference_event(*unsafe)['tv_lower'])>p[1]-q[0]
    return dict(status='PASS',whole_cell_future_tip_checks=len(cases),rational_virtual_tip_checks=geometry_checks,
        variance_identities=variance_checks,cantelli_event_checks=len(cert['rows']),terminal_cover_cells=len(combined),
        synthetic_product_poisson_comparison=True,
        controls=['equal means give no exclusion','law swap symmetry','omitting covariance weakens bound','underestimated variance fails exact Poisson control'],
        scope='Exact subset geometry and one-sided moment inequalities; no Monte Carlo overlap estimate.')

if __name__=='__main__':
    result=audit_overlap()
    if '--verify' in sys.argv:assert result==read(HERE/'overlap_audit.json')
    else:save(HERE/'overlap_audit.json',result)
    print(json.dumps(result))
