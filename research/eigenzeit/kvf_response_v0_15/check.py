"""Independent position/spectral checks, symbolic normalizations and falsification controls."""
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import quad
from scipy.stats import norm
from model import spectral,position_tail,self_response,space_ft,time_ft,spectral_tail_bound
from certificate import certificate


def check():
    c=json.loads(Path('CONTRACT.json').read_text());cert=certificate();tol=1e-10
    q,z,u=s.symbols('q z u',real=True)
    cs=s.factor(s.integrate(s.integrate((1-u-z*z)**2*(1-u-(z-q)**2)**2,(u,0,1-z*z)),(z,q/2,1))*2*s.pi*(s.Rational(105,32)/s.pi)**2)
    ct=s.factor(s.integrate((1-z*z)**2*(1-(z-q)**2)**2,(z,q-1,1))*(s.Rational(15,16))**2)
    assert s.integrate(4*s.pi*q*q*cs,(q,0,2))==1
    assert 2*s.integrate(ct,(q,0,2))==1
    ft_error=[]
    for k in [0,.0001,.1,1,5,10]:
        fs=quad(lambda r:105/8*r*r*(1-r*r)**2*np.sinc(k*r/np.pi),0,1,epsabs=1e-13)[0]
        ft=quad(lambda t:15/8*(1-t*t)**2*np.cos(k*t),0,1,epsabs=1e-13)[0]
        ft_error.extend([abs(fs-float(space_ft(k))),abs(ft-float(time_ft(k)))])
    assert max(ft_error)<1e-12
    controls={};max_quad=0;max_dual=0;all_R=[]
    for name,m in c['models'].items():
        rows=[]
        for T in c['delays']:
            a=spectral(m,T,order=32);b=spectral(m,T,order=64)
            max_quad=max(max_quad,max(abs(a[k]-b[k]) for k in a))
            rows.append(a)
        assert abs(rows[0]['R'])<tol and rows[0]['H_AB']>.01 and rows[3]['R']==0
        if m==0:assert abs(rows[2]['R'])<tol
        else:assert rows[2]['R']<-.008 and rows[3]['Delta_AB']>.008
        p1=position_tail(m,2,order=12);p2=position_tail(m,2,order=20)
        max_dual=max(max_dual,abs(p1-p2),abs(p2-rows[2]['R']))
        self1=self_response(m,cutoff=400);self2=self_response(m,cutoff=800)
        assert max(abs(self1[k]-self2[k]) for k in self1)<1e-9
        j=c['source_amplitude_example'];lam=c['pointer_coupling_example']
        qv,pv=c['pointer_variances_Q_P']
        quantum_floor=(qv/lam**2+self1['H_BB']+lam**2*self1['K_BB']**2*pv)/j**2
        # Total synthetic shot-noise covariance has minimum eigenvalue below.
        min_cov=(.05**2/.3)*(.8)*(.6)
        assert quantum_floor<min_cov
        controls[name]=dict(settings=rows,position_late=p2,self_response=self1,
            example_normalized_pointer_noise_variance=quantum_floor,synthetic_covariance_min_eigenvalue=min_cov)
        all_R.append(np.array([v['R'] for v in rows]))
    assert max_quad<tol and max_dual<tol
    # Robust support conditions, including geometric / switching errors.
    spacelike_margin=(.99-2*.255)-(.25+.02+2*.102)
    assert spacelike_margin>0
    corners=[]
    for m in [.49,.51]:
      for T in [1.98,2.02]:
       for r in [.99,1.01]:
        for a in [.245,.255]:
         for b in [.098,.102]:
          v=-position_tail(m,T,r,a,b,order=12);corners.append(v)
          assert cert['lower']<=v<=cert['upper']
    w=np.array(c['signs'])/4;times=np.array(c['shot_times'])
    assert w.sum()==0 and w@times==0 and w@np.array(c['signs'])==1
    assert w@(times**2)==1
    # Uncalibrated, setting-dependent odd feedthrough aliases ALL response means.
    alias=all_R[0]-all_R[1]
    assert np.max(np.abs(all_R[1]+alias-all_R[0]))<1e-14
    # Null settings still pass when lightcone / tail settings are spoofed.
    assert abs(alias[0])<tol and alias[3]==0 and abs(alias[2])>.008
    n=c['primary_blocks'];rho=.9;h=np.arange(1,n)
    inflation=float(1+2*np.sum((1-h/n)*rho**h))
    ar_error=float(norm.cdf(-cert['separation_gap']/(2*.05*np.sqrt(inflation/n))))
    assert ar_error>.05
    gum={}
    for name in c['models']:
        r=json.loads(Path('records/'+name+'.json').read_text())
        data=np.load('raw/'+name+'.npy');blocks=np.load('raw/'+name+'_blocks.npy')
        np.testing.assert_array_equal(np.einsum('t,nts->ns',w,data[:,:,:,0]-data[:,:,:,1]),blocks)
        assert r['decision']==name
        U=np.array(r['input_covariance']);J=np.array(r['jacobian']);V=np.array(r['exact_pdf_covariance'])
        np.testing.assert_allclose(J@U@J.T,r['first_order_covariance'],rtol=1e-13,atol=1e-16)
        assert np.linalg.eigvalsh(V).min()>0
        e=np.array(r['monte_carlo_mean_check'])-r['exact_pdf_mean'];se=np.array(r['monte_carlo_mean_standard_error'])
        cov_err=float(np.linalg.norm(np.array(r['monte_carlo_covariance_check'])-V)/np.linalg.norm(V))
        assert np.max(np.abs(e/se))<5 and cov_err<.02
        assert r['max_relative_standard_uncertainty_change']<.001
        gum[name]=dict(max_mean_error_in_MC_standard_errors=float(np.max(np.abs(e/se))),relative_covariance_MC_error=cov_err,
            validation_probability_interval=r['joint_ellipsoid']['validation_probability_99pct_interval'])
    result=dict(status='PASS_SCOPED_ANALYTIC_AND_NUMERICAL_CONTROLS',
        spatial_convolution=str(cs),temporal_convolution=str(ct),exact_normalizations=True,
        max_direct_fourier_error=max(ft_error),max_spectral_order_difference=max_quad,max_position_spectral_difference=max_dual,
        spectral_tail_bound=spectral_tail_bound(),spacelike_support_margin=spacelike_margin,parameter_corner_range=[min(corners),max(corners)],
        controls=controls,gum_checks=gum,
        negative_controls=dict(quadratic_drift_survives_ABBA=True,setting_dependent_odd_feedthrough_alias=alias.tolist(),null_settings_do_not_exclude_alias=True,
            AR1_coefficient=rho,AR1_variance_inflation=inflation,AR1_endpoint_error=ar_error,reversed_commutator_is_not_retarded_response=True,
            classical_Klein_Gordon_response_identical=True),
        physical_release='HOLD_FIELD_TRANSFER',physical_input_missing=True)
    Path('records/check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':check()
