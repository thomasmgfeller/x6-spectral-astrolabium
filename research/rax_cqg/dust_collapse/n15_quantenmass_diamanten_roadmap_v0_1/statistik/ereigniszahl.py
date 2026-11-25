"""Finite-sample decision bounds for the published conditional three-cell experiment."""
import hashlib
import json
from math import factorial
from pathlib import Path
import mpmath as mp

ROOT = Path(__file__).resolve().parent
mp.mp.dps = 65
mp.iv.dps = 65
SOURCE_HASH = '73bd1a8bcf649c2ec5b8beefa00bbd2bda43ed6eabbab6b9ea09c1accffd1c7b'


def gaussian_cdf(x, ctx):
    if ctx is mp.mp:
        return ctx.erfc(-x/ctx.sqrt(2))/2
    # Phi(x) = [1+erf(x/sqrt(2))]/2. The alternating Maclaurin tail
    # is bounded by its next term once terms decrease. This domain and
    # truncation cover all arguments of the endpoint certificates.
    z = x/ctx.sqrt(2)
    if not abs(z) < 4:
        raise ArithmeticError("outside the verified erf series range")
    term = z
    total = term
    for j in range(1,145):
        term = -term*z*z*(2*j-1)/(j*(2*j+1))
        total += term
    next_term = -term*z*z*289/(145*291)
    error = abs(next_term)
    enclosure = total + ctx.mpf([-1,1])*error
    return (1+2*enclosure/ctx.sqrt(ctx.pi))/2


def probabilities(row,ctx):
    result = []
    for name in ('flat','open'):
        raw=[ctx.mpf(x) for x in row['backgrounds'][name]['cell_probabilities']]
        if ctx is mp.iv:
            # Protect all displayed decimals and perturbations of up to
            # 1e-24 at the input before normalisation.
            raw=[x+ctx.mpf(['-1e-24','1e-24']) for x in raw]
        result.append([x/sum(raw) for x in raw])
    return result


def tilted(row,ctx):
    p,q=probabilities(row,ctx)
    roots=[ctx.sqrt(x*y) for x,y in zip(p,q)]
    rho=sum(roots)
    z=[ctx.ln(x/y) for x,y in zip(p,q)]
    weights=[r/rho for r in roots]
    mean=sum(w*v for w,v in zip(weights,z))
    variance=sum(w*(v-mean)**2 for w,v in zip(weights,z))
    skew_abs=sum(w*abs(v-mean)**3 for w,v in zip(weights,z))/variance**ctx.mpf('1.5')
    return rho,mean,variance,skew_abs


def bound(pars,n,ctx):
    rho,mean,variance,gamma=pars
    mu=n*mean
    sd=ctx.sqrt(n*variance)
    normal_integral=sum(ctx.exp(sd**2/8-sign*mu/2)*gaussian_cdf(sign*mu/sd-sd/2,ctx)
                        for sign in (-1,1))
    # The total variation of exp(-|s|/2) is 2; the classical iid
    # Berry-Esseen constant is < 0.48 (Shevtsova, arXiv:1111.6554).
    radius=2*ctx.mpf('0.48')*gamma/ctx.sqrt(n)
    prefactor=ctx.exp(n*ctx.ln(rho))/2
    return prefactor*(normal_integral-radius),prefactor*(normal_integral+radius)


def first_meeting(lo,hi,test):
    # Only finds candidate endpoints; final certification uses independent
    # interval computation and monotonicity of optimal iid Bayes error itself.
    if test(lo) or not test(hi):
        raise ValueError('inadequate initial bracket')
    while hi-lo>1:
        mid=(lo+hi)//2
        if test(mid):
            hi=mid
        else:
            lo=mid
    return hi


def direct(n,p,q):
    accuracy=mp.mpf(0)
    for a in range(n+1):
        for b in range(n-a+1):
            c=n-a-b
            c_n=factorial(n)//(factorial(a)*factorial(b)*factorial(c))
            x,y=[v[0]**a*v[1]**b*v[2]**c for v in (p,q)]
            accuracy+=c_n*max(x,y)/2
    return accuracy


def evaluate(row):
    ctx=mp.mp
    eps=gaussian_cdf(mp.mpf(-3),ctx)
    args=tilted(row,ctx)
    rho=args[0]
    nc=int(mp.ceil(mp.log(4*eps*(1-eps))/(2*mp.log(rho))))
    ns=int(mp.ceil(mp.log(2*eps)/mp.log(rho)))
    lower=first_meeting(nc,ns,lambda n:bound(args,n,ctx)[0]<=eps)
    upper=first_meeting(nc,ns,lambda n:bound(args,n,ctx)[1]<=eps)
    cert_args=tilted(row,mp.iv)
    target=gaussian_cdf(mp.iv.mpf(-3),mp.iv)
    # Check rigorous inequalities at the reported endpoints, including
    # positive separation from the threshold and input decimal sensitivity.
    too_small=bound(cert_args,lower-1,mp.iv)[0]
    sufficient=bound(cert_args,upper,mp.iv)[1]
    if not (too_small>target and sufficient<target):
        # Extend slightly if the last input decimal can change an endpoint.
        lower-=32
        upper+=32
        too_small=bound(cert_args,lower-1,mp.iv)[0]
        sufficient=bound(cert_args,upper,mp.iv)[1]
    if not (too_small>target and sufficient<target):
        raise ArithmeticError('uncertified decision bracket')
    accuracy=direct(15,*probabilities(row,ctx))
    if abs(accuracy-mp.mpf(row['synthetic_15']['oracle_accuracy']))>mp.mpf('1e-18'):
        raise ArithmeticError('published n=15 check')
    return dict(h=row['h'],one_sided_error_target=mp.nstr(eps,22),
                accuracy_at_external_n15=mp.nstr(accuracy,21),
                elementary_hellinger_bracket=[nc,ns],certified_minimum_bracket=[lower,upper],
                excluded_n=lower-1,certified_error_lower_at_excluded_n=str(too_small),
                sufficient_n=upper,certified_error_upper_at_sufficient_n=str(sufficient),
                certified_target_interval=str(target))


if __name__=='__main__':
    source=ROOT/'fenster.json'
    if hashlib.sha256(source.read_bytes()).hexdigest()!=SOURCE_HASH:
        raise RuntimeError('source SHA-256 mismatch')
    rows=json.loads(source.read_text())
    results=[evaluate(row) for row in rows]
    (ROOT/'ergebnis.json').write_text(json.dumps(results,indent=2)+'\n')
    for r in results:
        print(r['h'],r['certified_minimum_bracket'])
