"""Validated use of two exact flat-landmark consistency constraints."""
from pathlib import Path
from fractions import Fraction
import sys,math
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/'refined_bound_v0_4'))
import refined as baseline
from refined import C,GS2,DS2,GTERMS,CTERMS,K,R2,ceil_sqrt
from intervals import I,lo,hi
sys.path.insert(0,str(ROOT))
SCALE=2**20
BP2=np.zeros((20,4,2),dtype=np.int64);SP=np.zeros((20,2),dtype=np.int64)
for k,full in enumerate(baseline.previous.baseline.PRED):
    pair=baseline.previous.baseline.PAIRS[full]
    for a,target in enumerate([5,6]):
        SP[k,a]=int(pair==(0,target))
        for i in range(1,5):BP2[k,i-1,a]=int(pair==(0,i))+int(pair==(0,target))-int(pair==(i,target))

def select_coefficients(g,R,U):
    """Floating proposal only. Any bounded dyadic pair is valid for the proof."""
    g=np.array(g,float);R=np.array(R,float);U=np.array(U,float)
    S=(R*U)@R.T;t=(R*U)@g
    if not np.all(np.isfinite(S)) or np.linalg.det(S)<=1e-12*np.trace(S)**2:return [0,0]
    k=-np.linalg.solve(S,t)
    if not np.all(np.isfinite(k)) or np.max(abs(k))>16:return [0,0]
    return [int(np.rint(v*SCALE)) for v in k]

def evaluate(y,rigorous=False,coefficients=None,diagnostics=False):
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
    P=[[sum((s[k]*int(BP2[k,i,a])/2 for k in range(20)),zero) for a in range(2)] for i in range(4)]
    X=[[zero for a in range(2)] for i in range(4)]
    for a in range(2):
        z=[]
        for i in range(4):z.append(P[i][a]-sum((L[i][k]*z[k] for k in range(i)),zero))
        v=[z[i]/D[i] for i in range(4)]
        for i in range(3,-1,-1):X[i][a]=v[i]-sum((L[k][i]*X[k][a] for k in range(i+1,4)),zero)
    residual=[sum((P[i][a]*X[i][a] for i in range(4)),zero)-sum((s[k]*int(SP[k,a]) for k in range(20)),zero) for a in range(2)]
    gb=[];hj=[];lq=[];ljr=[]
    for k in range(20):
        terms=GTERMS[k]
        gb.append([sum((W[i][r]*W[j][c]*v/2 for i,j,v in terms),zero) for r in range(4) for c in range(4)])
        source=[[scalar(int(BP2[k,i,a]))/2-sum((v*X[j][a]/2 for ii,j,v in terms if ii==i),zero) for a in range(2)] for i in range(4)]
        hj.append([[sum((W[i][r]*source[i][a] for i in range(4)),zero) for a in range(2)] for r in range(4)])
        lq.append(sum((w[i]*w[j]*v/2 for i,j,v in terms),zero)-sum((w[i]*int(DS2[k,i]) for i in range(4)),zero))
        ljr.append([sum((X[i][a]*int(BP2[k,i,a]) for i in range(4)),zero)
                     -sum((X[i][a]*X[j][a]*v/2 for i,j,v in terms),zero)-int(SP[k,a]) for a in range(2)])
    derivative=[-one/(2*sqrt(scalar(n))) for n in counts]
    qgradient=[sum((lq[k]*derivative[k] for k in CTERMS[b]),zero) for b in range(20)]
    rgradient=[[sum((ljr[k][a]*derivative[k] for k in CTERMS[b]),zero) for b in range(20)] for a in range(2)]
    if coefficients is None:
        if rigorous:raise ValueError('rigorous evaluation requires explicit dyadic coefficients')
        coefficients=select_coefficients(qgradient,rgradient,U)
    if len(coefficients)!=2 or any(int(v)!=v or abs(int(v))>16*SCALE for v in coefficients):
        return {'certified':False,'reason':'COEFFICIENT_GUARD'}
    kappas=[scalar(int(v))/SCALE for v in coefficients]
    center=q+sum((kappas[a]*residual[a] for a in range(2)),zero)
    if lo(center)<=0:return {'certified':False,'reason':'NONPOSITIVE_CORRECTED_TIME'}
    l=[lq[k]+sum((kappas[a]*ljr[k][a] for a in range(2)),zero) for k in range(20)]
    lin=[sum((l[k]*derivative[k] for k in CTERMS[b]),zero) for b in range(20)]
    glin=[[sum((gb[k][j]*derivative[k] for k in CTERMS[b]),zero) for j in range(16)] for b in range(20)]
    hlin=[[[sum((hj[k][i][a]*derivative[k] for k in CTERMS[b]),zero) for a in range(2)] for i in range(4)] for b in range(20)]
    remainder=[scalar(R2*v)/(2*sqrt(scalar(n))*sq(sqrt(scalar(lw))+sqrt(scalar(n))))
               for v,lw,n in zip(variances,lower,counts)]
    def psd_bound(S):
        n=len(S);trace=sum((S[i][i] for i in range(n)),zero)
        frobenius=norm([S[i][j] for i in range(n) for j in range(n)])
        rows=[sum((abs(S[i][j]) for j in range(n)),zero) for i in range(n)]
        rowbound=scalar(max(hi(x) for x in rows))
        return min([trace,frobenius,rowbound],key=hi)
    SB=[[sum((scalar(U[b])*glin[b][4*k+i]*glin[b][4*k+j]
                    for b in range(20) for k in range(4)),zero) for j in range(4)] for i in range(4)]
    eps=sqrt(scalar(R2)*psd_bound(SB))+sum((remainder[k]*norm(gb[k]) for k in range(20)),zero)
    if hi(eps)>=1:return {'certified':False,'reason':'INVERSE_RADIUS','epsilon_upper':str(hi(eps))}
    # |K| = (K^2 + |det K| I) / sqrt(trace(K^2)+2|det K|).
    ka=kappas[0]-one;kc=kappas[1]-one
    det=Fraction(int(coefficients[0]),SCALE)-1
    det=det*(Fraction(int(coefficients[1]),SCALE)-1)-1
    ad=scalar(abs(det.numerator))/det.denominator
    denominator=sqrt(sq(ka)+sq(kc)+2+2*ad)
    floor=one/(2**40)
    M00=(sq(ka)+one+ad)/denominator+floor
    M11=(sq(kc)+one+ad)/denominator+floor
    M01=(ka+kc)/denominator
    R00=sqrt(M00);R10=M01/R00;R11=sqrt(M11-sq(R10))
    def weighted(h):
        out=[]
        for i in range(4):out.extend([h[i][0]*R00+h[i][1]*R10,h[i][1]*R11])
        return out
    hv=[weighted(h) for h in hlin];hr=[weighted(h) for h in hj]
    SH=[[sum((scalar(U[b])*hv[b][i]*hv[b][j] for b in range(20)),zero) for j in range(8)] for i in range(8)]
    H=sqrt(scalar(R2)*psd_bound(SH))+sum((remainder[k]*norm(hr[k]) for k in range(20)),zero)
    first=sqrt(scalar(R2)*sum((scalar(U[b])*sq(lin[b]) for b in range(20)),zero))
    first+=sum((remainder[k]*abs(l[k]) for k in range(20)),zero)
    bound=first+sq(H)/(one-eps)
    common={'coefficients':list(map(int,coefficients)),'coefficient_denominator':SCALE,'method':'geometric_constraints'}
    if rigorous:
        from intervals import DOWN,UP
        qlo=DOWN.subtract(center.lo,bound.hi);qhi=UP.add(center.hi,bound.hi)
        accepted=qlo>0 and DOWN.multiply(qlo,121)>=UP.multiply(center.hi,100) and UP.multiply(qhi,81)<=DOWN.multiply(center.lo,100)
        return {**common,'certified':bool(accepted),'reason':'CERTIFIED' if accepted else 'PRECISION_HOLD',
                'qhat_lower':str(center.lo),'qhat_upper':str(center.hi),'q_lower':str(max(0,qlo)),'q_upper':str(qhi),
                'raw_qhat_lower':str(q.lo),'raw_qhat_upper':str(q.hi),
                'error_bound_upper':str(bound.hi),'epsilon_upper':str(eps.hi)}
    qlo=max(0,center-bound);qhi=center+bound
    accepted=qlo>0 and qlo*121>=center*100 and qhi*81<=center*100
    result={**common,'certified':bool(accepted),'reason':'CANDIDATE' if accepted else 'PRECISION_HOLD',
            'qhat':center,'raw_qhat':q,'q_lower':qlo,'q_upper':qhi,'error_bound':bound,'epsilon_upper':eps}
    if diagnostics:result.update(gradient=lin,residuals=residual,first_bound=first,nonlinear_bound=sq(H)/(one-eps),H_bound=H)
    return result
