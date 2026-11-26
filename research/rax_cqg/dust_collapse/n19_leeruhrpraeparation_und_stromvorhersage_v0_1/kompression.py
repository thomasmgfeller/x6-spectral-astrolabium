"""Cut-data reconstruction with the reference receiver clock as a single parameter."""
from fractions import Fraction as F
from zustand import nominal,gradients


def run(early,witness):
    from quelle import box,hull,SCALE
    from gemischt import COEFF,PAST,WINDOWS
    y,w=nominal(early)[1]
    G,_=gradients(y,w)
    c=[COEFF.get((i,4),0) for i in PAST]
    assert all(c==[COEFF.get((i,j),0) for i in PAST] for j in (4,5,6)) and sum(c)==0
    assert all(COEFF.get((i,j),0)==0 for j in (4,5,6) for i in y if i not in PAST)
    v=(19+sum(a*y[i]*y[i] for i,a in zip(PAST,c)))/(2*sum(a*y[i] for i,a in zip(PAST,c)))
    assert all((v-y[j]).contains_zero() for j in (4,5,6))
    u=y[15]; s=(u*u-6)/(2*(u+3))
    mz=-(u+3)
    K0=w[16]*(y[16]-u)
    wz=K0/(s-u)
    c0=w[1]*(y[1]-y[0])-9*w[2]*(y[2]-y[0])+16*w[3]*(y[3]-y[0])
    weight_sum=((c0-G[0])/8-wz*(s-y[0]))/(v-y[0])
    assert (weight_sum-sum(w[i] for i in (4,5,6))).contains_zero()
    c1=-w[1]*(y[1]-y[0])+w[2]*(y[2]-y[1])-9*w[3]*(y[3]-y[1])
    R=(c1+16*((v-y[1])*weight_sum+(s-y[1])*wz)-G[1])/8
    assert (R-w[18]*(y[18]-y[1])).contains_zero()

    def prediction(t,J):
        h=t-(8*(t+4)*(t+4)-16*(t+3)*(t+3)+9*(t-u)*(t-u)-(t-s)*(t-s)-19).sqrt()
        wr=R/(t-y[1])
        mr=-8*(t+4)+16*(t+3)-9*(t-u)+(t-s)+(t-h)
        d=box(J)/(2*mz)
        B=mr-d
        C=d*(d-2*(t-s))
        assert B.hi<0
        q=C/(-B+(B*B-C).sqrt())
        assert (-2*B-q).lo>(high-low)*SCALE
        return wz*d*(1+(s+d-u)/(s-h))+wr*q*(s+d-u)*(s+d-h)/(mz*(t+q-h))

    low,high=[x*F(23,6)-F(11,6) for x in WINDOWS[1]]
    n=128
    arms=[]
    family=witness['results']['all_momenta']['backgrounds']
    for k,J in enumerate((-F(1,10**6),F(1,10**6))):
        pieces=[prediction(hull(low+(high-low)*i/n,low+(high-low)*(i+1)/n),J) for i in range(n)]
        cover=pieces[0]
        for piece in pieces[1:]:
            cover=cover.union(piece)
        estimate=prediction(box((low+high)/2),J)
        residual=cover-estimate
        abs_err=F(max(abs(residual.lo),abs(residual.hi)),SCALE)
        assert not cover.contains_zero()
        min_abs=F(min(abs(cover.lo),abs(cover.hi)),SCALE)
        for member in family:
            expected=prediction(y[18]+F(member['parameter']),J)
            direct=hull(*member['pulses'][k]['from_full_continuation'])
            assert (expected-direct).contains_zero()
            assert cover.lo<=direct.lo<=direct.hi<=cover.hi
        arms.append({'Jw':str(J),'midpoint_prediction':estimate.data(),'uniform_enclosure':cover.data(),
                     'max_absolute_error':str(abs_err),'max_relative_error':str(abs_err/min_abs)})
    return {'fixed_nominal_clock_e':'1/6','receiver_window_Y':list(map(str,(low,high))),
            'intervals':n,'fixed_wR_times_t_minus_Y1':R.data(),'reference_G0':G[0].data(),
            'reference_G1':G[1].data(),'bounds':arms}
