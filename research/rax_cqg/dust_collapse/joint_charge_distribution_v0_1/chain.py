"""Charge-blind exact chain-parent extension and obstruction certificates."""
import json
from collections import Counter,defaultdict
from fractions import Fraction as Q
from itertools import permutations
from zipfile import ZipFile
import numpy as np
import sympy as sp
from scipy.optimize import linprog
from weights import BASE
from extension import MASK, SIX, SEVEN, MARKS, relations, encode

def sparse_exact(A,b,objective):
    """HiGHS proposes a basis. Solve its equalities and check signs with fractions."""
    opt=linprog(objective,A_eq=np.array(A,float),b_eq=np.array(b,float),method='highs')
    if not opt.success: return None
    active=np.flatnonzero(opt.x>1e-10).tolist()
    S=sp.Matrix(A[:,active].tolist())
    vals=list(sp.linsolve((S,sp.Matrix(b))))[0]
    assert all(v.is_Rational and v>=0 for v in vals)
    out={j:Q(v) for j,v in zip(active,vals)}
    assert all(sum(int(A[i,j])*v for j,v in out.items())==b[i] for i in range(len(b)))
    return out
def separator(A,b):
    """Exactly check a witness y with A^T y >= 0 and b dot y < 0."""
    opt=linprog(np.array(b,float),A_ub=-A.T,b_ub=np.zeros(A.shape[1]),
                bounds=(-1,1),method='highs')
    y=[Q(float(v)).limit_denominator(1000000) for v in opt.x]
    assert min(sum(int(a)*v for a,v in zip(col,y) if a) for col in A.T)>=0
    upper=sum(v*w for v,w in zip(y,b))
    assert upper<0
    return y,upper

def run(certificate=None):
    with ZipFile(BASE/'inputs/four/CST_DUST_Praefix_1564_Selektionsgleichung_v0_1_Pruefpaket.zip') as z:
        def read(n):return json.loads(z.read('prefix_1564_selection_v0_1/inputs/'+n+'.json'))['chain']
        d=read('exchange');res=read('exchange_certificate')['residual_orbit_masses']
    parents={}
    for s,w in d['target_pair_marginal'].items():
        p=int(s);g={p,encode(relations(p,6),(0,1,2,4,3,5),6)}
        parents.update({i:Q(w)/len(g) for i in g})
    lookup={};orbits={}
    for end in d['fully_admissible_end_types']:
        E=[edge for j,edge in enumerate(SIX) if end>>j&1]
        for code in {encode(E,p,6) for p in permutations(range(6))}:
            if code in lookup or code&MASK not in parents: continue
            g={encode(relations(code,6),p,6) for p in MARKS}
            if all(x&MASK in parents for x in g):
                rep=min(g);orbits[rep]=g
                lookup.update({x:rep for x in g})
    assert len(orbits)==d['fully_admissible_orbits'] and len(lookup)==d['paths_valid_in_all_six_orders']
    u=Q(d['max_uniform_labelled_path_component'])
    parent14={s:u*len(g)/len(lookup)+(1-u)*Q(res.get(str(s),0)) for s,g in orbits.items()}
    cats=json.loads((BASE/'inputs/four/catalog.json').read_text())['ranks_pure_free_mixed']
    cols=defaultdict(lambda:defaultdict(set))
    for si,(a,_,b) in cats.items():
        if a or b: continue
        k=int(si);E=[edge for j,edge in enumerate(SEVEN) if k>>j&1]
        for root in permutations(range(7),3):
            a,b,c=root
            if any(e not in E for e in ((a,b),(a,c),(b,c))):continue
            extra=tuple(v for v in range(7) if v not in root)
            deleted=[]
            for j in extra:
                perm={v:t for t,v in enumerate(root+tuple(v for v in extra if v!=j))}
                raw=sum(1<<(6*perm[a]+perm[b]) for a,b in E if j not in (a,b))
                if raw not in lookup:break
                deleted.append(lookup[raw])
            if len(deleted)==4:
                def canonical(p):
                    perm={v:t for t,v in enumerate(root+p)}
                    return sum(1<<(7*perm[a]+perm[b]) for a,b in E)
                cols[tuple(sorted(deleted))][k].add(min(canonical(p) for p in permutations(extra)))
    columns=sorted(cols);fine_keys=sorted(orbits);pkeys=sorted(parents)
    C=np.array([[col.count(i) for col in columns] for i in fine_keys],int)
    # N13 paths appear after averaging over four deletions and six label permutations.
    P=np.array([[sum(6//len(orbits[v]) for raw in orbits[v] if raw&MASK==i)
               for v in fine_keys] for i in pkeys])@C
    assert np.all(C.sum(0)==4) and np.all(P.sum(0)==24)
    full_b=[4*parent14[i] for i in fine_keys]
    obj=np.arange(len(columns),dtype=float)/len(columns)
    floor=Q(1,10**8)
    proof={}
    check_full=certificate is not None and certificate['full_N14_test']
    if check_full:
        cert=[Q(certificate['full_N14_test']['full_N14_separator'].get(str(k),0)) for k in fine_keys]
        bound=sum(x*y for x,y in zip(full_b,cert))
        assert bound==Q(certificate['full_N14_test']['target_value']) and bound<0
        assert min(sum(int(a)*y for a,y in zip(col,cert) if a) for col in C.T)>=0
        proof=certificate['full_N14_test']; B=P;rhs=[24*parents[i] for i in pkeys];level='all archived N13 marginals'
    elif sparse_exact(C,full_b,obj) is None:
        cert,bound=separator(C,full_b)
        proof={'full_N14_separator':{str(i):str(v) for i,v in zip(fine_keys,cert) if v},'target_value':str(bound)}
        B=P;rhs=[24*parents[i] for i in pkeys];level='all archived N13 marginals'
    else:
        B=C;rhs=full_b;level='all archived N14 marginals'
    def checked_law(matrix,target,cost,case):
        if certificate is None:
            return sparse_exact(matrix,target,cost)
        src=certificate if case is None else certificate[case]
        sol={int(k):Q(v) for k,v in src['residual_certificate'].items()}
        assert min(sol.values())>=0 and all(0<=k<len(columns) for k in sol)
        assert all(sum(int(matrix[i,j])*v for j,v in sol.items())==x for i,x in enumerate(target))
        return sol
    w=checked_law(B,[x-floor*int(s) for x,s in zip(rhs,B.sum(1))],obj,None)
    if w is None:
        # A fixed positive floor can be incompatible with a marginal on the boundary.
        raise ValueError('Cannot extend with the prescribed common floor')
    def collapse(solution):
        per=Counter()
        for j,col in enumerate(columns):
            weight=floor+solution.get(j,0);g=cols[col];den=sum(map(len,g.values()))
            for k,reps in g.items():per[k]+=weight*len(reps)/den
        assert sum(per.values())==1 and min(per.values())>0
        return {str(k):str(v) for k,v in sorted(per.items())}
    per=collapse(w)
    reverse=checked_law(B,[x-floor*int(s) for x,s in zip(rhs,B.sum(1))],-obj,"alternative_same_N13")
    old14=[sum(int(C[i,j])*v for j,v in w.items()) for i in range(C.shape[0])]
    reverse14=checked_law(C,old14,-obj,"alternative_same_new_N14")
    def encode_alternative(solution):
        return {'residual_certificate':{str(j):str(v) for j,v in solution.items()},'law':collapse(solution)}
    return {'fixed_marginal_level':level,'charge_blind_objective':'column rank / column count',
            'full_N14_test':proof,'floor':str(floor),'columns':len(columns),'types':len(per),
            'chain_N13_paths':len(pkeys),'chain_N14_orbits':len(fine_keys),
            'residual_certificate':{str(j):str(v) for j,v in w.items()},'law':per, 'alternative_same_N13':encode_alternative(reverse),'alternative_same_new_N14':encode_alternative(reverse14)}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
