"""Standalone Python-standard-library exact check of the six-node witness.
No NumPy, SciPy, Sage, original inference module or original generator required.
The exact arithmetic refers to archived binary64 input numbers.
SPDX-License-Identifier: Apache-2.0
"""
from fractions import Fraction as F
import json
from pathlib import Path

here=Path(__file__).resolve().parent
w=json.loads((here/'evidence/minimal_counterexample.json').read_text())
lookup={tuple(sorted(r['pair'])):F(r['q']) for r in w['measurements']}
def q(a,b):return F(0) if a==b else lookup[tuple(sorted((a,b)))]
l=w['landmarks'];x,y=w['support_pair']
h=[[(q(l[i],l[j])-q(l[i],l[0])-q(l[0],l[j]))/2 for j in range(1,4)] for i in range(1,4)]
v=[(q(l[i],y)-q(l[0],y)-q(l[i],x)+q(l[0],x))/2 for i in range(1,4)]
# Solve H u = v in rational arithmetic by Gauss-Jordan elimination.
a=[h[i]+[v[i]] for i in range(3)]
for k in range(3):
    pivot=next(i for i in range(k,3) if a[i][k]);a[k],a[pivot]=a[pivot],a[k]
    d=a[k][k];a[k]=[b/d for b in a[k]]
    for i in range(3):
        if i!=k:
            d=a[i][k];a[i]=[b-d*c for b,c in zip(a[i],a[k])]
s=sum(v[i]*a[i][3] for i in range(3))
p,r=w['truth_coordinates'][4:]
delta=[F(b)-F(a) for a,b in zip(p,r)]
true=(-delta[0]**2+delta[1]**2+delta[2]**2)/F(w['scale'])**2
assert true>0 and s<0, 'The witness is expected to be spacelike -> timelike.'
out={'status':'PASS','original_cloud_index':w['original_cloud_index'],
     'nodes':6,'counted_intervals':14,'arithmetic':'exact fractions of archived binary64 inputs',
     'true_squared_interval':float(true),'reconstructed_squared_interval':float(s),
     'true_sign':'spacelike','reconstructed_sign':'timelike',
     'reconstructed_exact_fraction':str(s),'true_exact_fraction':str(true)}
(here/'evidence/minimal_counterexample_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if 'fraction' not in k},indent=2))
