"""Search with rational midpoint iterations; certify identical complete digit packets independently."""
from fractions import Fraction as F
from itertools import product
from empfangsbit import R,STEP,K0,V,receiver_bit,late_code,classify


def midpoint(x):
    from quelle import SCALE
    return F(x.lo+x.hi,2*SCALE)


def round_to(x,den=1000):
    return F(round(x*den),den)


def outputs(y,w,route,J,ys,verify_all=False):
    from quelle import box
    from staubgeraet import solve,verify
    from wege import forward
    from nullreferenz import digit
    vel=tuple(box(V*u) for u in ys);q=(box(0),)*3
    st=solve(y,w,J,vel,K0,box(-K0),route)
    h,A=(verify(st,J,vel,K0,box(-K0),route,q) if verify_all else forward(st,route,q,vel))
    word=[digit(st['y'][7]),*[digit(a[7]) for a in h],0,0,0]
    return word,[midpoint(a[7]) for a in h],[midpoint(a[7]) for a in A],digit(st['y'][18])


def search(y,w,route,j1,j2):
    from nullreferenz import digit
    base=digit(y[18])
    initial=[outputs(y,w,route,j,[0]*3) for j in (j1,j2)]
    target=[STEP*round((a+b)/(2*STEP)) for a,b in zip(initial[0][1],initial[1][1])]
    arms=[]
    for j in (j1,j2):
        vel=[F(0)]*3
        for _ in range(6):
            word,mid,coeff,clk=outputs(y,w,route,j,vel)
            if all(a==round(b/STEP) for a,b in zip(word[1:4],target)):break
            vel=[round_to(f+(goal-cur)/(gain*V)) for f,goal,cur,gain in zip(vel,target,mid,coeff)]
        word,_,_,clk=outputs(y,w,route,j,vel,verify_all=True)
        assert all(type(x) is int for x in word) and word[1:4]==[round(b/STEP) for b in target]
        bit=receiver_bit(clk,base);late=late_code(word[0],word[3],word[-1],base)
        arms.append(dict(J=str(j),y=[str(f) for f in vel],late_word=word,receiver_clock=clk,
                         transmitted_bit=bit,late_clock_difference=late,one_bit_label=str(classify(bit,late))))
    assert arms[0]['late_word']==arms[1]['late_word']
    return arms


def run(previous,early):
    from proben import samples
    from wege import ROUTES
    from uhrauslese import LABELS
    rows=[]
    for (name,y,w),route,pair in product(samples(previous,early)[0],ROUTES,zip(LABELS,LABELS[1:])):
        arms=search(y,w,route,*pair)
        cap=max(abs(F(z)) for arm in arms for z in arm['y'])
        rows.append(dict(background=name,route=route,arms=arms,max_abs_y=str(cap)))
    return rows
