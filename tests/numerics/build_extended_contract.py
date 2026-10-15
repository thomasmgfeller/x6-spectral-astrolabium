#!/usr/bin/env python3
"""Deterministic, pre-execution check-4 corpus and unchanged numeric tolerances."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import json, random

ROOT=Path(__file__).resolve().parents[2]
def decimal(q):
    with localcontext() as ctx:
        ctx.prec=2000
        return format(Decimal(q.numerator)/Decimal(q.denominator),'f')

cases=[]
def add(name,n,edges,family,order=None,rename=None,**extra):
    order=list(range(n)) if order is None else order
    rename={i:'v'+str(i) for i in range(n)} if rename is None else rename
    lines=[rename[i] for i in order]+[f'{rename[i]} {rename[j]} {decimal(Fraction(w))}' for i,j,w in edges]
    cases.append(dict(id=name,n=n,input='\n'.join(lines),family=family,**extra))

for n in [32,64,96,120]:
    add(f'path{n}',n,[(i,i+1,1) for i in range(n-1)],'path')
for family in ['cycle','star','complete','disconnected','zero']:
    n=120
    edges=([(i,(i+1)%n,1) for i in range(n)] if family=='cycle' else
           [(0,i,1) for i in range(1,n)] if family=='star' else
           [(i,j,1) for i in range(n) for j in range(i+1,n)] if family=='complete' else
           [(i,i+1,1) for i in range(n-1) if i%24!=23] if family=='disconnected' else [])
    add(f'{family}{n}',n,edges,family,expected_gap_status='NO_POSITIVE_MODE' if family=='zero' else 'RESOLVED_AT_TOLERANCE')
for seed in [104729,130363]:
    for n in [16,32,64,96,120]:
        rng=random.Random(seed+n)
        edges=[(i,i+1,Fraction(rng.randint(1,16),8)) for i in range(n-1)]
        edges += [(i,j,Fraction(rng.randint(1,16),8)) for i in range(n) for j in range(i+2,n) if rng.random()<4/n]
        name=f'random{n}_{seed}'
        add(name,n,edges,'seeded_weighted')
        if n==32:
            order=list(range(n));rng.shuffle(order)
            ren={i:'renamed_'+str((i*7)%n) for i in range(n)}
            add(name+'_relabel',n,edges,'metamorphic',order=order,rename=ren,base=name,to_base={ren[i]:'v'+str(i) for i in range(n)})
            reordered=list(edges);rng.shuffle(reordered)
            add(name+'_edgeorder',n,[(j,i,w) for i,j,w in reordered],'metamorphic',base=name,to_base={'v'+str(i):'v'+str(i) for i in range(n)})
            add(name+'_parallel',n,[(i,j,w/2) for i,j,w in edges for _ in range(2)],'metamorphic',base=name,to_base={'v'+str(i):'v'+str(i) for i in range(n)})
for exponent in [-500,500]:
    add('path120_scale_'+str(exponent),120,[(i,i+1,Fraction(2)**exponent) for i in range(119)],'scaled_boundary')
for exponent in [-40,-50]:
    edges=[(i,j,1) for i in range(16) for j in range(i+1,16) if i//8==j//8]+[(7,8,Fraction(2)**exponent)]
    add('cliques_bridge_'+str(exponent),16,edges,'unresolved_gap',expected_gap_status='UNRESOLVED_AT_TOLERANCE')
add('alternating_path16',16,[(i,i+1,Fraction(2)**(-40 if i%2 else 0)) for i in range(15)],'weight_contrast',expected_gap_status='UNRESOLVED_AT_TOLERANCE')
frozen=json.loads((ROOT/'docs/numerics-v1/historical/check3-contract.json').read_text())
contract={k:v for k,v in frozen.items() if k.endswith('_limit') or k=='cluster_relative_gap'}
contract.update(schema='x6.numerics.extended-contract/1',app_sha256='56df754a1c5c3d26022e54b000f0d9e52ab4067d39e6a664556de12bfd7dc071',
    scope='Deterministic 16-120 node corpus, fixed before execution; dyadic exact matrix inputs; finite software qualification only.',
    seeds=[104729,130363],metamorphic_spectrum_scaled_limit=1e-12,metamorphic_projector_frobenius_limit=1e-7,
    expected_controls={'negative':3,'positive':1},cases=cases)
out=ROOT/'docs/numerics-v1/extended/contract.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(contract,indent=2)+'\n')
print(json.dumps({'cases':len(cases),'metamorphic':sum(c['family']=='metamorphic' for c in cases),'path':str(out)}))
