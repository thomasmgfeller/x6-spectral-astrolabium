"""Native linear background constraints and verification of finite pulse solutions."""
from fractions import Fraction as F

SOURCES = (-F(1,10**6), F(1,10**6))


def background_rows(y):
    from gemischt import CLOCK,WEIGHT,FUT,COEFF
    from quelle import box
    keys = [('w',j) for j in WEIGHT+FUT]+[('M',j) for j in FUT]
    def row(i):
        result=[]
        for kind,j in keys:
            c=COEFF.get((i,j),0)
            if kind=='M':
                v=box(c)
            elif j in FUT:
                v=-c*y[i]
            else:
                v=c*(y[j]-y[i])
                if i==j:
                    v-=sum(a*(y[j]-y[k]) for (k,l),a in COEFF.items() if l==j)
            result.append(v)
        return result
    A=[row(i) for i in CLOCK+[0,1]]
    A.append([box(kind=='M' and j==7)-y[7]*int(kind=='w' and j==7) for kind,j in keys])
    return keys,A


def pulses(y,w):
    from gemischt import COEFF,WINDOWS
    from quelle import hull
    from basisdaten import hull as old, box as old_box
    from zustand import check
    import rand
    check(y,w)
    records=[]
    for source in SOURCES:
        arm=rand.finite({i:old(*v.data()) for i,v in y.items()},
                        {i:old(*v.data()) for i,v in w.items()},COEFF,old_box(F(1,6)),WINDOWS,source,False)
        yn,wn=y.copy(),w.copy()
        for key,values in arm['future_and_endpoints'].items():
            j=int(key)
            yn[j]+=hull(*values['dY'])
            wn[j]+=hull(*values['dw'])
        check(yn,wn,source)
        d=hull(*arm['delta_Y_z'])
        dw=hull(*arm['future_and_endpoints']['16']['dw'])
        delta=(y[16]+d-y[15])*dw+w[16]*d
        records.append((delta,yn,wn))
    return records
