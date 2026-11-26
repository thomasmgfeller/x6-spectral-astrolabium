"""Interval certificates for receiver and stored records, across independent read and load errors."""
from fractions import Fraction as F
from itertools import product
from speichermodell import coupled,square

LOAD=F(1,10**14)
READ_ERROR=F(1,10**12)
MISMATCH=F(1,10**11)


def abs_upper(v):
    from quelle import SCALE
    return F(max(abs(v.lo),abs(v.hi)),SCALE)


def receiver_read(t,xu,xh):
    from uhrauslese import decode
    return decode(t-xu,t-xh,t)


def stored_read(local_clock,stamp,zu,zh):
    return receiver_read(local_clock-stamp,zu,zh)


def certify(state,source,mismatch,load_per_inertia=LOAD):
    from quelle import hull,SCALE,box
    from uhrauslese import sender,J
    y,w=state['y'],state['w']
    u,h,s,t=(y[i] for i in (15,17,16,18))
    inv_z,inv_r,inv_7=(F(SCALE,w[j].lo) for j in (16,18,7))
    at_r=(READ_ERROR,2*READ_ERROR+load_per_inertia*(inv_z+inv_r),2*READ_ERROR+load_per_inertia*inv_r)
    stamp_error=2*READ_ERROR+load_per_inertia*inv_7
    at_7=(stamp_error,stamp_error+READ_ERROR+load_per_inertia*(inv_z+inv_r+inv_7),
          stamp_error+READ_ERROR+load_per_inertia*(inv_r+inv_7))
    # Exact residual of the true source at the loaded, unrounded clocks.
    defect=-state['receiver_source_defect']-mismatch*(square(t-s)+square(t-h))
    defect+=state['extra']*(2*t-s-sender(u,source))
    records={}
    for site,errors in ((18,at_r),(7,at_7)):
        dt,du,dh=errors
        U,H,T=(v+hull(-e,e) for v,e in zip((u,h,t),(du,dh,dt)))
        all_s=sender(U,hull(-J,J))
        derivative=(U-all_s)/(U+3)
        Ft=2*(T+16+9*U-all_s-H)
        Fu=18*(T-U)-2*(T-all_s)*derivative
        Fh=-2*(T-H)
        worst=abs_upper(defect)+sum(abs_upper(v)*e for v,e in zip((Ft,Fu,Fh),errors))
        sep=F((box(J)/(2*(U+3))*2*(T-all_s)).lo,SCALE)
        assert (U+3).lo>0 and (T-all_s).lo>0 and 2*worst<sep
        records[str(site)]={'clock_errors_t_u_h':list(map(str,errors)),'max_true_residual':str(worst),
                            'min_pairwise_separation':str(sep),'unique_label_margin':str(sep-2*worst)}
    return records


def run(previous,early):
    from quelle import box,hull,SCALE
    from gemischt import ORDER
    from proben import samples
    from uhrauslese import LABELS
    from felder import pulses
    links=[(15,16),(16,18),(17,18),(18,7)]
    for i,j in links:
        assert (i,j) in ORDER and not any((i,k) in ORDER and (k,j) in ORDER for k in range(19))
    fixtures,_=samples(previous,early)
    assert len(fixtures)==12
    p=hull(-LOAD,LOAD)
    delta=hull(-MISMATCH,MISMATCH)
    rows=[]
    count=0
    for name,y,w in fixtures:
        arms=pulses(y,w)
        for j,reference in zip(LABELS,(arms[0][1:],(y,w),arms[1][1:])):
            # Cover every load, the common coefficient error, and every readout error in these boxes.
            state=coupled(y,w,0,j,p,p,mismatch=delta,pt=p)
            bound=certify(state,j,delta)
            free=coupled(y,w,0,j,box(0),box(0))
            assert all((free[k][i]-expected[i]).contains_zero()
                       for k,expected in zip(('y','w'),reference) for i in y)
            assert receiver_read(free['y'][18],*free['read'])==j
            assert stored_read(free['y'][7],free['stamp'],*free['stored'])==j
            for a,b,c,d in product((-1,1),repeat=4):
                point=coupled(y,w,0,j,box(a*LOAD),box(b*LOAD),mismatch=box(c*MISMATCH),pt=box(d*LOAD))
                assert receiver_read(point['y'][18],*point['read'])==j
                assert stored_read(point['y'][7],point['stamp'],*point['stored'])==j
                count+=1
            rows.append({'background':name,'source':str(j),'bounds':bound,
                         'w_z_r_7':[state['w'][i].data() for i in (16,18,7)],
                         'clock_shift_from_unloaded_z_r':[state['extra'].data(),
                            (state['y'][18]-reference[0][18]).data()]})
    assert count==576
    return {'links':links,'box_families':len(rows),'four_parameter_corners':count,
            'load_limit':str(LOAD),'gain':1,'read_error':str(READ_ERROR),'mismatch_limit':str(MISMATCH),
            'worst_per_site':{i:{'max_true_residual':str(max(F(v['bounds'][i]['max_true_residual']) for v in rows)),
                                 'min_pairwise_separation':str(min(F(v['bounds'][i]['min_pairwise_separation']) for v in rows)),
                                 'max_clock_error':str(max(F(x) for v in rows for x in v['bounds'][i]['clock_errors_t_u_h'])),
                                 'min_unique_margin':str(min(F(v['bounds'][i]['unique_label_margin']) for v in rows))}
                              for i in ('18','7')},'families':rows}
