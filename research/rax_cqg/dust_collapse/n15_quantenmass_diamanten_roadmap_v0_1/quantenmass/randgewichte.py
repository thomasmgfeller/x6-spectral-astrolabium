"""Exact finite illustrations of a free exterior weight and weak consistency."""
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path

def verify(ok, message):
    if not ok:
        raise ArithmeticError(message)

def run():
    # Gram matrix of (1/2,1/4) and (1/2,-1/4); total vector (1,0).
    vectors = ((F(1,2),F(1,4)),(F(1,2),-F(1,4)))
    gram = [[sum(x*y for x,y in zip(a,b)) for b in vectors] for a in vectors]
    verify(sum(map(sum,gram))==1,'normalization')
    cases=[]
    pairs=list(product(range(2),repeat=2))
    for q in map(F,('0','1/4','1/2','3/4','1')):
        weights=(q,1-q)
        def joint(h,s,k,t):
            return weights[s]*gram[h][k] if s==t else F(0)
        local=[[sum(joint(h,s,k,t) for s,t in pairs) for k in range(2)] for h in range(2)]
        outer=[[sum(joint(h,s,k,t) for h,k in pairs) for t in range(2)] for s in range(2)]
        verify(local==gram,'local marginal')
        verify(outer==[[q,0],[0,1-q]],'exterior weights and decoherence')
        cases.append(dict(q_flat=str(q),open=str(1-q),retained_mass_in_shared_interval=str(1-q)))
    # D_12=i/2 and D_21=-i/2 arise from a rank-one complex Gram matrix.
    # For independent copies D_12*D_12=-1/4 alters the measure of the union.
    imag=F(1,2)
    diagonal_per_joint_atom=F(1,2)**2
    off_diagonal_real=-imag**2
    union=2*diagonal_per_joint_atom+2*off_diagonal_real
    verify(union==0 and 2*diagonal_per_joint_atom==F(1,2),'composition')
    return dict(local_gram=[[str(x) for x in row] for row in gram],exterior_cases=cases,
                two_copy_11_22=dict(sum_diagonal='1/2',one_cross_real='-1/4',union_measure=str(union)))

if __name__=='__main__':
    Path(__file__).with_name('randgewichte.json').write_text(json.dumps(run(),indent=2)+'\n')
