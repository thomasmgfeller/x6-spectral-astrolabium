"""Exact differences of the stationary equations and secants of native boundary preparations."""
from fractions import Fraction as F

def action_jacobian(proposal,coeff,free,source):
    from feldroehre import POS,jacobian
    from quelle import box
    y=list(map(F,proposal['y']));w=list(map(F,proposal['w']))
    def grad(y,w):
        # Differentiate edge energies with respect to each individual free variable.
        density=[19-(source if j==16 else 0)+sum(c*(y[b]-y[a])**2
                 for (a,b),c in coeff.items() if b==j) for j in POS]
        clocks=[sum(c*w[b]*(y[b]-y[a])*(int(j==a)-int(j==b))
                    for (a,b),c in coeff.items() if j==a or j==b) for j in free]
        return density+clocks
    h=F(1,1000)
    jac=jacobian(list(map(box,y)),list(map(box,w)),coeff,free)
    axes=[('y',j) for j in free]+[('w',j) for j in POS]
    checked=0
    for idx,(kind,j) in enumerate(axes):
        yp,ym,wp,wm=y.copy(),y.copy(),w.copy(),w.copy()
        plus,minus=(yp,ym) if kind=='y' else (wp,wm)
        plus[j]+=h;minus[j]-=h
        p,m=grad(yp,wp),grad(ym,wm)
        for i,(a,b) in enumerate(zip(p,m)):
            exact=(a-b)/(2*h)
            l,r=map(F,jac[i][idx].data())
            assert l<=exact<=r
            checked+=1
    return checked

def collar_secants(source,checks,y,w,functions):
    from ableitung import prepare
    from feldroehre import COLLAR
    n=0
    for (a,ca),(b,cb) in zip(checks,checks[1:]):
        yy,ww=prepare(y,w,a,b,source,functions)
        for idx,field in enumerate((yy,ww)):
            for j in COLLAR:
                ul,ur=map(F,ca[str(j)][idx]);vl,vr=map(F,cb[str(j)][idx])
                sl,sr=(vl-ur)/(b-a),(vr-ul)/(b-a)
                lo,hi=map(F,field[j].d.data())
                assert max(sl,lo)<=min(sr,hi)
                n+=1
    return n
