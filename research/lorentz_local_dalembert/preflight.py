"""Boguña–Krioukov coefficient preflight only, NOT an intrinsic implementation.

Neighborhood construction, intrinsic spatial distances and convergence remain
unimplemented. This prevents an assembly unit test being called a reproduction.
"""
import json
import math

def assemble(phi0, phi_minus, phi_plus, mean_minus, mean_plus, tau_n, tau_m, d, coefficient):
    values=[phi0,phi_minus,phi_plus,mean_minus,mean_plus,tau_n,tau_m,coefficient]
    if not all(math.isfinite(v) for v in values) or tau_n<=0 or tau_m<=0 or coefficient<=0 or type(d) is not int or d<1:
        raise ValueError('finite values, positive scales/coefficient and spatial dimension required')
    dt=(phi_plus+phi_minus-2*phi0)/tau_n**2
    ds=(mean_plus+mean_minus-2*phi0)/tau_m**2
    return -(coefficient+d+1)*dt+coefficient*ds

def check():
    d=2; c=243/29; tn=.1; tm=.2
    assert assemble(1,1,1,1,1,tn,tm,d,c)==0
    time_moment=(1+d/c)*tm**2
    spatial_moment=tm**2/c
    assert math.isclose(assemble(0,tn**2,tn**2,time_moment,time_moment,tn,tm,d,c),-2,abs_tol=1e-13)
    assert math.isclose(assemble(0,0,0,spatial_moment,spatial_moment,tn,tm,d,c),2,abs_tol=1e-13)
    return dict(status='PASS_ASSEMBLY_ONLY',intrinsic_reproduction=False,curvature_estimator=False,
        controls=['constant annihilation','time quadratic sign','space quadratic sign'])

if __name__=='__main__': print(json.dumps(check(),indent=2))
