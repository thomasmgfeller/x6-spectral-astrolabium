"""Reproduce exact clock-label, norm, instrument and stationarity controls."""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
from itertools import permutations,product,combinations
import json
from math import factorial,comb,prod
from pathlib import Path
import clock as c

ROOT=Path(__file__).resolve().parent


def serial(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):serial(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [serial(v) for v in x]
    return x


def digest_records(records):
    return hashlib.sha256((json.dumps(serial(records),sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()


def run(out):
    out.mkdir(parents=True,exist_ok=True)
    planbytes=(ROOT/'plan.json').read_bytes();plan=json.loads(planbytes)
    planhash=hashlib.sha256(planbytes).hexdigest()
    c.require(planhash==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    provenance=json.loads((ROOT/'inputs/provenance.json').read_text())
    for name,record in provenance['files'].items():
        b=(ROOT/'inputs'/name).read_bytes()
        s=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        c.require(s==record['sha'],'Source identity: '+name)
    controls=plan['controls'];maxm=controls['max_internal_elements']
    cuts=list(map(F,controls['cut_values']))
    census=[];phase_checks=cut_checks=0;representations=0;chron_records=0
    wrong_weight_failures=0
    for size in controls['clock_grids']:
        grid=tuple(F(-1)+F(2*i,size-1) for i in range(size))
        for n in range(maxm+1):
            original=defaultdict(F);sorted_route={};wrong={};accepted=0
            field_mass=F(1,(size*2)**n)
            for order in c.m.natural_orders(n):
                e=c.m.extensions(order);clock_count=0
                for times in permutations(grid,n):
                    if not c.causal_clock(order,times):continue
                    clock_count+=1
                    for tau in cuts:
                        mask=c.threshold(times,tau)
                        c.require(mask in c.m.ideals(order),'Relational cut must be an ideal')
                        cut_checks+=1
                    for marks in product(range(2),repeat=n):
                        state=order,times,marks;ranked=c.chronological(*state)
                        original[ranked]+=field_mass/e
                        c.require(c.action(state)==c.action(ranked),'Open phase covariance')
                        c.require(c.action(state,True)==c.action(ranked,True),'Closed phase covariance')
                        phase_checks+=1;accepted+=1
                c.require(clock_count==e*comb(size,n),'Independent clock-domain volume count')
                for times in combinations(grid,n):
                    for marks in product(range(2),repeat=n):
                        key=order,times,marks
                        sorted_route[key]=field_mass
                        wrong[key]=field_mass/e
            c.require(dict(original)==sorted_route,'Coherent amplitude equality per complete marked state')
            failures=sum(wrong[key]!=value for key,value in sorted_route.items())
            if n>=2:c.require(failures>0,'Wrong retained 1/e factor must be detected')
            wrong_weight_failures+=failures
            expected=F(len(c.m.natural_orders(n))*comb(size,n),size**n)
            c.require(sum(original.values(),F(0))==expected,'Chronological measure mass')
            records=[{'order':key[0],'times':key[1],'marks':key[2],'coefficient':value,
                      'action_open':c.action(key),'action_closed':c.action(key,True)}
                     for key,value in sorted(sorted_route.items())]
            census.append({'grid_size':size,'m':n,'natural_orders':len(c.m.natural_orders(n)),
                           'accepted_marked_natural_representations':accepted,
                           'chronological_marked_records':len(sorted_route),
                           'coherent_sum_mass':expected,'wrong_retained_factor_mass':sum(wrong.values(),F(0)),
                           'wrong_factor_entries':failures,'statewise_identity':'PASS',
                           'canonical_records_sha256':digest_records(records)})
            representations+=accepted;chron_records+=len(sorted_route)
    # A free, nonmonotone clock does not give an ideal threshold cut.
    invalid_order=(0,1);invalid_times=(F(1,2),F(-1,2))
    invalid_cut=c.threshold(invalid_times,F(0))
    c.require(invalid_cut not in c.m.ideals(invalid_order),'Nonmonotone cut negative control')

    domains=[]
    for n in range(maxm+1):
        orders=c.m.natural_orders(n)
        unrestricted=sum((F(1,c.m.extensions(p)) for p in orders),F(0))
        ordered=sum((F(1,c.m.extensions(p))*F(c.m.extensions(p),factorial(n)) for p in orders),F(0))
        c.require(ordered==F(len(orders),factorial(n)),'Continuous chamber volume')
        domains.append({'m':n,'unrestricted_phase_free_amplitude':unrestricted,
                        'ordered_sector_phase_free_amplitude':ordered,
                        'naive_chronological_retained_1_over_e':unrestricted/factorial(n),
                        'reference_terminal_dual_norm_squared':ordered,
                        'max_terminal_effect_scale':1/ordered})

    windows=[tuple(map(F,w)) for w in controls['wavepacket_windows']]
    widths=list(map(F,controls['tail_widths']));packets=[];bounds=[]
    for n in range(1,maxm+1):
        for order in c.m.natural_orders(n):
            d=len(c.m.ideals(order));c.require(d<=2**n,'Ideal-count upper bound')
            rows=[]
            for lo,hi in windows:
                r=c.packet_norm_ratio(order,lo,hi)
                c.require(r==c.birth_multiplier(order,(lo+hi)/2),'Independent integral and affine mean')
                rows.append({'window':[lo,hi],'output_norm_squared':r})
            tails=[]
            for eps in widths:
                r=c.packet_norm_ratio(order,F(1)-eps,F(1))
                c.require(r==F(d)*eps/4,'Localized endpoint packet formula')
                tails.append({'epsilon':eps,'output_norm_squared':r})
            packets.append({'m':n,'order':order,'ideal_count':d,'unit_input_norm':True,
                            'windows':rows,'endpoint_packets':tails})
        bounds.append({'m':n,'max_ideal_count':max(len(c.m.ideals(p)) for p in c.m.natural_orders(n)),
                       'operator_norm_squared_supremum':2**n,'safe_completion_scale':F(1,2**n)})
    one=packets[0]
    c.require([x['output_norm_squared'] for x in one['windows']]==[F(5,4),F(3,4)],'Distinct preparation norms')

    completion=[];point_checks=0
    for alpha in map(F,controls['completion_scales']):
        for lo,hi in windows:
            birth=alpha*c.packet_norm_ratio((0,),lo,hi)
            no_birth=1-birth
            c.require(0<=birth<=1 and birth+no_birth==1,'Two-outcome normalization')
            completion.append({'m':1,'alpha':alpha,'window':[lo,hi],
                               'birth_probability':birth,'no_birth_probability':no_birth})
    for n in range(1,maxm+1):
        alpha=F(1,2**n)
        for order in c.m.natural_orders(n):
            for t in cuts:
                e=alpha*c.birth_multiplier(order,t)
                c.require(0<=e<=1 and e+(1-e)==1,'Pointwise effect partition')
                point_checks+=1
    overscaled=c.birth_multiplier((0,),F(-1,2))
    c.require(overscaled==F(3,2) and 1-overscaled<0,'Overscaled completion negative control')

    # A new positive density can satisfy its own density stationarity while
    # changing the equation of an old free clock that was previously stationary.
    before=(0,1);after=(0,1,3)
    times=(F(0),F(11,45),F(43,90));weights=(F(0),F(0),F(1,2))
    old_gamma,old_q,old_j=c.gamma_gradient(before,times[:2],weights[:2])
    gamma,q,current=c.gamma_gradient(after,times,weights)
    c.require(old_q==[0,0] and gamma[2]==-1 and q[1]==F(7,120),'Stationarity counterexample')
    c.require(sum(q,F(0))==0 and c.causal_clock(after,times),'Clock order and total flux')
    step=F(1,97)
    for i in range(3):
        plus=list(times);minus=list(times);plus[i]+=step;minus[i]-=step
        central=(c.m.matter(after,tuple(plus),weights)-c.m.matter(after,tuple(minus),weights))/(2*step)
        c.require(central==q[i],'Independent full-action derivative')
    plus=list(weights);minus=list(weights);plus[2]+=step;minus[2]-=step
    density_diff=(c.m.matter(after,times,tuple(plus))-c.m.matter(after,times,tuple(minus)))/(2*step)
    c.require(density_diff==0,'New interior-density stationarity')

    results={
      'clock_ordering.json':{'grids':controls['clock_grids'],'census':census,
                            'total_natural_marked_representations':representations,
                            'total_chronological_marked_records':chron_records,
                            'open_and_closed_phase_covariance_checks':phase_checks,
                            'threshold_ideal_checks':cut_checks,
                            'wrong_factor_entries_detected':wrong_weight_failures,
                            'nonmonotone_cut_negative_control':{'order':invalid_order,'times':invalid_times,'cut':invalid_cut,'is_ideal':False}},
      'domain_measure.json':{'continuous_counts':domains,
                            'two_element_type_weights':{'unrestricted':{'antichain':'1/2','chain':'1'},
                                                       'ordered_sector':{'antichain':'1/2','chain':'1/2'}},
                            'sector_restriction_is_gauge':'NO'},
      'birth_norms.json':{'reference':'L=1; chronological corrected coefficient one; unit-density field measures',
                         'packets':packets,'operator_bounds':bounds,
                         'general_obstruction':'No bounded positive child metric and coercive positive parent metric make the full fixed-one-birth map isometric, for m>=1; localized clock-endpoint packets prove it.',
                         'scope':'Full declared stage spaces; restricted subspaces and singular metrics not excluded'},
      'instrument_completion.json':{'two_outcome_controls':completion,'pointwise_checks':point_checks,
                                   'overscaled_birth_effect':overscaled,'overscaled_complement':1-overscaled,
                                   'physical_no_birth_law':'NOT_DERIVED','scale_selected':'NO'},
      'stationarity.json':{'before_order':before,'after_order':after,'times':times,'weights':weights,
                           'before_clock_gradient':old_q,'after_gamma':gamma,'after_clock_gradient':q,
                           'currents':current,'new_density_derivative':density_diff,
                           'old_free_clock_equation_preserved':False,'future_boundary_clock_held':True,
                           'claim':'A prefix saddle is not automatically a saddle of a longer history; no canonical constraint interpretation assumed'},
      'verification.json':{'source_commit':plan['source_commit'],'plan_sha256':planhash,'sources_verified':len(provenance['files']),
                           'status':'PASS_WITH_SCOPED_CANDIDATE_FAILURE','candidate_closed_fixed_birth_isometry':'FAIL_ANALYTIC_FULL_STAGE_CLASS',
                           'physical_gates':{g:'HOLD' for g in ['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']},
                           'formal_proof_checker':False,'new_physical_4D_ensemble':False,'physical_clock_or_metric_selected':False}}
    for name,value in results.items():
        (out/name).write_text(json.dumps(serial(value),indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'PASS_WITH_SCOPED_CANDIDATE_FAILURE','natural_representations':representations,
                      'chronological_records':chron_records,'phase_covariance':phase_checks,
                      'cut_checks':cut_checks,'wrong_factor_entries':wrong_weight_failures,
                      'packet_checks':sum(len(p['windows'])+len(p['endpoint_packets']) for p in packets),
                      'output_files':len(results)}))


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'results')
    run(parser.parse_args().output)
