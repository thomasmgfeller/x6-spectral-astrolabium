"""Evaluate the fixed-type H3 Gaussian, conditional lobe integrals and boundary sources."""
from fractions import Fraction as Q
from itertools import combinations, product
from math import prod
from pathlib import Path
import sys

SRC=Path(__file__).resolve().parent/'quellen'
sys.path[:0]=[str(SRC),str(SRC/'pr353')]
import skalar as s
import auswerten as a
from traeger import read
iv=a.iv


def scalar(code):
    order=a.support.geometry(code)[1]
    active={(i,j):b for i,j,b in a.coefficients(order)}
    def framed_value(v):
        # Direct quadratic form in scalar fields, independent of Hessian assembly.
        x,y=v[:3],v[3:6]
        minus,plus=v[13:]
        clock=dict(zip(s.I,v[6:13]))
        am=(-128,241,119,-232); ap=am[::-1]
        bm=(-46,-32,-16,0); bp=tuple(-v for v in bm[::-1])
        for j,node in enumerate(s.P):
            clock[node]=((0,)+tuple(x))[j]+minus*bm[j]
        for j,node in enumerate(s.F):
            clock[node]=(tuple(y)+(0,))[j]+plus*bp[j]
        bare=-sum(Q(b,2)*(clock[i]-clock[j])**2 for (i,j),b in active.items())
        return (bare-2*minus*sum(j*k for j,k in zip(am[1:],x))+2*plus*sum(j*k for j,k in zip(ap,y))
                -minus**2*sum(j*k for j,k in zip(am,bm))+plus**2*sum(j*k for j,k in zip(ap,bp)))
    g=s.framed_hessian(15,active); basis=s.eye(15)
    diag=[framed_value(v) for v in basis]
    assert all(g[i][i]==diag[i] for i in range(15))
    for i,j in combinations(range(15),2):
        v=[r+t for r,t in zip(basis[i],basis[j])]
        assert 2*g[i][j]==framed_value(v)-diag[i]-diag[j]
    h=s.block(g,range(6,15),range(6,15));det,inv=s.det_inverse(h)
    l=s.block(g,range(6),range(6,15))
    corr=s.multiply(s.multiply(l,inv),s.transpose(l))
    k=[[g[i][j]-corr[i][j] for j in range(6)] for i in range(6)]
    A=s.block(k,range(3),range(3)); B=s.block(k,range(3),range(3,6))
    detB=s.det_inverse(B)[0]
    square=s.multiply(A,A)
    invT=s.det_inverse([[v+(i==j) for j,v in enumerate(row)] for i,row in enumerate(square)])[1]
    precision=s.multiply(s.multiply(s.transpose(B),invT),B)
    minors=[s.det_inverse(s.block(precision,range(n),range(n)))[0] for n in (1,2,3)]
    assert all(v>0 for v in minors)
    return dict(F4=15-sum(active.values()),hidden_det=det,mixed_det=detB,
                precision_leading_minors=minors,quadratic_coefficients_checked=120)


def jitter_error(tile,edges,setup):
    centres,radius,eta,max_f=setup[1],setup[2],setup[3],setup[-1]
    e=sorted(o/d for o in tile for d in a.support.DELTA)
    dmax=4*a.support.DELTA[1]-tile[0]
    fields={v:iv.bounds(Q(v-5)) for v in s.P+s.F}
    fields[3]=iv.add(fields[3],(e[0],e[-1]))
    for j,c in centres.items():
        lo,hi=c-radius,c+radius
        fields[j]=(-2+4*lo+(1-lo)*e[0],-2+4*hi+(1-hi)*e[-1])
    cf=dict.fromkeys(s.I,iv.bounds(Q(1)))
    for i,j,k in edges:
        if j in cf:
            cf[j]=iv.add(cf[j],iv.mul(iv.bounds(Q(k,19)),iv.sq(iv.sub(fields[j],fields[i]))))
    b2=sum((a.MASS*eta*f)**2 for f in max_f)/3
    a2=sum((a.MASS*eta*dmax*f*max(map(abs,cf[j]))/2)**2 for j,f in zip(s.I,max_f))/3
    t=a.COUPLING/2
    return t*a.sqroot(a2*b2,a2*b2)[1]+t*t*b2/2


def dust(code,rho,*,full_density_identity=False):
    order=a.support.geometry(code)[1];edges=a.coefficients(order);setup=a.tube.template(code)
    paths,centres,radius,eta,low,high=setup
    assert min(low)>0 and max(high)*4*(1+eta)*(4*a.support.DELTA[1]+Q(3,32))<1
    assert full_density_identity or all(sum((v,j) in order for v in s.I)<4 for j in s.I)
    mid=sum(a.support.WINDOWS[0])/2
    anchor=iv.center(a.phase_box((paths,centres,radius,0,low,high),edges,(mid,mid),rho,{j:(c,c) for j,c in centres.items()},(rho,rho)))
    profile={'clock_center':{str(j):str(c) for j,c in centres.items()},'clock_halfwidth':str(radius),
             'dwell_affine_ranges_per_vertex':{str(j):(str(l),str(h)) for j,l,h in zip(s.I,low,high)}}
    norms=[]; projections=[]; eps=Q(0)
    for start,end in a.support.WINDOWS:
        norms.append(a.tile_mass((start,end)))
        proj=Q(0)
        for i in range(8):
            step=(end-start)/8; tile=(start+i*step,start+(i+1)*step)
            old=iv.phase_box(order,tile,rho,4,profile); new=a.phase_box(setup,edges,tile,rho)
            both=(max(old[0],new[0]),min(old[1],new[1]))
            assert both[0]<=both[1]
            weight=a.tile_mass(tile)
            proj+=iv.mul(weight,iv.bounds(a.projection(both,anchor)))[0]
            eps+=weight[1]*jitter_error(tile,edges,setup)
        projections.append(proj)
    total=iv.add(*norms)
    eps=a.quant(iv.bounds(eps/total[0]))[1]
    def certify(lower):
        c=a.quant(iv.bounds(max(0,lower/total[1])))[0]
        if c<=eps:
            return dict(c=c,status='HOLD')
        rel=a.quant(iv.bounds(2*eps/(a.B*(c-eps))))[1]
        return dict(c=c,relative_upper=rel,status='PASS' if rel<=Q(1,50) and a.B*(1+rel)<3 else 'HOLD')
    base=certify(sum(projections))
    # Arbitrary phase of the right lobe has projection no less than minus its mass.
    any_angle=certify(projections[0]-norms[1][1])
    right=a.quant(a.ratio(norms[1],total))
    distance=2*right[1]
    if code==6840:
        old=read('pr353/ergebnis.json')[str(rho)]['raw_full_box']
        assert base['c']==Q(old['amplitude_modulus_lower'])
        assert abs(base['relative_upper']-Q(old['relative_abs_error_upper']))<=Q(1,10**12)
    return dict(raw=base,all_relative_lobe_phases=any_angle,right_weight=right,
                max_phase_only_distance=distance,arm_perturbation_upper=eps)


def blind_sources():
    census=read('kapazitaet.json')['by_type']; e=read('gewichte.json')['laws']; ch=read('kette.json')
    laws=[(v,w) for v in e.values() for w in (ch['law'],ch['alternative_same_N13']['law'],ch['alternative_same_new_N14']['law'])]
    union=set().union(*(set(v)|set(w) for v,w in laws))
    out={}; support=a.support
    for key in sorted(union,key=int):
        if not census[key]['full_box']: continue
        code=int(key);rel=support.geometry(code)[1]; coeff={(i,j):b for i,j,b in a.coefficients(rel)}
        visible=[j for j in s.I if sum((i,j) in rel for i in s.I)<4]
        if len(visible)==7:continue
        derived={j:-sum(coeff.get((i,j),0)*v for i,v in zip(s.P,(76,47,24,8)))/Q(64) for j in s.I+s.F}
        assert all(derived[j]==int(j in visible) for j in s.I+s.F)
        setup=a.tube.template(code);paths,centres,r,eta,_,high=setup
        assert max(high)*4*(1+eta)*(4*support.DELTA[1]+Q(3,32))<1
        def fraction(vals):
            return sum(x for j,x in zip(s.I,support.fractions_on_paths(paths,vals)) if j in visible)
        central=fraction(centres);dev=Q(0)
        for j in s.I:
            u=centres.copy();u[j]+=r;dev+=abs(fraction(u)-central)
        lo=(central-dev)*(1-eta);hi=(central+dev)*(1+eta)
        out[key]=dict(hidden=[j for j in s.I if j not in visible],relative_field_interval=(lo,hi),
                      six_weights=[(Q(v.get(key,0))+Q(w.get(key,0)))/2 for v,w in laws])
    example=min(out,key=lambda c:(-min(out[c]['six_weights']),int(c)))
    code=int(example);rows=out[example]; paths,centre,r,eta,_,_=a.tube.template(code)
    rel=support.geometry(code)[1];edges=a.coefficients(rel)
    # Exact test with e=1/4 (delta=Delta/4 in the right lobe). Scale W=w/Delta.
    y={j:Q(j-5) for j in s.P+s.F};y[3]+=Q(1,4);duration=y[7]-y[3]
    y.update({j:y[3]+duration*centre[j] for j in s.I})
    shares=support.fractions_on_paths(paths,centre)
    # W=w/Delta; the exact collar contributes another term proportional to 1/Delta.
    w={j:Q(0) for j in s.P+s.F}
    w.update({j:4*duration*f for j,f in zip(s.I,shares)})
    def action(y,w):
        return -sum(w.values())/2-sum(b*w[j]*(y[j]-y[i])**2 for i,j,b in edges)/38
    def source(w):
        A=Q(1,256);B=Q(1,16384);total=0
        for m,n in product((-1,1),repeat=2):
            shifted=y.copy()
            for j,v in zip(s.P,(76,47,24,8)):shifted[j]+=m*A+n*B*v
            total+=m*n*action(shifted,w)
        return Q(19,64)*total/(4*A*B*duration)
    j=rows['hidden'][0]
    assert all(not(i in s.P and end==j) for i,end,b in edges)
    w2=w.copy();w2[j]*=1+eta/2
    changed={i:t+(Q(i+2,1024) if i in s.P+s.F else 0) for i,t in y.items()}
    assert action(changed,w2)-action(changed,w)==action(y,w2)-action(y,w)
    collar={j:Q(j in s.P+s.F,8) for j in range(15)}
    assert source(collar)==0
    assert all(w2[j]*support.DELTA[1]<1 for j in s.I)
    assert source(w2)==source(w)==4*sum(f for v,f in zip(s.I,shares) if v not in rows['hidden'])
    return dict(rows=out,example=code,hidden_event=j,source_value=source(w),true_change=(w2[j]-w[j])/duration,
                below_98=sum(t['relative_field_interval'][1]<Q(98,100) for t in out.values()))


def chain_pointer(code,field_record,rho):
    setup=a.tube.template(code); paths,centres,r,eta,low,high=setup
    order=a.support.geometry(code)[1];eds=a.coefficients(order)
    assert len(paths)==1 and len(paths[0])==7
    X0=field_record['source_value']
    fl,fh=field_record['rows'][str(code)]['relative_field_interval']
    # A correction exp(±i t(X-X0)) moves each point by at most t*|X-X0|.
    perturb=a.COUPLING/2*max(abs(a.MASS*fl-X0),abs(a.MASS*fh-X0))
    mid=sum(a.support.WINDOWS[0])/2
    anchor=iv.center(a.phase_box((paths,centres,r,0,low,high),eds,(mid,mid),rho,
                                 {j:(c,c) for j,c in centres.items()},(rho,rho)))
    lower=Q(0);denom=Q(0)
    for l,h in a.support.WINDOWS:
        step=(h-l)/8
        for i in range(8):
            tile=(l+i*step,l+(i+1)*step)
            w=a.tile_mass(tile);denom+=w[1]
            phase=a.phase_box(setup,eds,tile,rho)
            lower+=iv.mul(w,iv.bounds(a.projection(phase,anchor)))[0]
    c=a.quant(iv.bounds(max(Q(0),lower/denom)))[0]
    if c<=perturb:
        return dict(status='HOLD',c=c)
    spread=2*perturb/(a.COUPLING*(c-perturb))
    bounds=a.quant((X0-spread,X0+spread))
    assert 0<a.COUPLING*bounds[0]<a.COUPLING*bounds[1]<3
    interval=a.quant((1-bounds[1]/a.MASS,1-bounds[0]/a.MASS))
    return dict(status='FAIL' if interval[0]>Q(1,50) else 'HOLD',
                amplitude_floor=c,perturbation=perturb,estimated_mass=bounds,
                relative_underread=interval)
