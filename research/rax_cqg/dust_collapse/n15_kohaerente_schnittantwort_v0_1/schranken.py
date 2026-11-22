"""Outward enclosures for a paired, coherent difference without subtracting close integrals."""
from fractions import Fraction as F
from modell import (ORDER,INNER,PAST,FUTURE,EDGES,EPS,H,NARROW,INNER_MEANS,PACKET_MEANS,clocks,dwell,link_change)
from intervalle import I,S

DELTA=I.of(F(3,722)).sqrt().sqrt()

def box(a,b):return I(I.of(a).lo,I.of(b).hi)

def up(x):return F(x.hi,S)

def absup(x):return F(x.absmax(),S)

def real_interval(vals):return I(min(x.lo for x in vals),max(x.hi for x in vals))

def phase(e,means,r,rho,step,jitter):
    """Enclose the clock dependence around central clock coordinates at fixed e.

    Integrate independent uniform density jitters analytically. The centre phase is real.
    First-order clock terms are collected before taking absolute values.
    """
    length=4-e; D=DELTA*length; y=clocks(e,list(map(I.of,means))); f=dwell(list(map(F,means)))
    t=I.of(step)/D.sqrt(); wr=dict.fromkeys(FUTURE,I.of(F(1,8)));wr.update(dict.fromkeys(PAST,I.of(rho)));wr.update({j:D*f[j] for j in INNER})
    coef={j:I.of(F(-1,2)) for j in ORDER};lin={i:I.of(0) for i in INNER};variation=dict.fromkeys(ORDER,F(0));quadr=F(0)
    for (i,j),b in EDGES.items():
        gap=I.of(y[j]-y[i])-(t if (i,j)==(4,12) else 0)
        k=F(-b,38); coef[j]+=k*gap**2
        dr=up(length)*r*(int(i in INNER)+int(j in INNER))
        variation[j]+=abs(k)*(2*absup(gap)*dr+dr**2)
        quadr+=abs(k)*absup(wr[j])*dr**2
        v=2*k*wr[j]*gap*length
        if j in INNER:lin[j]+=v
        if i in INNER:lin[i]-=v
    # Derivative of the dwell fractions at fixed D. End cells have a fixed outside face.
    for m,j in enumerate(INNER):
        for q in ((m,m+1) if m<6 else ()):
            lin[INNER[q]]+=D*coef[j]/2
        for q in ((m-1,m) if m>0 else ()):
            lin[INNER[q]]-=D*coef[j]/2
    centre=sum((wr[j]*coef[j] for j in ORDER),I.of(0))
    radius=r*sum(absup(v) for v in lin.values())+quadr+up(D)*r*sum(variation[j] for j in INNER)
    hull=centre+box(-radius,radius)
    # sinc(z)>=1-z²/6; product of numbers >=1-e_i is >=1-sum e_i, for sum e_i<1.
    past=sum((coef[j] for j in PAST),I.of(0)); assert not any(variation[j] for j in PAST)
    errors=(absup(past)/32)**2
    for j in INNER:
        amp=up(D)*(f[j]+r)*jitter*(absup(coef[j])+variation[j]);errors+=amp**2
    assert errors<F(6)
    return hull,box(1-errors/6,1)

def beta(e,step):
    length=4-e;D=DELTA*length;u={j:box(m-NARROW,m+NARROW) for j,m in zip(INNER,PACKET_MEANS)}
    c=I.of(F(-1,2))
    for (i,j),b in EDGES.items():
        if j==13:
            assert i in INNER
            c-=F(b,38)*length**2*(u[j]-u[i])**2
    gap=length*(u[12]-u[4]);return D*EPS*c*link_change(gap,I.of(step)/D.sqrt())

def cos_lower(x):
    # Actual differences are small. Alternating Taylor lower bound through degree 6.
    z=absup(x); assert z<2
    return 1-z*z/2+z**4/24-z**6/720

def reference_cells(rho,n=64):
    for m in (-F(1,16),F(1,16)):
        for k in range(n):
            a=m-F(1,32)+F(k,16*n);e=box(a,a+F(1,16*n))/DELTA
            yield phase(e,INNER_MEANS,F(1,64),rho,0,F(1,100))

def serial(x):return x.rounded(12)

def certify():
    e=box(F(1,4)-NARROW,F(1,4)+NARROW);result={}
    for rho in (F(1,8),F(1,4)):
        refs=list(reference_cells(rho));null=phase(e,PACKET_MEANS,NARROW,rho,0,F(1,500))
        group={}
        for step in (H,-H):
            centre,ap=phase(e,PACKET_MEANS,NARROW,rho,step,F(1,500));b=beta(e,step);bs=b if step>0 else -b
            assert 0<bs.lo<=bs.hi<S//10
            sn=I.of(1)*box(F(bs.lo,S)*(1-absup(bs)**2/6),up(bs))
            def factor(ref):
                hull,atten=ref; c=cos_lower(centre-hull);assert c>0
                return I.of(c)*ap*atten
            broad=min(F(factor(v).lo,S) for v in refs);narrow=F(factor(null).lo,S)
            positive=sn*box((broad+narrow)/2,1)
            amount=positive if step>0 else -positive
            group['+' if step>0 else '-']={'phase_mid_packet':serial(centre),'beta':serial(b),'delta_R_minus_pi_over_2':serial(amount),'narrow_cos_atten_lower':str(I.of(narrow).rounded(8)[0]),'broad_cos_atten_lower':str(I.of(broad).rounded(8)[0])}
        result[str(rho)]={'broad_null_phase_full_hull':serial(real_interval([h for h,_ in refs])),'narrow_null_phase':serial(null[0]),'directions':group}
    return result

if __name__=='__main__':
    import json
    print(json.dumps(certify(),indent=2,sort_keys=True))
