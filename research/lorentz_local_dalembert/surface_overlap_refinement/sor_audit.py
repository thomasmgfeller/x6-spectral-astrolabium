"""Independent geometry, direct PMFs, slice refinement and complete source cover.
SPDX-License-Identifier: Apache-2.0
"""
from sor_common import *
from decimal import Decimal
from sft_audit import decimal_difference
from ps_audit import tree as source_tree,independent_q
from ot_audit import slice_cover
from jr_audit import small_exact_reference
from ps_common import jr

def audit():
    frozen();c=read(HERE/'contract.json');previous,old_final,pending,missing,prior=inputs()
    archive=read(HERE/'certificates.json.gz');summary=read(HERE/'summary.json');b=setup(c);counts=Counter()
    bases=archive['base_laws'];seen_geometry=set();seen_laws=set();seen_pmf=set();used_bases=set();seen_refinement=set()
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
    def law(stats,k,cert,settings):
        key=json.dumps([stats,k,cert],sort_keys=True)
        if key in seen_laws:return
        seen_laws.add(key)
        if cert['status']!='ENCLOSED':
            assert cert['status'] in ('HOLD_RATE_BUDGET','HOLD_PROBABILITY_BUDGET') and cert['probability']==['0','1'];counts['budget_hold_laws']+=1;return
        a,d=[tuple(map(F,v)) for v in stats['count_mean_intervals']];lo=F(stats['common_mean_lower']);hi=min(a[1],d[1]);ss=cert['slices']
        assert 0<=lo<=hi and cert['threshold']==k and cert['overlap_range']==list(map(str,(lo,hi)))
        assert len(ss)==settings['overlap']['overlap_slices'];slice_cover(ss,lo,hi)
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
                assert 0<=x<=settings['overlap']['maximum_exclusive_mean'] and 0<=y<=settings['overlap']['maximum_exclusive_mean']
                signature=(str(x),str(y),k)
                if signature not in seen_pmf:
                    truth=decimal_difference(x,y,k);assert Decimal(rec['probability'][0])<=truth<=Decimal(rec['probability'][1]);seen_pmf.add(signature);counts['independent_110_digit_difference_PMF_checks']+=1
                assert F(rec['numerical_width_upper'])<=F(settings['overlap']['probability']['numerical_event_width_target'])+F(1,10**75)
                for name,mu in (('x',x),('y',y)):
                    meta=rec['normalization'][name];assert int(meta['mode'])==mu.__floor__()
                    assert int(meta['upper'])==int(meta['mode'])+settings['overlap']['probability'][name+'_upper_steps']
                    assert 0<int(meta['zlo'])<=int(meta['zhi']) and (int(meta['tail'])==0)==(mu==0)
            p=tuple(map(F,s['probability']));assert 0<=p[0]<=p[1]<=1
            assert p[0]<=F(s['records'][0]['probability'][0]) and p[1]>=F(s['records'][1]['probability'][1]);counts['exclusive_rate_rectangles']+=1
        assert list(map(F,cert['probability']))==[min(F(s['probability'][0]) for s in ss),max(F(s['probability'][1]) for s in ss)]
        counts['uniform_difference_laws']+=1
    def check_inputs(rows,wanted):
        assert [r['path'] for r in rows]==[r['path'] for r in wanted]
        assert len({r['path'] for r in rows})==len(rows)
        assert all(r['box']==s['box'] for r,s in zip(rows,wanted))
    def check_base(entry,r,stage):
        assert entry['stage']==stage and entry['slices']==c['slices'][stage]
        assert entry['anchor']==r['anchor'] and entry['threshold']==r['threshold']
        if entry['law']['status']=='ENCLOSED':assert len(entry['law']['slices'])==c['slices'][stage]
    def refinement(coarse,fine):
        signature=json.dumps([coarse,fine],sort_keys=True)
        if signature in seen_refinement:return
        seen_refinement.add(signature)
        if coarse['status']!='ENCLOSED' or fine['status']!='ENCLOSED':return
        assert coarse['threshold']==fine['threshold'] and coarse['overlap_range']==fine['overlap_range']
        assert len(fine['slices'])==8*len(coarse['slices'])==512
        for j,f in enumerate(fine['slices']):
            parent=coarse['slices'][j//8]
            for key in ('overlap','plus','minus'):
                a,d=map(F,parent[key]);e,g=map(F,f[key]);assert a<=e<=g<=d
            counts['fine_rate_rectangles_inside_coarse_parent']+=1
        # Verify the achieved numerical improvement as well as set containment.
        a,d=map(F,coarse['probability']);e,g=map(F,fine['probability']);assert a<=e<=g<=d
        counts['nested_probability_laws']+=1
    prior_map={r['path']:r for r in prior};first_map={r['path']:r for r in archive['missing']}
    for stage,wanted in (('missing',missing),('refined',pending_refinement(archive['missing']))):
        rows=archive[stage];settings=stage_contract(c,stage);check_inputs(rows,wanted)
        assert len(rows)<=(c['missing_overlap_cells'] if stage=='missing' else c['maximum_refined_cells'])
        if rows:
            try:check_inputs(rows[1:],wanted)
            except AssertionError:counts['missing_input_rectangle_controls']+=1
            else:raise AssertionError('missing input accepted')
        for index,(r,source) in enumerate(zip(rows,wanted)):
            choices=overlap_candidates(b,list(map(F,r['box'])))
            if 'reason' in r:assert not choices and r['status']=='HOLD';continue
            e=choices[0];assert all(r[k]==e[k] for k in ('anchor','side','threshold')) and r['score']==str(e['score'])
            assert r['base_statistics']==e['base'] and r['moved_statistics']==e['moved']
            base=bases[r['base_law_id']];used_bases.add(r['base_law_id']);check_base(base,r,stage)
            if index==0:
                broken=dict(base,stage='refined' if stage=='missing' else 'missing')
                try:check_base(broken,r,stage)
                except AssertionError:counts['wrong_resolution_cache_controls']+=1
                else:raise AssertionError('wrong cache resolution accepted')
            geometry([F(0)]*4,e['base']);geometry(list(map(F,r['box'])),e['moved'])
            law(e['base'],e['threshold'],base['law'],settings);law(e['moved'],e['threshold'],r['moved_law'],settings)
            p,q=[tuple(map(F,x['probability'])) for x in (base['law'],r['moved_law'])]
            tv=max(F(0),p[0]-q[1],q[0]-p[1]);assert r['tv_lower']==outward(tv)[0]
            assert r['status']==('OVERLAP_TAIL_EXCLUDED' if tv>F(c['tv_gate']) else 'HOLD')
            if stage=='refined':
                coarse=prior_map.get(r['path'],first_map.get(r['path']));assert coarse is not None
                assert all(r[k]==coarse[k] for k in ('anchor','side','threshold','score','base_statistics','moved_statistics'))
                old_base=coarse['base_law'] if 'base_law' in coarse else bases[coarse['base_law_id']]['law']
                refinement(old_base,base['law']);refinement(coarse['moved_law'],r['moved_law'])
                counts['unchanged_refined_events']+=1
            print(json.dumps(dict(stage_audited=stage,cells=index+1,total=len(rows),independent_PMF_checks=len(seen_pmf))),flush=True)
    assert used_bases==set(range(len(bases)))
    assert len({(r['stage'],r['anchor'],r['threshold']) for r in bases})==len(bases)
    # Independent source-tree reconstruction and stage replacement, retaining all boundaries.
    parent=read(HERE.parent/'paired_surface/certificates.json.gz')
    initial=source_tree(parent,read(HERE.parent/'paired_surface/contract.json'))
    active={r['path']:r for r in initial};tail=read(HERE.parent/'surface_tail/certificates.json.gz')
    for stage in ('marginal','overlap'):
        for r in tail[stage]:
            assert active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box'];active[r['path']]=r
    assert sorted(active.values(),key=path_key)==old_final
    untouched={p:r for p,r in active.items() if r['status']!='HOLD'};assert len(untouched)==2073
    paths={r['path'] for r in pending}
    for stage in ('missing','refined'):
        for r in archive[stage]:
            assert r['path'] in paths and active[r['path']]['status']=='HOLD' and active[r['path']]['box']==r['box'];active[r['path']]=r
    assert all(active[p]==r for p,r in untouched.items())
    final=sorted(active.values(),key=path_key);assert final==combined(archive)
    states=Counter(r['status'] for r in final);areas=Counter()
    for r in final:areas[r['status']]+=area(r)
    total=F(1,25);held=areas['HOLD'];assert sum(areas.values())==total
    assert states==summary['states'] and {k:str(v) for k,v in areas.items()}==summary['areas']
    assert str(held)==summary['hold_area'] and str(1-held/total)==summary['excluded_area_fraction']
    assert summary['unresolved_cells']==[dict(path=r['path'],box=r['box']) for r in final if r['status']=='HOLD']
    assert summary['new_states']==Counter(r['status'] for r in final if r['path'] in paths)
    assert summary['newly_excluded_cells']==sum(active[p]['status']!='HOLD' for p in paths)
    assert summary['status']==('TWO_PARAMETER_SQUARE_EXCLUDED' if not held else 'HOLD_SURFACE_OVERLAP_REFINEMENT')
    assert len(final)==summary['terminal_cells']==2104
    for x,y,k in ((F(1,4),F(1,2),0),(F(1,2),F(1,4),1),(F(1,4),F(1,4),0)):
        expected=small_exact_reference(x,y,1,k);got,_=jr.event(x,y,1,k,c['overlap']['probability'])
        assert got[0]<=expected[0]<=expected[1]<=got[1];truth=decimal_difference(x,y,k)
        assert Decimal(outward(*got,digits=65)[0])<=truth<=Decimal(outward(*got,digits=65)[1]);counts['exact_small_mean_controls']+=1
    independent,_=jr.event(F(1),F(1),1,0,c['overlap']['probability']);assert independent[1]<1
    assert jr.event(F(0),F(0),1,0,c['overlap']['probability'])[0]==(F(1),F(1))
    return dict(status='PASS',**dict(counts),new_input_rectangles_checked=len(pending),old_exclusions_preserved=len(untouched),complete_square_covers=1,terminal_rectangles=len(final),hold_cells_preserved=states.get('HOLD',0),dependence_counterexample=True,source_tree=c['source_tree'],scope='Exact whole-rectangle geometry and directed probabilities certify claims. Independent direct PMFs audit the computation. The same event is retained under slice refinement; all other cells are unchanged. No general stability claim.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
