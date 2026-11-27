"""One-point extensions of each fixed N21 partial order, with the prescribed serial cover."""
N = 21
OLD = (1<<19)-1
EVERY = (1<<N)-1


def masks(base):
    past = [0]*N
    future = [0]*N
    for i,j in base:
        past[j] |= 1<<i
        future[i] |= 1<<j
    return past, future


def ideals(past):
    values = [0]
    for j in sorted(range(N), key=lambda k:past[k].bit_count()):
        values += [v | (1<<j) for v in values if not past[j]&~v]
    return values


def enumerate_extensions(base, row, family):
    past,future = masks(base)
    down,up = ideals(past),ideals(future)
    assert set(up) == {EVERY^v for v in down}
    before = family == 'A'
    meas = 19 if before else 20
    other = 39-meas
    pp,ff = row[:2] if before else row[2:]
    plist = [p for p in down if not p & (1<<other) and bool(p & (1<<meas)) != before]
    flist = [f for f in up if not f & (1<<other) and bool(f & (1<<meas)) == before]
    result = {}
    for p in plist:
        allowed = EVERY
        for j in range(N):
            if p & (1<<j):
                allowed &= future[j]
        for f in flist:
            if f & ~allowed:
                continue
            intermediates = (f & past[meas]) if before else (p & future[meas])
            if intermediates:
                continue
            assert not p&f
            po,fo=p&OLD,f&OLD
            result[po,fo]=(po^pp).bit_count()+(fo^ff).bit_count()
    assert result[pp,ff]==0 and len(result)==len(set(result))
    return result


def relation(base, po, fo, family):
    pair=(21,19) if family=='A' else (20,21)
    edges = base | {pair}
    edges |= {(j,21) for j in range(19) if po & (1<<j)}
    edges |= {(21,j) for j in range(19) if fo & (1<<j)}
    return edges


def floyd(edges):
    bits=[0]*22
    for i,j in edges:
        bits[i] |= 1<<j
    for k in range(22):
        for i in range(22):
            if bits[i] & (1<<k):
                bits[i] |= bits[k]
    return {(i,j) for i in range(22) for j in range(22) if bits[i] & (1<<j)}


def naive_one(base, row, family):
    pp,ff = row[:2] if family=='A' else row[2:]
    confirmed = set()
    for k in range(38):
        po,fo = (pp ^ (1<<k),ff) if k<19 else (pp,ff ^ (1<<(k-19)))
        edges=relation(base,po,fo,family)
        if floyd(edges) != edges or any(i==j for i,j in edges):
            continue
        a,b=(21,19) if family=='A' else (20,21)
        if any((a,k) in edges and (k,b) in edges for k in range(22)):
            continue
        confirmed.add((po,fo))
    return confirmed


def coefficients(edges):
    pred = [set() for _ in range(22)]
    succ = [set() for _ in range(22)]
    for i,j in edges:
        pred[j].add(i)
        succ[i].add(j)
    layers = (1,-9,16,-8)
    return {(i,j):layers[n] for i,j in edges if (n:=len(succ[i]&pred[j]))<4}


def enumerate_by_insertion(base, family):
    # Introduce old labels one at a time. Every restriction of a valid full
    # extension is itself a transitive partial order on the retained labels.
    a,b = (21,19) if family=='A' else (20,21)
    states = [(0,0,{(a,b)})]
    for j in range(19):
        fixed = {e for e in base if j in e and all(k<=j or k>=19 for k in e)}
        children = []
        for p,f,prior in states:
            rest=prior|fixed
            for pp,ff,r in ((p,f,rest),(p|1<<j,f,rest|{(j,21)}),(p,f|1<<j,rest|{(21,j)})):
                if (a,j) in r and (j,b) in r:
                    continue
                # Prior was transitive, so every new violation has j as a vertex.
                past = {i for i,k in r if k==j}
                future = {k for i,k in r if i==j}
                if past&future or any((i,k) not in r for i in past for k in future):
                    continue
                if any(lo not in past for lo,hi in prior if hi in past):
                    continue
                if any(hi not in future for lo,hi in prior if lo in future):
                    continue
                children.append((pp,ff,r))
        states=children
    return {(p,f) for p,f,_ in states}
