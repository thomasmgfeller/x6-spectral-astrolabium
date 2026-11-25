"""Blind shell and current controls on the same evolving marginally bound dust ball."""
from fractions import Fraction as F
from math import sqrt
from basis.intervall import Box, box, SCALE
from basis.auslesen import PI, estimate, root_bound
from basis import klassik

END=5*box(5).sqrt_nonnegative_part()/3
PIBOX=Box.hull(*PI)
GRID=klassik.GRID
TIMES=tuple(F(k,4) for k in range(5))
MASSES=(F(1,4),F(1),F(4))


def ends(z):
    return [str(F(z.lo,SCALE)),str(F(z.hi,SCALE))]


def cube(z):
    return z*z.square()


def cbrt(z):
    assert z.lo>0
    lo=root_bound(F(z.lo,SCALE),3)[0]
    hi=root_bound(F(z.hi,SCALE),3)[1]
    return Box.hull(lo,hi)


def geom(a,x,mass,inside):
    # q=m(a)/a^3. L=R' and H=d(log L)/dx from the Einstein-dust solution.
    q=mass*(5-3*a.square()/100)/2000 if inside else box(mass)/cube(a)
    qp=-3*mass*a/100000 if inside else -3*q/a
    c=(2*q).sqrt_nonnegative_part()
    t=END*x
    f=1-F(3,2)*c*t
    d=-F(3,2)*c-a*qp/c
    numer=1+t*d
    root=cbrt(f)
    assert numer.lo>0
    return a*root.square(),numer/root,END*(d/numer+c/(2*f))


def locate(signs):
    if not signs or any(v not in (0,1) for v in signs):return None
    occupied=[i for i,v in enumerate(signs) if v]
    if not occupied:return None
    last=occupied[-1]
    if last+1>=len(signs) or occupied!=list(range(last+1)):raise ValueError('unvollständiger Materialrand')
    return last,last+1


def shell(a,b,x,m,inside):
    # Reflect at b. A clock on station a emits and receives the two radial rays.
    assert (b<=10 if inside else a>=10)
    spatial=Box.hull(a,b)
    guard=Box.hull(x-F(1,10),x+F(1,10))
    _,max_l,h=geom(spatial,guard,m,inside)
    cap=F(max_l.hi,SCALE)/F(END.lo,SCALE)
    drift=F(max(-h.lo,h.hi),SCALE)
    assert cap*(b-a)<F(1,10)
    steps=32
    da=(b-a)/steps
    emit=recv=box(x);vol=box(0)
    for i in range(steps):
        aa=Box.hull(b-(i+1)*da,b-i*da)
        radius,length,_=geom(aa,box(x),m,inside)
        vol+=4*PIBOX*radius.square()*length*da
        for sign in (-1,1):
            origin=emit if sign<0 else recv
            collar=origin+Box.hull(-da*cap,da*cap)
            assert guard.lo<=collar.lo<=collar.hi<=guard.hi
            _,L,_=geom(aa,collar,m,inside)
            target=origin+sign*da*L/END
            if sign<0:emit=target
            else:recv=target
    boundary_integral=4*PIBOX*(cube(geom(box(b),box(x),m,inside)[0])
                               -cube(geom(box(a),box(x),m,inside)[0]))/3
    assert vol.lo<=boundary_integral.lo<=boundary_integral.hi<=vol.hi
    # Enlarge acquired intervals for instrument tolerances. R at the true
    # boundary, mass, and comoving coordinates never enter the decoder.
    vol=vol*Box.hull(F(99,100),F(101,100))
    tickerr=F(recv.hi-emit.lo,2*SCALE*100)
    noise=Box.hull(-tickerr,tickerr)
    return {'volume':ends(vol),'emission':ends(emit+noise),'reception':ends(recv+noise)},drift


def mass_at(a,m):
    return m*klassik.mass_fraction(a)


def rk_track(a,m,until):
    # Particles evolve from initial data in areal coordinates. No boundary label enters.
    return klassik.rk_radius(float(a),float(mass_at(a,m)),until)


def cap_difference(m,t,cut=6):
    # Enclose m(a(t)) at a fixed areal radius by monotone interval bisection.
    a,b=F(1),F(10)
    for _ in range(36):
        mid=(a+b)/2
        rad=geom(box(mid),box(t),m,True)[0]
        if rad.hi<cut*SCALE:a=mid
        elif rad.lo>cut*SCALE:b=mid
        else:break
    assert a<b and b-a<F(1,100000)
    return Box.hull(mass_at(a,m),mass_at(b,m))


def tracer_faces(frame):
    # 1 unit of quantisation error per position and per face. A comparison
    # whose sign is unresolved must not be silently assigned to either side.
    units = frame['positions']
    states=[]
    for face in frame['faces']:
        if any(v is not None and abs(v-face)<=2 for v in units):
            raise ValueError('Tracer liegt in der Unsicherheit der Messfläche')
        states.append([v is not None and v<face for v in units])
    return states


def transfers(previous,current,weights):
    if len(previous)!=len(current) or len(weights)!=len(current[0]):
        raise ValueError('Unvollständige Traceraufnahme')
    result=[]
    for old,new in zip(previous,current):
        entered=sum((v for v,i,j in zip(weights,old,new) if j and not i),F())
        left=sum((v for v,i,j in zip(weights,old,new) if i and not j),F())
        result.append([str(entered),str(left)])
    return result


def generate():
    frames=[];flow=[];summaries=[]
    for m in MASSES:
        startpair=None; trajectories=[]
        # Mid-cell material tracers with exact initial rest mass per cell.
        labels=[(a+b)/2 for a,b in zip(GRID,GRID[1:])]
        weights=[mass_at(b,m)-mass_at(a,m) for a,b in zip(GRID,GRID[1:])]
        # Split the cell containing the true end of the initial support. The
        # split is generator-side and does not supply an endpoint to the detector.
        for k,(a,b) in enumerate(zip(GRID,GRID[1:])):
            if a<10<b:labels[k]=(a+10)/2
        for x in TIMES:
            t=float(x)*klassik.END
            signs=[int(klassik.evolve(float(a),t,float(m))[1]>0) for a in GRID]
            assert signs==[int(a<10) for a in GRID]
            band=locate(signs);assert band and (startpair is None or band==startpair)
            startpair=band
            left,right=band
            pair=[shell(GRID[left-5],GRID[left],x,m,True),
                  shell(GRID[right],GRID[right+5],x,m,False)]
            obs={'inside':pair[0][0],'outside':pair[1][0],'clock_unit':ends(END),
                 'log_L_drift_per_x':str(max(d for _,d in pair)),
                 'reflection_x':str(x),'verified_assumptions':True}
            frames.append({'case':str(m),'x':str(x),'marks':band,'occupied':signs,'reading':obs})
            got=estimate(obs)
            bounds=tuple(map(F,got['radius']))
            truth=geom(box(10),box(x),m,True)[0]
            assert bounds[0]<=F(truth.lo,SCALE)<=F(truth.hi,SCALE)<=bounds[1]
            relative=max(1-bounds[0]/F(truth.hi,SCALE),bounds[1]/F(truth.lo,SCALE)-1)
            summaries.append({'M':str(m),'x':str(x),'radius':got['radius'],
                              'truth':ends(truth),'max_error':float(relative)})
            pos=[rk_track(a,m,t) if weight else None for a,weight in zip(labels,weights)]
            supply=mass_at(F(10),m)
            assert sum(weights)==supply
            # Geometric bounds on the moving edge are the two identified gauges.
            limits=[klassik.evolve(float(GRID[k]),t,float(m))[0] for k in band]
            tracer={'positions':[round(v*10**8) if v is not None else None for v in pos],
                    'faces':[round(f*10**8) for f in (*limits,6)],'weights':list(map(str,weights))}
            frames[-1]['tracer']=tracer
            observed=tracer_faces(tracer)
            for side,k in enumerate(band):
                assert observed[side]==[bool(w) and a<GRID[k] for a,w in zip(labels,weights)]
            enclosed=cap_difference(m,x)
            for accepted,a,w in zip(observed[2],labels,weights):
                if not w:continue
                val=mass_at(a,m)*SCALE
                assert val<enclosed.lo if accepted else val>enclosed.hi
            trajectories.append(observed)
        for k in range(1,len(TIMES)):
            previous,current=trajectories[k-1],trajectories[k]
            counts=transfers(previous,current,weights)
            assert counts[:2]==[['0','0'],['0','0']]
            assert F(counts[2][0])>0 and F(counts[2][1])==0
            fixed=cap_difference(m,TIMES[k])-cap_difference(m,TIMES[k-1])
            assert fixed.lo>0
            # Midpoint tracer inventory has at most one partially cut mass cell
            # at each endpoint of the time window.
            gap=abs(F(counts[2][0])-F(fixed.lo,SCALE))
            assert gap<2*max(weights)
            flow.append({'M':str(m),'x_from':str(TIMES[k-1]),'x_to':str(TIMES[k]),
                         'inner_outer_fixedR6_in_out':counts,'fixed_gain_exact_bounds':ends(fixed)})
    assert locate([int(klassik.evolve(float(a),0,0)[1]>0) for a in GRID]) is None
    return frames,summaries,flow
