"""Cover the physical Y19 interval by closed adjacent slabs in the critical regular sector."""
from dichtevergleich import intersect_fields


def cover(previous,exe,row,initial,cap):
    # At each level the union of the eight closed children is their parent.
    # A rejected coarse search is only a hint to refine; only retained, closed trees count.
    stack=[(initial[19][0],initial[19][1],0)]
    accepted=[]
    coarse=0
    while stack:
        a,b,level=stack.pop()
        fields=[v.copy() for v in initial]
        fields[19][:2]=[a,b]
        narrowed,_=intersect_fields(row,fields,0)
        n,c,o,d=map(int,previous.invoke(exe,row,narrowed,0,cap,'tree').split())
        assert n==2*(c+o)-1
        if o and level<5 and b-a>=8:
            cuts=[a+(b-a)*k//8 for k in range(9)]
            stack.extend((cuts[i],cuts[i+1],level+1) for i in reversed(range(8)))
            coarse+=1
        else:
            accepted.append(dict(ticks=[a,b],nodes=n,closed=c,open=o,depth=d,level=level))
    assert accepted[0]['ticks'][0]==initial[19][0] and accepted[-1]['ticks'][1]==initial[19][1]
    assert all(l['ticks'][1]==r['ticks'][0] for l,r in zip(accepted,accepted[1:]))
    assert all(z['ticks'][0]<z['ticks'][1] for z in accepted)
    return dict(nodes=sum(z['nodes'] for z in accepted),closed=sum(z['closed'] for z in accepted),
                open=sum(z['open'] for z in accepted),depth=max(z['depth'] for z in accepted),
                budget=cap,refined=coarse,slabs=accepted)
