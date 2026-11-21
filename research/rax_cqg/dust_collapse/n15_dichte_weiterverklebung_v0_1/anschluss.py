"""Recount causal intervals in the full appended order; check action and covariance."""
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent/'basis'/'port'))
import zertifikat as old

P,I,F = old.P,old.I,old.F
LAYERS=(1,-9,16,-8)


def weights(nodes,order):
    edges={}
    for i,j in order:
        k=sum((i,v) in order and (v,j) in order for v in nodes)
        if k<4:
            edges[i,j]=LAYERS[k]
    return edges


def dust(nodes,edges,y,w):
    return -(sum(w[j] for j in nodes)+sum(b*w[j]*(y[i]-y[j])**2 for (i,j),b in edges.items())/19)/2


def scalar_pairs(edges,q):
    # Test the endpoint dependence of the quadratic pair sum; its overall
    # coupling and fixed geometry factor do not involve the old density.
    return sum(b*(q[i]-q[j])**2 for (i,j),b in edges.items())


def orders():
    for label,new,inside in [('ein_ereignis',(15,),()),('kette',(15,16),((15,16),)),
                             ('antikette',(15,16),())]:
        old_nodes=tuple(range(15))
        order=old.ORDER | set(product(old_nodes,new)) | set(inside)
        yield label,old_nodes,new,order


def check_caps():
    results={}
    pair,_=old.centers()
    for label,before,new,rel in orders():
        nodes=before+new
        full=weights(nodes,rel)
        pre=weights(before,old.ORDER)
        assert {k:v for k,v in full.items() if k[1] in before}==pre
        extra={k:v for k,v in full.items() if k[1] in new}
        assert all(i in F+new for i,j in extra)
        for j in new:
            n=sum((v,j) in rel for v in new)
            expect=tuple(LAYERS[3-i+n] if 3-i+n<4 else 0 for i in range(4))
            assert tuple(extra.get((f,j),0) for f in F)==expect
        for yc,wc in pair.values():
            y=dict(yc)|{j:Q(j-8) for j in new}
            w=dict(wc)|{j:Q(1,9+j-15) for j in new}
            q={j:Q(j*j-7,13) for j in nodes}
            for offset in (0,Q(1,2**20),-Q(1,2**20)):
                # W=w/Delta in the normalized action. The coefficient test
                # above is independent of this sampling scale.
                ww=w|{7:w[7]+offset}
                direct=dust(nodes,full,y,ww)-dust(before,pre,y,ww)
                assert direct==dust(new,extra,y,ww)
                assert scalar_pairs(full,q)-scalar_pairs(pre,q)==scalar_pairs(extra,q)
            sensitive=[j for j in new if (7,j) in extra]
            assert sensitive  # old clock Y7 can enter even though old density cannot
        results[label]={'neue_ziele':new,'neue_nichtverschwindende_paare':len(extra),
            'gewichte_vom_alten_zukunftsrand':{j:tuple(extra.get((f,j),0) for f in F) for j in new},
            'alte_dichten_in_neuen_termen':0}
    return results


def one_birth():
    # Every downward-closed predecessor set gives one labelled one-birth
    # extension. Compare the pair tables before integrating anything.
    before=tuple(range(15))
    pre=weights(before,old.ORDER)
    ideals=[frozenset()]
    for j in P+(4,5,6,11,12,13,14)+F:
        past={i for i,k in old.ORDER if k==j}
        ideals += [s|{j} for s in ideals if past<=s]
    assert len(ideals)==len(set(ideals))==28
    screened=[]
    for s in ideals:
        rel=old.ORDER|{(i,15) for i in s}
        full=weights(before+(15,),rel)
        assert {k:v for k,v in full.items() if k[1]!=15}==pre
        sources={i for i,j in full if j==15}
        if sources<=set(F):
            screened.append(sorted(s))
    return {'praekursorideale':len(ideals),'dichte_w7_in_der_zusatzwirkung':0,
            'nur_alter_zukunftskragen_oder_keine_quellen':screened}


def check_covariance():
    pair,ref=old.centers()
    # All interleavings of the inner chains of lengths 3 and 4, with the
    # entrance and future chains preserved; also rename the boundary numerals.
    a,b=old.CHAINS
    nodes=tuple(range(15))
    y,_=pair['positiv']
    direct=weights(nodes,old.ORDER)
    d0=-(1+sum(Q(q,19)*(y[i]-y[7])**2 for (i,j),q in direct.items() if j==7))/2
    passed=0
    for positions in combinations(range(7),len(a)):
        aa,bb=iter(a),iter(b)
        inner=tuple(next(aa) if k in positions else next(bb) for k in range(7))
        ordering=P+inner+F
        # Distinct external names, determined by birth ranks, not old numbers.
        rename={j:101+17*n for n,j in enumerate(ordering)}
        new=tuple(rename.values())
        rel={(rename[i],rename[j]) for i,j in old.ORDER}
        coeff=weights(new,rel)
        assert all(coeff.get((rename[i],rename[j]),0)==q for (i,j),q in old.B.items())
        future=tuple(rename[f] for f in F)
        lower=[j for j in future if all((k,j) not in rel for k in future)]
        assert lower==[rename[7]]
        point=lower[0]
        for offset in (Q(0),Q(3,7)):
            yy={rename[j]:v+offset for j,v in y.items()}
            value=-(1+sum(Q(q,19)*(yy[i]-yy[point])**2 for (i,j),q in coeff.items() if j==point))/2
            assert value==d0
        passed+=1
    assert passed==35
    return {'geburtsreihenfolgen':passed,'gemeinsame_uhrverschiebungen':['0','3/7'],
            'markierung':'einziges minimales Ereignis des mittransportierten Zukunftskragens'}


def classical():
    pair,_=old.centers()
    out={}
    for name,(yc,_) in pair.items():
        y={j:old.box(v,old.RADIUS if j in I+(3,) else old.H if j in F[1:] else 0) for j,v in yc.items()}
        c=old.coefs(y)
        assert c[4][0]>Q(58,1000) and c[7][0]>Q(67,10)
        out[name]={j:c[j] for j in I+(7,)}
    return out
