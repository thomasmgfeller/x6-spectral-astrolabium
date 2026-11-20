"""Supplementary calculation with all ten local weights and the entire N13 law fixed."""
from collections import Counter
from fractions import Fraction as F
import json
import numpy as np
import sympy as sp
from scipy.optimize import linprog
from scipy.sparse import csc_matrix
from extension import HERE, MASK, load_inputs, marked_three, build_columns

def solve(reps, parents, cols, target):
    parent_keys=sorted(parents)
    local_ids=sorted({e for e,orbit in reps.values() if any(k&MASK==1564 for k in orbit)})
    m=len(parent_keys)
    E=np.zeros((m+len(local_ids),len(cols)),int)
    idx={p:i for i,p in enumerate(parent_keys)}
    for j,col in enumerate(cols):
        for s in col:
            e,orbit=reps[s]
            for k in orbit:
                p=k&MASK
                E[idx[p],j]+=6//len(orbit)
                if p==1564:E[m+local_ids.index(e),j]+=6//len(orbit)
    joint=Counter()
    for s,v in target.items():
        e,orbit=reps[s]
        for k in orbit:
            if k&MASK==1564:joint[e]+=v/len(orbit)
    b=[24*parents[p] for p in parent_keys]+[24*joint[e] for e in local_ids]
    # Fix a positive common floor on every distinct projection column if feasible.
    for floor in (F(1,10**8),F(0)):
        residual=[v-floor*int(x) for v,x in zip(b,E.sum(axis=1))]
        pr=linprog(np.zeros(len(cols)),A_eq=csc_matrix(E),b_eq=np.array(residual,float),bounds=(0,None),method='highs',options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10})
        if not pr.success: continue
        J=np.flatnonzero(pr.x>1e-12)
        sub=sp.Matrix(E[:,J]); piv=sub.T.to_DM().rref()[1]
        assert len(piv)==len(J)
        vals=sub[list(piv),:].inv()*sp.Matrix([residual[i] for i in piv])
        assert sub*vals==sp.Matrix(residual) and min(vals)>=0
        return {'kind':'extension','common_floor_per_column':str(floor),
                'residual_column_weights':{','.join(map(str,list(cols)[j])):str(x) for j,x in zip(J,vals) if x}}
    return {'kind':'unresolved'}
if __name__=='__main__':
    d,res,w,cat=load_inputs()
    reps,by_code,parents,t=marked_three(d,res,w); cols=build_columns(reps,by_code,cat)
    result={k:solve(reps,parents,cols,v) for k,v in t.items()}
    (HERE/'local_proof.json').write_text(json.dumps(result,indent=2)+'\n')
    print([(k,s['kind'],s.get('common_floor_per_column')) for k,s in result.items()])
