"""Uniform enclosures for the original closure at event 13. No external dependencies."""
import json
import sys
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256

ROOT = Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'quellen'))
from intervalle import I, S
from ordnung import ORDER, pairs_from_intervals

EDGES=pairs_from_intervals()
K=F(15,4)
H=F(1,16384)
CENTRES={4:F(1,8),5:F(1,4),6:F(3,8),11:F(1,2),12:F(5,8),13:F(3,4),14:F(7,8)}
CLOSED=(4,5,6,12)


def box(a,b):
    return I(I.of(a).lo,I.of(b).hi)


def norm(a):
    return F(a.absmax(),S)


def upper(value,k):
    scale=10**k
    return str(F(-(-value*scale).__floor__(),scale))


def lower(value,k):
    scale=10**k
    return str(F((value*scale).__floor__(),scale))


def run():
    files=json.loads((ROOT/'herkunft.json').read_text())['files']
    for name,row in files.items():
        assert sha256((ROOT/'quellen'/name).read_bytes()).hexdigest()==row['sha256']
    p3=json.loads((ROOT/'quellen/p3.json').read_text())
    assert len(p3)==60 and all(row['checkpoint_id']=='P3' and row['execution']=='NOT_RUN' for row in p3)
    assert {j:b for (i,j),b in EDGES.items() if i==5 and ORDER.index(j)>ORDER.index(11)}=={12:16,13:-8}
    D=I.of(F(3,722)).sqrt().sqrt()*K
    radius=F((1/(72*D*K**2)+H).hi,S)
    u={j:box(t-F(1,64),t+F(1,64)) for j,t in CENTRES.items()}
    u[5]=box(CENTRES[5]-radius,CENTRES[5]+radius)
    u[6]=I.of(CENTRES[6])
    y={j:I.of(j-5) for j in range(4)}
    y[3]+=F(1,4)
    y.update({j:y[3]+K*u[j] for j in u})
    f={4:(u[4]+u[5])/2,5:(u[6]-u[4])/2,6:(u[11]-u[5])/2,
       12:(u[13]-u[11])/2,13:(u[14]-u[12])/2}
    for j in f:
        assert f[j].lo>0
    x13=f[13]*box(F(99,100),F(101,100))
    x12=f[12]*box(F(99,100),F(101,100))
    mid=box(F(255,2048)-H,F(257,2048)+H)
    tag_half=box(F(0),H)
    weights={**{j:f[j] for j in CLOSED},11:mid,13:x13}
    c={j:I.of(F(-1,2)) for j in weights}
    deriv={i:{j:I.of(0) for j in weights} for i in (4,5)}
    for (i,j),b in EDGES.items():
        if j not in c:
            continue
        gap=y[j]-y[i]
        c[j]-=gap**2*F(b,38)
        for k in deriv:
            deriv[k][j]-=gap*K*F(b,19)*(int(j==k)-int(i==k))
    df={4:{4:F(1,2),5:F(-1,2)},5:{4:F(1,2),6:F(-1,2)}}
    gradient={}
    rmax=F(0)
    for k in (4,5):
        phase=I.of(0)
        dlog=I.of(0)
        extra=F(0)
        for j,w in weights.items():
            dw=df[k].get(j,0)
            q=D*(w*deriv[k][j]+dw*c[j])
            phase+=q
            if j in CLOSED:
                dlog+=I.of(dw)/f[j]
                r=D*w*c[j]/100
                dr=q/100
            elif j==11:
                r=D*tag_half*c[j]
                dr=D*tag_half*deriv[k][j]
            else:
                continue
            rmax=max(rmax,norm(r))
            extra+=norm(r)*norm(dr)/(3*(1-norm(r)**2/6))
        gradient[k]=(norm(phase),norm(dlog)+extra)
    assert rmax<1
    # A reference vector common to both columns after coherent integration over u4.
    dz=gradient[4][0]/64
    q=sum(gradient[5])*radius
    assert dz<1 and q<1
    eta=q/(1-q)/(1-dz**2/2)
    real=1-2*eta-eta**2
    assert real>0
    r=F(I.of(1-(2*eta/(1-eta))**2).sqrt().lo,S)
    # Centre-angle difference from the two remaining edges; square differences are exact.
    gap=(16*x12*(u[12]-F(1,4))-8*x13*(u[13]-F(1,4)))/684
    assert gap.lo>0
    peak=(16*F(1,8)*(F(5,8)-F(1,4))-8*F(1,8)*(F(3,4)-F(1,4)))/684
    assert peak==F(1,2736)
    # Relative +/- pulse at the fixed output on the unresolved x12 fibre.
    lam=4*D*9*K*(u[12]-u[6])/(38*8*D.sqrt())
    phase_diameter=lam*2*f[12]/100
    assert lam.lo>0 and phase_diameter.hi<I.of(F(1,1000)).lo
    return dict(relative_pulse_frequency_abs=[lower(F(lam.lo,S),8),upper(F(lam.hi,S),8)],
                relative_pulse_phase_diameter_upper=upper(F(phase_diameter.hi,S),9),
                cut_after=13, P3_NOT_RUN=60, future_centre_gap_rad=str(peak),
                future_centre_gap_full_window_rad=[lower(F(gap.lo,S),9),upper(F(gap.hi,S),9)],
                max_sinc_argument=upper(rmax,8),theta_variation_in_u4=upper(dz,8),
                log_gradient_u5=upper(sum(gradient[5]),8),complex_disk_radius=upper(eta,9),
                relative_real_cross_lower=lower(real,9),inclusive_column_correlation_lower=lower(r,9),
                induced_gram_condition_normalized_columns_lower=lower((1+r)/(1-r),0),
                orthogonalizing_metric_condition_lower=lower((1+r)/(1-r),0))


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
