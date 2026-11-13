#!/usr/bin/env python3
"""Exact N11 full-memory action composition. Standard library only.

All action monomials are compared; no quadrature and no probability claim.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parent
N = 11
INTERIOR = {4, 5, 6}
BOUNDARY = set(range(N)) - INTERIOR
B = (1, -9, 16, -8)
SECTORS = ('gravity', 'dust_constant', 'dust_beta', 'scalar_beta')


def empty():
    return {k: {} for k in SECTORS}


def add_term(polynomial, sector, monomial, coefficient):
    key = tuple(sorted(monomial))
    value = polynomial[sector].get(key, F(0)) + coefficient
    if value:
        polynomial[sector][key] = value
    else:
        polynomial[sector].pop(key, None)


def sum_poly(*polys):
    result = empty()
    for p in polys:
        for k, terms in p.items():
            for monomial, coefficient in terms.items():
                add_term(result, k, monomial, coefficient)
    return result


def add_pair(p, i, j, c):
    add_term(p, 'gravity', (), -c)
    for left, right, multiple in [(j,j,1),(i,j,-2),(i,i,1)]:
        add_term(p, 'dust_beta', ('r'+str(j),'t'+str(left),'t'+str(right)), -F(c*multiple,4))
        add_term(p, 'scalar_beta', ('q'+str(left),'q'+str(right)), -F(c*multiple,4))


def direct_action(relations, vertices):
    p = empty()
    for j in vertices:
        add_term(p, 'gravity', (), 1)
        add_term(p, 'dust_constant', ('r'+str(j),), -F(1,2))
    for i,j in relations:
        if i not in vertices or j not in vertices:
            continue
        cardinality = sum((i,z) in relations and (z,j) in relations for z in vertices)
        add_pair(p,i,j,B[cardinality] if cardinality<4 else 0)
    return p


def incremental_action(relations, previous, new):
    if any((new,j) in relations for j in previous):
        raise ValueError('new element must be maximal in its prefix')
    p = empty()
    add_term(p,'gravity',(),1)
    add_term(p,'dust_constant',('r'+str(new),),-F(1,2))
    predecessor = {i for i in previous if (i,new) in relations}
    for i in predecessor:
        # This uses stored past successor sets and only the declared new past.
        old_successors = {z for z in previous if (i,z) in relations}
        count = len(old_successors & predecessor)
        add_pair(p,i,new,B[count] if count<4 else 0)
    return p


def crossing_action(relations, left, right):
    p=empty(); rows=[]
    for i in sorted(left):
        for j in sorted(right):
            if (i,j) not in relations:
                continue
            # Full open interval, including elements on either side of the cut.
            count = sum((i,z) in relations and (z,j) in relations for z in left|right)
            c=B[count] if count<4 else 0
            add_pair(p,i,j,c)
            rows.append({'source':i,'target':j,'open_interval_size':count,'b':c})
    return p,rows


def evaluate(p, fields):
    result={}
    for k,terms in p.items():
        value=F(0)
        for monomial,coefficient in terms.items():
            term=coefficient
            for name in monomial:
                term*=fields[name]
            value+=term
        result[k]=value
    return result


def encode_eval(result):
    return {k:str(v) for k,v in result.items()}


def serialise(p):
    return {k:[{'monomial':list(m),'coefficient':str(c)} for m,c in sorted(terms.items())]
            for k,terms in p.items()}


def run():
    chain={(i,j) for i in range(N) for j in range(i+1,N)}
    variant=chain-{(4,5),(5,6)}
    fields={**{'t'+str(i):F(i-5,5) for i in range(N)},
            **{'r'+str(i):F(i%4+1,8) for i in range(N)},
            **{'q'+str(i):F(i*i-17,11) for i in range(N)}}
    models={};prefix_checks=0;cut_checks=0
    for name,rel in [('chain',chain),('two_relation_variant',variant)]:
        assert all((i,k) in rel for i,j in rel for j2,k in rel if j==j2)
        full=direct_action(rel,set(range(N)))
        previous=set();increments=[]
        for j in range(N):
            inc=incremental_action(rel,previous,j)
            assert sum_poly(direct_action(rel,previous),inc)==direct_action(rel,previous|{j})
            increments.append(inc);previous.add(j);prefix_checks+=1
        assert sum_poly(*increments)==full
        assert full['gravity'][()]==(10 if name=='chain' else 18)
        cut_results=[]
        for last in (3,5):
            left=set(range(last+1));right=set(range(last+1,N))
            local_left=direct_action(rel,left);local_right=direct_action(rel,right)
            crossing,rows=crossing_action(rel,left,right)
            naive=sum_poly(local_left,local_right)
            sewn=sum_poly(naive,crossing)
            assert sewn==full and naive!=full
            direct_value=evaluate(full,fields);naive_value=evaluate(naive,fields)
            cross_value=evaluate(crossing,fields);sewn_value=evaluate(sewn,fields)
            assert sewn_value==direct_value
            assert any(naive_value[k]!=direct_value[k] for k in SECTORS)
            assert all(naive_value[k]+cross_value[k]==direct_value[k] for k in SECTORS)
            # Unique regulator/measure ownership follows the newly introduced variable.
            left_owners=sorted(INTERIOR&left);right_owners=sorted(INTERIOR&right)
            assert set(left_owners).isdisjoint(right_owners)
            assert sorted(left_owners+right_owners)==sorted(INTERIOR)
            extreme=[x for x in rows if (x['source'],x['target'])==(0,10)]
            assert extreme==[{'source':0,'target':10,'open_interval_size':9,'b':0}]
            # Negative control: erase a genuine cross term; must break polynomial equality.
            row=next(x for x in rows if x['b'])
            bad=sum_poly(crossing)
            add_pair(bad,row['source'],row['target'],-row['b'])
            assert sum_poly(naive,bad)!=full
            cut_results.append({'after_vertex':last,'left':sorted(left),'right':sorted(right),
                'crossing_pairs':len(rows),'nonzero_crossing_pairs':sum(bool(x['b']) for x in rows),
                'direct_action_coefficients':encode_eval(direct_value),
                'naive_local_sum_coefficients':encode_eval(naive_value),
                'required_cross_action_coefficients':encode_eval(cross_value),
                'exact_all_monomial_equality':True,'naive_product_rejected':True,
                'dropped_pair_negative_control':[row['source'],row['target'],row['b']],
                'zero_weight_long_interval':extreme[0],
                'Abel_regulator_owners':[left_owners,right_owners]})
            cut_checks+=1
        # Compare both parenthesisations of the same three causal shells.
        shells=[sum_poly(*increments[a:b]) for a,b in [(0,4),(4,6),(6,11)]]
        left_grouped=sum_poly(sum_poly(shells[0],shells[1]),shells[2])
        right_grouped=sum_poly(shells[0],sum_poly(shells[1],shells[2]))
        assert left_grouped==right_grouped==full
        observable=sum((a,b) in rel or (b,a) in rel for a,b in combinations(sorted(INTERIOR),2))
        assert observable==(3 if name=='chain' else 1)
        if name!='chain':
            alternate=[0,1,2,3,5,4,6,7,8,9,10]
            previous=set();alt=[]
            for j in alternate:
                alt.append(incremental_action(rel,previous,j));previous.add(j)
            assert sum_poly(*alt)==full
        models[name]={'F4':str(full['gravity'][()]),'comparable_interior_pairs':observable,
            'direct_action_polynomial_sha256':hashlib.sha256(json.dumps(serialise(full),sort_keys=True,separators=(',',':')).encode()).hexdigest(),
            'cuts':cut_results,'three_shell_associativity':True,
            'alternate_natural_labelling_invariant':True if name!='chain' else 'unique chain order'}
    contract_path=BASE.parents[1]/'contracts/interference_contract.json'
    contract=json.loads(contract_path.read_text())
    assert contract['N']==N and set(contract['interior'])==INTERIOR
    assert set(contract['boundary'])==BOUNDARY
    result={'id':'N11-FULL-MEMORY-COMPOSITION-0.1','all_checks_pass':True,
        'parent_contract_sha256':hashlib.sha256(contract_path.read_bytes()).hexdigest(),
        'parent_commit':contract['parent_commit'],
        'prefix_action_identities':prefix_checks,'two_cut_checks':cut_checks,
        'comparison':'all exact rational monomial coefficients in each action sector',
        'field_example':{k:str(v) for k,v in fields.items()},'models':models,
        'memory':'complete causal prefix relation plus all retained fields; no compression asserted',
        'density_and_clock_measure':'must be supplied once for each integrated variable; no AA seam factor2 transferred',
        'finite_epsilon_kernel_composition':'exact formal copying kernels; absolute convergence and Fubini as specified in report',
        'Abel_limit':'joint boundary test pairing, never a product of separately taken singular limits',
        'geometrical_observable':'number of comparable unordered pairs inside I, a history observable; no radius or physical time calibration',
        'new_integrations':0,'physical_evolution':'NOT_DERIVED',
        'not_proved':['physical history weights','physical state pairing','normalised geometric probabilities','clock calibration','finite-memory Markov closure']}
    (BASE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_checks_pass':True,'prefix_action_identities':prefix_checks,'two_cut_checks':cut_checks,
                      'geometry_values':{name:v['comparable_interior_pairs'] for name,v in models.items()},
                      'new_integrations':0},indent=2))


if __name__=='__main__':
    run()
