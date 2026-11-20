"""One-event pushforward at the marked prefix, with exact scalar arithmetic."""
from itertools import combinations, product
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import json
import sys

import sympy as s

F = s.Rational
BASE = Path(__file__).resolve().parent
ARCHIVE = 'CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip'
DIGEST = '4a2b985578e9bf41662af0dede7c2054c8406de4f49d077891f505b0fffd917e'
I = (4, 5, 6, 11, 12, 13)
PAST, FUTURE = tuple(range(4)), tuple(range(7,11))


def geometry_for(code, n):
    inn = I[:n]
    nodes = list(range(8+n))
    relations = set(combinations(PAST,2)) | set(combinations(FUTURE,2))
    relations.update(product(PAST, inn+FUTURE))
    relations.update(product(inn,FUTURE))
    relations.update((inn[i],inn[j]) for i in range(n) for j in range(n) if code & (1 << (6*i+j)))
    assert all((a,d) in relations for a,b in relations for c,d in relations if b==c)
    b = {}
    for i,j in sorted(relations):
        size = sum((i,k) in relations and (k,j) in relations for k in nodes)
        b[i,j] = (1,-9,16,-8)[size] if size < 4 else 0
    H = s.zeros(len(nodes))
    for (i,j),v in b.items():
        w = F(v,2)
        H[i,i] -= w
        H[j,j] -= w
        H[i,j] += w
        H[j,i] += w
    return H, b, len(nodes)-sum(b.values())


def collar(H, g):
    n = H.rows
    E = s.zeros(n)
    E[1:4,:3] = s.eye(3)
    E[7:10,3:6] = s.eye(3)
    E[:4,-2], E[7:11,-1] = g.BM, g.BP
    for col,node in enumerate(I[:n-8]):
        E[node,6+col] = 1
    G = E.T*H*E
    G[-2,:3] -= g.AM[1:4,:].T
    G[:3,-2] -= g.AM[1:4,:]
    G[-1,3:6] += g.AP[:3,:].T
    G[3:6,-1] += g.AP[:3,:]
    G[-2,-2] -= g.AM.dot(g.BM)
    G[-1,-1] += g.AP.dot(g.BP)
    return G


def eliminate(matrix, indices):
    keep = [k for k in range(matrix.rows) if k not in indices]
    pivot = matrix[indices,indices]
    cross = matrix[keep,indices]
    return matrix[keep,keep] - cross*pivot.inv()*cross.T


def sparse_upper(matrix):
    return [[i,j,str(matrix[i,j])] for i in range(matrix.rows) for j in range(i,matrix.cols) if matrix[i,j]]


def scalar_data(H, g):
    G = collar(H,g)
    V = G[6:,6:]
    K = eliminate(G,list(range(6,G.rows)))
    det_v, det_xy = V.det(), K[:3,3:].det()
    assert det_v and det_xy
    omega = K[:3,3:].T*(s.eye(3)-s.I*K[:3,:3]).inv()*K[:3,3:] - s.I*K[3:,3:]
    return G, K, V, abs(det_v*det_xy), omega.applyfunc(s.cancel)


def factorize(H, Hp, g, K, V):
    h, u = H[-1,-1], H[:-1,-1]
    info = {'h':str(h), 'u':list(map(str,u))}
    full = collar(H,g)
    mark = 11  # chart indices 6..11 are the six old/new inner variables
    assert full[mark,mark] == h
    if h:
        Heff = H[:-1,:-1] - u*u.T/h
        D = Heff-Hp
        info.update(kind='Fresnel', correction_upper=sparse_upper(D), rank=D.rank())
        reduced = eliminate(full,[mark])
        assert reduced == collar(Heff,g)
        leading_det, leading_signature = h, int(s.sign(h))
    else:
        # After integrating q13 the remaining amplitude is a Fourier delta.
        k = next(node for node in I[:-1] if u[node])
        pivot = 6+I.index(k)
        keep = [i for i in range(full.rows) if i not in (mark,pivot)]
        # Substitute q_k from the linear delta into the quadratic old action.
        E = s.zeros(full.rows,len(keep))
        for j,i in enumerate(keep):
            E[i,j] = 1
            E[pivot,j] = -full[mark,i]/full[mark,pivot]
        reduced = E.T*full*E
        assert reduced == eliminate(full,[mark,pivot])
        info.update(kind='Fourier delta', solve_old_field=k, inverse_abs_jacobian=str(1/abs(u[k])),
                    old_old_correction_upper=sparse_upper(H[:-1,:-1]-Hp))
        leading_det, leading_signature = -u[k]**2, 0
        D = None
    Vr = reduced[6:,6:]
    assert eliminate(reduced,list(range(6,reduced.rows))) == K
    assert leading_det*Vr.det() == V.det()
    assert leading_signature + g.inertia(Vr) == g.inertia(V)
    return info, D


def run(original):
    sys.path.insert(0,str(original))
    from prefix import row
    import scalar
    from clock_check import check_clocks
    g = scalar.geometry
    archived = json.loads((original/'result.json').read_text())
    Hp, bp, gp = geometry_for(1564,5)
    _, _, _, parent_scale, omega_p = scalar_data(Hp,g)
    by_end = {62:omega_p}
    path_rows, diffs = [], []
    singular_normals, singular_moments = [], []
    cases,_ = row()
    for end,code,_ in cases:
        H,b,gravity = geometry_for(code,6)
        _,K,V,scale,omega = scalar_data(H,g)
        assert omega == scalar.rate((6,end))
        assert gravity == archived['F4_parent_and_daughters'][f'14_{end}']
        if end in by_end:
            assert omega == by_end[end]
        by_end[end] = omega
        record, D = factorize(H,Hp,g,K,V)
        if D is not None:
            diffs.append(D)
        else:
            singular_normals.append(H[:-1,-1].T)
            # At zero density on all five old inner events, only future collars
            # contribute retained-dust s-dependence. Isolate the s=0 phase.
            S = sum(b.get((13,k),0) for k in FUTURE)
            L = sum((k-5)*b.get((13,k),0) for k in FUTURE)
            angle_bound = F(5,96)*(abs(S)*F(9,4) + abs(L))
            singular_moments.append({'code':code,'sum_future_b':S,'sum_future_index_b':L,
                                     'absolute_phase_deviation_upper':str(angle_bound),
                                     'rotated_real_dust_influence_lower':str(F(1,3)-angle_bound)})
            assert angle_bound <= F(85,384) and F(1,3)-angle_bound >= F(43,384)

        changes = [[i,j,b.get((i,j),0)-bp.get((i,j),0)] for i,j in sorted(set(b)|set(bp))
                   if b.get((i,j),0)!=bp.get((i,j),0)]
        path_rows.append(dict(end=end,code=code,delta_F4=gravity-gp,delta_interval_weights=changes,
                              scalar=record, abs_detV_detKxy=str(scale),
                              det_ratio_to_parent=str(scale/parent_scale),
                              sgn_V=g.inertia(V), det_V=str(V.det()), det_Kxy=str(K[:3,3:].det())))
    assert omega_p == scalar.rate((5,62))
    regular_differences = s.Matrix.vstack(*diffs)
    assert regular_differences.nullspace() == [s.ones(13,1)]
    assert (len(path_rows),len(diffs)) == (16,14)
    assert s.Matrix.vstack(*singular_normals).rank() == 2
    assert set(entry['end'] for entry in path_rows if entry['scalar']['kind']=='Fourier delta') == {926}
    # A cone of positive solid angle keeps all eleven Gaussian decay rates ordered.
    real_forms = {k:v.applyfunc(s.re) for k,v in by_end.items()}
    rates = {k:R[0,0] for k,R in real_forms.items()}
    for k,value in rates.items():
        tag = '13_62' if k==62 else f'14_{k}'
        assert value == F(archived['exact_gaussian_rates_axis_one'][tag][0])
    ordered = sorted(rates,key=rates.get)
    gap = min(rates[b]-rates[a] for a,b in zip(ordered,ordered[1:]))
    largest = max(abs(x) for form in real_forms.values() for x in form)
    halfwidth = F(1,2)
    while 2*(4*halfwidth+4*halfwidth**2)*largest >= gap:
        halfwidth /= 2
    cone = {'rates_ascending':[[k,str(rates[k])] for k in ordered],
            'minimum_gap':str(gap), 'max_matrix_entry':str(largest),
            'halfwidth_y2_y3_over_y1':str(halfwidth)}
    clocks = check_clocks(cases,geometry_for,scalar)
    return dict(prefix=1564, independent_bare_parent_F4=gp, parent_abs_detV_detKxy=str(parent_scale),
                branches=path_rows, singular_dust_certificate=singular_moments, common_nullity_of_regular_corrections=1,
                common_null_vector=[1]*13, scalar_tail_cone=cone, dust_clock_checks=clocks,
                continuous_pushforward='derived branchwise on the declared field and collar measures',
                physical_discrete_sum='underdetermined', stage_6='HOLD', P3='HOLD')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run without -O to keep exact checks enabled')
    zpath = BASE/ARCHIVE
    if sha256(zpath.read_bytes()).hexdigest()!=DIGEST:
        raise ValueError('Upstream archive digest mismatch')
    with TemporaryDirectory() as tmp:
        with ZipFile(zpath) as z:
            z.extractall(tmp)
        result = run(Path(tmp)/'prefix_1564_selection_v0_1')
    output = json.dumps(result,indent=2,ensure_ascii=False,allow_nan=False)+'\n'
    if len(sys.argv) == 2:
        Path(sys.argv[1]).write_text(output)
    else:
        print(output,end='')
