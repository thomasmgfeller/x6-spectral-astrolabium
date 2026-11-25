"""Independent finite quadratures of all fifty action pairs, in rank order."""
import cmath
from itertools import product
from math import cos, sin, sqrt, prod
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent/'basis'/'basis'))
from kontrollrechnung import D,R,CENTER,PAIRS,clocks,fields,coefficients,points,sinc

ETA=2**-20
T=1/(32*sqrt(D))
END=(2.,3.,4.,5.)


def quadrature(n):
    if n==2:return [(-1/sqrt(3),.5),(1/sqrt(3),.5)]
    return [(-sqrt(.6),5/18),(0.,4/9),(sqrt(.6),5/18)]


def tensor(rule,n):
    for row in product(rule,repeat=n):
        yield tuple(p[0] for p in row),prod(p[1] for p in row)


def expm1i(x):
    return complex(-2*sin(x/2)**2,sin(x))


def profile(u):
    return [-5.,-4.,-3.,-1.75]+[-1.75+3.75*v for v in u]+list(END)


def slopes(u,ref):
    # Start with two independently evaluated fifty-term actions at the
    # center. Their difference is affine in the target clock for C_j.
    y=profile(u)
    reference=profile(ref)
    c=coefficients(y)
    c0=coefficients(reference)
    beta=[c[j]-c0[j] for j in range(11,15)]
    v=[]
    for j,b in enumerate(beta,11):
        p=y.copy();q=reference.copy()
        p[j]+=1;q[j]+=1
        v.append(coefficients(p)[j]-coefficients(q)[j]-b)
    return tuple(beta),tuple(v)


def prepare(kind,w0,side,nu):
    ref=[k/8 for k in range(1,8)]
    arms=[[],[]]
    for arm in range(2):
        for lobe in (-1,1):
            for uv in points(nu,6):
                y4=CENTER+R*uv[0]+(T*arm if kind=='single' else 0)
                u=clocks(lobe,uv,y4)
                _,v,_,qs,f=fields(u,list(END))
                if arm and kind=='collective':
                    u=[x+(-1)**k*T/3.75 for k,x in enumerate(u)]
                c=coefficients(profile(u))
                x=f.copy()
                for j,z in enumerate(v,4):x[j]+=side*(-1.25/2**14)*z/qs
                phase=D*sum(a*b for a,b in zip(c[4:11],x))+w0*sum(c[11:])
                # The inlet amplitude is common and cancels. The seven
                # independent top-hat density jitters are integrated exactly.
                a=cmath.exp(1j*phase)*prod(sinc(D*z/2**20) for z in c[4:11])/(4*nu)
                arms[arm].append((a,*slopes(u,ref)))
    return arms


def trace(arms,kind,rule,w0,width):
    samples=[]
    norm=[sum(a[0] for a in arm) for arm in arms]
    probs=[[row[0]/total for row in arm] for arm,total in zip(arms,norm)]
    for zn,weight in tensor(rule,7):
        k=[0.]+[ETA*x for x in zn[:3]]
        h=[width*x for x in zn[3:]]
        def deviations(arm):
            return [expm1i(sum(bj*hj+vj*kj*(w0+hj) for bj,vj,kj,hj in zip(b,v,k,h)))
                    for _,b,v in arm]
        l=deviations(arms[0])
        left=1+sum(p*x for p,x in zip(probs[0],l))
        if kind=='single':
            diff=sum((r-p)*x for r,p,x in zip(probs[1],probs[0],l))
        else:
            right=deviations(arms[1])
            diff=sum(r*x-p*y for r,p,x,y in zip(probs[1],probs[0],right,l))
        samples.append((weight,left,diff))
    ll=sum(w*abs(l)**2 for w,l,d in samples)
    proj=sum(w*l.conjugate()*d for w,l,d in samples)/ll
    rr=sum(w*abs(l+d)**2 for w,l,d in samples)
    return sqrt(sum(w*abs(d-proj*l)**2 for w,l,d in samples)/rr)


def measured_matrix(arms,rule,w0,widths):
    half=[((p+1)/2,w) for p,w in rule]
    diag=[0.,0.,0.]
    cross=[0j,0j,0j]
    for coords,wk in tensor(rule,3):
        k=(0.,*(t*ETA for t in coords))
        rows=[]
        for ix,arm in enumerate(arms):
            for a,b,v in arm:
                a=a*cmath.exp(1j*w0*sum(vj*kj for vj,kj in zip(v,k)))
                rows.append((ix,a,tuple(bj+vj*kj for bj,vj,kj in zip(b,v,k))))
        for i,(bi,ai,ci) in enumerate(rows):
            for j in range(i+1):
                bj,aj,cj=rows[j]
                factor=aj.conjugate()*ai*wk
                x=[w*(bb-aa) for w,aa,bb in zip(widths,cj,ci)]
                cs=[sum(w*cos(y*t) for t,w in half) for y in x]
                ss=[sum(w*sin(y*t) for t,w in half) for y in x[1:3]]
                for l,term in enumerate((prod(cs),1j*cs[0]*ss[0]*cs[2]*cs[3],
                                          -cs[0]*cs[3]*ss[0]*ss[1])):
                    value=factor*term
                    if bi==bj:
                        diag[l]+=value.real*(.5 if i==j else 1)
                    else:
                        cross[l]+=value
    return [[d,c.real,-c.imag] for d,c in zip(diag,cross)]


def joint(matrix):
    d,c,_=matrix[0]
    ds,cs,_=matrix[2]
    return (cs-ds*c/d)/(2*(d+c))


def count_events(arms,rule,w0,widths,gamma):
    # Direct Born counting on the positive and negative halves, with sign
    # tests on w8, w9 only. Keep unnormalized rates until the very end.
    half=[(s*(x+1)/2,w/2) for s in (-1,1) for x,w in rule]
    moments=[0.,0.,0.]
    for coords,wk in tensor(rule,3):
        k=(0.,*(t*ETA for t in coords))
        rows=[[(a*cmath.exp(1j*w0*sum(vj*kj for vj,kj in zip(v,k))),
                 tuple(bj+vj*kj for bj,vj,kj in zip(b,v,k))) for a,b,v in arm] for arm in arms]
        for quad in product(rule,half,half,rule):
            h=[w*q[0] for w,q in zip(widths,quad)]
            z=[sum(a*cmath.exp(1j*sum(v*t for v,t in zip(b,h))) for a,b in rr) for rr in rows]
            l,r=z
            prob=.73*((abs(l)**2+abs(r)**2)/2+(gamma*l.conjugate()*r).real)
            w=wk*prod(q[1] for q in quad)
            sig=1 if h[1]>0 else -1
            for j,sgn in enumerate((1,sig,sig*(1 if h[2]>0 else -1))):
                moments[j]+=w*sgn*prob
    return [v/moments[0] for v in moments[1:]]


def recover(matrix,moments):
    rows=[[v-m*c for v,c in zip(row,matrix[0])] for row,m in zip(matrix[1:],moments)]
    (u,b,c),(v,e,f)=rows
    return complex((c*v-f*u)/(b*f-e*c),(e*u-b*v)/(b*f-e*c))


def run():
    assert len(PAIRS)==50
    out={}
    for kind in ('single','collective'):
        out[kind]={}
        cases=[('published',.125,[ETA]*4),('wide_control',.5,[.5]*4)]
        if kind=='collective':cases.append(('same_center_8_9',.125,[ETA,.125,.125,ETA]))
        for name,w0,widths in cases:
            out[kind][name]={}
            for side in (-1,1):
                rows=[]
                for n,nu in [(2,2),(3,3)]:
                    rule=quadrature(n)
                    arms=prepare(kind,w0,side,nu)
                    row={'nodes_per_output':n}
                    if name!='same_center_8_9':
                        row['trace']=trace(arms,kind,rule,w0,widths[0])
                    if kind=='collective':
                        mat=measured_matrix(arms,rule,w0,widths)
                        row['joint_difference']=joint(mat)
                        row['tomography_matrix']=mat
                        if n==3 and name!='published':
                            observed=count_events(arms,quadrature(2),w0,widths,complex(.37,-.42))
                            estimate=recover(mat,observed)
                            row['direct_count_moments']=observed
                            row['recovered_gamma']=[estimate.real,estimate.imag]
                    rows.append(row)
                out[kind][name][str(side)]=rows
    return out


if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2,sort_keys=True))
