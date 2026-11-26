"""Independent action variations and failure controls on the same causal order."""
from fractions import Fraction as F
from itertools import product
from speichermodell import coupled
from auslesetest import receiver_read,stored_read,abs_upper
from traeger import native_cases


def action_audit(order):
    # Inputs are exact fractions; centred differences are exact for every
    # separate coordinate of this quadratic-in-clocks, linear-in-weights action.
    edges={}
    for i,j in order:
        level=sum((i,k) in order and (k,j) in order for k in range(19))
        if level<4:
            edges[i,j]=(1,-9,16,-8)[level]
    J=F(1,10**6)
    tests=0; reductions=0
    for setting in range(1,5):
        g=F((-1)**setting*setting,3)
        stiffness=(F(1),F(1,10**11),F(3,7),F(5,3))[setting-1]
        mismatch=F(setting-2,51) if setting!=2 else -stiffness
        pu,ph,pt=F(setting,17),F(-1,9),F(2,23)
        y={i:F(i*i-4,17+setting) for i in range(19)}
        w={i:F(i+2,37) for i in y}
        state={**{('Y',i):v for i,v in y.items()},**{('w',i):v for i,v in w.items()}}
        a,x,h,zu,zh,b=coords=('A','X','H','Zu','Zh','B')
        state.update({k:F(i+3,5+setting) for i,k in enumerate(coords)})
        pairs=[(15,16,None,a,g),(16,18,a,x,g),(17,18,None,h,g),
               (18,7,x,zu,0),(18,7,h,zh,0),(18,7,None,b,1)]
        def value(v):
            ans=19*sum(v['w',i] for i in y)-J*v['w',16]
            for (i,j),weight in edges.items():
                ans+=weight*v['w',j]*(v['Y',j]-v['Y',i])**2
            for i,j,start,end,c in pairs:
                gap=v['Y',j]-v['Y',i]
                change=v[end]-(v[start] if start else 0)
                # Compute the expanded link action independently of the solver.
                ans+=v['w',j]*(stiffness*(change**2-2*c*change*gap+c*c*gap**2)+(mismatch if c else 0)*gap**2)
            return ans-2*(pu*v[zu]+ph*v[zh]+pt*v[b])
        deriv={k:F(0) for k in state}
        for i in y:deriv['w',i]=19-J*(i==16)
        for (i,j),weight in edges.items():
            gap=y[j]-y[i]
            deriv['w',j]+=weight*gap**2
            deriv['Y',i]-=2*weight*w[j]*gap
            deriv['Y',j]+=2*weight*w[j]*gap
        for i,j,start,end,c in pairs:
            gap=y[j]-y[i]
            velocity=state[end]-(state[start] if start else 0)-c*gap
            mom=stiffness*w[j]*velocity
            term=mismatch if c else 0
            deriv['Y',i]+=2*c*mom-2*term*w[j]*gap
            deriv['Y',j]-=2*c*mom-2*term*w[j]*gap
            deriv['w',j]+=stiffness*velocity**2+term*gap**2
            deriv[end]+=2*mom
            if start:deriv[start]-=2*mom
        for key,p in ((zu,pu),(zh,ph),(b,pt)):deriv[key]-=2*p
        step=F(2,7)
        for key in state:
            plus={**state,key:state[key]+step}
            minus={**state,key:state[key]-step}
            assert (value(plus)-value(minus))/(2*step)==deriv[key]
            tests+=1
        on=state.copy()
        on[a]=g*(y[16]-y[15])+pu/(stiffness*w[16])
        on[x]=on[a]+g*(y[18]-y[16])+pu/(stiffness*w[18])
        on[h]=g*(y[18]-y[17])+ph/(stiffness*w[18])
        on[zu]=on[x]+pu/(stiffness*w[7]);on[zh]=on[h]+ph/(stiffness*w[7])
        on[b]=y[7]-y[18]+pt/(stiffness*w[7])
        native=19*sum(w.values())+sum(c*w[j]*(y[j]-y[i])**2 for (i,j),c in edges.items())-J*w[16]
        reduced=-2*g*(pu*(y[18]-y[15])+ph*(y[18]-y[17]))-2*pt*(y[7]-y[18])
        reduced-=(pu**2/w[16]+(pu**2+ph**2)/w[18]+(pu**2+ph**2+pt**2)/w[7])/stiffness
        reduced+=mismatch*sum(w[j]*(y[j]-y[i])**2 for i,j,_,_,c in pairs if c)
        assert value(on)==native+reduced
        reductions+=1
    return {'exact_partial_derivatives':tests,'exact_reductions':reductions}


def run(early):
    from quelle import box,hull,DATA,SCALE
    from gemischt import ORDER
    from uhrauslese import LABELS,J
    from fenster import endpoints
    from zustand import nominal
    y,w=nominal(early)[1]
    zero=box(0)
    def observations(state,site):
        if site==18:return (state['y'][18],*state['read'])
        return (state['y'][7],state['stamp'],*state['stored'])
    # Without the quadratic compensation at unit gain, the native link
    # into the sender cancels exactly after free readout minimization.
    e,windows=DATA[-2:]
    s=hull(*endpoints(windows[0],e))
    bad_density=-6-6*s-s*s
    assert bad_density.hi<-6*SCALE
    # A highly loaded record need not preserve the old decision rule.
    large=box(F(1,10**11))
    wrong=[]
    for pu,ph in ((large,zero),(zero,large)):
        state=coupled(y,w,0,0,pu,ph)
        wrong.append(str(receiver_read(*observations(state,18))))
    assert wrong==[str(J),str(-J)]
    # Midpoint common to 0 and +J with coarse readout at BOTH sites.
    base=coupled(y,w,0,0,zero,zero)
    pulse=coupled(y,w,0,J,zero,zero)
    shared={}
    for i in (18,7):
        mid=[(a+b)/2 for a,b in zip(observations(base,i),observations(pulse,i))]
        for trial in (base,pulse):
            assert all(abs_upper(a-b)<F(3,10**10) for a,b in zip(observations(trial,i),mid))
        shared[str(i)]=[v.data() for v in mid]
    records=[]
    off=[]
    direct_tests=0
    for label,yy,ww,_ in native_cases(early)[0]:
        enabled=coupled(yy,ww,label,label,zero,zero)
        disabled=coupled(yy,ww,label,label,zero,zero,gain=0)
        assert receiver_read(*observations(enabled,18))==label
        assert stored_read(*observations(enabled,7))==label
        off.append([*observations(disabled,18),*observations(disabled,7)])
        records.append({'source':str(label),'records_18':[v.data() for v in observations(enabled,18)],
                        'records_7':[v.data() for v in observations(enabled,7)]})
    for vals in off[1:]:
        assert all((a-b).contains_zero() for a,b in zip(vals,off[0]))
    for j,a,b in product(LABELS,(-1,1),(-1,1)):
        state=coupled(y,w,0,j,box(F(a,10**14)),box(F(b,10**14)),chain=False)
        assert receiver_read(*observations(state,18))==j
        direct_tests+=1
    return {'action':action_audit(ORDER),'positive_cone_witness_with_memory':records,
            'coupling_off_same_receiver_and_stored_observations':True,
            'direct_link_variant_checks':direct_tests,'unit_gain_no_compensation_sender_D':bad_density.data(),
            'overloaded_null_classified_as':wrong,'single_channel_overload':'1/100000000000',
            'coarse_error_each':'3/10000000000','common_coarse_readings':shared}
