"""Exact disjoint radial/time cells covering ALL finite exterior source support."""
from fractions import Fraction as F
import itertools,math
from flint import arb
from common import ball,require

def eval_line(line,t):return line[0]*t+line[1]
def cube_integral(line,l,u):
    a,b=line
    return sum(F(math.comb(3,j))*a**j*b**(3-j)*(u**(j+1)-l**(j+1))/F(j+1) for j in range(4))
def clipped(t0,t1,r0,r1,kind):
    lower=[(F(0),r0),(F(0),F(0)),(F(-1),F(4))]
    upper=[(F(0),r1),(F(1),F(1,2) if kind=='front' else F(-1,2))]
    if kind=='front':lower.append((F(1),F(-1,2)))
    lines=lower+upper;cuts={t0,t1}
    for a,b in itertools.combinations(lines,2):
        if a[0]!=b[0]:
            t=(b[1]-a[1])/(a[0]-b[0])
            if t0<t<t1:cuts.add(t)
    cuts=sorted(cuts);segments=[];vol=F(0)
    for l,u in zip(cuts,cuts[1:]):
        m=(l+u)/2;lo=max(lower,key=lambda v:eval_line(v,m));hi=min(upper,key=lambda v:eval_line(v,m))
        if eval_line(lo,m)>=eval_line(hi,m):continue
        v=F(4,3)*(cube_integral(hi,l,u)-cube_integral(lo,l,u))
        require(v>0,'positive exact cell measure')
        segments.append((l,u,lo,hi));vol+=v
    if not segments:return None
    rs=[eval_line(edge,t) for l,u,lo,hi in segments for edge in [lo,hi] for t in [l,u]]
    return {'kind':kind,'tau0':segments[0][0],'tau1':segments[-1][1],
            'r0':min(rs),'r1':max(rs),'volume_over_pi':vol,'segments':segments}
def cells(n):
    out=[]
    for i in range(int(F(13,4)*n)):
        t0=F(7,4)+F(i,n);t1=t0+F(1,n)
        for j in range(int(F(11,2)*n)):
            for kind in ['deep','front']:
                c=clipped(t0,t1,F(j,n),F(j+1,n),kind)
                if c is not None:c['index']=[i,j,kind];out.append(c)
    return out
def exact_volume():
    return F(4,3)*(cube_integral((F(1),F(1,2)),F(7,4),F(5))-cube_integral((F(-1),F(4)),F(7,4),F(4)))
def detector_bins(nr=16,nt=8):
    def primitive(r):return -r**4+4*r**3-4*r*r
    mass=[primitive(F(1)+F(j+1,nr))-primitive(F(1)+F(j,nr)) for j in range(nr)]
    require(sum(mass)==1 and all(x>0 for x in mass),'exact normalized detector radial mass')
    out=[]
    for wi in range(2):
        lo=F(3+wi,4);rows=[]
        for k in range(nt):
            for j in range(nr):rows.append({'r0':F(1)+F(j,nr),'r1':F(1)+F(j+1,nr),'t_hi':lo+F(k+1,4*nt),'mass':mass[j]/nt})
        require(sum(x['mass'] for x in rows)==1,'complete normalized detector')
        out.append(rows)
    return out
def causal_cap(c,rp,t_end):
    """Supremum cap fraction over one root cell and a ball of endpoint radii."""
    D=ball(c['tau1'])+1+arb(t_end)
    if D.upper()<=0:return arb(0)
    if c['r0']==0 or rp.lower()<=0:return arb(1)
    R=ball(c['r0']).union(ball(c['r1']))
    delta=R-rp
    # python-flint 0.8.0 generic power may be nonfinite for a ball crossing 0.
    # Multiplication plus the exact nonnegative-square range is an enclosure.
    square=delta*delta
    square=max(arb(0),square.lower()).union(max(arb(0),square.upper()))
    q=(D*D-square)/(4*R*rp)
    require(q.is_finite(),'finite angular cap')
    return min(arb(1),max(arb(0),q.upper()))
