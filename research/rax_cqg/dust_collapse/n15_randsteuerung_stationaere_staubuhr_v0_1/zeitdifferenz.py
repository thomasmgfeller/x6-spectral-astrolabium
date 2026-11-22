"""Independent elimination for the first two density equations, in clock gaps."""
from fractions import Fraction as Q
from stationaer import box,DELTA
from intervalle import I,S

def gap(B):
    # Horner polynomial form of the second gap once the first clock has been eliminated.
    num=(((B+36)*B-44)*B-96)*B-8
    denom=4*(1+B)*((17*B+18)*B-2)
    return num/denom

def residual(y,past):
    return 19+sum(b*(y-i)**2 for b,i in zip((1,-9,16,-8),past[::-1]))

def run():
    # After clearing denominators the two residuals have degree <= 12 (Y4 degree 2/1,
    # Y5 degree <=4/3). Their vanishing at 17 distinct rational points proves the identities.
    for k in range(17):
        e=Q(1+k,23);past=[-5,-4,-3,-2+e];y4=(e*e-4*e-2)/(2*(1+e));y5=y4+gap(e)
        assert residual(y4,past)==0 and residual(y5,past[1:]+[y4])==0
    out={}
    for name,mid,want in [('left',Q(-1,16),Q(-1,5)),('right',Q(1,16),Q(-6,5))]:
        vals=[];den=[];n=1024
        for i in range(n):
            a=mid-Q(1,32)+Q(i,16*n);e=box(a,a+Q(1,16*n))/DELTA
            d=(17*e+18)*e-2;assert d.hi<0 or d.lo>0;den.append(d);vals.append(gap(e));assert (1+e).lo>0
        full=I(min(x.lo for x in vals),max(x.hi for x in vals));assert full.hi<want*S
        out[name]={'Y5_minus_Y4':full.rounded(6),'denominator_quadratic':I(min(x.lo for x in den),max(x.hi for x in den)).rounded(6),'tiles':n,'strict_upper_bound':str(want)}
    return out
if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2,sort_keys=True))
