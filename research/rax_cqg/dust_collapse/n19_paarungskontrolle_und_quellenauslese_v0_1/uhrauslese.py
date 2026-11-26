"""Decode one of three calibrated sources from the two empty clocks and the receiver clock."""
from fractions import Fraction as F
from itertools import product
import json

J=F(1,10**6)
LABELS=(-J,F(0),J)
EPS=F(1,10**11)


def sender(u,label):
    return (u*u-6-label)/(2*(u+3))


def residual(u,h,t,label):
    s=sender(u,label)
    return 19-8*(t+4)*(t+4)+16*(t+3)*(t+3)-9*(t-u)*(t-u)+(t-s)*(t-s)+(t-h)*(t-h)


def upper_abs(x):
    return max(abs(x.lo),abs(x.hi))


def lower_abs(x):
    return 0 if x.contains_zero() else min(abs(x.lo),abs(x.hi))


def decode(u,h,t):
    values={label:residual(u,h,t,label) for label in LABELS}
    winner=[k for k,v in values.items() if all(upper_abs(v)<lower_abs(w) for j,w in values.items() if j!=k)]
    assert len(winner)==1
    return winner[0]


def uniform():
    from quelle import DATA,box,hull,SCALE
    from fenster import endpoints
    e,windows=DATA[-2:]
    s0=hull(*endpoints(windows[0],e))
    t0=hull(*endpoints(windows[1],e))
    u0=s0-(s0*s0+6*s0+6).sqrt()
    h0=t0-(8*(t0+4)*(t0+4)-16*(t0+3)*(t0+3)+9*(t0-u0)*(t0-u0)
             -(t0-s0)*(t0-s0)-19).sqrt()
    error=hull(-EPS,EPS)
    u,h,t=u0+error,h0+error,t0+error
    # The true pulsed receiver clock is required to lie in its registered window.
    s_coarse=(u*u-6-hull(-J,J))/(2*(u+3))
    slope=F(upper_abs((u-s_coarse)/(u+3)),SCALE)
    dmax=F(upper_abs(box(J)/(2*(u0+3))),SCALE)
    margin=dmax+slope*EPS
    s=s0+hull(-margin,margin)
    ds=(u-s)/(u+3)
    dt=2*(t+16+9*u-s-h)
    du=18*(t-u)-2*(t-s)*ds
    dh=-2*(t-h)
    lipschitz=F(sum(map(upper_abs,(dt,du,dh))),SCALE)
    sep=F((box(J)/(2*(u+3))*(2*(t-s))).lo,SCALE)
    assert (u+3).lo>0 and (t-s).lo>0 and 2*lipschitz*EPS<sep
    return {'source_labels':list(map(str,LABELS)),'collar_e':e.data(),'clock_error_each':str(EPS),
            'sender_window_clock':s0.data(),'receiver_window_clock':t0.data(),'u_enclosure':u.data(),
            'h_enclosure':h.data(),'min_candidate_residual_separation':str(sep),
            'sum_of_absolute_derivative_bounds':str(lipschitz),'true_residual_max':str(lipschitz*EPS)}


def run(previous,early):
    from gemischt import ORDER
    from quelle import box,SCALE
    from felder import pulses
    from proben import samples
    theorem=uniform()
    sites=[i for i in range(19) if all(i==j or (j,i) in ORDER for j in (15,17,18))]
    assert sorted(i for i in sites if not any((j,i) in ORDER for j in sites))==[18]
    assert (15,18) in ORDER and (17,18) in ORDER
    fixtures,_=samples(previous,early)
    records=[]
    for name,y,w in fixtures:
        arms=pulses(y,w)
        clocks=[arms[0][1],y,arms[1][1]]
        for expected,yy in zip(LABELS,clocks):
            u,h,t=(yy[i] for i in (15,17,18))
            assert decode(u,h,t)==expected
            for a,b,c in product((-EPS,EPS),repeat=3):
                assert decode(u+a,h+b,t+c)==expected
            # Invert the passive receiver equation directly. Chronology fixes t-s>0.
            rad=-19+8*(t+4)*(t+4)-16*(t+3)*(t+3)+9*(t-u)*(t-u)-(t-h)*(t-h)
            inferred_s=t-rad.sqrt()
            inferred_j=u*u-6-2*(u+3)*inferred_s
            assert (inferred_j-box(expected)).contains_zero()
            assert not any((inferred_j-box(other)).contains_zero() for other in LABELS if other!=expected)
            records.append({'case':name,'label':str(expected),'inverse_J':inferred_j.data(),
                            'clock_displacement':(t-y[18]).data(),'correct_at_eight_corners':True})
        if name=='reference':
            tplus=clocks[-1][18]
            eps_coarse=F(3,10**10)
            assert (tplus-y[18]).lo>0 and (tplus-y[18]).hi<2*eps_coarse*SCALE
            midpoint=(tplus+y[18])/2
            assert all(upper_abs(midpoint-v)<eps_coarse*SCALE for v in (tplus,y[18]))
            assert all(clocks[-1][i] is y[i] for i in (15,17))
            overlap={'labels':['0',str(J)],'error_only_at_receiver':str(eps_coarse),
                     'null_to_positive_distance':(tplus-y[18]).data(),'common_reading_midpoint':midpoint.data()}
    return {'uniform':theorem,'first_joint_site':18,'point_classifications':len(records),
            'noise_corner_classifications':8*len(records),'overlapping_observations':overlap,'records':records}


if __name__=='__main__':
    from vorgaenger import inputs
    with inputs() as args:
        print(json.dumps(run(*args),indent=2,sort_keys=True))
