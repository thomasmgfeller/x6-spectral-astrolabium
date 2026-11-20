"""Apply the archived nine global perturbations to the 16 ordered local branches."""
from collections import Counter
from fractions import Fraction as Q
import sympy as sp

def analyse(archive, measures, witness, branches, inherited):
    m=archive
    pair_law={}
    for key,v in measures['target_pair_marginal'].items():
        code=int(key)
        pair={code,m.relabel(m.decode(code),(0,1,2,4,3,5))}
        for k in pair:pair_law[k]=Q(v)/len(pair)
    cols={}
    for end in measures['fully_admissible_end_types']:
        edges=[e for k,e in enumerate(m.EDGES) if end&(1<<k)]
        for code in sorted({m.relabel(edges,p) for p in m.LABELS}):
            if code & m.MASK not in pair_law:continue
            orbit={m.relabel(m.decode(code),p) for p in m.MARKS}
            if code!=min(orbit) or not all(x&m.MASK in pair_law for x in orbit):continue
            cols[code]=(end,orbit)
    keys=list(cols)
    counts=[Counter(x&m.MASK for x in orbit) for _,orbit in cols.values()]
    M=sp.Matrix([[cnt[p] for cnt in counts] for p in sorted(pair_law)])
    B=sp.Matrix([[int(row['code'] in orbit) for _,orbit in cols.values()] for row in branches])
    codes=[r['code'] for r in branches]
    types=sorted({r['end'] for r in branches})
    J=sp.Matrix([[int(r['end']==j) for r in branches] for j in types])
    D=sp.Matrix([[int(r['code']==code) for r in branches] for code in (132668,4294968892)])
    mass=sp.Rational(pair_law[1564])
    u=Q(measures['max_uniform_labelled_path_component'])
    base=sp.Matrix([u/measures['paths_valid_in_all_six_orders']+(1-u)*Q(witness.get(str(k),0))/len(cols[k][1]) for k in keys])
    assert min(base)>0 and M*base==sp.Matrix([pair_law[p] for p in sorted(pair_law)])
    assert (D*B*base/mass)==sp.Matrix([sp.Rational(1,18)]*2)
    vectors=[]; signed={}
    for target in sorted(map(int,inherited['moves'])):
        item=inherited['moves'][str(target)]
        step=sp.Rational(item['symmetric_positive_step'])
        x=sp.Matrix([sp.Rational(item['path_deltas'].get(str(k),0)) for k in keys])
        assert step==sp.Rational(1,36) and M*x==sp.zeros(M.rows,1) and min(base-step*x)>0 and min(base+step*x)>0
        v=B*x/mass
        assert J*v==sp.Matrix([(j==target)-(j==1790) for j in types])
        signed[str(target)]={str(c):str(f) for c,f in zip(codes,v) if f}
        vectors.append(v)
    V=sp.Matrix.hstack(*vectors)
    assert V.rank()==9 and (D*V).rank()==2
    def rank(x):return x.to_DM().rank()
    fixed=M.col_join(J*B)
    joint=fixed.col_join(D*B)
    r0,rb,rd,rl=map(rank,(M,fixed,joint,M.col_join(B)))
    out={'targets':sorted(map(int,signed)),'signed_marked_coefficients':signed,'singular_amplitude_rows':[[str(x) for x in row] for row in (D*V).tolist()],
         'rank_fixed_N13':r0,'rank_with_endtypes':rb,'rank_adding_both_delta_coefficients':rd,
         'rank_with_all_16_marks':rl}
    if rd>rb:
        rhs=sp.zeros(joint.rows,1);rhs[-2]=mass;rhs[-1]=-mass
        rows=list(joint.T.to_DM().rref()[1])
        sub=joint[rows,:]; ii=list(sub.to_DM().rref()[1])
        sol=sub[:,ii].inv()*rhs[rows,:]
        assert joint[:,ii]*sol==rhs
        step=min(base[i]/abs(z) for i,z in zip(ii,sol) if z)/2
        out['invisible_endtype_move']={'global_path_deltas':{str(keys[i]):str(z) for i,z in zip(ii,sol) if z},
                                      'local_marked':{str(k):str(z) for k,z in zip(codes,B[:,ii]*sol/mass) if z},
                                      'positive_step':str(step)}
    if rl>rd:
        # A second invisible direction freezes both marked 926 weights as well.
        for pos,code in enumerate(codes):
            enlarged=joint.col_join(B[pos,:])
            if rank(enlarged)==rd:
                continue
            rhs=sp.zeros(enlarged.rows,1)
            rhs[-1]=mass
            rows=list(enlarged.T.to_DM().rref()[1])
            sub=enlarged[rows,:]
            ii=list(sub.to_DM().rref()[1])
            sol=sub[:,ii].inv()*rhs[rows,:]
            assert enlarged[:,ii]*sol==rhs
            step=min(base[i]/abs(z) for i,z in zip(ii,sol) if z)/2
            out['second_invisible_endtype_move']={'global_path_deltas':{str(keys[i]):str(z) for i,z in zip(ii,sol) if z},
                         'local_marked':{str(k):str(z) for k,z in zip(codes,B[:,ii]*sol/mass) if z},
                         'positive_step':str(step)}
            break
    assert (r0,rb,rd,rl)==(38,47,48,49)
    return out
