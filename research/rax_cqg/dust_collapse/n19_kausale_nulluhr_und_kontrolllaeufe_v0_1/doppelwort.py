"""Rational search followed by a separate full stationarity and digit audit."""
from fractions import Fraction as F
from itertools import product

ZERO=(F(0),)*3
K=F(1,10**11)
V=F(1,10**14)
PULSE=F(1,10**6)
ROUTE='positive_bridge'


def scaled(bg,factor):
    from gemischt import PAST
    from zustand import check
    n,y,w=bg
    ww={i:(a if i in PAST else factor*a) for i,a in w.items()}
    check(y,ww)
    return n+'_'+str(factor),y,ww


def state(y,w,j,yh,full=False):
    from quelle import box
    from staubgeraet import solve,verify
    from wege import forward
    from nullreferenz import digit
    from kollision import midpoint
    vel=(box(0),box(yh*V),box(0))
    st=solve(y,w,j,vel,K,box(-K),ROUTE);q=(box(0),)*3
    h,a=verify(st,j,vel,K,box(-K),ROUTE,q) if full else forward(st,ROUTE,q,vel)
    word18=list(map(digit,[st['y'][18],h[0][18],h[1][18],q[0],q[1]]))
    word7=list(map(digit,[st['y'][7],*[h[i][7] for i in range(3)],*q]))
    assert all(type(code) is int for code in word18+word7)
    return (midpoint(st['y'][18]),midpoint(st['y'][17]),midpoint(a[1][18]),midpoint(st['w'][7]),
            word18,word7)


def solve_pair(A,B,both):
    from referenzwechsel import displaced
    from nullreferenz import digit
    from kollision import midpoint
    from zustand import gradients
    from gemischt import PAST
    alpha=F(0);ya=yb=F(0)
    for _ in range(6):
        ybkg,wbkg=displaced(B[1],B[2],alpha)
        ta,ha,aa,wa,*_=state(A[1],A[2],PULSE,ya)
        tb,hb,ab,wb,*_=state(ybkg,wbkg,0,yb)
        # Match the native receiver time and the h displacement; for both sites also
        # match v_h/w7, the added drift between receiver and memory on this track.
        ratio=wb/wa if both else F(-1)
        if abs(aa-ab*ratio)<F(1,1000):raise ValueError('degenerate transfer for this search')
        ya=F(round((tb-ta-hb+ha)/((aa-ab*ratio)*V)*10**6),10**6)
        yb=F(round(ya*ratio*10**6),10**6)
        alpha+=F(round((ta-tb)*10**18),10**18)
    # Rebuild, independently check *all* field equations, then read the actual digits.
    ybkg,wbkg=displaced(B[1],B[2],alpha)
    a=state(A[1],A[2],PULSE,ya,True);b=state(ybkg,wbkg,0,yb,True)
    ga,_=gradients(A[1],A[2]);gb,_=gradients(ybkg,wbkg)
    return {'background_A':A[0],'background_B_before_shift':B[0],
            'alpha_B':str(alpha),'weak_post_y_h':[str(ya),str(yb)],'max_abs_y':str(max(abs(ya),abs(yb))),
            'sources':[str(PULSE),'0'],'receiver_words':[a[4],b[4]],'late_words':[a[5],b[5]],
            'same_at_18':a[4]==b[4],'same_at_7':a[5]==b[5],'distinct_null_digits':[digit(A[1][18]),digit(ybkg[18])],
            'sender_weight_intervals':[A[2][16].data(),wbkg[16].data()],
            'early_momentum_difference_enclosures':[(ga[i]-gb[i]).data() for i in PAST]}


def run(previous,early):
    from proben import samples
    data=samples(previous,early)[0];bg={r[0]:r for r in data}
    local=[solve_pair(bg[name],bg[name],False) for name in ('reference','quarter')]
    dual=[]
    for factor in (F(1),F(1,2),F(1,4),F(1,8),F(1,16)):
        a=scaled(bg['G_-1/30'],factor);b=scaled(bg['G_1/30'],factor)
        dual.append(solve_pair(a,b,True))
    return {'local':local,'joint':dual,'position_and_other_momenta':'0'}
