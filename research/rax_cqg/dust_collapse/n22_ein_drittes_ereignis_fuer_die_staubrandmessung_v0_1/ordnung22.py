"""Independent Hasse closure for a serial N22 companion."""
def structure(old,row,family):
    cover=set(old)
    n_p,n_f,z_p,z_f=row
    for j,p,f in [(19,n_p,n_f),(20,z_p,z_f),(21,n_p if family=='A' else z_p,n_f if family=='A' else z_f)]:
        # Only maximal elements of the old past and minimal elements of the
        # old future are needed as generating links. Fill in by closure below.
        past=[i for i in range(19) if p & 1<<i]
        future=[i for i in range(19) if f & 1<<i]
        cover.update((i,j) for i in past if all((i,k) not in old for k in past))
        cover.update((j,i) for i in future if all((k,i) not in old for k in future))
    serial=(21,19) if family=='A' else (20,21)
    cover.add(serial)
    rel=cover
    while True:
        nxt=rel|{(a,d) for a,b in rel for c,d in rel if b==c}
        if nxt==rel:break
        rel=nxt
    assert {(i,j) for i,j in rel if i<19 and j<19}==set(old)
    assert not any(i==j for i,j in rel)
    assert {(i,j) for i,j in rel if min(i,j)>=19}=={serial}
    assert not any((serial[0],k) in rel and (k,serial[1]) in rel for k in range(22))
    counts={(i,j):sum((i,k) in rel and (k,j) in rel for k in range(22)) for i,j in rel}
    coeff={e:(1,-9,16,-8)[n] for e,n in counts.items() if n<=3}
    return rel,coeff
