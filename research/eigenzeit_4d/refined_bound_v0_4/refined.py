"""v0.4: sharper analytic bounds on the unchanged v0.3 confidence region.

The reconstruction and its 20-cell observable transform are inherited from
v0.3. No additional counts, geometry labels or true coordinates enter evaluate.
"""
from pathlib import Path
import sys,math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'joint_region_v0_3'))
import joint as previous
from joint import C,GS2,DS2,GTERMS,CTERMS,K,R2,ceil_sqrt
from intervals import I,lo,hi
# Frozen dependencies alter sys.path; keep this version's controls/audit local.
sys.path.insert(0,str(Path(__file__).resolve().parent))

def evaluate(y,rigorous=False,diagnostics=False):
    """Only the 20 observable cell counts enter this method; no true geometry."""
    scalar=I if rigorous else float
    zero=scalar(0);one=scalar(1)
    sqrt=lambda x:x.sqrt() if isinstance(x,I) else math.sqrt(x)
    sq=lambda x:x.square() if isinstance(x,I) else x*x
    norm=lambda xs:sqrt(sum((sq(v) for v in xs),zero))
    if len(y)!=20 or any(int(x)!=x or int(x)<0 for x in y):
        return {'certified':False,'reason':'INVALID_CELL_COUNTS'}
    y=[int(x) for x in y]
    counts=[sum(y[b]*int(C[k,b]) for b in range(20)) for k in range(20)]
    if min(counts)<16:return {'certified':False,'reason':'COUNT_GUARD'}
    # Integer upper envelope of max(y_i,lambda_i) on the KL region.
    U=[v+K+ceil_sqrt(K*K+2*K*v) for v in y]
    variances=[sum(U[b]*int(C[k,b]) for b in range(20)) for k in range(20)]
    lower=[n-ceil_sqrt(R2*v) for n,v in zip(counts,variances)]
    if min(lower)<=0:return {'certified':False,'reason':'MEAN_LOWER_BOUND'}
    s=[-sqrt(scalar(n)) for n in counts]
    G=[[sum((s[k]*int(GS2[k,i,j])/2 for k in range(20) if GS2[k,i,j]),zero) for j in range(4)] for i in range(4)]
    d=[sum((s[k]*int(DS2[k,i])/2 for k in range(20) if DS2[k,i]),zero) for i in range(4)]
    # LDL whitening, without fitted coordinates or eigenvalue sign repair.
    L=[[one if i==j else zero for j in range(4)] for i in range(4)];D=[]
    for i in range(4):
        pivot=G[i][i]-sum((sq(L[i][k])*D[k] for k in range(i)),zero)
        if (i==0 and hi(pivot)>=0) or (i>0 and lo(pivot)<=0):return {'certified':False,'reason':'LDL_SIGN'}
        D.append(pivot)
        for j in range(i+1,4):
            L[j][i]=(G[j][i]-sum((L[j][k]*L[i][k]*D[k] for k in range(i)),zero))/pivot
    W=[[zero for j in range(4)] for i in range(4)]
    for j in range(4):
        x=[zero]*4
        for i in range(3,-1,-1):
            x[i]=(one if i==j else zero)-sum((L[k][i]*x[k] for k in range(i+1,4)),zero)
        divisor=sqrt(abs(D[j]))
        for i in range(4):W[i][j]=x[i]/divisor
    db=[sum((W[i][j]*d[i] for i in range(4)),zero) for j in range(4)]
    wb=[-db[0],*db[1:]]
    w=[sum((W[i][j]*wb[j] for j in range(4)),zero) for i in range(4)]
    q=-sum((d[i]*w[i] for i in range(4)),zero)
    if lo(q)<=0:return {'certified':False,'reason':'NONPOSITIVE_TIME'}
    gb=[];hs=[];ls=[]
    for k in range(20):
        terms=GTERMS[k]
        gb.append([sum((W[i][r]*W[j][c]*v/2 for i,j,v in terms),zero) for r in range(4) for c in range(4)])
        h=[scalar(int(DS2[k,i]))/2-sum((v*w[j]/2 for ii,j,v in terms if ii==i),zero) for i in range(4)]
        hs.append([sum((W[i][j]*h[i] for i in range(4)),zero) for j in range(4)])
        ls.append(sum((w[i]*w[j]*v/2 for i,j,v in terms),zero)-sum((w[i]*int(DS2[k,i]) for i in range(4)),zero))
    derivative=[-one/(2*sqrt(scalar(n))) for n in counts]
    glin=[];hlin=[];llin=[]
    for b in range(20):
        terms=CTERMS[b]
        glin.append([sum((gb[k][j]*derivative[k] for k in terms),zero) for j in range(16)])
        hlin.append([sum((hs[k][j]*derivative[k] for k in terms),zero) for j in range(4)])
        llin.append(sum((ls[k]*derivative[k] for k in terms),zero))
    # Exact square-root remainder, bounded at the positive count lower bound.
    remainder=[scalar(R2*v)/(2*sqrt(scalar(n))*sq(sqrt(scalar(l))+sqrt(scalar(n))))
               for v,l,n in zip(variances,lower,counts)]
    def psd_bound(S):
        # Each expression upper-bounds lambda_max of the exact PSD matrix.
        trace=sum((S[i][i] for i in range(4)),zero)
        frobenius=norm([S[i][j] for i in range(4) for j in range(4)])
        rows=[sum((abs(S[i][j]) for j in range(4)),zero) for i in range(4)]
        rowbound=scalar(max(hi(x) for x in rows))
        choices=[trace,frobenius,rowbound]
        return min(choices,key=hi)
    SB=[[sum((scalar(U[b])*glin[b][4*k+i]*glin[b][4*k+j]
                    for b in range(20) for k in range(4)),zero) for j in range(4)] for i in range(4)]
    SH=[[sum((scalar(U[b])*hlin[b][i]*hlin[b][j] for b in range(20)),zero)
                    for j in range(4)] for i in range(4)]
    eps=sqrt(scalar(R2)*psd_bound(SB))
    eps+=sum((remainder[k]*norm(gb[k]) for k in range(20)),zero)
    if hi(eps)>=1:return {'certified':False,'reason':'INVERSE_RADIUS','epsilon_upper':str(hi(eps))}
    H=sqrt(scalar(R2)*psd_bound(SH))
    H+=sum((remainder[k]*norm(hs[k]) for k in range(20)),zero)
    first=sqrt(scalar(R2)*sum((scalar(U[b])*sq(llin[b]) for b in range(20)),zero))
    first+=sum((remainder[k]*abs(ls[k]) for k in range(20)),zero)
    bound=first+sq(H)/(one-eps)
    if rigorous:
        from intervals import DOWN,UP
        qlo=DOWN.subtract(q.lo,bound.hi);qhi=UP.add(q.hi,bound.hi)
        accepted=(qlo>0 and DOWN.multiply(qlo,121)>=UP.multiply(q.hi,100)
                  and UP.multiply(qhi,81)<=DOWN.multiply(q.lo,100))
        return {'certified':bool(accepted),'reason':'CERTIFIED' if accepted else 'PRECISION_HOLD',
                'qhat_lower':str(q.lo),'qhat_upper':str(q.hi),'q_lower':str(max(0,qlo)),
                'q_upper':str(qhi),'error_bound_upper':str(bound.hi),'epsilon_upper':str(eps.hi)}
    qlo=max(0,q-bound);qhi=q+bound
    accepted=qlo>0 and qlo*121>=q*100 and qhi*81<=q*100
    result={'certified':bool(accepted),'reason':'CANDIDATE' if accepted else 'PRECISION_HOLD',
            'qhat':q,'q_lower':qlo,'q_upper':qhi,'error_bound':bound,'epsilon_upper':eps}
    if diagnostics:result.update(gradient=llin,first_bound=first,nonlinear_bound=sq(H)/(one-eps),H_bound=H,epsilon=eps)
    return result
