"""Independent all-pair floating-point check of source coherences and aperture."""
import cmath
import math
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent/'basis'))
from kontrollrechnung import CENTER, D, R, clocks, fields, points, sinc, PAIRS


def simpson(n):
    assert n>0 and n%2==0
    for k in range(n+1):
        yield (2*k/n-1, (1 if k in (0,n) else 4 if k%2 else 2)/(3*n))


def audit(n, outer, inner):
    """Independent rates at both inlet densities, with the same final measure."""
    assert len(PAIRS)==50
    output={}
    for rho in (1/8,1/4):
        sums={mode:{name:[0.,0.] for name in ('left','right','same','plus_i','minus_i','pi','continuous','matched_same','matched_diag')}
              for mode in ('fixed','moving')}
        for z in points(outer,7):
            ends=[2.,3.+z[0]/2**20,4.+z[1]/2**20,5.+z[2]/2**20]
            densities=[.125+t/2**20 for t in z[3:]]
            waves={key:[0j,0j,0j,0j] for key in [(mode,side) for mode in sums for side in (-1,1)]}
            for uv in points(inner,6):
                for arm in (-1,1):
                    coords=[(0,CENTER+R*uv[0],1.),(1,CENTER+1/(32*math.sqrt(D))+R*uv[0],1.)]
                    coords.extend((2,CENTER+(3.75/64)*t,wt) for t,wt in simpson(n))
                    coords.append((3,CENTER+R*uv[0],1.))
                    for ix,y4,wy in coords:
                        u=clocks(arm,uv,y4)
                        c,v,q,qs,f=fields(u,ends)
                        if ix==3:
                            u_matched=[uk+(-1)**k/(32*math.sqrt(D)*3.75) for k,uk in enumerate(u)]
                            c,_,_,_,other_f=fields(u_matched,ends)
                            assert all(abs(a-b)<5e-15 for a,b in zip(f,other_f))
                        p=sum(c[:4])
                        weight=wy*sinc(p/32)*math.prod(sinc(D*a/2**20) for a in c[4:11])/(4*inner)
                        phase0=p*rho+sum(a*b for a,b in zip(c[11:],densities))
                        for (mode,side),branches in waves.items():
                            if mode=='moving' and ix==3:
                                continue
                            qden=qs if mode=='fixed' else q
                            x=f.copy()
                            for j,vj in enumerate(v,4):
                                x[j]+=side*(-1.25/2**14)*vj/qden
                            phase=phase0+D*sum(a*b for a,b in zip(c[4:11],x))
                            branches[ix]+=weight*cmath.exp(1j*phase)
            for (mode,side),(left,right,wide,matched) in waves.items():
                amps=(left,right,left+right,left+1j*right,left-1j*right,left-right,wide)
                for name,wave in zip(sums[mode],amps):
                    sums[mode][name][int(side>0)]+=abs(wave)**2/(2*outer)
                if mode=='fixed':
                    sums[mode]['matched_same'][int(side>0)]+=abs(left+matched)**2/(2*outer)
                    sums[mode]['matched_diag'][int(side>0)]+=(abs(left)**2+abs(matched)**2)/(2*outer)
        output[str(rho)]={}
        for mode,v in sums.items():
            d=[(a+b)/2 for a,b in zip(v['left'],v['right'])]
            u=[(a-b)/4 for a,b in zip(v['same'],v['pi'])]
            j=[(a-b)/4 for a,b in zip(v['plus_i'],v['minus_i'])]
            a,b,c=(x[1]-x[0] for x in (d,u,j))
            values={str(mu):(a+mu*b)/(d[0]+mu*u[0]) for mu in (0.,.001,.1,1.)}
            values['continuous']=(v['continuous'][1]-v['continuous'][0])/v['continuous'][0]
            if mode=='fixed':
                for name in ('matched_same','matched_diag'):
                    low,high=v[name]
                    values[name]=(high-low)/low
                values['root']=-a/b
                values['visibility_factor']=math.hypot(u[0],j[0])/d[0]
                def contrast(phi):return a+b*math.cos(phi)+c*math.sin(phi)
                lo,hi=-.0011,0.
                assert contrast(lo)<0<contrast(hi)
                for _ in range(45):
                    m=(lo+hi)/2
                    if contrast(m)<0:lo=m
                    else:hi=m
                values['phase_root']=(lo+hi)/2
            output[str(rho)][mode]=values
    return output


def run():
    return {str(n):audit(n,outer,inner) for n,outer,inner in [(12,2,3),(24,4,6)]}
