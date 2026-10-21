"""Independent high precision KKT solve of every accepted candidate's weights."""
import hashlib
import json
from pathlib import Path
from sage.all import QQ, RealField, matrix, vector, identity_matrix, ones_matrix, zero_matrix, block_matrix
from sage.env import SAGE_VERSION

HERE=Path(__file__).resolve().parent
inputs=json.loads((HERE/'intrinsic_inputs.json').read_text())
scales={(r['phase'],r['index']):r['scale'] for r in inputs['records'] if r['status']=='COMPLETE'}
rows=json.loads((HERE/'inference.json').read_text())['records']
checks=[]
def q(x):
    a,b=float(x).as_integer_ratio();return QQ(a)/b
def solve(points,scale,precision):
    R=RealField(precision)
    d=matrix(R,[[q(t),q(x),q(y),q(t)**2,q(x)**2,q(y)**2,q(t)*q(x),q(t)*q(y),q(x)*q(y)] for t,x,y in points]).T
    n=d.ncols();h=identity_matrix(R,n)+ones_matrix(R,n,n)
    target=vector(R,[0,0,0,-2,2,2,0,0,0])
    kkt=block_matrix([[h,d.T],[d,zero_matrix(R,9,9)]])
    solution=kkt.solve_right(vector(R,[0]*n+list(target)))
    a=solution[:n]
    return vector(R,[-sum(a)]+list(a))/R(q(scale))**2, max(abs(v) for v in d*a-target)
for row in rows:
    c=row.get('correction',{})
    if c.get('status')!='ACCEPTED':continue
    scale=scales[row['phase'],row['index']]
    low,_=solve(c['features'],scale,128);high,res=solve(c['features'],scale,256)
    convergence=max(float(abs(a-b)/(1+abs(b))) for a,b in zip(low,high))
    error=max(float(abs(a-q(b))/(1e-8+1e-7*abs(a))) for a,b in zip(high,c['weights']))
    passed=convergence<1e-22 and error<=1 and res<RealField(256)('1e-50')
    checks.append(dict(phase=row['phase'],index=row['index'],passed=bool(passed),
                       precision_relative_error=convergence,weight_tolerance_ratio=error))
    assert passed
out=dict(status='PASS',sage_version=SAGE_VERSION,checked=len(checks),checks=checks,
         inference_sha256=hashlib.sha256((HERE/'inference.json').read_bytes()).hexdigest())
(HERE/'sage_weight_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
