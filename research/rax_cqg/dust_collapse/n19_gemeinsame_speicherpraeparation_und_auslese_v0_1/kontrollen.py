"""Independent edge-action variations, fixed-output witnesses and scale identifiability."""
from fractions import Fraction as F
from itertools import combinations
from ensemble import B,V,FOCUS,quantize
from wege import ROUTES
from staubgeraet import solve,verify


def exact_actions():
    # Construct a fresh reference polynomial from the native order and the route.
    from gemischt import ORDER
    edges={}
    for i,j in ORDER:
        level=sum((i,n) in ORDER and (n,j) in ORDER for n in range(19))
        if level<4:edges[i,j]=(1,-9,16,-8)[level]
    total=0;reductions=0
    for route,tracks in ROUTES.items():
        for k,drift in ((F(1),F(1,10**11)),(F(1,10**11),-F(1,10**11))):
            w={i:(F(0) if i in (15,17) else F(i+3,37)) for i in range(19)}
            y={i:F(i*i-2,13) for i in range(19)}
            source=F(1,10**6)
            p=(F(1,7),F(-2,9),F(3,13))
            records={('Y',j):v for j,v in y.items()}
            records.update({('w',j):v for j,v in w.items()})
            on=records.copy()
            for a,track in enumerate(tracks):
                on[a,0]=records[a,0]=F(a+1,11)
                last=0
                for j,inertia,ij in track:
                    records[a,j]=F(j*j+3*a+2,19)
                    on[a,j]=on[a,last]+p[a]/(k*w[inertia])+(y[j]-y[ij[0]] if ij else 0)
                    last=j
            def action(z,include_device=True):
                ans=19*sum(z['w',j] for j in y)-source*z['w',16]
                ans+=sum(c*z['w',j]*(z['Y',j]-z['Y',i])**2 for (i,j),c in edges.items())
                if not include_device:return ans
                for a,track in enumerate(tracks):
                    last=0
                    for j,weight,ij in track:
                        d=z[a,j]-z[a,last]
                        dy=z['Y',j]-z['Y',ij[0]] if ij else 0
                        ans+=k*z['w',weight]*(d*d-2*d*dy+dy*dy)
                        if ij:ans+=drift*z['w',j]*dy*dy
                        last=j
                    ans-=2*p[a]*z[a,7]
                return ans
            # Compare complete Routh action for offset (position) + momentum initial data.
            routh=action(on,False)
            for a,track in enumerate(tracks):
                routh-=2*p[a]*on[a,0]
                for j,inertia,ij in track:
                    routh-=p[a]**2/(k*w[inertia])
                    if ij:
                        dy=y[j]-y[ij[0]]
                        routh+=drift*w[j]*dy*dy-2*p[a]*dy
            assert routh==action(on)
            reductions+=1
            # Analytic partials at fixed independent positions. Check all dust and device
            # coordinates by exact rational central differences, including source and collars.
            grad={j:F(0) for j in records}
            for j in y:grad['w',j]=19-source*(j==16)
            for (i,j),c in edges.items():
                gap=y[j]-y[i];cur=2*c*w[j]*gap
                grad['Y',j]+=cur;grad['Y',i]-=cur;grad['w',j]+=c*gap*gap
            for a,track in enumerate(tracks):
                last=0
                for j,inertia,ij in track:
                    gap=(y[j]-y[ij[0]]) if ij else 0
                    rel=records[a,j]-records[a,last]-gap
                    cur=2*k*w[inertia]*rel
                    grad[a,j]+=cur;grad[a,last]-=cur;grad['w',inertia]+=k*rel*rel
                    if ij:
                        correction=2*drift*w[j]*gap-cur
                        grad['Y',j]+=correction;grad['Y',ij[0]]-=correction;grad['w',j]+=drift*gap*gap
                    last=j
                grad[a,7]-=2*p[a]
            step=F(3,17)
            for key in grad:
                plus=records.copy();minus=records.copy()
                plus[key]+=step;minus[key]-=step
                finite=(action(plus)-action(minus))/(2*step)
                assert grad[key]==finite
                total+=1
    return {'rational_partials':total,'reduced_action_identities':reductions}


def controls(previous,early):
    from quelle import box,SCALE
    from proben import samples
    from uhrauslese import LABELS
    _,y,w=samples(previous,early)[0][0]
    rows=[]
    for J in LABELS:
        field=solve(y,w,J,(box(0),)*3,F(1),box(0),'positive_bridge')
        H,A=verify(field,J,(box(0),)*3,F(1),box(0),'positive_bridge',(box(0),)*3)
        inputs={18:[field['y'][18],H[0][18],H[1][18]],7:[field['y'][7],H[2][7],H[0][7],H[1][7]]}
        rows.append((J,inputs))
    collisions=[]
    for bits in range(26,44):
        step=F(16,2**bits)
        for (a,first),(b,second) in combinations(rows,2):
            matches=[]
            for i in (18,7):
                matches.append(all((v:=quantize(l,step)).lo==v.hi==(u:=quantize(r,step)).lo==u.hi
                                   for l,r in zip(first[i],second[i])))
            if all(matches):
                collisions.append({'bits':bits,'sources':list(map(str,(a,b))),
                    'integer_codes':{str(i):[int(F(quantize(v,step).lo,SCALE)/step) for v in first[i]]
                                      for i in (18,7)}})
    assert collisions
    hardest=max(collisions,key=lambda v:v['bits'])
    # Frozen-field quantum diagnostic. Even an arbitrary canonical input must obey the
    # two-readout uncertainty when they are interpreted as undisturbed Heisenberg observables.
    w7_min=min(F(w_case[7].lo,SCALE) for _,_,w_case in samples(previous,early)[0])
    two_time=4*w7_min*F(1,10**12)**2
    return {'action':exact_actions(),'largest_tested_joint_collision_at_nominal_settings':hardest,
            'fixed_clock_two_site_bound_if_both_rms_1e-12':{'w7_min':str(w7_min),'hbar_eff_upper_per_k':str(two_time)}}
