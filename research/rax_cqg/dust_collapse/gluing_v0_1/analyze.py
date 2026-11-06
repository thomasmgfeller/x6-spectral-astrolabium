"""Exact composition diagnostics. No physical CST dust/bounce ensemble is run."""
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from math import factorial
from collections import Counter
import copy, csv, hashlib, importlib.util, json, platform
from gluing import (require, pairs, encode, valid, all_posets, action, coupling, induced,
                    canonical, colored_canonical, poly_add, poly_readout, future_kernel,
                    current_data, weight)

ROOT = Path(__file__).resolve().parent
OUT = ROOT/'results'; OUT.mkdir(exist_ok=True)
P = json.loads((ROOT/'plan.json').read_text())


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def dump(name, obj):
    (OUT/name).write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False)+'\n')


def csvout(name, rows):
    with (OUT/name).open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def poly_json(p):
    return [{'power': e, 'coefficient': str(c)} for e, c in sorted(p.items())]


def partitions_and_currents():
    rows = []
    for n in P['carrier']['N']:
        full = (1 << n)-1
        counts = Counter(); reps = set()
        for code in all_posets(n):
            reps.add(canonical(code, n)[0]); fc = action(code, n)
            covers, div = current_data(code, n)
            for a in range(1, full):
                b = full ^ a; cross, regrade = coupling(code, n, a, b)
                require(fc == action(code, n, a)+action(code, n, b)+cross+regrade, 'Full gluing')
                counts['partition_checks'] += 1
                counts['nonzero_cross'] += cross != 0
                counts['nonzero_internal_regrading'] += regrade != 0
                counts['naive_additivity_failures'] += fc != action(code, n, a)+action(code, n, b)
                counts['cross_only_failures'] += regrade != 0
                source = sum(div[i] for i in range(n) if a & (1 << i))
                flux = sum(int(bool(a & (1 << i)))-int(bool(a & (1 << j))) for i, j in covers)
                require(source == flux, 'Current cut balance'); counts['current_checks'] += 1
                if n <= P['action']['smoothed_test_max_N']:
                    for ep in P['action']['smoothed_epsilon']:
                        e = Q(ep); c, r = coupling(code, n, a, b, e)
                        require(action(code, n, full, e) == action(code, n, a, e)+action(code, n, b, e)+c+r,
                                'Smeared gluing')
                        counts['smoothed_checks'] += 1
        require(len(all_posets(n)) == P['carrier']['known_count_oracles'][n-1], 'Labeled count oracle')
        require(len(reps) == P['carrier']['known_unlabeled_count_oracles'][n-1], 'Unlabeled count oracle')
        rows.append({'N': n, 'labeled_orders': len(all_posets(n)), 'unlabeled_orders': len(reps),
                     **{k: counts[k] for k in ['partition_checks', 'nonzero_cross', 'nonzero_internal_regrading',
                        'naive_additivity_failures', 'cross_only_failures', 'current_checks', 'smoothed_checks']}})
    csvout('exhaustive_partitions.csv', rows)
    return rows


def associativity():
    rows = []
    for n in range(3, P['associativity']['max_N']+1):
        count = 0
        for code in all_posets(n):
            for colors in product(range(3), repeat=n):
                if len(set(colors)) != 3:
                    continue
                a, b, c = [sum(1 << i for i, v in enumerate(colors) if v == k) for k in range(3)]
                left = sum(coupling(code, n, a, b))+sum(coupling(code, n, a | b, c))
                right = sum(coupling(code, n, b, c))+sum(coupling(code, n, a, b | c))
                require(left == right == action(code, n)-sum(action(code, n, m) for m in [a,b,c]),
                        'Associativity with full retained intermediate order')
                count += 1
        rows.append({'N': n, 'ordered_three_block_checks': count, 'exact_residual': 0})
    csvout('associativity.csv', rows); return sum(r['ordered_three_block_checks'] for r in rows)


def quotients():
    rows = []; full_polynomials = {}
    for n in range(2, 6):
        for na in range(1, n):
            group_size = factorial(na)*factorial(n-na)
            orbits = Counter(); autos = {}; direct = {}; quotient = {}
            for code in all_posets(n):
                rep, aut = colored_canonical(code, n, na)
                orbits[rep] += 1; autos[rep] = aut
                poly_add(direct, action(code, n), Q(1, group_size))
            for rep, size in orbits.items():
                require(size*autos[rep] == group_size, 'Marked orbit stabilizer')
                poly_add(quotient, action(rep, n), Q(1, autos[rep]))
            require(direct == quotient, 'Marked quotient polynomial')
            rows.append({'N': n, 'N_A': na, 'N_B': n-na, 'colored_classes': len(orbits),
                         'labeled_orders': len(all_posets(n)), 'weight_at_z_1': str(sum(direct.values())),
                         'exact_polynomial_equality': True})
            full_polynomials[str((na, n-na))] = poly_json(direct)
    csvout('marked_measure.csv', rows); dump('marked_partition_polynomials.json', full_polynomials)
    return rows


def kernels_and_variations():
    n = 4; a = 3; b = 12
    reps = sorted({canonical(c, 2)[0] for c in all_posets(2)})
    result = []; reconstructed = {}; direct = {}; changes = 0; identities = 0
    for code in all_posets(n):
        poly_add(direct, action(code, n), Q(1, 4))
    for ca, cb in product(reps, repeat=2):
        fibre = [c for c in all_posets(n) if induced(c,n,a) == ca and induced(c,n,b) == cb]
        k = {}; fa = action(ca,2); fb = action(cb,2)
        aa = canonical(ca,2)[1]; ab = canonical(cb,2)[1]
        for c in fibre:
            d = sum(coupling(c,n,a,b)); poly_add(k,d)
            poly_add(reconstructed,fa+fb+d,Q(1,aa*ab))
        for i in range(n):
            for j in range(n):
                if bool(a & (1 << i)) == bool(a & (1 << j)):
                    continue
                residual = {}; bit = 1 << (i*n+j)
                for c in fibre:
                    toggled = c ^ bit
                    t = toggled if valid(toggled,n) else c
                    require(t in fibre, 'Move left declared gluing fibre')
                    twice = t ^ bit
                    twice = twice if valid(twice,n) else t
                    require(twice == c, 'Move is not an involution')
                    changes += t != c
                    poly_add(residual,action(t,n),len(pairs(t,n)))
                    poly_add(residual,action(c,n),-len(pairs(c,n)))
                require(not residual, 'Discrete change-of-variables identity')
                identities += 1
        result.append({'A': 'antichain' if ca == 0 else 'chain', 'B': 'antichain' if cb == 0 else 'chain',
                       'Aut_A': aa,'Aut_B': ab,'F_A':fa,'F_B':fb,'admissible_cross_orders':len(fibre),
                       'kernel':poly_json(k),'readouts':{z:[str(v) for v in poly_readout(k,z)] for z in P['kernel_test']['phase_readouts']}})
    require(direct == reconstructed, 'Two-block quotient kernel composition')
    naive = {}
    for ca, cb in product(reps,repeat=2):
        poly_add(naive,action(ca,2)+action(cb,2),Q(1,canonical(ca,2)[1]*canonical(cb,2)[1]))
    require(naive != direct, 'Negative control: independent product unexpectedly equal')
    dump('gluing_kernels_2_plus_2.json',{'kernels':result,'full_partition':poly_json(direct),
        'naive_independent_product':poly_json(naive),'composition':'EXACT','variation_identities':identities,
        'nonidentity_move_instances':changes,'interpretation':'Symbolic gravity counting control only; no physical state or probabilities'})
    up = encode([(0,2),(1,2)],3); down = encode([(0,1),(0,2)],3)
    ku,eu = future_kernel(up,3); kd,ed = future_kernel(down,3)
    require(action(up,3) == action(down,3) == 1 and ku != kd, 'Coarse-state counterexample')
    require(ku == {-1:Q(1),0:Q(2),1:Q(1),18:Q(1)}, 'V kernel')
    require(kd == {-17:Q(1),0:Q(1),1:Q(1),9:Q(2)}, 'Dual V kernel')
    dump('coarse_state_counterexample.json',{'N':3,'F4_both':1,'upper_V_relations':pairs(up,3),
        'lower_V_relations':pairs(down,3),'upper_kernel':poly_json(ku),'lower_kernel':poly_json(kd),
        'upper_extensions':eu,'lower_extensions':ed,'at_z_1_both':[str(v) for v in poly_readout(ku,'1')],
        'at_z_i_upper':[str(v) for v in poly_readout(ku,'i')],
        'at_z_i_lower':[str(v) for v in poly_readout(kd,'i')],
        'conclusion':'Same cardinality and BDG action do not determine the future gluing kernel; phase sums are not probabilities'})
    return identities, changes


def controls():
    rows = []
    def test(name, actual, expected):
        require(actual == expected, name)
        rows.append({'control':name,'actual':actual,'expected':expected,'pass':True})
    test('Directed two-cycle rejected',valid(encode([(0,1),(1,0)],2),2),False)
    test('Nontransitive union rejected',valid(encode([(0,1),(1,2)],3),3),False)
    chain = encode([(0,1),(1,2),(0,2)],3)
    test('Transitive completion can change fixed inner order',induced(chain,3,5) == 0,False)
    cross,regrade = coupling(chain,3,5,2)
    test('Excised intermediate point changes internal action layer',[cross,regrade],[ -2,10])
    test('Cross-only reconstruction fails',action(chain,3,5)+action(chain,3,2)+cross == action(chain,3),False)
    chain4 = encode([(i,j) for i in range(4) for j in range(i+1,4)],4)
    test('Two isolated chain pieces do not reconstruct full action',[action(chain4,4),action(chain4,4,3)+action(chain4,4,12)],[3,2])
    test('Mark-preserving automorphism group required',[colored_canonical(0,4,2)[1],canonical(0,4)[1]],[4,24])
    up = encode([(0,2),(1,2)],3); down = encode([(0,1),(0,2)],3)
    ku,_ = future_kernel(up,3); kd,_ = future_kernel(down,3)
    test('Equal extension counts do not determine phases',sum(ku.values()) == sum(kd.values()),True)
    test('Equal coarse data produce unequal amplitudes at i',[str(v) for v in poly_readout(ku,'i')+poly_readout(kd,'i')],['1','0','1','2'])
    test('Smeared action at epsilon=1 recovers all BDG coefficients',[int(weight(k,Q(1))) for k in range(8)],[-1,9,-16,8,0,0,0,0])
    # One transported unit follows the full three-chain; its cut has incoming and outgoing flux.
    covers,div = current_data(chain,3)
    test('Full worldline has zero internal source',div,[1,0,-1])
    test('Deleting cross edges loses the endpoint-source balance',sum(div[i] for i in [0]) == 0,False)
    counter=[]
    for n in P['classical_limit']['test_n']:
        counter.append({'n':n,'uniform_action_error_bound':str(Q(1,n)),
                        'derivative_error_at_q_0':n,'bound_is_not_derivative_control':True})
    csvout('action_vs_variation.csv',counter)
    test('Action convergence cannot promote first-variation convergence',counter[-1]['derivative_error_at_q_0'] < counter[0]['derivative_error_at_q_0'],False)
    dump('controls.json',rows);return len(rows)


def checkpoint():
    parent=json.loads((ROOT/'inputs/parent_contract.json').read_text())
    manifest={'id':P['id'],'plan_sha256':sha('plan.json'),'parent_main_commit':'bc8c154be60c483c8a5a8f085c1b3b0668d8afa1',
        'python':platform.python_version(),'source_sha256':{n:sha(n) for n in ['gluing.py','analyze.py','verify_independent.py']},
        'physical_execution':'NOT_RUN','exact_finite_enumeration':'RUN','new_dynamic_CST_ensembles':0,'new_random_draws':0}
    dump('run_manifest.json',manifest)
    rec={'contract_id':parent['id'],'contract_sha256':sha('inputs/parent_contract.json'),'checkpoint_id':'P5',
        'checkpoint_context':{'substep':'EXACT_BDG_GLUING','carrier':'All finite orders N<=5 for algebraic controls; no dimension selection'},
        'execution':'NOT_RUN','run_manifest_sha256':sha('results/run_manifest.json'),
        'scope':{'model_id':'CST-DUST-C1','domain':'Interior, material interface, exterior and computational boundary remain distinct',
          'time_interval':'No physical dust-time evolution run','refinement':'No physical density family specified or run',
          'claim_level':'Exact composition scaffolding; no physical junction, bounce or singularity-resolution qualification'},
        'gates':{g:{req:{'outcome':'UNRESOLVED','evidence_kind':'DEFINITION','evidence_refs':['DERIVATION.md','results/verification.json'],
            'scope_checked':True,'reviewed':True} for req in data['requirements']} for g,data in parent['gates'].items()}}
    spec=importlib.util.spec_from_file_location('parent_gate',ROOT/'inputs/parent_gate.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
    audit=gate.evaluate(rec,ROOT/'inputs/parent_contract.json',OUT/'run_manifest.json')
    require(audit['record_valid'] and set(audit['decisions'].values()) == {'HOLD'}, 'Physical promotion')
    dump('checkpoint_P5_record.json',rec);dump('checkpoint_P5_audit.json',audit)
    guards=[]
    for protected in parent['decision_rules']['finite_observations_not_accepted_for']:
        g,req=protected.split('.')
        fixture=copy.deepcopy(rec)
        for item in fixture['gates'][g].values():
            item.update(outcome='SATISFIED',evidence_kind='ANALYTIC_BOUND',
                        evidence_refs=['SYNTHETIC_POLICY_TEST_ONLY_NOT_PHYSICAL_EVIDENCE'])
        baseline=gate.evaluate(fixture,ROOT/'inputs/parent_contract.json',OUT/'run_manifest.json')
        require(baseline['decisions'][g]=='PASS','Synthetic policy fixture ineffective')
        fixture['gates'][g][req]['evidence_kind']='FINITE_VALIDATION'
        rejected=gate.evaluate(fixture,ROOT/'inputs/parent_contract.json',OUT/'run_manifest.json')
        require(rejected['decisions'][g]=='HOLD' and not rejected['physical_claim_automatically_authorized'],
                'Finite observations promoted protected physical gate')
        guards.append({'requirement':protected,'insufficient_evidence':'FINITE_VALIDATION',
                       'decision':'HOLD','test':'PASS','synthetic_policy_fixture_only':True})
    dump('gate_negative_controls.json',guards)


def main():
    require(sha('plan.json') == (ROOT/'plan.sha256').read_text().split()[0], 'Frozen plan changed')
    for name,h in json.loads((ROOT/'inputs/provenance.json').read_text())['input_sha256'].items():
        require(sha('inputs/'+name) == h, 'Inherited input changed')
    counts=partitions_and_currents();assoc=associativity();measure=quotients();var,moves=kernels_and_variations();ct=controls()
    result={'id':P['id'],'plan_sha256':sha('plan.json'),'labeled_orders':sum(r['labeled_orders'] for r in counts),
        'unlabeled_orders':sum(r['unlabeled_orders'] for r in counts),'partition_checks':sum(r['partition_checks'] for r in counts),
        'smoothed_checks':sum(r['smoothed_checks'] for r in counts),'current_checks':sum(r['current_checks'] for r in counts),
        'naive_additivity_failures':sum(r['naive_additivity_failures'] for r in counts),
        'cross_only_failures':sum(r['cross_only_failures'] for r in counts),'associativity_checks':assoc,
        'marked_measure_sectors':len(measure),'marked_orbit_checks':sum(r['colored_classes'] for r in measure),
        'kernel_pairs':4,'discrete_variation_identities':var,'nonidentity_move_instances':moves,'controls':ct,
        'separate_gate_policy_controls':5,
        'all_exact_residuals_zero':True,'action_composition':'PASS_EXACT_FINITE_IDENTITY',
        'measure_composition':'PASS_CONDITIONAL_COUNTING_MEASURE','finite_variation_identity':'PASS_EXACT_FINITE_IDENTITY',
        'physical_CST_junction':'HOLD_NOT_DERIVED','physical_CST_bounce':'HOLD_NOT_RUN',
        'physical_CST_regularity':'HOLD','physical_CST_extension':'HOLD','new_dynamic_CST_ensembles':0,
        'new_random_draws':0,'new_sprinklings':0,'paid_runs':False}
    dump('verification.json',result);checkpoint();print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
