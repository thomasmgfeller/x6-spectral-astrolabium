"""Recompute all finite controls with exact fractions; no network or fitting."""
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import argparse
import hashlib
import json
import marked as z

ROOT = Path(__file__).resolve().parent


def clean(x):
    if isinstance(x, F):
        return str(x)
    if isinstance(x, dict):
        return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (tuple, list)):
        return [clean(v) for v in x]
    return x


def check(ok, message):
    if not ok:
        raise RuntimeError(message)


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    planbytes = (ROOT/'plan.json').read_bytes()
    planhash = hashlib.sha256(planbytes).hexdigest()
    check(planhash == (ROOT/'plan.sha256').read_text().split()[0], 'Frozen plan')
    plan = json.loads(planbytes)
    sources = json.loads((ROOT/'inputs/git_sources.json').read_text())
    for name, meta in sources['files'].items():
        data = (ROOT/'inputs'/name).read_bytes()
        gitsha = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        check(gitsha == meta['sha'], 'Input provenance '+name)
    maxn = plan['finite_reference']['max_m_quotient']
    natural_counts, orbit_counts, amplitudes, matrices = [], [], [], []
    representative_checks = deletion_entries = increment_checks = permutation_checks = 0
    for n in range(maxn+1):
        groups = z.groups(n)
        natural_counts.append(sum(map(len, groups.values())))
        orbit_counts.append(len(groups))
        amp = []
        for key, reps in groups.items():
            check(len(reps)*z.aut(key) == z.m.extensions(key[0]), 'Marked orbit count')
            coefficient = F(1, 2**n*z.aut(key))
            natural_sum = sum((F(1, 2**n*z.m.extensions(p)) for p, c in reps), F(0))
            check(coefficient == natural_sum, 'Marked endpoint coefficient')
            amp.append(coefficient)
            for state in reps:
                a, closed_a = z.action(state), z.action(state, True)
                for perm in permutations(range(n)):
                    relabeled = z.permute(state, perm)
                    check(z.action(relabeled) == a, 'Open action covariance')
                    check(z.action(relabeled, True) == closed_a, 'Closed action covariance')
                    permutation_checks += 1
                if n:
                    p, c = state
                    parent = p[:-1], c[:-1]
                    old = z.action(parent)
                    times = (F(-2),)+tuple(z.TIMES[i] for i in c[:-1])
                    delta = z.m.increment(z.m.with_anchor(p[:-1]), (p[-1]<<1)|1,
                                          times, z.TIMES[c[-1]], z.WEIGHTS[c[-1]])
                    check(tuple(x-y for x, y in zip(a, old)) == delta, 'Action increment')
                    increment_checks += 1
            if n < maxn:
                col = z.column(reps[0])
                for state in reps:
                    check(z.column(state) == col, 'Quotient descent from every representative')
                    representative_checks += 1
        amplitudes.append(amp)
        if n:
            b = z.matrix(n-1)
            check(z.mv(b, amplitudes[n-1]) == amp, 'Endpoint recursion')
            parents = list(z.groups(n-1))
            for row, child in zip(b, groups):
                independent = z.deletion_row(child)
                for value, parent in zip(row, parents):
                    check(value == independent.get(parent, F(0)), 'Maximal deletion route')
                    deletion_entries += 1
            matrices.append({'from_m':n-1,'parents':parents,'children':list(groups),'B':b})
        check(sum(amp) == sum((F(1,z.m.extensions(p)) for p in z.m.natural_orders(n)),F(0)),
              'Removing marks preserves the phase-free endpoint sum')

    metric_results, record_results = [], []
    metric_by_n = {}
    for weight in map(F, plan['finite_reference']['complement_weights']):
        metric = [[F(2),F(0)],[F(0),F(2)]]
        check(z.matmul(z.matmul(z.T(z.matrix(0)),metric),z.matrix(0)) == [[F(1)]], 'Root norm')
        records = [z.projector([True,False]),z.projector([False,True])]
        state = [F(1,2),F(1,2)]
        for n in range(1,plan['finite_reference']['max_m_metric']):
            b, ell = z.matrix(n), z.left_inverse(n)
            check(z.matmul(ell,b) == z.I(len(ell)), 'Left inverse')
            new = z.extend(n,metric,weight)
            pivots = z.q.ldl_pivots(new)
            check(z.matmul(z.matmul(z.T(b),new),b) == metric, 'Metric isometry')
            check(z.matmul(z.T(b),new) == z.matmul(metric,ell), 'Metric adjoint equals L')
            r = z.complement(b,ell)
            moved = [z.matmul(z.matmul(b,e),ell) for e in records]+[r]
            total = z.zero(len(b))
            for i,e in enumerate(moved):
                check(z.matmul(e,e) == e, 'Record idempotence')
                check(z.matmul(z.T(e),new) == z.matmul(new,e), 'Record selfadjointness')
                for j,f in enumerate(moved):
                    if i != j:
                        check(z.matmul(e,f) == z.zero(len(b)), 'Record orthogonality')
                total = z.add(total,e)
            check(total == z.I(len(b)), 'Record completeness')
            probabilities = [z.inner(state,metric,z.mv(e,state))/z.inner(state,metric,state)
                             for e in records]
            newstate = z.mv(b,state)
            newprob = [z.inner(newstate,new,z.mv(e,newstate))/z.inner(newstate,new,newstate)
                       for e in moved]
            check(newprob == probabilities+[F(0)], 'Preparation record probabilities')
            metric_results.append({'from_m':n,'K_scalar':weight,'M':new,'LDL_pivots':pivots,
                                   'L':ell,'isometry':'PASS','adjoint':'PASS'})
            record_results.append({'from_m':n,'K_scalar':weight,'probabilities':newprob,
                                   'projector_count':len(moved),'all_PVM_identities':'PASS'})
            metric,records,state = new,moved,newstate
            if weight == 1:
                metric_by_n[n+1] = new

    metric = metric_by_n[2]
    keys = list(z.groups(2))
    flags = [any(c) for p,c in keys]
    event = z.projector(flags)
    check(z.matmul(z.T(event),metric) != z.matmul(metric,event), 'Expected current-event obstruction')
    i,j = next((i,j) for i in range(len(keys)) for j in range(len(keys))
               if not flags[i] and flags[j] and metric[i][j])
    witness = [F(0)]*len(keys)
    witness[j] = F(1)
    witness[i] = -(metric[j][j]+1)/metric[i][j]
    norm = z.inner(witness,metric,witness)
    bad = z.inner(witness,metric,z.mv(event,witness))/norm
    check(bad < 0 and norm > 0, 'Negative putative Born weight')
    check(z.inner(witness,metric,z.mv(event,witness)) == -1, 'Exact witness numerator')
    atoms = [z.projector([sum(c) == count for p,c in keys]) for count in range(3)]
    branches = [z.mv(e,witness) for e in atoms]
    gram = [[z.inner(a,metric,b)/norm for b in branches] for a in branches]
    vectors = [[sum((branches[k][i] for k in range(3) if mask>>k&1),F(0))
                for i in range(len(keys))] for mask in range(8)]
    d = [[z.inner(a,metric,b)/norm for b in vectors] for a in vectors]
    check(d[7][7] == 1 and d == z.T(d), 'Event normalization and Hermiticity')
    addition_checks = grade2_checks = 0
    for a,b in product(range(8),repeat=2):
        if not a&b:
            for c in range(8):
                check(d[a|b][c] == d[a][c]+d[b][c], 'Event additivity')
                addition_checks += 1
    for a,b,c in product(range(8),repeat=3):
        if not (a&b or a&c or b&c):
            check(d[a|b|c][a|b|c] == d[a|b][a|b]+d[a|c][a|c]+d[b|c][b|c]
                  -d[a][a]-d[b][b]-d[c][c], 'Grade two')
            grade2_checks += 1
    check(all(d[a][a] >= 0 for a in range(8)), 'Branch norm positivity')
    check(sum(gram[k][k] for k in range(3)) != 1, 'Interfering alternatives are not probabilities')
    event_results = {'m':2,'predicate':'At least one nonzero internal dust mark',
                     'M_selfadjoint':'FAIL_EXPECTED','basis':keys,'witness':witness,
                     'witness_norm_squared':norm,'putative_Born_weight':bad,
                     'cross_entry':{'i':i,'j':j,'M_ij':metric[i][j]},
                     'event_atoms':'Number of nonzero dust marks: 0, 1, 2',
                     'atom_Gram':gram,'D_all_8_events':d,'sum_atom_diagonals':sum(gram[k][k] for k in range(3)),
                     'additivity_checks':addition_checks,'grade2_checks':grade2_checks,
                     'strong_positivity':'Analytic Gram-factorization certificate with positive M; no infinite extension claimed'}

    terminal = []
    for n,metric in metric_by_n.items():
        row = [F(1)]*len(metric)
        riesz = z.solve(metric,row)
        dual = sum(riesz)
        effect = [[x*y/dual for y in row] for x in riesz]
        check(dual > 0, 'Positive terminal dual norm')
        check(z.matmul(effect,effect) == effect, 'Normalized readout projector')
        check(z.matmul(z.T(effect),metric) == z.matmul(metric,effect), 'Readout selfadjoint')
        over = z.inner(riesz,metric,z.mv(z.scale(effect,F(2)),riesz))/z.inner(riesz,metric,riesz)
        check(over == 2, 'Overscaled readout fails probability bound')
        terminal.append({'m':n,'dual_norm_squared':dual,'max_lambda':1/dual,
                         'Riesz_vector':riesz,'overscaled_witness_probability':over})
    b,ell = z.matrix(2),z.left_inverse(2)
    old = [F(1)]*len(z.groups(2))
    nextrow = [F(1)]*len(z.groups(3))
    pulled = z.matmul([nextrow],b)[0]
    check(set(pulled) == {F(8,3),F(11,6)}, 'Sum readout cut defect')
    transported = z.matmul([old],ell)[0]
    check(z.matmul([transported],b)[0] == old, 'Transported readout compatibility')
    check(transported != nextrow, 'Transport changes original endpoint functional')
    parent_dual = sum(z.solve(metric_by_n[2],old))
    transported_dual = sum(x*y for x,y in zip(transported,z.solve(metric_by_n[3],transported)))
    check(parent_dual == transported_dual, 'Transported dual norm')

    results = {
        'marked_quotient.json':{'natural_marked_counts':natural_counts,'orbit_counts':orbit_counts,
                               'representative_columns_checked':representative_checks,
                               'independent_deletion_entries':deletion_entries,
                               'endpoint_amplitudes':amplitudes,'matrices':matrices},
        'action_covariance.json':{'permutations_checked_open_and_closed':permutation_checks,
                                  'increments_checked':increment_checks,'phase_handling':'Exact action pairs; no numerical exponential approximation'},
        'metrics_records.json':{'metrics':metric_results,'records':record_results},
        'current_events.json':event_results,
        'terminal_readout.json':{'finite_effects':terminal,'cut_pullback':pulled,
                                 'transported_row':transported,'transported_dual_norm_squared':transported_dual,
                                 'original_sum_cut_compatibility':'FAIL_EXPECTED',
                                 'transported_readout_compatibility':'PASS_WITH_CHANGED_FUNCTIONAL'},
        'verification.json':{'plan_sha256':planhash,'source_commit':plan['source_commit'],
                              'provenance_files_checked':len(sources['files']),
                              'status':'PASS_WITH_SCOPED_NEGATIVE_CONTROLS',
                              'physical_gates':{g:'HOLD' for g in ['MODEL','CURRENT','CORRESPONDENCE',
                                  'BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION']},
                              'formal_proof_checker':False,
                              'scope':plan['scope'],'finite_reference':plan['finite_reference']}}
    for name,value in results.items():
        (out/name).write_text(json.dumps(clean(value),indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':'PASS','natural_marked_states':sum(natural_counts),
                      'orbit_counts':orbit_counts,'representative_columns':representative_checks,
                      'deletion_entries':deletion_entries,'permutation_checks':permutation_checks,
                      'increment_checks':increment_checks,'negative_weight':str(bad),
                      'outputs':len(results)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'results')
    run(parser.parse_args().output)
