"""Separate replay, row/column isomorphism, determinants and pairwise summary."""
from collections import Counter, defaultdict
import copy
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('prior_checker', HERE.parent/'lorentz_observable_comparison/check.py')
prior = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prior)
METHODS = ['N1','H7','Q1','H7+N1','N1+Q1','H7+N1+Q1']
require = prior.require
match = prior.match


def replay(cfg, m, draw):
    edges = {(i, (i+s) % m) for i in range(m) for s in range(3)}; accepted = 0
    for step in range(20*m*m):
        label = '|'.join(str(x) for x in (cfg['seed'], m, draw, step))
        h = hashlib.sha256(label.encode('utf-8')).hexdigest()
        i, k, j, l = [int(h[z:z+8], 16) % m for z in range(0,32,8)]
        old = {(i,j),(k,l)}; new = {(i,l),(k,j)}
        if i != k and j != l and old <= edges and not new & edges:
            edges.difference_update(old); edges.update(new); accepted += 1
    c = [[int((i,j-m) in edges) if i < m <= j else 0 for j in range(2*m)] for i in range(2*m)]
    return c, accepted


def family(lines, m):
    c = prior.matrix(lines); require(len(c) == 2*m, 'family size')
    require(all(not c[i][j] for i in range(2*m) for j in range(2*m) if not i < m <= j), 'height-two form')
    require(all(sum(c[i]) == 3 for i in range(m)), 'lower degree')
    require(all(sum(c[i][j] for i in range(m)) == 3 for j in range(m,2*m)), 'upper degree')
    return c


def iso(a, b):
    """Exact for height-two regular family: row bijections then column patterns."""
    if len(a) != len(b):
        return False
    m = len(a)//2; x = [row[m:] for row in a[:m]]; y = [row[m:] for row in b[:m]]
    gx = [[sum(u*v for u,v in zip(r,s)) for s in x] for r in x]
    gy = [[sum(u*v for u,v in zip(r,s)) for s in y] for r in y]
    candidates = [[j for j in range(m) if sorted(gx[i]) == sorted(gy[j])] for i in range(m)]
    target = Counter(zip(*x)); mapping = {}; used = set()
    def visit():
        if len(mapping) == m:
            return Counter(tuple(y[mapping[i]][j] for i in range(m)) for j in range(m)) == target
        opts = [(len(poss), i, poss) for i in range(m) if i not in mapping
                for poss in [[j for j in candidates[i] if j not in used and all(gx[i][u] == gy[j][v] for u,v in mapping.items())]]]
        _, i, poss = min(opts)
        for j in poss:
            mapping[i] = j; used.add(j)
            # Partial full column-pattern counts are also a necessary condition.
            indices = sorted(mapping)
            if Counter(tuple(x[u][v] for u in indices) for v in range(m)) == Counter(tuple(y[mapping[u]][v] for u in indices) for v in range(m)) and visit():
                return True
            used.remove(j); del mapping[i]
        return False
    return visit()


def summary(records):
    cells = {}
    for m in sorted({r['m'] for r in records}):
        rr = [r for r in records if r['m'] == m]; methods = {}
        for method in METHODS:
            keys = method.split('+')
            equal = lambda a,b: all(a['features'][k] == b['features'][k] for k in keys)
            groups = []; remaining = list(rr)
            while remaining:
                a = remaining.pop(0); group = [a]+[b for b in remaining if equal(a,b)]
                remaining = [b for b in remaining if not equal(a,b)]; groups.append(group)
            methods[method] = {'classes':len(groups), 'unresolved_pairs':sum(equal(a,b) for a,b in combinations(rr,2)),
                               'max_class_size':max(map(len,groups)), 'residual_groups':sorted(sorted(r['id'] for r in g) for g in groups if len(g)>1)}
        pairs = [{'ids':[a['id'],b['id']], 'q1_separated':a['features']['Q1'] != b['features']['Q1']}
                 for a,b in combinations(rr,2) if a['features']['H7'] == b['features']['H7']]
        split = sum(p['q1_separated'] for p in pairs)
        cells[str(m)] = {'n':2*m, 'representatives':len(rr), 'methods':methods,
                        'n1_equal_pairs_split_by_q1':sum(a['features']['N1'] == b['features']['N1'] and a['features']['Q1'] != b['features']['Q1'] for a,b in combinations(rr,2)),
                        'h7_n1_equal_pairs_split_by_q1':split,
                        'incremental_gate':'ADDITIONAL_SEPARATION_OBSERVED' if split else 'NO_OPPORTUNITY' if not pairs else 'NO_ADDITIONAL_SEPARATION',
                        'all_h7_equal_pairs':pairs,
                        'costs':{k:{'polynomial_calls':3*len(rr) if k=='H7' else sum(6*len(r['relation_rows']) for r in rr) if k=='Q1' else 0,
                                    'integer_payload':sum(prior.payload(r['features'][k]) for r in rr)} for k in ['H7','N1','Q1']}}
    return {'schema':'x6.n1-stress-summary/1','cells':cells,
            'reference':'Full relations and exact directed isomorphism; equality of fingerprints never proves identity.'}


def validate_inputs(cfg, records, draws):
    lookup = {r['id']:r for r in records}; require(len(lookup)==len(records),'duplicate id')
    expected = [(cell['m'],i) for cell in cfg['cells'] for i in range(cell['draws'])]
    match([(d['m'],d['draw']) for d in draws], expected, 'draw coverage')
    match(len(draws),cfg['total_draws'],'draw total'); seen = set()
    for d in draws:
        m = d['m']; c, accepted = replay(cfg,m,d['draw'])
        match(prior.rows(c),d['relation_rows'],'draw replay'); match(accepted,d['accepted_switches'],'accepted count')
        family(d['relation_rows'],m); name=d['representative']; require(name in lookup,'missing representative')
        r = lookup[name]; match(r['m'],m,'representative cell')
        require(iso(c,family(r['relation_rows'],m)),'forged deduplication')
        if name not in seen:
            match(name,f'm{m}-r{d["draw"]:03d}','first representative name')
            match(d['relation_rows'],r['relation_rows'],'first representative relation')
        seen.add(name)
    match(seen,set(lookup),'unused representative')
    return lookup


def negative_controls(cfg, records, draws, expected_summary):
    rejected = list(prior.negative_controls())
    def reject(name, operation):
        try:
            operation()
        except (ValueError, KeyError):
            rejected.append(name)
        else:
            raise ValueError('negative control accepted: '+name)
    bad = copy.deepcopy(draws); bad[0]['relation_rows'][0]='1'+bad[0]['relation_rows'][0][1:]
    reject('stress_altered_relation',lambda:validate_inputs(cfg,records,bad))
    reject('stress_omitted_representative',lambda:validate_inputs(cfg,records[1:],draws))
    bad = copy.deepcopy(expected_summary); first = next(iter(bad['cells']))
    bad['cells'][first]['methods']['N1']['residual_groups'] = [['forged']]
    reject('stress_omitted_residual_results',lambda:match(bad,summary(records),'summary mismatch'))
    return rejected


def run(directory):
    cfg = json.loads((HERE/'contract.json').read_text())['population']
    records = [json.loads(s) for s in (directory/'records.jsonl').read_text().splitlines()]
    draws = json.loads((directory/'draws.json').read_text())
    validate_inputs(cfg,records,draws)
    n1 = {}; buckets = defaultdict(list); polynomials = 0
    for index,r in enumerate(records):
        c = family(r['relation_rows'],r['m']); actual=prior.compute(c)
        match(r['features'],{k:actual[k] for k in ['H7','N1','Q1']},'exact coefficients '+r['id'])
        n1.setdefault(r['m'],actual['N1']); match(actual['N1'],n1[r['m']],'N1 equality')
        prior.invariance(c); polynomials += 3+6*len(c)
        buckets[prior.key(actual['H7'])].append(c)
        if index % 5 == 0:
            print(json.dumps({'phase':'check','completed':index+1,'total':len(records)}),flush=True)
    tested_pairs=0
    for group in buckets.values():
        for a,b in combinations(group,2):
            require(not iso(a,b),'duplicate representatives'); tested_pairs += 1
    result=summary(records); match(json.loads((directory/'summary.json').read_text()),result,'complete summary')
    rejected=negative_controls(cfg,records,draws,result)
    # A false mapping between a proven nonisomorphic pair must also be rejected.
    for m in n1:
        rr=[r for r in records if r['m']==m]
        if len(rr)>1:
            bad=copy.deepcopy(draws); a,b=rr[:2]
            index=next(i for i,d in enumerate(bad) if d['representative']==a['id'])
            bad[index]['representative']=b['id']
            try:
                validate_inputs(cfg,records,bad)
            except ValueError:
                rejected.append('stress_forged_deduplication')
            else:
                raise ValueError('forged stress mapping accepted')
            break
    report={'status':'PASS_EXACT_COUNTERCHECK','draws':len(draws),'representatives':len(records),
            'exact_polynomials_checked':polynomials,'h7_equal_representative_pairs_nonisomorphic':tested_pairs,
            'relabelled_inputs_and_all_quills_checked':len(records),'negative_controls_rejected':rejected,
            'scope':'Separate algorithms in the same authoring process, not external independent human review.'}
    (directory/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
