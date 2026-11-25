"""Necessary structural conditions for quiet inner vertices at a stationary history."""
from collections import Counter
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'basis'))
import n15

INNER = n15.INNER
I = set(INNER)
FUTURE = set(n15.support.FUTURE)


def structure(typ):
    _,rel = n15.support.geometry(typ)
    all_nodes = set(range(15))
    # Compute the kernel from open intervals independent of the archived edge generator.
    layers = {(i,j):sum((i,k) in rel and (k,j) in rel for k in all_nodes) for i,j in rel}
    edges = {pair:(1,-9,16,-8)[k] for pair,k in layers.items() if k<4}
    maximal = {j for j in I if all((j,v) not in rel for v in I)}
    for j in maximal:
        assert [edges.get((j,k),0) for k in sorted(FUTURE)] == [1,-9,16,-8]
    return rel,edges,maximal


def test_type(typ):
    rel,edges,maximal = structure(typ)
    successors = {i:{j:b for (v,j),b in edges.items() if v==i} for i in INNER}
    forced = maximal | {i for i in I if successors[i].keys() & (maximal|FUTURE)}
    surviving = []
    count = 0
    for mask in range(128):
        occupied = {j for ix,j in enumerate(INNER) if mask & (1<<ix)}
        if not maximal<=occupied:
            continue
        quiet = []
        for i in sorted(I-occupied):
            signs = {1 if b>0 else -1 for j,b in successors[i].items() if j in occupied|FUTURE}
            if len(signs)==1:
                break
            if not signs:
                quiet.append(i)
        else:
            count+=1
            if quiet:
                assert set(quiet).isdisjoint(forced)
                surviving.append({'mask':mask,'quiet':quiet})
    return len(forced)==7, count,surviving


def run():
    stats=Counter()
    eligible={}
    for typ in n15.support.catalogue():
        all_forced,nm,quiet=test_type(typ)
        stats['types']+=1
        stats['support_masks_checked']+=128
        stats['covered_by_maxima_or_future']+=all_forced
        stats['masks_passing_sign_condition']+=nm
        stats['types_with_quiet_candidate']+=bool(quiet)
        stats['candidate_masks']+=len(quiet)
        if quiet:
            eligible[str(typ)]=quiet
    return {'counts':dict(stats),'candidates':eligible}


def prefix_certificate(rel, edges, j):
    """Minimum sum of predecessor coefficients over all prefix ideals."""
    preds={i for i,k in rel if k==j}
    past=list(n15.support.PAST)
    inner=sorted(preds & I)
    minima=[sum(edges.get((p,j),0) for p in past[:n]) for n in range(len(past))]
    for mask in range(1<<len(inner)):
        subset=set(past)|{i for k,i in enumerate(inner) if mask & (1<<k)}
        if all(i in subset or k not in subset for i,k in rel):
            minima.append(sum(edges.get((i,j),0) for i in subset))
    return min(minima)


def sharper_screen(candidates):
    remaining={}
    excluded=[]
    for key,opts in candidates.items():
        rel,edges,_=structure(int(key))
        prefix_min={j:prefix_certificate(rel,edges,j) for j in INNER}
        for row in opts:
            witness=next((j for k,j in enumerate(INNER) if row['mask']&(1<<k) and prefix_min[j]>=0),None)
            if witness is None:
                remaining.setdefault(key,[]).append(row)
            else:
                excluded.append({'type':int(key),'mask':row['mask'],'witness':witness})
    return {'excluded':excluded,'remaining':remaining}


def ratio_certificate(rel,edges,occupied):
    """Two zero-node clock equations that require incompatible values of the same density."""
    from fractions import Fraction as Q
    from itertools import permutations, combinations
    duration=Q(23,6)
    laws={}
    for i in I-occupied:
        receiving=[j for j in occupied if (i,j) in edges]
        if len(receiving)!=1:
            continue
        j=receiving[0]
        b=edges[i,j]
        future=[edges.get((i,k),0) for k in n15.support.FUTURE]
        laws[i]=(j,-Q(sum(future),b),-Q(sum(k*v for k,v in enumerate(future)),b))
    for i,l in combinations(sorted(laws),2):
        j,a,c=laws[i]
        target,d,e=laws[l]
        if j!=target:continue
        def polynomial(t):
            return (a*t[i]+c)*(t[l]-t[j])-(d*t[l]+e)*(t[i]-t[j])
        witnesses=[]
        for order in permutations([i,l,j]):
            # Increasing backwards time t = 2-Y. Later events come first.
            if any((u,v) in rel for n,u in enumerate(order) for v in order[n+1:]):
                continue
            vertices=[dict(zip(order,[Q(0)]*n+[duration]*(3-n))) for n in range(4)]
            coefs=[polynomial(t) for t in vertices]
            for s,t in combinations(vertices,2):
                midpoint={k:(s[k]+t[k])/2 for k in order}
                coefs.append(2*polynomial(midpoint)-(polynomial(s)+polynomial(t))/2)
            if not (min(coefs)>=0 and max(coefs)>0 or min(coefs)<0 and max(coefs)<=0):
                break
            witnesses.append({'order':order,'coefficient_min':str(min(coefs)),'coefficient_max':str(max(coefs))})
        else:
            # Incomparable source clocks may coincide. Strict signs inside the tetrahedra
            # alone say nothing about their shared face.
            if (i,l) not in rel and (l,i) not in rel:
                vertices=[{i:duration,l:duration,j:duration},{i:duration,l:duration,j:Q(0)},
                          {i:Q(0),l:Q(0),j:Q(0)}]
                coefs=[polynomial(t) for t in vertices]
                for s,t in combinations(vertices,2):
                    midpoint={k:(s[k]+t[k])/2 for k in (i,l,j)}
                    coefs.append(2*polynomial(midpoint)-(polynomial(s)+polynomial(t))/2)
                if not (min(coefs)>=0 and max(coefs)>0 or min(coefs)<0 and max(coefs)<=0):
                    continue
                witnesses.append({'tie':[i,l],'coefficient_min':str(min(coefs)),'coefficient_max':str(max(coefs))})
            if witnesses:
                return {'empty_pair':[i,l],'receiver':j,'ratio_laws':[list(map(str,(a,c))),list(map(str,(d,e)))],
                        'simplices':witnesses}
    return None


def ratio_screen(candidates):
    failed=[];remaining={}
    for key,opts in candidates.items():
        rel,edges,_=structure(int(key))
        for row in opts:
            occupied={j for k,j in enumerate(INNER) if row['mask'] & (1<<k)}
            witness=ratio_certificate(rel,edges,occupied)
            if witness:
                failed.append({'type':int(key),'mask':row['mask'],**witness})
            else:
                remaining.setdefault(key,[]).append(row)
    return {'excluded':failed,'remaining':remaining}
