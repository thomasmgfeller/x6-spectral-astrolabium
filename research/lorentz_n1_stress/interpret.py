"""Explicitly post-hoc interpretation; never changes the frozen endpoints.

Classify every H7 collision by order duality and retain full witness matrices.
This script was written after partial producer outcomes had been inspected.
"""
import hashlib
import json
from pathlib import Path
import check
import produce

HERE=Path(__file__).resolve().parent


def dual(c):
    m=len(c)//2
    b=[[c[j][m+i] for j in range(m)] for i in range(m)]
    return [[0]*m+row for row in b]+[[0]*(2*m) for _ in range(m)]


def run():
    directory=HERE/'results'
    manifest=json.loads((directory/'RESULTS.json').read_text())
    check.require(manifest['status']=='PASS_EXACT_STRESS_TEST_WITH_PRE_RUN_DEVIATION','completed verified run required')
    records=[json.loads(s) for s in (directory/'records.jsonl').read_text().splitlines()]
    lookup={r['id']:r for r in records}; summary=json.loads((directory/'summary.json').read_text())
    pairs=[]; witnesses={}
    for cell in summary['cells'].values():
        for p in cell['all_h7_equal_pairs']:
            a,b=[lookup[name] for name in p['ids']]
            ca,cb=[check.family(r['relation_rows'],r['m']) for r in (a,b)]
            isdual=check.iso(dual(ca),cb)
            check.match(isdual,produce.iso(dual(ca),cb),'dual classification solvers disagree')
            entry={**p,'n':len(ca),'isomorphic_to_time_reverse':isdual}
            pairs.append(entry)
            label='split' if p['q1_separated'] else 'residual'
            if label not in witnesses:
                witness={'ids':p['ids'],'n':len(ca),'isomorphic_to_time_reverse':isdual,
                         'relations':[a['relation_rows'],b['relation_rows']],
                         'bipartite_blocks':[[row[r['m']:] for row in r['relation_rows'][:r['m']]] for r in (a,b)]}
                if p['q1_separated']:
                    qa,qb=a['features']['Q1'],b['features']['Q1']
                    for root in range(len(qa)):
                        if qa[root]!=qb[root]:
                            found=False
                            for direction in range(2):
                                for operator in range(3):
                                    if qa[root][direction][operator]!=qb[root][direction][operator]:
                                        witness['first_sorted_deck_difference']={
                                            'deck_index':root,'direction':['future','past'][direction],
                                            'operator':['S','A','K'][operator],
                                            'coefficients_high_to_low':[qa[root][direction][operator],qb[root][direction][operator]],
                                            'note':'Sorted deck positions are not a proposed root correspondence.'}
                                        found=True; break
                                if found: break
                            break
                witnesses[label]=witness
    report={'schema':'x6.n1-stress-posthoc/1','status':'POST_HOC_DESCRIPTIVE_DIAGNOSIS',
            'knowledge':'Written after partial primary outcomes. Does not change primary sample, features or endpoints.',
            'source_records_sha256':hashlib.sha256((directory/'records.jsonl').read_bytes()).hexdigest(),
            'all_h7_equal_pairs':pairs,'witnesses':witnesses,
            'counts':{'split_dual':sum(p['q1_separated'] and p['isomorphic_to_time_reverse'] for p in pairs),
                      'split_nondual':sum(p['q1_separated'] and not p['isomorphic_to_time_reverse'] for p in pairs),
                      'residual_dual':sum(not p['q1_separated'] and p['isomorphic_to_time_reverse'] for p in pairs),
                      'residual_nondual':sum(not p['q1_separated'] and not p['isomorphic_to_time_reverse'] for p in pairs)}}
    (HERE/'interpretation.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report['counts']))


if __name__=='__main__':
    run()
