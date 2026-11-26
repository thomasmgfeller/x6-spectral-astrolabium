"""Common positive-oscillator preparation, classical coverage and canonical area."""
from fractions import Fraction as F
from ensemble import B,V,FOCUS


def exp_minus_bounds(x,terms=48):
    total=F(1);term=F(1)
    for i in range(1,terms+1):
        term*=x/i
        total+=term
    first=term*x/(terms+1)
    rem=first/(1-x/(terms+2))
    assert x<terms+2
    return 1/(total+rem),1/total


def run():
    from quelle import box
    from wege import topology
    c=FOCUS*V/B
    assert c==F(5,2)
    rad=box(c*c+4).sqrt()
    z=(rad+c)/2
    # Two quarter turns with positive oscillator impedances give
    # -diag(z,1/z). Then rotate clockwise by theta.
    cs=((1+c/rad)/2).sqrt()
    sn=((1-c/rad)/2).sqrt()
    large=z*z
    small=1/large
    cov=(cs*cs*large+sn*sn*small,cs*sn*(small-large),sn*sn*large+cs*cs*small)
    assert all((v-n).contains_zero() for v,n in zip(cov,(1+c*c,-c,1)))
    assert (1+c*c)-c*c==1
    qlo,qhi=exp_minus_bounds(F(9,2))
    cover=[(1-qhi)**3,(1-qlo)**3]
    assert cover[0]>F(966,1000)
    scales=[]
    for k in (F(1),F(1,10**11)):
        # Physical canonical momentum in units of the model action.
        variance_q=(B*B+(FOCUS*V)**2)/9
        variance_P=(2*k*V)**2/9
        cov_qP=-2*k*FOCUS*V**2/9
        det=variance_q*variance_P-cov_qP*cov_qP
        emittance=2*k*B*V/9
        assert det==emittance**2 and det>0
        scales.append({'k':str(k),'hard_impulse_support':str(k*V),'rms_half_momentum':str(k*V/3),
                       'ellipse_area_over_pi':str(2*k*B*V),'gaussian_covariance_q_qP_PP':list(map(str,(variance_q,cov_qP,variance_P))),
                       'sqrt_covariance_determinant':str(emittance),'max_hbar_effective_for_this_gaussian':str(2*emittance)})
    return {'order':topology(),'unit_oscillator_map':{'c':str(c),'impedance':z.data(),'cos_theta':cs.data(),
            'sin_theta':sn.data(),'target_covariance_times_nine':list(map(str,(1+c*c,-c,1)))},
            'gaussian_joint_capture_lower_upper':list(map(str,cover)),'canonical':scales}
