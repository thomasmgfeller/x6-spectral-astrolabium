"""Independent exact geometry identities in SageMath; no NumPy solver import."""
import json
from pathlib import Path
from sage.all import QQ, matrix, vector, diagonal_matrix, block_matrix
from sage.env import SAGE_VERSION

eta = diagonal_matrix(QQ, [-1, 1, 1])
landmarks = matrix(QQ, [[-8, 0, 0], [-9, 1, 0], [-10, 0, 1]])
x = vector(QQ, [-2, QQ(1)/3, -QQ(1)/4])
h = landmarks*eta*landmarks.transpose()
v = landmarks*eta*x
q0 = -x*eta*x
qa = vector(QQ, [-a*eta*a for a in landmarks.rows()])
qax = vector(QQ, [-(a-x)*eta*(a-x) for a in landmarks.rows()])
reconstructed_v = (qax-qa-vector(QQ, [q0]*3))/2
checks = []
def check(name, passed):
    checks.append(dict(name=name, passed=bool(passed)))
    assert passed, name

check('nondegenerate_timelike_landmarks', landmarks.det()!=0 and all(q>0 for q in qa))
check('polarization_identity', v==reconstructed_v)
check('schur_shell_identity', v*h.inverse()*v == -q0)
full = block_matrix(QQ, [[h, matrix(QQ, 3, 1, list(v))],
                        [matrix(QQ, 1, 3, list(v)), matrix(QQ, 1, 1, [-q0])]])
check('augmented_gram_rank_three', full.rank()==3 and full.det()==0)
bad_v = vector(QQ, list(v)); bad_v[1] += QQ(1)/10
bad = matrix(QQ, full.rows())
for i in range(3):
    bad[i, 3] = bad[3, i] = bad_v[i]
check('inconsistent_intervals_detected', bad_v*h.inverse()*bad_v != -q0 and bad.det()!=0)
check('exact_schur_determinant', bad.det()==h.det()*(-q0-bad_v*h.inverse()*bad_v))
recovered = eta*landmarks.inverse()*v
check('exact_coordinate_recovery', recovered==x)
lor = matrix(QQ, [[QQ(5)/4, -QQ(3)/4, 0], [-QQ(3)/4, QQ(5)/4, 0], [0, 0, 1]])
ll = landmarks*lor.transpose(); xx=lor*x
check('lorentz_metric', lor.transpose()*eta*lor==eta)
check('invariant_distance_constraints', ll*eta*ll.transpose()==h and ll*eta*xx==v)
check('three_landmark_differences_rank_limit',
      matrix(QQ, [landmarks[1]-landmarks[0], landmarks[2]-landmarks[0]]).rank()==2)
# A common affine error preserves the annihilation of all linear fields.
p = matrix(QQ, [[-1,0,0],[-2,0,0],[-2,1,0],[-2,-1,0],[-2,0,1],[-2,0,-1],[-3,1,1],[-3,1,0],[-3,0,1]])
a = vector(QQ, [2,-5,1,1,1,1,0,0,0])
affine = matrix(QQ, [[2,QQ(1)/3,0],[0,1,QQ(1)/5],[QQ(1)/7,0,3]])
check('common_linear_distortion_preserves_linear_null', p.transpose()*a==vector(QQ,[0,0,0]) and (p*affine).transpose()*a==vector(QQ,[0,0,0]))
out = dict(status='PASS', sage_version=SAGE_VERSION, checks=checks,
           defect_schur=str(-q0-bad_v*h.inverse()*bad_v),
           scope='Exact identities and counterexamples only; no noisy-cloud success implied.')
(Path(__file__).parent/'exact_geometry_results.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out, indent=2))
