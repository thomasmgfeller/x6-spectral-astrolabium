"""Nonlocal L2 projection on existing spatial sites; validated ball arithmetic.

SciPy proposes a tetrahedral complex only. Exact rational orientation,
oriented-face cancellation and convex-boundary predicates certify the mesh.
No quadrature point is inserted into the causal set.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
import math
import numpy as np
from scipy.spatial import Delaunay
from flint import arb, acb, arb_mat, ctx


def require(ok, message):
    if not ok:
        raise ArithmeticError(message)


def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            - a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            + a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def orient(a, b, c, d):
    return det3([[b[k]-a[k], c[k]-a[k], d[k]-a[k]] for k in range(3)])


def parity(seq):
    return (-1)**sum(seq[i] > seq[j] for i in range(len(seq)) for j in range(i+1, len(seq)))


def certify_mesh(points, simplices=None):
    """Positive 3-chain with convex oriented boundary = multiplicity-one hull.

Strict supporting-face tests exclude coplanar boundary ambiguities. All
sites must be vertices; duplicate, omitted or degenerate sites are HOLD.
"""
    points = np.asarray(points, dtype=float)
    require(points.ndim == 2 and points.shape[1] == 3 and np.isfinite(points).all(), 'GEOMETRY_HOLD: finite 3D sites')
    q = [tuple(Fraction(float(v)) for v in row) for row in points]
    require(len(set(q)) == len(q), 'GEOMETRY_HOLD: duplicate spatial sites')
    raw = Delaunay(points).simplices if simplices is None else simplices
    tets, faces, volumes = [], defaultdict(list), []
    for row in raw:
        s = list(map(int, row))
        require(len(s) == 4 and len(set(s)) == 4 and all(0 <= i < len(q) for i in s), 'GEOMETRY_HOLD: invalid simplex')
        v = orient(*(q[i] for i in s))
        require(v != 0, 'GEOMETRY_HOLD: degenerate simplex')
        if v < 0:
            s[0], s[1] = s[1], s[0]
            v = -v
        tets.append(tuple(s)); volumes.append(v/6)
        for j in range(4):
            face = s[:j]+s[j+1:]
            faces[tuple(sorted(face))].append(((-1)**j*parity(face), s[j]))
    require(len({tuple(sorted(s)) for s in tets}) == len(tets), 'GEOMETRY_HOLD: duplicate tetrahedra')
    require(set(i for s in tets for i in s) == set(range(len(q))), 'GEOMETRY_HOLD: unused sites')
    boundary = []
    for face, entries in faces.items():
        if len(entries) == 2:
            require(entries[0][0]+entries[1][0] == 0, 'GEOMETRY_HOLD: orientation mismatch')
        else:
            require(len(entries) == 1, 'GEOMETRY_HOLD: nonmanifold face')
            sign, opposite = entries[0]
            a,b,c = (q[i] for i in face)
            inward = orient(a,b,c,q[opposite])
            require(inward != 0, 'GEOMETRY_HOLD: boundary orientation')
            for j,p in enumerate(q):
                if j not in face:
                    require(orient(a,b,c,p)*inward > 0, 'GEOMETRY_HOLD: boundary not strictly supporting')
            boundary.append(face)
    require(bool(boundary), 'GEOMETRY_HOLD: empty boundary')
    edges = defaultdict(int)
    for f in boundary:
        for e in combinations(f,2): edges[e] += 1
    require(all(v == 2 for v in edges.values()), 'GEOMETRY_HOLD: boundary edge incidence')
    vertices = set(i for f in boundary for i in f)
    require(len(vertices)-len(edges)+len(boundary) == 2, 'GEOMETRY_HOLD: boundary Euler characteristic')
    adjacency = {i:set() for i in vertices}
    for a,b in edges: adjacency[a].add(b); adjacency[b].add(a)
    reached = set(); stack = [next(iter(vertices))]
    while stack:
        v = stack.pop()
        if v not in reached: reached.add(v); stack.extend(adjacency[v]-reached)
    require(reached == vertices, 'GEOMETRY_HOLD: disconnected boundary')
    return {'points':points, 'rational_points':q, 'tetrahedra':tets,
            'volumes':volumes, 'boundary':boundary}


def ball_fraction(x):
    return arb(x.numerator)/x.denominator


def ball_covered(mesh, radius=Fraction(1,2)):
    """Exact certificate B_radius(0) is inside the convex projection domain."""
    q=mesh['rational_points']; origin=(Fraction(0),)*3
    for face in mesh['boundary']:
        a,b,c=(q[i] for i in face)
        u=[b[k]-a[k] for k in range(3)];v=[c[k]-a[k] for k in range(3)]
        n=[u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0]]
        offset=sum(n[k]*a[k] for k in range(3)); n2=sum(z*z for z in n)
        other=next(i for i in range(len(q)) if i not in face)
        if orient(a,b,c,origin)*orient(a,b,c,q[other]) <= 0 or offset*offset < radius*radius*n2:
            return False
    return True


def mass_matrix(mesh):
    n=len(mesh['points']); M=arb_mat(n,n)
    for s,v in zip(mesh['tetrahedra'],mesh['volumes']):
        volume=ball_fraction(v)
        for i in s:
            for j in s: M[i,j] += volume*(2 if i==j else 1)/20
    return M


def bisect(vertices, lambdas):
    # Vertices are exact dyadic Fractions, as are all midpoint descendants.
    a,b=max(combinations(range(4),2),key=lambda ij:sum((vertices[ij[0]][k]-vertices[ij[1]][k])**2 for k in range(3)))
    mid=tuple((vertices[a][k]+vertices[b][k])/2 for k in range(3))
    lm=tuple((lambdas[a][k]+lambdas[b][k])/2 for k in range(4))
    va=list(vertices);vb=list(vertices);la=list(lambdas);lb=list(lambdas)
    va[a]=mid;vb[b]=mid;la[a]=lm;lb[b]=lm
    return (va,la),(vb,lb)


def field_ranges(vertices):
    """Enclose all five unchanged, amplitude-normalized fields on a tetrahedron."""
    zlo=min(v[2] for v in vertices);zhi=max(v[2] for v in vertices)
    z=ball_fraction(zlo).union(ball_fraction(zhi))
    waves=[acb(0,k*z).exp() for k in (0,2,4,8)]
    lo=[]
    for k in range(3):
        a=min(v[k] for v in vertices);b=max(v[k] for v in vertices)
        lo.append(Fraction(0) if a<=0<=b else min(a*a,b*b))
    rlo=sum(lo);rhi=max(sum(x*x for x in v) for v in vertices)
    if rlo >= Fraction(1,4):
        bump=acb(0)
    else:
        upper=(1-1/(1-4*ball_fraction(rlo))).exp()
        lower=arb(0) if rhi>=Fraction(1,4) else (1-1/(1-4*ball_fraction(rhi))).exp()
        envelope=lower.union(upper)
        bump=envelope*acb(0,4*z).exp()
    return waves+[bump]


def wave_simplex_load(vertices,volume,k,degree=80):
    """Analytic exponential moments; real-axis Taylor remainder, no sampling.

Weighted barycentrics have Dirichlet(2,1,1,1) moments. Complete homogeneous
polynomials use the four z-knots, with the weighted vertex repeated.
"""
    require(isinstance(degree,int) and degree>=0,'Taylor degree')
    z=[v[2] for v in vertices];center=(min(z)+max(z))/2
    knots=[ball_fraction(t-center) for t in z]
    halfwidth=ball_fraction((max(z)-min(z))/2)
    phase=acb(0,k*ball_fraction(center)).exp();out=[]
    tail=ball_fraction(volume)/4*(abs(k)*halfwidth)**(degree+1)/math.factorial(degree+1)
    for i in range(4):
        h=[arb(1)]+[arb(0)]*degree
        for knot in knots+[knots[i]]:
            for n in range(1,degree+1):h[n]+=knot*h[n-1]
        term=acb(1);value=acb(1)
        for n in range(1,degree+1):
            term*=acb(0,k)/(n+4)
            value+=term*h[n]
        er=arb(0,tail.upper())
        out.append(ball_fraction(volume)/4*phase*value+acb(er,er))
    return out


def wave_load(mesh,degree=80):
    B=[[acb(0) for _ in range(4)] for _ in mesh['points']]
    for s,v in zip(mesh['tetrahedra'],mesh['volumes']):
        vertices=[mesh['rational_points'][i] for i in s]
        for f,k in enumerate((0,2,4,8)):
            vals=wave_simplex_load(vertices,v,k,degree)
            for j,i in enumerate(s):B[i][f]+=vals[j]
    return B


def integrate_load(mesh, depth, waves=None):
    """Certified tetrahedral enclosure, not an empirical quadrature estimate.

On each sub-tetrahedron, integral(w_i) is exactly vol*mean(vertex w_i).
Multiplication by a range enclosure of f contains integral(w_i*f), w_i>=0.
"""
    require(isinstance(depth,int) and depth>=0, 'invalid subdivision depth')
    n=len(mesh['points'])
    waves=wave_load(mesh) if waves is None else waves
    B=[list(row)+[acb(0)] for row in waves]
    leaves=0
    unit=[tuple(Fraction(int(i==j)) for j in range(4)) for i in range(4)]
    for s,volume in zip(mesh['tetrahedra'],mesh['volumes']):
        stack=[([mesh['rational_points'][i] for i in s],unit,0)]
        while stack:
            v,l,d=stack.pop()
            if d<depth:
                for vv,ll in bisect(v,l):stack.append((vv,ll,d+1))
                continue
            leaves+=1;value=field_ranges(v)[4]
            for j,global_j in enumerate(s):
                weight=ball_fraction(volume*sum(row[j] for row in l)/(4*2**depth))
                B[global_j][4] += weight*value
    return B,leaves


def project(M,B):
    require(len(B)==M.nrows() and len(B)>0 and all(len(r)==len(B[0]) for r in B), 'load shape')
    rhs=arb_mat([[a for z in row for a in (z.real,z.imag)] for row in B])
    C=M.solve(rhs)
    require(all(C[i,j].is_finite() for i in range(C.nrows()) for j in range(C.ncols())), 'NUMERIC_HOLD: projection solve')
    return [[acb(C[i,2*j],C[i,2*j+1]) for j in range(len(B[0]))] for i in range(len(B))]


def history_polynomial(tau, f_coefficients, g_coefficients):
    """P applied to finite original Cauchy jets L^r f,L^r g, L=1-Delta.

Do not apply L repeatedly to piecewise-linear reconstructed fields.
"""
    require(len(f_coefficients)==len(g_coefficients)>0, 'equal nonempty jet orders')
    tau=arb(tau)
    return sum((-1)**r*(tau**(2*r)*f/math.factorial(2*r)+tau**(2*r+1)*g/math.factorial(2*r+1))
               for r,(f,g) in enumerate(zip(f_coefficients,g_coefficients)))


def temporal_remainder(tau,p,norm_f,norm_g):
    """||L^(p+2) f||_2 and ||L^(p+2) g||_2 are supplied proven bounds."""
    require(isinstance(p,int) and p>=0 and norm_f>=0 and norm_g>=0, 'remainder inputs')
    t=abs(arb(tau))
    return (t**(2*p+2)*norm_f/math.factorial(2*p+2)+t**(2*p+3)*norm_g/math.factorial(2*p+3))/(8*arb.pi()).sqrt()


def transfer_bound(T,errors):
    require(len(T)==len(errors), 'transfer dimensions')
    require(all(e>=0 for e in errors), 'nonnegative error bounds')
    return sum(t.abs_upper()*e for t,e in zip(T,errors))


def l2_residual_squared(norm_squared,B,C,field):
    energy=sum(B[i][field].conjugate()*C[i][field] for i in range(len(B)))
    require(energy.imag.contains(0),'real projected energy')
    e=norm_squared-energy.real
    require(e.upper()>=0,'negative projection residual')
    return max(arb(0),e.lower()).union(max(arb(0),e.upper()))


def gram_min_eigenvalue_bound(M):
    inv=M.inv()
    invnorm=max(sum(inv[i,j].abs_upper() for j in range(inv.ncols())).upper() for i in range(inv.nrows()))
    return (1/invnorm).lower(),inv


def finite_retarded_bound(K,history_error,residual_error):
    """Exact finite triangular propagation; no asymptotic stability claim."""
    nh=len(history_error);n=len(K)
    require(nh<=n and all(v>=0 for v in history_error),'history error inputs')
    require(len(residual_error)==n-nh and all(len(r)==n for r in K),'triangular dimensions')
    require(all(K[i][j]==0 for i in range(n) for j in range(i,n)),'strict retardation')
    e=list(history_error)
    for i in range(nh,n):
        require(residual_error[i-nh]>=0,'nonnegative residual bound')
        e.append(sum(abs(K[i][j])*e[j] for j in range(i))+residual_error[i-nh])
    return e
