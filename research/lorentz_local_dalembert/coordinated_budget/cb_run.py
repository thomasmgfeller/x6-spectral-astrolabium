"""All-direction certificate for a fixed-base additive displacement budget.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'conformal_sensitivity'))
from cs_run import I,T,matvec,mm,verified_solve,weights_from
from ct_run import inputs,F,read,save,boosted,exact_weights,sqrt_bounds,outward,atanh_bounds
from sc_run import constant
from st_certificate import solve

def matrices(z):
    y=[[a-b for a,b in zip(row,z[4])] for row in z[5:]]
    M=list(map(list,zip(*[[t,x,v,t*t,x*x,v*v,t*x,t*v,x*v] for t,x,v in y])))
    sums=[sum(row) for row in M]
    S=[[sum(a*b for a,b in zip(ri,rj))-si*sj/17 for rj,sj in zip(M,sums)] for ri,si in zip(M,sums)]
    return M,S

def derivatives(z,M,Q,lam0,node):
    t,x,y=[a-b for a,b in zip(z[node+5],z[4])]
    zero=t*0;one=zero+1
    ds=[[one,zero,zero,2*t,zero,zero,x,y,zero],
        [zero,one,zero,zero,2*x,zero,t,zero,y],
        [zero,zero,one,zero,zero,2*y,zero,t,x]]
    v=[row[node]-sum(row)/17 for row in M];qv=matvec(Q,v);blocks=[];residual=[]
    for dp in ds:
        qdp=matvec(Q,dp)
        blocks.append([[qdp[i]*v[j]+qv[i]*dp[j] for j in range(9)] for i in range(9)])
        residual.append([qdp[i]*sum(a*b for a,b in zip(v,lam0))+qv[i]*sum(a*b for a,b in zip(dp,lam0)) for i in range(9)])
    return blocks,residual

def dual_norm(a,b,c):
    return max(F(a.mag(),T),sqrt_bounds(F(b.mag(),T)**2+F(c.mag(),T)**2)[1])

def build():
    for name,h in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z0=inputs();z=boosted(z0);scale=F(w['scale']);C=constant(w)
    M0,S0=matrices(z);rhs=list(map(F,[0,0,0,-2,2,2,0,0,0]));lam0=solve(S0,rhs)
    Q=list(map(list,zip(*[solve(S0,[F(int(i==j)) for i in range(9)]) for j in range(9)])))
    ident=[[F(int(i==j)) for j in range(9)] for i in range(9)]
    assert mm(Q,S0)==ident and matvec(S0,lam0)==rhs
    base=weights_from(M0,lam0,scale)
    assert base==exact_weights(z,scale)==exact_weights(z0,scale)
    normbase=sqrt_bounds(sum(v*v for v in base))
    budget=F(c['enclosing_poisson_budget']);h=budget/C
    loglo,loghi=[2*v for v in atanh_bounds(F(1,7))]
    assert loghi<budget # log(4/3)=2 atanh(1/7); all TV-certificate eligible shifts covered
    zz=[[I(v-h,v+h) if i>=5 else I(v) for v in row] for i,row in enumerate(z)]
    M,_=matrices(zz);Ks=[];Rs=[]
    for node in range(16):
        B,R=derivatives(zz,M,Q,lam0,node)
        Ks.append([[dual_norm(B[0][i][j],B[1][i][j],B[2][i][j]) for j in range(9)] for i in range(9)])
        Rs.append([dual_norm(R[0][i],R[1][i],R[2][i]) for i in range(9)])
    K=[[max(v[i][j] for v in Ks) for j in range(9)] for i in range(9)]
    rr=[h*max(r[i] for r in Rs) for i in range(9)]
    A=[[I(int(i==j)-h*K[i][j],int(i==j)+h*K[i][j]) for j in range(9)] for i in range(9)]
    # Solve centered equation (Q S) e = -Q(S-S0)lam0; residual is symmetric.
    e,eta=verified_solve(A,[I(-v,v) for v in rr],ident)
    lam=[I(a)+b for a,b in zip(lam0,e)];weights=weights_from(M,lam,scale)
    distance=sqrt_bounds(sum(F((v-I(b)).mag(),T)**2 for v,b in zip(weights,base)))[1]
    relative=distance/normbase[0];assert relative<2
    symmetric=2*relative/(2-relative)
    assert symmetric<F(c['strong_symmetric_gap_gate']),'UNRESOLVED: strong gate not excluded'
    certificate=dict(inverse=[[str(v) for v in row] for row in Q],
       preconditioned_derivative_upper=[[str(v) for v in row] for row in K],
       centered_residual_upper=[str(v) for v in rr],
       multiplier_intervals=[[str(F(v.lo,T)),str(F(v.hi,T))] for v in lam],
       weight_intervals=[[str(F(v.lo,T)),str(F(v.hi,T))] for v in weights])
    summary=dict(status='CERTIFIED_COORDINATED_BUDGET_STOP',moving_nodes=16,coordinate_dimensions=48,
       poisson_coefficient=outward(C),displacement_budget=outward(h),
       enclosing_poisson_budget=str(budget),log_four_thirds=outward(loglo,loghi),
       inverse_residual_upper=outward(eta)[1],base_relative_gap_upper=outward(relative)[1],
       symmetric_relative_gap_upper=outward(symmetric)[1],strong_gate_excluded=True,
       scope='All fixed-base support deformations within the additive budget; coupling-law interpretation requires unchanged selected-node order and inherited admissibility gates. Not actual-TV, arbitrary-pair, global or continuum stability.')
    return certificate,summary

if __name__=='__main__':
    for name,data in zip(['certificate.json','summary.json'],build()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
    print(json.dumps(data))
