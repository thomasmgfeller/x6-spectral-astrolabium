"""Search for witnesses. verify.py checks their signs exactly using only the standard library."""
from collections import Counter
from fractions import Fraction as F
import json
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csc_matrix, hstack, vstack
from extension import HERE,load_inputs,marked_three,build_columns

def separate(A,b):
    # A has four deletions per column (including multiplicity).
    block=vstack([-A.T, csc_matrix(np.asarray(b,float))])
    r=linprog(np.ones(2*len(b)),A_ub=hstack([block,-block]),b_ub=np.r_[np.zeros(A.shape[1]),-1],bounds=(0,None),method='highs')
    if not r.success:
        return None
    for den in (10**7,10**9):
        y=[F(float(x)).limit_denominator(den) for x in (r.x[:len(b)]-r.x[len(b):])]
        L=min(sum(int(v)*y[i] for i,v in zip(A.indices[A.indptr[j]:A.indptr[j+1]],A.data[A.indptr[j]:A.indptr[j+1]])) for j in range(A.shape[1]))
        y=[z-min(F(0),L)/4 for z in y]
        if sum(x*z for x,z in zip(b,y))<0:
            return y
    return None

if __name__=='__main__':
    d,res,w,cat=load_inputs()
    reps,by_code,parents,targets=marked_three(d,res,w)
    cols=build_columns(reps,by_code,cat)
    keys=sorted(reps)
    rowid={k:i for i,k in enumerate(keys)}
    rr,cc=[],[]
    for j,col in enumerate(cols):
        for s in col:
            rr.append(rowid[s]); cc.append(j)
    A=csc_matrix((np.ones(len(cc),dtype=int),(rr,cc)),shape=(len(keys),len(cols)))
    proof={}
    for t,law in targets.items():
        b=[law[k] for k in keys]
        y=separate(A,b)
        if y is not None:
            proof[t]={'kind':'separating_functional','values':{str(k):str(v) for k,v in zip(keys,y) if v}}
        else:
            p=linprog(np.zeros(A.shape[1]),A_eq=A,b_eq=4*np.asarray(b,float),bounds=(0,None),method='highs')
            if not p.success: raise RuntimeError(p.message)
            import sympy as sp
            support=np.flatnonzero(p.x>1e-12)
            S=sp.Matrix(A[:,support].toarray())
            basis=S.T.rref()[1]
            assert len(basis)==len(support)
            solution=S[list(basis),:].inv()*sp.Matrix([4*b[i] for i in basis])
            assert min(solution)>=0 and S*solution==sp.Matrix([4*v for v in b])
            proof[t]={'kind':'extension','column_weights':{','.join(map(str,list(cols)[j])):str(x) for j,x in zip(support,solution) if x}}
    (HERE/'proof.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(len(cols), [(t,c['kind'],len(c.get('values',c.get('column_weights',{})))) for t,c in proof.items()])
