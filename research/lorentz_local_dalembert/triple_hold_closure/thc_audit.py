"""Independent child geometry, direct operator solves, PMFs and source cover.
SPDX-License-Identifier: Apache-2.0
"""
from thc_common import *
from tsd_audit import checked_cover as source_cover
from tc_audit import independent_q,box_for_path,projection_cover
from tc_algebra import algebra,direct_change
from decimal import Decimal,localcontext
from sft_audit import decimal_difference
from pto_audit import decimal_cdf
from ot_audit import slice_cover
from jr_audit import small_exact_reference

def checked_cover(ar,c,source):
    pending=sorted((r for r in source if r['status']=='HOLD'),key=path_key)
    assert len(source)==c['source_terminal_cells'] and len(pending)==c['parent_cells']
    assert ar['splits']==[r['path'] for r in pending]
    cube_contract=read(HERE.parent/'triple_cube/contract.json')
    expected=[p['path']+'/'+str(j) for p in pending for j in range(8)]
    assert [r['path'] for r in ar['cells']]==expected and len(expected)==c['child_cells']
    active={r['path']:r for r in ar['cells']};assert len(active)==len(expected)
    for r in ar['cells']:assert list(map(F,r['box']))==box_for_path(r['path'],cube_contract)
    for p in pending:
        assert sum(volume(active[p['path']+'/'+str(j)]) for j in range(8))==volume(p)
    for stage,maximum in (('marginal',c['maximum_marginal_cells']),('overlap',c['maximum_overlap_cells'])):
        wanted=sorted((r for r in active.values() if r['status']=='HOLD'),key=path_key)
        assert len(wanted)<=maximum and [r['path'] for r in ar[stage]]==[r['path'] for r in wanted]
        for r in ar[stage]:assert r['box']==active[r['path']]['box'];active[r['path']]=r
    final=sorted(replace_round({r['path']:r for r in source},ar).values(),key=path_key);lookup={r['path']:r for r in final};parents=set(ar['splits'])
    for r in source:
        if r['path'] not in parents:assert lookup[r['path']]==r and r['status']!='HOLD'
    assert len(lookup)==len(final)==c['expected_terminal_cells']
    assert set(lookup)==(set(r['path'] for r in source)-parents)|set(expected)
    return final

def audit_round(ar,c,source):
    b=setup(c);counts=Counter()
    checked=lambda a,d:checked_cover(a,d,source)
    final=checked(ar,c)
    cube_contract=read(HERE.parent/'triple_cube/contract.json')
    assert algebra(cube_contract)==read(HERE.parent/'triple_cube/algebra.json');counts['inherited_algebra_controls_rechecked']=len(cube_contract['algebra_controls'])
    for index in (0,len(ar['cells'])-1):
        bad=dict(ar,cells=[r for j,r in enumerate(ar['cells']) if j!=index])
        try:checked(bad,c)
        except (AssertionError,KeyError):counts['missing_child_controls']+=1
        else:raise AssertionError('missing child accepted')
    bad=dict(ar,cells=[dict(r) for r in ar['cells']]);bad['cells'][0]['box']=list(bad['cells'][0]['box']);bad['cells'][0]['box'][0]=str(F(bad['cells'][0]['box'][0])+F(1,100000))
    try:checked(bad,c)
    except (AssertionError,KeyError):counts['wrong_child_boundary_controls']+=1
    else:raise AssertionError('wrong child box accepted')
    for stage in ('marginal','overlap'):
        if ar[stage]:
            bad=dict(ar);bad[stage]=ar[stage][1:]
            try:checked(bad,c)
            except (AssertionError,KeyError):counts['missing_stage_input_controls']+=1
            else:raise AssertionError('missing event-stage input accepted')
    invs,strips=transport_inventory()
    assert invs==source_inventory(b) and strips==node5_strips(b)
    assert all(r['status']!='GAP_EXCLUDED' and all(5 not in pair for pair in r['pairs']) for r in invs)
    seen_projections=set();finite_operators=0
    def direct_operator(box,record,corners=False):
        center=[(box[2*i]+box[2*i+1])/2 for i in range(3)];points=[center]
        if corners:points+=list(itertools.product(*(box[2*i:2*i+2] for i in range(3))))
        for point in points:
            change=direct_change(b,point)
            assert all(F(lo)<=d<=F(hi) for (lo,hi),d in zip(record['weight_change_bounds'],change))
            with localcontext() as ctx:
                ctx.prec=100
                dec=lambda x:Decimal(x.numerator)/Decimal(x.denominator)
                truth=[w+d for w,d in zip(b['weights'],change)]
                gap=2*sum(dec(x)**2 for x in change).sqrt()/(sum(dec(x)**2 for x in truth).sqrt()+sum(dec(x)**2 for x in b['weights']).sqrt())
                assert gap<=Decimal(record['gap_upper'])
            counts['independent_direct_weight_enclosure_checks']+=1
    for index,r in enumerate(ar['cells']):
        box=list(map(F,r['box']));status=r['status']
        for i in range(21):
            for j in range(i+1,21):
                assert qrange(b,i,j,box)==independent_q(b,i,j,box);counts['independent_exact_q_ranges']+=1
        if status=='PROJECTION_EXCLUDED':
            key=tuple(box[:4]);selected=[invs[j] for j in r['projection']['source_cells']]
            if key not in seen_projections:
                assert projection_cover(box,selected)
                assert not projection_cover(box,selected[1:]);counts['missing_projection_rectangle_controls']+=1
                seen_projections.add(key);counts['closed_projection_covers']+=1
        elif status=='AXIS_LAW_EXCLUDED':
            end=box[4]
            for j in r['transfer']['source_strips']:
                s=strips[j];assert F(s['lo'])<=end;end=max(end,F(s['hi']))
            assert end>=box[5] and F(r['transfer']['tv_lower'])>F(c['tv_gate']);counts['closed_node5_strip_covers']+=1
        elif status=='ORDER_EXCLUDED':
            rec=r['order'];q=interval(b['z'],*rec['pair']);lo,hi=independent_q(b,*rec['pair'],box)
            assert rec['base_q']==str(q) and rec['range']==list(map(str,(lo,hi)))
            assert (q>0 and hi<=0) or (q<0 and lo>=0);counts['whole_box_order_checks']+=1
        else:assert status in ('GAP_EXCLUDED','HOLD')
        if 'operator' in r and 'gap_upper' in r['operator']:
            op=r['operator'];assert F(op['neumann_norm_upper'])<=1
            direct_operator(box,op,finite_operators<c['audit_corner_boxes']);finite_operators+=1
            assert (status=='GAP_EXCLUDED')==(F(op['gap_upper'])<=F(c['gap_gate']))
        elif status in ('GAP_EXCLUDED','HOLD'):assert status=='HOLD' and r['operator']['status']=='HOLD_RANK_OR_ENCLOSURE'
        if (index+1)%128==0:print(json.dumps(dict(geometric_cells_audited=index+1,direct_operator_checks=counts['independent_direct_weight_enclosure_checks'])),flush=True)
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
    return dict(status='PASS',**dict(counts),new_children=len(ar['cells']),terminal_cells=len(final),remaining_hold_cells=sum(r['status']=='HOLD' for r in final)),final


def audit():
    frozen();c=read(HERE/'contract.json');summary=read(HERE/'summary.json')
    src_ar=read(HERE.parent/'triple_subdivision/certificates.json.gz')
    src_c=read(HERE.parent/'triple_subdivision/contract.json')
    current=source_cover(src_ar,src_c)
    assert current==original()[0]
    original_exclusions={r['path']:r for r in current if r['status']!='HOLD'}
    reports=[];total=0
    for rec in summary['rounds']:
        level=rec['level'];ar=read(HERE/('round_%02d.json.gz'%level))
        pending=[r for r in current if r['status']=='HOLD']
        rc=dict(c,parent_cells=len(pending),source_terminal_cells=len(current),child_cells=8*len(pending),expected_terminal_cells=len(current)+7*len(pending),maximum_marginal_cells=8*len(pending),maximum_overlap_cells=8*len(pending))
        report,current=audit_round(ar,rc,current);report['level']=level;reports.append(report)
        total+=len(ar['cells'])
        hold=[r for r in current if r['status']=='HOLD']
        assert rec['source_hold_cells']==len(pending) and rec['child_cells']==len(ar['cells'])
        assert rec['remaining_cells']==len(hold) and rec['hold_volume']==str(sum((volume(r) for r in hold),F(0)))
        assert rec['geometric_states']==dict(Counter(r['status'] for r in ar['cells']))
        for key,arr in [('marginal_input_cells','marginal'),('overlap_input_cells','overlap'),('distinct_marginal_events','marginal_events'),('distinct_overlap_laws','overlap_laws')]:assert rec[key]==len(ar[arr])
        print(json.dumps(dict(audited_round=level,report=report)),flush=True)
    states=Counter(r['status'] for r in current);volumes=Counter()
    for r in current:volumes[r['status']]+=volume(r)
    held=volumes['HOLD'];lookup={r['path']:r for r in current}
    assert sum(volumes.values())==F(1,125)
    assert all(lookup[k]==v for k,v in original_exclusions.items())
    assert states==summary['states'] and {k:str(v) for k,v in volumes.items()}==summary['volumes']
    assert total==summary['evaluated_new_geometric_cells']<=c['maximum_new_geometric_cells']
    assert len(current)==summary['terminal_cells'] and str(held)==summary['hold_volume']
    assert str(1-held*125)==summary['excluded_volume_fraction']
    assert summary['unresolved_cells']==[dict(path=r['path'],box=r['box']) for r in current if r['status']=='HOLD']
    assert summary['status']==('THREE_PARAMETER_CUBE_EXCLUDED' if not held else 'HOLD_THREE_PARAMETER_CUBE')
    closed=[p['path'] for p in original()[1] if not any(r['status']=='HOLD' and (r['path']==p['path'] or r['path'].startswith(p['path']+'/')) for r in current)]
    assert summary['closed_source_paths']==closed and summary['closed_source_hold_cells']==len(closed)
    assert summary['source_hold_cells']==38 and summary['source_exclusions_preserved']==len(original_exclusions)==1314
    assert not held or len(reports)==c['maximum_rounds'] or total+8*states['HOLD']>c['maximum_new_geometric_cells']
    for x,y,k in ((F(1,4),F(1,2),0),(F(1,2),F(1,4),1),(F(1,4),F(1,4),0)):
        ref=small_exact_reference(x,y,1,k);got,_=jr.event(x,y,1,k,c['overlap']['probability']);assert got[0]<=ref[0]<=ref[1]<=got[1]
    independent,_=jr.event(F(1),F(1),1,0,c['overlap']['probability']);assert independent[1]<1
    assert jr.event(F(0),F(0),1,0,c['overlap']['probability'])[0]==(F(1),F(1))
    return dict(status='PASS',exact_small_mean_controls=3,dependence_counterexample=True,zero_rate_control=True,rounds=reports,source_exclusions_preserved=1314,source_hold_cells=38,closed_source_hold_cells=len(closed),terminal_cells=len(current),hold_cells=states.get('HOLD',0),complete_closed_cube_cover=True,scope='Inherited exact uniform interval/integer certificates, independent exact geometry, direct moment and PMF diagnostics, negative controls; no independent personnel or formal proof-assistant verification.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
