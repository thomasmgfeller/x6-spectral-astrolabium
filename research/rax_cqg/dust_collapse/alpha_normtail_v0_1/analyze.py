"""Reproduce analytic-tail certificates and refinements without new field integrals."""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib
import json
import sys
import bounds as b

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
import intervals as old
import memory
import readout as r

PLAN=json.loads((ROOT/'plan.json').read_text())
P=PLAN['controls'];OUT=ROOT/'results';require=b.require


def encode(x):
    if isinstance(x,F):return str(x)
    raise TypeError(type(x).__name__)
def dump(name,x):(OUT/name).write_text(json.dumps(x,indent=2,default=encode)+'\n')
def load(name):return json.loads((ROOT/'inputs'/name).read_text())
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,default=encode).encode()).hexdigest()
def key(x):return x['alpha'],F(x['h']),F(x['g_over_pi']),F(x['mu'])
def cparse(x):return r.C(F(x['re']),F(x['im']))
def visibility(z,e):
    slack=2*e+e*e
    return [max(F(0),z.abs2()-slack),min(F(1),z.abs2()+slack)]


def sources():
    ph=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(ph==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan digest')
    prov=load('provenance.json')
    require(prov['commit']==PLAN['source_commit'],'Pinned main commit')
    for name,x in prov['files'].items():
        data=(ROOT/'inputs'/name).read_bytes()
        require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==x['sha'],name)
    return ph,len(prov['files'])


def enumeration():
    records=[];counts=[];ideal_checks=0
    for n in range(P['enumeration_validation_through']+1):
        candidates=2**(n*(n-1)//2)
        require(candidates<=PLAN['cost_gate']['max_upper_triangle_candidates'],'Enumeration cost gate')
        a=memory.natural_orders(n);z=old.brute_orders(n)
        require(len(a)==len(set(a)) and set(a)==set(z),'Two complete enumerations agree')
        counts.append(len(a))
        require(counts[-1]<=candidates,'Upper-triangle bound')
        if n < P['enumeration_validation_through']:
            sizes=[len(memory.ideals(p)) for p in a]
            require(all(1<=v<=2**n for v in sizes),'At most 2^n ideals')
            ideal_checks+=len(sizes)
        else:sizes=[]
        records.append({'n':n,'natural_orders':len(a),'upper_triangle_candidates':candidates,
                        'canonical_orders_sha256':digest(sorted(a)),
                        'sum_one_step_ideal_counts':sum(sizes) if sizes else None,
                        'next_sector_used_in_production_tail':False})
    for n in range(len(counts)-1):
        require(records[n]['sum_one_step_ideal_counts']==counts[n+1], 'Exact continuation census')
        require(counts[n+1]<=counts[n]*2**n,'Recurrence bound')
    require(counts[:7]==[1,1,2,7,40,357,4824],'Inherited exact counts through six')
    return counts,{'records':records,'ideal_bound_checks':ideal_checks,
                   'exact_normalization_cap_used':6,'n7_count_is_validation_only':True}


def proof_controls(counts):
    records=[];invalid=[];steps=0;next_checks=0
    for alpha in P['tail_proof_grid_alpha']:
        for hs in P['tail_proof_grid_h']:
            h=F(hs)
            for K in P['tail_proof_grid_cap']:
                q=b.ratio(h,alpha,K+1)
                if q>=1:
                    try:b.anchored_tail(counts[K],h,alpha,K)
                    except RuntimeError:invalid.append({'alpha':alpha,'h':h,'K':K,'q':q,'status':'REJECTED'})
                    else:raise RuntimeError('Invalid ratio accepted')
                    continue
                bound=b.anchored_tail(counts[K],h,alpha,K)
                univ=b.universal_tail(h,alpha,K)
                require(bound<=univ,'Anchored bound below universal alpha bound')
                inherited=old.exponential_tail_bound(h,K) if h<K+2 else None
                if inherited is not None:require(univ<=inherited,'Alpha bound below inherited bound')
                first=b.majorant_term(counts[K],h,alpha,K,K+1)
                require(first/(1-q)==bound,'Independent recurrence and closed-form agreement')
                partial=F(0);previous=None;terms=[]
                for n in range(K+1,K+1+P['majorant_terms_checked']):
                    term=b.majorant_term(counts[K],h,alpha,K,n)
                    if previous is not None:require(term==previous*b.ratio(h,alpha,n-1),'Majorant recurrence')
                    require(b.ratio(h,alpha,n)<=q,'Monotone ratio for alpha>=1')
                    require(term<=first*q**(n-K-1),'Geometric domination')
                    partial+=term;previous=term;terms.append(term);steps+=1
                require(partial<=bound,'Positive majorant sum within infinite bound')
                actual=sum((b.coefficient(counts[n],h,alpha,n) for n in range(K+1,8)),F(0))
                require(actual<=bound,'Enumerated mass through seven below analytic tail')
                next_checks+=1
                records.append({'alpha':alpha,'h':h,'K':K,'q':q,'anchor_fraction':F(counts[K],2**(K*(K-1)//2)),
                                'first_majorant':first,'anchored_tail_upper':bound,'universal_alpha_tail_upper':univ,
                                'inherited_tail_upper':inherited,'enumerated_partial_tail_through_7':actual,
                                'majorant_term_checks':len(terms),'majorant_terms_sha256':digest(terms)})
    h=F(1,2);alpha=2;K=6
    actual7=b.coefficient(counts[7],h,alpha,7)
    wrong_exponent=b.coefficient(counts[K],h,alpha,K)*h/F(7)*b.power2(-alpha*K)/\
        (1-h/F(8)*b.power2(-alpha*7))
    require(actual7>wrong_exponent,'Wrong alpha exponent omits ideal branching and underbounds c7')
    wrong_multiplicity=b.anchored_tail(1,h,alpha,K)
    require(actual7>wrong_multiplicity,'Dropping N6 underbounds c7')
    rejected=[]
    for label,args in [('alpha_below_one',(F(1,2),0,6)),('negative_h',(F(-1),2,6)),
                       ('ratio_equals_one',(F(8),1,6)),('negative_cutoff',(F(1,2),2,-1))]:
        try:b.universal_tail(*args)
        except RuntimeError:rejected.append({'control':label,'status':'REJECTED'})
        else:raise RuntimeError('Invalid-domain negative control accepted')
    negatives={'wrong_alpha_instead_of_alpha_minus_one':{'wrong_upper':wrong_exponent,'actual_c7':actual7,'status':'REJECTED'},
               'dropped_N6_multiplicity':{'wrong_upper':wrong_multiplicity,'actual_c7':actual7,'status':'REJECTED'},
               'invalid_domain':rejected}
    return {'records':records,'invalid_ratio_cases':invalid,'majorant_recurrence_checks':steps,
            'enumerated_partial_tail_checks':next_checks,'negative_controls':negatives}


def refine(counts):
    prior=load('prior_extended_results.json')
    before={key(x):x for x in load('prior_tail_reduction.json')['cases']}
    summaries={};cases=[]
    for x in prior['cases']:
        alpha,h,gpi,mu=key(x);previous=before[key(x)]
        c=[b.coefficient(counts[n],h,alpha,n) for n in range(7)]
        Z4=sum(c[:5]);Z6=sum(c)
        require(Z4==F(x['Z4']) and Z6==F(previous['Z6']),'Pinned exact norm masses')
        old_delta=F(previous['normalization_tail_n_gt_6_upper'])
        require(old_delta==old.exponential_tail_bound(h,6),'Inherited tail identity')
        delta=b.anchored_tail(counts[6],h,alpha,6);universal=b.universal_tail(h,alpha,6)
        require(0<=delta<=universal<=old_delta,'Ordered tail certificates')
        Zmax=Z6+delta;known_unknown=Z6-Z4;Rmax=known_unknown+delta;pmax=Rmax/Zmax
        require(Zmax<2,'Vacuum guard for coherent channel')
        vis=[list(map(F,v)) for v in x['number_visibility_intervals']]
        t=list(map(cparse,x['number_amplitude_centers']));eps=list(map(F,x['number_amplitude_errors']))
        require(len(vis)==len(t)==len(eps)==5,'Only previously integrated sectors')
        require(vis==[visibility(z,e) for z,e in zip(t,eps)],'Unchanged amplitude error propagation')
        lo=sum((c[j]*vis[j][0] for j in range(5)),F(0))
        hi=sum((c[j]*vis[j][1] for j in range(5)),F(0))
        finite_t=sum((c[j]*t[j] for j in range(5)),r.ZERO)/Z4
        finite_eps=sum((c[j]*eps[j] for j in range(5)),F(0))/Z4
        count=[lo/Zmax,min(F(1),(hi+Rmax)/Zmax)]
        raw=visibility(finite_t,finite_eps+2*pmax)
        raw[0]=max(raw[0],(2/Zmax-1)**2)
        if gpi==mu==0:count=raw=[F(1),F(1)]
        old_count=list(map(F,previous['count_success_infinite_interval']))
        old_all=list(map(F,previous['all_success_infinite_interval']))
        old_raw=list(map(F,previous['all_success_infinite_raw_interval']))
        require(old_count[0]<=count[0]<=count[1]<=old_count[1],'Count interval containment')
        require(old_raw[0]<=raw[0]<=raw[1]<=old_raw[1],'Raw coherent interval containment')
        all_interval=[max(raw[0],old_all[0]),min(raw[1],old_all[1])]
        require(old_all[0]<=all_interval[0]<=all_interval[1]<=old_all[1],'Final coherent interval containment')
        accepted=[[c[j]*vis[j][0]/(hi+Rmax),min(F(1),c[j]*vis[j][1]/lo)] for j in range(5)]
        old_accepted=[list(map(F,v)) for v in previous['accepted_count_0_1_2_3_4_intervals']]
        require(all(a[0]<=v[0]<=v[1]<=a[1] for a,v in zip(old_accepted,accepted)), 'Accepted-count interval containment')
        accepted_tail=min(F(1),Rmax/lo)
        require(accepted_tail<=F(previous['accepted_n_ge_5_probability_upper']), 'Accepted higher-count tail improves')
        fields={k:x[k] for k in ['number_amplitude_centers','number_amplitude_errors','number_visibility_intervals']}
        cases.append({'alpha':alpha,'h':h,'g_over_pi':gpi,'mu':mu,'inherited_amplitude_data_sha256':digest(fields),
            'Z4':Z4,'Z6':Z6,'Zmax':Zmax,'normalization_tail_n_gt_6_upper':delta,
            'unintegrated_n5_to_6_mass':known_unknown,'unintegrated_n_ge_5_mass_upper':Rmax,
            'unintegrated_n_ge_5_probability_upper':pmax,'count_success_infinite_interval':count,
            'all_success_infinite_raw_interval':raw,'all_success_infinite_interval':all_interval,
            'all_interval_intersected_with_previous':True,'previous_count_interval':old_count,
            'previous_all_interval':old_all,'previous_all_raw_interval':old_raw,
            'accepted_count_0_1_2_3_4_intervals':accepted,'accepted_n_ge_5_probability_upper':accepted_tail,
            'count_containment':'PASS','all_containment':'PASS','new_field_integrals':0})
        old_p=F(previous['unintegrated_n_ge_5_probability_upper'])
        summaries[alpha,h]={'alpha':alpha,'h':h,'exact_N6':counts[6],
            'anchor_fraction':F(counts[6],2**15),'old_norm_tail_upper':old_delta,
            'universal_alpha_tail_upper':universal,'anchored_norm_tail_upper':delta,
            'norm_tail_fraction_removed':1-delta/old_delta,'n5_to_6_mass':known_unknown,
            'old_phase_tail_probability_upper':old_p,'new_phase_tail_probability_upper':pmax,
            'phase_tail_fraction_removed':1-pmax/old_p,'new_norm_tail_share_of_Rmax':delta/Rmax,
            'n5_share_of_Rmax':c[5]/Rmax,'n6_share_of_Rmax':c[6]/Rmax}
    require(len(cases)==36 and len(summaries)==4,'Frozen parameter census')
    return {'integrated_count_cap':4,'normalization_count_cap':6,'phase_tail_begins_at':5,
            'cases':cases,'count_containment_checks':36,'all_containment_checks':36,
            'accepted_count_containment_checks':180},list(summaries.values())


def main():
    OUT.mkdir(exist_ok=True);ph,n_sources=sources()
    counts,census=enumeration();print('Enumeration controls complete through n=7',flush=True)
    controls=proof_controls(counts);cases,summary=refine(counts)
    dump('combinatorial_certificate.json',census);dump('tail_bound_certificate.json',controls)
    dump('refined_results.json',cases);dump('improvement_summary.json',{'records':summary})
    verification={'status':'PASS_ALPHA_DEPENDENT_ANCHORED_NORMTAIL_REFERENCE_MODEL',
        'source_commit':PLAN['source_commit'],'plan_sha256':ph,'sources_verified':n_sources,
        'natural_order_counts_validation':counts,'production_normalization_cap':6,'field_integration_cap':4,
        'proof_grid_valid_cases':len(controls['records']),'proof_grid_rejected_ratio_cases':len(controls['invalid_ratio_cases']),
        'majorant_recurrence_checks':controls['majorant_recurrence_checks'],
        'count_interval_containment_checks':36,'coherent_interval_containment_checks':36,
        'accepted_count_interval_containment_checks':180,'new_field_integrals':0,
        'field_phases_n_ge_5':'NOT_INTEGRATED','all_amplitude_inputs_unchanged':True,
        'physical_gates':PLAN['physical_gates'],'external_replication':False,'formal_proof_checker':False,
        'physical_density_boundary_or_detector_selected':False,'physical_4d_dynamics_derived':False}
    dump('verification.json',verification)
    print(json.dumps({'status':'PASS','results':5,'cases':36,'gates':'8 HOLD'}))


if __name__=='__main__':main()
