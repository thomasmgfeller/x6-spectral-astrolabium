"""Trace-compatible auxiliary refinements and sharp energy quadrature controls.
SPDX-License-Identifier: Apache-2.0
"""
from ce_common import *
from ce_energy import laplacian

def path_trace(n,conductance):
    A=laplacian(n+1,[(i,i+1) for i in range(n)],conductance);boundary=[0,n]
    if n==1:return A
    Q=inv([row[1:n] for row in A[1:n]])
    return [[A[i][j]-dot(A[i][1:n],mv(Q,[A[k][j] for k in range(1,n)])) for j in boundary] for i in boundary]

def run():
    frozen();g=read(HERE/'energy_graph.json');edges=g['directed_hasse_edges'];m=len(edges);levels=[]
    field=[F(i%5-2) for i in range(21)];base=sum((field[i]-field[j])**2 for i,j in edges)
    for n in (1,2,4,8):
        trace=path_trace(n,F(n));assert trace==[[F(1),F(-1)],[F(-1),F(1)]]
        unscaled=path_trace(n,F(1));assert unscaled==[[F(1,n),F(-1,n)],[F(-1,n),F(1,n)]]
        refined=F(0)
        for i,j in edges:
            values=[field[i]+F(k,n)*(field[j]-field[i]) for k in range(n+1)]
            refined+=n*sum((a-b)**2 for a,b in zip(values,values[1:]))
        assert refined==base
        # On every mesh cell: f(s)=s*(ell-s). All quadrature samples vanish.
        ell=F(1,n);cell_integral=ell**3/6;cell_energy=ell**3/3
        total_energy=m*n*cell_energy;normalized_integral=n*cell_integral
        constant_squared=F(1,12*m*n*n)
        assert normalized_integral**2==constant_squared*total_energy
        levels.append(dict(subdivision=n,vertices=21+m*(n-1),edges=m*n,conductance=str(n),
            trace=[[str(v) for v in row] for row in trace],unrenormalized_trace_factor=str(F(1,n)),
            harmonic_extension_energy=str(refined),quadrature_constant_squared=str(constant_squared),
            saturating_bubble_energy=str(total_energy),saturating_bubble_error=str(normalized_integral)))
    return dict(status='AUXILIARY_TRACE_AND_REGULARITY_CERTIFIED',levels=levels,all_level_proofs='THEOREMS.md',
        causal_set_limit_status='HOLD_MISSING_GEOMETRIC_REFINEMENT_AND_LORENTZIAN_IDENTIFICATION',
        applicability=dict(positive_energy='PASS for the declared auxiliary Hasse graph',trace_compatibility='PASS for constructed edge subdivisions',
          physical_refinement='OPEN: artificial edge vertices are not new Poisson observations',
          measure_and_dimension='OPEN: normalized length measure is a chosen metric-graph measure, not spacetime volume',
          lorentzian_operator='OPEN: no identification between positive graph Laplacian and hyperbolic dAlembert operator'),
        scope='A compatible metric-graph auxiliary model and energy-times-discrepancy quadrature theorem. This is not a fractal or Lorentzian causal-set continuum limit; no Kigami/Strichartz theorem is applied outside its hypotheses.')

if __name__=='__main__':
    result=run()
    if '--verify' in sys.argv:assert result==read(HERE/'compatibility.json')
    else:save(HERE/'compatibility.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='levels'}))
