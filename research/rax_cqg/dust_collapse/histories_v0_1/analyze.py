#!/usr/bin/env python3
"""Exact polynomial integrals and rational error bounds; standard library only."""
import hashlib, itertools, json, math
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def require(ok, message):
    if not ok: raise RuntimeError(message)
@dataclass(frozen=True)
class Z:
    re: F=F(0)
    im: F=F(0)
    def __add__(self,o):
        o=as_z(o); return Z(self.re+o.re,self.im+o.im)
    __radd__=__add__
    def __neg__(self): return Z(-self.re,-self.im)
    def __sub__(self,o): return self+-as_z(o)
    def __mul__(self,o):
        o=as_z(o); return Z(self.re*o.re-self.im*o.im,self.re*o.im+self.im*o.re)
    __rmul__=__mul__
    def __truediv__(self,o): return self*(F(1)/o)
    def conj(self): return Z(self.re,-self.im)
def as_z(x): return x if isinstance(x,Z) else Z(F(x))
ZERO=Z(); PHASE=[Z(F(1)),Z(F(0),F(-1)),Z(F(-1)),Z(F(0),F(1))]
def moment(k,lo=F(-1),hi=F(1)):
    return (hi**(k+1)-lo**(k+1))/F(2*(k+1))
def kernel_polynomial(p):
    # K(s)=1/2 + 1/2 sum_k (-i)^k Q(s)^k/[k! (k+1)].
    out=[ZERO]*(2*p+1);out[0]=Z(F(1,2))
    for k in range(p+1):
        for l in range(k+1):
            out[2*l]=out[2*l]+PHASE[k%4]*F(math.comb(k,l),2*math.factorial(k)*(k+1))*F(1,2)**(k-l)*F(1,4)**l
    return out
def branch(poly,lo=F(-1),hi=F(1),input_power=0):
    # Integral K(b-a) a^input_power da/2, coefficients in b.
    out=[ZERO]*len(poly)
    for degree,c in enumerate(poly):
        if c==ZERO:continue
        for j in range(degree+1):
            out[j]=out[j]+c*(math.comb(degree,j)*(-1)**(degree-j)*moment(degree-j+input_power,lo,hi))
    return out
def inner(p,q):
    out=ZERO
    for i,a in enumerate(p):
        if a==ZERO:continue
        for j,b in enumerate(q):
            if b!=ZERO and (i+j)%2==0:out=out+a.conj()*b*F(1,i+j+1)
    return out
def evaluate(poly,x):
    out=ZERO
    for a in reversed(poly):out=out*x+a
    return out
def decimal_bound(x,digits=24,upper=False):
    scale=10**digits;y=x*scale
    n=-((-y.numerator)//y.denominator) if upper else y.numerator//y.denominator
    sign='-' if n<0 else '';s=str(abs(n)).zfill(digits+1)
    return sign+s[:-digits]+'.'+s[-digits:]
def interval(lo,hi=None):
    hi=lo if hi is None else hi
    return {'lower':decimal_bound(lo),'upper':decimal_bound(hi,upper=True),
            'exact_lower':str(lo),'exact_upper':str(hi)}
def ratio(num,den):
    require(den[0]>0,'Positive denominator')
    vals=[x/y for x in num for y in den];return min(vals),max(vals)
def vector_inner(a,b):return sum((x.conj()*y for x,y in zip(a,b)),ZERO)
def cut_controls():
    v=[(Z(F(1)),ZERO),(ZERO,Z(F(1))),(Z(F(1)),Z(F(0),F(1)))]
    gram=lambda w:[[vector_inner(a,b) for b in w] for a in w]
    g=gram(v); checks=0
    for scale in [F(1),F(2)]:
        transformed=[(a*scale,b*Z(F(0),scale)) for a,b in v]
        gg=gram(transformed)
        for i,j in itertools.product(range(3),repeat=2):
            require(gg[i][j]==g[i][j]*(scale*scale),'Scaled isometry control');checks+=1
    bad=gram([(a,b*2) for a,b in v])
    require(bad[0][0]==g[0][0] and bad[1][1]==g[1][1]*4,'Non-isometry witness')
    checks+=2
    restricted=[(Z(F(i)),ZERO) for i in [1,2,3]]
    require(gram(restricted)==gram([(a,b*2) for a,b in restricted]),'Reachable subspace qualification');checks+=1
    return {'exact_checks':checks,'unitary_and_scaled_unitary':'PASS',
            'diag_1_2_all_branches':'FAIL_AS_UNCONDITIONED_EXTENSION',
            'diag_1_2_restricted_to_first_axis':'PASS',
            'relative_gram_diagonal_after_extension':['1','4'],
            'scope':'Abstract cut controls, not a CST gluing or Markov proof'}
def joint_measure_checks():
    def expand_linear(a,b,n):
        return {(k,n-k):F(math.comb(n,k))*a**k*b**(n-k) for k in range(n+1)}
    def independent(p,q,L):
        m=lambda k:F(0) if k%2 else L**k/F(k+1)
        return sum((F(math.comb(p,k)*math.comb(q,l)*(-1)**(p+q-k-l))*m(k)*m(l)*m(p+q-k-l)
                    for k in range(p+1) for l in range(q+1)),F(0))
    def chambers(p,q,L):
        total=F(0)
        for perm in itertools.permutations(range(3)):
            pos={perm[0]:(0,0),perm[1]:(1,0),perm[2]:(1,1)}
            a,b=pos[0][0]-pos[2][0],pos[0][1]-pos[2][1]
            c,d=pos[1][0]-pos[2][0],pos[1][1]-pos[2][1]
            for (i,j),x in expand_linear(a,b,p).items():
                for (k,l),y in expand_linear(c,d,q).items():
                    P,Q=i+k,j+l
                    total+=x*y*(2*L)**(P+Q)*F(math.factorial(P)*math.factorial(Q),math.factorial(P+Q+3))
        return total
    checks=0
    for L in [F(1,2),F(1),F(2)]:
        for p,q in itertools.product(range(5),repeat=2):
            require(chambers(p,q,L)==independent(p,q,L),'Doubled measure moment');checks+=1
        require(chambers(1,1,L)==L*L/3 and chambers(0,0,L)==1,'Shared-anchor covariance')
    return {'exact_moment_checks':checks,'method_1':'Six ordered chambers with rational Dirichlet integrals',
       'method_2':'Binomial moments of three independent uniform clocks',
       'shared_anchor_covariance':'L^2/3','independent_triangular_product_covariance':'0',
       'density':'[2L-max(0,r,r_prime)+min(0,r,r_prime)]_+/(2L)^3',
       'scope':'All three clocks free, common final clock in bra and ket; constant input state'}
def main():
    plan=json.loads((ROOT/'plan.json').read_text());p=plan['definitions']['taylor_degree']
    require(p==40,'Fixed degree')
    require(hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()==(ROOT/'plan.sha256').read_text().split()[0],'Plan hash')
    prov=json.loads((ROOT/'inputs/provenance.json').read_text())
    for name,entry in prov['files'].items():
        require(hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==entry['sha256'],'Input hash '+name)
    poly=kernel_polynomial(p)
    # Uniform exact complex remainder on a,b in [-1,1].
    r=F(3,2)**(p+1)/F(2*math.factorial(p+1)*(p+2));eps=2*r+r*r
    algebra=0
    for a,b in itertools.product([F(-1),F(-1,3),F(0),F(1,2),F(1)],repeat=2):
        q=F(1,2)+(b-a)**2/4
        direct=Z(F(1,2))+sum((PHASE[k%4]*q**k/F(2*math.factorial(k)*(k+1)) for k in range(p+1)),ZERO)
        require(evaluate(poly,b-a)==direct,'Independent polynomial evaluation');algebra+=1
    full=branch(poly);odd=branch(poly,input_power=1)
    z0=inner(full,full);z1=inner(odd,odd)*3
    require(z0.im==z1.im==0 and inner(full,odd)==ZERO,'Norm reality and parity')
    i0=(z0.re-eps,z0.re+eps);i1=(z1.re-eps,z1.re+eps)
    require(i1[0]>0 and i0[0]>i1[1],'Disjoint continuum norm enclosures')
    mixture=ratio(i0,(i0[0]+i1[0],i0[1]+i1[1]))
    require(mixture[0]>F(1,2),'Conditional mixture differs from original half')
    bounds=[F(-1),F(-1,3),F(1,3),F(1)]
    vec=[branch(poly,bounds[i],bounds[i+1]) for i in range(3)]
    require(all(sum((v[k] for v in vec),ZERO)==full[k] for k in range(len(full))),'Partition integration')
    gram=[[None]*3 for _ in range(3)]
    for i in range(3):
        for j in range(i,3):
            gram[i][j]=inner(vec[i],vec[j]);gram[j][i]=gram[i][j].conj()
    event=lambda a,b:sum((gram[i][j] for i in range(3) if a>>i&1 for j in range(3) if b>>j&1),ZERO)
    checks={'hermiticity':0,'biadditivity':0,'normalization':1,'grade_two':0,'positive_quadratic_probes':0}
    require(event(7,7)==z0,'Full event norm')
    for a,b in itertools.product(range(8),repeat=2):
        require(event(a,b)==event(b,a).conj(),'Hermiticity');checks['hermiticity']+=1
        if not a&b:
            for c in range(8):
                require(event(a|b,c)==event(a,c)+event(b,c),'Additivity first')
                require(event(c,a|b)==event(c,a)+event(c,b),'Additivity second');checks['biadditivity']+=2
    for a,b,c in itertools.product(range(8),repeat=3):
        if a&b or a&c or b&c:continue
        mu=lambda e:event(e,e)
        require(mu(a|b|c)==mu(a|b)+mu(a|c)+mu(b|c)-mu(a)-mu(b)-mu(c),'Grade two');checks['grade_two']+=1
    for coeff in itertools.product([Z(F(-1)),ZERO,Z(F(1)),Z(F(0),F(1))],repeat=3):
        q=sum((coeff[i].conj()*gram[i][j]*coeff[j] for i in range(3) for j in range(3)),ZERO)
        require(q.im==0 and q.re>=0,'Positive exact Gram probe');checks['positive_quadratic_probes']+=1
    trace=sum((gram[i][i].re for i in range(3)),F(0))
    trace_norm=ratio((trace-3*eps,trace+3*eps),i0)
    require(trace_norm[1]<1,'Interference precludes probability interpretation')
    re01=ratio((gram[0][1].re-eps,gram[0][1].re+eps),i0)
    require(re01[0]>0,'Certified interference')
    results={
      'continuum_certificates.json':{'L':'1','p':p,'kernel_remainder':str(r),'gram_error':str(eps),
        'Z_constant_mode':interval(*i0),'Z_linear_normalized_mode':interval(*i1),
        'equal_prior_flag0_after_conditioning':interval(*mixture),
        'prior_flag0':'1/2','parity_overlap':'0 (exact, also for untruncated kernel)',
        'method':'Exact polynomial integration, rational complex remainder, outward decimals'},
      'history_events.json':{'atoms':['[-1,-1/3)','[-1/3,1/3)','[1/3,1]'],'events':8,
        'normalized_gram':[[{'real':interval(*ratio((g.re-eps,g.re+eps),i0)),
                            'imag':interval(*ratio((g.im-eps,g.im+eps),i0))} for g in row] for row in gram],
        'sum_diagonal':interval(*trace_norm),'real_D01':interval(*re01),
        'exact_polynomial_checks':checks,'strong_positivity':'PROVED_BY_GRAM_FORM_NOT_BY_FINITE_PROBES',
        'ordinary_probabilities':'NOT_JUSTIFIED_FOR_THIS_INTERFERING_PARTITION'},
      'cut_controls.json':cut_controls(),
      'joint_relative_measure.json':joint_measure_checks(),
      'verification.json':{'audit':plan['id'],'source_commit':plan['source_commit'],
        'plan_sha256':hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest(),
        'source_files_byte_verified':len(prov['files']),'polynomial_evaluation_checks':algebra,
        'exact_event_checks':checks,'scoped_decisions':{
          'FINITE_AUXILIARY_STRONGLY_POSITIVE_D':'PASS_CONDITIONAL_ON_DECLARED_BOUNDARY_PRODUCT',
          'SINGLE_CONSTANT_NORMALIZATION_ALL_CONTINUUM_STATES':'FAIL_FOR_RAW_COMPACT_KERNEL_FAMILY',
          'NORMALIZED_D_IS_AUTOMATIC_PROBABILITY':'FAIL_FOR_INTERFERING_PARTITION',
          'MARKOV_CUT_MAP_FOR_FULL_CST':'NOT_DERIVED',
          'PHYSICAL_DECOHERENCE_FUNCTIONAL':'HOLD',
          'INFINITE_HISTORY_EXTENSION':'NOT_EXECUTED'},
        'physical_decisions':plan['physical_decisions'],'formal_proof_checker':False,
        'new_dynamical_CST_ensembles':False,'reference_tests_are_physical_measurements':False}}
    results['verification.json']['supplement_01_sha256']=hashlib.sha256((ROOT/'supplement_01.json').read_bytes()).hexdigest()
    (ROOT/'results').mkdir(exist_ok=True)
    for name,data in results.items():(ROOT/'results'/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'PASS','files':len(results),'norm_constant':[float(x) for x in i0],
      'norm_linear':[float(x) for x in i1],'conditional_mixture':[float(x) for x in mixture],
      'sum_diagonal':[float(x) for x in trace_norm],'checks':checks},indent=2))
if __name__=='__main__':main()
