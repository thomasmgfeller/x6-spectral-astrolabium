"""Separate algebraic/numerical checks; no external independent audit implied."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import hashlib,json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.stats import binom
from model import coherence,positive_integral,momentum_integral,massless_closed_form
from gum import jacobian,correct_and_normalize,evaluate


def binomial_decimal(n,p,k,upper=False,precision=60):
    with localcontext() as c:
        c.prec=precision
        p=D(p);q=1-p;term=q**n;total=D(0)
        for j in range(n+1):
            if (j>k) if upper else (j<=k):total+=term
            if j<n:term=term*D(n-j)*p/(D(j+1)*q)
        return str(+total)


def preliminary():
    rows=[]
    for m in [0,.49,.5,.51]:
        for r in [0,1,2,3,3/.98,3/1.02]:
            positive=positive_integral(m,r)
            fourier=momentum_integral(m,r)
            assert abs(positive-fourier)<2e-12,(m,r,positive,fourier)
            assert momentum_integral(m,r,imaginary=True)==0
            rows.append({'mass':m,'distance':r,'positive':positive,'fourier':fourier,'absolute_difference':abs(positive-fourier)})
    for r in [0,.2,1,2,3,5]:
        assert abs(coherence(0,r)-massless_closed_form(r))<2e-13
    # A nonzero time separation produces a nonzero imaginary bidistribution.
    assert abs(momentum_integral(0,2,1,imaginary=True))>.001
    x=np.r_[[1.05,1.05,.84,1.05,1.05,.53,1.05,1.05,.28],[.05,.05,0.]]
    J=jacobian(x);num=np.zeros_like(J)
    for j in range(12):
        h=1e-5;dx=np.zeros(12);dx[j]=h
        num[:,j]=(correct_and_normalize(x+dx)-correct_and_normalize(x-dx))/(2*h)
    assert np.max(abs(J-num))<2e-9
    for bad in [np.zeros(12),np.r_[[1,1,2]*3,[0,0,0]]]:
        try:correct_and_normalize(bad)
        except ValueError:pass
        else:raise AssertionError('invalid domain accepted')
    assert evaluate([],[],mode='FIELD')['status']=='HOLD_FIELD_TRANSFER'
    return {'fourier_crosschecks':rows,'massless_closed_form_checks':6,
            'jacobian_maximum_difference':float(np.max(abs(J-num))),
            'invalid_domain_cases_rejected':2,'field_without_transfer':'HOLD_FIELD_TRANSFER'}


def check():
    result=preliminary()
    cert=json.loads(Path('records/certificate.json').read_text())
    checked=0
    for row in cert['settings']:
        r=row['distance_over_nominal_width']
        for i,mass in enumerate([0,.5]):
            lo,hi=map(float,row['models'][i]['rho_interval'])
            # Numerical grid is an additional diagnostic; the analytic monotonic
            # enclosure, not this grid, covers the continuous width interval.
            for width in np.linspace(.98,1.02,101):
                assert lo<=coherence(mass,r,width)<=hi
                checked+=1
    d=cert['decision'];n,k=d['pairs'],d['threshold']
    result['width_grid_diagnostics']=checked
    result['binomial_tail_checks']=[]
    for p,upper in [(d['p0_lower'],False),(d['p1_upper'],True)]:
        v50=binomial_decimal(n,p,k,upper,50)
        v70=binomial_decimal(n,p,k,upper,70)
        assert abs(D(v50)-D(v70))<D('1e-40')
        scipy_value=float(binom.sf(k,n,float(p)) if upper else binom.cdf(k,n,float(p)))
        assert abs(float(v70)-scipy_value)<2e-12
        result['binomial_tail_checks'].append({'probability':p,'upper_tail':upper,'decimal_70':v70,'scipy':scipy_value})
    # An elementary geometric proof of the arcsine law is in DERIVATION.md.
    # Cross-check its probability by an independent one-dimensional normal integral.
    from scipy.special import ndtr
    from math import exp,pi,sqrt,asin
    for correlation in [.2,.5,.85]:
        prob=2*quad(lambda x:exp(-x*x/2)/sqrt(2*pi)*ndtr(correlation*x/sqrt(1-correlation**2)),0,10,epsabs=1e-13)[0]
        assert abs(prob-(.5+asin(correlation)/pi))<2e-13
    result['orthant_integral_checks']=3
    for i in [0,1]:
        row=json.loads(Path(f'records/M{i}.json').read_text())
        arrays=[np.load(f'raw/M{i}_R{j}.npy',allow_pickle=False) for j in [1,2,3]]
        same=sum(int(x*y>=0) for x,y in arrays[2])
        assert same==row['same_sign_count_R3']
        u=np.array(row['gum']['input_covariance']);J=np.array(row['gum']['jacobian'])
        ref=np.array([[sum(J[a,k]*u[k,l]*J[b,l] for k in range(12) for l in range(12)) for b in range(3)] for a in range(3)])
        assert np.max(abs(ref-np.array(row['gum']['coherence_covariance_first_order'])))<1e-17
        assert np.linalg.eigvalsh(ref).min()>0
        assert row['gum']['joint_region']['validation_interval_contains_target']
        # With zero uncertainty in three shared calibrations, off-diagonal
        # coherence uncertainty is exactly zero for independent setting blocks.
        ua=u.copy();ua[9:,9:]=0
        independent=J@ua@J.T
        assert np.max(abs(independent-np.diag(np.diag(independent))))<1e-18
    controls=json.loads(Path('records/controls.json').read_text())
    assert controls['identical_model_status']=='HOLD_IDENTIFIABILITY'
    assert controls['single_setting_width_alias_massless_width']<.98
    assert all(x['minimum_noise_eigenvalue']>0 for x in controls['noise_alias'])
    result['status']='PASS_SCOPED_NUMERICAL_AND_ALGEBRAIC_CONTROLS'
    result['external_reproduction']=False
    Path('records/check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'])


if __name__=='__main__':check()
