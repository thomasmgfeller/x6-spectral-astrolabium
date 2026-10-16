"""Post-hoc unpacking of the already computed R2 round-two witness.

Not a fourth candidate in the frozen comparison. No change to its endpoints.
"""
from collections import Counter
from itertools import permutations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]


def require(ok,why):
    if not ok:
        raise ValueError(why)


def run():
    target=json.loads((HERE/'results/target.json').read_text())
    require(target['R2_first_distinguishing_round']==2,'witness stage')
    color=target['R2_witness_color']['color'];trace=json.loads((HERE/'results/rounds.json').read_text())['8']
    source={r['id']:r for r in map(json.loads,(ROOT/'research/lorentz_n1_stress/results/records.jsonl').read_text().splitlines())}
    graphs=[]
    for name in target['ids']:
        rows=source[name]['relation_rows'];m=len(rows)//2;b=[[int(x) for x in row[m:]] for row in rows[:m]]
        sets=[{j for j,x in enumerate(row) if x} for row in b]
        gram=[[sum(x*y for x,y in zip(a,d)) for d in b] for a in b]
        require(gram==[[len(a&d) for d in sets] for a in sets],'independent Gram calculation')
        graph_index=trace['ids'].index(name);colors=trace['rounds'][2]['matrices'][graph_index]
        signatures={(u,v):(gram[u][v],tuple(sorted((gram[u][w],gram[w][v]) for w in range(m)))) for u,v in permutations(range(m),2)}
        positions=[uv for uv in signatures if colors[uv[0]][uv[1]]==color]
        graphs.append({'id':name,'B':b,'signatures':signatures,'colors':colors,'positions':positions})
    require(not graphs[0]['positions'] and graphs[1]['positions'],'archived R2 witness counts')
    root=graphs[1]['positions'][0];descriptor=graphs[1]['signatures'][root]
    results=[]
    for g in graphs:
        matches=[uv for uv,s in g['signatures'].items() if s==descriptor]
        require(matches==g['positions'],'direct descriptor and recorded R2 class agree on all lower ordered pairs')
        results.append({'id':g['id'],'ordered_pair_count':len(matches),'pairs_zero_based':[list(uv) for uv in matches],
                        'B_rows':[''.join(map(str,row)) for row in g['B']]})
    out={'status':'PASS_POST_HOC_WITNESS_UNPACKING','scope':'Interpretation of the frozen R2 result; selected after results, not a fourth tested candidate or held-out endpoint.',
         'definition':'For ordered distinct lower vertices u,v, G=B B^T, use (G[u,v], multiset_w (G[u,w],G[w,v])) over every lower w, including u and v.',
         'common_successors_of_root_pair':descriptor[0],
         'joint_common_successor_histogram':[{'counts':list(k),'multiplicity':v} for k,v in sorted(Counter(descriptor[1]).items())],
         'records':results,'verification':'Scalar dot products equal explicit neighbor-set intersections; descriptor membership equals the original round-two R2 witness color on every ordered lower pair in both target orders.'}
    (HERE/'results/certificate.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))


if __name__=='__main__':
    run()
