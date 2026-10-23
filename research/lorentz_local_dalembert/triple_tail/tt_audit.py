"""Independent geometry, cache identities, PMFs and inherited-cover audit.
SPDX-License-Identifier: Apache-2.0
"""
from tt_common import *
from tc_audit import independent_q,tree
from decimal import Decimal,localcontext
from sft_audit import decimal_difference
from pto_audit import decimal_cdf
from ot_audit import slice_cover
from jr_audit import small_exact_reference

def checked_cover(ar,c):
    old,_,source,pending=inputs()
    _,independent=tree(old,read(HERE.parent/'triple_cube/contract.json'))
    assert independent==source
    assert len(pending)==c['expected_inputs'] and len(source)==c['expected_terminal_cells']
    assert [r['path'] for r in ar['marginal']]==[r['path'] for r in pending]
    assert [r['path'] for r in ar['overlap']]==[r['path'] for r in ar['marginal'] if r['status']=='HOLD']
    assert len(ar['marginal'])<=c['maximum_marginal_cells'] and len(ar['overlap'])<=c['maximum_overlap_cells']
    final=combined(ar);lookup={r['path']:r for r in final};changed={r['path'] for r in pending}
    for r in source:
        assert lookup[r['path']]['box']==r['box']
        if r['path'] not in changed:assert lookup[r['path']]==r
    assert len(lookup)==len(final)==len(source)
    return final

def audit():
    frozen();c=read(HERE/'contract.json');ar=read(HERE/'certificates.json.gz');summary=read(HERE/'summary.json');b=setup(c);counts=Counter()
    final=checked_cover(ar,c)
    for stage in ('marginal','overlap'):
        if ar[stage]:
            bad=dict(ar);bad[stage]=ar[stage][1:]
            try:checked_cover(bad,c)
            except (AssertionError,KeyError):counts['missing_stage_input_controls']+=1
            else:raise AssertionError('missing input accepted')
    rows=ar['marginal'];events=ar['marginal_events'];overlaps=ar['overlap'];laws=ar['overlap_laws']
    keys=[(e['index'],tuple(e['base']),tuple(e['moved'])) for e in events];assert len(keys)==len(set(keys))
    used=set();seen_marginal=set()
    def cached_event(a,e):
        assert a['score']==str(e['score']);v=events[a['event_id']]
        assert v['index']==e['index'] and v['base']==list(map(str,e['base'])) and v['moved']==list(map(str,e['moved']))
        return v
    for r in rows:
        box=list(map(F,r['box']));expected=marginal_candidates(b,box)[:c['maximum_marginal_events_per_cell']]
        assert 0<=len(r['attempts'])<=len(expected)
        for pos,(a,e) in enumerate(zip(r['attempts'],expected)):
            pair=b['ends'][e['index']];assert e['moved']==mean_bounds(b,independent_q(b,*pair,box))
            assert e['base']==mean_bounds(b,(interval(b['z'],*pair),)*2);counts['independent_event_mean_rectangles']+=1
            if 'reason' in a:
                assert a['index']==e['index'] and a['score']==str(e['score'])
                assert a['reason'] in ('HOLD_RATE_BUDGET','HOLD_OVERLAPPING_MEAN_BOUNDS','HOLD_EVENT_BUDGET')
                if a['reason']=='HOLD_RATE_BUDGET':assert max(e['base']+e['moved'])>c['poisson']['maximum_mean']
                if a['reason']=='HOLD_OVERLAPPING_MEAN_BOUNDS':assert not(e['base'][1]<e['moved'][0] or e['moved'][1]<e['base'][0])
                counts['skipped_marginal_attempts']+=1;continue
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
        # A precondition failure remains HOLD; it is not counted as an evaluated probability.
    assert used==set(range(len(events)))
    if len(events)>1:
        first=next(r for r in rows if r['attempts'] and 'event_id' in r['attempts'][0]);choice=marginal_candidates(b,list(map(F,first['box'])))[0]
        wrong=dict(first['attempts'][0],event_id=(first['attempts'][0]['event_id']+1)%len(events))
        try:cached_event(wrong,choice)
        except AssertionError:counts['wrong_cached_certificate_controls']+=1
        else:raise AssertionError('wrong cached event accepted')
    seen_geometry=set();seen_laws=set();seen_pmf=set();used_laws=set()
    def geometry(box,pair,v):
        key=(tuple(box),tuple(pair),v['anchor'])
        if key in seen_geometry:return
        seen_geometry.add(key);i,j=pair;k=v['anchor'];sgn=v['time_sign'];tip=v['tip'];delay=F(v['delay_upper']);duration=F(v['duration']);qsub=F(v['common_q_lower']);dt=abs(b['boost'][i][0]-b['boost'][j][0])
        qr=independent_q(b,i,j,box);assert v['pair_q_range']==list(map(str,qr))
        assert delay>=0 and (dt+delay)**2>=dt*dt-qr[0]
        assert qsub==independent_q(b,tip,k,box)[0]-2*duration*delay+delay*delay
        mu=[tuple(map(F,m)) for m in v['count_mean_intervals']];common=F(v['common_mean_lower'])
        assert mu==[mean_bounds(b,independent_q(b,node,k,box)) for node in (i,j)]
        assert F(v['variance_upper'])==mu[0][1]+mu[1][1]-2*common>=0
        assert list(map(F,v['mean']))==[mu[0][0]-mu[1][1],mu[0][1]-mu[1][0]]
        expected=mean_bounds(b,(qsub,qsub))[0] if delay<duration and qsub>0 else F(0);assert common==expected
        points=list(itertools.product(*(box[2*i:2*i+2] for i in range(3))))+[[sum(box[2*i:2*i+2])/2 for i in range(3)]]
        for point in points:
            zz=boosted(moved(b,*point));virtual=zz[tip].copy();virtual[0]+=sgn*delay
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
    def checked_law(r,e,side):
        record=laws[r[side+'_law_id']]
        assert all(record[k]==e[k] for k in ('pair','anchor','threshold'))
        assert record['statistics']==e[side]
        used_laws.add(r[side+'_law_id'])
        return record['law']
    for index,r in enumerate(overlaps):
        choices=overlap_candidates(b,list(map(F,r['box'])))
        if 'reason' in r:assert not choices and r['status']=='HOLD' and r['reason']=='NO_TIMELIKE_PAIR_ANCHOR';continue
        e=choices[0];assert all(r[k]==e[k] for k in ('pair','anchor','side','threshold')) and r['score']==str(e['score'])
        assert r['base_statistics']==e['base'] and r['moved_statistics']==e['moved']
        base=checked_law(r,e,'base');alt=checked_law(r,e,'moved')
        geometry([F(0)]*6,e['pair'],e['base']);geometry(list(map(F,r['box'])),e['pair'],e['moved'])
        law(e['base'],e['threshold'],base);law(e['moved'],e['threshold'],alt)
        a,d=[tuple(map(F,x['probability'])) for x in (base,alt)];tv=max(F(0),a[0]-d[1],d[0]-a[1])
        assert r['tv_lower']==outward(tv)[0] and r['status']==('OVERLAP_TAIL_EXCLUDED' if tv>F(c['tv_gate']) else 'HOLD')
        if (index+1)%16==0:print(json.dumps(dict(overlap_cells_audited=index+1,independent_PMF_checks=len(seen_pmf))),flush=True)
    assert used_laws==set(range(len(laws)))
    keys=[json.dumps([r['pair'],r['anchor'],r['threshold'],r['statistics']],sort_keys=True) for r in laws]
    assert len(keys)==len(set(keys))
    if len(laws)>1:
        r=next(r for r in overlaps if 'reason' not in r);e=overlap_candidates(b,list(map(F,r['box'])))[0]
        for side in ('base','moved'):
            wrong=dict(r);wrong[side+'_law_id']=(r[side+'_law_id']+1)%len(laws)
            try:checked_law(wrong,e,side)
            except AssertionError:counts['wrong_overlap_cache_controls']+=1
            else:raise AssertionError('wrong law accepted')
    states=Counter(r['status'] for r in final);volumes=Counter()
    for r in final:volumes[r['status']]+=volume(r)
    total=F(1,125);held=volumes['HOLD'];assert sum(volumes.values())==total
    assert states==summary['states'] and {k:str(v) for k,v in volumes.items()}==summary['volumes']
    assert str(held)==summary['hold_volume'] and str(1-held/total)==summary['excluded_volume_fraction']
    assert summary['unresolved_cells']==[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    assert len(final)==summary['terminal_cells']
    assert summary['status']==('THREE_PARAMETER_CUBE_EXCLUDED' if not held else 'HOLD_THREE_PARAMETER_CUBE')
    old,previous,source,pending=inputs();assert summary['previous_excluded_volume_fraction']==previous['excluded_volume_fraction']
    assert summary['new_excluded_volume']==str(F(previous['hold_volume'])-held)
    marg={r['path'] for r in rows if any('event_id' in a for a in r['attempts'])}
    ov={r['path'] for r in overlaps if 'reason' not in r and all(laws[r[k]]['law']['status']=='ENCLOSED' for k in ('base_law_id','moved_law_id'))}
    valid=marg|ov;pending_paths={r['path'] for r in pending}
    expected=dict(marginal_input_cells=len(rows),marginal_attempts=sum(len(r['attempts']) for r in rows),distinct_marginal_events=len(events),
        marginal_inputs_with_enclosed_event=len(marg),marginal_skipped_reasons=dict(Counter(a['reason'] for r in rows for a in r['attempts'] if 'reason' in a)),
        overlap_input_cells=len(overlaps),overlap_inputs_with_both_laws_enclosed=len(ov),distinct_overlap_laws=len(laws),overlap_law_states=dict(Counter(r['law']['status'] for r in laws)),
        inputs_with_enclosed_event=len(valid),inputs_without_enclosed_event=len(pending_paths-valid),
        preserved_previous_tested_holds=sum(r['status']=='HOLD' and r['path'] not in pending_paths for r in source),
        remaining_new_inputs=sum(r['status']=='HOLD' and r['path'] in pending_paths for r in final),
        remaining_new_inputs_without_enclosed_event=sum(r['status']=='HOLD' and r['path'] in pending_paths-valid for r in final),
        new_marginal_exclusions=sum(r['status']=='MARGINAL_TAIL_EXCLUDED' for r in rows),new_overlap_exclusions=sum(r['status']=='OVERLAP_TAIL_EXCLUDED' for r in overlaps))
    for k,v in expected.items():assert summary[k]==v,(k,v,summary[k])
    for x,y,k in ((F(1,4),F(1,2),0),(F(1,2),F(1,4),1),(F(1,4),F(1,4),0)):
        ref=small_exact_reference(x,y,1,k);got,_=jr.event(x,y,1,k,c['overlap']['probability']);assert got[0]<=ref[0]<=ref[1]<=got[1]
        counts['exact_small_mean_controls']+=1
    independent,_=jr.event(F(1),F(1),1,0,c['overlap']['probability']);assert independent[1]<1
    assert jr.event(F(0),F(0),1,0,c['overlap']['probability'])[0]==(F(1),F(1))
    return dict(status='PASS',**dict(counts),source_geometric_cells_checked=len(old['cells']),terminal_cells=len(final),complete_closed_cube_covers=1,
        source_exclusions_preserved=sum(r['status']!='HOLD' for r in source),source_tested_holds_preserved=expected['preserved_previous_tested_holds'],
        hold_cells_preserved=states.get('HOLD',0),all_398_inputs_attempted=True,inputs_with_enclosed_event=len(valid),distinct_cached_overlap_laws=len(laws),
        dependence_counterexample=True,zero_rate_control=True,source_tree=c['source_tree'],
        scope='Independent direct PMFs and point checks diagnose exact uniform interval/integer certificates. Cache reuse is not independent replication. No new operator solve or general stability claim.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
