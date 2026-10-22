"""A fixed order-derived auxiliary field energy and exact response dual norms.
SPDX-License-Identifier: Apache-2.0
"""
from ce_common import *
from sc_run import gap

def covers(order):
    n=len(order)
    return [(i,j) for i in range(n) for j in range(n) if order[i][j] and not any(order[i][k] and order[k][j] for k in range(n))]

def laplacian(n,edges,c=F(1)):
    assert c>0 and len({tuple(sorted(e)) for e in edges})==len(edges)
    A=[[F(0) for _ in range(n)] for _ in range(n)]
    for i,j in edges:
        assert 0<=i<n and 0<=j<n and i!=j
        A[i][i]+=c;A[j][j]+=c;A[i][j]-=c;A[j][i]-=c
    seen={0}
    while True:
        new=seen|{j for i in seen for j in range(n) if A[i][j]<0}
        if new==seen:break
        seen=new
    assert len(seen)==n,'disconnected auxiliary graph'
    return A

def dual_squared(v,Q):
    assert sum(v)==0
    answer=dot(v[1:],mv(Q,v[1:]));assert answer>=0
    return answer

def run():
    frozen();b=setup();edges=covers(b['w']['full_order']);L=laplacian(21,edges);Q=inv([row[1:] for row in L[1:]])
    base=[F(0)]*4+b['weights'];nb=sqrt_bounds(dual_squared(base,Q))
    scan=read(HERE.parent/'spatial_search'/'candidates.json.gz')
    ids=[read(HERE.parent/'spatial_search'/'summary.json')['selected']['index']]+[r['index'] for r in read(HERE.parent/'spatial_search'/'marginal_diagnostic.json')['results']]
    results=[];witness=None
    for index in ids:
        row=scan[index];zz=deform(b['z'],row['node'],row['axis'],row['sign'],F(row['step']));certify_order(zz,b['w']['full_order'])
        alt=[F(0)]*4+exact_weights(zz,F(b['w']['scale']));delta=[v-u for u,v in zip(base,alt)]
        d2=dual_squared(delta,Q);a2=dual_squared(alt,Q);nd,na=sqrt_bounds(d2),sqrt_bounds(a2)
        relative=outward(2*nd[0]/(nb[1]+na[1]),2*nd[1]/(nb[0]+na[0]))
        results.append(dict(index=index,symmetric_weight_gap=row['relative'],symmetric_energy_response_gap=relative,
            worst_response_difference=outward(*nd),response_difference_squared=outward(d2,digits=60)))
        if index==ids[0]:
            potential=[F(0)]+mv(Q,delta[1:])
            assert mv(L,potential)==delta and dot(potential,mv(L,potential))==d2==dot(delta,potential)
            witness=dict(index=index,delta=[str(x) for x in delta],grounded_potential=[str(x) for x in potential],squared_dual_norm=str(d2))
    full=[[F(0)]*21]+[[F(0)]+row for row in Q]
    resistances=[full[i][i]+full[j][j]-2*full[i][j] for i in range(21) for j in range(i+1,21)]
    assert min(resistances)>0
    graph=dict(nodes=21,directed_hasse_edges=[list(e) for e in edges],conductance='1',energy='sum over Hasse edges (f_i-f_j)^2',
        grounded_inverse=[[str(x) for x in row] for row in Q],resistance_range=[str(min(resistances)),str(max(resistances))],witness=witness)
    summary=dict(status='AUXILIARY_FIELD_RESPONSE_CERTIFIED',pairs=len(results),nodes=21,edges=len(edges),selected_pair=results[0],
        field_class='E(f)<=1 on fixed unit-conductance Hasse graph, modulo constants',
        physical_energy_claim=False,statistical_law_bounds_changed=False,
        scope='Additional explicitly chosen regularity class derived only from the shared selected-node order. Energy and conductances are fixed before comparing pairs. Neither Lorentzian physical energy nor field smoothness learned from the counts.')
    return graph,results,summary

if __name__=='__main__':
    for name,data in zip(('energy_graph.json','energy_pairs.json','energy_summary.json'),run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
    print(json.dumps(read(HERE/'energy_summary.json')))
