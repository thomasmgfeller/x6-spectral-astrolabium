"""Finite perturbation bound, with rational row transforms and outward norms.
No optimizer, source truth, field values or empirical covariance is used.
SPDX-License-Identifier: Apache-2.0
"""
import numpy as np
from scipy.linalg import qr
from fp_common import F,inverse,interval,exact_weights,up,rootup,normup,infnorm,outward


class Bound:
    def __init__(self,packet,mask,coordinates,box,pivots=None):
        self.scale=F(str(packet['scale']))
        z=[[F(f'{v:.12f}') for v in row] for row in coordinates]
        self.n=len(z)-5
        self.exact_center_order=True
        if 'full_order' in packet:
            for i in range(len(z)):
                for j in range(len(z)):
                    relation=interval(z,i,j)>0 and z[j][0]>z[i][0]
                    self.exact_center_order &= relation==packet['full_order'][i][j]
        nodes=packet['landmarks']+[packet['root']]+packet['support'];lookup={a:i for i,a in enumerate(nodes)}
        pairs=[packet['pairs'][i] for i in mask];m=len(pairs)
        where={tuple(sorted(pair)):k for k,pair in enumerate(pairs)}
        def coeff(a,b):
            row=np.full(m,F(0),dtype=object)
            if a!=b:row[where[tuple(sorted((a,b)))]]=F(1)
            return row
        self.q0=np.array([interval(z,lookup[a],lookup[b]) for a,b in pairs],dtype=object)
        self.radius=np.array([max(abs(lo-q),abs(hi-q)) for q,(lo,hi) in zip(self.q0,box)],dtype=object)
        anchors=packet['landmarks'];root=packet['root']
        hm=np.array([[(coeff(a,b)-coeff(a,anchors[0])-coeff(anchors[0],b))/2 for b in anchors[1:]] for a in anchors[1:]],dtype=object)
        Z=np.array([[(coeff(a,s)-coeff(anchors[0],s)-coeff(a,root)+coeff(anchors[0],root))/2 for a in anchors[1:]] for s in packet['support']],dtype=object)
        v=Z@self.q0
        D=np.array([[t,x,y,t*t,x*x,y*y,t*x,t*y,x*y] for t,x,y in v],dtype=object).T
        bm=np.vstack((np.full((3,m),F(0),dtype=object),2*hm[0,0],2*hm[1,1],2*hm[2,2],2*hm[0,1],2*hm[0,2],2*hm[1,2]))
        if pivots is None:pivots=list(map(int,qr(np.array(D,float),pivoting=True,mode='economic')[2][:9]))
        assert len(set(pivots))==9
        S=inverse(D[:,pivots]);self.pivots=pivots
        D0=S@D;b0=S@bm@self.q0
        assert np.array_equal(D0[:,pivots],np.eye(9,dtype=int))
        P=np.eye(self.n,dtype=object)-np.full((self.n,self.n),F(1,self.n+1),dtype=object)
        M=D0@P@D0.T;Minv=inverse(M);lam=Minv@b0
        a=P@D0.T@lam;w=np.r_[-sum(a),a]/self.scale**2
        independent=np.array(exact_weights(z,self.scale),dtype=object)
        assert np.array_equal(w,independent)
        self.reference_norm=sqrt_lower=__import__('fp_common').sqrt_bounds(sum(x*x for x in w))[0]
        assert sqrt_lower>0
        self.lamnorm=normup(lam)
        self.beta=up(infnorm(Minv))
        self.d0=rootup(infnorm(M))
        # Preserve first-order cancellation after the exact row transform.
        # Every monomial's quadratic remainder is bounded separately.
        L=np.full((9,self.n),F(0),dtype=object);Q=L.copy()
        for j in range(self.n):
            ev=abs(Z[j])@self.radius
            J=np.vstack((Z[j],*[2*v[j,i]*Z[j,i] for i in range(3)],
                          v[j,0]*Z[j,1]+v[j,1]*Z[j,0],
                          v[j,0]*Z[j,2]+v[j,2]*Z[j,0],
                          v[j,1]*Z[j,2]+v[j,2]*Z[j,1]))
            remainder=np.r_[np.full(3,F(0),dtype=object),ev*ev,ev[0]*ev[1],ev[0]*ev[2],ev[1]*ev[2]]
            L[:,j]=abs(S@J)@self.radius
            Q[:,j]=abs(S)@remainder
        self.L=normup(L);self.Q=normup(Q)
        self.B=normup(abs(S@bm)@self.radius)
        self.q_min_margin=min(self.q0-self.radius)
        self.center_in_box=all(lo<=q<=hi for q,(lo,hi) in zip(self.q0,box))
        # Optional finite envelope only on the inherited cond(D)<=1e5 domain.
        # This additional domain restriction is NOT established by coverage.
        ev=abs(Z)@self.radius
        raw_radius=np.array([[a,b,c,2*abs(t)*a+a*a,2*abs(x)*b+b*b,2*abs(y)*c+c*c,
                              abs(t)*b+abs(x)*a+a*b,abs(t)*c+abs(y)*a+a*c,abs(x)*c+abs(y)*b+b*c]
                             for (t,x,y),(a,b,c) in zip(v,ev)],dtype=object).T
        floor=max(max(F(0),abs(d)-r) for d,r in zip(D.flat,raw_radius.flat))
        borig=bm@self.q0;bradius=abs(bm)@self.radius
        self.gated_envelope=None
        if floor>0:
            upper=rootup(F(self.n+1))*F(10**5)*normup(abs(borig)+bradius)/(self.scale**2*floor)
            self.gated_envelope=outward(upper)[1]

    def evaluate(self,k):
        t=F(1,2**k)
        eps=up(t*self.L+t*t*self.Q);eb=up(t*self.B)
        em=up(2*self.d0*eps+eps*eps);gamma=up(self.beta*em)
        result=dict(k=k,fraction=str(t),contraction_upper=outward(gamma)[1],
                    confidence_scope='FULL_SIMULTANEOUS_BOX' if k==0 else 'LOCAL_ONLY_NO_COVERAGE',
                    status='NO_CONTRACTION_CERTIFICATE')
        if gamma>=1:return result
        dl=up(self.beta*(eb+em*self.lamnorm)/(1-gamma))
        dw=up((self.d0*dl+eps*(self.lamnorm+dl))/self.scale**2)
        relative=up(dw/self.reference_norm)
        result.update(status='FINITE_BOUND',absolute_error_upper=outward(dw)[1],
                      error_over_reference_norm_upper=outward(relative)[1])
        if relative<1:
            true_relative=up(relative/(1-relative))
            result.update(true_relative_error_upper=outward(true_relative)[1],ten_percent_certified=true_relative<=F(1,10))
        else:result['ten_percent_certified']=False
        return result

    def constants(self):
        return dict(pivots=self.pivots,center_in_confidence_box=self.center_in_box,
                    exact_center_order=self.exact_center_order,
                    inverse_moment_norm_upper=outward(self.beta)[1],moment_norm_sqrt_upper=outward(self.d0)[1],
                    linear_design_error_upper=outward(self.L)[1],quadratic_design_error_upper=outward(self.Q)[1],
                    target_error_upper=outward(self.B)[1],reference_weight_norm_lower=outward(self.reference_norm)[0],
                    restricted_condition_domain_weight_norm_upper=self.gated_envelope,
                    restricted_envelope_scope='Only geometries already assumed to satisfy intrinsic cond_2(D)<=1e5; does not prove true geometry meets this gate.')
