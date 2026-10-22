"""Exact group/conformal controls and independent quadrature/SVD checks.
SPDX-License-Identifier: Apache-2.0
"""
from ct_run import *
import numpy as np

def rest_map(X,k):
    t,x,y=X;q=t*t-x*x-y*y;D=1+2*k*t+k*k*q
    return [((1+k*k)*t+k*(1+q))/D,(1-k*k)*x/D,(1-k*k)*y/D]

def jacobian_control(X,k):
    t,x,y=X;q=t*t-x*x-y*y;D=1+2*k*t+k*k*q
    dD=[2*k+2*k*k*t,-2*k*k*x,-2*k*k*y]
    n=[(1+k*k)*t+k*(1+q),(1-k*k)*x,(1-k*k)*y]
    dn=[[1+k*k+2*k*t,-2*k*x,-2*k*y],[0,1-k*k,0],[0,0,1-k*k]]
    J=[[(dn[i][j]*D-n[i]*dD[j])/D**2 for j in range(3)] for i in range(3)]
    omega=(1-k*k)/D
    for i in range(3):
      for j in range(3):assert sum(F([1,-1,-1][a])*J[a][i]*J[a][j] for a in range(3))==(omega**2*[1,-1,-1][i] if i==j else 0)
    assert determinant(J)==omega**3

def controls():
    w,z=inputs();ks=[F(-1,2),F(-9,5000),F(0),F(1,5)]
    for k in ks:
        zz,om=flow(z,k);back,_=flow(zz,-k);assert back==z
        for j in [F(-1,7),F(1,9)]:
            composed,_=flow(zz,j);direct,_=flow(z,(k+j)/(1+k*j));assert composed==direct
        for t in [F(-1,4),F(0),F(1,3)]:
          for x,y in [(F(0),F(0)),(F(1,7),F(-1,9))]:jacobian_control([t,x,y],k)
    # Unit rest diamond: use independent Gauss-Legendre quadrature on each time half.
    nodes,weights=np.polynomial.legendre.leggauss(80);u=(nodes+1)/2;ww=weights/2
    normalized=[]
    for k in [-.5,-.2,-.0018,0.,.0018,.2,.5]:
        volume=second=jacmass=Jmass=0.
        for sign in [-1,1]:
          for a,wa in zip(u,ww):
            t=sign*a
            for b,wb in zip(u,ww):
                r=(1-a)*b;mass=wa*wb*2*np.pi*(1-a)**2*b
                q=t*t-r*r;omega=(1-k*k)/(1+2*k*t+k*k*q)
                volume+=mass;second+=mass*t*t;jacmass+=mass*omega**3
                Jmass+=mass*(omega**1.5-1)**2
        assert abs(volume/(2*np.pi/3)-1)<1e-12
        assert abs(second/volume-.1)<1e-12
        assert abs(jacmass/volume-1)<1e-12
        target=.9*np.arctanh(k)**2
        assert Jmass/volume<=target+1e-14
        normalized.append(dict(k=str(k),path_bound_verified=True,jacobian_mass_preserved=True))
    witness=read(HERE/'witness.json');zz=[[F(v) for v in row] for row in witness['coordinates']]
    svd=[]
    for geom,wt in [(z,witness['weights'][0]),(zz,witness['weights'][1])]:
        Y=np.array([[float(v-a) for v,a in zip(row,geom[4])] for row in geom[4:]])
        t,x,y=Y.T;D=np.array([np.ones(len(Y)),t,x,y,t*t,x*x,y*y,t*x,t*y,x*y])
        rhs=np.array([0,0,0,0,-2,2,2,0,0,0],float)/float(F(w['scale'])**2)
        direct=np.linalg.lstsq(D,rhs,rcond=None)[0];exact=np.array([float(F(v)) for v in wt])
        assert np.linalg.norm(direct-exact)/np.linalg.norm(exact)<1e-9;svd.append(True)
    return dict(exact_flow_inverse_cases=4,exact_composition_cases=8,exact_jacobian_metric_and_volume_cases=24,
      quadrature_cases=normalized,independent_svd_weight_checks=svd)

if __name__=='__main__':
    audit=dict(status='PASS',controls=controls())
    if '--verify' in sys.argv:assert audit==read(HERE/'audit.json')
    else:save(HERE/'audit.json',audit)
    print(json.dumps(audit))
