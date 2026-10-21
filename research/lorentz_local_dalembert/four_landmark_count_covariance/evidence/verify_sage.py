"""Post-run independent high-precision audit. No production inference imports."""
import gzip,json
from pathlib import Path
from sage.all import QQ,RealField,matrix,vector,identity_matrix,ones_matrix,zero_matrix,block_matrix
from sage.env import SAGE_VERSION
HERE=Path(__file__).resolve().parent
cfg=json.loads((HERE/'contract.json').read_text())

def exact_float(x):
    n,d=float(x).as_integer_ratio();return QQ(n)/d

def calculate(row,bits,covariance=False):
    R=RealField(bits);packet=row['selection']['fourth']['packet'];rep=row['replicates'][0]
    counts=rep['observed']['counts'];n=len(packet['support']);m=len(counts)
    scale=R(exact_float(packet['scale']));rho=R(cfg['count_density'])
    qs=vector(R,[(R(v)/(rho*R.pi()/12))**(R(2)/3)/scale**2 for v in counts])
    lookup={tuple(pair):i for i,pair in enumerate(packet['pairs'])}
    def coef(a,b):
        ans=vector(R,m)
        if a!=b:ans[lookup[tuple(sorted((a,b)))]]=1
        return ans
    l=packet['landmarks'];root=packet['root'];support=packet['support']
    gm=[[ (coef(l[i+1],l[j+1])-coef(l[i+1],l[0])-coef(l[0],l[j+1]))/2 for j in range(3)] for i in range(3)]
    zm=[[(coef(l[i+1],x)-coef(l[0],x)-coef(l[i+1],root)+coef(l[0],root))/2 for i in range(3)] for x in support]
    z=matrix(R,[[v*qs for v in a] for a in zm])
    d=matrix(R,[[t,x,y,t*t,x*x,y*y,t*x,t*y,x*y] for t,x,y in z]).T
    tm=matrix(R,[vector(R,m) for i in range(3)]+[2*gm[0][0],2*gm[1][1],2*gm[2][2],2*gm[0][1],2*gm[0][2],2*gm[1][2]])
    target=tm*qs;noise=identity_matrix(R,n)+ones_matrix(R,n,n)
    M=block_matrix([[noise,d.T],[d,zero_matrix(R,9,9)]])
    u=M.solve_right(vector(R,[0]*n+list(target)))
    weights=vector(R,[-sum(u[:n])]+list(u[:n]))/scale**2
    result=dict(weights=weights,residual=max(abs(v) for v in M*u-vector(R,[0]*n+list(target))))
    if covariance:
        derivatives=[]
        for k in range(m):
            dd=matrix(R,[[zm[j][0][k],zm[j][1][k],zm[j][2][k],
                          2*z[j,0]*zm[j][0][k],2*z[j,1]*zm[j][1][k],2*z[j,2]*zm[j][2][k],
                          z[j,0]*zm[j][1][k]+z[j,1]*zm[j][0][k],
                          z[j,0]*zm[j][2][k]+z[j,2]*zm[j][0][k],
                          z[j,1]*zm[j][2][k]+z[j,2]*zm[j][1][k]] for j in range(n)]).T
            rhs=vector(R,list(-dd.T*u[n:])+list(tm.column(k)-dd*u[:n]))
            derivatives.append(M.solve_right(rhs)[:n])
        da=matrix(R,derivatives).T
        J=matrix(R,[[-sum(da.column(k)) for k in range(m)]]+da.rows())/scale**2
        jacN=vector(R,[(R(2)/3)*qs[k]/counts[k] if counts[k] else R(0) for k in range(m)])
        K=matrix(R,rep['observed']['overlaps'])
        Cq=matrix(R,[[jacN[i]*K[i,j]*jacN[j] for j in range(m)] for i in range(m)])
        result['covariance']=J*Cq*J.T
    return result

checks=[]
for path in sorted((HERE/'results').glob('cloud-*.json.gz')):
    row=json.loads(gzip.decompress(path.read_bytes()))
    if not row['replicates'] or row['replicates'][0]['inference']['four']['status']!='WEIGHTS_VALID':continue
    low=calculate(row,128);high=calculate(row,256,True)
    saved=row['replicates'][0]['inference']['four']
    convergence=max(float(abs(a-b)/(1+abs(b))) for a,b in zip(low['weights'],high['weights']))
    ratio=max(float(abs(a-exact_float(b))/(1e-8+1e-7*abs(a))) for a,b in zip(high['weights'],saved['weights']))
    C=high['covariance'];R=C.base_ring();archive=matrix(R,[[exact_float(v) for v in rr] for rr in saved['weight_covariance']])
    discrepancy=float((C-archive).norm()/(R('1e-8')+C.norm()))
    passed=convergence<1e-22 and ratio<=1 and high['residual']<R('1e-50') and discrepancy<1e-6
    entry=dict(index=row['index'],passed=bool(passed),precision_relative_error=convergence,weight_tolerance_ratio=ratio,covariance_relative_error=discrepancy)
    checks.append(entry);assert passed,entry
out=dict(status='PASS',sage_version=SAGE_VERSION,checked_primary_operators=len(checks),checks=checks,
         scope='Independent high-precision numerical reproduction, not statistical validation')
(HERE/'sage_verification.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
