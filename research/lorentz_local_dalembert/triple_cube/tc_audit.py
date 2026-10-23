"""Independent three-variable geometry, direct moment solves, PMFs and coverage.
SPDX-License-Identifier: Apache-2.0
"""
from tc_common import *
from tc_algebra import algebra,direct_change
from decimal import Decimal,localcontext
from sft_audit import decimal_difference
from pto_audit import decimal_cdf
from ot_audit import slice_cover
from jr_audit import small_exact_reference
from ps_audit import tree as old_tree

def independent_q(b,i,j,box):
    shifts={node:tuple(box[2*k:2*k+2]) for k,node in enumerate(b['nodes'])}
    zi,zj=b['boost'][i],b['boost'][j];li,ui=shifts.get(i,(F(0),F(0)));lj,uj=shifts.get(j,(F(0),F(0)))
    lo=zj[1]-zi[1]+lj-ui;hi=zj[1]-zi[1]+uj-li
    q=(zj[0]-zi[0])**2-(zj[2]-zi[2])**2
    return q-max(lo*lo,hi*hi),q-(F(0) if lo<=0<=hi else min(lo*lo,hi*hi))

def box_for_path(path,c):
    parts=list(map(int,path.split('/')));n=c['grid_per_axis'];index=parts[0];assert 0<=index<n**3
    i,rest=divmod(index,n*n);j,k=divmod(rest,n);lo,hi=map(F,c['domain']);box=[]
    for a in (i,j,k):box.extend((lo+(hi-lo)*a/n,lo+(hi-lo)*(a+1)/n))
    for child in parts[1:]:
        assert 0<=child<8
        for axis,bit in enumerate((child//4,(child//2)%2,child%2)):
            mid=(box[2*axis]+box[2*axis+1])/2;box[2*axis+1-bit]=mid
    return box

def tree(ar,c):
    rows={r['path']:r for r in ar['cells']};assert len(rows)==len(ar['cells']);n=c['grid_per_axis']
    active={str(i):rows[str(i)] for i in range(n**3)};seen=set(active)
    assert len(ar['splits'])<=c['refinement_rounds']
    for level in ar['splits']:
        wanted=sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:c['maximum_parents_per_round']]
        assert level==[r['path'] for r in wanted]
        for path in level:
            assert active.pop(path)['status']=='HOLD'
            for j in range(8):
                name=path+'/'+str(j);assert name not in seen;seen.add(name);active[name]=rows[name]
    assert seen==set(rows)
    assert len(ar['splits'])==c['refinement_rounds'] or not any(r['status']=='HOLD' for r in active.values())
    for path,r in rows.items():assert list(map(F,r['box']))==box_for_path(path,c)
    geometric=list(active.values())
    for stage,maximum in (('marginal',c['maximum_marginal_cells']),('overlap',c['maximum_overlap_cells'])):
        wanted=sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:maximum]
        assert [r['path'] for r in ar[stage]]==[r['path'] for r in wanted]
        for r in ar[stage]:assert r['box']==active[r['path']]['box'];active[r['path']]=r
    return geometric,sorted(active.values(),key=path_key)

def projection_cover(box,entries):
    a,d,e,f=box[:4];cuts={a,d}
    for r in entries:
        x,y,_,_=map(F,r['box']);cuts.update(v for v in (x,y) if a<v<d)
    cuts=sorted(cuts)
    for x,y in zip(cuts,cuts[1:]):
        mid=(x+y)/2;segments=[]
        for r in entries:
            l,u,lo,hi=map(F,r['box'])
            if l<=mid<=u:segments.append((max(e,lo),min(f,hi)))
        end=e
        for lo,hi in sorted(segments):
            if hi<=end:continue
            if lo>end:return False
            end=hi
        if end<f:return False
    return True

def audit():
    frozen();c=read(HERE/'contract.json');ar=read(HERE/'certificates.json.gz');summary=read(HERE/'summary.json');b=setup(c);counts=Counter()
    assert algebra(c)==read(HERE/'algebra.json');counts['declared_algebra_controls']=len(c['algebra_controls'])
    geom,final=tree(ar,c);assert final==final_cells(ar)
    for cut in (0,len(ar['cells'])-1):
        bad=dict(ar,cells=[r for j,r in enumerate(ar['cells']) if j!=cut])
        try:tree(bad,c)
        except (AssertionError,KeyError):counts['missing_octree_cell_controls']+=1
        else:raise AssertionError('missing cell accepted')
    # Reconstruct the source cover before validating all projected event labels.
    parent=read(HERE.parent/'paired_surface/certificates.json.gz');parent_cells=old_tree(parent,read(HERE.parent/'paired_surface/contract.json'))
    active={r['path']:r for r in parent_cells}
    for folder,stages in (('surface_tail',('marginal','overlap')),('surface_overlap_refinement',('missing','refined'))):
        previous=read(HERE.parent/folder/'certificates.json.gz')
        for stage in stages:
            for r in previous[stage]:
                assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box'];active[r['path']]=r
    assert len(active)==2104 and all(r['status']!='HOLD' for r in active.values())
    invs=ar['projection_sources'];strips=ar['node5_strips'];assert invs==source_inventory(b) and strips==node5_strips(b)
    for r in invs:
        assert r['box']==active[r['path']]['box'] and r['status']==active[r['path']]['status']!='GAP_EXCLUDED'
        assert all(5 not in pair for pair in r['pairs'])
        if r['status']!='ORDER_EXCLUDED':assert F(r['tv_lower'])>F(c['tv_gate'])
    eligible={r['path'] for r in invs}
    assert not any(r['path'] in eligible for r in active.values() if r['status']=='GAP_EXCLUDED');counts['old_gap_nontransfer_controls']+=1
    pairs={tuple(pair) for r in invs for pair in r['pairs']}
    for pair in pairs:
        low=moved(b,F(1,100),F(-1,50),F(-1,10));high=moved(b,F(1,100),F(-1,50),F(1,10))
        assert all(low[n]==high[n] for n in pair);counts['projection_endpoint_invariance_checks']+=1
    for r in strips:
        assert all(n==5 or n<5 for pair in r['pairs'] for n in pair) and F(r['tv_lower'])>F(c['tv_gate'])
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
    rows=ar['marginal'];events=ar['marginal_events'];overlaps=ar['overlap'];bases=ar['overlap_base_laws']
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
        # A precondition failure remains HOLD; it is not counted as an evaluated probability.
    assert used==set(range(len(events)))
    if len(events)>1:
        first=next(r for r in rows if r['attempts'] and 'event_id' in r['attempts'][0]);choice=marginal_candidates(b,list(map(F,first['box'])))[0]
        wrong=dict(first['attempts'][0],event_id=(first['attempts'][0]['event_id']+1)%len(events))
        try:cached_event(wrong,choice)
        except AssertionError:counts['wrong_cached_certificate_controls']+=1
        else:raise AssertionError('wrong cached event accepted')
    seen_geometry=set();seen_laws=set();seen_pmf=set();used_bases=set()
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
    for index,r in enumerate(overlaps):
        choices=overlap_candidates(b,list(map(F,r['box'])))
        if 'reason' in r:assert not choices and r['status']=='HOLD';continue
        e=choices[0];assert all(r[k]==e[k] for k in ('pair','anchor','side','threshold')) and r['score']==str(e['score'])
        assert r['base_statistics']==e['base'] and r['moved_statistics']==e['moved']
        base=bases[r['base_law_id']];used_bases.add(r['base_law_id']);assert all(base[k]==r[k] for k in ('pair','anchor','threshold'))
        geometry([F(0)]*6,e['pair'],e['base']);geometry(list(map(F,r['box'])),e['pair'],e['moved'])
        law(e['base'],e['threshold'],base['law']);law(e['moved'],e['threshold'],r['moved_law'])
        a,d=[tuple(map(F,x['probability'])) for x in (base['law'],r['moved_law'])];tv=max(F(0),a[0]-d[1],d[0]-a[1])
        assert r['tv_lower']==outward(tv)[0] and r['status']==('OVERLAP_TAIL_EXCLUDED' if tv>F(c['tv_gate']) else 'HOLD')
        print(json.dumps(dict(overlap_cells_audited=index+1,independent_PMF_checks=len(seen_pmf))),flush=True)
    assert used_bases==set(range(len(bases))) and len({(tuple(r['pair']),r['anchor'],r['threshold']) for r in bases})==len(bases)
    states=Counter(r['status'] for r in final);volumes=Counter()
    for r in final:volumes[r['status']]+=volume(r)
    total=F(1,125);held=volumes['HOLD'];assert sum(volumes.values())==total
    assert states==summary['states'] and {k:str(v) for k,v in volumes.items()}==summary['volumes']
    assert str(held)==summary['hold_volume'] and str(1-held/total)==summary['excluded_volume_fraction']
    assert summary['unresolved_cells']==[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    assert len(final)==summary['terminal_cells'] and len(ar['cells'])==summary['evaluated_geometric_cells']
    assert summary['status']==('THREE_PARAMETER_CUBE_EXCLUDED' if not held else 'HOLD_THREE_PARAMETER_CUBE')
    for x,y,k in ((F(1,4),F(1,2),0),(F(1,2),F(1,4),1),(F(1,4),F(1,4),0)):
        expected=small_exact_reference(x,y,1,k);got,_=jr.event(x,y,1,k,c['overlap']['probability']);assert got[0]<=expected[0]<=expected[1]<=got[1]
        counts['exact_small_mean_controls']+=1
    independent,_=jr.event(F(1),F(1),1,0,c['overlap']['probability']);assert independent[1]<1
    assert jr.event(F(0),F(0),1,0,c['overlap']['probability'])[0]==(F(1),F(1))
    return dict(status='PASS',**dict(counts),source_square_cells_checked=2104,eligible_projection_source_cells=len(invs),node5_source_strips=len(strips),geometric_cells_checked=len(ar['cells']),finite_operator_enclosures=finite_operators,terminal_cells=len(final),hold_cells_preserved=states.get('HOLD',0),complete_closed_cube_covers=1,dependence_counterexample=True,inherited_zero_third_slice_fully_excluded=True,source_tree=c['source_tree'],scope='Exact uniform geometry and interval/integer certificates carry the exclusions. Direct point solves and decimal PMFs are independent diagnostic checks, not replacements for box proofs. No general stability claim.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
