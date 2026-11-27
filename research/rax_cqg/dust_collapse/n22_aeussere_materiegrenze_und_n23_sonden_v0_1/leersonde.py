"""Enumerate all nonempty futures for a free empty birth with old fields fixed."""
from fractions import Fraction as F
from itertools import combinations
from geometrie import diff, mul, square
from stationaritaet import add, const, scale, ratio, kernel

def subsets(s):
    s=sorted(s)
    for n in range(len(s)+1):
        for group in combinations(s,n):
            yield set(group)

def scan(rel,y,w,clock):
    nodes=set(range(22))
    window=(F(15,32),F(17,32))
    allowed={j for j in nodes if clock[j][1]>window[0]}
    base=kernel(rel)
    rows=[]
    for f in subsets(allowed):
        if not f or any(i in f and j not in f for i,j in rel):continue
        # Incoming pairs to the old future depend on the past, outgoing
        # coefficients of the new point depend on the future alone.
        outgoing=kernel(rel|{(22,j) for j in f})
        total=const(0);moment=const(0)
        for j in f:
            weight=scale(w[j],outgoing[22,j])
            total=add(total,weight);moment=add(moment,mul(weight,y[j]))
        assert total[0]*total[1]>0
        raw=ratio(moment,total)
        root=ratio(diff(raw,y[3]),diff(y[7],y[3]))
        band=(window[0],min(window[1],*(clock[i][1] for i in f)))
        if root[1]<band[0] or root[0]>band[1]:
            rows.append(dict(future=sorted(f),root_x=root,allowed=False))
            continue
        assert band[0]<root[0]<=root[1]<min(window[1],*(clock[i][0] for i in f))
        # Include time-overlapping clock boxes in this superset of pasts.
        pool={i for i in nodes-f if clock[i][0]<root[1] and all((i,j) in rel for j in f)}
        vetoes=[]
        for past in subsets(pool):
            if any(j in past and i not in past for i,j in rel):continue
            extended=rel|{(i,22) for i in past}|{(22,j) for j in f}
            new=kernel(extended)
            assert all((i,k) in new for i,j in new for l,k in new if l==j)
            reject={}
            # Corrections on old device edges agree exactly and cancel in delta D.
            for j in f-{7,8,9,10}:
                if w[j][0]<=0:continue
                change=scale(square(diff(y[j],raw)),new[22,j])
                for i in nodes:
                    delta=new.get((i,j),0)-base.get((i,j),0)
                    if delta:
                        change=add(change,scale(square(diff(y[j],y[i])),delta))
                if change[0]*change[1]>0:reject[j]=change
            vetoes.append(dict(past=sorted(past),changed_density=reject))
        assert all(row['changed_density'] for row in vetoes)
        rows.append(dict(future=sorted(f),root_x=root,allowed=True,old_field_vetoes=vetoes))
    assert len(rows)==31
    assert {tuple(q['future']) for q in rows if q['allowed']}=={
        (7,8,9,10,14,21),(7,8,9,10,18,21)}
    assert all(not (q['root_x'][0]<=F(1,2)<=q['root_x'][1]) for q in rows)
    return rows
