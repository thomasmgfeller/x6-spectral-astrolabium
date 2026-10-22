"""V2 proof fixtures, independently assembled in rational Sage arithmetic."""
import json
from pathlib import Path
from sage.all import QQ, matrix, vector, diagonal_matrix, block_matrix, identity_matrix, ones_matrix, zero_matrix
from sage.env import SAGE_VERSION

HERE=Path(__file__).resolve().parent
eta=diagonal_matrix(QQ,[-1,1,1])
anchors=matrix(QQ,[[-8,0,0],[-10,1,0],[-12,0,1],[-15,0,0]])
p=matrix(QQ,[[-1,0,0],[-2,0,0],[-2,1,0],[-2,-1,0],[-2,0,1],[-2,0,-1],[-3,1,1],[-3,1,0],[-3,0,1],[-4,1,2],[-4,-2,1]])
q=lambda a,b: -(a-b)*eta*(a-b)
root=vector(QQ,[0,0,0])
qa=matrix(QQ,[[q(a,b) for b in anchors] for a in anchors])
qr=vector(QQ,[q(a,root) for a in anchors])
qx=matrix(QQ,[[q(a,x) for x in p] for a in anchors])
diff=matrix(QQ,[a-anchors[0] for a in anchors.rows()[1:]])
psi=matrix(QQ,[[(qx[i,j]-qx[0,j]-qr[i]+qr[0])/2 for j in range(p.nrows())] for i in range(1,4)]).T
h=matrix(QQ,[[(qa[i,j]-qa[i,0]-qa[0,j])/2 for j in range(1,4)] for i in range(1,4)])
checks=[]
def check(name,value):
    checks.append(dict(name=name,passed=bool(value)))
    assert value,name
def design(x):
    return matrix(QQ,[[t,a,b,t*t,a*a,b*b,t*a,t*b,a*b] for t,a,b in x]).T
def solve(d,target):
    n=d.ncols();noise=identity_matrix(QQ,n)+ones_matrix(QQ,n,n)
    kkt=block_matrix([[noise,d.T],[d,zero_matrix(QQ,9,9)]])
    sol=kkt.solve_right(vector(QQ,[0]*n+list(target)))
    return sol[:n]
target=vector(QQ,[0,0,0,2*h[0,0],2*h[1,1],2*h[2,2],2*h[0,1],2*h[0,2],2*h[1,2]])
a=solve(design(psi),target)
physical=vector(QQ,[0,0,0,-2,2,2,0,0,0])
reference=solve(design(p),physical)
check('all_external_intervals_timelike', all(qa[i,j]>0 for i in range(4) for j in range(i)) and all(v>0 for v in qr) and all(v>0 for v in qx.list()))
check('affine_landmark_rank_three',diff.det()!=0)
check('squared_distance_difference_linear',psi==p*eta*diff.T)
check('metric_from_anchor_distances',h==diff*eta*diff.T)
check('physical_linear_moments_exact',p.T*a==vector(QQ,[0,0,0]))
check('physical_quadratic_moments_exact',design(p)*a==physical)
check('same_unique_minimum_variance_operator',a==reference)
scaled=solve(design(psi/QQ(7)**2),target/QQ(7)**2)/QQ(7)**2
check('normalization_scale_invariance',scaled==a)
perm=[2,0,3,1]
aa=anchors.matrix_from_rows(perm)
dd=matrix(QQ,[v-aa[0] for v in aa.rows()[1:]])
hh=dd*eta*dd.T;pp=p*eta*dd.T
tt=vector(QQ,[0,0,0,2*hh[0,0],2*hh[1,1],2*hh[2,2],2*hh[0,1],2*hh[0,2],2*hh[1,2]])
check('landmark_permutation_exact_weights',solve(design(pp),tt)==a)
check('only_three_external_landmarks_insufficient',diff.matrix_from_rows([0,1]).rank()==2)
out=dict(status='PASS',sage_version=SAGE_VERSION,checks=checks,checks_total=len(checks),
         noisy_cloud_validation='NOT_RUN',scope='Exact-distance theorem and rational fixtures, not a finite-density guarantee.')
(HERE/'four_landmark_exact_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
