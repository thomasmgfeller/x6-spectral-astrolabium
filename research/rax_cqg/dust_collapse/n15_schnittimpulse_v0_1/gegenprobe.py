"""Independent unexpanded quadratic action, exact symmetric sources and round trips."""
import json
from fractions import Fraction as Q
from math import isqrt
from random import Random

from basis import density_translation_375841 as ref
from rueckrechnung import initial_readout

P,I,F=ref.PAST,ref.INNER,ref.FUTURE
REL,CHAINS,_=ref.local_geometry()
EDGES=[]
for i,j in sorted(REL):
    size=len({v for v in range(15) if (i,v) in REL and (v,j) in REL})
    if size<4:
        EDGES.append((i,j,(1,-9,16,-8)[size]))
SEAM=(5,11)
CUT=P+(4,5,6,11)
NAMES=('pr340','pr341','gegenpaar','ohne_gesamtinformation')


def action(y,w):
    return -(sum(w)+sum(b*w[j]*(y[i]-y[j])**2 for i,j,b in EDGES)/19)/2


def perturb(y,vertices,step):
    return [t+step if i in vertices else t for i,t in enumerate(y)]


def response(y,w,vertices,h=Q(1,128)):
    up,low=(action(perturb(y,vertices,sign*h),w) for sign in (1,-1))
    return (up-low)/(2*h),(up+low-2*action(y,w))/h**2


def sample(rng,mode,center=False,broad=False):
    def noise(r):
        return 0 if center else r*Q(rng.randint(-997,997),1000)
    e=Q(-1,4)+noise(ref.RADIUS)
    u={v:ref.CENTER[v]+noise(ref.RADIUS) for v in I}
    if mode in NAMES[2:]:
        u[4]+=Q(1,128)
        u[6]-=Q(1,128)
    if broad:
        e=rng.choice([-1,1])*Q(1,4)+noise(Q(1,128))
        u={v:ref.CENTER[v]+noise(Q(1,64)) for v in I}
    y=[Q(0)]*15
    for v in P+F: y[v]=Q(v-5)
    for v in F[1:]: y[v]+=noise(Q(1,2**20))
    y[3]+=e
    for v in I: y[v]=-2+e+(4-e)*u[v]
    f=dict.fromkeys(I,Q(0))
    for chain in CHAINS:
        ends=[0]+[(u[i]+u[j])/2 for i,j in zip(chain,chain[1:])]+[1]
        for v,left,right in zip(chain,ends,ends[1:]):
            f[v]+=(right-left)/len(CHAINS)
    c={v:1+sum(b*(y[i]-y[j])**2 for i,j,b in EDGES if j==v)/19 for v in I}
    d=dict.fromkeys(I,Q(0))
    if mode in NAMES[:2]:
        a,b,g=(5,12,13) if mode=='pr340' else (4,12,13)
        for i,j,k in ((a,b,g),(b,g,a),(g,a,b)):
            d[i]=-ref.COFACTOR_SCALE*(c[j]-c[k])
    elif mode=='gegenpaar':
        # Solve the three constraints by elimination, independently of the
        # cofactor expressions in the cell proof. d13 is the free scale.
        d[13]=(y[12]-y[11])*(c[4]-c[6])/10000
        d[12]=9*(y[11]-y[13])*d[13]/(y[11]-y[12])
        d[4]=-((c[12]-c[6])*d[12]+(c[13]-c[6])*d[13])/(c[4]-c[6])
        d[6]=-sum(d.values())
    elif mode=='ohne_gesamtinformation':
        d[4]=c[6]/64
        d[6]=-c[4]/64
    x={v:f[v]+noise(f[v]/200 if broad else ref.RADIUS) for v in I}
    if mode in NAMES[2:]:
        x[12]+=Q(1,8320)
        x[13]-=Q(1,8320)
    n=10**18
    lo=isqrt(isqrt(3*n**4//722))
    dlo,dhi=Q(lo,n),Q(lo+1,n)
    w=[Q(1,8)/dlo]*15
    for v in F:
        w[v]+=noise(Q(1,2**21))
        assert Q(1,8)-Q(1,2**20)<dlo*w[v]<=dhi*w[v]<Q(1,8)+Q(1,2**20)
    for v in P: assert Q(3,32)<w[v]*dlo<=w[v]*dhi<Q(5,32)
    branches=[]
    for sgn in (1,-1):
        frame=w.copy()
        for v in I:
            value=x[v]+sgn*d[v]
            assert f[v]*Q(99,100)<value<f[v]*Q(101,100)
            frame[v]=(4-e)*value/4
        branches.append(frame)
    return y,branches


def observe(y,w):
    e5,h5=response(y,w,(5,))
    e11,h11=response(y,w,(11,))
    p=-response(y,w,P)[0]
    cut_flux=-response(y,w,CUT)[0]
    known={j:w[j] for j in SEAM+F}
    amount=sum(w[v] for v in I)
    additional={'curvature11':h11}, {'cut_current':cut_flux}
    for option in additional:
        val,reconstructed=initial_readout(y,known,amount,e5,e11,**option)
        assert val==p
        assert reconstructed==(w[4]+w[6],w[12],w[13],w[14])
    return p,(e5,e11),(h5,h11),cut_flux


def verify():
    rng=Random(37673)
    counts={}
    centers={}
    sham_errors=0
    for name in NAMES:
        for i in range(25):
            y,(left,right)=sample(rng,name,center=i==0)
            a,b=observe(y,left),observe(y,right)
            assert a[0]>0>b[0]
            assert action(y,left)==action(y,right)
            if name in NAMES[:2]:
                assert a[1]!=b[1]
            else:
                assert a[1]==b[1] and all(left[s]==right[s] for s in SEAM)
            if name=='gegenpaar':
                assert sum(left)==sum(right) and a[2][1]!=b[2][1]
                assert a[3]!=b[3]
                # A finite seam translation checks the actual quadratic
                # coefficient at fixed paired fields. The slope cancels.
                h=Q(1,64)
                shifted=perturb(y,[11],h)
                assert action(shifted,left)-action(shifted,right)==h*h*(a[2][1]-b[2][1])/2
            if name=='ohne_gesamtinformation':
                assert sum(left)!=sum(right) and a[2:]==b[2:]
                yy=perturb(perturb(y,[5],Q(1,17)),[11],-Q(1,28))
                for s in F: yy[s]+=Q(s-6,35)
                wl,wr=left.copy(),right.copy()
                for s in SEAM+F: wl[s]=wr[s]=left[s]*Q(1001,1000)
                assert action(yy,wl)==action(yy,wr)
                known={j:right[j] for j in SEAM+F}
                fake=initial_readout(y,known,sum(left[v] for v in I),*b[1],curvature11=b[2][1])[0]
                assert fake==a[0] and fake!=b[0]
                sham_errors+=1
            if i==0:
                centers[name]={'p':[str(a[0]),str(b[0])],
                               'delta_E':[str(x-z) for x,z in zip(a[1],b[1])],
                               'delta_Delta_H11':str(a[2][1]-b[2][1])}
        counts[name]=25
    # Fresh clocks and densities from the broader preparation. No sign labels
    # are used when acquiring source responses or calling the inverse.
    for _ in range(32):
        y,(w,_)=sample(rng,'allgemein',broad=True)
        observe(y,w)
    return {'rationale_paketpaare':counts,'weitere_feldbelegungen':32,
            'rueckrechnungen_je_weg_exakt':2*sum(counts.values())+32,
            'falsches_vorzeichen_bei_vertauschter_summe':sham_errors,'zentren':centers}

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Ohne -O ausführen.')
    print(json.dumps(verify(),indent=2,ensure_ascii=False))
