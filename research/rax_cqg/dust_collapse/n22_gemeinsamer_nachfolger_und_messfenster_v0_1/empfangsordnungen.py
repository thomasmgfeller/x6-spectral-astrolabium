"""One-point extensions in the strict common future of 19 and 20."""
MEASUREMENTS = (19, 20)
OLD = (1 << 19) - 1


def relation(base, past, future):
    edges = base | {(j, 21) for j in MEASUREMENTS}
    edges.update((j, 21) for j in range(19) if past & (1 << j))
    edges.update((21, j) for j in range(19) if future & (1 << j))
    return edges


def via_ideals(base):
    from anbindungen import ideals, masks

    past, future = masks(base)
    required = (1 << 19) | (1 << 20)
    upsets = ideals(future)
    pairs = set()
    for below in ideals(past):
        if below & required != required:
            continue
        possible = (1 << 21) - 1
        for j, above in enumerate(future):
            if below & (1 << j):
                possible &= above
        pairs.update((below & OLD, above) for above in upsets if above & ~possible == 0)
    return pairs


def via_insertion(base):
    # A restriction to previously inserted labels of a transitive order is transitive.
    states = [(0, 0, {(19, 21), (20, 21)})]
    for j in range(19):
        add = {e for e in base if j in e and all(k <= j or k >= 19 for k in e)}
        children = []
        for past, future, previous in states:
            common = previous | add
            options = ((past, future, common),
                       (past | (1 << j), future, common | {(j, 21)}),
                       (past, future | (1 << j), common | {(21, j)}))
            for p, f, edges in options:
                before = {a for a, b in edges if b == j}
                after = {b for a, b in edges if a == j}
                if before & after:
                    continue
                if any((a, b) not in edges for a in before for b in after):
                    continue
                if any(a not in before for a, b in previous if b in before):
                    continue
                if any(b not in after for a, b in previous if a in after):
                    continue
                children.append((p, f, edges))
        states = children
    return {(p, f) for p, f, _ in states}


def classify(edges):
    return tuple(sum((j, k) in edges and (k, 21) in edges for k in range(19))
                 for j in MEASUREMENTS)
