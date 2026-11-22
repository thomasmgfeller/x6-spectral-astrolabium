"""Certified intensity asymmetry at M=1 on the full broad seven-clock box."""
from fractions import Fraction as F
from randquelle import DELTA,EDGES,ETA,H,INNER,PAST,FUTURE,ORDER,RADIUS
from modell import clocks,dwell,INNER_MEANS
from intervalle import I,S
from phase359 import box,up,absup,real_interval,cos_lower

def phase_cell(e,rho,sign,alpha):
    length=4-e;D=DELTA*length;t=sign*H/D.sqrt()
    f0=dwell(INNER_MEANS)
    centres={j:I.of(f0[j]) for j in INNER}
    centres[11]-=alpha*DELTA*t/(2*D)
    y=clocks(e,[I.of(v) for v in INNER_MEANS])
    weights={**dict.fromkeys(PAST,I.of(rho)),**dict.fromkeys(FUTURE,I.of(F(1,8))),
             **{j:D*centres[j] for j in INNER}}
    c=dict.fromkeys(ORDER,I.of(F(-1,2)))
    derivative=dict.fromkeys(INNER,I.of(0))
    change=dict.fromkeys(ORDER,F(0));rest=F(0)
    for (i,j),b in EDGES.items():
        gap=I.of(y[j]-y[i])-(t if i==6 and j in (12,13,14) else 0)
        k=F(-b,38);c[j]+=k*gap**2
        width=up(length)*RADIUS*(int(i in INNER)+int(j in INNER))
        change[j]+=abs(k)*(2*absup(gap)*width+width**2)
        rest+=abs(k)*absup(weights[j])*width**2
        slope=2*k*weights[j]*gap*length
        if j in INNER:derivative[j]+=slope
        if i in INNER:derivative[i]-=slope
    for idx,j in enumerate(INNER):
        if idx<len(INNER)-1:
            for v in (idx,idx+1):derivative[INNER[v]]+=D*c[j]/2
        if idx>0:
            for v in (idx-1,idx):derivative[INNER[v]]-=D*c[j]/2
    mid=sum((weights[j]*c[j] for j in ORDER),I.of(0))
    radius=RADIUS*sum(absup(v) for v in derivative.values())+rest+up(D)*RADIUS*sum(change[j] for j in INNER)
    angles=mid+box(-radius,radius)
    p=sum((c[j] for j in PAST),I.of(0))
    assert all(change[j]==0 for j in PAST)
    squared=(absup(p)/32)**2
    for j in INNER:
        z=up(D)*(up(centres[j])+RADIUS)*ETA*(absup(c[j])+change[j])
        squared+=z*z
    assert squared<1
    attenuation=I.of(1-squared/6)
    f11=box(f0[11]-RADIUS,f0[11]+RADIUS)
    volume=1-alpha*DELTA*t/(2*D*f11)
    return angles,attenuation,volume

def amplitudenbetrag(rho,sign,alpha,n=64):
    cells=[]
    for mid in (-F(1,16),F(1,16)):
        for k in range(n):
            a=mid-F(1,32)+F(k,16*n)
            cells.append(phase_cell(box(a,a+F(1,16*n))/DELTA,rho,sign,alpha))
    full=real_interval([x[0] for x in cells])
    direction=I.of(F(full.lo+full.hi,2*S))
    floors=[I.of(cos_lower(v-direction))*atten*vol for v,atten,vol in cells]
    bound=I(min(v.lo for v in floors),max(v.hi for _,_,v in cells))
    assert bound.lo>0
    return bound

def endpoints(r):
    return (F(r.lo,S),F(r.hi,S))

def run():
    result={};safe_lo=[];safe_hi=[]
    for rho in (F(1,8),F(1,4)):
        ratios={}
        for alpha in (0,1):
            minus=amplitudenbetrag(rho,-1,alpha);plus=amplitudenbetrag(rho,1,alpha)
            ratio=(minus/plus)**2
            l,u=endpoints(ratio)
            asym=box((l-1)/(l+1),(u-1)/(u+1))
            assert (asym.hi<F(1,10)*S if alpha==0 else asym.lo>F(1,10)*S)
            result[f'{rho}|{alpha}']={'betrag_minus':minus.rounded(10),'betrag_plus':plus.rounded(10),
                'intensitaetsverhaeltnis':ratio.rounded(10),'asymmetrie':asym.rounded(10)}
            ratios[alpha]=ratio
        safe_lo.append(F(11,9)/endpoints(ratios[1])[0]);safe_hi.append(F(11,9)/endpoints(ratios[0])[1])
    # Round allowable gain range inward; it is sufficient, not a necessary bound.
    result['zulaessige_relative_intensitaetsverstaerkung_offen']=[
        I.of(max(safe_lo)).rounded(8)[1],I.of(min(safe_hi)).rounded(8)[0]]
    return result

if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2,sort_keys=True))
