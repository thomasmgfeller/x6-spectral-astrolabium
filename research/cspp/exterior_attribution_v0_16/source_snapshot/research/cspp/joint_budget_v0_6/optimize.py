"""Finite parameter scan, monotone density elimination and explicit resource gates."""
import json
from functools import lru_cache
from flint import arb,ctx
import model as m


def plan():return json.loads((m.HERE/'PROTOCOL.json').read_text())


def mean(ell):return m.previous_mean.mean_witness(ell)


def best_lower(ell,H,p):
    options=[]
    for start in p['lower_boxes_v']:
        out=m.lower_box(ell,H,start,m.a(start)+m.a(p['lower_box_v_width']))
        if out is not None:options.append(out)
    if not options:return None
    # A choice between valid lower endpoints need not identify a global maximum.
    return max(options,key=lambda x:float(x[0].lower()))


def sufficient_options(ell,sigma2,p):
    options=[]
    for cap in p['epsilon_caps']:
        K,parts=m.variance.upper_coefficient(ell,epsilon_cap=m.a(cap))
        rho=max((m.a(ell)**-4/m.a(cap)).upper(),(K/sigma2).upper())
        rho=int(rho.ceil().unique_fmpz())+1
        if not(K/rho<=sigma2 and m.a(rho)>=m.a(ell)**-4/m.a(cap)):
            raise ArithmeticError('invalid sufficient density')
        options.append((rho,cap,K,parts))
    return min(options,key=lambda x:x[0])


def compute():
    p=plan();den=m.a('1/2');targets=p['relative_targets'];tau=m.a(targets['single_cloud_total_RMS'])*den
    sig=m.a(targets['single_cloud_stochastic_RMS'])*den
    rows=[];means=[];allfieldstatus='NOT_QUALIFIED';pointbudget=p['resource_budget']['expected_points_per_cloud']
    for ell in p['ell_k']:
        mu,meta=mean(ell);bias=abs(mu+den)/den;q=m.a(ell)**-4
        # Density upper certificate uses the fixed 7% allocation. Final total
        # target is checked separately with the actual finite-domain mean ball.
        upper=sufficient_options(ell,sig**2,p) if bias<=m.a(targets['nonlocal_bias']) else None
        means.append({'ell_k':ell,'mean_infinite':m.encode(mu),'relative_nonlocal_bias':m.encode(bias),
                      'bias_allocation_status':'WITHIN' if upper else 'EXCEEDS' if bias>m.a(targets['nonlocal_bias']) else 'UNDECIDED'})
        for H in p['H']:
            D=m.volume(H);Omega=m.volume(m.a(H)+4)
            row={'ell_k':ell,'H':H,'q_rho_admissibility_min':m.encode(q),
                'expected_N_admissibility_D':m.encode(q*D),'expected_N_admissibility_Omega':m.encode(q*Omega),
                'volume_D':m.encode(D),'volume_Omega':m.encode(Omega),
                'relative_nonlocal_bias':m.encode(bias)}
            c=(arb.pi()*q/24).sqrt()
            if c*m.a(H)**2 >= 8:
                boundary,berr=m.outside_boundary(ell,H,order=p['boundary_series_order']);muf=mu-boundary
                method='GAMMA_SERIES_PLUS_TWO_REMAINDERS'
            else:
                muf=m.finite_mean_direct(ell,H);boundary=mu-muf
                berr={'direct_quadrature_component_radius':muf.rad()}
                method='DIRECT_FINITE_DOMAIN_INTERVAL_QUADRATURE'
            brel=abs(boundary)/den;finitebias=abs(muf+den)
            lower=best_lower(ell,H,p)
            kl,ldetail=lower if lower else (arb(0),{})
            low=kl.lower()
            allocation_ok=brel<=m.a(targets['boundary'])
            status=('NONLOCAL_BIAS_REJECT' if bias>m.a(targets['nonlocal_bias']) else 'NONLOCAL_BIAS_UNDECIDED') if upper is None else ('WITHIN' if allocation_ok else 'BOUNDARY_REJECT' if brel>m.a(targets['boundary']) else 'BOUNDARY_UNDECIDED')
            biaslo=max(arb(0),finitebias.lower())
            remaining_upper=tau**2-biaslo**2
            necessary_total=None if not remaining_upper>0 else max(q,low/remaining_upper.upper())
            necessary_stoch=max(q,low/sig**2)
            necessary_plan=None if necessary_total is None else max(necessary_total,necessary_stoch)
            rho_u,cap,K,parts=upper if upper else (None,None,None,None)
            rms_u=(finitebias.upper()**2+K/rho_u).sqrt()/den if upper else None
            row.update({'allocation_status':status,'finite_mean_method':method,'positive_variance_lower_established':bool(lower),'mean_finite':m.encode(muf),'signed_boundary_delta':m.encode(boundary),
                'relative_boundary':m.encode(brel),'relative_finite_bias':m.encode(finitebias/den),
                'boundary_errors':{k:m.encode(v) if isinstance(v,arb) else v for k,v in berr.items()},
                'variance_lower_coefficient':m.encode(kl),'lower_box':{k:m.encode(v) for k,v in ldetail.items()},
                'rho_necessary_total_10pct':None if necessary_total is None else m.encode(necessary_total),
                'rho_necessary_stochastic_7pct':m.encode(necessary_stoch),
                'rho_necessary_for_all_allocations':None if necessary_plan is None else m.encode(necessary_plan),
                'rho_sufficient_for_all_allocations':str(rho_u) if upper and allocation_ok and rms_u<=m.a(targets['single_cloud_total_RMS']) else None,
                'upper_epsilon_cap':cap,'upper_variance_coefficient':m.encode(K) if upper else None,'relative_total_RMS_upper_at_sufficient_density':m.encode(rms_u) if upper else None})
            for label,V in [('D',D),('Omega',Omega)]:
                rho_max=m.a(pointbudget)/V
                admiss=rho_max>=q
                rmslo=(biaslo**2+low/rho_max).sqrt()/den
                row['budget_'+label]={'rho_max':m.encode(rho_max),'epsilon_at_budget':m.encode(q/rho_max),
                    'admissible':bool(admiss),'relative_total_RMS_lower_at_budget':m.encode(rmslo),
                    'single_witness_total_10pct_excluded':bool(rmslo>m.a(targets['single_cloud_total_RMS'])),
                    'expected_N_necessary_total':None if necessary_total is None else m.encode(necessary_total*V),
                    'expected_N_necessary_plan':None if necessary_plan is None else m.encode(necessary_plan*V),
                    'expected_N_sufficient_plan':m.encode(rho_u*V) if row['rho_sufficient_for_all_allocations'] else None}
            rows.append(row)
        print('optimized scale',ell,flush=True)
    eligible=[r for r in rows if r['allocation_status']=='WITHIN']
    if not eligible:raise ArithmeticError('no systematic-allocation candidates')
    summaries={};sensitivity={}
    for label in ['D','Omega']:
        def minrow(key):
            available=[r for r in eligible if r['budget_'+label][key] is not None]
            return min(available,key=lambda r:float(m.balls.decode(r['budget_'+label][key]).real.lower()))
        lowerrow=minrow('expected_N_necessary_plan');upperrow=minrow('expected_N_sufficient_plan')
        admissrow=min(eligible,key=lambda r:float(m.balls.decode(r['expected_N_admissibility_'+label]).real.lower()))
        summaries[label]={'smallest_admissibility_candidate':{k:admissrow[k] for k in ['ell_k','H','expected_N_admissibility_'+label]},
            'smallest_necessary_budget_candidate':{k:lowerrow[k] for k in ['ell_k','H']},
            'necessary_expected_N_plan':lowerrow['budget_'+label]['expected_N_necessary_plan'],
            'smallest_sufficient_bound_candidate':{k:upperrow[k] for k in ['ell_k','H']},
            'sufficient_expected_N_plan':upperrow['budget_'+label]['expected_N_sufficient_plan'],
            'necessary_is_not_feasible_or_optimal':True}
        sc=[]
        for B in p['budget_sensitivity_expected_points']:
            counts={'inadmissible':0,'excluded_by_variance_or_total_RMS':0,'unresolved':0,'certified_for_single_witness_only':0}
            for row in eligible:
                if m.balls.decode(row['expected_N_admissibility_'+label]).real>m.a(B):counts['inadmissible']+=1;continue
                lo=row['budget_'+label]['expected_N_necessary_plan'];hi=row['budget_'+label]['expected_N_sufficient_plan']
                if lo is None or m.balls.decode(lo).real>m.a(B):counts['excluded_by_variance_or_total_RMS']+=1
                elif hi is not None and m.balls.decode(hi).real<=m.a(B):counts['certified_for_single_witness_only']+=1
                else:counts['unresolved']+=1
            sc.append({'expected_point_budget':str(B),**counts})
        sensitivity[label]=sc
    rescued_cases=[]
    for row in rows:
        bd=row['budget_D']
        if not bd['admissible']:
            row['family_budget_status']='ADMISSIBILITY_REJECT'
        elif bd['single_witness_total_10pct_excluded']:
            row['family_budget_status']='GAUSSIAN_TOTAL_RMS_REJECT'
        else:
            checks=[]
            for w,k in [('0','0'),('1/4','0'),('0','1/4'),('1/4','1/4')]:
                z=m.finite_mode_direct(row['ell_k'],row['H'],w,k)
                exact=m.a(w)**2-m.a(k)**2-den
                lower=(z-exact).abs_lower()/abs(exact)
                upper=(z-exact).abs_upper()/abs(exact)
                checks.append({'omega':w,'k':k,'mean':m.balls.encode(z),'exact_Box':m.encode(exact),
                               'relative_bias_lower':m.encode(lower),'relative_bias_upper':m.encode(upper),
                               'total_RMS_excluded_at_every_density':bool(lower>m.a(targets['single_cloud_total_RMS']))})
            row['additional_fixed_mode_checks']=checks
            row['family_budget_status']='FIXED_MODE_BIAS_REJECT' if any(x['total_RMS_excluded_at_every_density'] for x in checks) else 'UNRESOLVED'
            rescued_cases.append({'ell_k':row['ell_k'],'H':row['H'],'checks':checks})
    no_run=all(r['family_budget_status']!='UNRESOLVED' for r in rows)
    relaxed={}
    for label in ['D','Omega']:
        valid=[r for r in rows if r['budget_'+label]['expected_N_necessary_total'] is not None and r['family_budget_status']!='FIXED_MODE_BIAS_REJECT']
        best=min(valid,key=lambda r:float(m.balls.decode(r['budget_'+label]['expected_N_necessary_total']).real.lower()))
        relaxed[label]={'ell_k':best['ell_k'],'H':best['H'],'necessary_expected_N_10pct_total_only':best['budget_'+label]['expected_N_necessary_total'],
                        'meaning':'necessary Gaussian bound after excluding the known fixed-mode counterexample; relaxing the separate allocations does not establish feasibility'}
    if not no_run:raise ArithmeticError('a fixed-family candidate remains unresolved; no automatic run authorization')
    return {'schema':'cspp.joint-budget/0.6','precision_bits':ctx.prec,'mean_rows':means,'rows':rows,
            'fixed_mode_followups':rescued_cases,'systematic_allocation_candidates':len(eligible),'relaxed_total_only':relaxed,'summaries':summaries,'budget_sensitivity':sensitivity,
            'decision':'NO_NEW_SPRINKLING_AT_INHERITED_BUDGET','expected_point_budget':pointbudget,
            'all_fields_status':allfieldstatus,'scope':'finite declared grid and the fixed L=2 necessary witness; no continuum-wide optimum or full E4 exclusion',
            'new_poisson_clouds':0,'confirmation_seed_used':False,'gate_status':p['scientific_status']}
