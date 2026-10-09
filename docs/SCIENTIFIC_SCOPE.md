# Scientific contract

For a finite connected undirected graph with strictly positive rational weights, L is the symmetric Laplacian. Its nullspace is span(1). On that space, M(b)=L+(b+1)J/n-bI has eigenvalue 1. On the orthogonal complement, eigenvalues are lambda_i(L)-b. Therefore M(b) is positive definite iff lambda_2(L)>b. An upper bound is supplied by a Rayleigh quotient of x orthogonal to 1; choosing x=e_i-e_j gives (d_i+d_j+2w_ij)/2.

Limits: component-wise bounds do not imply positive global lambda_2 for disconnected graphs; rounding changes the operator; floating-point Julia checks do not prove exact certificates; signal-to-graph mapping is a modelling choice, not a physical theorem. No general quantum-gravity or Temperley-Lieb result is certified by this package.

Falsification: test equality cases, too-high lower bounds, disconnected graphs, isolated nodes, invalid weights, malformed input, tampered certificates, extreme rational sizes and browser failures. Never treat NOT_EXECUTED as PASS.
