"""Independent arithmetic at finite cubature nodes, by two routes to the kernel."""
import cmath
import math
from itertools import product

ORDER=(0,1,2,3,4,5,6,11,12,13,14,7,8,9,10)
ROOT=(3/722)**.25
D=3.75*ROOT
H=.125
EPS=2**-14
LAYER=(1,-9,16,-8)
EARLY=(76/64,47/64,24/64,8/64)
BASES=(2,3,5,7,11,13,17)
# Independent relative arm labels.
MODES=['0','A+','A-','B+','B-','C+','C-','J+','J-']+[p+s+t for p in ('AB','UV') for s,t in product('+-', repeat=2)]
REL={(a,b) for k,b in enumerate(ORDER) for a in ORDER[:k]}
PAIRS=[]
for i,j in REL:
    count=sum((i,k) in REL and (k,j) in REL for k in ORDER)
    if count<4:
        PAIRS.append((ORDER.index(i),ORDER.index(j),LAYER[count]))

def rule(n,dim):
    # Reflected low-discrepancy points integrate all odd linear terms exactly.
    for j in range(1,n+1):
        u=[]
        for b in BASES[:dim]:
            k=j;t=0.;a=1./b
            while k:
                k,r=divmod(k,b)
                t+=r*a
                a/=b
            u.append(2*t-1)
        yield u
        yield [-x for x in u]

def multipliers(mode):
    vals=dict.fromkeys('ABCUVJ',0)
    if mode!='0':
        letters=mode.rstrip('+-')
        for x,s in zip(letters,mode[len(letters):]):
            vals[x]=1 if s=='+' else -1
    return vals

def offset(mode):
    m=multipliers(mode)
    dz=[m['U']+m['V']*v for v in EARLY]+[0.]*11
    dz[7]=m['A'];dz[9]=m['B']
    return [d*H/math.sqrt(D) for d in dz],m['J']*H/math.sqrt(D),m['C']*H

def coeff(y,spec,stream):
    dz,local,_=spec
    if stream:
        memory=[]
        c=[]
        for j,clock in enumerate(y):
            current=clock+dz[j]
            site=-.5
            for lag,(i,old) in enumerate(reversed(memory),1):
                past=old+local if i==4 and j>7 else old
                site-=LAYER[lag-1]*(current-past)**2/38
            c.append(site)
            memory=(memory+[(j,current)])[-4:]
    else:
        c=[-.5]*15
        for i,j,b in PAIRS:
            diff=(y[j]-y[i])+(dz[j]-dz[i])-(local if (ORDER[i],ORDER[j])==(4,12) else 0)
            c[j]-=b*diff**2/38
    return c

def sinc(x):
    return math.sin(x)/x if x else 1.

def phase_readout(p):
    def aa(letter):return (p[letter+'+']+p[letter+'-'])/H**2
    def ab(letters):
        return (p[letters+'++']+p[letters+'--']-p[letters+'+-']-p[letters+'-+'])/(4*H**2)
    m=(p['C+']-p['C-'])/(2*H)-19*(aa('A')+10/9*ab('AB')-15*aa('B')-ab('UV'))
    return m,19/8*aa('J')

def calc(nz,nu,stream):
    modes={m:offset(m) for m in MODES}
    output_rows={}
    zz=list(rule(nz,7))
    uu=list(rule(nu,6))
    totals={(rho,s):{m:[0j,0.] for m in MODES} for rho,s in product((.125,.25),(-1,1))}
    closure=0.
    phase_difference=0.
    for z in zz:
        wend=[.125+t/2**20 for t in z[3:]]
        amps={key:dict.fromkeys(MODES,0j) for key in totals}
        for uvec,lobe in product(uu,(-1,1)):
            t=iter(uvec)
            u=[k/8+(0 if k==3 else next(t)/2**22) for k in range(1,8)]
            u[1]+=lobe/1000
            y=[-5.,-4.,-3.,-1.75]+[-1.75+3.75*v for v in u]+[2.,3.+z[0]/2**20,4.+z[1]/2**20,5.+z[2]/2**20]
            c0=coeff(y,modes['0'],stream)
            # Independently solve the two homogeneous constraints.
            a,b,c=y[8:11]
            s13=9*(c-a)/(16*(c-b))
            s14=(-9+16*s13)/8
            n=(1.,s13,s14)
            q=sum(x*v for x,v in zip(c0[8:11],n))
            faces=[0]+[(a+b)/2 for a,b in zip(u,u[1:])]+[1]
            f=[b-a for a,b in zip(faces,faces[1:])]
            f[3]=255/2048
            for m,spec in modes.items():
                cc=coeff(y,spec,stream)
                compare=coeff(y,spec,not stream)
                closure=max(closure,max(abs(a-b) for a,b in zip(cc,compare)))
                past=sum(cc[:4])
                common=sum(a*b for a,b in zip(wend,cc[11:]))+spec[2]*(-127*wend[0]+240*wend[1]-120*wend[2])/D
                amp_size=sinc(past/32)*math.prod(sinc(D*a/2**20) for a in cc[4:11])
                for rho,side in amps:
                    w=f.copy()
                    for j,v in enumerate(n,4):
                        w[j]+=side*EPS*(-1.25/q)*v
                    phi=common+past*rho+D*sum(a*b for a,b in zip(cc[4:11],w))
                    amps[rho,side][m]+=amp_size*cmath.exp(1j*phi)/(2*len(uu))
        for key,row in amps.items():
            a=row['0']
            for m,b in row.items():
                # Reconstruct overlap from four port intensities.
                x=(abs(a+b)**2-abs(a-b)**2)/4
                v=(abs(a-1j*b)**2-abs(a+1j*b)**2)/4
                port=complex(x,v)
                direct=a.conjugate()*b
                phase_difference=max(phase_difference,abs(port-direct))
                totals[key][m][0]+=(port if stream else direct)/len(zz)
                totals[key][m][1]+=(abs(a)**2+abs(b)**2)/len(zz)
    assert closure<2e-13 and phase_difference<3e-15
    for rho in (.125,.25):
        rows={}
        for s,which in ((-1,'niedrig'),(1,'hoch')):
            vals=totals[rho,s]
            ph={m:cmath.phase(v[0]) for m,v in vals.items()}
            mass,density=phase_readout(ph)
            rows[which]={'summe':mass,'dichte12':density,'P_plus':.5+vals['J+'][0].imag/vals['J+'][1]}
        rows['differenz_P_plus']=rows['hoch']['P_plus']-rows['niedrig']['P_plus']
        output_rows[str(rho)]=rows
    return output_rows

def test(bounds):
    out={}
    for nz,nu,stream in ((3,4,False),(5,10,True)):
        r=calc(nz,nu,stream)
        for row in r.values():
            for lab in ('niedrig','hoch'):
                for name in ('summe','dichte12'):
                    lo,hi=map(float,bounds['phase_readouts'][lab][name]['readout'])
                    assert lo<row[lab][name]<hi
            lo,hi=map(float,bounds['single_output']['P_plus_high_minus_low'])
            assert lo<row['differenz_P_plus']<hi
        out['chronologisch' if stream else 'direkt']=r
    return out
