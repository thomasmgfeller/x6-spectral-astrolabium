"""Proof-only subdivision for the three undecided types. Both children are always kept."""
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction as Q
from hashlib import sha256
from math import prod
import json
import sys

import pruefen as p
from pruefen import ROOT, support, tube

BUDGET = 512


def split_row(item):
    code,rho = item
    setup = tube.template(code)
    _,center,radius,_,lo,hi = setup
    _, order = support.geometry(code)
    edges = p.coefficients(order)
    profile = {'clock_center':{str(j):str(c) for j,c in center.items()},'clock_halfwidth':str(radius),
               'dwell_affine_ranges_per_vertex':{str(j):[str(a),str(b)] for j,a,b in zip(support.I,lo,hi)}}
    def bound(box):
        return p.phase_box(setup,edges,box[0],rho,dict(zip(support.I,box[1:-1])),box[-1])
    leaves = {}
    roots = {}
    for a,b in support.WINDOWS:
        for i in range(8):
            tile = (a+(b-a)*i/8,a+(b-a)*(i+1)/8)
            box = (tile,)+tuple((center[j]-radius,center[j]+radius) for j in support.I)+((rho-Q(1,32),rho+Q(1,32)),)
            old = p.coherence.phase_box(order,tile,rho,p.MASS,profile)
            new = bound(box)
            k=len(leaves)
            roots[k]=box
            leaves[(k,'')] = (box,(0,)*9,(max(old[0],new[0]),min(old[1],new[1])))
    trace = []
    while True:
        low_key = min(leaves, key=lambda k:(leaves[k][2][0],k))
        high_key = min(leaves, key=lambda k:(-leaves[k][2][1],k))
        bounds = (leaves[low_key][2][0],leaves[high_key][2][1])
        error = p.angle_bound(bounds[1]-bounds[0])
        if p.accepted(error) or len(trace)==BUDGET:
            break
        pick_low = len(trace)%2==0
        key = low_key if pick_low else high_key
        box,depths,parent = leaves.pop(key)
        options = []
        for axis,(left,right) in enumerate(box):
            midpoint=(left+right)/2
            children = []
            for half in ((left,midpoint),(midpoint,right)):
                child = box[:axis]+(half,)+box[axis+1:]
                l,r=bound(child)
                interval = (max(l,parent[0]),min(r,parent[1]))
                assert interval[0]<=interval[1]
                children.append((child,interval))
            score = (-min(c[1][0] for c in children) if pick_low else max(c[1][1] for c in children))
            options.append((score,depths[axis],axis,children))
        _,_,axis,children=min(options)
        trace.append([key[0],key[1],axis])
        depth = depths[:axis]+(depths[axis]+1,)+depths[axis+1:]
        for side,(child,enclosure) in enumerate(children):
            leaves[key[0],key[1]+str(side)] = (child,depth,enclosure)
    # Independently reconstruct the entire leaf partition from the applied cuts.
    reconstructed = {(k,''):box for k,box in roots.items()}
    for k,path,axis in trace:
        box=reconstructed.pop((k,path))
        a,b=box[axis]
        for side,interval in enumerate(((a,(a+b)/2),((a+b)/2,b))):
            reconstructed[k,path+str(side)]=box[:axis]+(interval,)+box[axis+1:]
    assert reconstructed=={k:v[0] for k,v in leaves.items()}
    volume=lambda box:prod(b-a for a,b in box)
    assert sum(map(volume,reconstructed.values()))==sum(map(volume,roots.values()))
    return f'{code};{rho}', dict(passes=p.accepted(error),relative_upper=str(error) if error is not None else None,
                                  phase_interval=list(map(str,bounds)),leaves=len(leaves),splits=trace)


def evaluate():
    archive=json.loads((ROOT/'zeugen.json').read_text())
    table=json.loads((ROOT/'ergebnis.json').read_text())['per_type']
    codes=archive['unresolved_types']
    assert codes==[2454,2456,7069]
    cases=[(c,Q(rho)) for c in codes for rho,v in table[str(c)].items() if not v['angle_joint']]
    with ProcessPoolExecutor(max_workers=len(cases)) as pool:
        rows=dict(pool.map(split_row,cases))
    closed=[c for c in codes if all(rows[f'{code};{rho}']['passes'] for code,rho in cases if code==c)]
    return dict(rows=rows,newly_certified=closed,open_types=sorted(set(codes)-set(closed)))


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Use Python without -O.')
    digest,name=(ROOT/'teilungsplan.sha256').read_text().split()
    assert sha256((ROOT/name).read_bytes()).hexdigest()==digest
    data=evaluate()
    if '--emit' in sys.argv:
        print(json.dumps(data,sort_keys=True,indent=2))
    else:
        assert data==json.loads((ROOT/'teilung.json').read_text())
        print('PASS',data['newly_certified'],'newly certified;',data['open_types'],'open')
