"""One-dimensional outer cover for the regular sector of the certified witness order."""
from fractions import Fraction as F
from klassen import S


def intersect_fields(row,fields,sector):
    assert row['id']=='216141/229383/0/+'
    incoming=lambda j: {a:c for (a,b),c in row['coeff'].items() if b==j}
    assert incoming(16)=={0:-8,1:16,2:-9,15:1}
    assert incoming(19)=={1:-8,2:16,15:-9,16:1}
    assert incoming(18)=={**incoming(19),17:1,20:1}
    outgoing=lambda j:{b:c for (a,b),c in row['coeff'].items() if a==j}
    assert outgoing(17)==outgoing(20)=={7:-9,8:16,9:-8,18:1,21:1}
    assert all(fields[i][:2]==[x*S,x*S] for i,x in enumerate((-5,-4,-3)))
    if sector & 1:
        return fields,None
    tolerance=F(2001,S)
    tlo,thi=[3+F(x,S) for x in fields[19][:2]]
    # D16=u²-2uv+3, D19=11+(18u-2v-16)t-9u²+v².
    # These coefficient checks sample the polynomials on a unisolvent tensor grid.
    for u in (1,2,3):
        for v in (2,3,4):
            for t in (3,4,5):
                y={0:-5,1:-4,2:-3,15:u-3,16:v-3,19:t-3}
                def density(j):return 19+sum(c*(y[j]-y[i])**2 for i,c in incoming(j).items())
                assert density(16)==u*u-2*u*v+3
                assert density(19)==11+(18*u-2*v-16)*t-9*u*u+v*v
    assert (2,15) in row['edges'] and (15,16) in row['edges'] and (16,19) in row['edges']
    # 0<u<v<t. Thus 2u t > 3-tolerance and u²<3+tolerance.
    low,high=F(2,5),F(7,4)
    assert low<(3-tolerance)/(2*thi) and high*high>3+tolerance
    todo=[(low,high)]
    kept=[]
    while todo:
        a,b=todo.pop()
        c,d=a/2+(3-tolerance)/(2*b), b/2+(3+tolerance)/(2*a)
        slopes=18*a-2*d-16,18*b-2*c-16
        terms=[x*t for x in slopes for t in (tlo,thi)]
        lower=11+min(terms)-9*b*b+c*c
        upper=11+max(terms)-9*a*a+d*d
        if not lower<=0<=upper:
            continue
        if b-a <= F(1,20000):
            kept.append((a,b,c,d))
        else:
            mid=(a+b)/2
            todo.extend(((a,mid),(mid,b)))
    assert kept
    result=[f.copy() for f in fields]
    limits={}
    for k,j in ((0,15),(2,16)):
        a=min(v[k] for v in kept)-3
        b=max(v[k+1] for v in kept)-3
        limits[j]=(a*S//1,-(-b*S//1))
        result[j][0]=max(result[j][0],limits[j][0])
        result[j][1]=min(result[j][1],limits[j][1])
    return result,limits
