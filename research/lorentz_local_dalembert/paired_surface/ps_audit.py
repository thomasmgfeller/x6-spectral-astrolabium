"""Independent bivariate algebra, direct PMFs, source transport and tree audit.
SPDX-License-Identifier: Apache-2.0
"""
from ps_run import *
from decimal import Decimal,localcontext
from pto_audit import decimal_cdf
from ot_audit import decimal_difference,slice_cover
from pf_audit import check_event

def independent_q(b,i,j,box):
    # Compute the range from fixed time/y and extrema of the spatial distance.
    a,d,e,f=box;zi,zj=b['boost'][i],b['boost'][j]
    displacement={15:(a,d),17:(e,f)}
    li,ui=displacement.get(i,(F(0),F(0)));lj,uj=displacement.get(j,(F(0),F(0)))
    left=zj[1]-zi[1]+lj-ui;right=zj[1]-zi[1]+uj-li
    square_min=F(0) if left<=0<=right else min(left*left,right*right)
    square_max=max(left*left,right*right);constant=(zj[0]-zi[0])**2-(zj[2]-zi[2])**2
    return constant-square_max,constant-square_min

def box_for_path(path,c):
    parts=list(map(int,path.split('/')));n=c['grid_per_axis'];lo,hi=map(F,c['domain']);i,j=divmod(parts[0],n)
    assert 0<=i<n and 0<=j<n
    a,d=lo+(hi-lo)*i/n,lo+(hi-lo)*(i+1)/n;e,f=lo+(hi-lo)*j/n,lo+(hi-lo)*(j+1)/n
    for k in parts[1:]:
        assert 0<=k<4;u=(a+d)/2;v=(e+f)/2
        if k//2:a=u
        else:d=u
        if k%2:e=v
        else:f=v
    return [a,d,e,f]

def tree(archive,c):
    rows={r['path']:r for r in archive['cells']};assert len(rows)==len(archive['cells'])
    n=c['grid_per_axis'];active={str(i):rows[str(i)] for i in range(n*n)};seen=set(active)
    assert len(archive['splits'])<=c['refinement_rounds']
    for level in archive['splits']:
        expected=sorted((r for r in active.values() if r['status']=='HOLD'),key=lambda r:(-area(r),tuple(map(int,r['path'].split('/')))))[:c['maximum_parents_per_round']]
        assert level==[r['path'] for r in expected]
        for path in level:
            old=active.pop(path);assert old['status']=='HOLD'
            for i in range(4):
                child=path+'/'+str(i);assert child not in seen;active[child]=rows[child];seen.add(child)
    assert seen==set(rows)
    assert len(archive['splits'])==c['refinement_rounds'] or not any(r['status']=='HOLD' for r in active.values())
    for path,r in rows.items():assert list(map(F,r['box']))==box_for_path(path,c)
    for stage,maximum in (('marginal',c['maximum_marginal_cells']),('overlap',c['maximum_overlap_cells'])):
        wanted=sorted((r for r in active.values() if r['status']=='HOLD'),key=priority)[:maximum]
        assert [r['path'] for r in archive[stage]]==[r['path'] for r in wanted]
        for r in archive[stage]:assert r['box']==active[r['path']]['box'];active[r['path']]=r
    return list(active.values())

def audit():
    frozen();c=read(HERE/'contract.json');ar=read(HERE/'certificates.json.gz');summary=read(HERE/'summary.json');b=setup(c);counts=Counter();seen_pmf=set();seen_laws=set()
    final=tree(ar,c);assert len(final)==summary['terminal_cells']
    for cut in (0,len(ar['cells'])-1):
        broken=dict(ar,cells=[r for i,r in enumerate(ar['cells']) if i!=cut])
        try:tree(broken,c)
        except (AssertionError,KeyError):counts['missing_rectangle_controls']+=1
        else:raise AssertionError('hole accepted')
    assert ar['strips']==strips(b) and len(ar['strips'])==145
    # Independent source lookup and projection geometry, rather than reuse of
    # the inherited gap decisions or independence of all observed counts.
    old=read(HERE.parent/'continuous_energy/cells.json.gz');oldmap={(r['ray'],r['path']):r for r in old['cells']}
    for s in ar['strips']:
        node=s['node'];other=17 if node==15 else 15
        if s['source']=='continuous_energy':
            r=oldmap[(s['ray'],s['path'])];assert r['status']=='LAW_EXCLUDED' and s['tv_lower']==r['law']['tv_lower']
            assert old['rays'][r['ray']][0:2]==[node,1]
        assert all(other not in pair and all(n==node or n<5 for n in pair) for pair in s['pairs'])
        for pair in s['pairs']:
            for fixed in map(F,(s['lo'],s['hi'])):
                zz1=moved(b,fixed,F(-1,10)) if node==15 else moved(b,F(-1,10),fixed)
                zz2=moved(b,fixed,F(1,10)) if node==15 else moved(b,F(1,10),fixed)
                assert interval(zz1,*pair)==interval(zz2,*pair);counts['transport_geometry_identities']+=1
    def direct_weights(u,v,record=None):
        z=moved(b,u,v);truth=exact_weights(z,F(b['w']['scale']))
        A=[[pval(p,u,v) for p in row] for row in b['A']];rhs=[pval(p,u,v) for p in b['rhs']]
        eta=matrix_vector(inv(A),rhs);delta=[sum(pval(p,u,v)*a for p,a in zip(row,eta))/F(b['w']['scale'])**2 for row in b['W']]
        assert all(w+d==t for w,d,t in zip(b['weights'],delta,truth));counts['exact_direct_nine_moment_comparisons']+=1
        if record:
            assert all(F(a)<=t-w<=F(d) for (a,d),w,t in zip(record['weight_change_bounds'],b['weights'],truth))
            with localcontext() as ctx:
                ctx.prec=100
                def dec(f):return Decimal(f.numerator)/Decimal(f.denominator)
                gap=2*sum(dec(t-w)**2 for t,w in zip(truth,b['weights'])).sqrt()/(sum(dec(t)**2 for t in truth).sqrt()+sum(dec(w)**2 for w in b['weights']).sqrt())
                assert gap<=Decimal(record['gap_upper']);counts['sample_gap_enclosure_checks']+=1
    # Mixed two-variable algebra controls include both axes, diagonals and off-diagonals.
    for u,v in ((F(0),F(0)),(F(1,100),F(-1,100)),(F(-1,100),F(1,50)),(F(1,10),F(0)),(F(0),F(-1,10)),(F(-1,10),F(1,10)),(F(1,10),F(1,10))):direct_weights(u,v)
    cross=qrange(b,15,17,[F(1,100)]*2+[F(1,50)]*2)[0]-interval(b['z'],15,17)
    one=qrange(b,15,17,[F(1,100)]*2+[F(0)]*2)[0]-interval(b['z'],15,17)
    two=qrange(b,15,17,[F(0)]*2+[F(1,50)]*2)[0]-interval(b['z'],15,17)
    assert cross-one-two==2*F(1,100)*F(1,50)!=0;counts['mixed_term_negative_controls']+=1
    def geometry(box,v):
        i,j=b['nodes'];k=v['anchor'];sgn=v['time_sign'];tip=v['tip'];delay=F(v['delay_upper']);duration=F(v['duration']);qsub=F(v['common_q_lower']);dt=abs(b['boost'][i][0]-b['boost'][j][0])
        qmin=independent_q(b,i,j,box)[0];assert F(v['pair_q_range'][0])==qmin
        assert delay>=0 and (dt+delay)**2>=dt*dt-qmin
        assert qsub==independent_q(b,tip,k,box)[0]-2*duration*delay+delay*delay
        mus=[tuple(map(F,m)) for m in v['count_mean_intervals']];common=F(v['common_mean_lower'])
        assert mus==[mean_bounds(b,independent_q(b,node,k,box)) for node in (i,j)]
        assert F(v['variance_upper'])==mus[0][1]+mus[1][1]-2*common>=0
        assert list(map(F,v['mean']))==[mus[0][0]-mus[1][1],mus[0][1]-mus[1][0]]
        a,d,e,f=box
        for u,vv in ((a,e),(a,f),(d,e),(d,f),((a+d)/2,(e+f)/2)):
            zz=boosted(moved(b,u,vv));virtual=zz[tip].copy();virtual[0]+=sgn*delay
            for n in (i,j):
                dt1,dx,dy=[x-y for x,y in zip(virtual,zz[n])];assert sgn*dt1>=0 and dt1*dt1-dx*dx-dy*dy>=0
            if common:
                assert delay<duration and qsub>0;dt1,dx,dy=[x-y for x,y in zip(zz[k],virtual)]
                assert sgn*dt1>0 and dt1*dt1-dx*dx-dy*dy>=qsub
            counts['virtual_subset_point_checks']+=1
        counts['whole_rectangle_subset_checks']+=1
    # Check every geometric archive record, including refined parents.
    detailed=0
    for r in ar['cells']:
        box=list(map(F,r['box']));a,d,e,f=box
        for pair in ((15,17),(15,1),(15,2),(17,1),(17,2)):
            assert qrange(b,*pair,box)==independent_q(b,*pair,box);counts['independent_quadratic_rectangle_ranges']+=1
        if r['status']=='ORDER_EXCLUDED':
            o=r['order'];q=interval(b['z'],*o['pair']);lo,hi=independent_q(b,*o['pair'],box)
            assert o['base_q']==str(q) and o['range']==list(map(str,(lo,hi)))
            assert (q>0 and hi<=0) or (q<0 and lo>=0)
        elif r['status']=='TRANSFERRED_LAW_EXCLUDED':
            t=r['transfer'];lo,hi=box[:2] if t['node']==15 else box[2:];end=lo
            for index in t['strips']:
                s=ar['strips'][index];assert s['node']==t['node'] and F(s['lo'])<=end<F(s['hi']);end=F(s['hi'])
            assert end>=hi and F(t['tv_lower'])>F(1,4)
        if 'operator' in r and 'gap_upper' in r['operator']:
            record=r['operator'];assert F(record['neumann_norm_upper'])<1
            direct_weights((a+d)/2,(e+f)/2,record)
            if detailed<24:
                for u,v in ((a,e),(a,f),(d,e),(d,f)):direct_weights(u,v,record)
                detailed+=1
            if r['status']=='GAP_EXCLUDED':assert F(record['gap_upper'])<=F(1,5)
        if r['status']=='DIFFERENCE_LAW_EXCLUDED':
            law=r['law'];alt=law['statistics'];geometry(box,alt);check_event(b['base_statistics'][law['anchor']],alt,law['event']);assert F(law['tv_lower'])>F(1,4)
        elif r['status']=='MARGINAL_LAW_EXCLUDED':
            law=r['law'];index=law['index'];mu=mean_bounds(b,independent_q(b,*b['ends'][index],box))
            assert law['moved']==list(map(str,mu)) and law['base']==list(map(str,b['basemeans'][index]))
            assert F(1,4)<F(law['tv_lower'])<=lower_bound(b['basemeans'][index],mu)[1]
    for r in ar['marginal']:
        expected=marginal_candidates(b,list(map(F,r['box'])))[:c['maximum_marginal_events_per_cell']]
        assert 1<=len(r['attempts'])<=len(expected)
        for a,e in zip(r['attempts'],expected):
            assert a['index']==e['index']
            if 'reason' in a:assert max(e['base']+e['moved'])>c['poisson']['maximum_mean'];continue
            assert a['score']==str(e['score']) and a['base']==list(map(str,e['base'])) and a['moved']==list(map(str,e['moved']))
            cert=a['certificate'];ordered=sorted((e['base'],e['moved']),key=lambda x:x[0]);wanted=[*ordered[0],*ordered[1]]
            assert len(cert['endpoint_cdf_records'])==4
            for rec,mu in zip(cert['endpoint_cdf_records'],wanted):
                assert F(rec['mean'])==mu;truth=decimal_cdf(mu,cert['threshold'])
                assert Decimal(rec['cdf'][0])<=truth<=Decimal(rec['cdf'][1]);counts['independent_100_digit_marginal_PMF_checks']+=1
                assert rec['omitted_weight_upper_grid_units']>0
            p,q,t,u=[tuple(map(F,v['cdf'])) for v in cert['endpoint_cdf_records']]
            assert F(cert['full_law_tv_lower'])<=max(F(0),q[0]-t[1])+F(2,10**60)
        if r['status']=='MARGINAL_TAIL_EXCLUDED':assert F(r['attempts'][-1]['certificate']['full_law_tv_lower'])>F(1,4)
        else:assert r['status']=='HOLD' and len(r['attempts'])==len(expected) and all(F(a.get('certificate',{}).get('full_law_tv_lower','0'))<=F(1,4) for a in r['attempts'])
    def law(stats,k,cert):
        signature=json.dumps([stats,k,cert],sort_keys=True)
        if signature in seen_laws:return
        seen_laws.add(signature)
        if cert['status']!='ENCLOSED':assert cert['probability']==['0','1'];counts['budget_hold_laws']+=1;return
        a,b0=[tuple(map(F,x)) for x in stats['count_mean_intervals']];lo=F(stats['common_mean_lower']);hi=min(a[1],b0[1]);ss=cert['slices']
        assert cert['threshold']==k and cert['overlap_range']==list(map(str,(lo,hi))) and len(ss)==c['overlap']['overlap_slices'];slice_cover(ss,lo,hi)
        for j,s in enumerate(ss):
            l=lo+(hi-lo)*j/len(ss);u=lo+(hi-lo)*(j+1)/len(ss);plus=(max(F(0),a[0]-u),a[1]-l);minus=(max(F(0),b0[0]-u),b0[1]-l)
            assert s['overlap']==list(map(str,(l,u))) and s['plus']==list(map(str,plus)) and s['minus']==list(map(str,minus))
            for rec,(x,y) in zip(s['records'],((minus[0],plus[1]),(minus[1],plus[0]))):
                assert F(rec['x_mean'])==x and F(rec['y_mean'])==y;key=(str(x),str(y),k)
                if key not in seen_pmf:
                    truth=decimal_difference(x,y,k);assert Decimal(rec['probability'][0])<=truth<=Decimal(rec['probability'][1]);seen_pmf.add(key);counts['independent_110_digit_difference_PMF_checks']+=1
                assert F(rec['numerical_width_upper'])<=F(c['overlap']['probability']['numerical_event_width_target'])+F(1,10**75)
            assert F(s['probability'][0])<=F(s['records'][0]['probability'][0]) and F(s['probability'][1])>=F(s['records'][1]['probability'][1]);counts['exclusive_rate_rectangles']+=1
        assert list(map(F,cert['probability']))==[min(F(s['probability'][0]) for s in ss),max(F(s['probability'][1]) for s in ss)]
    for r in ar['overlap']:
        choices=overlap_candidates(b,list(map(F,r['box'])))
        if 'reason' in r:assert not choices and r['status']=='HOLD';continue
        e=choices[0];assert all(r[k]==e[k] for k in ('anchor','side','threshold')) and r['score']==str(e['score'])
        assert r['base_statistics']==e['base'] and r['moved_statistics']==e['moved']
        geometry([F(0)]*4,e['base']);geometry(list(map(F,r['box'])),e['moved'])
        law(e['base'],e['threshold'],r['base_law']);law(e['moved'],e['threshold'],r['moved_law'])
        p,q=[tuple(map(F,r[k]['probability'])) for k in ('base_law','moved_law')];tv=max(F(0),p[0]-q[1],q[0]-p[1]);assert r['tv_lower']==outward(tv)[0]
        assert (r['status']=='OVERLAP_TAIL_EXCLUDED')==(tv>F(1,4));print(json.dumps(dict(overlap_audited=r['path'],pmf_checks=len(seen_pmf))),flush=True)
    areas=Counter();states=Counter(r['status'] for r in final)
    for r in final:areas[r['status']]+=area(r)
    total=F(1,25);held=areas['HOLD'];assert sum(areas.values())==total
    assert states==summary['states'] and {k:str(v) for k,v in areas.items()}==summary['areas']
    assert str(held)==summary['hold_area'] and str(1-held/total)==summary['excluded_area_fraction']
    assert summary['unresolved_cells']==[dict(path=r['path'],box=r['box']) for r in final_cells(ar) if r['status']=='HOLD']
    counts['complete_square_covers']=1;counts['terminal_rectangles']=len(final);counts['source_strips']=len(ar['strips'])
    return dict(status='PASS',**dict(counts),source_tree=c['source_tree'],hold_cells_preserved=states.get('HOLD',0),parameter_area_is_not_probability=True,
        scope='Exact uniform rectangle bounds and source-event transport constitute the proof; direct point solves and Decimal PMFs independently audit implementations, not continuous coverage.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result),flush=True)
