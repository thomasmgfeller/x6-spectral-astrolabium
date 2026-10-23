"""Independent direct-PMF checks, exact geometry and full paired-family coverage.
SPDX-License-Identifier: Apache-2.0
"""
from pft_common import *
from collections import Counter
from decimal import Decimal,localcontext
from pto_audit import decimal_cdf
from jr_audit import small_exact_reference

def decimal_joint(x,y,a,k):
    # Independent direct exp/PMF expression; no normalized mode recurrence.
    assert 0<=x<=256
    with localcontext() as ctx:
        ctx.prec=110
        x=Decimal(x.numerator)/Decimal(x.denominator);y=Decimal(y.numerator)/Decimal(y.denominator)
        cutoff=1536;last=max(0,k+a*cutoff);term=(-y).exp();prefix=[term]
        for n in range(1,last+1):term=term*y/n;prefix.append(prefix[-1]+term)
        term=(-x).exp();total=Decimal(0)
        for n in range(cutoff+1):
            if k+a*n>=0:total+=term*prefix[k+a*n]
            term=term*x/(n+1)
        return +total

def direct_q(p,q):
    dt,dx,dy=[a-b for a,b in zip(p,q)]
    return dt*dt-dx*dx-dy*dy

def audit():
    frozen();c=read(HERE/'contract.json');old,source=inputs();rows=read(HERE/'certificates.json.gz')
    summary=read(HERE/'summary.json');strip=read(HERE/'strip_certificate.json')
    assert len(rows)==len(source)==c['source_hold_cells'];assert old['unresolved_signed_rays']==c['source_unresolved_signed_rays']
    base=base_setup();base['basemeans']=means(base['w'],base['z'],base['ends'],base['pi'])
    base['joint_base_cache']={};rays=read(HERE.parent/'coordinated_motions/directions.json');counts=Counter();seen=set()
    def audit_geometry(b,pairs,lo,hi):
        for h in (lo,(lo+hi)/2,hi):
            zz=cm.moved(b['z'],b['ray'],h)
            for pair in pairs:
                lower,upper=qrange(b,*pair,lo,hi)
                assert lower<=direct_q(zz[pair[0]],zz[pair[1]])<=upper
                counts['direct_geometry_checks']+=1
    def audit_joint(b,lo,hi,cert):
        if 'reason' in cert:assert F(cert['tv_lower'])==0;return
        node=cert['node'];pairs=[cert['X'],cert['Y']];a=cert['coefficient'];k=cert['threshold']
        require_disjoint(b,node,*pairs)
        assert cert['base_mean_intervals']==[[str(v) for v in b['basemeans'][b['ends'].index(tuple(p))]] for p in pairs]
        assert cert['moved_mean_intervals']==[[str(v) for v in mean_bounds(b,qrange(b,*p,lo,hi))] for p in pairs]
        assert cert['q_ranges']==[[str(v) for v in qrange(b,*p,lo,hi)] for p in pairs]
        audit_geometry(b,pairs,lo,hi)
        for kind,mean_key in (('base','base_mean_intervals'),('moved','moved_mean_intervals')):
            x,y=[tuple(map(F,v)) for v in cert[mean_key]]
            assert len(cert['records'][kind])==2
            for record,(mx,my) in zip(cert['records'][kind],((x[0],y[1]),(x[1],y[0]))):
                assert F(record['x_mean'])==mx and F(record['y_mean'])==my
                key=(str(mx),str(my),a,k)
                if key not in seen:
                    value=decimal_joint(mx,my,a,k)
                    assert Decimal(record['probability'][0])<=value<=Decimal(record['probability'][1])
                    counts['independent_110_digit_joint_PMF_checks']+=1;seen.add(key)
                assert F(record['numerical_width_upper'])<=F(c['joint_probability']['numerical_event_width_target'])
                assert all(int(record['normalization'][v]['tail'])>0 for v in ('x','y'))
        p,q=[tuple(map(F,cert[v])) for v in ('base_probability','moved_probability')]
        assert F(cert['tv_lower'])<=max(F(0),p[0]-q[1],q[0]-p[1])+F(2,10**60)
        counts['joint_event_certificates']+=1
    stripbase=setup(base,dict(nodes=[15],axis=1,velocities=['-1']))
    assert strip['domain']==c['strip'];audit_joint(stripbase,*map(F,c['strip']['step_interval']),strip)
    for r,s in zip(rows,source):
        assert all(r[k]==v for k,v in s.items());b=setup(base,rays[r['ray']]);lo,hi=F(r['lo']),F(r['hi'])
        if r['status']=='STRIP_JOINT_EXCLUDED':
            assert b['ray']['axis']==1
            steps=sorted(-b['velocities'][15]*h for h in (lo,hi));a,d=map(F,c['strip']['step_interval'])
            assert a<=steps[0]<=steps[1]<=d and list(map(str,steps))==r['strip_steps']
            assert r['tv_lower']==strip['tv_lower'] and F(r['tv_lower'])>F(1,4)
            # Exact polynomial equality to the inherited fixed-event displacement.
            factor=-b['velocities'][15]
            for pair in ([2,15],[15,1]):
                assert qpoly(b,*pair)==[v*factor**k for k,v in enumerate(qpoly(stripbase,*pair))]
                counts['strip_polynomial_identities']+=1
            continue
        assert len(r['marginal'])<=c['maximum_marginal_tests_per_cell'] and len(r['joint'])<=c['maximum_joint_tests_per_cell']
        expected=[v for v in marginal_candidates(b,lo,hi)[:c['maximum_marginal_tests_per_cell']] if max(v['base']+v['moved'])<=c['poisson']['maximum_mean']]
        for m,e in zip(r['marginal'],expected):
            assert m['index']==e['index'] and m['score']==str(e['score']) and m['pair']==e['pair']
            assert m['base_mean']==list(map(str,e['base'])) and m['moved_mean']==list(map(str,e['moved']))
            audit_geometry(b,[m['pair']],lo,hi);cert=m['certificate']
            sorted_means=sorted((e['base'],e['moved']),key=lambda v:v[0])
            wanted=[sorted_means[0][0],sorted_means[0][1],sorted_means[1][0],sorted_means[1][1]]
            assert len(cert['endpoint_cdf_records'])==4
            for record,mu in zip(cert['endpoint_cdf_records'],wanted):
                assert F(record['mean'])==mu
                value=decimal_cdf(mu,cert['threshold'])
                assert Decimal(record['cdf'][0])<=value<=Decimal(record['cdf'][1])
                assert record['omitted_weight_upper_grid_units']>0
                counts['independent_100_digit_marginal_PMF_checks']+=1
            p,q,t,u=[tuple(map(F,v['cdf'])) for v in cert['endpoint_cdf_records']]
            assert F(cert['full_law_tv_lower'])<=max(F(0),q[0]-t[1])+F(2,10**60)
            counts['marginal_event_certificates']+=1
        expected=joint_candidates(b,lo,hi,c)[:c['maximum_joint_tests_per_cell']]
        for j,e in zip(r['joint'],expected):
            assert j['candidate']=={k:str(v) if k=='score' else v for k,v in e.items()}
            cert=j['certificate']
            if 'reason' not in cert:assert all(cert[k]==e[k] for k in ('node','X','Y','coefficient','threshold'))
            audit_joint(b,lo,hi,cert)
        if r['status']=='MARGINAL_TAIL_EXCLUDED':
            assert not r['joint'] and r['tv_lower']==r['marginal'][-1]['certificate']['full_law_tv_lower']
        elif r['status']=='DISJOINT_JOINT_EXCLUDED':assert r['tv_lower']==r['joint'][-1]['certificate']['tv_lower']
        else:assert r['status']=='HOLD'
        if r['status']!='HOLD':assert F(r['tv_lower'])>F(1,4)
        if r['index']%100==0:print(json.dumps(dict(audited_index=r['index'],checks=dict(counts))),flush=True)
    # Rebuild the complete old cover, replacing only its 574 HOLD cells.
    initial=read(HERE.parent/'paired_family/cells.json.gz');transfer=read(HERE.parent/'paired_family/transfer_cells.json.gz')
    lookup={(r['ray'],r['lo'],r['hi'],r['parent']):r for r in rows};assert len(lookup)==574
    final_states=Counter();pending=[];complete=[]
    for line,trans in zip(initial['lines'],transfer['lines']):
        assert line['ray']==trans['ray'];parents={p for level in line['splits'] for p in level}
        final=[r for r in line['cells'] if r['path'] not in parents and r['status']!='HOLD']
        for r in trans['cells']:
            if r['status']=='HOLD':r=lookup[(line['ray'],r['lo'],r['hi'],r['parent'])]
            final.append(r)
        final.sort(key=lambda r:F(r['lo']));cover(final,F(-1,10),F(1,10));final_states.update(r['status'] for r in final)
        for sign,index in ((-1,line['ray']-1),(1,line['ray'])):
            remains=any(r['status']=='HOLD' and ((sign<0 and F(r['lo'])<0) or (sign>0 and F(r['hi'])>0)) for r in final)
            (pending if remains else complete).append(index)
        try:cover(final[1:],F(-1,10),F(1,10))
        except AssertionError:counts['missing_cell_controls']+=1
        else:raise AssertionError('missing cell accepted')
        intervals=[]
        for r in final:
            if r['status']!='HOLD':continue
            if intervals and intervals[-1][1]==r['lo']:intervals[-1][1]=r['hi']
            else:intervals.append([r['lo'],r['hi']])
        assert intervals==next(v for v in summary['lines'] if v['ray']==line['ray'])['unresolved_intervals']
    assert pending==summary['unresolved_signed_rays'] and len(complete)+2==summary['total_excluded_signed_rays']
    assert sorted(set(complete)&set(old['unresolved_signed_rays']))==summary['newly_excluded_signed_rays']
    assert final_states==summary['combined_states'] and Counter(r['status'] for r in rows)==summary['new_states']
    # Include the separately inherited node-15/node-5 x line for all 60 rays.
    pc=read(HERE.parent/'paired_continuous/cells.json.gz');po=read(HERE.parent/'paired_continuous/overlap_certificates.json')
    parents={p for level in pc['splits'] for p in level};pmap={r['path']:r for r in po['rows']}
    leaves=[pmap.get(r['path'],r) for r in pc['cells'] if r['path'] not in parents]
    cover(leaves,F(-1,10),F(1,10));assert all(r['status']!='HOLD' for r in leaves)
    counts['complete_line_covers']=len(initial['lines'])+1;counts['complete_signed_ray_covers']=60
    counts['combined_terminal_cells']=sum(final_states.values())+len(leaves)
    # Independent exact small-mean factorial-series controls.
    jc=c['joint_probability'];small=0
    for a,k in ((1,0),(2,1),(3,1)):
        expected=small_exact_reference(F(1,4),F(1,4),a,k);got,_=jr.event(F(1,4),F(1,4),a,k,jc)
        assert got[0]<=expected[0]<=expected[1]<=got[1];small+=1
    # Reject an overlapping pair; identical variables are not independent copies.
    try:require_disjoint(stripbase,15,[2,15],[3,15])
    except AssertionError:pass
    else:raise AssertionError('overlap admitted')
    independent,_=jr.event(F(1),F(1),1,0,jc);assert independent[1]<1
    rough,_=jr.event(F(10),F(15),1,0,dict(jc,x_upper_steps=1));fine,_=jr.event(F(10),F(15),1,0,jc)
    x=jr.weights(F(10),80,1,32768);y=jr.weights(F(15),80,2048,32768)
    naive=F(sum(x['hi'][j]*sum(y['hi'][:j+1]) for j in range(x['upper']+1)),x['zlo']*y['zlo'])
    assert x['tail']>0 and naive<fine[0] and rough[0]<=fine[0]<=fine[1]<=rough[1]
    return dict(status='PASS',**dict(counts),exact_small_mean_factorial_controls=small,overlap_pair_rejected=True,
        dependence_counterexample=True,omitted_tail_negative_control=True,source_cells_checked=574,
        scope='Whole-cell claims use exact geometric extrema and directed integer probabilities; independent numerical PMFs are audit checks, not the proof.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
