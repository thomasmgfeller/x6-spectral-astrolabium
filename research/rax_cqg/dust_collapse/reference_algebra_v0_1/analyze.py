"""Exact finite controls and certified rational intervals; Python stdlib only."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial, isqrt
from functools import lru_cache
import hashlib, json, sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'inputs'))
from exact_core import C, as_c, matrix, mul, add, scale, dag, trace, outer, real, encode, require, gitsha, PHASES
ZERO = C()

def zero(n): return [[ZERO for _ in range(n)] for _ in range(n)]
def diag(xs):
    a=zero(len(xs))
    for i,x in enumerate(xs): a[i][i]=as_c(x)
    return a
def eye(n): return diag([1]*n)
def kron(a,b): return [[x*y for x in ar for y in br] for ar in a for br in b]
def expectation(e,rho):
    return real(sum((e[i][j]*rho[j][i] for i in range(len(e)) for j in range(len(e))),ZERO))
def commutes_diag(a,charges):
    return all(x*(charges[i]-charges[j])==ZERO for i,row in enumerate(a) for j,x in enumerate(row))
def twirl(a,charges):
    return [[x if charges[i]==charges[j] else ZERO for j,x in enumerate(row)] for i,row in enumerate(a)]
def effective(effect,sigma,ds):
    dr=len(sigma)
    return [[sum((sigma[n][r]*effect[i*dr+r][j*dr+n] for n in range(dr) for r in range(dr)),ZERO) for j in range(ds)] for i in range(ds)]
def magnitude(z):
    sq=z.norm2();n=isqrt(sq.numerator);d=isqrt(sq.denominator)
    require(n*n==sq.numerator and d*d==sq.denominator,'Rational magnitude in declared finite controls')
    return F(n,d)
def dump(name,value):
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/name).write_text(json.dumps(encode(value),indent=2,sort_keys=True)+'\n')
def outward_decimal(x,places,up=False):
    s=10**places;num=x.numerator*s;den=x.denominator
    k=-(-num//den) if up else num//den
    sign='-' if k<0 else '';k=abs(k)
    return sign+str(k//s)+'.'+str(k%s).zfill(places)
def atan_interval(x,terms):
    require(terms%2==0,'Even alternating partial sum')
    lo=sum(((-1)**k*x**(2*k+1)/F(2*k+1) for k in range(terms)),F(0))
    return lo,lo+x**(2*terms+1)/F(2*terms+1)
def pi_interval(plan):
    a,b=atan_interval(F(1,5),plan['atan_terms']),atan_interval(F(1,239),plan['atan_terms'])
    lo,hi=16*a[0]-4*b[1],16*a[1]-4*b[0]
    d=plan['pi_round_digits']
    return F(outward_decimal(lo,d)),F(outward_decimal(hi,d,True))
def bounds_factory(plan):
    plo,phi=pi_interval(plan);degree=plan['cos_degree']
    require(degree%2==0,'Even cosine degree')
    def poly(x):return sum(((-1)**k*x**(2*k)/factorial(2*k) for k in range(degree//2+1)),F(0))
    @lru_cache(None)
    def cosine(L):
        require(L>=0,'Nonnegative finite ladder length')
        if L==0:return F(0),F(0)
        lo,hi=plo/F(L+2),phi/F(L+2)
        # Taylor through degree+1 has the same polynomial; derivative bound is 1.
        return poly(hi)-hi**(degree+2)/factorial(degree+2),poly(lo)+lo**(degree+2)/factorial(degree+2)
    def tau(L):
        lo,hi=cosine(L)
        return max(F(0),(1-hi)/2),min(F(1,2),(1-lo)/2)
    return (plo,phi),cosine,tau

def run():
    plan=json.loads((ROOT/'plan.json').read_text())
    plan_sha=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(plan_sha==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    provenance=json.loads((ROOT/'provenance.json').read_text())
    for name,info in provenance['inputs'].items():
        require(gitsha((ROOT/name).read_bytes())==info['git_blob'],'Pinned source '+name)
    require(not plan['physical_algebra_selected'] and not plan['charge_is_physical_dust_mass'],'Conditional charge and algebra only')
    require(not plan['paid_compute'] and not plan['n5_production'],'No paid or production run')
    require(set(plan['physical_gates'].values())=={'HOLD'},'Physical gates remain HOLD')
    pi_bounds,cos_bounds,tau_bounds=bounds_factory(plan)

    # Compatible algebras containing the same declared diagonal records/action.
    charge=[0,1,0,1];rho=scale(outer([1,1,0,0]),F(1,2));dephased=twirl(rho,charge)
    pa=diag([1,0,1,0]);action_rows=[];block_count=0
    for h in map(F,plan['algebra_h']):
        s1=-F(1,3)*(F(1,2)+4*h*h*F(1,4)**2)
        s2=-F(1,2)*(F(1,2)+4*h*h*F(3,4)**2)
        action=diag([0,s1,0,s2])
        require(commutes_diag(action,charge),'Record action is block preserving')
        for i in range(4):
            for j in range(4):
                if charge[i]!=charge[j]:continue
                b=zero(4);b[i][j]=as_c(1)
                require(mul(pa,b)==mul(b,pa),'Centrality in block algebra')
                # Matrix units are a spanning algebra basis, not all individual effects.
                require(trace(mul(b,rho))==trace(mul(b,dephased)),'Block algebra cannot distinguish twirl')
                block_count+=1
        action_rows.append({'h':h,'action_diagonal':[0,s1,0,s2]})
    require(mul(pa,rho)!=mul(rho,pa),'Same record projector noncentral in full algebra')
    require(expectation(rho,rho)==1 and expectation(rho,dephased)==F(1,2),'Full algebra distinguishes same block records')

    # Charge conserving exchange, without separate subsystem charge conservation.
    u=eye(4);indices=[1,2];r,t=map(F,plan['exchange_rotation'])
    for i,row in enumerate([[r,t],[-t,r]]):
        for j,x in enumerate(row):u[indices[i]][indices[j]]=as_c(x)
    total=[0,1,1,2];local=[0,0,1,1]
    require(mul(dag(u),u)==eye(4),'Exact exchange unitarity')
    require(commutes_diag(u,total) and not commutes_diag(u,local),'Global conservation permits subsystem exchange')
    algebra={'action_controls':action_rows,'block_basis_controls':block_count,
        'compatible_algebras':['B(H_a) direct_sum B(H_c)','B(H_a direct_sum H_c)'],
        'full_algebra_probabilities':[1,F(1,2)],'exchange_unitary':u,
        'global_charge_conserved':True,'subsystem_charge_separately_conserved':False,
        'physical_algebra_selected':False,'sector_label_is_dust_mass':False}
    dump('algebra_and_conservation.json',algebra)

    states={'a':diag([1,0,0]),'c':diag([0,1,0]),'leak':diag([0,0,1]),
        'plus':scale(outer([1,1,0]),F(1,2)), 'minus':scale(outer([1,-1,0]),F(1,2)),
        'plus_i':scale(outer([1,C(F(0),F(1)),0]),F(1,2))}
    target=states['plus'];rows=[];probability_checks=0;diagonal_cases=0;example=None
    leakage_witness=None;endpoint_witness=None
    for L in plan['reference_L']:
        d=L+1;charges=[q+n for q in [0,1,0] for n in range(d)]
        for profile in plan['profiles']:
            amps={'uniform':[1]*d,'ramp':list(range(1,d+1)),
                  'tent':[min(n+1,d-n) for n in range(d)],'edge':[1]+[0]*(d-1)}[profile]
            norm=sum(x*x for x in amps)
            for eta in map(F,plan['coherence']):
                for phase in plan['phases']:
                    z=PHASES[phase];v=[];power=as_c(1)
                    for a in amps:v.append(a*power);power=power*z
                    sig=add(scale(outer(v),eta/F(norm)),diag([(1-eta)*F(a*a,norm) for a in amps]))
                    require(trace(sig)==as_c(1) and sig==dag(sig),'Reference density trace and adjoint')
                    # Positivity follows exactly from this convex mixture of projectors.
                    fx=zero(3*d)
                    for j in range(2*d):fx[j][j]=as_c(F(1,2))
                    coherence=F(0)
                    for n in range(L):
                        b=sig[n][n+1];m=magnitude(b);coherence+=m
                        align=scale([[b.conj()]],1/m)[0][0] if m else as_c(1)
                        x,y=n+1,d+n;off=F(1,2)*align
                        fx[x][y]=off;fx[y][x]=off.conj()
                        block=[[fx[x][x],off],[off.conj(),fx[y][y]]]
                        require(mul(block,block)==block and trace(block)==as_c(1),'Each active charge doublet is a rank-one effect')
                    require(fx==dag(fx) and commutes_diag(fx,charges),'Invariant Hermitian joint effect')
                    # Other orthogonal blocks: two endpoint effects 1/2 and leakage effect 0.
                    require(fx[0][0]==fx[2*d-1][2*d-1]==as_c(F(1,2)),'Unpaired endpoints included')
                    require(all(fx[i][j]==ZERO for i in range(2*d,3*d) for j in range(3*d)),'Full leakage complement rejected')
                    failure=add(eye(3*d),scale(fx,-1))
                    require(add(fx,failure)==eye(3*d),'Both measurement outcomes retained')
                    e=effective(fx,sig,3)
                    expected=matrix([[F(1,2),coherence/2,0],[coherence/2,F(1,2),0],[0,0,0]])
                    require(e==expected,'Induced effect saturates adjacent coherence bound')
                    error=add(e,scale(target,-1));delta=(1-coherence)/2
                    require(mul(error,error)==diag([delta*delta,delta*delta,0]),'Exact universal full-space norm error')
                    require(F(0)<=coherence<=cos_bounds(L)[1],'Finite-support reference upper bound')
                    if eta==0 or profile=='edge' or L==0:
                        require(coherence==0 and delta==F(1,2),'No adjacent reference coherence gives half bound');diagonal_cases+=1
                    probabilities={}
                    for name in plan['system_states']:
                        state=states[name];joint=kron(state,sig)
                        p=expectation(fx,joint);p_reduced=expectation(e,state)
                        p_twirl=expectation(fx,twirl(joint,charges))
                        require(p==p_reduced==p_twirl and 0<=p<=1,'Born reduction and global twirl statistics')
                        probabilities[name]=p;probability_checks+=1
                    if L==1 and profile=='uniform' and eta==1 and phase=='1':
                        require(probabilities['plus']==F(3,4) and probabilities['minus']==F(1,4),'Relational phase witness')
                        jt=twirl(kron(states['plus'],sig),charges)
                        marginal=[[sum((jt[i*d+n][j*d+n] for n in range(d)),ZERO) for j in range(3)] for i in range(3)]
                        require(marginal==diag([F(1,2),F(1,2),0]),'Local marginal dephased despite relational signal')
                        example={'probabilities':probabilities,'system_marginal':marginal,'joint_twirl':jt,'effect':e}
                        bad=add(fx,kron(diag([0,0,1]),eye(d)))
                        ebad=effective(bad,sig,3)
                        require(ebad[0][:2]==e[0][:2] and ebad[1][:2]==e[1][:2],'Unchanged target compression')
                        require(expectation(ebad,states['leak'])==1,'Uncontrolled complement error one')
                        leakage_witness={'good_leak_probability':0,'bad_leak_probability':1,'bad_full_norm_error':1,'two_mode_error':delta}
                        omitted=[row[:] for row in fx];omitted[0][0]=ZERO;omitted[2*d-1][2*d-1]=ZERO
                        e_omitted=effective(omitted,sig,3)
                        endpoint_witness={'complete_plus_probability':probabilities['plus'],
                            'omitted_plus_probability':expectation(e_omitted,states['plus'])}
                        require(endpoint_witness['omitted_plus_probability']==F(1,2),'Omitted endpoints change unconditional readout')
                    rows.append({'L':L,'profile':profile,'eta':eta,'phase':phase,'adjacent_coherence':coherence,'tau':delta,'probabilities':probabilities})
    require(example is not None and leakage_witness is not None,'Declared examples present')
    dump('finite_reference_effects.json',{'cases':rows,'born_and_twirl_controls':probability_checks,
        'incoherent_reference_controls':diagonal_cases,'relational_example':example,'leakage_counterexample':leakage_witness,
        'endpoint_counterexample':endpoint_witness,
        'scope':'Finite exact controls of a conditional charge model, not a physical CST detector or continuum discretization.'})

    budgets=[]
    for L in plan['budget_L']:
        lo,hi=tau_bounds(L)
        budgets.append({'L':L,'levels':L+1,'tau_interval':[lo,hi],
            'tau_decimal_outward':[outward_decimal(lo,15),outward_decimal(hi,15,True)],
            'uniform_tau':F(1,2*(L+1))})
    thresholds=[]
    for goal in map(F,plan['target_tolerances']):
        found=None
        for L in range(plan['search_max_L']+1):
            lo,hi=tau_bounds(L)
            if hi<=goal:found=L;break
        require(found is not None,'Threshold found within frozen search range')
        require(found==0 or tau_bounds(found-1)[0]>goal,'Previous support provably insufficient')
        thresholds.append({'target_tau':goal,'minimum_L':found,'minimum_levels':found+1,
            'tau_interval':tau_bounds(found),'previous_tau_interval':tau_bounds(found-1) if found else None})
    require([r['minimum_L'] for r in thresholds]==[3,14,48,156],'Threshold regression')
    dump('reference_budgets.json',{'pi_interval':pi_bounds,'rows':budgets,'thresholds':thresholds,
        'method':'Machin formula, alternating arctangent bounds, outward rational rounding, Taylor remainder',
        'formula':'tau_min(L) = (1-cos(pi/(L+2)))/2','single_use_only':True,
        'reference_label_is_cost_or_causalset_size':False})

    negative=[]
    def reject(name,fn):
        try:fn()
        except RuntimeError:negative.append({'case':name,'status':'REJECTED'});return
        raise RuntimeError('Negative control unexpectedly accepted: '+name)
    reject('record action commutation selects central sector in full algebra',lambda:require(mul(pa,rho)==mul(rho,pa),'Noncentral full algebra witness'))
    reject('global charge conservation implies subsystem conservation',lambda:require(commutes_diag(u,local),'Allowed charge exchange'))
    diagonal_row=next(row for row in rows if row['L']==2 and row['eta']==0)
    reject('diagonal reference removes half error bound',lambda:require(diagonal_row['tau']<F(1,2),'Measured matrix error with C=0'))
    reject('finite reference achieves exact target',lambda:require(tau_bounds(255)[1]==0,'Strict finite-support bound'))
    reject('two-mode compression certifies full-space effect',lambda:require(leakage_witness['two_mode_error']==leakage_witness['bad_full_norm_error'],'Leakage witness'))
    reject('unpaired endpoint outcomes can be discarded',lambda:require(endpoint_witness['complete_plus_probability']==endpoint_witness['omitted_plus_probability'],'Unconditional endpoint contribution'))
    reject('sector charge already derived as dust mass',lambda:require(plan['charge_is_physical_dust_mass'],'No physical identification'))
    reject('changed pinned input accepted',lambda:require(gitsha((ROOT/'inputs/variation_DERIVATION.md').read_bytes()+b' ')==provenance['inputs']['inputs/variation_DERIVATION.md']['git_blob'],'Source identity'))
    result={'status':'PASS_CONDITIONAL_ALGEBRA_AND_REFERENCE_AUDIT','plan_sha256':plan_sha,
        'algebra_basis_controls':block_count,'exchange_unitarity_controls':1,'reference_effect_cases':len(rows),
        'born_and_twirl_controls':probability_checks,'incoherent_reference_controls':diagonal_cases,
        'certified_budget_rows':len(budgets),'certified_thresholds':len(thresholds),'negative_controls':negative,
        'physical_gates':plan['physical_gates'],'physical_algebra_selected':False,'physical_charge_derived':False,
        'physical_reference_prepared':False,'physical_detector_derived':False,
        'external_replication':False,'paid_compute':False,'n5_production_run':False}
    dump('verification.json',result);return result

if __name__=='__main__':print(json.dumps(encode(run()),indent=2,sort_keys=True))
