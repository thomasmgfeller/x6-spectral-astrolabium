"""Common, source-independent canonical preparation and the readout certificate."""
from fractions import Fraction as F
from math import isqrt
from itertools import product

from staubgeraet import solve,verify
from wege import ROUTES

B=F(1,10**12)
V=F(1,10**14)
FOCUS=F(250)
READ=F(1,10**12)
STEP=2*READ


def abs_upper(v):
    from quelle import SCALE
    return F(max(abs(v.lo),abs(v.hi)),SCALE)


def sqrt_upper(n):
    scale=10**45
    floor=isqrt(n.numerator*scale*scale//n.denominator)
    result=F(floor,scale)
    return result if result*result==n else result+F(1,scale)


def pointer_radius(factor,focus,ratio,extent):
    return extent*sqrt_upper(B*B+(V*abs_upper(ratio*factor-focus))**2)


def certify(state,factors,J,mismatch,focus,ratio=1,extent=1,read_error=READ):
    from quelle import hull,box,SCALE
    from uhrauslese import sender,LABELS
    from speichermodell import square
    y=state['y'];u,h,s,t=(y[j] for j in (15,17,16,18))
    defect=state['extra']*(2*t-s-sender(u,J))-state['receiver_defect']
    defect-=mismatch*(square(t-s)+square(t-h))
    separation_step=LABELS[1]-LABELS[0]
    out={}
    for site in (18,7):
        u_error=read_error+pointer_radius(factors[0][site],focus,ratio,extent)
        h_error=read_error+pointer_radius(factors[1][site],focus,ratio,extent)
        t_error=read_error if site==18 else 2*read_error+pointer_radius(factors[2][site],focus,ratio,extent)
        # Interpolate from the true to the reported readings in their actual
        # input coordinates (t shift, material pointer shifts), not as three
        # independent reconstructed clock errors.
        T=t+hull(-t_error,t_error)
        U=u+hull(-t_error-u_error,t_error+u_error)
        H=h+hull(-t_error-h_error,t_error+h_error)
        levels=sender(U,hull(LABELS[0],LABELS[-1]))
        ds=(U-levels)/(U+3)
        Ft=2*(T+16+9*U-levels-H)
        Fu=18*(T-U)-2*(T-levels)*ds
        Fh=-2*(T-H)
        max_residual=abs_upper(defect)+abs_upper(Ft+Fu+Fh)*t_error+abs_upper(Fu)*u_error+abs_upper(Fh)*h_error
        sep=F((box(separation_step)/(2*(U+3))*2*(T-levels)).lo,SCALE)
        assert (T-levels).lo>0 and (U+3).lo>0
        out[str(site)]={'margin':str(sep-2*max_residual),'true_residual_max':str(max_residual),
                        'residual_distance_min':str(sep),
                        'pointer_error_max':str(max(pointer_radius(f[site],focus,ratio,extent) for f in factors[:2 if site==18 else 3]))}
    return out


def quantize(interval,step=STEP):
    from quelle import SCALE,hull
    def nearest(i):
        v=F(i,SCALE)/step+F(1,2)
        return (v.numerator//v.denominator)*step
    return hull(nearest(interval.lo),nearest(interval.hi))


def local_read(y,history,site,step=STEP):
    from uhrauslese import decode
    if site==18:
        t=quantize(y[18],step)
    else:
        t=quantize(y[7],step)-quantize(history[2][7],step)
    a,b=(quantize(history[i][site],step) for i in (0,1))
    return decode(t-a,t-b,t)


def test_points():
    # Four asymmetric initial conditions on each ellipse. The 64 products
    # exercise different phases and signs on the three simultaneous channels.
    return tuple(product(((F(0),F(1)),(F(0),F(-1)),(F(3,5),F(4,5)),(F(-4,5),F(3,5))),repeat=3))


def run(previous,early):
    from quelle import hull,box
    from proben import samples
    from uhrauslese import LABELS
    fixtures,_=samples(previous,early)
    assert len(fixtures)==12
    rr=hull(-V,V)
    rawq=hull(-B-FOCUS*V,B+FOCUS*V)
    rows=[];explicit=0
    points=test_points()
    for route in ROUTES:
        for k in (F(1),F(1,10**11)):
            mismatch=hull(-F(1,10**11),F(1,10**11)) if k==1 else box(-k)
            for name,y,w in fixtures:
                for J in LABELS:
                    state=solve(y,w,J,(rr,)*3,k,mismatch,route)
                    _,factors=verify(state,J,(rr,)*3,k,mismatch,route,(rawq,)*3)
                    focused=certify(state,factors,J,mismatch,FOCUS)
                    control=certify(state,factors,J,mismatch,0)
                    assert all(F(t['margin'])>0 for t in focused.values())
                    rows.append({'route':route,'k':str(k),'case':name,'J':str(J),'focused':focused,'unsheared':control,
                                 'transfer_coefficients':{str(i):[a[i].data() for a in factors] for i in (18,7)}})
                    # Full phase grid on the reference and leanest (quarter)
                    # states; all twelve states are covered above by enclosure.
                    if name in ('reference','quarter'):
                        for idx,point in enumerate(points):
                            vel=tuple(box(V*vy) for _,vy in point)
                            q=tuple(box(B*bx-FOCUS*V*vy) for bx,vy in point)
                            delta=box((1 if idx%2 else -1)*F(1,10**11)) if k==1 else mismatch
                            field=solve(y,w,J,vel,k,delta,route)
                            hist,_=verify(field,J,vel,k,delta,route,q)
                            assert local_read(field['y'],hist,18)==J and local_read(field['y'],hist,7)==J
                            explicit+=1
    def summary(key,site):
        values=[F(row[key][str(site)]['margin']) for row in rows]
        return {'positive_margins':sum(v>0 for v in values),'min_margin':str(min(values)),
                'max_pointer_radius':str(max(F(row[key][str(site)]['pointer_error_max']) for row in rows))}
    return {'families':rows,'count':len(rows),'concrete_source_trials':explicit,
            'decision_count':2*explicit,'settings':{'B':str(B),'V':str(V),'focus':str(FOCUS),'rounding_step':str(STEP)},
            'summary':{key:{str(site):summary(key,site) for site in (18,7)} for key in ('focused','unsheared')}}
