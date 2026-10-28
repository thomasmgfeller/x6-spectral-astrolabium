"""Exactly soluble random-frequency oscillator with correlated Cauchy data."""
from flint import arb,acb
from kernel import require


def average(sign,lo,hi):
    s=arb(sign);w=(1+s/4).sqrt();f=1+s/5;g=s/10
    return (f*((w*hi).sin()-(w*lo).sin())/w+g*((w*lo).cos()-(w*hi).cos())/(w*w))/(hi-lo)


def predict():
    rows=[];sigma=arb(1)/4;kappa=arb(1)/5;gamma=arb(1)/10
    for lo,hi in [('7/4','2'),('2','9/4')]:
        a,b=arb(lo),arb(hi);dt=b-a
        plus,minus=average(1,a,b),average(-1,a,b)
        mu=(plus+minus)/2;spread=(plus-minus)/2
        base=(b.sin()-a.sin())/dt
        linear=kappa*base+gamma*(a.cos()-b.cos())/dt-sigma/(2*dt)*(-b*b.cos()+b.sin()+a*a.cos()-a.sin())
        def quadratic(t,analytic):
            return sigma*sigma*(t*t.sin()-t*t*t.cos())/8-kappa*sigma*t*t.sin()/2+gamma*sigma*(t*t.cos()-t.sin())/2
        second=acb.integral(quadratic,acb(a),acb(b),abs_tol=arb('1e-25'),rel_tol=arb('1e-25')).real/dt
        x=sigma.sqrt()*b
        rem1=x.cosh()-1-sigma*b*b/2+kappa*(x.cosh()-1)+gamma*(x.sinh()/sigma.sqrt()-b)
        rem2=x.cosh()-1-sigma*b*b/2-sigma*sigma*b**4/24+kappa*(x.cosh()-1-sigma*b*b/2)+gamma*(x.sinh()/sigma.sqrt()-b-sigma*b**3/6)
        for sign,val in [(1,plus),(-1,minus)]:
            require((val-base-sign*linear).abs_upper()<=rem1,'oscillator linear remainder')
            require((val-base-sign*linear-second).abs_upper()<=rem2,'oscillator quadratic remainder')
        require((mu-base-second).abs_upper()<=rem2,'oscillator mean second-order remainder')
        rows.append({'shifted_window':[lo,hi],'plus':plus,'minus':minus,'mean':mu,'half_difference':spread,
                     'frozen_mean':base,'mean_shift':mu-base,'linear_coefficient':linear,'quadratic_mean_correction':second,
                     'linear_remainder_upper':rem1,'quadratic_remainder_upper':rem2})
    C=[[r['half_difference']*s['half_difference'] for s in rows] for r in rows]
    Cl=[[r['linear_coefficient']*s['linear_coefficient'] for s in rows] for r in rows]
    bounds=[[r['linear_coefficient'].abs_upper()*s['linear_remainder_upper']+s['linear_coefficient'].abs_upper()*r['linear_remainder_upper']+r['linear_remainder_upper']*s['linear_remainder_upper'] for s in rows] for r in rows]
    for i in range(2):
        for j in range(2):require((C[i][j]-Cl[i][j]).abs_upper()<=bounds[i][j],'oscillator covariance remainder')
    return {'windows':rows,'covariance':C,'relation':C,'linear_covariance':Cl,'linear_covariance_error_upper':bounds,
            'law':'xi=-1,+1 equiprobable; omega^2=1+xi/4, f=1+xi/5, g=xi/10; exact window averages'}
