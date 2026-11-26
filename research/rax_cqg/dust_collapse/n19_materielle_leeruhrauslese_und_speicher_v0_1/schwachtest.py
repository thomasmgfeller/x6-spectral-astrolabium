"""Linear link-current coupling without a tuning subtraction in its defining action."""
from fractions import Fraction as F
from itertools import product
from auslesetest import LOAD,certify,receiver_read,stored_read,abs_upper
from speichermodell import coupled


def run(previous,early):
    from proben import samples
    from quelle import box,hull
    from uhrauslese import LABELS
    k=F(1,10**11)
    max_load=k*LOAD
    p=hull(-max_load,max_load)
    delta=box(-k)
    rows=[]
    corners=0
    for name,y,w in samples(previous,early)[0]:
        for j in LABELS:
            state=coupled(y,w,0,j,p,p,pt=p,mismatch=delta,stiffness=k)
            # The per-inertia load p/k has exactly the limit used by certify.
            bounds=certify(state,j,delta,max_load/k)
            rows.append({'background':name,'source':str(j),'bounds':bounds})
            for a,b,c in product((-max_load,max_load),repeat=3):
                point=coupled(y,w,0,j,box(a),box(b),pt=box(c),mismatch=delta,stiffness=k)
                assert receiver_read(point['y'][18],*point['read'])==j
                assert stored_read(point['y'][7],point['stamp'],*point['stored'])==j
                corners+=1
        if name=='reference':
            control=coupled(y,w,0,0,box(LOAD),box(0),pt=0,mismatch=delta,stiffness=k)
            t=control['y'][18]
            u_displacement=t-control['read'][0]-y[15]
            assert u_displacement.hi<0 and abs_upper(u_displacement)>F(1,100)
            misidentified=receiver_read(t,*control['read'])
            assert misidentified!=0
            overload={'physical_model_impulse':str(LOAD),'actual_source':'0',
                      'decoded_as':str(misidentified),'early_clock_bias':u_displacement.data()}
    return {'kinetic_coefficient':str(k),'mismatch_equals_minus_kinetic_coefficient':True,
            'per_channel_model_impulse_bound':str(max_load),'load_per_kinetic_coefficient':str(max_load/k),
            'families':rows,'exact_corner_classifications_per_site':corners,'overload':overload,
            'min_positive_margins':{i:str(min(F(v['bounds'][i]['unique_label_margin']) for v in rows))
                                    for i in ('18','7')}}
