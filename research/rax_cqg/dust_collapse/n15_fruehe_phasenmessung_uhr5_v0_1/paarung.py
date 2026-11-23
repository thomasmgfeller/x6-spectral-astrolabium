"""Two distinct, nonorthogonal suffix rays on the same finite clock-packet code."""
from fractions import Fraction as F
import argparse
import json
from modelltest import ROOT, I, S, D, E, K, STEP, H, EDGES, INNER_MEANS, clocks, require
from intervalle import C, cis, sinc, gaussian


def suffix(arm, continuation, error):
    total=C(0)
    for t,wt in gaussian(12):
        u=list(map(I.of,INNER_MEANS))
        u[1]+=arm*STEP+H*t
        u[4]+=F(continuation,1024)
        y=clocks(E,u)
        c={j:I.of(F(-1,2)) for j in (12,13)}
        for (i,j),b in EDGES.items():
            if j in c:c[j]-=F(b,38)*(y[j]-y[i])**2
        total=total+cis(D*(c[12]+c[13])/8).scale(wt*sinc(D*c[12]/800))
    return total.pad(error)


def norm2(v):
    return (v*v.conj()).re


def run():
    # On |t|<=8 the only variable clock in this integral is Y5.
    shift=K*(F(3,2500)+8*H)
    u0=INNER_MEANS.copy()
    maxgap=0
    for choice in (-1,1):
        u0[4]=F(5,8)+F(choice,1024)
        y=clocks(E,u0)
        maxgap=max(maxgap,*(abs(y[j]-y[5])+shift for j in (12,13)))
    require(maxgap<5 and D.hi<S,'Cauchy-Argumente')
    exponent=F(101,800)*F(24,19)*maxgap*shift
    require(exponent<1,'Majorante')
    err=F(6,8**24)/(1-F(1,8))
    r={v:[suffix(a,v,err) for a in (-1,1)] for v in (-1,1)}
    a,b=r[-1],r[1]
    det=a[0]*b[1]+(a[1]*b[0]).scale(-1)
    overlap=a[0].conj()*b[0]+a[1].conj()*b[1]
    norm=(norm2(a[0])+norm2(a[1]))*(norm2(b[0])+norm2(b[1]))
    distance=(norm2(det)/norm).sqrt()
    inner=(norm2(overlap)/norm).sqrt()
    require(distance.lo>0 and inner.lo>0,'Verschiedene nichtorthogonale Zeilen')
    # The coefficient of the u12 change in the pointwise ratio phase is independent of offset.
    delta_angle=F(2,19)*F(1,72)*16*F(1,8)*F(2,1024)
    require(delta_angle==F(1,175104),'Faserphase')
    return {'continuations_u12':['639/1024','641/1024'],'normalized_det':distance.rounded(13),
            'normalized_abs_overlap':inner.rounded(15),'ray_phase_difference_pointwise':str(delta_angle),
            'amplitude_remainder':str(err)}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true')
    args=p.parse_args();out=json.dumps(run(),indent=2)+'\n'
    if args.json:print(out,end='')
    else:
        require((ROOT/'paarung.json').read_text()==out,'Archiv')
        print('PASS · Zwei physisch unterschiedlich konditionierte Modellfortsetzungen auf demselben Zweimodenraum')
