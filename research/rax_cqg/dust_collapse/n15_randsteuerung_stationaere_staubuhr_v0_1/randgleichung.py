"""Clock displacements at fixed interior force. All systems use exact rationals."""
from basis import A, B, E, FUTURE, INNER, ORDER, PAST, Q, dwells, matrix, nullspace, rank, solve, unit

def study(M,D):
    weights=dict.fromkeys(ORDER,Q(1,8));weights.update(zip(INNER,[M*D*f for f in dwells([Q(k,8) for k in range(1,8)])]));K=matrix(weights)
    inner=[[K[i,j] for j in INNER] for i in INNER];assert rank(inner)==7
    modes={'inlet':PAST,'outlet':FUTURE,'both':E,'fixed_3_7':tuple(v for v in E if v not in (3,7)), 'fixed_7':tuple(v for v in E if v!=7)};out={}
    for label,cols in modes.items():
        ext=[[K[i,j] for j in cols] for i in INNER];tar=[[K[i,A],K[i,B]] for i in INNER];joint=[x+y for x,y in zip(ext,tar)]
        obstructions=nullspace(list(zip(*ext)));conditions=[[sum(n*x[j] for n,x in zip(v,tar)) for j in range(2)] for v in obstructions];constraints=[r for r in conditions if any(r)];d=2-(rank(constraints) if constraints else 0)
        assert d==2+rank(ext)-rank(joint)
        control={name:solve(ext,[-row[j] for row in tar]) for j,name in enumerate(('A','B'))}
        targets=nullspace(constraints) if constraints else [[1,0],[0,1]]
        for a,b in targets:assert solve(ext,[-(a*x+b*y) for x,y in tar]) is not None
        out[label]={'ports':cols,'rank':rank(ext),'accessible_target_dimension':d,'accessible_combinations':targets,'unit_controls':control,
                    'witnesses':[{'left':v,'target_coefficients':c} for v,c in zip(obstructions,conditions) if any(c)]}
    return {'inner_rank':7,'modes':out}

def robust():
    # A universal controller depending only on exterior data would survive separate variations of w12 and w13 at fixed exterior inputs.
    # Their active predecessors are all interior, so every exterior clock column of these two density derivatives vanishes.
    rows=[]
    for j,i in ((12,11),(13,12)):
        u=unit(j);k=matrix(u);assert all(k[n,e]==0 for n in INNER for e in E)
        rows.append([k[i,A],k[i,B]])
    assert rank(rows)==2
    return {'density_and_equation':[[12,11],[13,12]],'target_matrix':rows,'rank':2}

def run():return {'references':{f'{m}|{d}':study(m,d) for m in (Q(1,4),Q(1),Q(4)) for d in (Q(15,16),Q(17,16))},'common_control':robust()}
if __name__=='__main__':
    import json
    print(json.dumps(run(),default=str,indent=2,sort_keys=True))
