# Julia 1.9+; independent floating-point spectral reference (NOT a formal certificate)
using LinearAlgebra
function laplacian(n, edges)
    L=zeros(Float64,n,n)
    for (a,b,w) in edges
        @assert 1<=a<=n && 1<=b<=n && a!=b && w>0
        L[a,a]+=w;L[b,b]+=w;L[a,b]-=w;L[b,a]-=w
    end
    L
end
cases=[("path4",4,[(1,2,1.0),(2,3,1.0),(3,4,1.0)],2-sqrt(2.0)),
       ("triangle",3,[(1,2,1.0),(2,3,1.0),(1,3,1.0)],3.0),
       ("weighted2",2,[(1,2,0.125)],0.25),
       ("rounded_signal_path",4,[(1,2,0.367879),(2,3,0.367879),(3,4,0.367879)],0.367879*(2-sqrt(2.0)))]
for (name,n,edges,expected) in cases
    eig=sort(eigvals(Symmetric(laplacian(n,edges))))
    @assert isapprox(eig[2],expected,atol=1e-12,rtol=1e-12)
    println(name,": PASS gap=",eig[2])
end
