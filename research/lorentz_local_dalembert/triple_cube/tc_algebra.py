"""Independent direct nine-moment comparisons for the joint rank-six formula.
SPDX-License-Identifier: Apache-2.0
"""
from tc_common import *
from cb_run import matrices

def direct_change(b,s):
    return [a-w for a,w in zip(exact_weights(moved(b,*s),F(b['w']['scale'])),b['weights'])]

def algebra(c):
    b=setup(c);count=Counter()
    for source in c['algebra_controls']:
        s=list(map(F,source));z=moved(b,*s);M,S=matrices(z)
        U=[[M[i][node-5]-b['M'][i][node-5] for i in range(9)] for node in b['nodes']]
        V=[[r[node-5]-sum(r)/17 for r in b['M']] for node in b['nodes']]
        L=V+U
        # Build the six-dimensional matrix directly from changed moment columns.
        direct=[[dot(x,matrix_vector(b['Q'],y)) for y in L] for x in L]
        for i in range(3):
            for j in range(3):direct[i][j]-=F(int(i==j))-F(1,17)
            direct[i][i+3]+=1;direct[i+3][i]+=1
        A=[[pval(p,*s) for p in row] for row in b['A']];rhs=[pval(p,*s) for p in b['rhs']]
        assert A==direct and rhs==[dot(x,b['lam']) for x in L]
        eta=matrix_vector(inv(A),rhs);change=[sum(pval(p,*s)*v for p,v in zip(row,eta))/F(b['w']['scale'])**2 for row in b['W']]
        assert change==direct_change(b,s);count['exact_direct_nine_moment_comparisons']+=1
        # Gram expansion includes every U_i K_ij U_j^T term, including all cross terms.
        _,S0=matrices(b['z'])
        expected=[[S0[i][j]+sum(V[a][i]*U[a][j]+U[a][i]*V[a][j] for a in range(3))+sum(U[a][i]*(F(int(a==d))-F(1,17))*U[d][j] for a in range(3) for d in range(3)) for j in range(9)] for i in range(9)]
        assert S==expected;count['joint_Gram_identities']+=1
        center=[F(1,100),F(-1,200),F(1,300)];delta=[x-y for x,y in zip(s,center)]
        for row in b['A']:
            for p in row:assert pval(pshift(p,*center),*delta)==pval(p,*s)
        count['exact_polynomial_shift_checks']+=36
    for a,d in itertools.combinations(range(3),2):
        s=[F(0)]*3;s[a]=F(1,100);s[d]=F(1,50)
        one=s.copy();one[d]=0;two=s.copy();two[a]=0;i,j=b['nodes'][a],b['nodes'][d]
        q=lambda t:interval(moved(b,*t),i,j)
        assert q(s)-q(one)-q(two)+q([F(0)]*3)==2*s[a]*s[d]
        count['nonzero_pairwise_mixed_geometry_controls']+=1
    s=[F(1,100),F(-1,50),F(3,100)];joint=direct_change(b,s);parts=[]
    for i in range(3):v=[F(0)]*3;v[i]=s[i];parts.append(direct_change(b,v))
    assert joint!=[sum(v) for v in zip(*parts)];count['additive_operator_negative_controls']+=1
    return dict(status='PASS',**dict(count),scope='Declared algebra controls only; no domain classification or probability scan.')

if __name__=='__main__':
    result=algebra(read(HERE/'contract.json'))
    if '--verify' in sys.argv:assert result==read(HERE/'algebra.json')
    else:save(HERE/'algebra.json',result)
    print(json.dumps(result),flush=True)
