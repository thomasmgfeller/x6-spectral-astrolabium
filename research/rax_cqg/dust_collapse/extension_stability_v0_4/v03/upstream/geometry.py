"""Exact scalar rigging and phase of each branch, in PR 293 boundary coordinates."""
import json
from pathlib import Path
import itertools
import sympy as s
import mpmath as mp

ROOT = Path(__file__).resolve().parent
CONTRACT = json.loads((ROOT / "contract.json").read_text())
P, F = tuple(range(4)), tuple(range(7, 11))
AM = s.Matrix([-128,241,119,-232]); BM = s.Matrix([-46,-32,-16,0])
AP = s.Matrix([-232,119,241,-128]); BP = s.Matrix([0,16,32,46])


def order(name):
    inner = (4,5,6,11) if name.endswith("_lift") else (4,5,6)
    edges = set(itertools.combinations(P,2)) | set(itertools.combinations(F,2))
    edges.update(itertools.product(P,inner+F))
    edges.update(itertools.product(inner,F))
    edges.update(map(tuple,CONTRACT["interior"][name.removesuffix("_lift")]))
    assert all((a,d) in edges for a,b in edges for c,d in edges if b == c)
    weights = {}
    for a,b in sorted(edges):
        size = sum((a,k) in edges and (k,b) in edges for k in P+inner+F)
        weights[a,b] = (1,-9,16,-8)[size] if size<4 else 0
    return inner, weights, len(P+inner+F)-sum(weights.values())


def symplectic(n):
    return s.zeros(n).row_join(s.eye(n)).col_join((-s.eye(n)).row_join(s.zeros(n)))


def inertia(H):
    """Signature by exact congruence, including a zero-diagonal 2x2 pivot."""
    if not H.rows: return 0
    for i in range(H.rows):
        if H[i,i]:
            rest=[j for j in range(H.rows) if j!=i]
            return int(s.sign(H[i,i])) + inertia(H[rest,rest]-H[rest,[i]]*H[[i],rest]/H[i,i])
    for i in range(H.rows):
        for j in range(i):
            if H[i,j]:
                rest=[k for k in range(H.rows) if k not in (i,j)]
                return inertia(H[rest,rest]-H[rest,[i,j]]*H[[i,j],[i,j]].inv()*H[[i,j],rest])
    return 0


def numeric(A):
    return mp.matrix([[mp.mpc(str(s.re(z).evalf(65)),str(s.im(z).evalf(65))) for z in row]
                      for row in A.tolist()])


def kernel(name, divide_bulk_volume=False):
    inner, b, F4 = order(name)
    n=len(inner)
    H=s.zeros(8+n)
    for (i,j),w in b.items():
        h=s.Rational(w,2)
        H[i,i]-=h; H[j,j]-=h; H[i,j]+=h; H[j,i]+=h
    # Coordinates (x[3],y[3],q_I[n],t_minus,t_plus).
    E=s.zeros(8+n,8+n)
    E[1:4,:3]=s.eye(3); E[7:10,3:6]=s.eye(3)
    for j,node in enumerate(inner): E[node,6+j]=1
    E[:4,-2]=BM; E[7:11,-1]=BP
    G=E.T*H*E
    # Section chirps +f_plus - f_minus.
    G[-2,:3]-=AM[1:4,:].T; G[:3,-2]-=AM[1:4,:]
    G[-1,3:6]+=AP[:3,:].T; G[3:6,-1]+=AP[:3,:]
    G[-2,-2]-=AM.dot(BM); G[-1,-1]+=AP.dot(BP)
    V=G[6:,6:]; link=G[:6,6:]
    piv=list(V.rref()[1]); reg=V[piv,piv]
    K=G[:6,:6]-link[:,piv]*reg.inv()*link[:,piv].T if piv else G[:6,:6]
    null=V.nullspace()
    Z=s.Matrix.hstack(*null) if null else s.zeros(V.rows,0)
    raw=(link*Z).T
    rows=list(raw.T.rref()[1]); L=raw[rows,:] if rows else s.zeros(0,6)
    free=G[:,6:].nullspace()
    freeM=s.Matrix.hstack(*free) if free else s.zeros(V.rows,0)
    external_gauge_rank=freeM[-2:,:].rank()
    lx,ly=L[:,:3],L[:,3:]
    M=K[:3,3:].row_join(lx.T).col_join(ly.row_join(s.zeros(L.rows)))
    result=dict(inner=list(inner),F4=F4,bulk_gauge_signature=inertia(reg),integration_rank=reg.rows,
                free_directions=len(free),external_gauge_rank=external_gauge_rank,
                delta_constraints=L.rows,delta_rows=[[str(z) for z in row] for row in L.tolist()],
                legendre_rank=M.rank(),legendre_size=M.rows)
    reasons=[]
    result["pure_bulk_null_vectors"] = [[str(z) for z in vec] for vec in G[:,6:6+n].nullspace()]
    result["reduced_mixed_null_vectors"] = [[str(z) for z in vec] for vec in M.nullspace()]
    if len(free)!=external_gauge_rank and not divide_bulk_volume: reasons.append("independent pure bulk zero mode with no inherited quotient")
    if M.rank()!=M.rows: reasons.append("reduced mixed Legendre system is singular")
    if reasons:
        result.update(status="OBSTRUCTION",reasons=reasons)
        return result,None
    rhs=(-K[:3,:3]).row_join(-s.eye(3)).col_join((-lx).row_join(s.zeros(L.rows,3)))
    sol=M.inv()*rhs
    phase_map=sol[:3,:].col_join(K[3:,:3].row_join(s.zeros(3))+K[3:,3:]*sol[:3,:]+ly.T*sol[3:,:])
    J=symplectic(3)
    assert phase_map.T*J*phase_map==J and phase_map*J*phase_map.T==J
    # Impose the independent Fourier deltas by solving for input components.
    pivx=list(lx.rref()[1]); others=[j for j in range(3) if j not in pivx]
    k=len(others); S=s.zeros(6,k+3)
    S[3:,k:]=s.eye(3)
    for j,idx in enumerate(others): S[idx,j]=1
    if pivx:
        sub=-lx[:,pivx].inv()*(lx*S[:3,:]+ly*S[3:,:])
        for j,idx in enumerate(pivx): S[idx,:]=sub[j,:]
    assert L*S==s.zeros(L.rows,k+3)
    Q=S.T*(s.diag(1,1,1,0,0,0)-s.I*K)*S
    T=Q[:k,:k]
    Om=Q[k:,k:]-(Q[k:,:k]*T.inv()*Q[:k,k:] if k else s.zeros(3))
    Om=Om.applyfunc(s.cancel)
    expected=-s.I*(phase_map[3:,:3]+s.I*phase_map[3:,3:])*(phase_map[:3,:3]+s.I*phase_map[:3,3:]).inv()
    assert (Om-expected).applyfunc(s.cancel)==s.zeros(3)
    assert Om.applyfunc(s.re).is_positive_definite
    angle=mp.pi*result["bulk_gauge_signature"]/4
    if k:
        A=numeric(T.applyfunc(s.re)).apply(mp.re)
        B=numeric(T.applyfunc(s.im)).apply(mp.re)
        C=mp.cholesky(A)**-1
        eigenvalues,_=mp.eigsy(C*B*C.T)
        angle-=sum(mp.atan(v) for v in eigenvalues)/2
    beta=4/mp.sqrt(6)
    precision=beta*numeric(Om)
    factor=mp.power(mp.det(precision.apply(mp.re))/mp.pi**3,mp.mpf("0.25"))*mp.exp(1j*angle)
    result.update(status="ADMISSIBLE",symplectic_both_directions=True,gaussian_phase_radians=float(angle))
    return result,(precision,factor)


def continued_sqrt(A):
    A=mp.matrix(A); root=mp.mpc(1)
    for j in range(A.rows):
        pivot=A[j,j]
        assert mp.re(pivot)>0
        root*=mp.sqrt(pivot)
        for k in range(j+1,A.rows):
            for l in range(j+1,A.cols): A[k,l]-=A[k,j]*A[j,l]/pivot
    return root


def readout(states):
    """Three accepted effects for the common noisy q7 pointer. Failure is 1 minus success."""
    import numpy as np
    names=list(states); bins=np.zeros((3,len(names),len(names)),dtype=complex)
    for i,a in enumerate(names):
        P,N=states[a]
        for j,b in enumerate(names):
            Q,M=states[b]
            T=P.conjugate()+Q
            z=N.conjugate()*M*(2*mp.pi)**mp.mpf("1.5")/continued_sqrt(T)
            u=1+(T**-1)[0,0]
            center=z*mp.erf(1/mp.sqrt(2*u))
            bins[:,i,j]=[complex((z-center)/2),complex(center),complex((z-center)/2)]
            if i==j: assert abs(z-1)<mp.mpf("1e-42")
    assert np.max(np.abs(bins-bins.swapaxes(1,2).conj()))<1e-13
    assert np.min(np.linalg.eigvalsh(bins))>-1e-13
    return bins
