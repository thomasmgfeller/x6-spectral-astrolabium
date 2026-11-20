"""Four-mark projection to the published N14 witness, on the one-edge family."""
import hashlib
import json
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations, product
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
SIX = tuple(combinations(range(6), 2))
SEVEN = tuple(combinations(range(7), 2))
MARKS = [(0, 1, 2, *p) for p in permutations(range(3, 6))]
MASK = sum(1 << (6*i+j) for i in range(5) for j in range(5) if i != j)

def encode(edges, perm, width):
    return sum(1 << (width*perm[i]+perm[j]) for i,j in edges)

def relations(code,n):
    return [divmod(k,n) for k in range(n*n) if code & (1<<k)]

def load_inputs():
    src = HERE/'CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip'
    assert hashlib.sha256(src.read_bytes()).hexdigest() == '4a2b985578e9bf41662af0dede7c2054c8406de4f49d077891f505b0fffd917e'
    with ZipFile(src) as z:
        def read(k):
            return json.loads(z.read('prefix_1564_selection_v0_1/inputs/'+k+'.json'))
        d, residual, weights = read('exchange')['one'], read('exchange_certificate')['one']['residual_orbit_masses'], read('weights')
    c=(HERE/'catalog.json').read_bytes()
    assert hashlib.sha1(b'blob '+str(len(c)).encode()+b'\0'+c).hexdigest()=='f9243eb0396b641413378c3b7936dec4f5d4921a'
    return d, residual, weights, json.loads(c)

def marked_three(d, residual, weights):
    parents={}
    for s,w in d['target_pair_marginal'].items():
        p=int(s)
        pp={p,encode(relations(p,6),(0,1,2,4,3,5),6)}
        parents.update({q:F(w)/len(pp) for q in pp})
    representatives, by_code={}, {}
    for end in d['fully_admissible_end_types']:
        edges=[e for k,e in enumerate(SIX) if end & (1<<k)]
        for code in {encode(edges,p,6) for p in permutations(range(6))}:
            if code & MASK not in parents or code in by_code:
                continue
            orbit={encode(relations(code,6),p,6) for p in MARKS}
            if all(x & MASK in parents for x in orbit):
                rep=min(orbit)
                representatives[rep]=(end, sorted(orbit))
                by_code.update({x:rep for x in orbit})
    assert len(representatives)==d['fully_admissible_orbits'] and len(by_code)==d['paths_valid_in_all_six_orders']
    u=F(d['max_uniform_labelled_path_component'])
    targets={}
    for t in [F(0), F(1,1764)]:
        b={s:len(orbit)*u/len(by_code)+(1-u)*F(residual.get(str(s),0))
           for s,(end,orbit) in representatives.items()}
        b[weights['A']['orbit']]-=t
        b[weights['B']['orbit']]+=t
        assert sum(b.values())==1 and min(b.values())>0
        check=Counter()
        totals=Counter()
        for s,(end,orbit) in representatives.items():
            for raw in orbit:
                check[raw & MASK]+=b[s]/len(orbit)
                if raw&MASK==1564:
                    totals[end]+=b[s]/len(orbit)
        assert check==parents
        assert totals[1790]/totals[5374]==(1 if not t else F(1,3))
        targets[str(t)]=b
    return representatives,by_code,parents,targets

def natural_masks(edges):
    pred=[sum(1<<i for i,j in edges if j==v) for v in range(7)]
    index={p:i for i,p in enumerate(SEVEN)}
    def extend(order,used):
        if len(order)==7:
            pos={v:i for i,v in enumerate(order)}
            yield sum(1<<index[pos[i],pos[j]] for i,j in edges)
        else:
            for v in range(7):
                if not used>>v&1 and not pred[v]&~used:
                    yield from extend(order+(v,),used|1<<v)
    return extend((),0)

def build_columns(reps, by_code, cat):
    good_natural={}
    for k,ranks in cat['ranks_pure_free_mixed'].items():
        if ranks[0] or ranks[2]:
            continue
        key=int(k)
        e=[edge for bit,edge in enumerate(SEVEN) if key & 1<<bit]
        for natural in natural_masks(e):
            good_natural[natural]=key
    assert len(set(good_natural.values()))==cat['counts']['good']==1048
    columns={}
    for rep in sorted(reps):
        edges=relations(rep,6)
        past=[sum(1<<i for i,j in edges if j==v) for v in range(6)]
        future=[sum(1<<j for i,j in edges if i==v) for v in range(6)]
        for pattern in product((-1,0,1),repeat=6):
            pr=sum(1<<i for i,k in enumerate(pattern) if k<0)
            su=sum(1<<i for i,k in enumerate(pattern) if k>0)
            if any((pr>>i&1 and (past[i]&~pr or su&~future[i])) or
                   (su>>i&1 and future[i]&~su) for i in range(6)):
                continue
            fine=edges+[(i,6) for i in range(6) if pr>>i&1]+[(6,j) for j in range(6) if su>>j&1]
            projected=[]
            for v in range(3,7):
                # Delete one mark, keep all earlier root labels fixed and compact the others.
                raw=sum(1 << (6*(i-(i>v)) + j-(j>v)) for i,j in fine if i!=v and j!=v)
                if raw not in by_code: break
                projected.append(by_code[raw])
            if len(projected)!=4:
                continue
            daughter=good_natural.get(next(natural_masks(fine)))
            if daughter is None:
                continue
            key=tuple(sorted(projected))
            code=encode(fine,range(7),7)
            if key not in columns or code<columns[key][1]:
                columns[key]=(daughter,code)
    return dict(sorted(columns.items()))
