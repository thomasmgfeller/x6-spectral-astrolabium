"""Rational sign certificate for the two density equations shared by the matched A+ cases."""
from fractions import Fraction as F
from math import comb


def bernstein(power, a, b):
    # Substitute u=a+(b-a)s, then convert monomials on s in [0,1] to Bernstein form.
    degree = len(power)-1
    shifted = [sum(power[i]*comb(i,j)*a**(i-j)*(b-a)**j
                   for i in range(j,degree+1)) for j in range(degree+1)]
    return [sum(shifted[j]*F(comb(k,j),comb(degree,j)) for j in range(k+1))
            for k in range(degree+1)]


def sign_intervals(lo, hi, sign, endpoints):
    pending = [(lo,hi)]
    closed = 0
    while pending:
        a,b = pending.pop()
        if all(all(sign*v > 0 for v in bernstein(coeff,a,b)) for coeff in endpoints):
            closed += 1
        else:
            assert b-a > F(1,10**8)
            mid = (a+b)/2
            pending.extend(((a,mid),(mid,b)))
    return closed


def check(order_coefficients, collar, window, scale):
    for j,val in enumerate((-5,-4,-3)):
        assert collar[j][:2] == [val*scale,val*scale]
    for coeff in order_coefficients:
        assert {i:c for (i,j),c in coeff.items() if j == 21} == {0:-8,1:16,2:-9,15:1}
        assert {i:c for (i,j),c in coeff.items() if j == 19} == {1:-8,2:16,15:-9,21:1}
    # u=Y15+3, v=Y21+3, t=Y19+3. Physical ordering gives 0<v<t<13/4 and u<v.
    # D21=0 -> 2uv=u^2+3 -> u>6/13 and u<sqrt(3)<7/4.
    t_bounds = [F(z,scale)+3 for z in window]
    assert 0 < t_bounds[0] <= t_bounds[1] < F(13,4)
    polys = [[9,-12*t,50-64*t,68*t,-35] for t in t_bounds]
    # Independently reconstruct the quartic identity against the original layer coefficients
    # at five distinct u and two t, sufficient for degrees <=4 and <=1.
    for u in (F(1,2),F(2,3),F(1),F(4,3),F(3,2)):
        v = (u*u+3)/(2*u)
        for t,poly in zip(t_bounds,polys):
            y = {0:F(-5),1:F(-4),2:F(-3),15:u-3,19:t-3,21:v-3}
            def density(j):
                return 19 + sum(c*(y[j]-y[i])**2 for (i,target),c in order_coefficients[0].items() if target == j)
            assert density(21)==0 and 4*u*u*density(19)==sum(c*u**i for i,c in enumerate(poly))
    a,b = F(1001,1000),F(1008,1000)
    low = sign_intervals(F(6,13),a,-1,polys)
    high = sign_intervals(b,F(7,4),1,polys)
    # v(u) is decreasing for u^2<3.
    vb = [(z*z+3)/(2*z) for z in (b,a)]
    return dict(t=[str(x) for x in t_bounds],u=[str(a),str(b)],
                Y15=[str(x-3) for x in (a,b)],Y21=[str(x-3) for x in vb],
                left_sign_boxes=low,right_sign_boxes=high)
