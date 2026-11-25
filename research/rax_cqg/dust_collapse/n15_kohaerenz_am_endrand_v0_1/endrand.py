"""Certified boundary rays from the retarded N15 dust action."""
from fractions import Fraction as F
from pathlib import Path
from math import isqrt
import json
import sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'basis'))
from rechnung import (I,S,D,K,R,H,EPS,Q0,ZERO,ONE,cell,coeffs,
                      EDGES,INNER,ORDER,decimals,hull,sin_box)
from versuch import FUTURE,ETA
from intervalle import sinc,cis,C

MID={i:F(-7,4)+K*F(k,8) for k,i in enumerate(INNER,1)}
END={j:F(j-5) for j in FUTURE}
CROSS=[(i,j,b) for (i,j),b in EDGES.items() if i in INNER and j in FUTURE]
SIGNS=dict(zip(INNER,(1,-1,1,-1,1,-1,1)))


def mag(x):
    return F(I.of(x).absmax(),S)


def radius(x):
    return F(x.hi-x.lo,2*S)


def upper(x):
    return F(I.of(x).hi,S)


def bounds(x,n=17):
    return decimals(I.of(x),n)


def phase_at_center(kind,side,w0,lobe,bran,open_clocks=False):
    t=H/D.sqrt()
    move=(t if kind=='single' and bran else ZERO)
    y,n,_,x,_,_,_,qs,_=cell(lobe,move-R,move+R)
    if not open_clocks:
        y.update({j:I.of(END[j]) for j in FUTURE})
    if kind=='collective' and bran:
        y.update({i:y[i]+SIGNS[i]*t for i in INNER})
    full=coeffs(y)
    return sum(D*(x[i]+(side*EPS*Q0*n[i]/qs if i in (12,13,14) else 0))*full[i]
               for i in INNER) + sum(w0*full[j] for j in FUTURE)


def model_shift(kind,bran):
    t=H/D.sqrt()
    return {i:(SIGNS[i]*t if kind=='collective' and bran else ZERO) for i in MID}


def gradients(kind):
    s=model_shift(kind,1)
    beta={j:ZERO for j in FUTURE}
    velocity={j:ZERO for j in FUTURE}
    for i,j,b in CROSS:
        beta[j]+=F(b,38)*s[i]*(2*(END[j]-MID[i])-s[i])
        velocity[j]+=F(b,19)*s[i]
    return beta,velocity


def packet_error(shift,w0,width,u):
    # Uniform bound on the double difference in the late phase with respect
    # to internal clock jitter and output displacement from its center.
    total=F(0)
    for i,j,b in CROSS:
        k=(u if j!=7 else 0)
        gap=mag(END[j]-MID[i]-shift[i])
        total+=F(abs(b),38)*(width*(2*gap*R+R**2)+2*(w0+width)*k*R)
    return total


def limited(x):
    return I(max(0,x.lo),min(S,x.hi))


def domain(kind,wide):
    w0,width=(F(1,2),F(1,2)) if wide else (F(1,8),ETA)
    beta,velocity=gradients(kind)
    cosmean=ONE
    span=ZERO
    nonlinear=F(0)
    for j in FUTURE:
        cosmean*=sinc(beta[j]*width)
        k=ETA if j!=7 else 0
        cosmean*=sinc(velocity[j]*(w0*k))
        span+=mag(beta[j])*width + mag(velocity[j])*w0*k
        nonlinear+=mag(velocity[j])*k*width
    opt=limited(ONE-cosmean**2).sqrt()
    best=max(FUTURE,key=lambda j:mag(beta[j]))
    # Midpoint phase compensation, followed by the same +/- i interference
    # between the two halves of a single end-density coordinate.
    detector=sin_box(I.of(mag(beta[best]))*width/2)
    # For each pulse-pair measurement the error from approximating the two
    # physical rays is at most the sum of their trace distance errors.
    rows={}
    for side in (-1,1):
        phases=[[phase_at_center(kind,side,w0,l,b) for l in (-1,1)] for b in (0,1)]
        masses=[1-radius(hull(block))**2/2 for block in phases]
        assert min(masses)>F(99,100)
        eps=[packet_error(model_shift(kind,b),w0,width,ETA)/m for b,m in enumerate(masses)]
        # ||F-1||_2 <= eps for each dephased, center-normalized ray.
        # Its distance to the ideal ray is at most eps/(1-eps).
        shape_error=sum(e/(1-e) for e in eps)
        ray_error=shape_error+nonlinear
        upper_T=min(ONE.hi,(opt+ray_error).hi)
        lower_T=max(0,(opt-ray_error).lo)
        anyweight=min(F(1),upper(span*sinc(span))+ray_error)
        if kind=='single':
            assert all(b.lo==b.hi==0 for b in beta.values())
            # Both arms have the same spectator jitter and boundary carrier.
            pair_delta=radius(hull([phases[1][k]-phases[0][k] for k in (0,1)]))
            raw=packet_error(model_shift(kind,0),w0,width,ETA)
            anchored=raw*pair_delta*(1+1/masses[0])/masses[1]
            anyweight=min(anyweight,anchored/(1-eps[1]))
            upper_T=min(upper_T,I.of(anyweight).hi)
        T=I(lower_T,upper_T)
        assert T.hi<S
        # The ideal linear phase is pure. Only its real coordinate-space
        # modulus is used in the direct coordinate readout.
        direct=min(shape_error,upper(T),anyweight)
        coeff_sqrt=limited(limited(ONE-T**2).sqrt())
        rows[str(side)]={'trace_distance':bounds(T,21),'accuracy_percent':bounds(50*(ONE+T),15),
                        'one_density_detector_coordinate':best,
                        'one_density_accuracy_percent_lower':bounds(50*(ONE+detector-ray_error),13)[0] if kind=='collective' else '50',
                        'coordinate_only_accuracy_percent_upper':bounds(50*(1+I.of(direct)),13)[1],
                        'arbitrary_common_weight_accuracy_percent_upper':bounds(50*(1+I.of(anyweight)),13)[1],
                        'overlap_modulus':bounds(coeff_sqrt,22),'packet_ray_error_sum_upper':bounds(shape_error,20)[1],
                        'reference_mass_lower':bounds(min(masses),13)[0]}
    return rows


def sign_moment(x):
    return x*sinc(x/2)**2/2


def det3(m):
    a,b,c=m
    return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])
            +a[2]*(b[0]*c[1]-b[1]*c[0]))


def joint_readout(name,side):
    w0=F(1,2) if name=='wide_control' else F(1,8)
    if name=='same_center_8_9':
        widths={j:(F(1,8) if j in (8,9) else ETA) for j in FUTURE}
    else:
        widths={j:(F(1,2) if name=='wide_control' else ETA) for j in FUTURE}
    beta,velocity=gradients('collective')
    rr=I(-I.of(R).hi,I.of(R).hi)
    clock=I(-I.of(ETA).hi,I.of(ETA).hi)
    err={}
    for b in (0,1):
        shift=model_shift('collective',b)
        err[b]={j:ZERO for j in FUTURE}
        for i,j,bond in CROSS:
            z=END[j]+(clock if j!=7 else ZERO)
            err[b][j]+=F(bond,38)*rr*(2*(z-MID[i]-shift[i])-rr)
    phases=[[phase_at_center('collective',side,w0,l,b,True) for l in (-1,1)] for b in (0,1)]

    def stats(a,b):
        # Fourier half-range integrals of 1, sign(h8), sign(h8)*sign(h9).
        signed=[ONE,ONE,-ONE]
        for j in FUTURE:
            mid=(b-a)*(beta[j]+(velocity[j]*clock if j!=7 else ZERO))
            arg=widths[j]*(mid+err[b][j]-err[a][j])
            co,si=sinc(arg),sign_moment(arg)
            signed[0]*=co
            signed[1]*=si if j==8 else co
            signed[2]*=si if j in (8,9) else co
        phase=sum((cis(y-x) for x in phases[a] for y in phases[b]),C(0)).scale(F(1,4))
        return [phase.scale(signed[0]),(C(0,1)*phase).scale(signed[1]),phase.scale(signed[2])]

    ll,rr_=stats(0,0),stats(1,1)
    cross=stats(0,1)
    matrix=[[(l.re+r.re)/2,z.re,-z.im] for l,r,z in zip(ll,rr_,cross)]
    determinant=det3(matrix)
    assert determinant.lo>0 or determinant.hi<0
    diag,re,_=matrix[0]
    diag_s,re_s,_=matrix[2]
    assert diag.lo>0 and re.lo>0
    pm_bias=diag_s/(2*diag)
    pc_bias=(diag_s+re_s)/(2*(diag+re))
    diff=(re_s-(diag_s/diag)*re)/(2*(diag+re))
    assert diff.lo>0
    separation=F(pc_bias.lo-pm_bias.hi,S)
    assert separation>0
    n=6/separation**2
    sufficient=-(-n.numerator//n.denominator)
    return {'sufficient_independent_accepted_events_5pct_known_class':sufficient,
            'coherent_probability_minus_half':bounds(pc_bias,25),
            'mixture_probability_minus_half':bounds(pm_bias,25),
            'coherent_minus_mixture_probability':bounds(diff,25),
            'coherent_probability_percent':bounds(100*(F(1,2)+pc_bias),16),
            'mixture_probability_percent':bounds(100*(F(1,2)+pm_bias),16),
            'tomography_matrix':[[bounds(x,29) for x in row] for row in matrix],
            'tomography_determinant':bounds(determinant,34)}


def rational_checks():
    last=(11,12,13,14)
    assert len(CROSS)==10 and tuple(FUTURE)==(7,8,9,10)
    for k,j in enumerate(FUTURE):
        assert set(i for i,jj,b in CROSS if jj==j)==set(last[k:])
        assert EDGES[last[k],j]==-8
    samples=[{i:MID[i]+F(k*(i%4-2),2**20) for i in last} for k in range(-6,7)]
    def inverse(y):
        c={j:-sum(F(b,38)*(END[j]-y[i])**2 for i,jj,b in CROSS if jj==j) for j in FUTURE}
        back={}
        for i,j in reversed(list(zip(last,FUTURE))):
            other=sum(F(b,38)*(END[j]-back[h])**2 for h,jj,b in CROSS if jj==j and h!=i)
            sq=(c[j]+other)*F(38,8)
            nr,dr=isqrt(sq.numerator),isqrt(sq.denominator)
            assert nr*nr==sq.numerator and dr*dr==sq.denominator
            back[i]=END[j]-F(nr,dr)
        assert back==y
    for sample in samples:inverse(sample)
    h=F(1,2**24)
    # Only Y11 moves. Its coefficient C7 spans all five test frequencies.
    gap=END[7]-MID[11]
    freq_margin=F(8,38)*(2*gap*R-R**2)
    assert 2*h<freq_margin
    return {'inverse_round_trip_profiles':len(samples),'verified_cross_edges':len(CROSS),
            'fourth_difference_frequency_step':str(h),'fourth_difference_uniform_amplitude_upper':bounds(2*(h/2)**4,40)[1]}


def run():
    beta,vel=gradients('collective')
    return {'geometry':rational_checks(),
            'joint_readout':{name:{str(side):joint_readout(name,side) for side in (-1,1)}
                             for name in ('published','same_center_8_9','wide_control')},
            'collective_phase_density_slopes':{str(j):bounds(beta[j],16) for j in FUTURE},
            'collective_phase_mixed_slopes':{str(j):bounds(vel[j],16) for j in FUTURE},
            'distinguishability':{kind:{name:domain(kind,wide) for name,wide in (('published',False),('wide_control',True))}
                                  for kind in ('single','collective')}}


if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))
