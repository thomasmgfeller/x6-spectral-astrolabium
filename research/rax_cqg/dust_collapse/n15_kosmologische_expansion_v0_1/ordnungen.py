"""All inner inclusion-maximal antichains and independent minimum chain covers."""
from collections import Counter
import csv
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT/'quellen'
sys.path.insert(0,str(SOURCE))
import support
import ordnung

def check(condition, text):
    if not condition:
        raise ValueError(text)

def maximal_antichains(nodes, relation):
    neighbors = {v: {w for w in nodes if (v,w) in relation or (w,v) in relation} for v in nodes}
    maximal = []
    for size in range(1,len(nodes)+1):
        for c in combinations(nodes,size):
            if any(w in neighbors[v] for v,w in combinations(c,2)):
                continue
            if any(w not in c and all(w not in neighbors[v] for v in c) for w in nodes):
                continue
            maximal.append(c)
    return maximal

def min_chain_cover(nodes,relation):
    # Bipartite maximum matching in the strict order. Endpoints of matched
    # pairs concatenate into disjoint chains because the order has no cycles.
    right_match = {}
    def augment(i,seen):
        for j in nodes:
            if (i,j) not in relation or j in seen:
                continue
            seen.add(j)
            if j not in right_match or augment(right_match[j],seen):
                right_match[j]=i
                return True
        return False
    for i in nodes:
        augment(i,set())
    return len(nodes)-len(right_match)

def summary(rows):
    return dict(types=len(rows), width_histogram=dict(sorted(Counter(r['width'] for r in rows).items())),
                different_maximal_sizes=sum(r['minimum'] != r['width'] for r in rows),
                maximal_sets=sum(r['count'] for r in rows))

def run(out):
    catalogue = json.loads((SOURCE/'gesamtkatalog.json').read_text())
    eligible = sorted(int(i) for i,(a,_,c) in catalogue['ranks_pure_free_mixed'].items() if a==c==0)
    assay = {int(i) for i in json.loads((SOURCE/'typkatalog.json').read_text())['evaluation_rows']}
    with (SOURCE/'entscheidungen.csv').open() as f:
        second_assay = {int(row['type']) for row in csv.DictReader(f)}
    check(len(eligible)==catalogue['counts']['good']==1048 and len(assay)==61 and
          assay==second_assay and assay.issubset(eligible),'Typauswahl')
    rows=[]
    example=None
    for code in eligible:
        nodes,rel=support.geometry(code)
        check(all((i,k) in rel for i,j in rel for jj,k in rel if j==jj),'Transitivität')
        check(not any((j,i) in rel for i,j in rel),'Zyklus')
        maximal=maximal_antichains(nodes,rel)
        sizes=Counter(map(len,maximal))
        w=max(sizes)
        check(min_chain_cover(nodes,rel)==w,'Breite und Kettenüberdeckung')
        check(all((i,j) in rel for i,j in product(support.PAST,nodes)) and
              all((i,j) in rel for i,j in product(nodes,support.FUTURE)),
              'Randordnung')
        rows.append(dict(type=code, assay61=int(code in assay), minimum=min(sizes),
                         width=w, count=len(maximal),
                         counts_by_size=' '.join(f'{k}:{sizes[k]}' for k in sorted(sizes))))
        if code in assay and min(sizes)<w and example is None:
            example=dict(type=code,smaller=min(maximal,key=len),larger=max(maximal,key=len))
    chain=2**21-1
    nodes,rel=support.geometry(chain)
    check(rel==set(combinations(ordnung.ORDER,2)),'Referenzordnung')
    inner=maximal_antichains(nodes,rel)
    total=maximal_antichains(ordnung.ORDER,rel)
    check(len(inner)==7 and len(total)==15 and all(len(x)==1 for x in total),'Referenzkette')
    register=json.loads((SOURCE/'p3_register.json').read_text())
    state=Counter(row['execution'] for row in register if row['checkpoint_id']=='P3')
    expected=set(product(('1/4','1','4'),('0','1/4','1/2','3/4','1'),(1,2,4,8)))
    keys={(r['checkpoint_context']['M'],r['checkpoint_context']['x'],r['checkpoint_context']['density_ratio']) for r in register}
    check(keys==expected and state=={'NOT_RUN':60},'P3-Eingaberegister')
    with (out/'antiketten.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result=dict(all_1048=summary(rows), subset_61=summary([r for r in rows if r['assay61']]),
                witness=example,chain=dict(type=chain,in_subset_61=chain in assay,
                    inner_events=list(nodes),all_events=list(ordnung.ORDER),pairs=len(rel),
                    inner_maximal_antichains=inner,full_maximal_antichains=total),P3=state)
    (out/'ordnung.json').write_text(json.dumps(result,indent=2)+'\n')
