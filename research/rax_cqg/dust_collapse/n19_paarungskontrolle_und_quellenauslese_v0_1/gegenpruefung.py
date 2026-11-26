"""Independent native-row and history-identification controls."""
from fractions import Fraction as F
from itertools import combinations
import json

from leser import PROBES,old_clocks,read
from proben import samples


def run(previous,early):
    from gemischt import ORDER,COEFF,FUT,WINDOWS
    from quelle import box
    from felder import pulses
    from algebra import gauss_box
    from zustand import check
    edges={}
    for i,j in ORDER:
        depth=sum((i,k) in ORDER and (k,j) in ORDER for k in range(19))
        if depth<4:
            edges[i,j]=(1,-9,16,-8)[depth]
    assert edges=={ij:c for ij,c in COEFF.items() if c}
    layers=[edges.get((12,j),0) for j in FUT]
    assert layers==[-9,16,-8,0]==[edges.get((13,j),0) for j in FUT]
    assert {ij for ij in edges if ij[1]==18}=={(1,18),(2,18),(15,18),(16,18),(17,18)}
    assert [edges[i,18] for i in (1,2,15,16,17)]==[-8,16,-9,1,1]
    assert sorted((i,v) for (i,j),v in edges.items() if j==16)==[(0,-8),(1,16),(2,-9),(15,1)]
    fixtures,_=samples(previous,early)
    def predict(y,w):
        old=old_clocks({i:y[i] for i in range(4)},edges,ORDER)
        assert all((t-y[i]).contains_zero() for i,t in old.items())
        return read(old,{i:w[i] for i in PROBES},y[15],y[17],edges,ORDER,WINDOWS)
    def overlap(a,b):
        return (a-b).contains_zero()
    tags={}
    for name,y,w in fixtures:
        pred=predict(y,w)
        tags[name]=pred['arms'][0]['delta']
        # Use true fields in this independent audit, after prediction.
        for yy,ww in [(y,w)]+[(yy,ww) for _,yy,ww in pulses(y,w)]:
            W=sum(v*ww[j] for j,v in zip(FUT,layers))
            M=sum(v*ww[j]*yy[j] for j,v in zip(FUT,layers))
            assert overlap(W,pred['W']) and overlap(M,pred['M'])
            def rhs(i):
                incoming=sum(c*(yy[i]-yy[j]) for (j,k),c in edges.items() if k==i)
                known=sum(c*ww[j]*(yy[j]-yy[i]) for (k,j),c in edges.items()
                          if k==i and j not in FUT and j!=14)
                return ww[i]*incoming-known
            A=[[box(0),box(0),edges[4,14]*(yy[14]-yy[4])]]
            A.extend([[-yy[i],box(1),edges[i,14]*(yy[14]-yy[i])] for i in (12,13)])
            solved=gauss_box(A,[rhs(i) for i in (4,12,13)])
            assert all(overlap(a,b) for a,b in zip(solved,(pred['W'],pred['M'],ww[14])))
    pair_count=sum(not overlap(x,z) for x,z in combinations(tags.values(),2))
    assert pair_count==66

    # Change only the four future weights and their moments. The clock equations
    # stay invariant because three layer rows annihilate this direction and
    # the remaining row acts on delta(wY)-Y6*delta(w).
    _,y,w=fixtures[0]
    amplitude=F(1,10**9)
    direction=[F(1),F(2),F(23,8),F(29,8)]
    shifted_y=y.copy()
    shifted_w=w.copy()
    for i in (11,12,14):
        assert sum(edges.get((i,j),0)*d for j,d in zip(FUT,direction))==0
    for j,d in zip(FUT,direction):
        dw=amplitude*d
        shifted_w[j]+=dw
        shifted_y[j]=(w[j]*y[j]+dw*y[6])/shifted_w[j]
        assert not overlap(shifted_w[j],w[j])
    check(shifted_y,shifted_w)
    same=predict(shifted_y,shifted_w)
    assert same['arms'][0]['delta'].data()==tags[fixtures[0][0]].data()
    for src,alt in zip(pulses(y,w),pulses(shifted_y,shifted_w)):
        assert overlap(src[0],alt[0]) and not overlap(src[2][7],alt[2][7])
    return {'native_rows_checked_per_solution':[4,12,13],'stationary_solutions_checked':3*len(fixtures),
            'distinct_tags_among_66_pairs':pair_count,
            'same_tag_distinct_history':{'future_weight_shift':list(map(str,[amplitude*d for d in direction])),
                'future_moment_shift_per_weight':'Y6','identical_T':same['arms'][0]['delta'].data(),
                'two_pulses_checked':True}}


if __name__=='__main__':
    from vorgaenger import inputs
    with inputs() as args:
        print(json.dumps(run(*args),indent=2,sort_keys=True))
