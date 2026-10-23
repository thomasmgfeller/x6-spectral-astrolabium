"""Independent PMF expressions, overlap boxes, geometry and complete covers.
SPDX-License-Identifier: Apache-2.0
"""
from ot_common import *
from collections import Counter
from decimal import Decimal,localcontext
from pf_audit import check_virtual
from jr_audit import small_exact_reference

def decimal_difference(x,y,k):
    # Direct exp and factorial recurrence, independently of the mode-normalized
    # integer recurrence. At x<=2048, P[X>8192] < exp(-5000) by Chernoff.
    assert 0<=x<=2048 and 0<=y<=2048
    with localcontext() as ctx:
        ctx.prec=110
        x=Decimal(x.numerator)/Decimal(x.denominator)
        y=Decimal(y.numerator)/Decimal(y.denominator)
        cutoff=8192;last=max(0,k+cutoff);term=(-y).exp();prefix=[term]
        for n in range(1,last+1):term=term*y/n;prefix.append(prefix[-1]+term)
        term=(-x).exp();total=Decimal(0)
        for n in range(cutoff+1):
            if k+n>=0:total+=term*prefix[k+n]
            term=term*x/(n+1)
        return +total

def slice_cover(rows,lo,hi):
    assert rows and F(rows[0]['overlap'][0])==lo and F(rows[-1]['overlap'][1])==hi
    for r in rows:assert lo<=F(r['overlap'][0])<=F(r['overlap'][1])<=hi
    assert all(a['overlap'][1]==b['overlap'][0] for a,b in zip(rows,rows[1:]))

def audit():
    frozen();c=read(HERE/'contract.json');old,source=inputs();rows=read(HERE/'certificates.json.gz')
    summary=read(HERE/'summary.json');counts=Counter();seen=set();geometries=set();laws=set()
    assert len(rows)==len(source)==c['source_hold_cells']
    assert old['unresolved_signed_rays']==c['source_unresolved_signed_rays']
    base=base_setup();rays=read(HERE.parent/'coordinated_motions/directions.json');bases={}
    def geometry(b,lo,hi,v):
        key=(b['ray']['index'],str(lo),str(hi),v['anchor'])
        if key in geometries:return
        check_virtual(b,lo,hi,v);counts['virtual_subset_checks']+=1;geometries.add(key)
        for h in (lo,(lo+hi)/2,hi):
            zz=cm.moved(b['z'],b['ray'],h)
            for node in b['ray']['nodes']:
                p,q=zz[node],zz[v['anchor']];dt,dx,dy=[a-d for a,d in zip(p,q)]
                lower,upper=qrange(b,node,v['anchor'],lo,hi)
                assert lower<=dt*dt-dx*dx-dy*dy<=upper
                counts['direct_geometry_checks']+=1
    def law(stats,k,cert):
        key=json.dumps([stats,k,cert],sort_keys=True)
        if key in laws:return
        laws.add(key)
        if cert['status']!='ENCLOSED':
            assert cert['status'] in ('HOLD_RATE_BUDGET','HOLD_PROBABILITY_BUDGET')
            assert cert['probability']==['0','1'];counts['budget_hold_laws']+=1;return
        assert cert['threshold']==k
        a,b=[tuple(map(F,v)) for v in stats['count_mean_intervals']]
        lo=F(stats['common_mean_lower']);hi=min(a[1],b[1]);assert 0<=lo<=hi
        assert cert['overlap_range']==list(map(str,(lo,hi)))
        slices=cert['slices'];assert len(slices)==c['overlap_slices'];slice_cover(slices,lo,hi)
        for j,r in enumerate(slices):
            l=lo+(hi-lo)*j/len(slices);u=lo+(hi-lo)*(j+1)/len(slices)
            assert r['overlap']==list(map(str,(l,u)))
            plus=(max(F(0),a[0]-u),a[1]-l);minus=(max(F(0),b[0]-u),b[1]-l)
            assert r['plus']==list(map(str,plus)) and r['minus']==list(map(str,minus))
            assert len(r['records'])==2
            for rec,label,(x,y) in zip(r['records'],('lower','upper'),((minus[0],plus[1]),(minus[1],plus[0]))):
                assert rec['endpoint']==label and F(rec['x_mean'])==x and F(rec['y_mean'])==y
                assert 0<=x<=c['maximum_exclusive_mean'] and 0<=y<=c['maximum_exclusive_mean']
                signature=(str(x),str(y),k)
                if signature not in seen:
                    truth=decimal_difference(x,y,k)
                    assert Decimal(rec['probability'][0])<=truth<=Decimal(rec['probability'][1]),signature
                    counts['independent_110_digit_difference_PMF_checks']+=1;seen.add(signature)
                assert F(rec['numerical_width_upper'])<=F(c['probability']['numerical_event_width_target'])+F(1,10**75)
                for name,mu in (('x',x),('y',y)):
                    meta=rec['normalization'][name];assert int(meta['mode'])==mu.__floor__()
                    assert int(meta['upper'])==int(meta['mode'])+c['probability'][name+'_upper_steps']
                    assert 0<int(meta['zlo'])<=int(meta['zhi']) and int(meta['tail'])>=0
                    assert (int(meta['tail'])==0)==(mu==0)
            p=tuple(map(F,r['probability']));assert 0<=p[0]<=p[1]<=1
            assert p[0]<=F(r['records'][0]['probability'][0]) and p[1]>=F(r['records'][1]['probability'][1])
            counts['exclusive_rate_rectangles']+=1
        assert list(map(F,cert['probability']))==[min(F(r['probability'][0]) for r in slices),max(F(r['probability'][1]) for r in slices)]
        if hi>lo:
            try:slice_cover(slices[1:],lo,hi)
            except AssertionError:counts['missing_overlap_slice_controls']+=1
            else:raise AssertionError('missing overlap slice accepted')
        counts['uniform_difference_laws']+=1
    for r,s in zip(rows,source):
        assert all(r[k]==v for k,v in s.items())
        if r['ray'] not in bases:bases[r['ray']]=setup(base,rays[r['ray']])
        b=bases[r['ray']];lo,hi=F(r['lo']),F(r['hi']);expected=candidates(b,lo,hi)[:c['maximum_anchor_events_per_cell']]
        assert 1<=len(r['attempts'])<=len(expected)
        for i,(a,e) in enumerate(zip(r['attempts'],expected)):
            assert all(a[k]==e[k] for k in ('anchor','side','threshold')) and a['score']==str(e['score'])
            assert a['base_statistics']==e['base'] and a['moved_statistics']==e['moved']
            geometry(b,F(0),F(0),e['base']);geometry(b,lo,hi,e['moved'])
            law(e['base'],e['threshold'],a['base_law']);law(e['moved'],e['threshold'],a['moved_law'])
            p,q=[tuple(map(F,a[v]['probability'])) for v in ('base_law','moved_law')]
            tv=max(F(0),p[0]-q[1],q[0]-p[1]);assert a['tv_lower']==outward(tv)[0]
            if i+1<len(r['attempts']):assert tv<=F(c['tv_gate'])
            counts['event_attempts']+=1
        if r['status']=='OVERLAP_DIFFERENCE_EXCLUDED':
            assert tv>F(c['tv_gate']) and r['tv_lower']==r['attempts'][-1]['tv_lower']
        else:
            assert r['status']=='HOLD' and len(r['attempts'])==len(expected)
            assert all(F(a['tv_lower'])<=F(c['tv_gate']) for a in r['attempts'])
        print(json.dumps(dict(audited_cell=r['index'],unique_PMF_checks=len(seen))),flush=True)
    # Replace only source HOLD cells, then reconstruct all thirty full lines.
    initial=read(HERE.parent/'paired_family/cells.json.gz');transfer=read(HERE.parent/'paired_family/transfer_cells.json.gz')
    prior=read(HERE.parent/'paired_tail/certificates.json.gz')
    lookup={(r['ray'],r['lo'],r['hi'],r['parent']):r for r in rows};assert len(lookup)==38
    oldmap={(r['ray'],r['lo'],r['hi'],r['parent']):r for r in prior};assert len(oldmap)==574
    states=Counter();pending=[];closed=[];used=set()
    for line,trans in zip(initial['lines'],transfer['lines']):
        assert line['ray']==trans['ray'];parents={p for level in line['splits'] for p in level}
        final=[r for r in line['cells'] if r['path'] not in parents and r['status']!='HOLD']
        for r in trans['cells']:
            if r['status']=='HOLD':
                key=(line['ray'],r['lo'],r['hi'],r['parent']);r=oldmap[key]
                if r['status']=='HOLD':r=lookup[key];used.add(key)
            final.append(r)
        final.sort(key=lambda r:F(r['lo']));cover(final,F(-1,10),F(1,10));states.update(r['status'] for r in final)
        for sign,index in ((-1,line['ray']-1),(1,line['ray'])):
            remains=any(r['status']=='HOLD' and ((sign<0 and F(r['lo'])<0) or (sign>0 and F(r['hi'])>0)) for r in final)
            (pending if remains else closed).append(index)
        intervals=[]
        for r in final:
            if r['status']!='HOLD':continue
            if intervals and intervals[-1][1]==r['lo']:intervals[-1][1]=r['hi']
            else:intervals.append([r['lo'],r['hi']])
        reported=[v for v in summary['lines'] if v['ray']==line['ray']]
        assert intervals==(reported[0]['unresolved_intervals'] if reported else [])
        try:cover(final[1:],F(-1,10),F(1,10))
        except AssertionError:counts['missing_cell_controls']+=1
        else:raise AssertionError('missing cell accepted')
    assert used==set(lookup) and states==summary['combined_states']
    assert pending==summary['unresolved_signed_rays'] and len(closed)+2==summary['total_excluded_signed_rays']
    assert sorted(set(closed)&set(old['unresolved_signed_rays']))==summary['newly_excluded_signed_rays']
    assert Counter(r['status'] for r in rows)==summary['new_states']
    pc=read(HERE.parent/'paired_continuous/cells.json.gz');po=read(HERE.parent/'paired_continuous/overlap_certificates.json')
    parents={p for level in pc['splits'] for p in level};pmap={r['path']:r for r in po['rows']}
    leaves=[pmap.get(r['path'],r) for r in pc['cells'] if r['path'] not in parents]
    cover(leaves,F(-1,10),F(1,10));assert all(r['status']!='HOLD' for r in leaves)
    counts['complete_line_covers']=30;counts['complete_signed_ray_covers']=60
    counts['combined_terminal_cells']=sum(states.values())+len(leaves)
    # Small means: independent exact factorial/exponential-series reference.
    for x,y,k in ((F(1,4),F(1,2),0),(F(1,2),F(1,4),1),(F(1,4),F(1,4),0)):
        expected=small_exact_reference(x,y,1,k);got,_=jr.event(x,y,1,k,c['probability'])
        assert got[0]<=expected[0]<=expected[1]<=got[1];counts['exact_small_mean_controls']+=1
    assert jr.event(F(0),F(0),1,0,c['probability'])[0]==(F(1),F(1))
    assert jr.event(F(0),F(0),1,-1,c['probability'])[0]==(F(0),F(0))
    counts['zero_rate_exact_controls']=2
    # Unknown common intensity must include BOTH endpoints, not a midpoint law.
    toy=dict(count_mean_intervals=[['1','1'],['1','1']],common_mean_lower='0')
    enclosure=enclose_difference(toy,0,c);assert enclosure['status']=='ENCLOSED'
    independent,_=jr.event(F(1),F(1),1,0,c['probability'])
    midpoint,_=jr.event(F(1,2),F(1,2),1,0,c['probability'])
    assert F(enclosure['probability'][0])<=independent[0]<midpoint[0]<1==F(enclosure['probability'][1])
    # Identical A=B gives D=0 with probability one; independent copies do not.
    assert independent[1]<1 and midpoint[1]<1
    fail=enclose_difference(toy,0,dict(c,maximum_exclusive_mean=0))
    assert fail==dict(status='HOLD_RATE_BUDGET',probability=['0','1'])
    return dict(status='PASS',**dict(counts),source_cells_checked=38,dependence_counterexample=True,
        midpoint_overlap_negative_control=True,unknown_overlap_endpoints_retained=True,budget_failure_is_hold=True,
        scope='Directed integer probability enclosures and exact whole-cell geometry constitute the certificates; independent decimal PMFs are diagnostic audit checks.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
