"""Rigorous oracle error at the two candidate integers for h=1/8.

Starting at the binomial mode, likelihood ratios of adjacent masses are
rational. Every stored bound is a scaled integer. The omitted binomial tails
are bounded by two geometric series. The only transcendental operation used
by the decision is the logarithm used to certify which count triples choose
each model; Decimal.ln is correctly rounded to nearest.
"""
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from fractions import Fraction as F
from pathlib import Path
from math import isqrt, factorial
import hashlib, json

ROOT=Path(__file__).resolve().parent
S=10**60
TARGET=(F('0.00134989803163009452664'),F('0.00134989803163009452667'))
INITIAL_N=4915831
SOURCE_HASH='73bd1a8bcf649c2ec5b8beefa00bbd2bda43ed6eabbab6b9ea09c1accffd1c7b'


def ceildiv(num,den):
    return -((-num)//den)


def mul(pair,num,den):
    assert num>=0 and den>0
    return pair[0]*num//den,ceildiv(pair[1]*num,den)


def add(x,y):
    return x[0]+y[0],x[1]+y[1]


def binomial_weights(n,p,obligatory=None):
    a=p.numerator
    b=p.denominator-a
    mode=(n+1)*a//(a+b)
    # The geometric bounds below justify any truncation width, independently
    # of any Gaussian tail or normal approximation.
    span=12*(1+isqrt(n*a*b//(a+b)**2))
    lo=max(0,mode-span)
    hi=min(n,mode+span)
    if obligatory is not None:
        lo=min(lo,obligatory)
        hi=max(hi,obligatory)
    w=[None]*(hi-lo+1)
    w[mode-lo]=(S,S)
    for k in range(mode,lo,-1):
        w[k-lo-1]=mul(w[k-lo],k*b,(n-k+1)*a)
    for k in range(mode,hi):
        w[k-lo+1]=mul(w[k-lo],(n-k)*a,(k+1)*b)
    numerator=lo*b
    denom=(n-lo+1)*a
    left=ceildiv(w[0][1]*numerator,denom-numerator) if lo else 0
    numerator=(n-hi)*a
    denom=(hi+1)*b
    right=ceildiv(w[-1][1]*numerator,denom-numerator) if hi<n else 0
    norm=(sum(x[0] for x in w),sum(x[1] for x in w)+left+right)
    return lo,w,norm,left,right


def get_state(n,p,k):
    first,weights,norm,left,_=binomial_weights(n,p,k)
    j=k-first
    pmf=(weights[j][0]*S//norm[1],ceildiv(weights[j][1]*S,norm[0]))
    cdf=(sum(x[0] for x in weights[:j+1])*S//norm[1],
         ceildiv((sum(x[1] for x in weights[:j+1])+left)*S,norm[0]))
    return pmf,cdf


def log_bounds(p,q):
    with localcontext() as ctx:
        ctx.prec=80
        d=Decimal
        ratio=p/q
        x=d(ratio.numerator)/d(ratio.denominator)
        # One representable step covers division roundoff. Two more steps
        # enclose both rounded logarithms before scaling by a power of ten.
        lo=x.next_minus().ln().next_minus()*S
        hi=x.next_plus().ln().next_plus()*S
        return (int(lo.to_integral_value(rounding=ROUND_FLOOR)),
                int(hi.to_integral_value(rounding=ROUND_CEILING)))


def certified_threshold(n,k,logs):
    mids=[a+b for a,b in logs]
    # log likelihood flat/open is increasing in the count of central cells
    # at fixed k (count in the first cell). Strict inequalities exclude ties.
    den=mids[1]-mids[2]
    assert logs[1][0]>logs[2][1] and den>0
    j=(-n*mids[2]-k*(mids[0]-mids[2]))//den
    strict_lo=k*logs[0][1]+j*logs[1][1]+(n-k-j)*logs[2][1]<0
    strict_hi=k*logs[0][0]+(j+1)*logs[1][0]+(n-k-j-1)*logs[2][0]>0
    if not (0<=j<n-k and strict_lo and strict_hi):
        raise ArithmeticError('undecided likelihood sign')
    return j


def error_under(n,prob,logs,flat):
    low,weights,norm,tail_left,tail_right=binomial_weights(n,prob[0])
    theta=prob[1]/(1-prob[0])
    a=theta.numerator
    b=theta.denominator-a
    j=certified_threshold(n,low,logs)
    mass,cdf=get_state(n-low,theta,j)
    lower=upper=0
    for idx,w in enumerate(weights):
        k=low+idx
        m=n-k
        conditional=cdf if flat else (S-cdf[1],S-cdf[0])
        lower+=w[0]*max(0,conditional[0])
        upper+=w[1]*min(S,conditional[1])
        if idx+1==len(weights):
            break
        newj=certified_threshold(n,k+1,logs)
        # Bin(m,theta)=Bin(m-1,theta)+Bernoulli(theta). Thus F_{m-1}(j)
        # =F_m(j)+theta*f_{m-1}(j). The cutoff moves up by 0 or 1.
        mass=mul(mass,(m-j)*(a+b),m*b)
        cdf=add(cdf,mul(mass,a,a+b))
        if newj==j+1:
            mass=mul(mass,(m-1-j)*a,(j+1)*b)
            cdf=add(cdf,mass)
        elif newj!=j:
            raise ArithmeticError('unexpected conditional cutoff increment')
        j=newj
    return (F(lower,norm[1]*S), F(upper+(tail_left+tail_right)*S,norm[0]*S))


def readable(x,rounding):
    with localcontext() as ctx:
        ctx.prec=30
        ctx.rounding=rounding
        return str(Decimal(x.numerator)/Decimal(x.denominator))


def verify_gaussian_target():
    # Machin's pi identity, enclosed by alternating arctan series.
    def atan_bounds(x):
        s = sum((-1)**j*x**(2*j+1)/(2*j+1) for j in range(80))
        return s,s+x**161/161
    a,b=atan_bounds(F(1,5)),atan_bounds(F(1,239))
    pi=(16*a[0]-4*b[1],16*a[1]-4*b[0])
    rootlo=F(isqrt((2*pi[0]*S*S).__floor__()),S)
    roothi=F(isqrt((2*pi[1]*S*S).__floor__())+1,S)
    # Phi(-3) = 1/2 - 3/sqrt(2*pi) * sum of the integrated Gaussian series.
    terms=[F(-9,2)**k/((2*k+1)*factorial(k)) for k in range(121)]
    s=sum(terms[:120])
    if not (TARGET[0] < F(1,2)-3*(s+terms[120])/rootlo and
            F(1,2)-3*s/roothi < TARGET[1]):
        raise ArithmeticError('Gaussian target enclosure')


def audit():
    verify_gaussian_target()
    src=ROOT/'fenster.json'
    if hashlib.sha256(src.read_bytes()).hexdigest()!=SOURCE_HASH:
        raise ValueError('source sha256')
    row=next(x for x in json.loads(src.read_text()) if x['h']=='1/8')
    models=[]
    for k in ('flat','open'):
        v=[F(t) for t in row['backgrounds'][k]['cell_probabilities']]
        models.append([x/sum(v) for x in v])
    p,q=models
    logs=list(map(log_bounds,p,q))
    results=[]
    for n in (INITIAL_N-1,INITIAL_N):
        both=[error_under(n,p,logs,True),error_under(n,q,logs,False)]
        # An unnormalised input perturbation <=1e-24 per category changes
        # total variation after normalisation by <4e-24 per draw (L1 triangle
        # inequality, both input sums >0.999999). Product-TV <= n times this.
        tol=4*n*F(1,10**24)
        lo=sum(x[0] for x in both)/2-tol
        hi=sum(x[1] for x in both)/2+tol
        passes=(lo>TARGET[1]) if n<INITIAL_N else (hi<TARGET[0])
        if not passes:
            raise ArithmeticError('threshold not certified')
        results.append(dict(n=n,error_lower=readable(lo,ROUND_FLOOR),
                            error_upper=readable(hi,ROUND_CEILING),
                            nominal_conditional_error_bounds=[
                              [readable(x,ROUND_FLOOR),readable(y,ROUND_CEILING)] for x,y in both]))
    return dict(h='1/8',minimum_for_equal_prior_average_error=INITIAL_N,
                target='Phi(-3)',certificate=results)


if __name__=='__main__':
    data=audit()
    (ROOT/'exakte_schwelle.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
