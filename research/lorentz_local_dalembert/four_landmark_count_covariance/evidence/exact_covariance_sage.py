"""Exact count covariance and KKT differentiation on a rational fixture."""
import json
from pathlib import Path
from sage.all import QQ,matrix,vector,diagonal_matrix,identity_matrix,ones_matrix,block_matrix,zero_matrix
from sage.env import SAGE_VERSION
checks=[]
def check(name,x):checks.append(dict(name=name,passed=bool(x)));assert x,name
L=matrix(QQ,[[1,1,0],[1,0,1],[0,1,0]])
C=L*diagonal_matrix(QQ,[50,30,40])*L.T
c=vector(QQ,[1,-1,0])
check('shared_region_covariance',C==matrix(QQ,[[80,50,30],[50,90,0],[30,0,30]]))
check('correlated_difference_variance',c*C*c==70)
check('independent_counts_negative_control',c*diagonal_matrix(QQ,C.diagonal())*c==170)
d=matrix(QQ,[[1,2,3],[1,4,9]]);dd=matrix(QQ,[[1,0,0],[2,0,0]])
t=vector(QQ,[0,2]);dt=vector(QQ,[0,0]);h=identity_matrix(QQ,3)+ones_matrix(QQ,3,3)
M=block_matrix([[h,d.T],[d,zero_matrix(QQ,2,2)]])
u=M.solve_right(vector(QQ,[0,0,0]+list(t)))
dM=block_matrix([[zero_matrix(QQ,3,3),dd.T],[dd,zero_matrix(QQ,2,2)]])
du=M.solve_right(vector(QQ,list(-dd.T*u[3:])+list(dt-dd*u[:3])))
check('KKT_derivative_exact_identity',dM*u+M*du==vector(QQ,[0,0,0]+list(dt)))
J=matrix(QQ,[[-sum(du[:3])]]+[[v] for v in du[:3]])
check('full_root_covariance_preserves_constants',vector(QQ,[1]*4)*J==vector(QQ,[0]))
out=dict(status='PASS',sage_version=SAGE_VERSION,checks=checks,checks_total=len(checks))
(Path(__file__).parent/'exact_covariance_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
