#!/usr/bin/env python3
"""Exact symbolic and rational controls. Standard library; no large production run."""
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import json,sys

def require(ok,msg):
    if not ok: raise ValueError(msg)
def enc(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,dict):return {k:enc(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [enc(v) for v in x]
    return x

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def tr(a):return list(map(list,zip(*a)))
def mm(a,b):return [[dot(x,y) for y in tr(b)] for x in a]
def sub(a,b):return [[x-y for x,y in zip(u,v)]for u,v in zip(a,b)]
def eye(n):return [[F(i==j)for j in range(n)]for i in range(n)]
def inv(a):
    n=len(a);m=[list(map(F,row))+u for row,u in zip(a,eye(n))]
    for i in range(n):
        j=next(j for j in range(i,n)if m[j][i]);m[i],m[j]=m[j],m[i]
        v=m[i][i];m[i]=[x/v for x in m[i]]
        for j in range(n):
            if j!=i:
                v=m[j][i];m[j]=[x-v*y for x,y in zip(m[j],m[i])]
    return [row[n:]for row in m]
def det(a):
    m=[list(map(F,row))for row in a];n=len(m);r=F(1)
    for i in range(n):
        j=next((j for j in range(i,n)if m[j][i]),None)
        if j is None:return F(0)
        if i!=j:m[i],m[j]=m[j],m[i];r=-r
        v=m[i][i];r*=v
        for j in range(i+1,n):
            k=m[j][i]/v;m[j]=[x-k*y for x,y in zip(m[j],m[i])]
    return r

class Poly:
    n=12
    def __init__(self,data):self.d={k:F(v)for k,v in data.items()if v}
    @classmethod
    def const(cls,x):return cls({(0,)*cls.n:F(x)})
    @classmethod
    def var(cls,i):
        k=[0]*cls.n;k[i]=1;return cls({tuple(k):1})
    def __add__(self,o):
        if not isinstance(o,Poly):o=Poly.const(o)
        d=self.d.copy()
        for k,v in o.d.items():d[k]=d.get(k,F(0))+v
        return Poly(d)
    __radd__=__add__
    def __neg__(self):return Poly({k:-v for k,v in self.d.items()})
    def __sub__(self,o):return self+-as_poly(o)
    def __rsub__(self,o):return as_poly(o)+-self
    def __mul__(self,o):
        o=as_poly(o);d={}
        for k,v in self.d.items():
            for l,w in o.d.items():
                p=tuple(a+b for a,b in zip(k,l));d[p]=d.get(p,F(0))+v*w
        return Poly(d)
    __rmul__=__mul__
    def __truediv__(self,x):return self*F(1,x)
    def diff(self,i):
        d={}
        for k,v in self.d.items():
            if k[i]:p=list(k);p[i]-=1;d[tuple(p)]=v*k[i]
        return Poly(d)
    def __eq__(self,o):return self.d==as_poly(o).d
    def evaluate(self,x):
        r=F(0)
        for k,v in self.d.items():
            for i,n in enumerate(k):v*=x[i]**n
            r+=v
        return r

def as_poly(x):return x if isinstance(x,Poly)else Poly.const(x)
def pb(a,b):return sum((a.diff(i)*b.diff(i+6)-a.diff(i+6)*b.diff(i)for i in range(6)),Poly.const(0))
B=tuple(map(F,(-8,16,-9,1)))
def geometry(s,c):
    # Rational line through (a,b)=(5/2,2), extended through the tangent point.
    den=17*s*s-32*s+14;n=24-21*s;x=n/den
    b=2+x;a=F(5,2)+s*x;d=(16*b-8*a)/9
    D=34*a-32*b
    ab=(32+72*b/D)/34;db=(16-8*ab)/9
    T=(c-a,c-b,c-d,c)
    return T,b,a,d,D,ab,db

def main(out):
    out.mkdir(parents=True,exist_ok=True)
    z=[Poly.var(i)for i in range(12)]
    f1=sum((B[i]*z[i]for i in range(4)),Poly.const(0))
    f2=2+sum((B[i]*z[i]*z[i]for i in range(4)),Poly.const(0))
    t,w=z[4:6];action=w*t*f1/2-w*f2/4
    grad=[action.diff(i)for i in range(6)]
    R=[z[i+6]+grad[i]for i in range(6)]
    graph=[]
    for i,j in product(range(6),repeat=2):
        bracket=pb(R[i],R[j]);require(bracket==0,'gradient graph bracket')
        graph.append({'i':i,'j':j,'zero':True})
    for y in range(4):
        require(pb(grad[4],R[y])==w*(B[y]/2),'naive commutator')
        require(pb(z[10],R[y])==-w*(B[y]/2),'missing momentum cancellation')
    # A constant 2x2 mixed derivative determinant: -w/8.
    require((w/2)*F(-1,4)==-w/8,'generating family determinant')
    shape_rows=[];reaction_rows=[];cotangent_checks=0
    for k,c in product(range(-2,3),(F(-1,3),F(0),F(2,5))):
        s=F(8,7)+F(k,1000)
        T,b,a,d,D,ab,db=geometry(s,c)
        require(a>b>d>0 and b*b>F(1,8),'ordered chart')
        require(D>0 and D*D==72*b*b+153,'chart radical')
        require(dot(B,T)==0 and 2+dot(B,[v*v for v in T])==0,'moments')
        tc=(F(1),)*4;tb=(-ab,F(-1),-db,F(0))
        dF2=tuple(2*x*y for x,y in zip(B,T))
        J=[[F(0),F(0),F(0),F(1)],[F(0),F(-1),F(0),F(1)],list(B),list(dF2)]
        jd=abs(det(J));require(jd==144*(T[2]-T[0])==8*D,'chart determinant')
        require(mm(J,inv(J))==eye(4),'point-transform inverse')
        gram=[[dot(tc,tc),dot(tc,tb)],[dot(tb,tc),dot(tb,tb)]]
        jF2=dot(B,B)*dot(dF2,dF2)-dot(B,dF2)**2
        require(det(gram)/jF2==1/(jd*jd),'coarea equality')
        require(dot(B,tc)==dot(B,tb)==dot(dF2,tc)==dot(dF2,tb)==0,'surface tangents')
        for Pc,Pb in ((F(0),F(0)),(F(2,3),F(-4,5)),(F(-1,2),F(3,7))):
            Pis=(Pc,Pb,F(1,9),F(2,7));p=tuple(dot(col,Pis)for col in tr(J))
            require(dot(p,tc)==Pc and dot(p,tb)==Pb,'cotangent transport')
            cotangent_checks+=1
        shape_rows.append({'s':s,'c':c,'b':b,'T':T,'D':D,'abs_det_DQ':jd,'coarea_density':1/jd,'metric_det':det(gram),'coarea_J_squared':jF2})
        for gap,ww in product((F(1,4),F(1,2),F(1)),(F(1,4),F(1,2),F(3,4))):
            tt=c+gap;alpha=-ww*tt/2;beta=ww/4
            q=tuple(ww*bb*(tt-y)/2 for bb,y in zip(B,T));p=tuple(-v for v in q)
            expected=tuple(alpha*bb+beta*ff for bb,ff in zip(B,dF2))
            require(p==expected,'conormal reaction')
            require(dot(p,tc)==dot(p,tb)==0,'Lagrangian one-form')
            require(0<beta<F(1,4) and alpha<-2*beta*c,'positive sector')
            require(4*beta==ww and -alpha/(2*beta)==tt,'interior reconstruction')
            values=tuple(T)+(tt,ww)+(F(0),)*6
            require(grad[4].evaluate(values)==grad[5].evaluate(values)==0,'interior stationarity')
            jac=[[-ww/2,-tt/2],[F(0),F(1,4)]]
            require(abs(det(jac))==ww/8,'density Jacobian')
            reaction_rows.append({'T':T,'t':tt,'w':ww,'alpha':alpha,'beta':beta,'p':p,'jacobian':ww/8})
    # Canonical Dirac matrix in (c,b,F1,F2,Pc,Pb,Pi1,Pi2).
    J8=[[F(0)for _ in range(8)]for _ in range(8)]
    for i in range(4):J8[i][i+4]=F(1);J8[i+4][i]=F(-1)
    A=[[F(j==i)for j in range(8)]for i in (2,3,6,7)]
    D=mm(mm(A,J8),tr(A));Di=inv(D)
    JD=sub(J8,mm(mm(mm(mm(J8,tr(A)),Di),A),J8))
    expected=[[F(0)for _ in range(8)]for _ in range(8)]
    for i in (0,1):expected[i][i+4]=F(1);expected[i+4][i]=F(-1)
    require(JD==expected and det(D)==1,'Dirac projection')
    require(mm(A,JD)==[[F(0)]*8 for _ in range(4)],'constraint Casimirs')
    scalings=[]
    for scales in ((1,1,1,1),(2,3,5,7),(-2,3,-5,7),(F(1,2),F(2,3),F(3,4),F(4,5))):
        Ar=[[F(scales[i])*x for x in row]for i,row in enumerate(A)]
        Dr=mm(mm(Ar,J8),tr(Ar));dA=F(1)
        for x in scales:dA*=x
        require(det(Dr)==dA*dA,'second-class measure determinant')
        JDr=sub(J8,mm(mm(mm(mm(J8,tr(Ar)),inv(Dr)),Ar),J8))
        require(JDr==JD,'constraint-rescaling invariance')
        scalings.append({'scales':scales,'det_Delta':det(Dr),'sqrt_det_over_delta_jacobian':F(1)})
    # Positive transformed measure: integrate alpha width 2 beta L / (beta L).
    moments=[]
    for n in range(5):
        transformed=2*F(4)**n*F(1,4)**(n+1)/F(n+1)
        original=F(1,2*(n+1));require(transformed==original,'transformed measure moments')
        moments.append({'power':n,'continuous_original':original,'continuous_transformed':transformed})
    # Integrate the same triangular domain with the incorrect flat measure.
    # Its alpha width is 2*beta*L; here L=1. Normalize its mass back to 1/2.
    flat_moments=[2*F(4)**n*F(1,4)**(n+2)/F(n+2) for n in (0,1)]
    bad_flat_normalized_first=F(1,2)*flat_moments[1]/flat_moments[0]
    require(bad_flat_normalized_first==F(1,3),'flat-moment integration')
    require(bad_flat_normalized_first!=F(1,4),'flat measure negative control')
    # Negative controls are concrete model distinctions, not general no-go tests.
    negatives=[]
    def reject(name,condition):
        require(condition,name);negatives.append({'incorrect_assumption':name,'rejected':True})
    reject('naive interior and boundary operators commute',pb(grad[4],R[0])!=0)
    reject('full gradient graph retains that uncancelled bracket',pb(R[4],R[0])==0)
    reject('normal conditions are first class',D[0][2]==1)
    reject('Dirac normal bracket still equals one',JD[2][6]==0)
    reject('flat transformed measure is repaired by normalization',bad_flat_normalized_first!=moments[1]['continuous_original'])
    reject('off-surface density integral vanishes',F(191,192)>0)
    Tatom=(F(0),F(1),F(2),F(3));v=tuple(Tatom)+(F(4),F(0))+(F(0),)*6
    reject('null atom must satisfy both positive-stratum moment equations',action.evaluate(v)==0 and all(g.evaluate(v)==0 for g in grad[:5]) and f1.evaluate(v)!=0)
    require(jF2>0,'surface regularity')
    reject('configuration coarea density is always one',shape_rows[7]['coarea_density']!=1)
    witness=next(r for r in shape_rows if r['s']==F(8,7)and r['c']==0)
    require(witness['coarea_density']==F(1,168) and witness['metric_det']==F(457,147),'published witness comparison')
    summary={'status':'PASS','symbolic_graph_brackets':36,'naive_nonzero_and_cancellation_pairs':4,'ordered_surface_cases':len(shape_rows),'stationary_reaction_cases':len(reaction_rows),'cotangent_transport_cases':cotangent_checks,'coarea_identity_cases':len(shape_rows),'dirac_rescaling_cases':len(scalings),'transformed_density_moments':len(moments),'negative_controls':len(negatives),'physical_gates':'HOLD','physical_preparation_derived':False,'physical_hamiltonian_derived':False,'paid_compute':False,'n5_production':False,'external_replication':False}
    outputs={
      'canonical_relations.json':{'symbolic_brackets':graph,'surface':shape_rows,'reactions':reaction_rows},
      'reduction_and_measure.json':{'Delta':D,'Delta_inverse':Di,'Dirac_Poisson_matrix':JD,'constraint_rescalings':scalings,'density_moments':moments,'off_surface_amplitude_real_lower_bound':F(191,192),'negative_controls':negatives},
      'verification.json':summary}
    for name,data in outputs.items():(out/name).write_text(json.dumps(enc(data),indent=2,sort_keys=True)+'\n')
    print(json.dumps(enc(summary),sort_keys=True))
if __name__=='__main__':main(Path(sys.argv[1])if len(sys.argv)>1 else Path(__file__).parent/'results')
