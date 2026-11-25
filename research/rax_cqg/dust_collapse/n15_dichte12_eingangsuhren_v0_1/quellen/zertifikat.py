"""Exact no-record witness and uniform bounds on the seven-dimensional collar."""
import json
import sys
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from fenster import box, phases, half_diameter, K, D, I, S, ORDER, PAST, INNER, FUTURE, EDGES

ETA=F(1,2**20)
W0=F(1,8)
ORIGIN={j:F(-7,4)+K*F(k,8) for k,j in enumerate(INNER,1)}
ORIGIN.update({j:F(j-5) for j in FUTURE})
CROSS=[(i,j,b) for (i,j),b in EDGES.items() if i in INNER and j in FUTURE]

def up(q):
    return str(F(-(-q*10**17).__floor__(),10**17))

def collar():
    # Interaction remainder after subtracting the common reference history's phase.
    assert {i for i,j,b in CROSS}=={11,12,13,14}
    assert len(CROSS)==10
    radius=K/64
    first=F(0)
    second=F(0)
    for i,j,b in CROSS:
        dy=ETA if j!=7 else 0
        gap=abs(ORIGIN[j]-ORIGIN[i])
        first+=abs(b)*(ETA*(2*gap*radius+radius**2)+2*W0*dy*radius)/38
        second+=abs(b)*2*ETA*dy*radius/38
    phase_bound=first+second
    rows={}
    for p in (-1,0,1):
        _,_,closed,_=phases(p)
        cosine=1-half_diameter(closed)**2/2
        assert cosine>F(96,100)
        eps=phase_bound/cosine
        trace=2*eps/(1-eps)
        # Uniform distance, in sup norm, from the affine state on the scaled cube.
        rem=(second+phase_bound**2/2)/cosine
        rem2=(phase_bound**3/6+first*second+second**2/2)/cosine
        rows[str(p)]={'reference_ratio_disk_upper':up(eps),'trace_distance_upper':up(trace),
                      'equal_prior_percent_upper':up(50*(1+trace)),
                      'affine_state_sup_remainder':up(rem),
                      'trace_distance_error_two_affine_rays':up(2*rem/(1-eps)),
                      'quadratic_state_sup_remainder':str(rem2),
                      'trace_distance_error_two_quadratic_rays_upper':str(F(-(-(2*rem2/(1-eps))*10**23).__floor__(),10**23))}
    return {'edges':[list(t) for t in sorted(CROSS)],'eta':str(ETA),
            'mixed_phase_bound_rad':up(phase_bound),'rows':rows}

def profile(u):
    y={j:F(j-5) for j in PAST+FUTURE}
    y[3]=F(-7,4)
    y.update({j:y[3]+K*t for j,t in u.items()})
    c={j:-F(1,2)-sum(F(b,38)*(y[j]-y[i])**2 for (i,t),b in EDGES.items() if t==j) for j in INNER}
    # Lagrange weights solve both pulse constraints pointwise in the clocks.
    r=(y[14]-y[12])/(y[14]-y[13])
    d={12:F(1),13:F(9,16)*r,14:F(9,8)*(r-1)}
    m=sum(d.values())
    energy=sum(c[j]*t for j,t in d.items())
    d[4]=(m*c[5]-energy)/(c[4]-c[5])
    d[5]=-m-d[4]
    return y,c,d

def support():
    radius=F(1,2**22); offset=F(1,2**14); noise=F(1,2**20)
    assert {(j,b) for (i,j),b in EDGES.items() if i==6 and ORDER.index(j)>ORDER.index(11)}=={(12,-9),(13,16),(14,-8)}
    rows=[]
    for arm in (-1,1):
        center={j:F(k,8) for k,j in enumerate(INNER,1)}
        center[5]+=arm*F(1,1000)
        s=1/(72*D*K*K)
        assert (I.of(center[5]-F(1,4))-arm*s).absmax()/F(S)+radius < F(1,16384)
        u={j:box(t-radius,t+radius) if j!=6 else I.of(t) for j,t in center.items()}
        y,c,d=profile(u)
        faces=[I.of(0)]+[(u[i]+u[j])/2 for i,j in zip(INNER,INNER[1:])]+[I.of(1)]
        f={j:faces[k+1]-faces[k] for k,j in enumerate(INNER)}
        # The absolute/relative thresholds simultaneously separate the two cells.
        margins=[]
        for j in INNER:
            delta=d.get(j,I.of(0))*offset
            for side in (-1,1):
                midpoint=I.of(F(255,2048)) if j==11 else f[j]+side*delta
                x=midpoint+box(-noise,noise)
                margins.extend([(x-F(99,100)*f[j]).lo,(F(101,100)*f[j]-x).lo])
                if j==12:
                    assert (side*(x-W0)).lo>0
                    assert offset>noise # x12-f12 = side*offset + independent noise
        assert min(margins)>0 and noise<F(1,16384)
        yc,cc,dc=profile(center)
        assert sum(dc.values())==0 and sum(cc[j]*t for j,t in dc.items())==0
        for power in (0,1):
            assert sum(EDGES[6,j]*dc[j]*yc[j]**power for j in (12,13,14))==0
        # Check an independent complete action at asymmetric inner points, shifted
        # future fields and pulses, including a pulse outside the original pair.
        trials=0
        for k in (-1,0,1):
            sample={j:t+(radius*F(k*(j%3-1),2) if j!=6 else 0) for j,t in center.items()}
            yy,_,dd=profile(sample)
            midfaces=[F(0)]+[(sample[i]+sample[j])/2 for i,j in zip(INNER,INNER[1:])]+[F(1)]
            xx={j:midfaces[n+1]-midfaces[n]+noise*F(k,2) for n,j in enumerate(INNER)}
            xx[11]=F(255,2048)
            for j in (8,9,10): yy[j]+=k*ETA*F(j-7,4)
            for pulse in (F(0),F(-1,8),F(1,8),F(5,17)):
                # Use physical w=D*x in the proof. In this rational witness check
                # common rescaling of all inner w cancels, so D is set to one.
                vals=[]
                for sign in (-1,1):
                    w={j:xx[j]+sign*offset*dd.get(j,0) for j in INNER}
                    w.update({j:W0+k*ETA*F(j-6,5) for j in FUTURE})
                    w.update({j:W0 for j in PAST})
                    action=-sum(w.values())/2
                    for end,j in enumerate(ORDER):
                        for lag,b in enumerate((1,-9,16,-8),1):
                            if end<lag: break
                            i=ORDER[end-lag]
                            step=pulse if i==6 and j in (12,13,14) else 0
                            action-=F(b,38)*w[j]*(yy[j]-yy[i]-step)**2
                    vals.append(action)
                assert vals[0]==vals[1]
                trials+=1
        rows.append({'arm':arm,'d_at_center':{str(j):str(v) for j,v in sorted(dc.items())},
                     'action_equalities':trials,'band_margin_at_least':str(F(min(margins)*10**9//S,10**9))})
    return {'offset':str(offset),'clock_box_radius':str(radius),'density_noise_radius':str(noise),'rows':rows}

if __name__=='__main__':
    print(json.dumps({'collar':collar(),'witness':support()},indent=2))
