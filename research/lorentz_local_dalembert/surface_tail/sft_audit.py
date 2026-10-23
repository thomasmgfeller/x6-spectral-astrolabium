"""Direct PMF checks, exact source coverage and cached-certificate integrity.
SPDX-License-Identifier: Apache-2.0
"""
from sft_common import *
from decimal import Decimal,localcontext
from ps_audit import tree as source_tree,independent_q
from pto_audit import decimal_cdf
from ot_audit import slice_cover
from jr_audit import small_exact_reference
from ps_common import jr

def decimal_difference(x,y,k):
    # Independent direct exponential/factorial PMFs, not mode normalization.
    # For x<=2048, Markov on 2**X gives P[X>4096] <= exp(2048)/2**4097 < 1e-330.
    assert 0<=x<=2048 and 0<=y<=2048
    with localcontext() as ctx:
        ctx.prec=110;x=Decimal(x.numerator)/Decimal(x.denominator);y=Decimal(y.numerator)/Decimal(y.denominator)
        cutoff=4096;last=max(0,k+cutoff);term=(-y).exp();prefix=[term]
        for n in range(1,last+1):term=term*y/n;prefix.append(prefix[-1]+term)
        term=(-x).exp();answer=Decimal(0)
        for n in range(cutoff+1):
            if k+n>=0:answer+=term*prefix[k+n]
            term=term*x/(n+1)
        return +answer

def audit():
    frozen();c=read(HERE/'contract.json');old,previous,old_final,pending=inputs();archive=read(HERE/'certificates.json.gz');summary=read(HERE/'summary.json');b=setup(c);counts=Counter()
    source=source_tree(old,read(HERE.parent/'paired_surface/contract.json'));assert {r['path'] for r in source}=={r['path'] for r in old_final}
    rows=archive['marginal'];events=archive['marginal_events'];overlaps=archive['overlap'];bases=archive['overlap_base_laws']
    assert len(rows)==len(pending)==c['source_untested_cells']==744
    assert [r['path'] for r in rows]==[r['path'] for r in pending]
    assert all(r['box']==s['box'] for r,s in zip(rows,pending))
    assert len({r['path'] for r in rows})==len(rows)
    try:assert [r['path'] for r in rows[1:]]==[r['path'] for r in pending]
    except AssertionError:counts['missing_input_rectangle_controls']+=1
    else:raise AssertionError('missing rectangle accepted')
    keys=[(e['index'],tuple(e['base']),tuple(e['moved'])) for e in events];assert len(keys)==len(set(keys))
    used=set();seen_marginal=set()
    def cached_event(a,e):
        assert a['score']==str(e['score']);v=events[a['event_id']]
        assert v['index']==e['index'] and v['base']==list(map(str,e['base'])) and v['moved']==list(map(str,e['moved']))
        return v
    for r in rows:
        box=list(map(F,r['box']));expected=marginal_candidates(b,box)[:c['maximum_marginal_events_per_cell']]
        assert 1<=len(r['attempts'])<=len(expected)
        for pos,(a,e) in enumerate(zip(r['attempts'],expected)):
            pair=b['ends'][e['index']];assert e['moved']==mean_bounds(b,independent_q(b,*pair,box))
            assert e['base']==mean_bounds(b,(interval(b['z'],*pair),)*2);counts['independent_event_mean_rectangles']+=1
            if 'reason' in a:
                assert a['index']==e['index'] and a['score']==str(e['score'])
                assert a['reason'] in ('HOLD_RATE_BUDGET','HOLD_OVERLAPPING_MEAN_BOUNDS','HOLD_EVENT_BUDGET');continue
            v=cached_event(a,e);used.add(a['event_id']);cert=v['certificate']
            if a['event_id'] not in seen_marginal:
                low,high=sorted((e['base'],e['moved']),key=lambda x:x[0]);assert low[1]<high[0]
                wanted=[*low,*high];assert len(cert['endpoint_cdf_records'])==4
                for rec,mu in zip(cert['endpoint_cdf_records'],wanted):
                    assert F(rec['mean'])==mu;truth=decimal_cdf(mu,cert['threshold'])
                    assert Decimal(rec['cdf'][0])<=truth<=Decimal(rec['cdf'][1]);counts['independent_100_digit_marginal_PMF_checks']+=1
                    assert rec['omitted_weight_upper_grid_units']>0
                p,q,t,u=[tuple(map(F,x['cdf'])) for x in cert['endpoint_cdf_records']]
                assert F(cert['full_law_tv_lower'])<=max(F(0),q[0]-t[1])+F(2,10**60)
                seen_marginal.add(a['event_id'])
            if pos+1<len(r['attempts']):assert F(cert['full_law_tv_lower'])<=F(c['tv_gate'])
        if r['status']=='MARGINAL_TAIL_EXCLUDED':
            assert F(events[r['attempts'][-1]['event_id']]['certificate']['full_law_tv_lower'])>F(c['tv_gate'])
        else:
            assert r['status']=='HOLD' and len(r['attempts'])==len(expected)
            assert all('reason' in a or F(events[a['event_id']]['certificate']['full_law_tv_lower'])<=F(c['tv_gate']) for a in r['attempts'])
        assert any('event_id' in a for a in r['attempts']) # Actual evaluation, not only failed preconditions.
    assert used==set(range(len(events)))
    first=rows[0];choice=marginal_candidates(b,list(map(F,first['box'])))[0];wrong=dict(first['attempts'][0],event_id=(first['attempts'][0]['event_id']+1)%len(events))
    try:cached_event(wrong,choice)
    except AssertionError:counts['wrong_cached_certificate_controls']+=1
    else:raise AssertionError('wrong cached event accepted')
    wanted=sorted((r for r in rows if r['status']=='HOLD'),key=lambda r:overlap_priority(b,r))[:c['maximum_overlap_cells']]
    assert [r['path'] for r in overlaps]==[r['path'] for r in wanted]
    seen_geometry=set();seen_laws=set();seen_pmf=set();used_bases=set()
    def geometry(box,v):
        key=(tuple(box),v['anchor'])
        if key in seen_geometry:return
        seen_geometry.add(key);i,j=b['nodes'];k=v['anchor'];sgn=v['time_sign'];tip=v['tip'];delay=F(v['delay_upper']);duration=F(v['duration']);qsub=F(v['common_q_lower']);dt=abs(b['boost'][i][0]-b['boost'][j][0])
        qr=independent_q(b,i,j,box);assert v['pair_q_range']==list(map(str,qr))
        assert delay>=0 and (dt+delay)**2>=dt*dt-qr[0]
        assert qsub==independent_q(b,tip,k,box)[0]-2*duration*delay+delay*delay
        mu=[tuple(map(F,m)) for m in v['count_mean_intervals']];common=F(v['common_mean_lower'])
        assert mu==[mean_bounds(b,independent_q(b,node,k,box)) for node in (i,j)]
        assert F(v['variance_upper'])==mu[0][1]+mu[1][1]-2*common>=0
        assert list(map(F,v['mean']))==[mu[0][0]-mu[1][1],mu[0][1]-mu[1][0]]
        expected=mean_bounds(b,(qsub,qsub))[0] if delay<duration and qsub>0 else F(0);assert common==expected
        a,d,e,f=box
        for u,vv in ((a,e),(a,f),(d,e),(d,f),((a+d)/2,(e+f)/2)):
            zz=boosted(moved(b,u,vv));virtual=zz[tip].copy();virtual[0]+=sgn*delay
            for n in (i,j):
                dt1,dx,dy=[x-y for x,y in zip(virtual,zz[n])];assert sgn*dt1>=0 and dt1*dt1-dx*dx-dy*dy>=0
            if common:
                dt1,dx,dy=[x-y for x,y in zip(zz[k],virtual)];assert sgn*dt1>0 and dt1*dt1-dx*dx-dy*dy>=qsub
            counts['direct_subset_point_checks']+=1
        counts['whole_rectangle_subset_checks']+=1
    def law(stats,k,cert):
        key=json.dumps([stats,k,cert],sort_keys=True)
        if key in seen_laws:return
        seen_laws.add(key)
        if cert['status']!='ENCLOSED':
            assert cert['status'] in ('HOLD_RATE_BUDGET','HOLD_PROBABILITY_BUDGET') and cert['probability']==['0','1'];counts['budget_hold_laws']+=1;return
        a,d=[tuple(map(F,v)) for v in stats['count_mean_intervals']];lo=F(stats['common_mean_lower']);hi=min(a[1],d[1]);ss=cert['slices']
        assert 0<=lo<=hi and cert['threshold']==k and cert['overlap_range']==list(map(str,(lo,hi)))
        assert len(ss)==c['overlap']['overlap_slices'];slice_cover(ss,lo,hi)
        if hi>lo:
            try:slice_cover(ss[1:],lo,hi)
            except AssertionError:counts['missing_overlap_slice_controls']+=1
            else:raise AssertionError('omitted overlap slice accepted')
        for j,s in enumerate(ss):
            l=lo+(hi-lo)*j/len(ss);u=lo+(hi-lo)*(j+1)/len(ss);plus=(max(F(0),a[0]-u),a[1]-l);minus=(max(F(0),d[0]-u),d[1]-l)
            assert s['overlap']==list(map(str,(l,u))) and s['plus']==list(map(str,plus)) and s['minus']==list(map(str,minus))
            assert len(s['records'])==2
            for rec,label,(x,y) in zip(s['records'],('lower','upper'),((minus[0],plus[1]),(minus[1],plus[0]))):
                assert rec['endpoint']==label and F(rec['x_mean'])==x and F(rec['y_mean'])==y
                assert 0<=x<=c['overlap']['maximum_exclusive_mean'] and 0<=y<=c['overlap']['maximum_exclusive_mean']
                signature=(str(x),str(y),k)
                if signature not in seen_pmf:
                    truth=decimal_difference(x,y,k);assert Decimal(rec['probability'][0])<=truth<=Decimal(rec['probability'][1]);seen_pmf.add(signature);counts['independent_110_digit_difference_PMF_checks']+=1
                assert F(rec['numerical_width_upper'])<=F(c['overlap']['probability']['numerical_event_width_target'])+F(1,10**75)
                for name,mu in (('x',x),('y',y)):
                    meta=rec['normalization'][name];assert int(meta['mode'])==mu.__floor__()
                    assert int(meta['upper'])==int(meta['mode'])+c['overlap']['probability'][name+'_upper_steps']
                    assert 0<int(meta['zlo'])<=int(meta['zhi']) and (int(meta['tail'])==0)==(mu==0)
            p=tuple(map(F,s['probability']));assert 0<=p[0]<=p[1]<=1
            assert p[0]<=F(s['records'][0]['probability'][0]) and p[1]>=F(s['records'][1]['probability'][1]);counts['exclusive_rate_rectangles']+=1
        assert list(map(F,cert['probability']))==[min(F(s['probability'][0]) for s in ss),max(F(s['probability'][1]) for s in ss)]
        counts['uniform_difference_laws']+=1
    for index,(r,source) in enumerate(zip(overlaps,wanted)):
        assert r['box']==source['box'];choices=overlap_candidates(b,list(map(F,r['box'])))
        if 'reason' in r:assert not choices and r['status']=='HOLD';continue
        e=choices[0];assert all(r[k]==e[k] for k in ('anchor','side','threshold')) and r['score']==str(e['score'])
        assert r['base_statistics']==e['base'] and r['moved_statistics']==e['moved']
        base=bases[r['base_law_id']];used_bases.add(r['base_law_id']);assert base['anchor']==r['anchor'] and base['threshold']==r['threshold']
        geometry([F(0)]*4,e['base']);geometry(list(map(F,r['box'])),e['moved'])
        law(e['base'],e['threshold'],base['law']);law(e['moved'],e['threshold'],r['moved_law'])
        p,q=[tuple(map(F,x['probability'])) for x in (base['law'],r['moved_law'])];tv=max(F(0),p[0]-q[1],q[0]-p[1]);assert r['tv_lower']==outward(tv)[0]
        assert (r['status']=='OVERLAP_TAIL_EXCLUDED')==(tv>F(c['tv_gate']))
        if (index+1)%8==0:print(json.dumps(dict(overlap_audited=index+1,independent_PMF_checks=len(seen_pmf))),flush=True)
    assert used_bases==set(range(len(bases))) and len({(r['anchor'],r['threshold']) for r in bases})==len(bases)
    # Rebuild the complete original tree and apply only the declared replacements.
    oldmap={r['path']:r for r in old_final};active=dict(oldmap);paths={r['path'] for r in pending}
    for stage in (rows,overlaps):
        for r in stage:assert r['path'] in paths and active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box'];active[r['path']]=r
    assert set(active)==set(oldmap)
    untouched=[p for p in oldmap if p not in paths];assert all(active[p]==oldmap[p] for p in untouched)
    assert sum(oldmap[p]['status']=='HOLD' for p in untouched)==31
    final=sorted(active.values(),key=lambda r:tuple(map(int,r['path'].split('/'))));assert final==combined(archive)
    states=Counter(r['status'] for r in final);areas=Counter()
    for r in final:areas[r['status']]+=area(r)
    total=F(1,25);held=areas['HOLD'];assert sum(areas.values())==total
    assert states==summary['states'] and {k:str(v) for k,v in areas.items()}==summary['areas']
    assert str(held)==summary['hold_area'] and str(1-held/total)==summary['excluded_area_fraction']
    assert summary['unresolved_cells']==[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    assert summary['new_states']==Counter(r['status'] for r in final if r['path'] in paths)
    assert summary['newly_excluded_cells']==sum(active[p]['status']!='HOLD' for p in paths)
    assert len(final)==summary['terminal_cells']==2104
    for x,y,k in ((F(1,4),F(1,2),0),(F(1,2),F(1,4),1),(F(1,4),F(1,4),0)):
        expected=small_exact_reference(x,y,1,k);got,_=jr.event(x,y,1,k,c['overlap']['probability'])
        assert got[0]<=expected[0]<=expected[1]<=got[1];truth=decimal_difference(x,y,k)
        assert Decimal(outward(*got,digits=65)[0])<=truth<=Decimal(outward(*got,digits=65)[1]);counts['exact_small_mean_controls']+=1
    independent,_=jr.event(F(1),F(1),1,0,c['overlap']['probability']);assert independent[1]<1
    assert jr.event(F(0),F(0),1,0,c['overlap']['probability'])[0]==(F(1),F(1))
    return dict(status='PASS',**dict(counts),new_input_rectangles_checked=len(rows),old_rectangles_preserved=len(untouched),unchanged_prior_holds=31,complete_square_covers=1,terminal_rectangles=len(final),hold_cells_preserved=states.get('HOLD',0),all_inputs_received_actual_exact_events=True,dependence_counterexample=True,source_tree=c['source_tree'],scope='Exact whole-rectangle geometry and directed probabilities certify claims; independent direct PMFs audit the computation. Caches are exact certificate reuse, not independent statistical replicates. Area is not probability.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
