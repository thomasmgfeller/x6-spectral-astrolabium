"""Forward apparatus trajectory on two material links and their boundary forces."""
from fractions import Fraction as F

TOTAL = F(-78302831, 10**9)
MOMENTUM = F(-8404505923, 10**9)
EPSILON = F(1, 10**6)


def trajectory(y, w, p, t, gain=1, initial=(0, 0)):
    a = y[1] + 4
    b = y[0] - y[1] + 1
    x0, u0 = initial
    x1 = x0 + p/w[1] - gain*b
    u1 = u0 + t/w[1] - a
    x2 = x1 + p/w[2]
    u2 = u1 + t/w[2]
    return [(x0, u0), (x1, u1), (x2, u2)]


def local_readout(q, weight):
    return tuple(weight*(end-start) for start,end in zip(q[1],q[2]))


def full_link_action(y, w, q, gain):
    dx,du = (v-u for u,v in zip(q[0],q[1]))
    ex,eu = (v-u for u,v in zip(q[1],q[2]))
    b = y[0]-y[1]+1
    a = y[1]+4
    return w[1]*((dx+gain*b)**2+(du+a)**2) + w[2]*(ex**2+eu**2)


def fixed_target_coupling():
    """Positive X contribution of the free link at a fixed native target."""
    w = [F(1,8)]*3
    values = []
    for gain in (F(1),F(1,2),F(1,10)):
        p = MOMENTUM/gain
        # Shifted early clocks check independence from clock displacements.
        q = trajectory([F(-5)+EPSILON,F(-4)-EPSILON],w,p,TOTAL,gain)
        travel = q[2][0]-q[1][0]
        cost = w[2]*travel**2
        assert gain*p == MOMENTUM and cost == MOMENTUM**2/(gain**2*w[2])
        values.append({'gain':str(gain),'prepared_P':str(p),
                       'X_coast_action':str(cost), 'factor_vs_unit':str(1/gain**2)})
    return values
