"""All one-event extensions, counted independently by marked insertion and deletion."""
from collections import Counter
from itertools import combinations
from math import factorial
import json
import numpy as np
import sympy as sp
from model import CACHE, growth, orders, geometry, layout, write

def linear_orders(n, edges):
    predecessors = [sum(1 << i for i,j in edges if j==v) for v in range(n)]
    def walk(prefix, used):
        if len(prefix)==n:
            yield prefix
        else:
            for v in range(n):
                if not used & (1<<v) and not predecessors[v] & ~used:
                    yield from walk(prefix+(v,), used | (1<<v))
    return walk((),0)

def natural_mask(edges, order):
    pos = {v:k for k,v in enumerate(order)}
    bits = growth.positions(len(order))
    return sum(bits[pos[i],pos[j]] for i,j in edges)

def seven_catalog(six):
    # The largest natural label is maximal. Its predecessor set is an ideal.
    all_masks=set()
    for parent in six:
        edges=orders.bit_edges(6,parent)
        for ideal in range(64):
            if any(ideal>>j&1 and not ideal>>i&1 for i,j in edges):
                continue
            new=edges | {(i,6) for i in range(6) if ideal>>i&1}
            all_masks.add(natural_mask(new,range(7)))
    lookup, automorphisms={},{}
    for mask in sorted(all_masks):
        if mask in lookup:
            continue
        edges=orders.bit_edges(7,mask)
        orbit=Counter(natural_mask(edges,o) for o in linear_orders(7,edges))
        assert min(orbit)==mask and len(set(orbit.values()))==1
        automorphisms[mask]=orbit[mask]
        lookup.update(dict.fromkeys(orbit,mask))
    assert all_masks==set(lookup)
    return lookup,automorphisms

def action_matrix(key):
    # Twice the Hessian, with integer section and both boundary chirps.
    inner,coef,_=layout(key)
    n=len(inner)
    H=np.zeros((8+n,8+n),dtype=np.int64)
    for (i,j),w in coef.items():
        H[i,i]-=w; H[j,j]-=w; H[i,j]+=w; H[j,i]+=w
    E=np.zeros_like(H)
    E[1:4,:3]=E[7:10,3:6]=np.eye(3,dtype=int)
    for j,node in enumerate(inner):
        E[node,6+j]=1
    am,bm,ap,bp=[np.array(v,dtype=np.int64).ravel() for v in (geometry.AM,geometry.BM,geometry.AP,geometry.BP)]
    E[:4,-2]=bm; E[7:11,-1]=bp
    G=E.T@H@E
    G[-2,:3]-=2*am[1:]; G[:3,-2]-=2*am[1:]
    G[-1,3:6]+=2*ap[:3]; G[3:6,-1]+=2*ap[:3]
    G[-2,-2]-=2*(am@bm); G[-1,-1]+=2*(ap@bp)
    return G

def ranks(key):
    G=action_matrix(key); n=key[0]; I=list(range(6,n+8))
    def rank(a):
        return sp.Matrix(a.tolist()).to_DM().rank()
    pure=n-rank(G[:,6:6+n])
    free=n+2-rank(G[:,I])
    defect=len(I)+3-free-rank(G[np.ix_([0,1,2]+I,[3,4,5]+I)])
    assert free>=pure>=0 and defect>=0
    return [pure,free,defect]

def cheap_plan(mask):
    # Search for an elimination of maximum joint factor size three.
    inner,coef,_=layout((7,mask))
    scopes=[frozenset([j]+[i for i in inner if coef.get((i,j),0)]) for j in inner]
    def search(active,left):
        if not left:
            return ()
        for j in left:
            joint=frozenset.union(*(s for s in active if j in s))
            if len(joint)>3:
                continue
            tail=search([s for s in active if j not in s]+[joint-{j}],tuple(k for k in left if k!=j))
            if tail is not None:
                return (j,)+tail
        return None
    return search(scopes,inner)

def calculate():
    prior=json.loads((CACHE/'reference/growth.json').read_text())
    parents=prior['sequential_admissible']
    six,aut6=growth.natural_orbits(6)
    seven,aut7=seven_catalog(six)
    assert (len(seven),len(aut7))==(96428,2045)
    forward={}
    for p in parents:
        forward[p]=Counter(seven[natural_mask(e,next(linear_orders(7,e)))] for e in orders.extend(orders.bit_edges(6,p),6))
    for end,a in aut7.items():
        e=orders.bit_edges(7,end)
        deletes=Counter(six[natural_mask({(i,j) for i,j in e if v not in (i,j)},[i for i in range(7) if i!=v])] for v in range(7))
        for p in parents:
            assert forward[p][end]*a==deletes[p]*aut6[p],(p,end)
    ends=sorted(set().union(*forward.values()))
    # Replay the rank convention on all 238 published N14 screens.
    for name,v in prior['audit'].items():
        z=v['independent_integer_rank_check']
        assert ranks((6,int(name)))==[z['pure_bulk_nullity'],z['full_free_nullity'],z['reduced_mixed_defect']]
    audit={m:ranks((7,m)) for m in ends}
    good=[m for m,(p,_,d) in audit.items() if p==0 and d==0]
    support=set(good)
    exclusions=Counter((bool(p),bool(d)) for p,_,d in audit.values())
    pilot={m:plan for m in good if (plan:=cheap_plan(m)) is not None}
    byroot={}
    for root,row in prior['by_root'].items():
        paths=Counter()
        for p,count in row['admissible_end_marked_paths'].items():
            paths.update({m:count*k for m,k in forward[int(p)].items()})
        byroot[root]={'before':sum(paths.values()),'after':sum(paths[m] for m in support),
                      'ends':{m:c for m,c in paths.items() if m in support}}
    counts={'natural':len(seven),'unlabelled':len(aut7),'labelled':sum(factorial(7)//a for a in aut7.values()),
            'parents':len(parents),'raw':len(ends),'good':len(good),'excluded':len(ends)-len(good),
            'only_bulk':exclusions[True,False],'only_mixed':exclusions[False,True],'both':exclusions[True,True],
            'pairs_before':sum(map(len,forward.values())),'pairs_after':sum(len(set(r)&support) for r in forward.values()),
            'parents_with_child':sum(bool(set(r)&support) for r in forward.values()),
            'paths_before':sum(r['before'] for r in byroot.values()),'paths_after':sum(r['after'] for r in byroot.values()),
            'width_le_3':len(pilot),'deletion_checks':len(aut7)*len(parents)}
    return {'counts':counts,'parents':forward,'ranks_pure_free_mixed':audit,'cheap_orders':pilot,'roots':byroot}

if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run without -O')
    d=calculate();write('catalog.json',d);print(d['counts'],flush=True)
