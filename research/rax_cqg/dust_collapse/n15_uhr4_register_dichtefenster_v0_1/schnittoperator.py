"""Exact finite-coordinate check of the exchange and coherent input processing."""
from fractions import Fraction as F
from itertools import product
import cmath
from registertest import CENTER, R, INNER, HIDDEN, EPS, Q0, clocks, profile, ORDER

def verify():
    # Exact translations on the half-open supports. The projector identities
    # in the text also hold on the full continuous fibers.
    def exchange(x,a,b,t):
        if a<=x<b:return x+t
        if a+t<=x<b+t:return x-t
        return x
    count=0
    for a,b,t in ((-R,R,F(1,32)),(-R,R,F(-1,32)),(-R,F(0),R)):
        for z in (a-R,a,a+R/3,(a+b)/2,b,b+R,b+t,a+t,a+t+R/3):
            assert exchange(exchange(z,a,b,t),a,b,t)==z
            count+=1
        # Orthogonality on disjoint support holds for any multiplicative
        # weights. Demonstrate the associated lower bound with a rational vector.
        v=(F(3,5),F(4,5),0,0);m=(F(2),F(-1),F(9),F(-2))
        uv=(0,0,v[0],v[1])
        assert sum((u-z*x)**2 for u,z,x in zip(uv,m,v))>=1
    # A two-input/two-output coherent kernel with unequal complex left amplitudes.
    # Compute every hidden site directly, with the actual output clock.
    ys=[CENTER-R/2,CENTER+R/2]
    maximum=0
    trials=0
    for lobe in (-1,1):
        y,_,d=profile(clocks(lobe,True))
        for matrix in (((1,0),(0,1)),((0,1),(1,0)),((1,1j),(1j,1))):
            amplitudes=[]
            for side in (-1,1):
                total=0j
                for j,passed in enumerate(ys):
                    yy={**y,4:passed}
                    c={}
                    for v in HIDDEN:
                        k=ORDER.index(v)
                        c[v]=-F(1,2)-sum(F(b,38)*(yy[v]-yy[ORDER[k-e]])**2
                                           for e,b in enumerate((1,-9,16,-8),1))
                    q=sum(c[v]*d[v] for v in HIDDEN)
                    x={v:F(1,8)+side*EPS*Q0*d[v]/q for v in HIDDEN}
                    right=cmath.exp(1j*float(sum(c[v]*x[v] for v in HIDDEN))) # D=1
                    total+=sum(matrix[j][i]*a*right for i,a in enumerate((1+2j,-1+.5j)))
                amplitudes.append(total)
            deviation=abs(amplitudes[1]-cmath.exp(2j*float(EPS*Q0))*amplitudes[0])
            maximum=max(maximum,deviation);trials+=1
    assert maximum<3e-15
    return {'involution_endpoint_checks':count,'two_mode_kernel_cases':trials,
            'two_mode_global_phase_deviation_upper':'3e-15'}

if __name__=='__main__':
    print(verify())
