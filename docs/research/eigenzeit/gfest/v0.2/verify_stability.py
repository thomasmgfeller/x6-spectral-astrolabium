"""GFEST v0.2: exact rational local certificate and labelled diagnostics.
Run with Python 3, sympy, numpy, scipy, mpmath. No optimizer is used.
SPDX-License-Identifier: Apache-2.0
"""
import json, math, hashlib, platform
from pathlib import Path
import sympy as S
import numpy as np
import scipy
from scipy.stats import poisson
import mpmath as mp

HERE=Path(__file__).resolve().parent
R=S.Rational
J=S.diag(1,-1,-1)
def ab(M): return M.applyfunc(abs)
def fro2(M): return sum(x*x for x in M)
def infnorm(M): return max(sum(abs(M[i,j]) for j in range(M.cols)) for i in range(M.rows))
def sqrt_bounds(x, digits=35):
    x=R(x); assert x>=0
    t=10**digits; a=math.isqrt(int(S.floor(x*t*t)))
    return R(a,t),R(a+1,t)
def display(x): return str(S.N(x,18))
def q(x,y):
    v=x-y; return (v.T*J*v)[0]
def phi(x): return S.Matrix([1,*x,*[v*v for v in x],x[0]*x[1],x[0]*x[2],x[1]*x[2]])
def rhs(M): return S.Matrix([0,0,0,0,-2*M[0,0],-2*M[1,1],-2*M[2,2],-2*M[0,1],-2*M[0,2],-2*M[1,2]])
def weights(A,b): return A.T*(A*A.T).inv()*b
def precondition(A):
    a=np.array(A,dtype=float)
    T=np.linalg.inv(np.linalg.cholesky(a@a.T))
    # Floating construction is untrusted; all subsequent checks are rational.
    return S.Matrix([[R(str(round(float(v),14))) for v in row] for row in T])
def sigma_lower(A):
    err=infnorm(A*A.T-S.eye(A.rows))
    assert err<1
    return sqrt_bounds(1-err)[0],err
def pi_bounds():
    def atan(n):
        total=sum((R((-1)**k,(2*k+1)*n**(2*k+1)) for k in range(50)),R(0))
        nxt=R(1,101*n**101)
        return total,total+nxt
    a,b=atan(5);c,d=atan(239);t=10**40
    return R(S.floor((16*a-4*d)*t),t),R(S.ceiling((16*b-4*c)*t),t)
def marginal_radius(qs,delta,rho):
    """Rational TV lower bound at both q-box faces from fixed CDF events.
    Uses only Chebyshev, the Poisson mode, and dF_k/dlambda=-p_lambda(k).
    """
    pl,pu=pi_bounds(); bounds=[]
    for qq in qs:
        assert qq>delta
        lq=qq-delta;uq=qq+delta
        L=rho*pl/12*lq*sqrt_bounds(lq)[0]
        U=rho*pu/12*uq*sqrt_bounds(uq)[1]
        k=int(S.floor(L)); mmax=int(S.floor(U))
        radius=int(S.ceiling(sqrt_bounds(2*U)[1]))
        pmode=R(1,2*(2*radius+1))
        factor=R(1)
        for j in range(k+1,mmax+1): factor*=min(R(1),R(j)/U)
        pmf_lower=pmode*factor
        dmean=rho*pl/8*sqrt_bounds(lq)[0]*delta
        bounds.append(dmean*pmf_lower)
    return min(bounds)/2
def direct(z):
    A=S.Matrix.hstack(*[phi(x-z[4]) for x in z[4:]])
    b=rhs(J); return A,b,weights(A,b)

def run():
    witness_path=HERE/'witness.json'
    w=json.loads(witness_path.read_text())
    scale=R(w['scale']); rho=R(w['rho'])
    zz=[[S.Matrix([R(v)*scale for v in row]) for row in conf] for conf in w['coordinates']]
    # Fixed rational Lorentz frame, only a polynomial row-basis change.
    L=S.Matrix([[R(5,3),R(4,3),0],[R(4,3),R(5,3),0],[0,0,1]])
    assert L.T*J*L==J
    zz=[[L*x for x in conf] for conf in zz]
    z=zz[0]; B=S.Matrix.hstack(*[z[i]-z[0] for i in range(1,4)])
    G=B.T*J*B; Gi=G.inv()
    c=[B.inv()*(x-z[4]) for x in z[4:]]
    ys=[B*x for x in c]
    A0,b0,w0=direct(z); A1,b1,w1=direct(zz[1])
    assert A0==S.Matrix.hstack(*map(phi,ys))
    assert B*Gi*B.T==J
    expected={tuple(sorted((i,j))) for i in range(4) for j in range(i)}
    expected|={tuple(sorted((i,j))) for i in range(4,21) for j in range(4)}
    observed={tuple(sorted(p)) for p in w['pairs']}
    assert expected==observed and len(expected)==74
    qs=[q(z[i],z[j]) for i,j in sorted(expected)]
    assert min(qs)>0
    # Reconstruct the independently moved endpoint in the FIXED reference chart.
    zp=zz[1]; Bp=S.Matrix.hstack(*[zp[i]-zp[0] for i in range(1,4)])
    Gp=Bp.T*J*Bp; Mp=B*Gp.inv()*B.T
    yp=[B*Bp.inv()*(x-zp[4]) for x in zp[4:]]
    Ap=S.Matrix.hstack(*map(phi,yp)); bp=rhs(Mp)
    assert weights(Ap,bp)==w1 and bp!=b0
    # Exact identity for finite simultaneous movements, in a fixed row basis.
    T=precondition(A0); A=T*A0; b=T*b0
    At=T*A1; bt=T*b1; E=At-A
    AAi=(A*A.T).inv(); Atplus=At.T*(At*At.T).inv()
    P=Atplus*At; y=AAi*b
    r=bt-b-E*w0; s=E.T*y
    u=Atplus*r; v=(S.eye(17)-P)*s
    assert w1-w0==u+v and (u.T*v)[0]==0
    assert fro2(w1-w0)==fro2(u)+fro2(v)
    sig,whiten_error=sigma_lower(A)
    eta=sqrt_bounds(fro2(E))[1]
    point={'actual_relative_gap':display(2*S.sqrt(fro2(w1-w0))/(S.sqrt(fro2(w0))+S.sqrt(fro2(w1)))),
           'orthogonal_identity_exact':True,'row_preconditioner_residual':display(whiten_error),
           'finite_E_frobenius_upper':display(eta)}
    if eta<sig:
        R2=fro2(r)/(sig-eta)**2+fro2(s)
        point['absolute_bound']=display(S.sqrt(R2))
        point['actual_absolute_gap']=display(S.sqrt(fro2(w1-w0)))
        point['relative_bound_using_exact_endpoint_norms']=display(2*S.sqrt(R2)/(S.sqrt(fro2(w0))+S.sqrt(fro2(w1))))
        assert fro2(w1-w0)<=R2
    else: point['bound_status']='HOLD_NEUMANN_RADIUS'
    # Frozen radius grid, physical squared-length units; every member reported.
    cells=[]
    for exponent in range(2,13):
        delta=R(1,10**exponent)
        rec={'delta_q':str(delta),'status':'HOLD'}
        # Form the six EXACT linear coefficient matrices before taking abs.
        # This preserves cancellations due to the common landmark q terms.
        coeff=[]
        for a in range(1,4):
            for bb in range(a):
                F=S.zeros(3,3)
                for i in range(1,4):
                    for k in range(1,4):
                        F[i-1,k-1]=R(int((bb,a)==(0,i))+int((bb,a)==(0,k))-int(tuple(sorted((i,k)))==(bb,a)),2)
                coeff.append(B.inv().T*F*B.inv())
        H=delta*sum((ab(F) for F in coeff),S.zeros(3,3)); h=infnorm(H)
        if exponent==2:
            dq=[q(zp[a],zp[bb])-q(z[a],z[bb]) for a in range(1,4) for bb in range(a)]
            assert sum((F*v for F,v in zip(coeff,dq)),S.zeros(3,3))==B.inv().T*(Gp-G)*B.inv()
        rec['inverse_neumann_norm_upper']=display(h)
        if h>=1:
            rec['reason']='GRAM_RADIUS'; cells.append(rec); continue
        C=(S.eye(3)-H).inv()
        assert all(x>=0 for x in C)
        RM=C*H
        Rb=ab(T)*ab(rhs(RM))
        RA=S.zeros(10,17)
        for j in range(1,17):
            yj=ys[j]
            U=B.inv().T
            Ru=delta*(ab(U*S.ones(3,1))+ab(U)*S.ones(3,1))
            Rf=Ru+delta*sum((ab(F*yj) for F in coeff),S.zeros(3,1))
            Ry=C*Rf
            col=[0,*Ry,*[2*abs(yj[i])*Ry[i]+Ry[i]**2 for i in range(3)]]
            for i,k in ((0,1),(0,2),(1,2)):
                col.append(abs(yj[i])*Ry[k]+abs(yj[k])*Ry[i]+Ry[i]*Ry[k])
            RA[:,j]=S.Matrix(col)
        RE=ab(T)*RA
        e=sqrt_bounds(fro2(RE))[1]
        rec['moment_perturbation_upper']=display(e)
        if e>=sig:
            rec['reason']='MOMENT_RADIUS'; cells.append(rec); continue
        rr=Rb+RE*ab(w0); ss=RE.T*ab(y)
        R2=fro2(rr)/(sig-e)**2+fro2(ss)
        w02=fro2(w0)
        passed=121*R2<=w02
        rw=sqrt_bounds(R2)[1]; nw=sqrt_bounds(w02)[0]
        rec.update({'status':'PASS_LOCAL_PAIRSPACE' if passed else 'HOLD',
                    'reason':'RADIUS_CERTIFICATE' if passed else 'BOUND_EXCEEDS_TARGET',
                    'weight_radius_upper':display(rw),
                    'reference_weight_norm_lower':display(nw),
                    'pair_gap_upper':display(min(R(2),2*rw/(nw-rw))) if rw<nw else '2',
                    'exact_gate_121_R2_le_normw2':bool(passed),
                    'R2_exact':str(R2),'reference_norm_squared_exact':str(w02)})
        if passed:
            # Positive, rational sufficient full-law TV radius to the reference.
            # c3=pi/12>1/4. Concavity of q^(3/4) gives the derivative bound.
            Q=max(qs)+delta
            sqrtQ=sqrt_bounds(Q)[1]
            h2=rho*R(9,64)*delta**2/sqrtQ
            eps=h2/(2+h2)
            epscdf=marginal_radius(qs,delta,rho)
            rec['reference_TV_Hellinger_radius']=display(eps)
            eps=max(eps,epscdf)
            rec['reference_TV_sufficient_radius_exact']=str(eps)
            rec['reference_TV_sufficient_radius']=display(eps)
        cells.append(rec)
    passing=[v for v in cells if v['status']=='PASS_LOCAL_PAIRSPACE']
    assert passing
    advertised=next(v for v in passing if v['delta_q']=='1/1000000')
    ar=sqrt_bounds(R(advertised['R2_exact']))[1]
    an=sqrt_bounds(R(advertised['reference_norm_squared_exact']))[0]
    assert 2*ar/(an-ar)<R(7,100)
    assert R(advertised['reference_TV_sufficient_radius_exact'])>R(1,100000)
    # Positive homogeneity and equal-total-mean cancellation controls.
    scaled=[2*x for x in z]
    assert direct(scaled)[2]==w0/4
    assert w0!=S.zeros(17,1)
    # Exact marginal TV formula vs direct high-precision PMF diagnostic.
    mp.mp.dps=70; pois=[]
    for aa,bb in [('0','0.1'),('0.2','0.3'),('1','2'),('20','22'),('100','101')]:
        a,bb=mp.mpf(aa),mp.mpf(bb)
        if a==0: formula=1-mp.exp(-bb); k=0
        else:
            k=int(mp.floor((bb-a)/mp.log(bb/a)))
            formula=mp.gammainc(k+1,a,mp.inf)/mp.factorial(k)-mp.gammainc(k+1,bb,mp.inf)/mp.factorial(k)
        pa,pb=mp.exp(-a),mp.exp(-bb); total=abs(pa-pb)/2
        for j in range(1,1200):
            pa*=a/j; pb*=bb/j; total+=abs(pa-pb)/2
        assert abs(total-formula)<mp.mpf('1e-60')
        for dim in (2,3,4,5,8):
            # k=rho*c_d normalized to 1 for this analytic scalar control.
            Q=max(a,bb)**(mp.mpf(2)/dim)
            hh=mp.sqrt(-2*mp.log1p(-formula))
            bound=(mp.mpf(4)/dim)*Q**(1-mp.mpf(dim)/4)*hh if dim<=4 else hh**(mp.mpf(4)/dim)
            assert abs(a**(mp.mpf(2)/dim)-bb**(mp.mpf(2)/dim))<=bound+mp.mpf('1e-55')
        pois.append({'mu':aa,'nu':str(bb),'tv':str(formula),'pmf_agreement_60_digits':True})
    # Correlation countercontrol: identical Poisson marginals, different joint laws.
    lam=mp.mpf(1)
    diag_prob=mp.exp(-2*lam)*mp.besseli(0,2*lam)
    result={'schema':'gfest.v0.2.validation/1','status':'PASS_SCOPED_CHECKS',
            'input_sha256':hashlib.sha256(witness_path.read_bytes()).hexdigest(),
            'model':{'dimension':3,'rho':str(rho),'physical_scale':str(scale),'observed_pairs':74,
                     'fixed_rational_Lorentz_frame':[[str(x) for x in row] for row in L.tolist()],
                     'supports_including_root':17,'moment_rows':10,'complete_required_mask_exact':True},
            'endpoint_diagnostic':point,'radius_grid':cells,'largest_certified_grid_radius':passing[0]['delta_q'],
            'moving_landmark_metric_and_chart_exact':True,'six_Gram_coefficients_exact':True,
            'control_scale_ambiguity_exact':True,'poisson_diagnostics':pois,
            'same_marginals_different_joint_control_TV_lower':str(1-diag_prob),
            'proof_scope':'All pairs in the declared local physical q-box around endpoint 0. No certificate for TV<=1/4 over the original class, no replacement of the 38 HOLD boxes, no selection-law or continuum guarantee.',
            'versions':{'python':platform.python_version(),'sympy':S.__version__,'numpy':np.__version__,'scipy':scipy.__version__,'mpmath':mp.__version__}}
    (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    concise={k:v for k,v in result.items() if k not in ('radius_grid','poisson_diagnostics')}
    concise['radius_grid']=[{k:v for k,v in c.items() if not k.endswith('_exact')} for c in cells]
    print(json.dumps(concise,indent=2))
if __name__=='__main__': run()
