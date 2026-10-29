"""Resource accounting and an explicit Poisson count-cap guard; no timing fit."""
from flint import arb
import model as m
import optimize


def compute(scan):
    p=optimize.plan();b=p['resource_budget'];M=b['reference_development_ensemble_size'];cap=b['actual_point_cap_if_a_run_is_later_authorized'];n=cap+1
    def risk(nu):return M*(-m.a(nu)+n*(1+(m.a(nu)/n).log())).exp()
    # Fixed 1% allocation for the planning overflow guard, not scientific alpha.
    lo,hi=1,cap
    while hi-lo>1:
        mid=(lo+hi)//2
        if risk(mid)<=arb(b['planning_overflow_probability_total']):lo=mid
        else:hi=mid
    rows=[]
    for domain in ['D','Omega']:
        s=scan['summaries'][domain]
        for purpose,key in [('admissibility','smallest_admissibility_candidate'),('necessary_error_budget','smallest_necessary_budget_candidate')]:
            selected=s[key]
            if purpose=='admissibility':N=m.balls.decode(selected['expected_N_admissibility_'+domain]).real
            else:N=m.balls.decode(s['necessary_expected_N_plan']).real
            # Counts.cpp simultaneously holds int32 N*N plus two N*ceil(N/64)
            # uint64 bitsets. For Poisson N: E[N²]=nu²+nu.
            mem=arb('17/4')*(N*N+N)
            rows.append({'domain':domain,'purpose':purpose,'ell_k':selected['ell_k'],'H':selected['H'],
                         'expected_N':m.encode(N),'expected_count_kernel_memory_lower_GiB':m.encode(mem/2**30),
                         'expected_unordered_pairs':m.encode(N*N/2),
                         'memory_is_expectation_lower_bound_not_peak_upper_bound':True})
    return {'budget':b,'resource_overflow_planning_guard':{'ensemble_clouds':M,'actual_N_cap':cap,
          'overflow_probability_allocation':b['planning_overflow_probability_total'],'largest_integer_mean_certified_by_Chernoff_union_bound':lo,
          'union_upper_bound':m.encode(risk(lo)),'next_integer_union_upper_bound':m.encode(risk(lo+1)),
          'exceedance_behavior':'RESOURCE_HOLD; preserve failed identity; no redraw'},
          'count_kernel_memory':rows,'wall_time_status':'NOT_EXTRAPOLATED_OR_CERTIFIED; no candidate passes the point/error screen',
          'ensemble_note':'The 10% target concerns one cloud. Averaging 16 clouds does not certify a 10% single-cloud operator.',
          'run_authorized_by_numerical_decision':False,'new_random_realizations':0}
