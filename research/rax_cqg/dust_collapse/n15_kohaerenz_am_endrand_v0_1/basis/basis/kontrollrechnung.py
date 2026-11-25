"""Independent integration of the full physical phase and of the local two-column Gram matrix."""
import cmath
import math
from itertools import product

D=3.75*(3/722)**.25
R=3.75/2**22
CENTER=-1.75+3.75/8
Z0=-1.75+3.75*5/8
ORDER=(0,1,2,3,4,5,6,11,12,13,14,7,8,9,10)
PAIRS=[]
for i,j in ((i,j) for i in range(15) for j in range(i+1,15)):
    between=sum(i<k<j for k in range(15))
    if between<4: PAIRS.append((i,j,(1,-9,16,-8)[between]))

def sinc(x):
    return math.sin(x)/x if x else 1.

def clocks(lobe,v,y4):
    point=iter(v)
    u=[k/8+(next(point)/2**22 if k!=3 else 0.) for k in range(1,8)]
    u[0]=(y4+1.75)/3.75
    u[1]+=lobe/1000
    return u

def coefficients(y):
    c=[-.5]*15
    for i,j,b in PAIRS:
        c[j]-=b*(y[j]-y[i])**2/38
    return c

def fields(u,yend):
    y=[-5.,-4.,-3.,-1.75]+[-1.75+3.75*a for a in u]+yend
    c=coefficients(y)
    reference=coefficients(y[:4]+[CENTER]+y[5:])
    a,b,k=y[8:11]
    n13=9*(k-a)/(16*(k-b))
    n=(1.,n13,(16*n13-9)/8)
    q=sum(c[i]*x for i,x in zip((8,9,10),n))
    qs=sum(reference[i]*x for i,x in zip((8,9,10),n))
    faces=[0]+[(v+w)/2 for v,w in zip(u,u[1:])]+[1]
    f=[high-low for low,high in zip(faces,faces[1:])]
    f[3]=255/2048
    return c,n,q,qs,f

def points(count,dimension):
    for index in range(1,count+1):
        row=[]
        for b in (2,3,5,7,11,13,17)[:dimension]:
            k=index;value=0.;place=1./b
            while k:
                k,d=divmod(k,b);value+=place*d;place/=b
            row.append(2*value-1)
        yield row
        yield [-x for x in row]

def end(nz,nu,wide):
    keys=list(product(('laufend','fest'),(.125,.25),(-1,1)))
    intensity={key:[0.,0.,0.,0.] for key in keys}
    for z in points(nz,7):
        wend=[.125+t/2**20 for t in z[3:]]
        ends=[2.,3.+z[0]/2**20,4.+z[1]/2**20,5.+z[2]/2**20]
        amps={key:[0j,0j] for key in keys}
        for half,lobe,uv in product((0,1),(-1,1),points(nu,6)):
            y4=(CENTER+half/(32*math.sqrt(D))+R*uv[0] if wide
                else CENTER+(half-.5)*R+R*uv[0]/2)
            u=clocks(lobe,uv,y4)
            c,n,q,qs,f=fields(u,ends)
            inlet=sum(c[:4])
            weight=sinc(inlet/32)*math.prod(sinc(D*x/2**20) for x in c[4:11])/(4*nu)
            future=sum(a*b for a,b in zip(c[11:],wend))
            for key in keys:
                kind,rho,side=key
                den=q if kind=='laufend' else qs
                x=f.copy()
                for i,v in enumerate(n,4): x[i]+=side*(-1.25/2**14)*v/den
                phase=inlet*rho+future+D*sum(a*b for a,b in zip(c[4:11],x))
                amps[key][half]+=weight*cmath.exp(1j*phase)
        for key,(l,h) in amps.items():
            for i,k in enumerate((-1j,1j,1,-1)):
                intensity[key][i]+=abs(l+k*h)**2/(2*nz)
    rows={}
    for kind in ('laufend','fest'):
        rows[kind]={}
        for rho in (.125,.25):
            rates=[intensity[kind,rho,s] for s in (-1,1)]
            p=[v[0]/(v[0]+v[1]) for v in rates]
            rows[kind][str(rho)]={'p_minus_i_low_high':p,'difference':p[1]-p[0],
                                 'intensities_low_high_in_common_units':rates}
    return rows

def simpson(n):
    return [(2*j/n-1,(1 if j in (0,n) else (4 if j%2 else 2))/(3*n)) for j in range(n+1)]

def birth(n,wide,opening,side):
    # Other retained clocks at midpoint of the positive clock-5 lobe.
    center,r,t=(CENTER,R,1/(32*math.sqrt(D))) if wide else (CENTER-R/2,R/2,R)
    fixed=clocks(1,[0]*6,CENTER)
    c,nvec,q,qs,f=fields(fixed,[2.,3.,4.,5.])
    w0=.5 if opening else D*(f[4]+side*(-1.25/2**14)/qs)
    rule=simpson(n);a=8/38
    rows=[]
    for (zz,wz),(xx,wx) in product(rule,rule):
        z=Z0+zz*(3.75/64 if opening else R)
        fixed[4]=(z+1.75)/3.75
        _,_,_,qs,f=fields(fixed,[2.,3.,4.,5.])
        w=(xx+1)/2 if opening else D*(f[4]+side*(-1.25/2**14)/qs+xx/2**20)
        direct=0j;diff=0j
        for node,wi in rule:
            v=r*node
            wave=cmath.exp(1j*a*w*(z-center-v)**2)
            rel=a*t*((w-w0)*(t-2*(Z0-center))-2*w*((z-Z0)-v))
            direct+=wi*wave
            diff+=wi*wave*2j*cmath.exp(.5j*rel)*math.sin(.5*rel)
        rows.append((wz*wx,direct,diff))
    aa=sum(k*abs(l)**2 for k,l,d in rows)
    bb=sum(k*abs(l+d)**2 for k,l,d in rows)
    proj=sum(k*l.conjugate()*d for k,l,d in rows)/aa
    residual=sum(k*abs(d-proj*l)**2 for k,l,d in rows)
    determinant=aa*residual
    largest=(aa+bb+math.sqrt((aa+bb)**2-4*determinant))/2
    return {'trace_distance':math.sqrt(residual/bb),'sigma_min_over_max':math.sqrt(determinant)/largest}

def check(cert):
    result={}
    for name,wide in (('breit',True),('benachbart',False)):
        result[name]={}
        for i,(nz,nu,n) in enumerate(((3,4,6),(6,12,12)),1):
            ports={}
            for kind,opening,sign in [('geoeffnete_dichte_und_uhr',True,1),('hohe_dichte',False,1),('niedrige_dichte',False,-1)]:
                val=birth(n,wide,opening,sign)
                bound=cert['birth'][name][kind]
                assert 0<val['trace_distance']<float(bound['trace_distance_upper'])
                assert 0<val['sigma_min_over_max']<float(bound['sigma_min_over_max_upper'])
                ports[kind]=val
            rates=end(nz,nu,wide)
            for kind,mode in [('laufend','gemeinsam'),('fest','festes_profil')]:
                lo,hi=map(float,cert['phase_preparation'][name][mode]['delta_conditional_minus_i_label'])
                for row in rates[kind].values():
                    assert lo-2e-15<=row['difference']<=hi+2e-15
                    low, high = row['intensities_low_high_in_common_units']
                    relative = (high[2] - low[2]) / low[2]
                    if kind == 'laufend':
                        assert abs(relative) < 2e-14
                    elif wide:
                        lower, upper = map(float, cert['equal_phase_wide']['relative_intensity_high_minus_low'])
                        assert lower <= relative <= upper
            result[name][str(i)]={'port':ports,'phase':rates}
    return result
