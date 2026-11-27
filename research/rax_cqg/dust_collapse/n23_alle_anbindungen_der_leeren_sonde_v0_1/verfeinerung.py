"""Additional interval consequences used inside the subdivided searches."""
from intervall import I, S, Empty, point
from filter import Z, FREE, intersect
from ordnungen import COLLAR, EMPTY

def moments(eq,center,y):
    # Compute sum k*(x-y_i)^2 as a polynomial about center.
    a=point(sum(k for i,k,_ in eq))
    b=2*sum((c*(center-y[i]) for i,k,c in eq),Z)
    d=sum((c*(center-y[i]).sq() for i,k,c in eq),Z)
    return a,b,d

def extra(model,y,w):
    for j,i in ((16,15),(18,17),(18,20),(21,20),(21,17)):
        eq=model.inc[j]
        r=next((k for n,k,c in eq if n==i),0)
        if not r:continue
        mid=I((y[j].l+y[j].h)//2,(y[j].l+y[j].h)//2)
        a,b,d=moments([(n,k,c) for n,k,c in eq if n!=i],mid,y)
        x=y[j]-mid
        gap=(-(19+d+x*(b+a*x))/point(r)).sqrt()
        intersect(y,i,y[j]-gap)
        intersect(y,j,y[i]+gap)

    for i,k,c in model.inc[21]:
        A=model.terminal_sum
        B=A-k
        if i in COLLAR or not B:continue
        rest=[(n,u,v) for n,u,v in model.inc[21] if n!=i]
        center=I((y[i].l+y[i].h)//2,(y[i].l+y[i].h)//2)
        m=sum((point(u/B)*(y[n]-center) for n,u,v in rest),Z)
        variance=sum((v*(y[n]-center).sq() for n,u,v in rest),Z)-point(B)*m.sq()
        offset=(-(19+variance)/point(k*B/A)).sqrt()
        if B/A>0:offset=-offset
        intersect(y,i,center+m+offset)
        intersect(y,21,center+m+point(k/A)*offset)

    for i in FREE:
        out=model.out[i]
        inc=model.inc[i] if i not in EMPTY else []
        s=sum((v*w[j] for j,k,v in out),Z)+point(sum(k for j,k,v in inc))*w[i]
        if s.l<=0<=s.h:continue
        # Recenter near the current clock to bound cancellation in the affine equation.
        mid=I((y[i].l+y[i].h)//2,(y[i].l+y[i].h)//2)
        val=sum((v*w[j]*(y[j]-mid) for j,k,v in out),Z)
        val+=w[i]*sum((v*(y[j]-mid) for j,k,v in inc),Z)
        intersect(y,i,mid+val/s)

    for i,j in ((17,20),(20,22),(17,22)):
        ci={n:k for n,k,v in model.out[i]}
        cj={n:k for n,k,v in model.out[j]}
        s=sum((point(k)*w[n] for n,k in ci.items()),Z)
        if s.l<=0<=s.h:continue
        delta=sum((point(ci.get(n,0)-cj.get(n,0))*w[n]*(y[n]-y[j])
                   for n in sorted(ci.keys()|cj.keys()) if ci.get(n,0)!=cj.get(n,0)),Z)/s
        # G_i-G_j=0 implies Y_i-Y_j=delta.
        intersect(y,i,y[j]+delta)
        intersect(y,j,y[i]-delta)

def refine(model,y,w):
    for k in range(3):
        extra(model,y,w)
        model.contract(y,w,2)

def split(y,w,key):
    source=w if key>=100 else y
    j=key-100 if key>=100 else key
    intervals=source[j].halves()
    for interval in intervals:
        Y,W=y.copy(),w.copy()
        (W if key>=100 else Y)[j]=interval
        yield Y,W
