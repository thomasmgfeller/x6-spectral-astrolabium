#!/usr/bin/env python3
"""Exact finite checks for PROOF.md; standard library only, no Monte Carlo."""
from fractions import Fraction as F
from math import comb, isqrt
from pathlib import Path
import hashlib
import json
import platform
import sys

ROOT = Path(__file__).resolve().parent

def zero(n, m=None):
    return [[F(0) for _ in range(n if m is None else m)] for _ in range(n)]

def eye(n):
    a = zero(n)
    for i in range(n): a[i][i] = F(1)
    return a

def add(a, b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def mul(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0))
             for j in range(len(b[0]))] for i in range(len(a))]

def norm(a):
    return max((sum(map(abs,row),F(0)) for row in a), default=F(0))

def inverse_dense(a):
    """Generic exact Gauss-Jordan: independent of forward path recursion."""
    n=len(a); t=[row[:] + er for row,er in zip(a,eye(n))]
    for j in range(n):
        p=next(i for i in range(j,n) if t[i][j])
        t[p],t[j]=t[j],t[p]
        pivot=t[j][j]; t[j]=[x/pivot for x in t[j]]
        for i in range(n):
            if i != j and t[i][j]:
                factor=t[i][j]; t[i]=[x-factor*y for x,y in zip(t[i],t[j])]
    assert [row[:n] for row in t] == eye(n)
    return [row[n:] for row in t]

def response(k):
    n=len(k); r=eye(n)
    for i in range(n):
        assert all(k[i][j]==0 for j in range(i,n))
        for j in range(i):
            if k[i][j]:
                r[i]=[x+k[i][j]*y for x,y in zip(r[i],r[j])]
    return r

def weights(c, eps, n):
    return sum((ck*comb(n,j)*eps**j*(1-eps)**(n-j)
                for j,ck in enumerate(c) if j<=n),F(0))

def coeff(theta):
    return [F(x)+theta*y for x,y in zip([1,-9,16,-8,0],
                         [F(9,8),F(-141,8),F(111,2),F(-63),F(24)])]

def fan_geometry(m,r):
    pts=[(F(0),F(i,4*(m+1)),F(0),F(0)) for i in range(1,m+1)]
    pts += [(F(1)+F(j,2*(r+1)),F(0),F(0),F(0)) for j in range(1,r+1)]
    pts += [(F(2),F(0),F(0),F(0))]
    n=len(pts); causal=[[False]*n for _ in range(n)]
    for i,p in enumerate(pts):
        for j,q in enumerate(pts):
            dt=p[0]-q[0]; ds=sum((p[h]-q[h])**2 for h in range(1,4))
            causal[i][j]=dt>0 and dt**2>ds
            if i!=j: assert dt**2 != ds
            expected=(i>=m and j<i)
            assert causal[i][j]==expected
    # Coordinate boxes of half-width delta preserve all relations:
    # perturbation loses at most 2delta in time + 2sqrt(3)delta in space.
    margins=[F(1)]
    for i,p in enumerate(pts):
        assert abs(p[0]-1)+abs(p[1])<3
        for j,q in enumerate(pts[:i]):
            dt=abs(p[0]-q[0]); dx=abs(p[1]-q[1])
            margins.append(abs(dt-dx))
    delta=min(margins)/16
    assert delta>0
    interval=[[sum(causal[i][h] and causal[h][j] for h in range(n))
               if causal[i][j] else -1 for j in range(n)] for i in range(n)]
    return causal,interval,delta

def fan_transfer(c,eps,beta,m,r):
    order,counts,delta=fan_geometry(m,r); n=len(order); k=zero(n)
    for i in range(n):
        for j in range(n):
            if order[i][j]: k[i][j]=beta*weights(c,eps,counts[i][j])
    return k,delta

def cell_transfer(n,a,b,c):
    k=zero(2*n)
    for j in range(n):
        x,y=2*j,2*j+1; k[y][x]=b
        if j:
            k[x][y-2]=a; k[y][y-2]=c
    return k

def sub(a,ii,jj):
    return [[a[i][j] for j in jj] for i in ii]

def geometric(g,n):
    return sum((abs(g)**j for j in range(n)),F(0))

def atan_bounds(q,terms):
    x=F(1,q)
    s=sum(((-1)**j*x**(2*j+1)/F(2*j+1) for j in range(terms)),F(0))
    nxt=(-1)**terms*x**(2*terms+1)/F(2*terms+1)
    return min(s,s+nxt),max(s,s+nxt)

def pi_bounds(terms):
    # Machin: pi/4 = 4 atan(1/5)-atan(1/239).
    # tan(4 atan(1/5))=120/119; subtraction gives tan=1 in (0,pi/2).
    lo5,hi5=atan_bounds(5,terms); lo239,hi239=atan_bounds(239,terms)
    return 16*lo5-4*hi239,16*hi5-4*lo239

def sqrt_bounds(x,digits):
    s=10**digits; k=isqrt(x.numerator*s*s//x.denominator)
    lo,hi=F(k,s),F(k+1,s)
    assert lo*lo<=x<hi*hi
    return lo,hi

def decimal_bound(x,digits,upper=False):
    s=10**digits; k=x.numerator*s//x.denominator
    if upper and F(k,s)<x: k+=1
    return f'{k//s}.{k%s:0{digits}d}'

def interval_json(lo,hi,digits=35):
    return {'lower_fraction':str(lo),'upper_fraction':str(hi),
            'lower_decimal':decimal_bound(lo,digits),
            'upper_decimal':decimal_bound(hi,digits,True)}

def constants(terms,digits):
    pl,ph=pi_bounds(terms)
    al,_=sqrt_bounds(1/(2*ph),digits)
    _,ah=sqrt_bounds(1/(2*pl),digits)
    assert F(3)<pl<ph<F(22,7)
    out={}
    for name,th in [('theta_0',F(0)),('theta_21',F(21)),('theta_minus_8_over_9',F(-8,9))]:
        cs=coeff(th); r=next(i for i,c in enumerate(cs) if c)
        eps=F(1,16); d=-1-F(3,8)*th
        w=weights(cs,eps,r)
        assert w>0 and d<0
        f=lambda a:a*eps*w/(1-a*d)
        lo,hi=f(al),f(ah)
        assert 0<lo<hi and hi-lo<F(1,10**30)
        out[name]={'r':r,'alpha':interval_json(lo,hi),
                   'norms':{str(m):interval_json(1+m*lo,1+m*hi,12)
                            for m in [1,10,100,1000,10000]}}
    return out

def verify():
    counts={}
    source=json.loads((ROOT/'evidence/SOURCES.json').read_text())
    for s in source['sources']:
        b=(ROOT/'evidence'/s['file']).read_bytes()
        assert hashlib.sha256(b).hexdigest()==s['sha256']
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==s['git_blob']
    counts['source_hashes']=len(source['sources'])
    assert coeff(F(-8,9))[:2]==[F(0),F(20,3)]
    assert coeff(F(21))==[F(197,8),F(-3033,8),F(2363,2),F(-1331),F(504)]
    kernels=[coeff(t) for t in [F(0),F(21),F(-8,9)]]
    kernels += [[F(0)]*r+[F(2),F(-7)] for r in [2,3,4]]
    cases=0
    for cs in kernels:
        r=next(i for i,x in enumerate(cs) if x)
        for eps in [F(1,16),F(1,3),F(1)]:
            for beta in [F(3,7),F(-2,5)]:
                alpha=beta*cs[r]*eps**r
                for m in [1,2,5,12]:
                    k,delta=fan_transfer(cs,eps,beta,m,r); n=len(k)
                    assert mul(k,k)==zero(n)
                    expected=add(eye(n),k)
                    assert response(k)==expected
                    dense=inverse_dense(add(eye(n),[[-x for x in row] for row in k]))
                    assert dense==expected
                    assert norm(dense)==1+m*abs(alpha)
                    f=[F(1 if alpha>0 else -1)]*m+[F(0)]*r+[F(1)]
                    assert sum(dense[-1][j]*f[j] for j in range(n))==1+m*abs(alpha)
                    assert sum(abs(k[-1][j]) for j in range(m))==m*abs(alpha)
                    cases+=1
    counts['exact_fan_cases']=cases
    cell_cases=0; cell_results=[]
    for g in [F(0),F(1,4),F(-1,2),F(1),F(-1),F(5,4)]:
        rows=[]
        for n in [1,2,4,8,12]:
            a,b,c=F(2),F(1),g-2; k=cell_transfer(n,a,b,c)
            r=response(k)
            exact=max(2*geometric(g,n),1+4*geometric(g,n-1))
            assert norm(r)==exact
            assert inverse_dense(add(eye(2*n),[[-x for x in row] for row in k]))==r
            ee=list(range(0,2*n,2)); bb=list(range(1,2*n,2))
            re=inverse_dense(add(eye(n),[[-x for x in row] for row in sub(k,ee,ee)]))
            reduced=add(sub(k,bb,bb),mul(mul(sub(k,bb,ee),re),sub(k,ee,bb)))
            expected=zero(n)
            for j in range(1,n):expected[j][j-1]=g
            assert reduced==expected
            if abs(g)<1:
                bound=max(F(2)/(1-abs(g)),1+F(4)/(1-abs(g)))
                assert norm(r)<=bound
            if g==0 and n>=2: assert norm(r)==5 and norm(k)==3
            rows.append({'cells':n,'norm_exact':str(exact)})
            cell_cases+=1
        cell_results.append({'g':str(g),'results':rows})
    counts['exact_cell_cases']=cell_cases
    # Genuine negative controls: wrong intervals, missing transfer, wrong sign.
    cs=coeff(F(21)); eps=F(1,16); beta=F(3,7)
    k,_=fan_transfer(cs,eps,beta,5,0)
    assert beta*weights(cs,eps,1)!=beta*weights(cs,eps,0)
    missing=[row[:] for row in k];missing[-1][0]=0
    assert norm(response(missing))!=norm(response(k))
    assert norm(response(cell_transfer(4,F(2),F(1),F(2))))>5
    # A cancellation across DIFFERENT path lengths is not K^3=0.
    k=cell_transfer(2,F(2),F(1),F(-2))
    assert mul(mul(k,k),k)!=zero(4)
    counts['negative_controls']=4
    low=constants(40,45); high=constants(60,65)
    for name in low:
        l=low[name]['alpha'];h=high[name]['alpha']
        assert max(F(l['lower_fraction']),F(h['lower_fraction'])) < min(F(l['upper_fraction']),F(h['upper_fraction']))
    counts['overlapping_rational_alpha_intervals']=3
    return {'status':'PASS','version':'0.26','base_commit':source['commit'],
            'arithmetic':'fractions.Fraction; integer isqrt; exact rational intervals',
            'checks':counts,'constants':high,'cells':cell_results,
            'limits':['Finite checks supplement the analytic proofs; no proof assistant.',
                      'No typical-realization instability, variance or KG-detector claim.',
                      'No new ensembles; METHOD and G1 remain HOLD.']}

def main():
    out=verify(); data=(json.dumps(out,indent=2,ensure_ascii=False)+'\n').encode()
    target=ROOT/'results/RESULTS.json'; target.parent.mkdir(exist_ok=True)
    if '--check' in sys.argv:
        assert target.read_bytes()==data,'Stored result differs from exact recomputation'
        print('Exact replay: byte-identical PASS')
    else: target.write_bytes(data)
    print(json.dumps(out['checks'],sort_keys=True))
    print('alpha21:',out['constants']['theta_21']['alpha']['lower_decimal'],
          out['constants']['theta_21']['alpha']['upper_decimal'])
    return out

if __name__=='__main__': main()
