"""Exact positive-density integration, tensor GL contractions and analytic tails."""
from itertools import product
from flint import arb,acb
from inputs import core as pc

class Quadrature:
    def __init__(self,n):
        self.n=n
        rules=[arb.legendre_p_root(n,k,weight=True) for k in range(n)]
        self.t=[x for x,w in rules];self.w=[w/2 for x,w in rules]
        assert all(w>0 for w in self.w) and sum(self.w).contains(1)
        self.dd=[[(x-y)*(x-y)*pc.beta()/4 for y in self.t] for x in self.t]
        self.cache={};self.evaluations=0

    def output(self,coefficients,indices):
        items=tuple(sorted((c,i) for c,i in zip(coefficients,indices) if c))
        mirror=tuple(sorted((c,self.n-1-i) for c,i in items));key=min(items,mirror)
        if key not in self.cache:
            value=acb(0)
            for l,w in enumerate(self.w):
                k=arb(1)/2+sum(c*self.dd[l][i] for c,i in key)
                value+=w*pc.E(k)
            self.evaluations+=self.n
            if not value.is_finite():raise ArithmeticError('invalid output-clock integral')
            self.cache[key]=value
        return self.cache[key]

    def single_masks(self,code):
        terms=pc.pair_coefficients(code);pred=[i for i,j,c in terms if j==2]
        outs=[[next((c for i,j,c in terms if i==a and j==x),0) for a in (0,1,2)] for x in (3,4)]
        values=[acb(0),acb(0),acb(0)]
        for i,wi in enumerate(self.w):
            for j,wj in enumerate(self.w):
                for k,wk in enumerate(self.w):
                    inds=(i,j,k);k2=arb(1)/2+sum(self.dd[k][inds[a]] for a in pred)
                    f=self.output(outs[0],inds);g=self.output(outs[1],inds)
                    common=wi*wj*wk*(1+pc.E(k2))/16
                    for a,v in enumerate((f,g,f*g)):values[a]+=common*v
        # Each mask has analytic majorant 1/8 exp(exponent*W_j).
        degrees=[sum(abs(c) for i,j,c in terms if v in (i,j)) for v in range(5)]
        error=ellipse_tail(self.n,degrees,2,arb(1)/8)
        return values,error

    def chain(self,length):
        if not 2<=length<=4:raise ValueError('declared chain lengths are 2..4')
        values=[acb(0),acb(0)];coeff=(1,-9,16,-8)
        def walk(indices,weight):
            j=len(indices)
            if j==length-1:
                f=self.output([coeff[j-i-1] for i in range(j)],indices)
                values[0]+=weight;values[1]+=weight*f
                return
            for k,w in enumerate(self.w):
                value=arb(1)/2+sum(coeff[j-i-1]*self.dd[k][v] for i,v in enumerate(indices))
                walk(indices+(k,),weight*w*(1+pc.E(value))/2)
        for k,w in enumerate(self.w):walk((k,),acb(w))
        degrees=[sum(abs(coeff[abs(j-i)-1]) for j in range(length) if j!=i) for i in range(length)]
        error=ellipse_tail(self.n,degrees,arb(3)/2,arb(1))
        return values,error

def ellipse_tail(n,degrees,rho,majorant):
    r=arb(rho);a=(r+1/r)/2;b=(r-1/r)/2
    exponent=pc.beta()*b*(a+1)/2
    return 4*majorant*r**(-2*n)/(1-1/r)*sum((exponent*d).exp() for d in degrees)

def chain_pair_dust(first,second,coefficients):
    (a,ea),(b,eb)=first,second
    products=((a[1],b[0]),(a[0],b[1]),(a[1],b[1]))
    value=sum(c*x*y for c,(x,y) in zip(coefficients,products))/8
    error=sum(abs(c)*(ea*abs(y)+eb*abs(x)+ea*eb) for c,(x,y) in zip(coefficients,products))/8
    return value,error
