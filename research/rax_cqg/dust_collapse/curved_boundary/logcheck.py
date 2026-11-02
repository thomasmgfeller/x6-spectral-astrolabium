import json
import math
from pathlib import Path
from prediction import A
from reference import physical_expectation
from common import write_rows

cfg=json.loads(Path('logcheck_design.json').read_text())
s=cfg['s']; U=1-s
records=[];slopes=[]
for P,F in cfg['windows']:
    values=[]
    for lam in cfg['intensities']:
        ns=cfg['orders']
        r0=physical_expectation(s,P,F,lam,ns[0],cap=15.)
        r1=physical_expectation(s,P,F,lam,ns[1],cap=13.)
        r2=physical_expectation(s,P,F,lam,ns[2],lens=True,cap=12.)
        values.append((lam,r0,r1,r2))
        records.append(dict(s=s,P=P,F=F,lam=lam,R112=r0,R160=r1,R208=r2))
        print(P,F,lam,r0,r1,r2,flush=True)
    for (l0,*prev),(l1,*cur) in zip(values,values[1:]):
        a=[U**2*(math.sqrt(l1)*(v1-1)-math.sqrt(l0)*(v0-1))/math.log(l1/l0)
           for v0,v1 in zip(prev,cur)]
        slopes.append(dict(P=P,F=F,lo=l0,hi=l1,A112=a[0],A160=a[1],A208=a[2],target=A,
                           last_gap=abs(a[1]-a[2])))
write_rows('logcheck_values.csv',records)
write_rows('logcheck_slopes.csv',slopes)
print(*slopes,sep='\n')
