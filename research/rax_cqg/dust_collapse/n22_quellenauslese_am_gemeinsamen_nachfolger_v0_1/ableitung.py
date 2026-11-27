"""Enclose first derivatives of the archived zero-momentum collar in the native drift."""
from fractions import Fraction as F
from quelle import box, hull, SCALE
from algebra import solve_box as solve_native
from speichermodell import square as native_square

class Jet:
    def __init__(self, value, derivative=0):
        self.v=box(value)
        self.d=box(derivative)

    def __add__(self,other):
        b=jet(other)
        return Jet(self.v+b.v,self.d+b.d)
    __radd__=__add__

    def __neg__(self):
        return Jet(-self.v,-self.d)

    def __sub__(self,other):
        return self+-jet(other)
    def __rsub__(self,other):
        return jet(other)+-self

    def __mul__(self,other):
        b=jet(other)
        return Jet(self.v*b.v,self.d*b.v+self.v*b.d)
    __rmul__=__mul__

    def __truediv__(self,other):
        b=jet(other)
        v=self.v/b.v
        return Jet(v,(self.d-v*b.d)/b.v)
    def __rtruediv__(self,other):
        return jet(other)/self

    def sqrt(self):
        v=self.v.sqrt()
        assert v.lo>0
        return Jet(v,self.d/(2*v))
    def contains_zero(self):
        return self.v.contains_zero()
    @property
    def lo(self):
        return self.v.lo
    @property
    def hi(self):
        return self.v.hi

def jet(x):
    return x if isinstance(x,Jet) else Jet(x)

def square(x):
    x=jet(x)
    return Jet(native_square(x.v),2*x.v*x.d)

def linear_solve(matrix,rhs):
    a=[[jet(v).v for v in row] for row in matrix]
    x=solve_native(a,[jet(v).v for v in rhs])
    b=[jet(v).d-sum((jet(m).d*u for m,u in zip(row,x)),box(0)) for row,v in zip(matrix,rhs)]
    dx=solve_native(a,b)
    return [Jet(v,u) for v,u in zip(x,dx)]


def lifted_functions():
    # Run the pinned preparation algebra with value-and-derivative pairs.
    # The unchanged native routines check admissibility of the value enclosures.
    import inspect
    from randpraeparation import response
    from staubgeraet import solve
    from zustand import gradients as native_gradients, check
    def vals(s):return {k:x.v for k,x in s.items()}
    def gradients(y,w):
        return native_gradients(vals(y),vals(w))
    def check_values(y,w):
        return check(vals(y),vals(w))
    def adapt(fn,changes):
        code=inspect.getsource(fn)
        for old,new in changes:
            assert code.count(old)==1
            code=code.replace(old,new)
        env=dict(fn.__globals__,jet=jet,dsolve=linear_solve,check_values=check_values,
                 value_gradients=gradients,jet_square=square,jethull=lambda a,b:Jet(hull(a,b)))
        exec(compile(code,fn.__code__.co_filename,'exec'),env)
        return env[fn.__name__]
    response_j=adapt(response,[('from quelle import box','box=jet'),
        ('from algebra import solve_box','solve_box=dsolve'),
        ('from zustand import gradients,check','gradients,check=value_gradients,check_values')])
    solve_j=adapt(solve,[('from quelle import box,hull,SCALE','from quelle import SCALE\n    box,hull=jet,jethull'),
        ('from speichermodell import square','square=jet_square')])
    return response_j,solve_j


def prepare(y,w,left,right,source,functions):
    from empfangsbit import STEP,K0
    from staubgeraet import verify
    ys={j:Jet(v) for j,v in y.items()}
    ws={j:Jet(v) for j,v in w.items()}
    response,solve=functions
    yy,ww=response(ys,ws,Jet(hull(6*STEP+left,6*STEP+right),1))
    # At zero momentum the fixed-point equation for extra involves only
    # Y15, Y16, J and constants. It is independent of this drift.
    assert all(yy[j].d.lo==yy[j].d.hi==0 for j in (15,16))
    zeros=(Jet(0),)*3
    st=solve(yy,ww,source,zeros,K0,Jet(-K0),'positive_bridge')
    assert st['extra'].d.lo==st['extra'].d.hi==0
    vals={k:({j:v.v for j,v in x.items()} if isinstance(x,dict) else x.v) for k,x in st.items()}
    verify(vals,source,(box(0),)*3,K0,box(-K0),'positive_bridge',(box(0),)*3)
    return st['y'],st['w']
