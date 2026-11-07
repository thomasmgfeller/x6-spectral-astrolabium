#!/usr/bin/env python3
"""Exact finite checks of auxiliary existence, coherent bounds and quotient scope."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import normpath as q
m = q.m
ROOT = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def dump(name, obj):
    (ROOT/'results'/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False)+'\n')


def main():
    plan = json.loads((ROOT/'plan.json').read_text())
    ph = hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(ph == (ROOT/'plan.sha256').read_text().split()[0], 'Plan hash')
    provenance = json.loads((ROOT/'inputs/provenance.json').read_text())
    for name, item in provenance['files'].items():
        require(hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest() == item['sha256'], 'Source '+name)
    ps = [F(p) for p in plan['percolation_p']]
    counts = [len(m.natural_orders(n)) for n in range(7)]
    require(counts == [1,1,2,7,40,357,4824], 'Natural-order census')
    checks = {'independent_DAGs':0, 'edge_probability_comparisons':0, 'transition_recursions':0,
              'metric_recursions':0, 'positive_metric_values':0, 'normalization_sums':0}
    norm_records = []
    for n in range(7):
        independent = q.edge_distribution(n, ps)
        checks['independent_DAGs'] += 2**(n*(n-1)//2)
        mass_sum = sum((F(1,m.extensions(o)) for o in m.natural_orders(n)), F(0))
        require(mass_sum >= F(2**((n//2)*(n-n//2)), math.factorial(n)), 'Bipartite lower bound')
        record = {'m':n, 'sum_inverse_extensions':str(mass_sum), 'percolation':[]}
        for p, dist in zip(ps, independent):
            total = F(0)
            dual_squared = F(0)
            for order in m.natural_orders(n):
                u, h = q.mu(order,p), q.metric(order,p)
                require(dist[order] == u and h > 0, 'Independent DAG probability and positivity')
                checks['edge_probability_comparisons'] += 1
                checks['positive_metric_values'] += 1
                total += u
                dual_squared += 1/h
                if n < 6:
                    children = [order+(s,) for s in m.ideals(order)]
                    require(sum((q.transition(order,s,p) for s in m.ideals(order)),F(0)) == 1,
                            'Transition sum')
                    require(sum((q.mu(c,p) for c in children),F(0)) == u, 'Cylinder consistency')
                    require(all(q.mu(c,p) == u*q.transition(order,c[-1],p) for c in children),
                            'Transition products')
                    checks['transition_recursions'] += 1
                    require(sum((F(m.extensions(order),m.extensions(c))**2*q.metric(c,p)
                                 for c in children),F(0)) == h, 'Metric recursion')
                    checks['metric_recursions'] += 1
            require(total == 1 and dual_squared >= mass_sum**2, 'Normalized norm and dual bound')
            checks['normalization_sums'] += 1
            record['percolation'].append({'p':str(p),'dual_norm_squared':str(dual_squared),
                                          'auxiliary_state_norm_squared':str(total)})
        norm_records.append(record)
    dump('diagonal_norms.json', {'natural_counts':counts,'checks':checks,'records':norm_records,
          'existence':'All finite stages and an auxiliary Hilbert inductive limit; not the original quantum-measure extension',
          'classification':'h(P)=e(P)^2 mu(P), normalized consistent full-support cylinder probabilities'})

    horizon = []
    harmonic_checks = 0
    chain, antichain = (0,1), (0,0)
    for M in plan['horizons']:
        for p in ps:
            weights = m.pullback(M,lambda order:q.metric(order,p))
            for (n,order), value in weights.items():
                require(value == q.metric(order,p), 'Exact horizon independence for harmonic end weights')
                harmonic_checks += 1
        for label, terminal in [('1',lambda order:F(1)),
                                ('1+relations',lambda order:F(1+q.relation_count(order)))]:
            weights = m.pullback(M,terminal)
            c,a,empty = weights[2,chain],weights[2,antichain],weights[0,()]
            horizon.append({'M':M,'terminal':label,'h0':str(empty),'h2_chain':str(c),
                            'h2_antichain':str(a),'chain_over_antichain':str(c/a),
                            'normalized_chain':str(c/empty),'normalized_antichain':str(a/empty)})
    dump('horizon_controls.json', {'exact_harmonic_checks':harmonic_checks,
          'harmonic_ratio_chain_over_antichain':{str(p):str(p/(4*(1-p))) for p in ps},
          'nonharmonic_controls':horizon,'inference':'Finite trends are not a convergence proof for nonharmonic endpoints'})

    class_counts = [len(q.groups(n)) for n in range(6)]
    require(class_counts == [1,1,2,5,16,63], 'Unlabelled census')
    quotient_checks = {'orbit_aut_counts':0,'representative_independent_columns':0,
                       'endpoint_amplitudes':0,'left_inverse_entries':0}
    for n in range(6):
        for key, copies in q.groups(n).items():
            aut = q.aut_count(copies[0])
            require(len(copies)*aut == m.extensions(copies[0]), 'Orbit count')
            require(sum((F(1,m.extensions(o)) for o in copies),F(0)) == F(1,aut), 'Coherent original sum')
            require(all(q.metric(o,p) == q.metric(copies[0],p) for o in copies for p in ps), 'Isomorphic norm')
            quotient_checks['orbit_aut_counts'] += 1
            if n < 5:
                reference = q.column(copies[0])
                for order in copies:
                    require(q.column(order) == reference, 'Q V = B Q')
                    quotient_checks['representative_independent_columns'] += 1
        if n < 5:
            b,ell = q.quotient_matrix(n),q.left_inverse(n)
            product = q.multiply(ell,b)
            require(product == q.identity(len(q.groups(n))), 'Unique-greatest-element left inverse')
            quotient_checks['left_inverse_entries'] += len(product)**2
            amplitudes = [[F(1,q.aut_count(c[0]))] for c in q.groups(n).values()]
            grown = q.multiply(b,amplitudes)
            expected = [[F(1,q.aut_count(c[0]))] for c in q.groups(n+1).values()]
            require(grown == expected, 'Coherent endpoint amplitude')
            quotient_checks['endpoint_amplitudes'] += len(expected)
    b = q.quotient_matrix(2)
    pkeys,ckeys = list(q.groups(2)),list(q.groups(3))
    ci,ai = pkeys.index(q.canonical(chain)),pkeys.index(q.canonical(antichain))
    mixed = ckeys.index(q.canonical((0,1,0)))
    overlaps = [i for i,row in enumerate(b) if row[ci] and row[ai]]
    require(overlaps == [mixed] and b[mixed][ci] == F(1,3) and b[mixed][ai] == F(4,3), 'Common child witness')
    constructor = []
    for weight in [F(1),F(2)]:
        metric = [[F(1)]]
        for n in range(4):
            grown = q.extend_metric(n,metric,weight)
            bstep = q.quotient_matrix(n)
            require(q.multiply(q.multiply(q.transpose(bstep),grown),bstep) == metric, 'Constructive isometry')
            pivots = q.ldl_pivots(grown)
            constructor.append({'stage':n+1,'complement_weight':str(weight),'dimension':len(grown),
                                 'positive_LDL_pivots':[str(x) for x in pivots]})
            metric = grown
    explicit = q.extend_metric(2,q.identity(2),F(1))
    require(q.multiply(q.multiply(q.transpose(b),explicit),b) == q.identity(2), 'Two-parent full metric')
    q.ldl_pivots(explicit)
    dump('coherent_quotient.json', {'scope':'Unmarked geometry amplitudes after removal of telescoping action phases; full marked-field quotient not constructed',
          'class_counts':class_counts,'checks':quotient_checks,'parents':[list(x) for x in pkeys],
          'children':[list(x) for x in ckeys],'B_2_to_3':[[str(x) for x in row] for row in b],
          'common_child_coefficients':['1/3','4/3'],'forced_diagonal_metric_offdiagonal':'4*d_mixed/9',
          'positive_full_metric_for_identity_parent':[[str(x) for x in row] for row in explicit],
          'constructive_metric_checks':constructor,'uniform_bounds':'NOT_PROVED',
          'physical_event_algebra':'NOT_SELECTED'})

    bounds=[]
    for n in [2,4,6,8,16,32,64]:
        value=F(2**((n//2)*(n-n//2)),math.factorial(n))
        bounds.append({'m':n,'universal_dual_norm_lower_bound':str(value)})
    dump('coherent_contraction.json', {'formula':'||ell_m||^2=sum_P 1/h_m(P)',
          'universal_bound':'||ell_m|| >= sum_P 1/e(P) >= 2^(floor(m/2)*ceil(m/2))/m!',
          'all_integer_bound_examples':bounds,
          'asymptotic':'Bound diverges for all normalized full-support diagonal field-independent norm paths',
          'excluded_claim':'No claim that every quantum measure or unbounded/distributional final contraction is impossible'})
    gates=['MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']
    dump('verification.json', {'audit':plan['id'],'source_commit':plan['source_commit'],'plan_sha256':ph,
          'source_files':len(provenance['files']), 'scoped_decisions':{
              'DIAGONAL_AUXILIARY_NORM_PATH_EXISTENCE':'PASS_CONSTRUCTIVE_ALL_STAGES',
              'UNIQUENESS_FROM_POSITIVITY_AND_COVARIANCE':'FAIL',
              'HARMONIC_TERMINAL_HORIZON_INDEPENDENCE':'PASS_EXACT_CONDITIONAL',
              'UNIFORMLY_BOUNDED_INHERITED_COHERENT_CONTRACTION':'FAIL_IN_DECLARED_DIAGONAL_CLASS',
              'UNMARKED_COHERENT_QUOTIENT_DESCENT':'PASS_EXACT',
              'DIAGONAL_QUOTIENT_ISOMETRY_ALL_STATES':'FAIL_AT_TWO_TO_THREE_ELEMENTS',
              'NONDIAGONAL_UNMARKED_QUOTIENT_METRICS':'PASS_CONSTRUCTIVE_UNQUALIFIED_PHYSICALLY',
              'PHYSICAL_PRODUCT_AND_QUANTUM_MEASURE_EXTENSION':'HOLD'},
          'physical_decisions':{g:'HOLD' for g in gates},'formal_proof_checker':False,
          'new_dynamical_CST_ensembles':False,'physical_parameter_selected':False})
    print(json.dumps({'checks':checks,'harmonic_horizon_checks':harmonic_checks,'quotient_checks':quotient_checks,
                      'exact_result_files':5,'physical_gates':'8 HOLD'},indent=2))


if __name__ == '__main__':
    main()
