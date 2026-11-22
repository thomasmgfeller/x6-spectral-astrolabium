"""High-precision center probabilities from direct interval sums and quadrature."""
from itertools import product
import json
import mpmath as mp
from gegenprobe import ROOT, Q, N, P, I, F, STEP, packet_family, rebuild


def probabilities(case,q,n,digits):
    with mp.workdps(digits):
        def real(v):
            r=Q(v)
            return mp.mpf(r.numerator)/r.denominator

        m=real(Q(1,8)); h=real(Q(1,2**20)); delta=(mp.mpf(3)/722)**(mp.mpf(1)/4)
        weights=rebuild(case)
        by_target=[[(i,b) for (i,j),b in weights.items() if j==k] for k in range(N)]
        def slope(y,k):
            return -mp.mpf('.5')-sum(b*(y[i]-y[k])**2 for i,b in by_target[k])/38
        def box_factor(d,center,width):
            return mp.expj(center*d)*mp.sinc(width*d)
        x,w=mp.gauss_quadrature(n,'legendre')
        grid=[(a,b/2) for a,b in zip(x,w)]
        tout=[m+(side+z)*h/2 for side in [-1,1] for z,_ in grid]
        _,family=packet_family(q)
        results=[]
        for sign,(yc,wc) in family.items():
            amplitudes=[mp.mpc(0)]*len(tout)
            for zs in product(grid,repeat=3):
                y=[real(yc[k]) for k in range(15)]+[mp.mpf(6),mp.mpf(7)]
                for i,(z,_) in zip(F[1:],zs):
                    y[i]+=h*z
                ds=[slope(y,k) for k in range(15)]
                old=box_factor(sum(ds[k] for k in P),m,real(Q(1,32)))
                old*=mp.expj(delta*sum(real(wc[k])*ds[k] for k in I))
                old*=mp.fprod(box_factor(ds[k],m,h) for k in F)*mp.fprod(b for _,b in zs)
                for z,b in grid:
                    y[15]=6+h*z
                    coef=old*b*box_factor(slope(y,15),m,h)
                    last=slope(y,16)
                    for k,t in enumerate(tout): amplitudes[k]+=coef*mp.expj(t*last)
            assert min(abs(a) for a in amplitudes)>mp.mpf('0.99')
            halves=[sum(w*abs(a)**2 for (_,w),a in zip(grid,amplitudes[j*n:(j+1)*n])) for j in (0,1)]
            results.append(halves[1]/sum(halves))
        return results[0]-results[1]


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run without -O')
    raw=json.loads((ROOT/'uhrfenster.json').read_text())
    for case, paired in raw.items():
        for label,q in [('original',STEP),('transfer',STEP/2)]:
            gaps=[probabilities(case,q,n,digits) for n,digits in [(3,65),(4,85)]]
            with mp.workdps(85):
                assert abs(gaps[0]-gaps[1])<mp.mpf('1e-49')
                for key in ['whole_gap']+(['center_gap'] if 'center_gap' in paired[label] else []):
                    lo,hi=map(Q,paired[label][key])
                    assert mp.mpf(lo.numerator)/lo.denominator<=gaps[1]<=mp.mpf(hi.numerator)/hi.denominator
            print(f'PASS {case} {label}: '+', '.join(mp.nstr(g,13) for g in gaps))
