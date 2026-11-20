"""Check the projection catalogue twice and validate both rational certificates offline."""
from collections import Counter
from fractions import Fraction as F
from itertools import permutations
import json
from extension import HERE, MASK, SEVEN, relations, load_inputs, marked_three, build_columns

def deletion_catalogue(by_code, cat):
    # Reverse enumeration, starting at every approved canonical seven-point end.
    # Fix the original labelled triple and forget the ordering of the remaining four.
    outputs=set()
    for key,ranks in cat['ranks_pure_free_mixed'].items():
        if ranks[0] or ranks[2]:
            continue
        edges=[e for i,e in enumerate(SEVEN) if int(key)&(1<<i)]
        for root in permutations(range(7),3):
            root_edges={(root.index(a),root.index(b)) for a,b in edges if a in root and b in root}
            if root_edges!={(0,2)}:
                continue
            extras=tuple(k for k in range(7) if k not in root)
            projections=[]
            for deleted in extras:
                order=root+tuple(k for k in extras if k!=deleted)
                pos={v:i for i,v in enumerate(order)}
                code=sum(1<<(6*pos[a]+pos[b]) for a,b in edges if deleted not in (a,b))
                if code not in by_code:
                    break
                projections.append(by_code[code])
            if len(projections)==4:
                outputs.add(tuple(sorted(projections)))
    return outputs

def marginals(reps, law):
    parent=Counter()
    local=Counter()
    for s,(end,orbit) in reps.items():
        for raw in orbit:
            share=law[s]/len(orbit)
            parent[raw&MASK]+=share
            if raw&MASK==1564:
                local[end]+=share
    return parent,local

def verify():
    d,res,w,cat=load_inputs()
    reps,by_code,parents,targets=marked_three(d,res,w)
    cols=build_columns(reps,by_code,cat)
    assert set(cols)==deletion_catalogue(by_code,cat)
    proof=json.loads((HERE/'proof.json').read_text())
    local_proof=json.loads((HERE/'local_proof.json').read_text())
    assert set(targets)==set(proof)==set(local_proof)
    out={}
    for t,b in targets.items():
        cert=proof[t]
        assert cert['kind']=='separating_functional'
        y={s:F(cert['values'].get(str(s),0)) for s in reps}
        least=min(sum(y[s] for s in c)/4 for c in cols)
        coarse=sum(y[s]*b[s] for s in reps)
        assert coarse<0<=least

        alt=local_proof[t]
        assert alt['kind']=='extension'
        floor=F(alt['common_floor_per_column'])
        assert floor>0
        residual={tuple(map(int,k.split(','))):F(v) for k,v in alt['residual_column_weights'].items()}
        assert residual.keys()<=cols.keys() and min(residual.values())>=0
        law=Counter()
        for c in cols:
            for s in c:
                law[s]+=(floor+residual.get(c,0))/4
        assert set(law)==set(reps) and min(law.values())>0 and sum(law.values())==1
        # Relabel a representative fine order 24 ways, then delete the fixed last mark.
        # This reconstructs individual N14 weights without grouping by deletion orbit.
        fine_to_marked=Counter()
        for c,(_,code) in cols.items():
            edges=relations(code,7)
            share=(floor+residual.get(c,0))/24
            for extra in permutations((3,4,5,6)):
                perm=(0,1,2)+extra
                raw=sum(1<<(6*perm[i]+perm[j]) for i,j in edges if perm[i]!=6 and perm[j]!=6)
                fine_to_marked[raw]+=share
        assert set(fine_to_marked)==set(by_code)
        assert all(v==law[by_code[raw]]/len(reps[by_code[raw]][1]) for raw,v in fine_to_marked.items())
        parent,local=marginals(reps,law)
        prior_parent,prior_local=marginals(reps,b)
        assert parent==parents==prior_parent and local==prior_local
        assert len(local)==10 and local[5374]>0
        out[t]={'minimum_functional_over_fine_columns':str(least),
                'functional_on_archived_witness':str(coarse),
                'full_archived_witness_extension':'EXCLUDED_UNDER_FOUR_MARK_EXCHANGEABILITY',
                'fixed_N13_and_ten_local_N14_weights':'EXACT_POSITIVE_EXTENSION',
                'local_conditional_weights':{str(i):str(v/parents[1564]) for i,v in sorted(local.items())},
                'A_over_B':str(local[1790]/local[5374]),'common_floor_per_projection_column':str(floor),
                'positive_N14_orbits':len(law),'additional_nonzero_column_weights':len(residual)}
    assert proof['0']['values']==proof['1/1764']['values']
    y=proof['0']['values']
    assert F(y.get(str(w['A']['orbit']),'0'))==F(y.get(str(w['B']['orbit']),'0'))
    return {'shared_separator_constant_on_archived_AB_line':True,'scope':'four exchangeable insertion marks, one-edge N11 family on the finite scalar-admissible N15 support',
            'published_scalar_admissible_N15_types':cat['counts']['good'],'marked_N13_prefixes':len(parents),
            'N14_orbits':len(reps),'N14_marked_paths_checked_individually':len(by_code),'distinct_N15_projection_columns':len(cols),
            'forward_reverse_columns_equal':True,'witnesses':out}
if __name__=='__main__':
    if not __debug__: raise SystemExit('Use Python without -O.')
    print(json.dumps(verify(),indent=2))
