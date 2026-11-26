"""Uniform signed response bounds and paired source reversal on published windows."""
from fractions import Fraction as F
from itertools import product

JABS=F(1,10**6)


def parts(a,b,n):
    from quelle import hull
    return [hull(a+(b-a)*k/n,a+(b-a)*(k+1)/n) for k in range(n)]


def endpoints(window,e):
    values=[(4-v)*x+v-2 for x in window for v in map(F,e.data())]
    return min(values),max(values)


def geometry(s,t,u,max_receiver_chord):
    from quelle import box,SCALE
    h=t-(8*(t+4)*(t+4)-16*(t+3)*(t+3)+9*(t-u)*(t-u)-(t-s)*(t-s)-19).sqrt()
    mz=-(u+3)
    mr=-8*(t+4)+16*(t+3)-9*(t-u)+(t-s)+(t-h)
    D=box(JABS)/(2*(u+3))
    gap=t-s
    assert (gap*2-D).lo>0 and D.lo>0 and mr.hi<0 and mz.hi<0
    pairs=[]
    for d in (D,-D):                       # Negative, then positive, density source.
        B=mr-d
        C=d*(d-2*gap)
        divisor=-B+(B*B-C).sqrt()
        q=C/divisor
        assert B.hi<0 and divisor.lo>max_receiver_chord*SCALE
        az=d*(1+(s+d-u)/(s-h))
        ar=q*(s+d-u)*(s+d-h)/(mz*(t+q-h))
        pairs.append((d,q,az,ar))
    _,qn,an,bn=pairs[0]
    _,qp,ap,bp=pairs[1]
    assert min(an.lo,bn.lo,qp.lo)>0 and max(ap.hi,bp.hi,qn.hi)<0
    # Ratios of correlated factors are evaluated as 1 + their small difference.
    rz=1-2*D/(2*s-h-u+D)
    Hp=-2*(mr+D)-qp
    rr=(1+2*D/(2*gap-D))*(1+(4*D+qp-qn)/Hp)
    rr*= (1-2*D/(s-u+D))*(1-2*D/(s-h+D))*(1+(qn-qp)/(t-h+qp))
    assert (rz-(-ap/an)).contains_zero() and (rr-(-bp/bn)).contains_zero()
    return ((an,bn),(-ap,-bp)),rz,rr


def report_abs(limits):
    from quelle import SCALE
    a,b=(F(v,SCALE) for v in (limits.lo,limits.hi))
    assert 0<a<=b
    return {'magnitude':limits.data(),'prediction':str(2*a*b/(a+b)),
            'guaranteed_relative_error':str((b-a)/(b+a))}


def accumulate(value,previous):
    return value if previous is None else previous.union(value)


def run(early,amplitudes):
    from quelle import DATA,box,hull
    from zustand import nominal
    y,w=nominal(early)[1]
    e,windows=DATA[-2:]
    schart=endpoints(windows[0],e)
    tchart=endpoints(windows[1],e)
    width=tchart[1]-tchart[0]
    refK=w[16]*(y[16]-y[15])
    unit=F(1,8)
    possible_wr=hull(0,1)
    results={}
    sender_coefficients=[None,None]
    receiver_coefficients=[None,None]
    # Nominal calculation retaining only K0 and the old pre-set clock.
    general_z=general_r=None
    for name,K,domains in [
        ('nominal_only_K0',refK,[(y[16],t,y[15]) for t in parts(*endpoints(windows[1],box(F(1,6))),128)]),
        ('whole_windows_prefix_setpoint',box(unit),None)]:
        if domains is None:
            domains=[]
            for s in parts(*schart,24):
                u=s-(s*s+6*s+6).sqrt()
                for t in parts(*tchart,24):
                    domains.append((s,t,u))
        limits=[None,None]
        for s,t,u in domains:
            coeffs,rz,rr=geometry(s,t,u,width)
            if name=='whole_windows_prefix_setpoint':
                general_z=accumulate(rz,general_z)
                general_r=accumulate(rr,general_r)
            for i,(az,ar) in enumerate(coeffs):
                if name=='whole_windows_prefix_setpoint':
                    sender_coefficients[i]=accumulate(az/(s-u),sender_coefficients[i])
                    receiver_coefficients[i]=accumulate(ar,receiver_coefficients[i])
                value=az*K/(s-u)+ar*possible_wr
                limits[i]=accumulate(value,limits[i])
        results[name]=[report_abs(v) for v in limits]
    wide=general_z.union(general_r)
    # Complete on-shell pulse checks against the prediction including midpoint examples.
    for sample in amplitudes['scaling']+amplitudes['same_G0_G1']['members']:
        sampleQ=hull(*sample['Q'])
        assert wide.lo<=sampleQ.lo<=sampleQ.hi<=wide.hi
    for case,index in [('nominal_only_K0',0),('whole_windows_prefix_setpoint',3)]:
        for arm,exact in zip(results[case],amplitudes['scaling'][index]['delta_K']):
            mag=hull(*exact)
            if mag.hi<0: mag=-mag
            dom=hull(*arm['magnitude'])
            assert dom.lo<=mag.lo<=mag.hi<=dom.hi
    from quelle import SCALE
    p=F(1,20)
    tolerances=[]
    for ac,bc in zip(sender_coefficients,receiver_coefficients):
        lo,hi=F(ac.lo,SCALE)*unit,F(ac.hi,SCALE)*unit
        maxr=F(bc.hi,SCALE)
        eps=((1+p)*lo-(1-p)*(hi+maxr))/((1+p)*lo+(1-p)*hi)
        assert 0<eps<1
        tolerances.append(eps)
    # Round down to one tenth of one percent, then propagate each error again.
    eps=F(int(1000*min(tolerances)),1000)
    tolK=hull(unit*(1-eps),unit*(1+eps))
    robust=[report_abs(ac*tolK+bc*possible_wr) for ac,bc in zip(sender_coefficients,receiver_coefficients)]
    assert all(F(entry['guaranteed_relative_error'])<=p for entry in robust)
    small,large=amplitudes['same_G0_G1']['members']
    mix=[]
    for pos,neg in ((large,small),(small,large)):
        naive=-hull(*pos['delta_K'][1])/hull(*neg['delta_K'][0])
        assert naive.hi<wide.lo or naive.lo>wide.hi
        mix.append(naive.data())
    return {'tolerance_around_early_setpoint':{'certified_threshold_each':list(map(str,tolerances)),
            'working_relative_halfwidth':str(eps),'working_K0_range':tolK.data(),'predictions':robust},
            'crossed_background_control':mix,'e':e.data(),'expanded_sender_Y_window':[str(v) for v in schart],
            'expanded_receiver_Y_window':[str(v) for v in tchart],
            'positive_weight_reversal':{'Q':wide.data(),'sender_ratio':general_z.data(),
            'receiver_ratio':general_r.data(),'grid':[24,24]},
            'absolute_given_K0':results,'source_order':['-1/1000000','1/1000000']}


if __name__=='__main__':
    import json
    from grundlage import inputs,ROOT
    with inputs() as (_,early):
        print(json.dumps(run(early,json.loads((ROOT/'Amplituden.json').read_bytes())),indent=2,sort_keys=True))
