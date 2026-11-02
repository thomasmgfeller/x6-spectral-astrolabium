"""Round-off audit for density slopes; independent pair quadratures and precision."""
import json
import math
from pathlib import Path
from common import write_rows
from precision import polished
from prediction import A
from reference import physical_expectation

cfg=json.loads(Path('logcheck_design.json').read_text())
s=cfg['s'];U=1-s
rows=[];slopes=[]
for P,F in cfg['windows']:
    series=[]
    for lam in cfg['intensities']:
        # Both integrate the exact volume polynomial. Different radial cuts and orders.
        a=physical_expectation(s,P,F,lam,88,cap=14,node_rule=polished)
        b=physical_expectation(s,P,F,lam,128,cap=12,node_rule=polished)
        prev=series[-1] if series else None
        series.append((lam,a,b))
        rows.append(dict(P=P,F=F,lam=lam,R88=a,R128=b))
        if prev:
            lo=prev[0]
            estimates=[U**2*(math.sqrt(lam)*(val-1)-math.sqrt(lo)*(old-1))/math.log(lam/lo)
                       for val,old in zip([a,b],prev[1:])]
            slopes.append(dict(P=P,F=F,lo=lo,hi=lam,A88=estimates[0],A128=estimates[1],
                               target=A,gap=abs(estimates[0]-estimates[1])))
        print(P,F,lam,a,b,flush=True)
write_rows('logcheck_precision.csv',rows)
write_rows('logcheck_precision_slopes.csv',slopes)
print(*slopes,sep='\n')
