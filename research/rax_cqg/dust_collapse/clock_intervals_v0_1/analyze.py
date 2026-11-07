"""Exact finite controls plus explicit scope for analytic infinite statements."""
from fractions import Fraction as F
from itertools import combinations,product
from math import factorial
from pathlib import Path
import hashlib
import json
import intervals as v

ROOT=Path(__file__).resolve().parent
PLAN=json.loads((ROOT/'plan.json').read_text())
CONTROLS=PLAN['controls']
OUT=ROOT/'results'


def require(ok,message):v.require(ok,message)


def dump(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2,default=lambda x:str(x))+'\n')


def sources():
    digest=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(digest==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    prov=json.loads((ROOT/'inputs/provenance.json').read_text())
    require(prov['commit']==PLAN['source_commit'],'Source commit')
    for name,r in prov['files'].items():
        b=(ROOT/'inputs'/name).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['sha'],name)
    return digest,len(prov['files'])


def counts():
    cap=CONTROLS['max_total_elements'];census=[];records=[];checks=0
    for n in range(cap+1):
        orders=v.brute_orders(n)
        require(set(orders)==set(v.m.natural_orders(n)),'Independent order census')
        census.append(len(orders))
    for n in range(CONTROLS['max_parent_elements']+1):
        for p in v.brute_orders(n):
            e=[]
            for k in range(cap-n+1):
                count=v.continuations(p,k)
                require(count==len(v.descendants(p,k)),'Independent continuation count')
                require(count<=2**(n*k+k*(k-1)//2),'Elementary branching upper bound')
                e.append(count);checks+=1
            records.append({'parent':p,'continuations':e,'raw_norm_coefficients':v.coefficients(p,cap)})
    ac=(0,0);chain=(0,1);h=F(1,4)
    witnesses={'cap':3,'h':h,'antichain_norm_squared':v.partition(ac,h,3),
               'chain_norm_squared':v.partition(chain,h,3)}
    require(witnesses['antichain_norm_squared']==2 and
            witnesses['chain_norm_squared']==F(7,4),'Geometry-dependent raw norm')
    dump('counts_norms.json',{'natural_order_census':census,'independent_counts':checks,
        'records':records,'raw_norm_witness':witnesses,
        'no_birth_contribution':'1; raw norm is greater than one if births are allowed'})


def sewing():
    grid=tuple(map(F,CONTROLS['clock_grid']));cuts=[tuple(map(F,x)) for x in CONTROLS['clock_cuts']]
    marked=phase_checks=kernel_checks=0
    for n in range(CONTROLS['marked_max_elements']+1):
        for p in v.brute_orders(n):
            for t in combinations(grid,n):
                for w in product(map(F,CONTROLS['binary_density_marks']),repeat=n):
                    state=p,t,w
                    require(v.action(state)==v.action_by_increments(state),'Increment/full-action identity')
                    marked+=1
                    for a,b,c in cuts:
                        xa,xb,xc=(v.cut(state,tau) for tau in (a,b,c))
                        sa,sb,sc=map(v.action,(xa,xb,xc))
                        ia,ib,ic=map(v.action_by_increments,(xa,xb,xc))
                        require(tuple(sc[j]-sa[j] for j in range(2))==
                                tuple((ic[j]-ib[j])+(ib[j]-ia[j]) for j in range(2)),
                                'Full-past action sewing')
                        phase_checks+=1
                        m0,n1,n2=map(lambda x:len(x[0]),(xa,xb,xc))
                        for alpha in CONTROLS['alpha_values']:
                            require(v.number_weight_squared(m0,n2-m0,alpha)==
                                    v.number_weight_squared(m0,n1-m0,alpha)*
                                    v.number_weight_squared(n1,n2-n1,alpha),'Count-weight cocycle')
                            kernel_checks+=1
    complete=((0,1),(F(0),F(1,2)),(F(0),F(1,2)))
    old=(complete[0][:1],complete[1][:1],complete[2][:1])
    isolated=((0,),(F(1,2),),(F(1,2),))
    full_delta=tuple(x-y for x,y in zip(v.action(complete),v.action(old)))
    wrong_delta=tuple(x-y for x,y in zip(v.action(isolated),v.action(((),(),()))))
    require(full_delta!=wrong_delta,'Missing past must be detected')
    factorial_controls=[]
    for z in map(F,CONTROLS['amplitude_fugacities']):
        for j in range(1,4):
            for k in range(1,4):
                require(z**(j+k)==z**j*z**k,'Fugacity multiplication')
                require(z**(j+k)/factorial(j+k)!=z**(j+k)/(factorial(j)*factorial(k)),
                        'Extra factorial negative control')
                factorial_controls.append({'z':z,'first_births':j,'second_births':k})
    dump('interval_sewing.json',{'marked_records':marked,'full_action_cut_checks':phase_checks,
        'count_cocycle_checks':kernel_checks,'extra_factorial_negative_controls':len(factorial_controls),
        'missing_past_example':{'state':complete,'correct_increment':full_delta,
                                'incorrect_isolated_increment':wrong_delta},
        'per_interval_cap_negative_control':{'cap_per_interval':1,'births_first':1,'births_second':1,
            'direct_two_birth_amplitude':0,'sewn_two_birth_coefficient_at_z_1':1},
        'composition':'PASS with one global cap and complete past; the unique clock cut is not an extra history sum'})


def entropy():
    families=[]
    for n in range(7):
        a=n//2;b=n-a
        family={tuple([0]*a+list(bits)) for bits in product(range(1<<a),repeat=b)}
        require(len(family)==2**(a*b) and family<=set(v.brute_orders(n)),
                'Two-layer family injection')
        families.append({'n':n,'two_layer_records':len(family)})
    lower=[]
    for x in [F(1,16),F(1,4),F(1),F(4)]:
        terms=[{'n':n,'lower_term':F(2**(n*n//4),factorial(n))*x**n}
               for n in CONTROLS['entropy_even_orders']]
        ratios=[]
        for r in range(CONTROLS['entropy_ratio_r_max']+1):
            ratio=F(2**(2*r+1),(2*r+2)*(2*r+1))*x*x
            before=F(2**(r*r),factorial(2*r))*x**(2*r)
            after=F(2**((r+1)**2),factorial(2*r+2))*x**(2*r+2)
            require(after/before==ratio,'Even lower-term ratio')
            ratios.append(ratio)
        lower.append({'x_equals_abs_z_squared_times_h':x,'terms':terms,'ratios':ratios})
    dump('entropy_bounds.json',{'finite_family_controls':families,'lower_terms':lower,
        'analytic_lower_bound':'E_P(k) >= 2^floor(k^2/4), by appending a two-layer order above the entire old past',
        'analytic_ratio':'B_(2r+2)/B_(2r)=2^(2r+1)*x^2/((2r+2)*(2r+1)) -> infinity for every x>0',
        'raw_infinite_L2_candidate':'FAIL: every nonzero finite-stage input has infinite output norm on any positive interval if z != 0',
        'raw_conditioned_cap_removal':'For fixed starting P and terminal interval, mass leaves every fixed finite birth-count sector',
        'scope':'Orthogonal full-history L2 sum; no claim about cancellation in oscillatory scalar amplitudes, different inner products or the general CST quantum measure'})


def horizons():
    cap=CONTROLS['max_total_elements'];identities=derivatives=0;demos=[]
    for m0 in range(CONTROLS['max_parent_elements']+1):
        for p in v.brute_orders(m0):
            for alpha in CONTROLS['alpha_values']:
                for z in map(F,CONTROLS['amplitude_fugacities']):
                    q=z*z
                    for a,b in (map(F,pair) for pair in CONTROLS['sewing_intervals']):
                        rhs=F(0)
                        for j in range(cap-m0+1):
                            weight=q**j*v.number_weight_squared(m0,j,alpha)*a**j/factorial(j)
                            rhs+=weight*sum((v.partition(child,b,cap,alpha,q)
                                            for child in v.descendants(p,j)),F(0))
                        lhs=v.partition(p,a+b,cap,alpha,q)
                        require(lhs==rhs,'Common-horizon partition/norm identity')
                        identities+=1
                        require(v.hazard(p,b,cap,alpha,q)==
                                v.derivative(p,b,cap,alpha,q)/v.partition(p,b,cap,alpha,q),
                                'Backward equation and total hazard')
                        derivatives+=1
    # Check the actual horizon-factor cocycle statewise, independent of interval integration.
    cocycles=0
    for n in range(cap+1):
        for final in v.brute_orders(n):
            for split in range(n+1):
                parent=();middle=final[:split]
                for alpha in CONTROLS['alpha_values']:
                    za=v.partition(parent,F(1,2),cap,alpha)
                    zb=v.partition(middle,F(1,4),cap,alpha)
                    zc=v.partition(final,F(1,8),cap,alpha)
                    first=v.number_weight_squared(0,split,alpha)*zb/za
                    second=v.number_weight_squared(split,n-split,alpha)*zc/zb
                    direct=v.number_weight_squared(0,n,alpha)*zc/za
                    require(first*second==direct,'Horizon-kernel squared coefficient composition')
                    cocycles+=1
    for alpha in CONTROLS['alpha_values']:
        p=();N=2;H=F(1,2);b=F(1,4);Z=v.partition(p,H,N,alpha)
        probs=[c*H**k/Z for k,c in enumerate(v.coefficients(p,N,alpha))]
        require(sum(probs)==1,'Terminal count normalization')
        first_none=v.partition(p,H-b,N,alpha)/Z
        second_none=1/v.partition(p,H-b,N,alpha)
        require(first_none*second_none==probs[0],'Common-horizon no-birth composition')
        demos.append({'alpha':alpha,'cap':N,'horizon':H,'cut':b,'Z':Z,
            'terminal_birth_count_probabilities':probs,'no_birth_first_interval':first_none,
            'no_birth_second_given_none':second_none,'initial_total_hazard':v.hazard(p,H,N,alpha)})
    naive={'cap':2,'alpha':0,'half_interval_Z_product':v.partition((),F(1,4),2)**2,
           'full_interval_Z':v.partition((),F(1,2),2)}
    require(naive['half_interval_Z_product']!=naive['full_interval_Z'],
            'Separate endpoint normalization must fail')
    dump('horizon_completion.json',{'partition_norm_identities':identities,'hazard_identities':derivatives,
        'horizon_coefficient_cocycles':cocycles,'terminal_demos':demos,
        'separate_endpoint_normalization_negative_control':naive,
        'status':'PASS conditional on a declared common endpoint, count weights and local reference product',
        'unitary_surjectivity':'NOT_CLAIMED','physical_waiting_law':'NOT_DERIVED'})


def alternatives():
    caps=CONTROLS['max_total_elements'];bounds=[];tails=[]
    for alpha in [1,2]:
        for m0 in range(CONTROLS['max_parent_elements']+1):
            for p in v.brute_orders(m0):
                for k in range(caps-m0+1):
                    value=F(v.continuations(p,k))*v.number_weight_squared(m0,k,alpha)
                    require(value<=1,'Uniform coefficient bound for damped count cocycle')
                    bounds.append(value)
        for x in [F(1,8),F(1,4),F(1,2),F(1)]:
            for K in CONTROLS['tail_orders']:
                bound=v.exponential_tail_bound(x,K)
                observed=sum((x**k/factorial(k) for k in range(K+1,K+21)),F(0))
                require(0<=observed<=bound,'Certified exponential tail bound')
                tails.append({'alpha':alpha,'x':x,'K':K,'uniform_partition_remainder_bound':bound})
    infinite_examples=[]
    for alpha in [1,2]:
        Z=v.partition((),F(1,2),caps,alpha)
        err=v.exponential_tail_bound(F(1,2),caps)
        infinite_examples.append({'alpha':alpha,'cap_used_for_Z':caps,'horizon':'1/2',
            'Z_partial':Z,'Z_remainder_upper':err,
            'infinite_no_birth_probability_interval':[1/(Z+err),1/Z]})
    a,b=infinite_examples
    require(a['infinite_no_birth_probability_interval'][1] <
            b['infinite_no_birth_probability_interval'][0],
            'Distinct uncapped predictions with certified non-overlap')
    dump('weight_alternatives.json',{'weighted_extension_bound_checks':len(bounds),
        'weights':'f_alpha(n)=2^(-alpha*n*(n-1)/4), alpha=1,2 are explicit model choices',
        'raw_bounded_operator_norm_squared_bound':'exp(|z|^2*h), uniformly over all parent sizes and geometries',
        'conditional_completion_total_hazard_bound':'|z|^2 * exp(|z|^2*H), H the fixed total normalized horizon',
        'no_finite_interval_explosion':'PASS for this bounded-rate completed reference construction',
        'tail_controls':tails,'distinct_uncapped_predictions':infinite_examples,
        'physical_weight_or_endpoint_selected':False,
        'fixed_final_size_relative_geometry_amplitudes':'unchanged by f; relative weights between sizes and intermediate norm factors are changed'})


def main():
    OUT.mkdir(exist_ok=True);digest,n=sources()
    counts();sewing();entropy();horizons();alternatives()
    dump('verification.json',{'source_commit':PLAN['source_commit'],'plan_sha256':digest,
        'sources_verified':n,'status':'PASS_WITH_SCOPED_OBSTRUCTION_AND_CONDITIONAL_COMPLETION',
        'finite_global_cap_composition':'PASS','raw_uncapped_L2_candidate':'FAIL_ANALYTIC',
        'weighted_common_horizon_completion':'PASS_CONDITIONAL_REFERENCE',
        'physical_gates':{k:'HOLD' for k in ['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']},
        'formal_proof_checker':False,'physical_4D_ensemble':False,'physical_quantum_definition_selected':False})
    print(json.dumps({'status':'PASS','exact_result_files':6,'source_files':n,'physical_gates':'8 HOLD'}))


if __name__=='__main__':main()
