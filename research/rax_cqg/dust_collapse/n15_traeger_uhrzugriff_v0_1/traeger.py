"""Support of the published two-parent amplitude laws. No dust observable enters the laws."""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import csv
import json
import zipfile

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'quellen'


def read(name):
    return json.loads((SRC/name).read_bytes())


def edges(code, size):
    return {e for j,e in enumerate(combinations(range(size),2)) if code>>j & 1}


def natural(edgeset, vertices):
    index=list(combinations(range(len(vertices)),2))
    values=[]
    for perm in permutations(vertices):
        p={v:j for j,v in enumerate(perm)}
        if all(p[a]<p[b] for a,b in edgeset):
            values.append(sum(1<<j for j,(i,k) in enumerate(index) if (perm[i],perm[k]) in edgeset))
    return values


def delete_control(code):
    E=edges(code,7)
    samples=natural(E,range(7))
    archive={int(k) for k in read('katalog.json')['ranks_pure_free_mixed']}
    assert set(samples)&archive=={code}
    with zipfile.ZipFile(SRC/'praefix.zip') as z:
        parents=json.loads(z.read('prefix_1564_selection_v0_1/inputs/exchange.json'))
    @lru_cache(None)
    def six_key(d):
        nodes=tuple(v for v in range(7) if v!=d)
        return min(natural({e for e in E if d not in e},nodes))
    out={}
    for label,target in parents.items():
        if label not in ('one','chain'):
            continue
        six={min(natural(edges(k,6),range(6))) for k in target['fully_admissible_end_types']}
        pairs=set(map(int,target['target_pair_marginal']))
        for raw in list(pairs):
            swap=(0,1,2,4,3,5)
            pairs.add(sum(1<<(6*swap[i]+swap[j]) for i in range(5) for j in range(5) if raw>>(6*i+j)&1))
        histogram=Counter()
        for root in permutations(range(7),3):
            root_edges={(i,j) for i in range(3) for j in range(3) if (root[i],root[j]) in E}
            wanted={(0,2)} if label=='one' else {(0,1),(0,2),(1,2)}
            if root_edges!=wanted:
                continue
            other=tuple(v for v in range(7) if v not in root)
            admissible=0
            for deleted in other:
                tail=tuple(v for v in other if v!=deleted)
                def valid_pair(pair):
                    nodes=root+pair
                    mask=sum(1<<(6*i+j) for i in range(5) for j in range(5) if (nodes[i],nodes[j]) in E)
                    return mask in pairs
                if six_key(deleted) in six and all(valid_pair(p) for p in permutations(tail,2)):
                    admissible+=1
            histogram[admissible]+=1
        out[label]=dict(sorted(histogram.items()))
    return dict(topological_orders=len(samples),distinct_codes=len(set(samples)),archive_match=code,
                root_counts_by_admissible_deletions=out)


def evaluate():
    e=read('gewichte.json')['laws']; ch=read('kette.json')
    families={'Basis':ch['law'],'N13':ch['alternative_same_N13']['law'],'N14':ch['alternative_same_new_N14']['law']}
    with (SRC/'entscheidungen.csv').open() as stream:
        data=list(csv.DictReader(stream))
    assert len({(r['type'],r['inlet_density_center']) for r in data})==len(data)==122
    targets={int(row['type']) for row in data}
    negative={int(row['type']) for row in data if row['status']=='COUNTEREXAMPLE'}
    census=read('kapazitaet.json')['by_type']
    def visible(c):
        rel=edges(c,7)
        return all(sum((v,j) in rel for v in range(7))<4 for j in range(7))
    def cell(c):
        return ('sichtbar' if visible(c) else 'teilweise_unsichtbar')+'__'+('volle_Box' if census[str(c)]['full_box'] else 'Box_nicht_voll')
    assert {int(c) for c in census if cell(int(c))=='sichtbar__volle_Box'}==targets
    assert len(targets)==61 and len(negative)==15
    all_laws={}; support=None
    for ekey,ep in e.items():
        for ckey,cp in families.items():
            for law in (ep,cp):
                assert min(map(Q,law.values()))>0 and sum(map(Q,law.values()))==1
            ea,ca=set(map(int,ep)),set(map(int,cp)); union=ea|ca
            assert (len(ea),len(ca),len(ea&ca),len(union))==(310,206,63,453)
            assert support is None or support==union
            support=union
            all_laws[ekey+' / '+ckey]={t:(Q(ep.get(str(t),0))+Q(cp.get(str(t),0)))/2 for t in union}
    supported=targets&support
    comparison=min((supported&negative) or supported,key=lambda c:(-min(law[c] for law in all_laws.values()),c))
    rows={}
    for key,law in all_laws.items():
        sums=Counter()
        for typ,q in law.items(): sums[cell(typ)]+=q
        assert sum(sums.values())==1
        rows[key]=dict(amplitude_6840=law.get(6840,0),supported_61={c:law[c] for c in sorted(supported)},
                       amplitude_sum_61=sum(law[c] for c in supported),amplitude_sum_by_class=dict(sums))
    checks={c:delete_control(c) for c in {6840,comparison}|supported}
    for c,b in checks.items():
        for name,law in [('one',next(iter(e.values()))),('chain',families['Basis'])]:
            assert bool(b['root_counts_by_admissible_deletions'][name].get(4))==(str(c) in law)
    return dict(selected=comparison,union_count=len(support),certified_or_counterexample_61=sorted(supported),
                counterexamples_in_union=sorted(negative&support),sizes=dict(Counter(cell(c) for c in support)),
                laws=rows,deletion_checks=checks)
