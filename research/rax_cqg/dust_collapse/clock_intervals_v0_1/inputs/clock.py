"""Exact controls for a declared ordered-clock sector, not a physical clock law."""
from fractions import Fraction as F
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'inputs'))
import memory as m


def require(ok,message):
    if not ok:
        raise RuntimeError(message)


def causal_clock(order,times):
    return all(times[y] < times[x] for x,s in enumerate(order) for y in m.bits(s))


def chronological(order,times,marks):
    perm = tuple(sorted(range(len(order)),key=lambda i:times[i]))
    require(len(set(times)) == len(times),'Distinct clock values required')
    return m.relabel(order,perm),tuple(times[i] for i in perm),tuple(marks[i] for i in perm)


def threshold(times,tau):
    return sum(1 << i for i,t in enumerate(times) if t <= tau)


def action(state,close=False):
    order,times,marks=state
    pred=m.with_anchor(order,close)
    t=(F(-2),)+times+((F(2),) if close else ())
    w=(F(0),)+tuple(F(c,2) for c in marks)+((F(0),) if close else ())
    return m.gravity(pred),m.matter(pred,t,w)


def birth_multiplier(order,last_clock,L=F(1)):
    return F(len(m.ideals(order)))*(L-last_clock)/(2*L)


def packet_norm_ratio(order,lo,hi,L=F(1)):
    require(-L <= lo < hi <= L,'Packet inside the declared clock interval')
    # Exact antiderivative of sum_J integral_{t_last}^L dt/(2L).
    d=F(len(m.ideals(order)))
    integral=d*(L*(hi-lo)-(hi*hi-lo*lo)/2)/(2*L)
    return integral/(hi-lo)


def gamma_gradient(order,times,weights):
    """Direct pair form, checked against the inherited full matter action."""
    gamma=[F(0)]*len(order)
    grad=[F(0)]*len(order)
    currents=[]
    for y,x,k in m.intervals(order):
        b=m.B[k] if k < 4 else 0
        gap=times[x]-times[y]
        gamma[x]+=F(b,2)*gap**2
        j=weights[x]*F(b,2)*gap
        grad[y]+=j;grad[x]-=j
        currents.append((y,x,j))
    return gamma,grad,currents
