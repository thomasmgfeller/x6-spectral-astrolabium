"""Independent native-action and boundary checks at rational test centres."""
from fractions import Fraction as F
import json
from basisdaten import read, ROOT, SCALE
from antwort import LIVE


class Quad:
    """Exact a+b sqrt(rad); sign comparisons use rationals only."""
    rad=F(0)
    def __init__(self,a=0,b=0):
        self.a,self.b=F(a),F(b)
    def __add__(self,v):
        v=number(v);return Quad(self.a+v.a,self.b+v.b)
    __radd__=__add__
    def __neg__(self):return Quad(-self.a,-self.b)
    def __sub__(self,v):return self+-number(v)
    def __rsub__(self,v):return number(v)+-self
    def __mul__(self,v):
        v=number(v)
        return Quad(self.a*v.a+self.rad*self.b*v.b,self.a*v.b+self.b*v.a)
    __rmul__=__mul__
    def __truediv__(self,v):
        v=number(v);n=v.a*v.a-self.rad*v.b*v.b
        assert n
        g=self*Quad(v.a,-v.b);return Quad(g.a/n,g.b/n)
    def __rtruediv__(self,v):return number(v)/self
    def __bool__(self):return bool(self.a or self.b)
    def __eq__(self,v):
        v=number(v);return self.a==v.a and self.b==v.b
    def sign(self):
        if self.b==0:return (self.a>0)-(self.a<0)
        if self.b<0:return -(-self).sign()
        if self.a>=0:return 1
        test=self.b*self.b*self.rad-self.a*self.a
        return (test>0)-(test<0)


def number(q):return q if isinstance(q,Quad) else Quad(q)


def enclosed(q,interval):
    low,high=map(F,interval);x=number(q)
    return (x-low).sign()>=0 and (high-x).sign()>=0


def centre(v):return F(v.lo+v.hi,2*SCALE)


def solve(a,b):
    n=len(a);v=[list(row)+[t] for row,t in zip(a,b)]
    for j in range(n):
        k=next(i for i in range(j,n) if v[i][j])
        v[j],v[k]=v[k],v[j];pivot=v[j][j]
        v[j]=[x/pivot for x in v[j]]
        for i in range(n):
            if i!=j and v[i][j]:
                c=v[i][j]
                v[i]=[x-c*y for x,y in zip(v[i],v[j])]
    return [row[-1] for row in v]


def gradients(y,w,b):
    gy={i:0 for i in y};gw={i:19 for i in w}
    for (i,j),c in b.items():
        d=y[j]-y[i];g=2*c*w[j]*d
        gy[j]+=g;gy[i]-=g;gw[j]+=c*d*d
    return gy,gw


def energy(y,w,b):
    return 19*sum(w.values())+sum(v*w[j]*(y[j]-y[i])**2 for (i,j),v in b.items())


def finite_test(y,w,b,dataset):
    z,r=16,18
    gy,gw=gradients(y,w,b)
    # Derive changes of the two D-rows by sampling their exact monic/linear polynomials.
    J=F(dataset['source_w'])
    slope=gradients({**y,z:y[z]+1},w,b)[1][z]-gw[z]
    d=J/slope
    def polynomial(t):
        return gradients({**y,z:y[z]+d,r:y[r]+t},w,b)[1][r]-gw[r]
    C=polynomial(0);B=(polynomial(1)-polynomial(-1))/4
    A=(polynomial(1)+polynomial(-1)-2*C)/2
    assert A==1 and B<0
    Quad.rad=B*B-C
    assert Quad.rad>0
    from math import isqrt
    assert (isqrt(Quad.rad.numerator)**2!=Quad.rad.numerator or
            isqrt(Quad.rad.denominator)**2!=Quad.rad.denominator)
    dt=Quad(-B,-1)
    assert (dt*dt+2*B*dt+C)==0
    # Unknowns: two endpoint weights and six future moments. Site 7 stays fixed.
    def state(x):
        ww=w.copy();yy={**y,z:y[z]+d,r:y[r]+dt}
        ww[z]+=x[0];ww[r]+=x[1]
        for n,j in enumerate([8,9,10]):
            ww[j]+=x[2+2*n]
            yy[j]=(w[j]*y[j]+x[3+2*n])/ww[j]
        return yy,ww
    def equations(x):
        yy,ww=state(x)
        ny,_=gradients(yy,ww,b)
        g=[ny[i]-gy[i] for i in (11,12,13,14,15,17,18)]
        if dataset['construction']=='pure':g.append(ny[z]-gy[z])
        else:g.append(sum(ny[i]-gy[i] for i in (0,1,2,3)))
        return g
    zero=[Quad() for _ in range(8)]
    start=equations(zero)
    cols=[]
    for k in range(8):
        trial=zero.copy();trial[k]=Quad(1)
        cols.append([v-r0 for v,r0 in zip(equations(trial),start)])
    root=solve(list(zip(*cols)),[-q for q in start])
    yy,ww=state(root);ny,nw=gradients(yy,ww,b)
    assert all(a==0 for a in equations(root))
    for j in (4,5,6,11,12,13,14,15,17,18):assert ny[j]-gy[j]==0
    for j in (4,5,6,11,12,13,14,16,18):assert nw[j]-gw[j]==(J if j==z else 0)
    assert enclosed(ny[z]-gy[z],dataset['source_Y'])
    delta_p=[-(ny[i]-gy[i])/2 for i in (0,1,2,3)]
    assert all(enclosed(q,iv) for q,iv in zip(delta_p,dataset['delta_boundary_momenta']))
    if dataset['construction']=='pure':assert ny[z]==gy[z] and sum(delta_p)!=0
    else:assert sum(delta_p)==0 and ny[z]!=gy[z]
    for key,item in dataset['future_and_endpoints'].items():
        j=int(key)
        for q,k in [(yy[j]-y[j],'dY'),(ww[j]-w[j],'dw'),(ww[j]*yy[j]-w[j]*y[j],'dM')]:
            assert enclosed(q,item[k])
    assert all(number(yy[j]-yy[i]).sign()>0 for i,j in b)
    return True


def audit():
    yb,wb,rel,edges,e,windows=read()
    y={k:centre(v) for k,v in yb.items()};w={k:centre(v) for k,v in wb.items()}
    pred={i:{k for k,j in rel if j==i} for i in y}
    succ={i:{k for j,k in rel if j==i} for i in y}
    b={(i,j):{0:1,1:-9,2:16,3:-8}.get(len(succ[i]&pred[j]),0) for i,j in rel}
    assert b==edges
    anchor=json.loads((ROOT/'Dirichlet.json').read_bytes())
    boundary=json.loads((ROOT/'Anfangsdaten.json').read_bytes())
    def shifted(updates):
        yy=y.copy();ww=w.copy()
        for i,size in updates:
            k,j=LIVE[i];(yy if k=='Y' else ww)[j]+=size
        return energy(yy,ww,b)
    mat=[]
    for i in range(6):
        row=[]
        for j in range(6):
            value=sum(a*c*shifted([(i,a),(j,c)]) for a in (-1,1) for c in (-1,1))/4
            assert enclosed(value,anchor['H'][i][j])
            row.append(value)
        mat.append(row)
    for j,label in enumerate(anchor['coordinates']):
        response=solve(mat,[F(k==j) for k in range(6)])
        for i,target in enumerate(anchor['coordinates']):
            assert enclosed(response[i],anchor['inverse'][target][label])
    for dataset in boundary['finite']:assert finite_test(y,w,b,dataset)
    # Check the full homogeneous neighbour (all 20 first derivatives, all initial momenta).
    gy,gw=gradients(y,w,b)
    for strength,record in boundary['zero_source_free_future'].items():
        yp,wp=y.copy(),w.copy()
        for j,n in zip((7,8,9,10),map(F,('1','2','23/8','29/8'))):
            d=F(strength)*n;wp[j]+=d;yp[j]=(w[j]*y[j]+y[6]*d)/wp[j]
            assert enclosed(yp[j]-y[j],record[str(j)]['dY'])
        a,d=gradients(yp,wp,b)
        assert all(a[i]==gy[i] for i in set(y)-{7,8,9,10})
        assert all(d[i]==gw[i] for i in (4,5,6,11,12,13,14,16,18))
    return {'exact_quadratic_field_controls':len(boundary['finite']),'native_equations_per_control':20,
            'hessian_entries':36,'response_entries':36,'homogeneous_finite_witnesses':2}


if __name__=='__main__':print(json.dumps(audit(),sort_keys=True,indent=2))
