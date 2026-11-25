"""Outward interval certificates for an operation on the actual cut register."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys
import json

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'vorstudie'))
from auswertung import binary_test as published_binary
from versuch import (I,S,K,D,EPS,NOISE,ETA,W0,Q0,RADIUS,PAST,FUTURE,INNER,
                     HIDDEN,EDGES,ORDER,clocks,profile,box,decimals,coeffs)
from intervalle import C,cis,sinc

CENTER=F(-7,4)+K/8
R=K*RADIUS
H=F(1,32)
G=F(-8,38)


def cell(lobe,low,high):
    u=clocks(lobe)
    u[4]=box(F(1,8)+low/K,F(1,8)+high/K)
    y,c,d=profile(u)
    for j in PAST+FUTURE: y[j]=I.of(y[j])
    for j in FUTURE[1:]: y[j]+=box(-ETA,ETA)
    faces=[I.of(0)]+[(u[i]+u[j])/2 for i,j in zip(INNER,INNER[1:])]+[I.of(1)]
    f={j:faces[k+1]-faces[k] for k,j in enumerate(INNER)}
    x={j:(F(255,2048) if j==11 else f[j])+box(-NOISE,NOISE) for j in INNER}
    w={j:D*x[j] for j in INNER}
    w.update({j:box(W0-ETA,W0+ETA) for j in FUTURE})
    full=coeffs(y)
    neutral=sum(w[j]*full[j] for j in w)
    # The past factor is independent of setting and all inner/future variables.
    assert (sum(full[j] for j in PAST)/32).absmax()<S
    q=sum(c[j]*d[j] for j in HIDDEN)
    fixed=dict(y);fixed[4]=CENTER
    qstar=sum(coeffs(fixed)[j]*d[j] for j in HIDDEN)
    dy=y[4]-CENTER
    qdiff=G*dy*(2*(y[12]-CENTER)-dy)
    assert max(q.hi,qstar.hi)<0
    return y,d,f,x,w,neutral,q,qstar,qdiff


def odd_phases(data,mode,t):
    y,_,_,_,_,_,q,qs,diff=data
    dc=G*t*(2*(y[12]-y[4])-t)
    if mode=='gemeinsam':
        # Re-evaluating q at the actual cut argument leaves a common class phase.
        assert (q+dc).hi<0
        odd=I.of(0)
    elif mode=='wirkungsquelle':
        odd=D*EPS*Q0*dc/q
    elif mode=='festes_profil':
        odd=D*EPS*Q0*(diff+dc)/qs
    else:
        raise ValueError(mode)
    return dc,odd


def amplitudes(data,mode,t):
    _,_,_,_,w,neutral,_,_,_=data
    dc,odd=odd_phases(data,mode,t)
    mid=cis(neutral+w[12]*dc)
    return mid*cis(-odd),mid*cis(odd),mid*C(0,2*odd*sinc(odd))


def mean_enclosures(mode,t,lower,upper,parts):
    acc=[C(0) for _ in range(6)]
    for lobe in (-1,1):
        for k in range(parts):
            data=cell(lobe,lower+(upper-lower)*k/parts,lower+(upper-lower)*(k+1)/parts)
            vals=amplitudes(data,mode,I.of(0))+amplitudes(data,mode,t)
            acc=[v+a for v,a in zip(acc,vals)]
    return [a.scale(F(1,2*parts)) for a in acc]


def binary(mode,t,lower,upper,parts):
    alo,ahi,da,blo,bhi,db=mean_enclosures(mode,t,lower,upper,parts)
    def norm(x): return (x.conj()*x).re
    nlo,nhi=norm(alo)+norm(blo),norm(ahi)+norm(bhi)
    assert min(nlo.lo,nhi.lo)>0
    # Multiply at equal z before the positive outer diagonal pairing.
    dj=(da.conj()*bhi+alo.conj()*db).im
    dn=((ahi+alo).conj()*da+(bhi+blo).conj()*db).re
    contrast=(dj-(alo.conj()*blo).im/nlo*dn)/nhi
    if mode=='gemeinsam': assert contrast.lo==contrast.hi==0
    else: assert contrast.hi<0
    return {'P_plus_hoch_minus_niedrig':decimals(contrast,17),
            'treffer_prozent_plus_als_niedrig':decimals(50*(1-contrast),14)}


def aperture():
    # Bands in Y, prepared inside the old broad u4 window 1/8 +/- 1/64.
    t=H/D.sqrt()
    assert (t-2*R).lo>0 and (K/64-t-R).lo>0
    assert (F(1,8)/D.sqrt()+R-K/64).lo>0
    min_order=I.of(1)
    worst={key:F(0) for key in ('tv','phase','center')}
    margin=I.of(1).lo
    label_margin=I.of(1).lo
    for lobe in (-1,1):
        data=cell(lobe,-R,R)
        y,d,f,x,_,_,q,qs,diff=data
        min_order=I(min(min_order.lo,(y[4]-t-y[3]).lo,(y[5]-y[4]-t).lo),S)
        shifts=[EPS*Q0*d[j]*diff/(q*qs) for j in HIDDEN]
        worst['center']=max(worst['center'],*(F(s.absmax(),S) for s in shifts))
        tv=sum(F(s.absmax(),S)/(2*NOISE) for s in shifts)
        worst['tv']=max(worst['tv'],tv)
        worst['phase']=max(worst['phase'],F((D*EPS*Q0*diff/qs).absmax(),S))
        wall=F(t.hi,S)
        for step in (-t,I.of(0),t,box(-wall,wall)):
            dc,_=odd_phases(data,'gemeinsam',step)
            for den in (qs,q+dc):
                for sign,j in product((-1,1),INNER):
                    v=x[j]+(sign*EPS*Q0*d[j]/den if j in HIDDEN else 0)
                    margin=min(margin,(v-F(99,100)*f[j]).lo,(F(101,100)*f[j]-v).lo)
                    if j==12:
                        label_margin=min(label_margin,(sign*(v-W0)).lo,(sign*(v-f[j])).lo)
    assert min(margin,label_margin,min_order.lo)>0
    # At null source, remove +/- the common phase. Each wave differs from
    # the neutral wave by at most worst['phase'] per unit preparation mass.
    cells=[cell(a,-R,R) for a in (-1,1)]
    neutral=[v[5] for v in cells]
    diameter=F(max(v.hi for v in neutral)-min(v.lo for v in neutral),S)
    c=1-diameter**2/8
    # For unit positive measure in z, the neutral wave has norm >= c.
    # Normalization bound via projection onto the neutral ray, then triangle.
    eps=worst['phase']
    trace=2*eps/(c-eps)
    return {'shift_Y':decimals(t),'clearance_in_broad_u_window':decimals((K/64-t-R)/K),
            'clock_order_margin_Y_lower':decimals(I(min_order.lo,min_order.lo))[0],
            'relative_and_absolute_threshold_margin':decimals(I(label_margin,label_margin))[0],
            'density_band_margin':decimals(I(margin,margin))[0],
            'maximum_zero_pulse_movement_of_one_center':decimals(I.of(worst['center']),17)[1],
            'initial_TV_distance_upper':decimals(I.of(worst['tv']),12)[1],
            'zero_pulse_residual_per_class_rad_upper':decimals(I.of(eps),17)[1],
            'neutral_relative_amplitude_lower':decimals(I.of(c))[0],
            'zero_pulse_trace_distance_upper':decimals(I.of(trace),18)[1],
            'zero_pulse_equal_prior_optimal_percent_upper':decimals(I.of(50*(1+trace)),14)[1]}


def ensemble(mode,side):
    # Same cubic phase bound and external pairing as in PR 370.
    data=[cell(a,-R,R) for a in (-1,1)]
    errors=F(0)
    base=[]
    for x in data:
        _,a=odd_phases(x,mode,I.of(0))
        base.append(x[5]+side*a)
    for t in (-H/D.sqrt(),H/D.sqrt()):
        terms=[]
        for x in data:
            dc,a=odd_phases(x,mode,t)
            terms.extend(x[5]+x[4][12]*dc+side*a-p for p in base)
        mean=sum(terms)/4
        radius=max(F((x-mean).absmax(),S) for x in terms)
        err=radius**3/(6*(1-radius**2/2))
        assert radius<1 and mean.absmax()+I.of(err).hi<S
        errors+=F(19,8)*err/H**2
    target=I.of(W0)
    if mode!='gemeinsam':
        idx=7 if mode=='festes_profil' else 6
        target+=side*EPS*Q0*sum(1/x[idx] for x in data)/2
    result=target+box(-errors,errors)
    return {'anzeige':decimals(result,12),'maximaler_bias':decimals(I.of(errors),12)[1]}


def exact_controls():
    assert [(i,j,b) for (i,j),b in EDGES.items() if i==4 and ORDER.index(j)>ORDER.index(11)]==[(4,12,-8)]
    tests=0
    for lobe in (-1,1):
        for pos in (F(-2,3),F(0),F(3,5)):
            u=clocks(lobe,True)
            u={j:(z if j==6 else z+RADIUS*pos*F((j%5)+1,6)) for j,z in u.items()}
            y,c,d=profile(u)
            def direct(arg):
                alt={**y,4:arg}
                out={}
                for j in HIDDEN:
                    k=ORDER.index(j)
                    out[j]=-F(1,2)-sum(F(b,38)*(alt[j]-alt[ORDER[k-lag]])**2
                                        for lag,b in enumerate((1,-9,16,-8),1))
                return sum(out[j]*d[j] for j in HIDDEN)
            q=direct(y[4]);assert q==sum(c[j]*d[j] for j in HIDDEN)
            for t in (F(-1,32),F(0),F(1,32),F(1,8),R):
                qt=direct(y[4]+t)
                assert qt-q==G*t*(2*(y[12]-y[4])-t)
                for mode,den in [('gemeinsam',qt),('wirkungsquelle',q),('festes_profil',direct(CENTER))]:
                    odds=EPS*Q0*qt/den # divide the full odd phase by D
                    if mode=='gemeinsam': assert odds==EPS*Q0
                    if mode=='festes_profil':
                        assert odds==EPS*Q0*(1+(G*(y[4]+t-CENTER)*(2*(y[12]-CENTER)-(y[4]+t-CENTER)))/den)
                    tests+=1
    return tests


def run():
    wide=H/D.sqrt()
    cases={}
    for name,step,left,right,parts in [('breites_uhrfenster',wide,-R,R,2),('beide_pakethaelften',I.of(R),-R,F(0),16)]:
        cases[name]={mode:binary(mode,step,left,right,parts) for mode in ('gemeinsam','wirkungsquelle','festes_profil')}
    old=published_binary()
    assert list(map(F,old['P_plus_high_minus_low']))[0]<0
    reproduced=binary('wirkungsquelle',F(1,8)/D.sqrt(),-R,R,1)
    prev=list(map(F,old['P_plus_high_minus_low']))
    now=list(map(F,reproduced['P_plus_hoch_minus_niedrig']))
    assert prev[0]<=now[0]<=now[1]<=prev[1]<0
    bounds=aperture()
    trace=F(bounds['zero_pulse_trace_distance_upper'])
    contrast=-F(cases['breites_uhrfenster']['festes_profil']['P_plus_hoch_minus_niedrig'][1])
    assert 0<trace<contrast
    after={'max_erfolgsschance_kleinere_klasse_prozent':decimals(I.of(100*trace/contrast),10)[1],
           'mindestverhaeltnis_aktiver_kontrast_zu_passiver_spurdistanz':decimals(I.of(contrast/trace),3)[0]}
    return {'zwei_arme':cases,'h_1_8_referenz':reproduced,'fenster':bounds,'spaeter_filter':after,
            'drei_stellungen':{m:{name:ensemble(m,s) for s,name in [(-1,'niedrig'),(1,'hoch')]}
                               for m in ('gemeinsam','wirkungsquelle','festes_profil')},
            'rationale_kontrollen':exact_controls()}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
