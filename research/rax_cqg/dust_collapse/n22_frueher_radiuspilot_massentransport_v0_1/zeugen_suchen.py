"""Optional proposal generator (NumPy, SciPy). Verification uses only fractions."""
from pathlib import Path
import json,sys

from pilotfelder import *
import numpy as np
from scipy.optimize import linprog

templates={}
with archive() as (rows,rel,coeff,free,goals):
    x,w,pos,nodes=read_box(rows[0][2]); chains=paths(nodes,rel)
    for i,(_,_,row) in enumerate(rows):
        x,w,pos,nodes=read_box(row)
        crossing=[p for p in chains if x[p[0]][1]<HALF<x[p[-1]][0]]
        b=[float(sum(w[j])/2) for j in nodes]
        cols=[shares(p,x) for p in crossing]
        A=np.array([[float(sum(s.get(j,(0,0)))/2) for s in cols] for j in nodes])
        result=linprog(-np.ones(len(cols)),A_ub=A,b_ub=b,bounds=(0,None),method='highs')
        assert result.success,result.message
        scale=10**12
        templates[str(i)]=dict(primal={','.join(map(str,p)):int(round(v*scale)) for p,v in zip(crossing,result.x) if v>0},
                               dual={str(j):int(round(-v*scale)) for j,v in zip(nodes,result.ineqlin.marginals) if v<0})
        if i in (0,63): print(len(chains),len(crossing),nodes,'fraction',-result.fun/sum(b),templates[str(i)],flush=True)
(ROOT/'Optimierungszeugen_neu.json').write_text(json.dumps(templates,sort_keys=True,indent=2)+'\n')
