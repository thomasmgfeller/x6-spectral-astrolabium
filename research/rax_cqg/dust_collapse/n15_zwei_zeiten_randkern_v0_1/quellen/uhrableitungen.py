"""Exact observability of the seven free inner densities through clock-Hessian queries on the chain."""
from fractions import Fraction as Q
from itertools import combinations
from collections import Counter

from modell import a,s


def combination(rows,target):
    # Row reduction with tracked coefficients, over Q.
    pivots={}
    def reduce_row(row,weights):
        for j,(v,w) in sorted(pivots.items()):
            z=row[j]
            if z:
                row=[r-z*x for r,x in zip(row,v)]
                weights=[r-z*x for r,x in zip(weights,w)]
        return row,weights
    n=len(rows)
    for i,row in enumerate(rows):
        v,w=reduce_row(list(map(Q,row)),[Q(i==j) for j in range(n)])
        pivot=next((j for j,x in enumerate(v) if x),None)
        if pivot is not None:
            c=v[pivot]
            pivots[pivot]=([x/c for x in v],[x/c for x in w])
    residual,weights=reduce_row(list(map(Q,target)),[Q(0)]*n)
    if any(residual):
        return None
    coeff=[-x for x in weights]
    assert all(sum(c*row[j] for c,row in zip(coeff,rows))==v for j,v in enumerate(target))
    return coeff


def evaluate(code):
    order=a.support.geometry(code)[1]
    edges=a.coefficients(order);nodes=s.I
    assert all((i,j) in order for i,j in combinations(nodes,2))
    def row(i,j):
        # Query -19 times the second derivative; subtract known collar densities.
        return [sum(b*((start==i)-(end==i))*((start==j)-(end==j))
                    for start,end,b in edges if end==v) for v in nodes]
    outcome={}
    invisible_directions={}
    for size in range(len(nodes)+1):
        for selected in combinations(nodes,size):
            access=tuple(s.P)+tuple(s.F)+selected
            keys=[];rows=[]
            for i,ix in enumerate(access):
                for iy in access[i:]:
                    vals=row(ix,iy)
                    if any(vals):
                        keys.append((ix,iy));rows.append(vals)
            answer=combination(rows,[1]*len(nodes))
            if answer is not None:
                outcome[selected]={f'{keys[k][0]},{keys[k][1]}':v for k,v in enumerate(answer) if v}
            elif size<=1:
                # One explicit perturbation with unchanged queries and a unit mass shift.
                columns=[[r[j] for r in rows]+[1] for j in range(len(nodes))]
                witness=combination(columns,[0]*len(rows)+[1])
                assert witness is not None
                invisible_directions[str(selected[0]) if selected else 'exterior_only']=witness
    minimal=min(map(len,outcome));sets=[k for k in outcome if len(k)==minimal]
    access=sets[0]; weights=outcome[access]
    # Direct second differences of the full action; use nonuniform rational fields and
    # include the entire known collar. Zeroing inner weights isolates its Hessian.
    y={v:Q(j*j+1,20) for j,v in enumerate(s.P+s.I+s.F)}
    w={v:Q(2+v,19) for v in range(15)}; collar={v:(0 if v in nodes else z) for v,z in w.items()}
    def act(fields,density):
        return -sum(density.values())/2-sum(b*density[j]*(fields[i]-fields[j])**2 for i,j,b in edges)/38
    step=Q(1,1024)
    def query(i,j,density):
        total=Q(0)
        for p in (-1,1):
            for n in (-1,1):
                args=y.copy();args[i]+=p*step;args[j]+=n*step
                total+=p*n*act(args,density)
        return -19*total/(4*step**2)
    val=Q(0)
    for key,coefficient in weights.items():
        i,j=map(int,key.split(','))
        val+=coefficient*(query(i,j,w)-query(i,j,collar))
    assert val==sum(w[j] for j in nodes)
    # A triangular implementation on the last visible site and the sixth chain site.
    assert (11,13) in sets
    w14=query(13,13,w)+9*w[7]-16*w[8]+8*w[9]
    w13=query(11,13,w)/9
    w12=query(11,11,w)+9*w13-16*w14+8*w[7]
    assert (w12,w13,w14)==tuple(w[j] for j in (12,13,14))
    # Verify the identities coefficient by coefficient for arbitrary densities.
    for v in range(15):
        unit={j:Q(j==v) for j in range(15)}
        recovered14=query(13,13,unit)+9*unit[7]-16*unit[8]+8*unit[9]
        recovered13=query(11,13,unit)/9
        recovered12=query(11,11,unit)+9*recovered13-16*recovered14+8*unit[7]
        assert (recovered12,recovered13,recovered14)==tuple(unit[j] for j in (12,13,14))
    assert len(invisible_directions)==8 and minimal==2
    return dict(inner_order=list(nodes),null_witnesses_for_at_most_one_port=invisible_directions,
                max_inner_clocks_on_one_antichain=1,
                triangular_ports=[11,13],triangular_basis_checks=15,subsets_tested=2**len(nodes),successful_by_cardinality=dict(Counter(map(len,outcome))),
                minimal_number= minimal,smallest_subsets=sets,example_ports=access,
                coefficients_on_collar_subtracted_queries=weights,exact_reconstruction=val)
