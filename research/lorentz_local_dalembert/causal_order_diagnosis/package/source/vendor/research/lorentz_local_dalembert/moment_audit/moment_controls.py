"""Analytic continuum moments and separately injected geometric defects."""
import json
import numpy as np
from moment_common import config
from moments import ETA,NAMES,boost,diagnose,shapley
from controls import compare


def check():
    _,cfg=config(); c=cfg['coefficient_C']; tm=.17; tn=.29
    # Uniform hyperbolic area in 2+1 dimensions: cosh(chi) uniform [1,11/9].
    # Two-point Gauss exactly integrates quadratic moments; 32 angles integrate
    # trigonometric first/second moments. Equal radial weights allow plain mean.
    h=1+(1+np.array([-1,1])/np.sqrt(3))/9
    angle=2*np.pi*np.arange(32)/32
    cap=np.array([[x,np.sqrt(x*x-1)*np.cos(a),np.sqrt(x*x-1)*np.sin(a)] for x in h for a in angle])*tm
    temporal=np.array([[-tn,0,0],[tn,0,0]])
    refs=np.array([[tm,0,0],[-tm,0,0]]); shells=[cap,-cap]
    baseline=diagnose(temporal,shells,refs,tn,tm,c)
    for row in baseline['variants'].values(): np.testing.assert_allclose(row['metric'],ETA,atol=3e-13)
    tbad=diagnose(1.7*temporal,shells,refs,tn,tm,c)
    sbad=diagnose(temporal,[1.4*cap,-.8*cap],refs,tn,tm,c)
    u=np.array([1.,0.,0.]); a=np.array([np.cosh(.6),np.sinh(.6),0.]); b=a*np.array([1,-1,1])
    A=boost(u,a); B=boost(u,b)
    tv=np.array([temporal[0]@B.T,temporal[1]@A.T])
    ss=[cap@A.T,-cap@B.T]; rr=np.array([refs[0]@A.T,refs[1]@B.T])
    dbad=diagnose(temporal,ss,rr,tn,tm,c)
    ebad=diagnose(tv,shells,refs,tn,tm,c)
    for result,factor in [(tbad,'T'),(sbad,'S'),(dbad,'D'),(ebad,'D')]:
        assert result['variants']['raw']['error']>.1
        np.testing.assert_allclose(result['variants'][factor]['metric'],ETA,atol=1e-12)
    # Combined defect, non-collinear observer change: tests the tensor law,
    # not merely rest-frame recovery. Error norms intentionally need not agree.
    v=tv*1.3; w=[1.6*ss[0],.7*ss[1]]
    L=boost(u,np.array([np.cosh(.4),0.,np.sinh(.4)]))
    np.testing.assert_allclose(L.T@ETA@L,ETA,atol=1e-14)
    original=diagnose(v,w,rr,tn,tm,c)
    transformed=diagnose(v@L.T,[s@L.T for s in w],rr@L.T,tn,tm,c)
    for name in NAMES:
        np.testing.assert_allclose(transformed['variants'][name]['metric'],L@original['variants'][name]['metric']@L.T,atol=2e-12)
    np.testing.assert_allclose(original['variants']['TSD']['metric'],ETA,atol=1e-12)
    np.testing.assert_allclose(sum(shapley(np.arange(8.)**2)),-49.)
    rejected=0
    for vv,ww in [(np.zeros((2,3)),shells),(temporal,[np.empty((0,3)),-cap]),(temporal,[np.array([[0.,1.,0.]]),-cap])]:
        try: diagnose(vv,ww,refs,tn,tm,c)
        except ValueError: rejected+=1
        else: raise AssertionError('degenerate input not rejected')
    return dict(status='PASS_SOFTWARE_CONTROLS',analytic_cap_variants=8,
                isolated_defects=4,combined_defect_recovery=True,lorentz_covariance_variants=8,
                degenerate_rejections=rejected,shapley_conservation=True)

if __name__=='__main__': print(json.dumps(check(),indent=2))
