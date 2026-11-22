"""Exact cross-cut data and source insertions for the published total order."""
from fractions import Fraction as F
from itertools import combinations, product

PAST=(0,1,2,3)
INNER=(4,5,6,11,12,13,14)
FUTURE=(7,8,9,10)
ORDER=PAST+INNER+FUTURE
LAYERS=(1,-9,16,-8)
A,B=11,13

def pairs_from_intervals():
    precedes=set(combinations(ORDER,2))
    weights={}
    for i,j in precedes:
        n=sum((i,k) in precedes and (k,j) in precedes for k in ORDER)
        if n<len(LAYERS):
            weights[i,j]=LAYERS[n]
    return weights

def links_to(rank):
    """Local forward recurrence. Keep the last four earlier events."""
    return [(ORDER[rank-lag],LAYERS[lag-1]) for lag in range(1,min(rank,4)+1)]

def source_parts(edges):
    visible={};hidden={};p=dict(zip(PAST,(76,47,24,8)))
    for j in ORDER:
        v=F(0); h=F(0)
        for (i,end),b in edges.items():
            if end!=j:
                continue
            d1=int(j==A)-int(i==A);d2=int(j==B)-int(i==B)
            h+=b*(d1*d1+F(10,9)*d1*d2-15*d2*d2)
            v-=F(b,64)*(int(j in PAST)-int(i in PAST))*(p.get(j,0)-p.get(i,0))
        h+={7:-127,8:240,9:-120}.get(j,0)
        visible[j]=v;hidden[j]=h
    return visible,hidden

def determinant(matrix):
    if not matrix:return 1
    return sum((-1)**k*v*determinant([row[:k]+row[k+1:] for row in matrix[1:]])
               for k,v in enumerate(matrix[0]))

def exact():
    edges=pairs_from_intervals()
    assert edges=={(i,j):b for k,j in enumerate(ORDER) for i,b in links_to(k)}
    v,h=source_parts(edges)
    assert [j for j in ORDER if v[j]]==list(INNER[:4])
    assert [j for j in ORDER if h[j]]==list(INNER[4:])
    assert all(v[j]+h[j]==int(j in INNER) for j in ORDER)
    blocks=(ORDER[:8],ORDER[8:10],ORDER[10:])
    splits=[[sum(1 for i,j in edges if i in left and j in right) for right in blocks] for left in blocks]
    assert sum(map(sum,splits))==len(edges)
    assert edges[A,B]==-9
    cut=8
    past=ORDER[cut-4:cut]; future=ORDER[cut:cut+3]
    # Active fields in the interior of the right clock window at e=1/4.
    e=F(1,4);duration=4-e
    u={j:F(k+1,8) for k,j in enumerate(INNER)}
    y={j:F(-2)+e+duration*t for j,t in u.items()}
    w={j:4*duration*F(1,8) for j in INNER}
    w[4]=w[14]=4*duration*F(3,16)
    # The five interior shares are 1/8; the two terminal shares are 3/16.
    cols=[[F(edges.get((i,j),0),19)*w[j] for i in past] for j in future]
    cols.append([F(edges.get((i,12),0),19)*(y[12]-y[i]) for i in past])
    matrix=list(map(list,zip(*cols)))
    det=determinant(matrix)
    assert det!=0
    # A four-point action difference on fixed fields isolates precisely the crossing edge.
    step=F(1,256)
    yy={j:F(k,3) for k,j in enumerate(ORDER)}
    ww={j:F(j+1,23) for j in ORDER}
    pieces={}
    for b1,b2 in product((-1,1),repeat=2):
        shifted=yy.copy();shifted[A]+=b1*step;shifted[B]+=b2*step
        terms=[-sum(ww[j] for j in group)/2 for group in blocks]
        for (i,j),coef in edges.items():
            k=next(k for k,group in enumerate(blocks) if j in group)
            terms[k]-=F(coef,38)*ww[j]*(shifted[j]-shifted[i])**2
        direct=-sum(ww.values())/2-sum(F(c,38)*ww[j]*(shifted[j]-shifted[i])**2 for (i,j),c in edges.items())
        assert direct==sum(terms);pieces[b1,b2]=terms
    mixed=[-19*sum(b1*b2*terms[k] for (b1,b2),terms in pieces.items())/(4*step**2) for k in range(3)]
    assert mixed==[0,9*ww[B],0]
    return dict(order=ORDER,blocks=blocks,active_pairs=len(edges),pair_counts=splits,mixed_cross_coefficient=edges[A,B],
                partial_responses=mixed,visible=v,hidden=h,cut_past=past,cut_columns=['Y12','Y13','Y14','W12'],
                rank_witness=matrix,rank_determinant=det,rank=4)

def discrete_control():
    """Two allowed density assignments at identical clocks. Their amplitude weights are 2:1."""
    e=F(1,4);du=4-e
    y={j:F(j-5) for j in PAST+FUTURE};y[3]+=e
    y.update({j:y[3]+du*F(k+1,8) for k,j in enumerate(INNER)})
    # Symmetric +/- half a jitter width on the sixth inner event.
    change_W=4*du*F(1,8)*F(1,100)
    g=F(-1,2);ga=gb=F(0)
    for (i,j),c in pairs_from_intervals().items():
        if j!=B:continue
        diff=y[j]-y[i];g-=F(c,38)*diff**2
        ga-=F(c,19)*diff*(int(j==A)-int(i==A))
        gb-=F(c,19)*diff*(int(j==B)-int(i==B))
        assert i not in PAST
    # alpha = Delta*phase_coefficient and Q(delta J) = Delta*q_coefficient.
    phase_coefficient=g*change_W
    q_coefficient=(ga*ga+F(10,9)*ga*gb-15*gb*gb)*change_W**2/du
    assert q_coefficient and phase_coefficient and abs(phase_coefficient)<1
    assert F(1,4)**4 < F(3,722) < F(1,3)**4
    # Im[p1 p2] = 6 sin(alpha)/(5+4 cos(alpha))². For |alpha|<1
    # use |sin(alpha)| >= |alpha|(1-alpha²/6), cos(alpha) in [1/2,1].
    lo=19*F(1,4)*abs(q_coefficient)*6*F(1,4)*abs(phase_coefficient)*F(5,6)/81
    hi=19*F(1,3)*abs(q_coefficient)*6*F(1,3)*abs(phase_coefficient)/49
    return dict(phase_difference_in_delta_units=phase_coefficient,
                quadratic_score_difference_in_delta_units=q_coefficient,
                sign_of_mass_difference=1 if phase_coefficient*q_coefficient>0 else -1,
                absolute_mass_difference_bounds=[lo,hi])
