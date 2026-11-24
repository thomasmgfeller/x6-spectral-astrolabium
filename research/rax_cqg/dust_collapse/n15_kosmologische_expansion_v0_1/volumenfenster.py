"""External comoving clock slabs in two synthetic dust FLRW backgrounds."""
from fractions import Fraction as F
from math import factorial
import json
import mpmath as mp

def number(q):
    return mp.mpf(q.numerator)/q.denominator

def integrated_series(m,order=48):
    # Taylor coefficients of a(s); a(0)=a'(0)=1 and a²a''=-Omega_m/2.
    a=[F(1),F(1)]
    a2=[]
    for n in range(order-1):
        a2.append(sum(a[i]*a[n-i] for i in range(n+1)))
        source = -m/2 if n==0 else F(0)
        lower = sum(a2[j]*(n-j+2)*(n-j+1)*a[n-j+2] for j in range(1,n+1))
        a.append((source-lower)/((n+2)*(n+1)))
    a2=[sum(a[i]*a[n-i] for i in range(n+1)) for n in range(order+1)]
    v=[sum(a2[i]*a[n-i] for i in range(n+1)) for n in range(order+1)]
    return [F(0)]+[u/(i+1) for i,u in enumerate(v)]

def primitive_by_quadrature(s,m):
    # Integrate in scale factor instead of Taylor-expanding in clock time.
    def ds_da(a):
        return mp.sqrt(a/(m+(1-m)*a))
    def elapsed(a):
        return mp.quad(ds_da,[1,a])
    a=mp.findroot(lambda b:elapsed(b)-s,(1+s/2,1+3*s/2),tol=mp.mpf('1e-47'))
    return mp.quad(lambda b:b**3*ds_da(b),[1,a])

def exact_classifier(first,second,n):
    total=mp.mpf(0)
    count=0
    for i in range(n+1):
        for j in range(n-i+1):
            k=n-i-j
            coefficient=factorial(n)//(factorial(i)*factorial(j)*factorial(k))
            p=first[0]**i*first[1]**j*first[2]**k
            q=second[0]**i*second[1]**j*second[2]**k
            total+=coefficient*max(p,q)/2
            count+=1
    return total,count

def run(out):
    mp.mp.dps=60
    results=[]
    coeffs=[integrated_series(m) for m in (F(1),F(64,125))]
    for h in (F(1,8),F(1,16),F(1,32),F(1,64)):
        row=dict(h=str(h), backgrounds={})
        probs=[]
        for label,m,poly in zip(('flat','open'),(F(1),F(64,125)),coeffs):
            ends=[h*j/2 for j in (-3,-1,1,3)]
            primitives=[primitive_by_quadrature(number(s),number(m)) for s in ends]
            integrated=[b-a for a,b in zip(primitives,primitives[1:])]
            w_series=[sum(c*(b**k-a**k) for k,c in enumerate(poly)) for a,b in zip(ends,ends[1:])]
            relative=max(abs(number(v)/r-1) for v,r in zip(w_series,integrated))
            if relative>mp.mpf('1e-20'):
                raise ValueError('Vierervolumina der zwei Rechenwege weichen ab')
            l,c,r=integrated
            d=4*c*(r-2*c+l)/(r-l)**2
            expected=F(2,3)-m/6
            if m==1 and abs(d-number(F(1,2)+3*h*h/32))>mp.mpf('1e-46'):
                raise ValueError('Flache Referenzformel')
            if abs(d-number(expected))>number(h*h):
                raise ValueError('Kontinuumsgrenze auf Kontrollgittern')
            p=[t/sum(integrated) for t in integrated]
            probs.append(p)
            row['backgrounds'][label]=dict(
                W=[mp.nstr(t,25) for t in integrated],cell_probabilities=[mp.nstr(t,25) for t in p],
                D_h=mp.nstr(d,23),D_exact=str(expected),omega_from_D_h=mp.nstr(4-6*d,18),
                relative_disagreement=mp.nstr(relative,7))
        accuracy,terms=exact_classifier(*probs,15)
        if terms!=136 or not mp.mpf('.5')<=accuracy<=1:
            raise ValueError('Fehler in der Multinomialrechnung')
        row['synthetic_15']=dict(oracle_accuracy=mp.nstr(accuracy,20),triples=terms)
        results.append(row)
    (out/'volumenfenster.json').write_text(json.dumps(results,indent=2)+'\n')
