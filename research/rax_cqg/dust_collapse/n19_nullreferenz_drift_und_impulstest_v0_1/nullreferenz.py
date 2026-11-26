"""Source-blind two-site digit decoder and uniform bounds for a stored initial reading."""
from fractions import Fraction as F
from itertools import product

K0 = F(1,10**11)
V = F(1,10**14)
R = F(1,10**12)
STEP = 2*R
MESH = tuple(map(F, (0,'1/4','1/2',1,2,3,4,8)))
SITES = (18,7)
TRACKS = ('u','h','t')


def maxabs(value):
    from quelle import SCALE
    return F(max(abs(value.lo), abs(value.hi)), SCALE)


def digit(value):
    from quelle import SCALE
    if value.lo < -8*SCALE or value.hi >= 8*SCALE:
        return None
    def code(n):
        return (F(n,SCALE)/STEP + F(1,2)).__floor__()
    lo,hi = code(value.lo),code(value.hi)
    if lo != hi or not -8 <= hi*STEP < 8:
        return None
    return lo


def local_decode(site, shot, clock, end_codes, reference):
    from quelle import box
    from uhrauslese import decode
    if reference is None or reference.get('shot') != shot or site not in SITES:
        return None
    active = TRACKS[:2] if site == 18 else TRACKS
    if not isinstance(reference.get('initial'),dict) or not isinstance(end_codes,dict):
        return None
    values = [clock, *(end_codes.get(k) for k in active), *(reference['initial'].get(k) for k in active)]
    if any(type(v) is not int or not -8 <= v*STEP < 8 for v in values):
        return None
    displacement = {k:box(STEP*(end_codes[k]-reference['initial'][k])) for k in active}
    t = box(STEP*clock)
    if site == 7:
        t -= displacement['t']
    try:
        return decode(t-displacement['u'],t-displacement['h'],t)
    except AssertionError:
        return None


def split_residual(t,u,h,J,e,a,b):
    # e, a, b are errors in t, t-u, t-h. This secant form preserves their dependence.
    from uhrauslese import sender
    du=e-a
    ds=F(1,2)-(3-J)/(2*(u+3)*(u+du+3))
    gap=t-sender(u,J)
    return ((16*t+32+2*gap*(1-ds))*e + (-18*(t-u)+2*gap*ds)*a
            +2*(t-h)*b + 8*e*e-9*a*a+(e-ds*du)*(e-ds*du)+b*b)


def margin(state,A,J,delta,site,velocity_bound,offset):
    from quelle import hull,SCALE,box
    from uhrauslese import sender,LABELS
    from speichermodell import square
    y=state['y']
    t,u,h,s=(y[i] for i in (18,15,17,16))
    errors=[2*R+offset+maxabs(row[site])*velocity_bound for row in A]
    e_bound=R+(errors[2] if site==7 else 0)
    e,a,b=[hull(-z,z) for z in (e_bound,errors[0],errors[1])]
    native=state['extra']*(2*t-s-sender(u,J))-state['receiver_defect']-delta*(square(t-s)+square(t-h))
    total=maxabs(native+split_residual(t,u,h,J,e,a,b))
    uu=u+e-a
    tt=t+e
    levels=sender(uu,hull(LABELS[0],LABELS[-1]))
    assert (uu+3).lo>0 and (tt-levels).lo>0
    separation=F((box(LABELS[1]-LABELS[0])*(tt-levels)/(uu+3)).lo,SCALE)
    return separation-2*total


def digits(y,hist,q,site,initial=None):
    packet={'shot':'run','initial':{k:digit(v) for k,v in zip(TRACKS,q)}} if initial is None else initial
    return local_decode(site,'run',digit(y[site]),{k:digit(row[site]) for k,row in zip(TRACKS,hist)},packet)


def run(previous,early):
    from quelle import box,hull,SCALE
    from proben import samples
    from uhrauslese import LABELS,residual
    from staubgeraet import solve,verify
    from ensemble import local_read
    from wege import ROUTES
    fixtures,_=samples(previous,early)
    budgets=(F(0),R/4,R)
    records={(m,o):[] for m in MESH for o in budgets}
    concrete=0
    checks=0
    for t,u,h in [(F(1,2),F(-2),F(-1,5)),(F(9,13),F(1,6),F(-2,3))]:
        for J in LABELS:
            for e,a,b in product((F(-3,100),F(1,16)),repeat=3):
                exact=residual(u+e-a,h+e-b,t+e,J)-residual(u,h,t,J)
                assert exact==split_residual(t,u,h,J,e,a,b)
                checks+=1
    failures=[]
    for route,k,(name,y,w),J in product(ROUTES,(F(1),K0),fixtures,LABELS):
        delta=hull(-K0,K0) if k==1 else box(-k)
        for m in MESH:
            limit=m*K0*V/k
            vv=(hull(-limit,limit),)*3
            state=solve(y,w,J,vv,k,delta,route)
            # Absolute q cancels from every equation; broad range here tests the ADC.
            history,A=verify(state,J,vv,k,delta,route,(hull(-1,1),)*3)
            all_values=[state['y'][j] for j in SITES]+[h[j] for j in SITES for h in history]
            assert all(maxabs(z)<8-2*STEP for z in all_values)
            for offset in budgets:
                margins=[margin(state,A,J,delta,site,limit,offset) for site in SITES]
                records[m,offset].append((min(margins),str(k),route,name,str(J),[str(v) for v in margins]))
        # These offsets are deliberately different and unrelated to the common momenta.
        q=tuple(box(x) for x in (F(1),F(-2,3),F(5,11)))
        vel=tuple(box(K0*V*x/k) for x in (F(1,2),F(-1,3),F(1,4)))
        delta0=box(-K0)
        st=solve(y,w,J,vel,k,delta0,route)
        hist,_=verify(st,J,vel,k,delta0,route,q)
        for site in SITES:
            assert digits(st['y'],hist,q,site)==J
            concrete+=1
        if J==0 and name=='reference':
            for z in (-1,1):
                q=(box(z*64*R),box(0),box(0))
                st=solve(y,w,J,(box(0),)*3,k,delta0 if k==K0 else box(0),route)
                hist,_=verify(st,J,(box(0),)*3,k,delta0 if k==K0 else box(0),route,q)
                nominal=[local_read(st['y'],hist,j) for j in SITES]
                corrected=[digits(st['y'],hist,q,j) for j in SITES]
                assert all(x!=0 for x in nominal) and corrected==[0,0]
                swapped={'shot':'run','initial':dict(zip(TRACKS,[0,0,digit(q[0])]))}
                bad=[digits(st['y'],hist,q,j,swapped) for j in SITES]
                assert bad[0]!=0
                for invalid in ({'shot':'other','initial':{}},{'shot':'run','initial':{}},
                                {'shot':'run','initial':dict(zip(TRACKS,[None,0,0]))}):
                    assert all(digits(st['y'],hist,q,j,invalid) is None for j in SITES)
                failures.append(dict(route=route,k=str(k),offset_B=64*z,raw=list(map(str,nominal)),
                                     referenced=list(map(str,corrected)),permuted=[str(b) if b is not None else None for b in bad]))
    assert digit(box(8)) is None and digit(box(-9)) is None
    rows=[]
    for (m,o),values in records.items():
        assert len(values)==144
        least=min(values)
        rows.append(dict(m=str(m),additional_reference_error=str(o),joint_pass=sum(x[0]>0 for x in values),
                         total=len(values),minimum_margin=str(least[0]),worst_family=least[1:5],
                         worst_site_margins=least[5]))
    return dict(mesh=rows,family_count=144,concrete_decisions=concrete,false_pulse_replay=failures,
                independent_finite_difference_identities=checks,initial_position_interval=['-1','1'],
                half_momentum_scale=str(K0*V),same_trial_reference_required=True)
