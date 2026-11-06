"""Independent closure enumeration and set-intersection arithmetic.

Implementation audit, not a new physical experiment. Uses a different generator
from gluing.py: forward DAGs, transitive closure, then all label permutations.
"""
from itertools import permutations
from pathlib import Path
import json
import gluing

ROOT=Path(__file__).resolve().parent

def check(ok, message):
    if not ok:
        raise RuntimeError(message)

def relation_orders(n):
    forward=[(i,j) for i in range(n) for j in range(i+1,n)]
    natural=set()
    for bits in range(1 << len(forward)):
        edges={edge for k,edge in enumerate(forward) if bits & (1 << k)}
        while True:
            expanded=edges | {(a,d) for a,b in edges for c,d in edges if b==c}
            if expanded==edges:
                break
            edges=expanded
        natural.add(frozenset(edges))
    labeled=set()
    for rel in natural:
        for p in permutations(range(n)):
            labeled.add(frozenset((p[i],p[j]) for i,j in rel))
    return labeled

def scalar(rel, nodes):
    values={0:-1,1:9,2:-16,3:8}
    return len(nodes)+sum(values.get(len({z for z in nodes if (x,z) in rel and (z,y) in rel}),0)
                         for x,y in rel if x in nodes and y in nodes)

def run():
    rows=[]
    for n in range(1,6):
        orders=relation_orders(n)
        codes={sum(2**(i*n+j) for i,j in r) for r in orders}
        check(codes==set(gluing.all_posets(n)),f'Enumeration N={n}')
        count=0
        for rel in orders:
            code=sum(2**(i*n+j) for i,j in rel)
            nodes=set(range(n)); full=scalar(rel,nodes)
            check(full==gluing.action(code,n),'Independent full action')
            for mask in range(1,2**n-1):
                a={i for i in nodes if mask & (1 << i)}; b=nodes-a
                delta=full-scalar(rel,a)-scalar(rel,b)
                check(delta==sum(gluing.coupling(code,n,mask,(2**n-1)^mask)),
                      'Independent gluing correction')
                count+=1
        rows.append({'N':n,'labeled_orders':len(orders),'partition_checks':count})
    result={'status':'PASS_IMPLEMENTATION_CROSSCHECK','method':'Forward DAG closure plus all permutations; independent set-based interval counts',
            'rows':rows,'total_orders':sum(r['labeled_orders'] for r in rows),
            'total_partition_checks':sum(r['partition_checks'] for r in rows),
            'physical_ensemble':False}
    (ROOT/'results/independent_verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    run()
