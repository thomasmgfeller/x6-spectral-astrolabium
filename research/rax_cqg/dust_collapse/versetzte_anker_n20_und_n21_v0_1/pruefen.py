"""Reproduce the anchor census and finite order and interval certificates offline."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
from randdaten import ROOT,collect
from ordnungen import enumerate_extensions,coefficients,two_station_register
from auslese import screen,affine,target
from freie_felder import COLLAR,validate_dust
from empfang import classify_receiver
from innenzweig import classify14
from intervall import I
from zweipunkt import nearest_refinement,screen_native_pasts
from kontrollen import action_checks,arithmetic


def freeze_screen(order,records,Y,W):
    groups,passed,uncertain=screen(records,order,Y,W)
    assert not uncertain and len(passed)==404 and len(groups)==7
    feasible={(p,f) for p,f,_ in passed}
    return feasible,[{'future':list(f),'count':n,'clock_residual':r.endpoints()}
                     for f,(n,r) in sorted(groups.items())]


def classify(order,records,Y,W,windows):
    result=[]
    totals=Counter()
    for p,f,markers in records:
        row={'past':sorted(p),'future':sorted(f),'material_anchor_pairs':markers}
        if f<=set(COLLAR):
            residual=affine(coefficients(order,f),Y,W,target(Y))
            assert not residual.haszero()
            row.update(reason='pure_collar',Gz=residual.endpoints())
        else:
            dust=validate_dust(order,p,f,Y,W,depth=4)
            row['dust_checks']=dict(dust)
            if not dust['open']:
                row['reason']='dust_branch_or_time'
            else:
                assert f-set(COLLAR) in ({18},{17,18}) and set(markers)=={16}
                check=classify_receiver(order,p,f,Y,W,windows,max_depth=15)
                assert not check['terminal'].get('open'),(sorted(p),sorted(f),check)
                row.update(reason='receiver_branch',receiver_checks=check['terminal'])
        totals[row['reason']]+=1
        result.append(row)
    return result,dict(totals)


def known_control():
    # Positive control for the isolated vacuum equation: all old fields clamped,
    # a new free empty event incomparable with old material event 1.
    o={(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)}
    c=coefficients(o,{2,3})
    assert c=={2:1,3:-9}
    Y={2:I.enclose(1),3:I.enclose(2)}
    W={2:I.enclose(F(3,5)),3:I.enclose(F(1,30))}
    # Exact root at zero, with opposing certified signs on either side.
    for t,sign in [(F(-1,10),1),(F(0),0),(F(1,10),-1)]:
        direct=F(3,5)*(1-t)-9*F(1,30)*(2-t)
        assert direct==-F(3,10)*t
        r=affine(c,Y,W,I.enclose(t))
        assert (r.l>0 if sign==1 else r.h<0 if sign==-1 else r.haszero())
    return 'Known root recovered with strict signs at +/-1/10.'


def study():
    if not __debug__:raise RuntimeError('Python ohne -O verwenden.')
    source=json.loads((ROOT/'Quellen.json').read_bytes())
    for name,v in source['files'].items():
        if sha256((ROOT/name).read_bytes()).hexdigest()!=v['sha256']:raise ValueError('Quelle '+name)
    order,times,weights,windows,cells,routes=collect()
    assert len(order)==129 and cells==168
    total,records=enumerate_extensions(order)
    assert total==1017 and len(records)==570
    feasible,frozen=freeze_screen(order,records,times,weights)
    by={i:times[i] for i in COLLAR};bw={i:weights[i] for i in COLLAR}
    assert all((by[i].l,by[i].h)==(I.enclose(t).l,I.enclose(t).h) for i,t in ((0,-5),(1,-4),(2,-3),(7,2)))
    rows,summary=classify(order,records,by,bw,windows)
    for row in rows:
        row['parent_time_compatible']=(frozenset(row['past']),frozenset(row['future'])) in feasible
    assert summary=={'pure_collar':400,'dust_branch_or_time':161,'receiver_branch':9}
    independent_14=classify14(order,records,by,bw,depth=16)
    assert len(independent_14)==17 and all(row['unresolved']==0 for row in independent_14)
    wide_y=dict(by);wide_w=dict(bw)
    for i in (7,8,9,10):wide_w[i]+=I.enclose(F(-1,10**6),F(1,10**6))
    for i in (8,9,10):wide_y[i]+=I.enclose(F(-1,10**4),F(1,10**4))
    _,wide=classify(order,records,wide_y,wide_w,windows)
    assert sum(wide.values())==570
    n21=nearest_refinement(order,times)
    for r in n21['variants']:
        lo,hi=map(F,r['D19'])
        assert lo>(F('12.88') if 13 in r['past_n'] else F('45.53')) and r['roots_overlapping_target']==0
    native=screen_native_pasts(order,by)
    assert len(native)==18 and all(row['reason'] in ('past_outside_window','no_target_root','residual_sign') for row in native)
    register=two_station_register(order)
    assert register=={'common_anchors_total':406142,'after_boundary_time_order':393264,
                      'after_positive_past_test':227676,'after_pure_collar_future_test':42716}
    inp=json.loads((ROOT/'basis/P3.json').read_text())
    assert len(inp)==60 and all(r['execution']=='NOT_RUN' for r in inp)
    selected={(r['checkpoint_context']['M'],r['checkpoint_context']['density_ratio']) for r in inp if r['checkpoint_context']['x']=='1/2' and r['checkpoint_context']['M'] in ('1/4','4')}
    assert len(selected)==8
    return {'source_commit':source['commit'],'reference_cases':cells,'labelled_one_point_orders':total,
            'orders_with_material_marker_and_two_anchors':len(records),'admissible_filters':len({f for p,f,a in records}),
            'fixed_field_time_compatible':len(feasible),'fixed_field_groups':frozen,
            'free_field_summary':summary,'independent_14_checks':independent_14,'free_field_certificates':rows,'wider_collar_summary':wide,
            'native_enclosures':{k:{'clock':v.endpoints(),'weight':weights[k].endpoints()} for k,v in times.items()},
            'nearest_two_point_refinement':n21,'device_free_native_pasts':native,'two_point_filter_register':register,'exact_variations':action_checks(order,records,routes),
            'exact_interval_control_pairs':arithmetic(),'positive_control':known_control(),
            'P3':{'checkpoints_NOT_RUN':60,'unmeasured_two_mass_radius_cells':len(selected),'physical_radius':None}}

def raw(v):
    return (json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()

if __name__=='__main__':
    for fn in ['SHA256SUMS','Pruefplan.sha256','Ergaenzung.sha256','Ergaenzung_Vergangenheiten.sha256']:
        for l in (ROOT/fn).read_text().splitlines():
            h,path=l.split('  ',1)
            if sha256((ROOT/path).read_bytes()).hexdigest()!=h:raise ValueError('Hash '+path)
    if raw(study())!=(ROOT/'Ergebnisse.json').read_bytes():raise ValueError('Ergebnisabweichung')
    print('PASS · 1 017 N20-Erweiterungen · 570 mit Ankern geprüft · 4 N21-Anbindungen an 12 und 14 ausgeschlossen.')
    print('Physisches P3-Register: 60 NOT_RUN.')
