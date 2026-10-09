"""Independent rational spectral-gap checks. Requires Python stdlib only."""
from fractions import Fraction as F
import json
from pathlib import Path

def laplacian(n,edges):
    L=[[F(0) for _ in range(n)] for _ in range(n)]
    for a,b,w in edges:
        w=F(w)
        assert 0<=a<n and 0<=b<n and a!=b and w>0
        L[a][a]+=w;L[b][b]+=w;L[a][b]-=w;L[b][a]-=w
    return L

def positive_definite(M):
    # Independent rational elimination: symmetric Schur complements
    A=[row[:] for row in M]
    for k in range(len(A)):
        p=A[k][k]
        if p<=0:return False
        for i in range(k+1,len(A)):
            for j in range(k+1,len(A)):
                A[i][j]-=A[i][k]*A[k][j]/p
    return True

def certified_lower(L,b):
    n=len(L); b=F(b)
    M=[[L[i][j]+(b+1)/n-(b if i==j else 0) for j in range(n)] for i in range(n)]
    return positive_definite(M)

def rayleigh_upper(L):
    n=len(L)
    return min((L[i][i]+L[j][j]-2*L[i][j])/2 for i in range(n) for j in range(i+1,n))

def run():
    cases=[('path4',4,[(0,1,'1'),(1,2,'1'),(2,3,'1')],'1/2','3/5'),
           ('triangle',3,[(0,1,'1'),(1,2,'1'),(0,2,'1')],'2','3'),
           ('weighted2',2,[(0,1,'1/8')],'1/8','1/4'),
           ('rounded_signal_path',4,[(0,1,'367879/1000000'),(1,2,'367879/1000000'),(2,3,'367879/1000000')],'367879/6000000','1/2'),
           ('disconnected',4,[(0,1,'1'),(2,3,'1')],'1/10','1/2')]
    results=[]
    for name,n,edges,valid,invalid in cases:
        L=laplacian(n,edges)
        p=certified_lower(L,valid);q=not certified_lower(L,invalid)
        expected_valid=name!='disconnected'
        results.append(dict(name=name,valid_bound=valid,valid_accepted=p,expected_valid=expected_valid,invalid_bound=invalid,invalid_rejected=q,upper=str(rayleigh_upper(L)),pass_=p==expected_valid and q))
    report={'schema':'x6-community-audit-1','engine':'Python stdlib fractions','results':results,'passed':sum(r['pass_'] for r in results),'total':len(results)}
    Path(__file__).with_name('python_results.local.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2));assert all(r['pass_'] for r in results)
if __name__=='__main__':run()
