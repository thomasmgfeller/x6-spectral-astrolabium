"""Validated Gaussian mean screen for a normalized five-layer GCB family.

No random sampling. Decision-making uses Arb balls, never display midpoints.
See PROOF.md for the reduction, endpoint bounds and scope of each test.
"""
import argparse, json, math, platform
from pathlib import Path
from fractions import Fraction as F
from flint import arb, acb, arb_mat, ctx
import flint

ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'PROTOCOL.json').read_text())
C0=list(map(F,P['coefficients_c_base']))
CQ=list(map(F,P['coefficients_c_direction']))
CT=list(map(F,P['coefficients_c_candidate']))

def a(x):
    if isinstance(x,F): return arb(x.numerator)/x.denominator
    return arb(x)

def enc(x):
    x=a(x)
    if not x.is_finite(): raise ArithmeticError('nonfinite result')
    s=x.str(55,more=True)
    if not arb(s).contains(x): raise ArithmeticError('serialization enclosure lost')
    return {'ball':s,'display_mid':float(x.mid()),'display_radius':float(x.rad())}

def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def mean(L,coeff,diag):
    q=3/(16*arb.pi()); pref=4*(q/6).sqrt(); c=(arb.pi()*q/24).sqrt()
    delta=a(F(P['delta'])); Y=a(P['upper_y']); L=a(L)
    pp=[a(x)/math.factorial(n) for n,x in enumerate(coeff)]
    def fun(y,analytic):
        if not y.real>0: return acb('nan')
        z=y/(2*c*L*L); v=sum(k*y**(2*n) for n,k in enumerate(pp))
        return y*v*(-y*y).exp()*(z.bessel_k(1)-z.bessel_k(0))
    core=acb.integral(fun,delta,Y,abs_tol=arb(P['abs_tol']),rel_tol=arb(P['rel_tol']),
                      eval_limit=P['eval_limit'],depth_limit=100)
    if not core.is_finite() or not core.imag.contains(0): raise ArithmeticError('invalid quadrature')
    low=8*arb.pi().sqrt()*q*L*L*delta*sum(abs(k)*delta**(2*n) for n,k in enumerate(pp))
    tail=arb.pi().sqrt()*Y.erfc()/2; high=abs(pp[0])*tail
    for n in range(1,len(pp)):
        tail=Y**(2*n-1)*(-Y*Y).exp()/2+(2*n-1)*tail/2
        high+=abs(pp[n])*tail
    high*=8*arb.pi().sqrt()*q*L*L
    out=pref*(a(diag)+12*core.real)+arb(0,(low+high).abs_upper())
    if not out.rad()<arb(P['mean_radius_goal']): raise ArithmeticError('mean radius goal failed')
    return out,{'low_tail':enc(low),'high_tail':enc(high),'core':enc(core.real)}

def rising(s,n):
    z=F(1)
    for j in range(n): z*=s+j
    return z/F(math.factorial(n))

def deriv_rising(s,n):
    # Used only for positive rational s, so no zero division.
    return rising(s,n)*sum((1/(s+j) for j in range(n)),F(0))

def mellin(c,s): return sum((x*rising(s,n) for n,x in enumerate(c)),F(0))
def dmellin(c,s): return sum((x*deriv_rising(s,n) for n,x in enumerate(c)),F(0))

def rational_checks():
    checks={}
    for label,c in [('base',C0),('direction',CQ),('candidate',CT)]:
        for s in [F(1,2),F(1),F(3,2)]: checks[f'{label}_cancel_{s}']=mellin(c,s)==0
    checks['normalization_base']=dmellin(C0,F(3,2))==F(-2,3)
    checks['normalization_direction']=dmellin(CQ,F(3,2))==0
    checks['normalization_candidate']=dmellin(CT,F(3,2))==F(-2,3)
    checks['diagonal_candidate']=-3*dmellin(CT,F(1))==F(-71,8)
    checks['candidate_coefficients']=CT==[u+21*v for u,v in zip(C0,CQ)]
    # Rank of the four IR rows: the first four coefficient columns suffice.
    M=[[rising(s,n) for n in range(4)] for s in [F(1,2),F(1),F(3,2)]]
    M.append([deriv_rising(F(3,2),n) for n in range(4)])
    det=F(1)
    for i in range(4):
        k=next(j for j in range(i,4) if M[j][i])
        if k!=i: M[k],M[i]=M[i],M[k];det=-det
        pivot=M[i][i];det*=pivot
        for j in range(i+1,4):
            fac=M[j][i]/pivot
            for k in range(i,4):M[j][k]-=fac*M[i][k]
    checks['rank_four']=det!=0
    # Exact polynomial identity at five distinct points fixes degree <=4.
    for s in range(5):
        checks[f'Q_factorization_{s}']=mellin(CQ,F(s))==(F(s)-F(1,2))*(s-1)*(F(s)-F(3,2))**2
    # Deliberate coefficient error must fail an IR identity.
    bad=CT.copy();bad[0]+=1
    checks['negative_wrong_coefficient_detected']=mellin(bad,F(1,2))!=0
    if not all(checks.values()): raise ArithmeticError('rational constraints failed')
    return {'checks':checks,'rank_minor_determinant':str(det)}

def weight(n):
    e=F(1,16)
    return sum((c*math.comb(n,k)*e**k*(1-e)**(n-k) for k,c in enumerate(CT) if k<=n),F(0))

def finite_stability():
    aa=1/(2*arb.pi()).sqrt(); D=1+aa*arb(71)/8; beta=aa/(16*D)
    gamma=beta*1331
    # Total order: three history nodes, five active nodes, one passive query.
    # This embeds as collinear timelike points. n(j,i)=i-j-1 exactly.
    nh,na=3,5
    K=[[beta*a(weight(nh+i-j-1)) if j<nh+i else arb(0) for j in range(nh+na)] for i in range(na)]
    A=arb_mat([[int(i==j)-K[i][nh+j] for j in range(na)] for i in range(na)])
    H=arb_mat([[K[i][j] for j in range(nh)] for i in range(na)])
    dense=A.inv()*H
    triangular=[]
    gains=[]
    for i in range(na):
        triangular.append([K[i][j]+sum(K[i][nh+k]*triangular[k][j] for k in range(i)) for j in range(nh)])
        gains.append(sum(abs(K[i][j]) for j in range(nh))+sum(abs(K[i][nh+k])*gains[k] for k in range(i)))
    q=[beta*a(weight(nh+na-j-1)) for j in range(nh+na)]
    transfer=[q[j]+sum(q[nh+k]*triangular[k][j] for k in range(na)) for j in range(nh)]
    gain=sum(abs(q[j]) for j in range(nh))+sum(abs(q[nh+k])*gains[k] for k in range(na))
    norm=sum(abs(z) for z in transfer)
    checks={
      'positive_diagonal_denominator':bool(D>0),
      'dense_vs_triangular':all(dense[i,j].overlaps(triangular[i][j]) for i in range(na) for j in range(nh)),
      'determinant_one':bool(A.det().contains(1)),
      'history_gain_majorizes_norm':bool(gain>=norm),
      'future_entries_exact_zero':all(K[i][j].is_zero() for i in range(na) for j in range(nh+i,nh+na)),
      'query_gain_below_uniform_envelope':bool(gain<=gamma*nh*(1+gamma)**na),
    }
    # Deliberately drop all active transport; test that the exact transfer differs.
    checks['negative_omitted_paths_detected']=any(not (transfer[j]-q[j]).contains(0) for j in range(nh))
    if not all(checks.values()): raise ArithmeticError('finite stability checks failed')
    return {'checks':checks,'D':enc(D),'beta':enc(beta),'gamma_uniform':enc(gamma),
      'history_gain_enclosure':enc(gain),'actual_history_operator_norm':enc(norm),
      'scope':'finite history problem only; no density-uniform or infinite-past spectral stability claim'}

def compute(bits):
    ctx.prec=bits
    rows=[]; base={}; slope={}
    for L in P['gaussian_L']:
        b,mb=mean(L,C0,F(-1)); v,mv=mean(L,CQ,F(-3,8))
        direct,md=mean(L,CT,F(-71,8)); target=-arb(2)/(L*L)
        combined=b+21*v
        if not direct.overlaps(combined): raise ArithmeticError('affine reconstruction failed')
        if not v<0: raise ArithmeticError('slope sign undecided')
        left=(target+abs(target)/10-b)/v; right=(target-abs(target)/10-b)/v
        base[L]=(b-target)/abs(target); slope[L]=-v/abs(target)
        rows.append({'L':L,'target':enc(target),'base_mean':enc(b),'direction_mean':enc(v),
          'candidate_mean':enc(direct),'candidate_relative_bias':enc(abs(direct-target)/abs(target)),
          'theta_interval_lower_endpoint':enc(left),'theta_interval_upper_endpoint':enc(right),
          'candidate_passes_mean_screen':bool(abs(direct-target)/abs(target)<=arb('0.1')),
          'base_tails':mb,'direction_tails':mv,'direct_tails':md})
        print('certified L',L,'theta21 bias',float((abs(direct-target)/abs(target)).mid()),flush=True)
    a2,a4=base[2],base[4];b2,b4=slope[2],slope[4]
    theta=(a2+a4)/(b2+b4); best=(a2*b4-a4*b2)/(b2+b4)
    if not best>arb('0.1'):raise ArithmeticError('family exclusion not certified')
    gap=arb(rows[0]['theta_interval_lower_endpoint']['ball'])-arb(rows[1]['theta_interval_upper_endpoint']['ball'])
    if not gap>0:raise ArithmeticError('intervals not disjoint')
    return {'schema':P['schema'],'precision_bits':bits,'python':platform.python_version(),'python_flint':flint.__version__,
      'rational':rational_checks(),'rows':rows,'family':{'theta_minimax':enc(theta),'minimax_relative_bias':enc(best),
      'admissible_interval_gap':enc(gap),'all_real_theta_excluded_at_fixed_q':True,
      'scope':'two Gaussian scales L=2,4; normalized polynomial degree<=4; full-past mean; fixed q'},
      'finite_stability':finite_stability(),'decision':'REJECT_FOR_CONTINUATION_TWO_SCALE_SCREEN',
      'compact_detector_production':'NOT_RUN_EARLY_ABORT',
      'full_spectral_stability':'NOT_RUN_EARLY_ABORT','METHOD':'HOLD','G1':'HOLD',
      'new_random_clouds':0,'confirmation_seed_used':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,default=128);ap.add_argument('--out',type=Path)
    args=ap.parse_args();out=args.out or ROOT/'results'/f'CERTIFICATE_{args.bits}.json'
    write(out,compute(args.bits))
