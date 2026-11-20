"""Rank, composition and domain tests for the two marked-field eliminations."""
from collections import Counter
from contextlib import contextmanager
from hashlib import sha256
from io import BytesIO
from itertools import combinations, product
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import sys

import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent
OLD = (4, 5, 6, 11, 12)
INNER = OLD + (13, 14)
PAST, FUTURE = tuple(range(4)), tuple(range(7,11))
ARCHIVE = "CST_DUST_Randabbildung_1564_v0_1_Pruefpaket.zip"
EXPECTED = {
    "design.json": "79fdf60b0a962172fe579234de3ce85a48a37f32475eccd23835d9b021181417",
    "inputs/catalog.json": "394f438f7041f5d87db34cbdd162c2eeb5ad71841fb2f965bdd9cd67aa02051a",
    "inputs/"+ARCHIVE: "ab2204236c27e8b804849d78889823927110e8fb41dabde3b8ab8e31018c325f",
}


@contextmanager
def upstream():
    for name, expected in EXPECTED.items():
        assert sha256((HERE/name).read_bytes()).hexdigest() == expected, name
    with TemporaryDirectory() as tmp, ZipFile(HERE/"inputs"/ARCHIVE) as study:
        parent_name, = [name for name in study.namelist() if name.endswith(".zip")]
        with ZipFile(BytesIO(study.read(parent_name))) as original:
            directory = Path(tmp)
            for name in ["geometry.py","contract.json"]:
                src, = [x for x in original.namelist() if x.endswith("/inputs/"+name)]
                (directory/name).write_bytes(original.read(src))
            (directory/"boundary.py").write_bytes(study.read("boundary.py"))
            sys.path.insert(0,tmp)
            try:
                import boundary
                import geometry
                boundary.I = INNER  # Extend the inherited collar chart by one identity column.
                yield json.loads(study.read("result.json")), boundary, geometry
            finally:
                sys.path.remove(tmp)


def edges6(code):
    return {(i,j) for i in range(6) for j in range(6) if code & 1 << (6*i+j)}


def transitive(edges):
    return all((i,k) in edges for i,j in edges for h,k in edges if h==j)


def natural7(edges):
    """Minimum upper-triangular bit mask over all topological orders."""
    bits = {pair:1<<i for i,pair in enumerate(combinations(range(7),2))}
    pred = [{i for i,j in edges if j==k} for k in range(7)]
    def masks(order,remaining):
        if not remaining:
            pos = {node:i for i,node in enumerate(order)}
            yield sum(bits[pos[i],pos[j]] for i,j in edges)
        for v in sorted(remaining):
            if not pred[v] & remaining:
                yield from masks(order+(v,),remaining-{v})
    return min(masks((),set(range(7))))


def full_geometry(internal):
    relations = set(combinations(PAST,2)) | set(combinations(FUTURE,2))
    relations.update(product(PAST,INNER+FUTURE))
    relations.update(product(INNER,FUTURE))
    relations.update((INNER[i],INNER[j]) for i,j in internal)
    assert transitive(relations)
    H = s.zeros(15)
    b = {}
    for i,j in sorted(relations):
        length = sum((i,k) in relations and (k,j) in relations for k in range(15))
        w = (1,-9,16,-8)[length] if length<4 else 0
        b[i,j] = w
        a = s.Rational(w,2)
        H[i,i] -= a
        H[j,j] -= a
        H[i,j] += a
        H[j,i] += a
    return H,b,15-sum(b.values())


def candidates(prior, boundary, geom):
    catalog = json.loads((HERE/"inputs/catalog.json").read_text())
    rows = sorted((row["end"],row["code"]) for row in prior["branches"])
    assert len(rows)==16 and prior["prefix"]==1564
    counts = Counter()
    keep = []
    for (end1,c1),(end2,c2) in combinations(rows,2):
        if end1 == end2:
            continue
        counts["distinct_type_pairs"]+=1
        e1,e2=edges6(c1),edges6(c2)
        prefix={p for p in e1 if 5 not in p}
        assert prefix == {p for p in e2 if 5 not in p} == edges6(1564)
        fine = e1 | {(6 if i==5 else i,6 if j==5 else j) for i,j in e2}
        if not transitive(fine):
            continue
        counts["transitive_incomparable"]+=1
        code=natural7(fine)
        if not all(str(code) in catalog["parents"][str(p)] for p in (end1,end2)):
            continue
        counts["both_catalog_edges"]+=1
        if catalog["ranks_pure_free_mixed"][str(code)] != [0,0,0]:
            continue
        counts["catalog_rank_admissible"]+=1
        H,_,_=full_geometry(fine)
        G=boundary.collar(H,geom)
        if not G[6:,6:].det():
            continue
        K=boundary.eliminate(G,list(range(6,15)))
        if not K[:3,3:].det():
            continue
        block=H[13:,13:]
        missing=2-len({1790,5374}&{end1,end2})
        key=(missing,code,end1,end2,c1,c2)
        keep.append((key, fine, int(block.rank()), block.det()!=0 and 0 in (block[0,0],block[1,1])))
        counts["eligible"]+=1
        counts["eligible_AB" if missing==0 else "eligible_one_AB" if missing==1 else "eligible_no_AB"]+=1
        counts["two_field_rank_"+str(block.rank())]+=1
    return counts, sorted(keep,key=lambda row:row[0])


def stepwise(H, order):
    """Integrate one scalar variable at a time, retaining Fourier constraints."""
    retained=list(range(H.rows))
    Q=H
    coeff=s.Integer(1)
    sig=0
    rows=[]
    for new in order:
        j=retained.index(new)
        keep=[k for k in range(Q.rows) if k!=j]
        h=Q[j,j]
        u=Q[keep,[j]]
        if h:
            Q=Q[keep,keep]-u*u.T/h
            coeff*=abs(h)
            sig+=int(s.sign(h))
        else:
            # On these incomparable diamonds the other new coordinate is absent.
            coords=[retained[k] for k in keep]
            assert all(u[k]==0 for k,node in enumerate(coords) if node>=13)
            rows.append((new,[u[coords.index(k)] for k in range(13)]))
            Q=Q[keep,keep]
        retained.pop(j)
    return Q,[(k,v) for k,v in sorted(rows)],coeff,sig


def scalar_check(H, boundary, geom):
    A=H[:13,:13]; U=H[:13,13:]; D=H[13:,13:]
    assert D[0,1]==D[1,0]==0
    live=[i for i in range(2) if D[i,i]]
    null=[i for i in range(2) if not D[i,i]]
    assert D.rank()==len(live)
    Q=A-(U[:,live]*D[live,live].inv()*U[:,live].T if live else s.zeros(13))
    constraints=[(i+13,list(U[:,i])) for i in null]
    coeff=s.prod(abs(D[i,i]) for i in live)
    sig=sum(int(s.sign(D[i,i])) for i in live)
    assert all(stepwise(H,order)==(Q,constraints,coeff,sig) for order in [(13,14),(14,13)])
    G=boundary.collar(H,geom)
    K=boundary.eliminate(G,list(range(6,15)));V=G[6:,6:]
    qr=boundary.collar(Q,geom)
    raw_kept=list(range(11))+[13,14]
    fine_regular=[11+i for i in live]
    if fine_regular:
        reg_reduced=boundary.eliminate(G,fine_regular)
    else:
        reg_reduced=G
    fine_keep=[i for i in range(15) if i not in fine_regular]
    keep_positions=[fine_keep.index(k) for k in raw_kept]
    assert qr==reg_reduced[keep_positions,keep_positions]
    delta=G[[11+i for i in null],raw_kept]
    assert delta.rank()==len(null)
    pivot=[6+i for i in delta[:,6:].rref()[1]]
    assert len(pivot)==len(null)
    jac=abs(delta[:,pivot].det()) if null else s.Integer(1)
    stay=[k for k in range(13) if k not in pivot]
    E=s.zeros(13,len(stay))
    for j,k in enumerate(stay):
        E[k,j]=1
    if pivot:
        replacement=-delta[:,pivot].inv()*delta[:,stay]
        for i,k in enumerate(pivot):
            E[k,:]=replacement[i,:]
        assert delta*E==s.zeros(len(null),E.cols)
    quotient=E.T*qr*E
    vsmall=quotient[6:,6:]
    ksmall=boundary.eliminate(quotient,list(range(6,quotient.rows)))
    signed_det=s.prod(D[i,i] for i in live)*(-1)**len(null)*jac**2
    assert ksmall==K and signed_det*vsmall.det()==V.det()
    assert sig+geom.inertia(vsmall)==geom.inertia(V)
    return dict(new_field_hessian=[[str(x) for x in D.row(i)] for i in range(2)],
                raw_delta_normals=[[str(x) for x in v] for k,v in constraints],
                raw_effective_quadratic_upper=boundary.sparse_upper(Q),
                scalar_prefactor=dict(two_pi_over_beta_exponent=str(s.Rational(len(live),2)+len(null)),
                                      inverse_sqrt_denominator=str(coeff),pi_over_four_phase_multiplier=sig),
                chart_delta_pivots=pivot,chart_delta_inverse_abs_jacobian=str(1/jac),
                det_V=str(V.det()),signature_V=geom.inertia(V),det_Kxy=str(K[:3,3:].det()),
                inherited_normalization_square_without_beta=str(abs(V.det()*K[:3,3:].det())),
                outer_K_upper=boundary.sparse_upper(K),
                raw_two_orders_and_direct_match=True,outer_kernel_determinant_and_phase_match=True)


def check_clocks(b,grav,old_geometry):
    """Identical quadrature on the two new normalized clocks; densities analytic."""
    beta=4/np.sqrt(6.)
    step=np.sqrt(2/(19*beta))
    def row(weights,j,t):
        return 1+beta/2*sum(c*(t[j]-t[i])**2 for (i,k),c in weights.items() if k==j and c)
    def dust(u):
        return (1+np.exp(-.25j*u)*np.sinc(u/(4*np.pi)))/2
    records=[]
    for n in (8,16):
        nodes,weights=np.polynomial.legendre.leggauss(n)
        weights=weights/2
        for rho,side in product((1/8,1/4),(-1,1)):
            t={k:(k-5)*step for k in (*PAST,*FUTURE)}
            t[3]=-2*step+side/16
            t.update(zip(OLD,[-.7,.4,-.1,1.15,-1.2]))
            t[13]=1.5*nodes[:,None]
            t[14]=1.5*nodes[None,:]
            fixed=dict.fromkeys(PAST,rho)
            fixed.update(dict.fromkeys(FUTURE,1/8))
            fixed.update(zip(OLD,[0.,.3,.7,0.,.5]))
            def old_phase(weights,g):
                return g-.5*sum(den*row(weights,j,t) for j,den in fixed.items())
            fine_phase=old_phase(b,grav)
            t13=dust(row(b,13,t));t14=dust(row(b,14,t))
            direct=np.sum(weights[:,None]*weights[None,:]*np.exp(1j*fine_phase)*t13*t14)
            vals=[]
            for kept, integrated in ((13,14),(14,13)):
                bi,gi=old_geometry[kept]
                assert np.array_equal(row(b,kept,t),row(bi,kept,t))
                mid_phase=old_phase(bi,gi)
                insertion=np.exp(1j*(fine_phase-mid_phase))*dust(row(b,integrated,t))
                coarse=np.exp(1j*mid_phase)*dust(row(bi,kept,t))
                if integrated==14:
                    value=weights @ ((insertion @ weights)*coarse[:,0])
                else:
                    value=(coarse[0,:]*(weights @ insertion)) @ weights
                vals.append(value)
            err=max(abs(direct-v) for v in vals)
            assert err<1e-12
            records.append(dict(n=n,initial_density="1/8" if rho==1/8 else "1/4",lobe=side,
                                direct_center=[float(direct.real),float(direct.imag)],
                                max_absolute_order_difference=float(err)))
    return records


def local_weight_check():
    """Explicit positive marked continuations projecting to each supplied coarse witness."""
    cat=json.loads((HERE/"inputs/catalog.json").read_text())
    with ZipFile(HERE/"inputs"/ARCHIVE) as outer:
        archive=next(n for n in outer.namelist() if n.endswith(".zip"))
        with ZipFile(BytesIO(outer.read(archive))) as inner:
            data=json.loads(inner.read("prefix_1564_selection_v0_1/result.json"))
    eligible={k for k,(pure,free,mix) in cat["ranks_pure_free_mixed"].items() if pure==0 and mix==0}
    assigned={}
    for code in data["conditional_weights_at_zero"]:
        multiplicities={k:w for k,w in cat["parents"][code].items() if k in eligible}
        assert multiplicities
        assigned[code]=multiplicities
    rows=[]
    for t in (s.S.Zero,s.Rational(1,1764)):
        q={k:s.Rational(v)+t*s.Rational(data["q_slope_per_unit_orbit_t"].get(k,0))
           for k,v in data["conditional_weights_at_zero"].items()}
        assert sum(q.values())==1 and min(q.values())>0
        for code,child in assigned.items():
            denom=sum(child.values())
            y=[q[code]*s.Rational(m,denom) for m in child.values()]
            assert min(y)>0 and sum(y)==q[code]
        ratio=q["1790"]/q["5374"]
        assert ratio==(1 if t==0 else s.Rational(1,3))
        rows.append(dict(t=str(t),conditional_A=str(q["1790"]),conditional_B=str(q["5374"]),
                         ratio_A_over_B=str(ratio),
                         conditional_weights={k:str(v) for k,v in q.items()}))
    return dict(witnesses=rows,positive_local_child_path_counts={k:sum(x.values()) for k,x in assigned.items()},
                construction="Each marked N14 path distributes its coefficient uniformly among its allowed labelled N15 insertion choices, pooling them by the N15 type multiplicities. No equality between different parent paths imposed.",
                extra_equation_from_fixed_fine_geometry="identically zero for every coefficient",
                rank_gained_on_nine_weight_directions=0,
                independent_physical_cross_history_pairing="not supplied",
                four_mark_exchangeability="not asserted by these local witnesses",
                normalized_weights_not_Born_probabilities=True)


def ordered_AB(prior, boundary, geom):
    """Post-selection explanatory control: transitive completion of the A/B pair."""
    rows = prior["branches"]
    A, = [r for r in rows if r["end"]==1790]
    B, = [r for r in rows if r["end"]==5374]
    merged = edges6(A["code"]) | {(6 if i==5 else i,6 if j==5 else j) for i,j in edges6(B["code"])}
    witnesses = sorted((i,j,k) for i,j in merged for h,k in merged if h==j and (i,k) not in merged)
    forced = {(i,k) for i,j,k in witnesses}
    assert forced=={(5,6)}
    fine=merged|forced
    assert transitive(fine)
    code=natural7(fine)
    cat=json.loads((HERE/"inputs/catalog.json").read_text())
    assert cat["ranks_pure_free_mixed"][str(code)]==[0,0,0]
    assert all(str(code) in cat["parents"][str(x)] for x in (1790,5374))
    H,_,g=full_geometry(fine)
    D=H[13:,13:]; U=H[:13,13:]
    Q=H[:13,:13]-U*D.inv()*U.T
    pivots={}
    for first in (13,14):
        once = boundary.eliminate(H,[first])
        second=once[-1,-1]
        pivots[str(first)] = [str(H[first,first]),str(second)]
        assert boundary.eliminate(once,[13])==Q
        assert H[first,first]*second==D.det()
        assert s.sign(H[first,first])+s.sign(second)==geom.inertia(D)
    G=boundary.collar(H,geom); V=G[6:,6:]
    K=boundary.eliminate(G,list(range(6,15)))
    qchart=boundary.collar(Q,geom)
    assert V.det()==D.det()*qchart[6:,6:].det()
    assert geom.inertia(V)==geom.inertia(D)+geom.inertia(qchart[6:,6:])
    assert K==boundary.eliminate(qchart,list(range(6,13)))
    return dict(status="post-selection scalar control only; excluded from incomparable diamonds",
                transitivity_witnesses_7_inner_indices=witnesses,forced_edge=[5,6],
                natural_N15_type=code,N14_marked_codes_A_B=[A["code"],B["code"]],
                F4_N15=g,raw_block=[[str(x) for x in row] for row in D.tolist()],
                det_D=str(D.det()),signature_D=geom.inertia(D),sequential_pivots=pivots,
                raw_two_orders_and_direct_match=True,final_K_determinant_signature_match=True)


def run():
    with upstream() as (prior,boundary,geom):
        counts,options=candidates(prior,boundary,geom)
        cases={}
        for name,which in [("primary",lambda row:True),("rank_deficient",lambda row:row[2]<2),
                           ("zero_pivot_invertible",lambda row:row[3])]:
            choice=next((row for row in options if which(row)),None)
            if choice is None:
                cases[name]=None
                continue
            (missing,code,e1,e2,c1,c2),edges,_,_=choice
            H,b,grav=full_geometry(edges)
            mids={}
            for retained,mid_code in ((13,c1),(14,c2)):
                _,bi,gi=boundary.geometry_for(mid_code,6)
                if retained==14:
                    bi={(14 if i==13 else i,14 if j==13 else j):v for (i,j),v in bi.items()}
                mids[retained]=(bi,gi)
                for k in list(range(13))+[retained]:
                    if k==retained:
                        assert all(b.get((i,k),0)==bi.get((i,k),0) for i in range(15))
            pg=prior["independent_bare_parent_F4"]
            assert all((mids[v][1]-pg)+(grav-mids[v][1])==grav-pg for v in mids)
            cases[name]=dict(N15_type=code,N14_types=[e1,e2],N14_marked_codes=[c1,c2],
                             N15_internal_edges=sorted(edges),F4_N13=pg,F4_N14=[mids[j][1] for j in (13,14)],F4_N15=grav,
                             scalar=scalar_check(H,boundary,geom),clock=check_clocks(b,grav,mids))
        return dict(study="CST-DUST N15 to N13, prefix 1564",
                    counts=dict(counts),distinct_N15_types_in_eligible_diamonds=len({key[1] for key,edges,rank,mixed in options}),
                    exact_AB_pairs_eligible=counts.get("eligible_AB",0),cases=cases,
                    weights=local_weight_check(),exploratory_ordered_AB=ordered_AB(prior,boundary,geom),stage_6="HOLD",P3="HOLD")


if __name__=="__main__":
    if not __debug__:
        raise SystemExit("Run without -O to retain domain and composition checks")
    print(json.dumps(run(),indent=2,allow_nan=False)+"\n",end="")
