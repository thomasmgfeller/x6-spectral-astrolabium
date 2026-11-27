"""Independent integer evaluations of the action and its exact centered differences."""
from fractions import Fraction

S = 10**9
CLOCKS = tuple(range(15,22))
WEIGHTS = (16,18,19,21)


def check(call, coefficients, collar, kind, sector):
    y = [0]*22
    w = [0]*22
    dots = {}
    for j, (a,b,c,d) in collar.items():
        y[j], w[j] = (a+b)//2, (c+d)//2
        dots[j] = [y[j],y[j],w[j],w[j]]
    for j, v in zip(CLOCKS, [-16,-8,-4,5,1,2,-2]):
        y[j] = v*(S//8)
    for j, v in zip(WEIGHTS, [5,3,2,1]):
        w[j] = v*(S//32)
    if kind == 'A0':
        w[21] = 0
    for i, j in enumerate((16,18)):
        if sector & (1 << i):
            w[j] = 5
    variables = [(y,j) for j in CLOCKS] + [(w,j) for j in WEIGHTS]
    centers = [(a[j],a[j]) for a,j in variables]
    got = [list(map(int, row.split())) for row in call(dots, centers).splitlines()]
    assert len(got) == 11 and all(len(row)==24 for row in got)
    step = S//8

    def action():
        return 19*S*S*sum(w) + sum(c*w[j]*(y[j]-y[i])**2 for (i,j),c in coefficients.items())

    def diff(fn, var, j):
        var[j] += step
        hi = fn()
        var[j] -= 2*step
        lo = fn()
        var[j] += step
        return Fraction(hi-lo, 2*step)

    for ir, (a,j) in enumerate([(w,j) for j in WEIGHTS]+[(y,j) for j in CLOCKS]):
        weight_constraint = ((ir in (0,1) and sector & (1 << ir)) or (ir == 3 and kind == 'A0'))
        def value():
            if weight_constraint:
                return Fraction(w[j],S)
            scale = 1 if ir < 4 else Fraction(-1,2)
            return scale*diff(action,a,j)/S**2
        expected = [value()*S] + [S*S*diff(value,v,k) for v,k in variables]
        for col, (target,lo,hi) in enumerate(zip(expected,got[ir][::2],got[ir][1::2])):
            assert lo <= target <= hi, (kind,sector,j,col,target,lo,hi)
            if ir == 3 and kind == 'A0':
                assert lo == hi == target
    return 132
