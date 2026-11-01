"""Exact rational support/separation certificate; numerical risk is supplementary."""
from fractions import Fraction as F
import json,math
from pathlib import Path


def certificate():
    mlo,mhi=F(49,100),F(51,100)
    tlo,thi=F(198,100),F(202,100)
    rlo,rhi=F(99,100),F(101,100)
    ahi,bhi=F(255,1000),F(102,1000)
    future_margin=tlo-2*bhi-rhi-2*ahi
    z2max=mhi*mhi*((thi+2*bhi)**2-(rlo-2*ahi)**2)
    # 2 J1(z)/z = sum (-z^2/4)^k/(k!(k+1)!). For z^2<8,
    # alternating terms decrease, giving 1-z^2/8 <= 2J1(z)/z <= 1.
    assert future_margin>0 and 0<z2max<8 and rlo>2*ahi
    lower=mlo*mlo*(1-z2max/8)/(8*F(22,7))
    upper=mhi*mhi/(8*F(333,106))
    claimed=F(8,1000)
    assert lower>claimed
    gap=F(99,100)*claimed-2*F(5,10000)
    n=2048;sigma=F(5,100)
    exponent=F(n)*gap*gap/(8*sigma*sigma)
    # exp(exponent)>100 by an exact finite lower Taylor sum.
    partial=sum((exponent**k/F(math.factorial(k)) for k in range(25)),F(0))
    assert partial>100
    return dict(status='PASS_CONDITIONAL_RATIONAL_CERTIFICATE',
        future_support_margin=str(future_margin),zmax_squared=str(z2max),
        negative_response_magnitude_lower_rational=str(lower),
        negative_response_magnitude_upper_rational=str(upper),
        lower=float(lower),upper=float(upper),claimed_lower=float(claimed),
        raw_mean_M0_lower=-.0005,raw_mean_M1_upper=-.00742,
        separation_gap=float(gap),decision_threshold=-.00396,blocks=n,
        block_sd_upper=float(sigma),error_bound_each=math.exp(-float(exponent)),
        proof_exp_lower_sum_over_100=str(partial>100),
        status_field='HOLD_FIELD_TRANSFER')


if __name__=='__main__':
    out=certificate();Path('records').mkdir(exist_ok=True)
    Path('records/certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
