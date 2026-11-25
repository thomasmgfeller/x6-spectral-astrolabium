"""Exact test of three relational interval signatures on the 1048 published N15 types.

Usage: python diamanten.py PATH/TO/gesamtkatalog.json [--out result.json].
Standard library only. Sector labels are the given past/interior/future marks.
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path

CATALOG_HASH = "394f438f7041f5d87db34cbdd162c2eeb5ad71841fb2f965bdd9cd67aa02051a"
P, I, F = (0,1,2,3), (4,5,6,11,12,13,14), (7,8,9,10)
NODES = P+I+F
SECTORS = {v:s for s,g in enumerate((P,I,F)) for v in g}

def require(value, message):
    if not value:
        raise ValueError(message)

def build(code):
    inner = {ij for n,ij in enumerate(combinations(I,2)) if code >> n & 1}
    return set(combinations(P,2))|set(combinations(F,2))|set(product(P,I+F))|set(product(I,F))|inner

def intervals(rel,nodes):
    past = {v:{i for i in nodes if (i,v) in rel} for v in nodes}
    future = {v:{i for i in nodes if (v,i) in rel} for v in nodes}
    order = sorted(nodes,key=lambda v:(len(past[v]),v))
    pairs={}
    for p in order:
        dist={p:0}
        for q in order:
            if q in future[p]:
                length = 1+max(dist[i] for i in past[q] if i in dist)
                dist[q] = length
                pairs[p,q] = (len(future[p]&past[q]),length)
    return pairs

def chain_oracle(rel, p, q, inner_chains):
    # Independent all-subsets oracle using the linear order of both collars.
    strict_between = {v for v in NODES if (p,v) in rel and (v,q) in rel}
    longest_inner = max(len(s) for s in inner_chains if s <= strict_between)
    collars = len(strict_between - set(I))
    return len(strict_between), collars + longest_inner + 1

def profile(rel,nodes,sector):
    pairs = intervals(rel,nodes)
    plain = tuple(sorted(pairs.values()))
    tagged = tuple(sorted((sector[p],sector[q],k,l) for (p,q),(k,l) in pairs.items()))
    return pairs,plain,tagged

def isomorphic_on_inner(c1,c2, reverse=False):
    r={(i,j) for i,j in build(c1) if i in I and j in I}
    target={(j,i) if reverse else (i,j) for i,j in build(c2) if i in I and j in I}
    for sequence in permutations(I):
        mp=dict(zip(I,sequence))
        if {(mp[i],mp[j]) for i,j in r} == target:
            return True
    return False

def invariant_witness_measure(code):
    edges=build(code)
    # Additional label-invariant of the interior for distinguishing chosen witnesses.
    return sorted((sum((w,v) in edges for w in I),sum((v,w) in edges for w in I)) for v in I)

def summarize(blocks):
    sizes=Counter(len(c) for c in blocks.values())
    return dict(signatures=len(blocks),singles=sizes[1],multiple=len(blocks)-sizes[1],
                types_in_multiple=sum(n*v for n,v in sizes.items() if n>1),
                max_multiplicity=max(sizes), multiplicities=dict(sorted(sizes.items())))

def run(catalog):
    raw=catalog.read_bytes()
    require(sha256(raw).hexdigest()==CATALOG_HASH, "catalog SHA-256")
    data=json.loads(raw)
    codes=sorted(int(k) for k,(a,_,c) in data["ranks_pure_free_mixed"].items() if a==c==0)
    require(len(codes)==data["counts"]["good"]==1048,"catalog selection")
    blocks=[defaultdict(list) for _ in range(3)]
    # A bijection deliberately changing labels and the numerical topological order.
    rename={v:(7*v+4)%15 for v in NODES}
    renamed_sector={rename[v]:SECTORS[v] for v in NODES}
    n_checked=0
    for c in codes:
        rel=build(c)
        require(all((i,k) in rel for i,j in rel for jj,k in rel if j==jj),"transitivity")
        require(all((j,i) not in rel for i,j in rel),"asymmetry")
        pairs,plain,tagged=profile(rel,NODES,SECTORS)
        inner_chains=[set(s) for n in range(8) for s in combinations(I,n)
                      if all((a,b) in rel for a,b in combinations(s,2))]
        require(all(pair==chain_oracle(rel,p,q,inner_chains) for (p,q),pair in pairs.items()),"chain oracle")
        n_checked+=len(pairs)
        rp,pl,ta=profile({(rename[i],rename[j]) for i,j in rel},tuple(reversed(sorted(NODES))),renamed_sector)
        require((plain,tagged)==(pl,ta) and all(rp[rename[i],rename[j]]==v for (i,j),v in pairs.items()),"relabel")
        fixed=pairs[P[-1],F[0]]
        require(fixed[0]==7, "fixed interval")
        for block,key in zip(blocks,(fixed,plain,tagged)):
            block[key].append(c)
    witness=None
    for members in sorted(blocks[2].values(),key=lambda t:t[0]):
        for c1,c2 in combinations(members,2):
            deg1,deg2=map(invariant_witness_measure,(c1,c2))
            if deg1==deg2 or deg1==sorted((b,a) for a,b in deg2):
                continue
            require(not isomorphic_on_inner(c1,c2) and not isomorphic_on_inner(c1,c2,reverse=True),"nondual witness")
            witness=dict(code1=c1,code2=c2,
                         inner_past_future_degree_multisets=(deg1,deg2),
                         exhaustive_inner_bijections=5040,
                         same_signature_with_endpoint_sectors=True,
                         inner_isomorphic=False,inner_dual_isomorphic=False)
            break
        if witness: break
    return dict(catalog_sha256=CATALOG_HASH,types=len(codes),comparable_pairs_checked=n_checked,
                endpoint_conventions="I open; Lmax length in edges including both endpoints of a chain; cover = 1.",
                fixed_boundary=dict(**summarize(blocks[0]),classes=[dict(n=n,length=l,count=len(v)) for (n,l),v in sorted(blocks[0].items())]),
                all_comparable_pairs_multiset=summarize(blocks[1]),
                all_comparable_pairs_with_endpoint_sectors=summarize(blocks[2]),
                nondual_collision=witness)

if __name__=="__main__":
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("catalog",type=Path)
    ap.add_argument("--out",type=Path)
    args=ap.parse_args()
    text=json.dumps(run(args.catalog),indent=2,ensure_ascii=False)+"\n"
    if args.out:
        args.out.write_text(text)
    else:
        print(text,end="")
