"""Independent geometry, complete slices, nesting, cache and cover checks.
SPDX-License-Identifier: Apache-2.0
"""
from tor_common import *
from tt_audit import checked_cover as parent_cover
from tc_audit import independent_q
from decimal import Decimal
from sft_audit import decimal_difference
from ot_audit import slice_cover
from jr_audit import small_exact_reference

def checked_cover(ar,c):
    old,_,source,pending,missing,prior=inputs()
    assert parent_cover(old,read(HERE.parent/'triple_tail/contract.json'))==source
    assert len(source)==c['expected_terminal_cells'] and len(pending)==c['expected_source_holds']
    assert len(missing)==c['missing_overlap_cells'] and len(prior)==c['prior_overlap_holds']
    assert [r['path'] for r in ar['missing']]==[r['path'] for r in missing]
    active={r['path']:r for r in pending}
    for r in ar['missing']:
        assert active[r['path']]['box']==r['box'] and r['stage']=='missing';active[r['path']]=r
    wanted=sorted((r for r in active.values() if r['status']=='HOLD'),key=path_key)
    assert len(wanted)<=c['maximum_refined_cells']
    assert [r['path'] for r in ar['refined']]==[r['path'] for r in wanted]
    for r in ar['refined']:assert active[r['path']]['box']==r['box'] and r['stage']=='refined'
    final=combined(ar);lookup={r['path']:r for r in final};pending_paths=set(active)
    for r in source:
        assert lookup[r['path']]['box']==r['box']
        if r['path'] not in pending_paths:assert lookup[r['path']]==r
    assert len(lookup)==len(final)==len(source)
    return final

def audit():
    frozen();c=read(HERE/'contract.json');ar=read(HERE/'certificates.json.gz');summary=read(HERE/'summary.json');b=setup(c);counts=Counter()
    final=checked_cover(ar,c);laws=ar['laws']
    old,previous,source,pending,missing,prior=inputs();cube=read(HERE.parent/'triple_cube/certificates.json.gz')
    for stage in ('missing','refined'):
        if ar[stage]:
            bad=dict(ar);bad[stage]=ar[stage][1:]
            try:checked_cover(bad,c)
            except (AssertionError,KeyError):counts['missing_stage_input_controls']+=1
            else:raise AssertionError('missing stage input accepted')
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
    def law(stats,k,cert,n):
        key=json.dumps([stats,k,cert],sort_keys=True)
        if key in seen_laws:return
        seen_laws.add(key)
        if cert['status']!='ENCLOSED':
            assert cert['status'] in ('HOLD_RATE_BUDGET','HOLD_PROBABILITY_BUDGET') and cert['probability']==['0','1'];counts['budget_hold_laws']+=1;return
        a,d=[tuple(map(F,v)) for v in stats['count_mean_intervals']];lo=F(stats['common_mean_lower']);hi=min(a[1],d[1]);ss=cert['slices']
        assert 0<=lo<=hi and cert['threshold']==k and cert['overlap_range']==list(map(str,(lo,hi)))
        assert len(ss)==n;slice_cover(ss,lo,hi)
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
        assert record['stage']==r['stage'] and record['slices']==r['slices']==c['slices'][r['stage']]
        assert all(record[k]==e[k] for k in ('pair','anchor','threshold'))
        assert record['statistics']==e[side]
        used_laws.add(r[side+'_law_id'])
        return record['law']
    earlier={r['path']:r for r in prior};earlier.update({r['path']:r for r in ar['missing'] if r['status']=='HOLD'})
    first_paths={r['path'] for r in ar['missing']};seen_nesting=set()
    def previous_law(row,side):
        if row['path'] in first_paths:return laws[row[side+'_law_id']]['law']
        if 'moved_law_id' in row:return old['overlap_laws'][row[side+'_law_id']]['law']
        return cube['overlap_base_laws'][row['base_law_id']]['law'] if side=='base' else row['moved_law']
    def nesting(fine_id,coarse):
        fine=laws[fine_id]['law'];key=(fine_id,hashlib.sha256(json.dumps(coarse,sort_keys=True).encode()).hexdigest())
        if key in seen_nesting:return
        seen_nesting.add(key)
        if coarse['status']!='ENCLOSED' or fine['status']!='ENCLOSED':counts['unavailable_nesting_checks']+=1;return
        assert coarse['threshold']==fine['threshold'] and coarse['overlap_range']==fine['overlap_range']
        assert len(coarse['slices'])==64 and len(fine['slices'])==512
        for j,s in enumerate(fine['slices']):
            q=coarse['slices'][j//8]
            for name in ('overlap','plus','minus'):
                a,d=map(F,q[name]);x,y=map(F,s[name]);assert a<=x<=y<=d
            counts['nested_exclusive_rectangle_checks']+=1
        counts['fine_coarse_law_nesting_checks']+=1
    for stage in ('missing','refined'):
        for index,r in enumerate(ar[stage]):
            choices=overlap_candidates(b,list(map(F,r['box'])))
            if 'reason' in r:assert not choices and r['status']=='HOLD' and r['reason']=='NO_TIMELIKE_PAIR_ANCHOR';continue
            e=choices[0];assert all(r[k]==e[k] for k in ('pair','anchor','side','threshold')) and r['score']==str(e['score'])
            assert r['base_statistics']==e['base'] and r['moved_statistics']==e['moved']
            base=checked_law(r,e,'base');alt=checked_law(r,e,'moved')
            geometry([F(0)]*6,e['pair'],e['base']);geometry(list(map(F,r['box'])),e['pair'],e['moved'])
            law(e['base'],e['threshold'],base,c['slices'][stage]);law(e['moved'],e['threshold'],alt,c['slices'][stage])
            a,d=[tuple(map(F,x['probability'])) for x in (base,alt)];tv=max(F(0),a[0]-d[1],d[0]-a[1])
            assert r['tv_lower']==outward(tv)[0] and r['status']==('OVERLAP_TAIL_EXCLUDED' if tv>F(c['tv_gate']) else 'HOLD')
            if stage=='refined':
                before=earlier[r['path']]
                assert all(before[k]==r[k] for k in ('box','pair','anchor','side','threshold','score','base_statistics','moved_statistics'))
                for side in ('base','moved'):nesting(r[side+'_law_id'],previous_law(before,side))
                counts['unchanged_event_refinements']+=1
            if (index+1)%8==0:print(json.dumps(dict(stage=stage,overlap_cells_audited=index+1,independent_PMF_checks=len(seen_pmf))),flush=True)
    assert used_laws==set(range(len(laws)))
    keys=[json.dumps([r[k] for k in ('stage','slices','pair','anchor','threshold','statistics')],sort_keys=True) for r in laws]
    assert len(keys)==len(set(keys))
    if len(laws)>1:
        r=next(r for stage in ('missing','refined') for r in ar[stage] if 'reason' not in r);e=overlap_candidates(b,list(map(F,r['box'])))[0]
        for side in ('base','moved'):
            wrong=dict(r);wrong[side+'_law_id']=(r[side+'_law_id']+1)%len(laws)
            try:checked_law(wrong,e,side)
            except AssertionError:counts['wrong_overlap_cache_controls']+=1
            else:raise AssertionError('wrong law accepted')
        wrong=dict(r,slices=512 if r['slices']==64 else 64)
        try:checked_law(wrong,e,'base')
        except AssertionError:counts['wrong_resolution_controls']+=1
        else:raise AssertionError('wrong resolution accepted')
    states=Counter(r['status'] for r in final);volumes=Counter()
    for r in final:volumes[r['status']]+=volume(r)
    total=F(previous['total_volume']);held=volumes['HOLD'];assert sum(volumes.values())==total
    assert states==summary['states'] and {k:str(v) for k,v in volumes.items()}==summary['volumes']
    assert str(held)==summary['hold_volume'] and str(1-held/total)==summary['excluded_volume_fraction']
    assert outward(100*(1-held/total))==summary['excluded_volume_percent']
    assert summary['unresolved_cells']==[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    assert len(final)==summary['terminal_cells']
    assert summary['status']==('THREE_PARAMETER_CUBE_EXCLUDED' if not held else 'HOLD_THREE_PARAMETER_CUBE')
    assert summary['previous_excluded_volume_fraction']==previous['excluded_volume_fraction']
    paths={r['path'] for r in pending};excluded=[r for r in final if r['path'] in paths and r['status']!='HOLD']
    comparisons=[dict(path=r['path'],old_tv_lower=earlier[r['path']].get('tv_lower'),new_tv_lower=r.get('tv_lower'),status=r['status']) for r in ar['refined']]
    expected=dict(source_hold_cells=len(pending),missing_overlap_cells_tested=len(ar['missing']),refined_cells_tested=len(ar['refined']),
        stage_states={stage:dict(Counter(r['status'] for r in ar[stage])) for stage in ('missing','refined')},
        comparisons_with_both_laws_enclosed={stage:sum('reason' not in r and all(laws[r[k]]['law']['status']=='ENCLOSED' for k in ('base_law_id','moved_law_id')) for r in ar[stage]) for stage in ('missing','refined')},
        distinct_laws=len(laws),law_states=dict(Counter(r['law']['status'] for r in laws)),distinct_laws_by_stage=dict(Counter(r['stage'] for r in laws)),
        newly_excluded_cells=len(excluded),newly_excluded_volume=str(sum((volume(r) for r in excluded),F(0))),
        minimum_new_full_law_tv_lower=min((r['tv_lower'] for r in excluded),key=F,default=None),prior_overlap_comparisons=comparisons)
    for k,v in expected.items():assert summary[k]==v,(k,v,summary[k])
    for x,y,k in ((F(1,4),F(1,2),0),(F(1,2),F(1,4),1),(F(1,4),F(1,4),0)):
        ref=small_exact_reference(x,y,1,k);got,_=jr.event(x,y,1,k,c['overlap']['probability']);assert got[0]<=ref[0]<=ref[1]<=got[1]
        counts['exact_small_mean_controls']+=1
    independent,_=jr.event(F(1),F(1),1,0,c['overlap']['probability']);assert independent[1]<1
    assert jr.event(F(0),F(0),1,0,c['overlap']['probability'])[0]==(F(1),F(1))
    return dict(status='PASS',**dict(counts),terminal_cells=len(final),complete_closed_cube_covers=1,
        source_exclusions_preserved=sum(r['status']!='HOLD' for r in source),hold_cells_preserved=states.get('HOLD',0),
        distinct_cached_overlap_laws=len(laws),dependence_counterexample=True,zero_rate_control=True,source_tree=c['source_tree'],
        scope='Independent geometry, complete slices and direct PMFs diagnose exact uniform interval/integer certificates. Cache reuse is not independent evidence. No general stability theorem.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
