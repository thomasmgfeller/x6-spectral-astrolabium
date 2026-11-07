"""Exact controls for conditional operational closure; Python stdlib only."""
from pathlib import Path
from fractions import Fraction as F
from math import comb, factorial, isqrt
from dataclasses import dataclass
import hashlib, json
ROOT=Path(__file__).resolve().parent

def require(ok, message):
    if not ok: raise RuntimeError(message)

@dataclass(frozen=True)
class C:
    r: F=F(0)
    i: F=F(0)
    def __add__(self, other):
        o=as_c(other);return C(self.r+o.r,self.i+o.i)
    __radd__=__add__
    def __neg__(self): return C(-self.r,-self.i)
    def __sub__(self, other): return self+-as_c(other)
    def __mul__(self, other):
        o=as_c(other);return C(self.r*o.r-self.i*o.i,self.r*o.i+self.i*o.r)
    __rmul__=__mul__
    def conj(self): return C(self.r,-self.i)
    def norm2(self): return self.r*self.r+self.i*self.i

def as_c(x): return x if isinstance(x,C) else C(F(x))
def matrix(rows): return [[as_c(x) for x in row] for row in rows]
def mul(a,b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))),C()) for j in range(len(b[0]))] for i in range(len(a))]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,s): return [[s*x for x in row] for row in a]
def dag(a): return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]
def trace(a): return sum((a[i][i] for i in range(len(a))),C())
def outer(v): return [[as_c(x)*as_c(y).conj() for y in v] for x in v]
def real(x): require(x.i==0,'Real probability');return x.r
I=matrix([[1,0],[0,1]])
P=matrix([[F(1,2),F(1,2)],[F(1,2),F(1,2)]])
Q=add(I,scale(P,-1))
PHASES={'1':C(F(1)),'-1':C(F(-1)),'i':C(F(0),F(1)),'-i':C(F(0),F(-1))}
def density(eta): return matrix([[F(1,2),eta/2],[eta/2,F(1,2)]])
def effect(kappa): return density(kappa)
def evolve(d,rho): return mul(mul(d,rho),dag(d))
def prob(e,rho): return real(trace(mul(e,rho)))
def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,C): return {'re':str(x.r),'im':str(x.i)}
    if isinstance(x,dict): return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [encode(v) for v in x]
    return x
def dump(name,x):
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/name).write_text(json.dumps(encode(x),indent=2,sort_keys=True)+'\n')
def gitsha(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def clock_moment(k,h):
    return sum((F(comb(k,j),2*j+1)*F(1,2)**(k-j)*(4*h*h)**j for j in range(k+1)),F(0))

def continuous_components(h,mu,degree):
    # U=w(1/2+4h^2 x^2) with x,w independently uniform on (0,1).
    moments=[clock_moment(k,h)/F(k+1) for k in range(degree+1)]
    re_coeff=[];abs_coeff=[]
    for k in range(0,degree+1,2):
        re_coeff.append(F((-1)**(k//2),factorial(k))*moments[k])
        diff=sum(((-1)**j*comb(k,j)*moments[k-j]*moments[j] for j in range(k+1)),F(0))
        require(diff>=0,'Even continuous difference moment')
        abs_coeff.append(F((-1)**(k//2),factorial(k))*diff)
    re=sum((c*mu**(2*j) for j,c in enumerate(re_coeff)),F(0))
    ab=sum((c*mu**(2*j) for j,c in enumerate(abs_coeff)),F(0))
    amax=F(1,2)+4*h*h
    rem=(abs(mu)*amax)**(degree+2)/factorial(degree+2)
    return re,ab,rem,re_coeff,abs_coeff

def sqrt_upper(x,denominator=10**12):
    require(x>=0,'Nonnegative square root')
    n,d=x.numerator,x.denominator
    k=isqrt(n*denominator*denominator//d)
    if k*k*d<n*denominator*denominator:k+=1
    y=F(k,denominator)
    require(y*y>=x and (k==0 or F(k-1,denominator)**2<x),'Outward square root')
    return y

def run():
    plan=json.loads((ROOT/'plan.json').read_text())
    plan_sha=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(plan_sha==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    for name,info in json.loads((ROOT/'provenance.json').read_text())['inputs'].items():
        require(gitsha((ROOT/name).read_bytes())==info['git_blob'],'Pinned source '+name)
    etas=list(map(F,plan['eta']));kappas=list(map(F,plan['kappa']))
    old=json.loads((ROOT/'inputs/previous_one_element_witnesses.json').read_text())
    oldrows={(F(x['h']),F(x['mu'])):x for x in old['channels'] if F(x['theta'])==0}
    continuous=[];baseline_controls=0;degeneracy=0
    for h in map(F,plan['h']):
        for mu in map(F,plan['mu']):
            re,ab,rem,rc,ac=continuous_components(h,mu,plan['cosine_degree'])
            groups={}
            for eta in etas:
                for kappa in kappas:
                    t=eta*kappa;center=(1+ab+2*t*re)/4;radius=(1+2*abs(t))*rem/4
                    interval=[max(F(0),center-radius),min(F(1),center+radius)]
                    require(interval[0]<=interval[1],'Nonempty probability enclosure')
                    if mu==0:require(interval==[(1+t)/2]*2,'Zero-phase calibration law')
                    if t in groups:require(groups[t]==interval,'Only product eta*kappa identifiable');degeneracy+=1
                    else:groups[t]=interval
                    if eta==kappa==1 and mu:
                        prior=list(map(F,oldrows[(h,mu)]['visibility_interval']))
                        require(max(interval[0],prior[0])<=min(interval[1],prior[1]),'Published reference enclosure recovered')
                        require(center==F(oldrows[(h,mu)]['visibility_center']),'Independent mixture/difference-moment polynomial identity')
                        baseline_controls+=1
                    continuous.append({'h':h,'mu':mu,'eta':eta,'kappa':kappa,'eta_kappa':t,'success_interval':interval,'center':center,'radius':radius})
    dump('continuous_readout.json',{'cases':continuous,'reference_recoveries':baseline_controls,
         'identical_product_controls':degeneracy,'scope':'Conditional n=1; only atom-versus-continuous coherence varied. Internal continuous/clock coherence stays fixed.'})

    finite=[];transport_count=sequences=completeness=0
    for s0,s1 in (map(F,row) for row in plan['transport_scales']):
        u=matrix([[s0,0],[0,s1]]);ui=matrix([[1/s0,0],[0,1/s1]])
        metric=mul(dag(u),u);mi=mul(ui,dag(ui))
        sharp=lambda a:mul(mul(mi,dag(a)),metric)
        trans=lambda a:mul(mul(ui,a),u)
        ks=[trans(P),trans(Q)]
        require(add(mul(sharp(ks[0]),ks[0]),mul(sharp(ks[1]),ks[1]))==I,'Weighted Kraus completeness');completeness+=1
        for eta in etas:
            rho=density(eta);rt=trans(rho)
            require(trace(rt)==C(F(1)) and sharp(rt)==rt,'Weighted density trace and adjoint')
            for phase in plan['finite_phases']:
                z=PHASES[phase];d=matrix([[1,0],[0,z]])
                sig=evolve(d,rho);dt=trans(d);sigt=mul(mul(dt,rt),sharp(dt))
                require(mul(sharp(dt),dt)==I,'Weighted phase unitary')
                for kappa in kappas:
                    e=effect(kappa);et=trans(e)
                    require(sharp(et)==et,'Weighted effect adjoint')
                    p=prob(e,sig);pt=real(trace(mul(et,sigt)))
                    require(p==pt==(1+eta*kappa*z.r)/2,'Probability and representation covariance')
                    transport_count+=1
                    if s0==s1==1:finite.append({'eta':eta,'kappa':kappa,'phase':phase,'p':p})
                for k,kt in zip([P,Q],ks):
                    first=mul(mul(k,sig),dag(k));firstt=mul(mul(kt,sigt),sharp(kt))
                    for l,lt in zip([P,Q],ks):
                        second=mul(mul(l,first),dag(l));secondt=mul(mul(lt,firstt),sharp(lt))
                        require(real(trace(second))==real(trace(secondt)),'Sequential instrument covariance');sequences+=1
    zmat=matrix([[1,0],[0,-1]])
    same_effect=mul(dag(mul(zmat,P)),mul(zmat,P))
    require(same_effect==P,'Alternative Kraus update has same effect')
    state_a=mul(mul(P,P),P);state_b=mul(mul(mul(zmat,P),P),dag(mul(zmat,P)))
    require(prob(P,state_a)==1 and prob(P,state_b)==0,'Follow-up readout separates instruments')
    dump('instrument_covariance.json',{'finite_cases':finite,'weighted_probability_controls':transport_count,
         'sequential_controls':sequences,'weighted_completeness_controls':completeness,
         'same_effect_different_update':{'initial_success':'1','followup_luders':'1','followup_phase_flip':'0'},
         'scope':'Finite algebraic controls, not a quadrature or physical detector implementation.'})

    vectors=[tuple(map(F,row)) for row in plan['calibration_pythagorean']]
    states=[outer((a,sign*b)) for a,b in vectors for sign in [1,-1]]+[density(eta) for eta in etas]
    calibration=[]
    for a,b in vectors:
        e=outer((a,b));require(mul(e,e)==e and trace(e)==C(F(1)),'Rank-one target projector')
        for n,rho in enumerate(states):
            eps=1-prob(e,rho);require(0<=eps<=1,'Calibration deficit')
            for phase in plan['finite_phases']:
                z=PHASES[phase];d=matrix([[1,0],[0,z]])
                actual=prob(e,evolve(d,rho));target=prob(e,evolve(d,e))
                require(target==(C(a*a)+b*b*z).norm2(),'Matched pure return equals characteristic visibility')
                gap=abs(actual-target);require(gap*gap<=eps,'Pure-target trace-distance calibration bound')
                if eps==0:require(rho==e and gap==0,'Perfect calibration closes the preparation')
                calibration.append({'target':[a,b],'state_index':n,'phase':phase,'epsilon':eps,'probability_gap':gap})
    budgets=[]
    for row in plan['error_budgets']:
        eps,tau,delta=(F(row[k]) for k in ['epsilon','tau','delta'])
        upper=min(F(1),tau+sqrt_upper(min(F(1),eps+tau))+4*delta)
        budgets.append({**row,'probability_error_upper':upper,'experimental_status':'NOT_MEASURED_DIAGNOSTIC_BUDGET'})
    dump('calibration_bounds.json',{'exact_matrix_controls':calibration,'diagnostic_budgets':budgets,
         'bound':'min(1, tau + sqrt(min(1, epsilon+tau)) + 4*delta)',
         'delta_scope':'Total variation of the full joint classical record law, not merely a finite set of moments or marginals.'})

    negative=[]
    def reject(name,fn):
        try:fn()
        except RuntimeError:negative.append({'case':name,'status':'REJECTED'});return
        raise RuntimeError('Negative control not rejected: '+name)
    reject('diagonal data determine coherence',lambda:require(prob(P,density(F(1)))==prob(P,density(F(-1))),'Same diagonal, different filter'))
    reject('zero-phase success alone certifies a rank-one detector',lambda:require(I==P,'Identity detector also passes zero-phase test'))
    reject('same effect determines state update',lambda:require(state_a==state_b,'Different post-measurement states'))
    reject('preparation and detector coherence separately identifiable',lambda:require((F(1),F(1,2))==(F(1,2),F(1)),'Only product identified'))
    u=matrix([[F(1,2),0],[0,F(3,2)]]);ui=matrix([[2,0],[0,F(2,3)]])
    pt=mul(mul(ui,P),u)
    reject('untransported effect under changed representation',lambda:require(prob(P,pt)==1,'Wrong effect representation'))
    reject('ordinary adjoint used in weighted representation',lambda:require(dag(pt)==pt,'Weighted adjoint required'))
    reject('invalid coherence parameter',lambda:require(abs(F(3,2))<=1,'Nonpositive state or effect'))
    reject('changed source byte',lambda:require(gitsha((ROOT/'inputs/previous_measure_derivation.md').read_bytes()+b' ')==json.loads((ROOT/'provenance.json').read_text())['inputs']['inputs/previous_measure_derivation.md']['git_blob'],'Source identity'))
    summary={'status':'PASS_CONDITIONAL_OPERATIONAL_AUDIT','plan_sha256':plan_sha,
       'continuous_cases':len(continuous),'reference_recoveries':baseline_controls,'product_degeneracy_checks':degeneracy,
       'weighted_probability_controls':transport_count,'sequential_controls':sequences,
       'calibration_controls':len(calibration),'negative_controls':negative,'physical_gates':plan['physical_gates'],
       'physical_selection_law':'NOT_DERIVED','rank_one_and_classical_law':'ADDITIONAL_OPERATIONAL_ASSUMPTIONS',
       'external_replication':False,'n5_production_run':False}
    dump('verification.json',summary);return summary

if __name__=='__main__':print(json.dumps(encode(run()),indent=2,sort_keys=True))
