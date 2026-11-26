"""Independent chain sum, endpoint check and Gaussian probability quadrature."""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
from itertools import combinations
import json
from vorstudie import inputs
from sonden import (SOURCE, POINTER, analyse, arms, blocks, circuit, labels, topological)


def product(a,b):
    cols=list(zip(*b))
    return [[sum(u*v for u,v in zip(row,col)) for col in cols] for row in a]


def local_operators(bg):
    past={j:{i for i,k in bg.relation if k==j} for j in bg.nodes}
    future={i:{j for k,j in bg.relation if k==i} for i in bg.nodes}
    coeff={0:1,1:-9,2:16,3:-8}
    kernel={(i,j):coeff.get(len(future[i]&past[j]),0) for i,j in bg.relation}
    return kernel


def transfer(bg, kernel):
    live=sorted(set(bg.nodes)-bg.past)
    n=len(live)
    layer=[[kernel.get((i,j),0) for i in live] for j in live]
    power=[[int(i==j) for j in live] for i in live]
    total=[row[:] for row in power]
    for _ in range(n):
        power=product(layer,power)
        total=[[x+y for x,y in zip(r,s)] for r,s in zip(total,power)]
    assert not any(any(r) for r in power)
    return {(j,i):total[x][k] for x,j in enumerate(live) for k,i in enumerate(live)}


def normal_cdf(t,mu,var):
    # Integrate the standard normal power series. All requested arguments have |x|<=1.
    with localcontext() as ctx:
        ctx.prec=60
        x=(D(t)-D(mu.numerator)/D(mu.denominator))/(D(var.numerator)/D(var.denominator)).sqrt()
        assert abs(x)<=1
        term=x
        integral=term
        for k in range(1,45):
            term=term*(-x*x/2)/k
            integral+=term/(2*k+1)
        pi=D('3.141592653589793238462643383279502884197169399375105820974944')
        return D('0.5')+integral/(2*pi).sqrt()


def check(bg, select, matrices, archived):
    z,r=select(bg)
    kernel=local_operators(bg)
    flow=transfer(bg,kernel)
    data=analyse(bg,select,matrices)
    live=sorted(set(bg.nodes)-bg.past)
    earlier_or_parallel=[(j,i) for j in live for i in live if i!=j and (i,j) not in bg.relation]
    assert all(flow[j,i]==0 for j,i in earlier_or_parallel)
    for i in bg.inner:
        for j in bg.inner:
            assert -flow[j,i]==F(archived['bd_probe']['all_inner_sources'][str(i)]['response'][str(j)])
    modes=labels(bg)
    idx={k:i for i,k in enumerate(modes)}
    cdf_count=0
    for key,(src, rec, tx, rx, centre) in arms(bg,z,r).items():
        q,p=circuit(bg,blocks(bg,matrices[0],src,rec,tx,rx),rec,topological(bg))
        rows=[]
        for j in live:
            rows.append([flow[j,i] for i in live]+[-int(tx)*flow[j,src],0])
        rows.append([0]*len(live)+[1,0])
        rows.append([int(rx)*v+int(k==idx[POINTER]) for k,v in enumerate(rows[idx[rec]])])
        assert rows==q
        recrow=rows[-1]
        mu=F(recrow[-2]*centre)
        var=sum(F(v*v,2) for v in recrow[:-2])+recrow[-2]**2+recrow[-1]**2
        arm=data['arms'][key]
        assert (str(mu),str(var))==(arm['mean'],arm['variance'])
        lo,hi=normal_cdf(-1,mu,var),normal_cdf(1,mu,var)
        for a,b in zip(arm['p_left_middle_right'],(lo,hi-lo,1-hi)):
            assert abs(D(a)-b)<D('0.000000000051')
            cdf_count+=1
    # Compute matrix rows via the gradient of the independent pair action.
    ep=data['endpoint']
    def residual(j,field):
        return -sum(F(b,2)*(field.get(j,0)-field.get(i if k==j else k,0))
                    for (i,k),b in kernel.items() if i==j or k==j)
    for key in ('with_receiver_reaction','without_receiver_reaction'):
        phi=dict(zip(ep['support'],map(F,ep[key]['field'])))
        found={str(j):str(g) for j in bg.inner if (g:=residual(j,phi))}
        assert found==ep[key]['source']
    u,h=ep['unforced_rows']
    exact=[[residual(j,{k:1}) for k in (z,r)] for j in (u,h)]
    assert [[str(v) for v in row] for row in exact]==ep['two_rows']
    assert exact[0][0]*exact[1][1]-exact[0][1]*exact[1][0]==F(1,4)
    for j in ep['columns_future_free']:
        assert residual(z,{j:1})==residual(h,{j:1})
    # Covariance under every generator transposition, including collar and probe locations.
    swaps=0
    for i,j in combinations(bg.nodes,2):
        perm={a:(j if a==i else i if a==j else a) for a in bg.nodes}
        other=bg.renamed(perm)
        assert select(other)==(perm[z],perm[r])
        transformed=local_operators(other)
        assert transformed=={(perm[a],perm[b]):v for (a,b),v in kernel.items()}
        assert transfer(other,transformed)=={(perm[a],perm[b]):v for (a,b),v in flow.items()}
        swaps+=1
    # The apparatus has no admissible material readout if its positive carrier is absent.
    changed=bg.renamed({i:i for i in bg.nodes})
    changed.weights[r]=(F(0),F(0))
    try:
        select(changed)
    except ValueError:
        pass
    else:
        raise AssertionError('missing material receiver accepted')
    row={str(i):flow[r,i] for i in live if flow[r,i]}
    return {'receiver_chain_sum':row,'field_transfer_entries':len(flow),
            'checked_not_in_causal_future':len(earlier_or_parallel),'archived_inner_entries':len(bg.inner)**2,
            'relabel_checks':swaps,'cdf_values':cdf_count,'endpoint_minor':'1/4',
            'causality_and_storage':'PASS','no_material_marker':'NO_READOUT'}


if __name__=='__main__':
    with inputs() as values:
        print(json.dumps(check(*values),sort_keys=True,indent=2))
