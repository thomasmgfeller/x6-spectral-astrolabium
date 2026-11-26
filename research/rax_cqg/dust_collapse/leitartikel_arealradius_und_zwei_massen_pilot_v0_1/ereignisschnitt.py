"""Necessary vertex condition for a direct material 2-sphere at the target cut."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import sys

BASE=Path(__file__).resolve().parent/'basis'
sys.path.insert(0,str(BASE))
from quellenpaket import model


def subsets(order,nodes,k):
    return [s for s in combinations(sorted(nodes),k)
            if all((a,b) not in order and (b,a) not in order for a,b in combinations(s,2))]


def extend(order,nodes):
    """Generate antichains by inserting one event into compatible smaller sets."""
    families=[()]
    for v in sorted(nodes):
        families += [s+(v,) for s in families if all((u,v) not in order and (v,u) not in order for u in s)]
    return families


def distances(state):
    y=state['y']
    den=y[7]-y[3]
    assert den.lo>0
    result={}
    for k,t in y.items():
        c=(t-y[3])/den
        l,h=map(F,c.data())
        lo=max(F(0),l-F(1,2),F(1,2)-h)
        hi=max(abs(l-F(1,2)),abs(h-F(1,2)))
        result[k]=(lo,hi)
    return result


def mesh_audit(archived):
    with model() as (_,__,prev,early):
        from gemischt import ORDER
        from quelle import box,hull
        from modell import setup
        from staubgeraet import solve,verify
        from empfangsbit import K0,STEP,V
        from referenzwechsel import displaced
        from driftfamilie import LABELS, LIMIT
        y,w=setup(prev,early)
        nodes=set(y)
        assert nodes==set(range(19))
        material={v for v in nodes if w[v].lo>0}
        assert nodes-material=={15,17}
        families=extend(ORDER,material)
        four=subsets(ORDER,material,4)
        assert sorted(four)==sorted(s for s in families if len(s)==4)
        width=max(map(len,families))
        assert len(ORDER)==len(set(ORDER))
        assert all((a,c) in ORDER for a,b in ORDER for v,c in ORDER if b==v)
        for i,j in combinations(nodes,2):
            swap={i:j,j:i}
            p=lambda v:swap.get(v,v)
            rel={(p(a),p(b)) for a,b in ORDER}
            new=subsets(rel,{p(n) for n in material},4)
            assert set(new)=={tuple(sorted(p(n) for n in s)) for s in four}
        v=(hull(-112*V,112*V),)*3
        q=(hull(-1,1),)*3
        future=sorted(i for i in nodes if (18,i) in ORDER)
        earliest=[i for i in future if not any((other,i) in ORDER for other in future)]
        assert (16,18) in ORDER and not any((16,i) in ORDER and (i,18) in ORDER for i in nodes)
        assert earliest==[7] and all((7,i) in ORDER for i in future if i!=7)
        rows=[]
        leaves=[tuple(map(F,c['delta'])) for c in archived['leaves']]
        assert leaves[0][0]==-LIMIT and leaves[-1][1]==LIMIT
        assert all(a<b for a,b in leaves) and all(a[1]==b[0] for a,b in zip(leaves,leaves[1:]))
        for l,h in leaves:
            yy,ww=displaced(y,w,hull(6*STEP+l,6*STEP+h))
            for j in LABELS:
                st=solve(yy,ww,j,v,K0,box(-K0),'positive_bridge')
                verify(st,j,v,K0,box(-K0),'positive_bridge',q)
                assert all(st['w'][i].lo>0 for i in material)
                assert all(st['w'][i].lo==st['w'][i].hi==0 for i in nodes-material)
                d=distances(st)
                # For every true point of this cell enclose min_S max_{i in S}|x_i-1/2|.
                row={'delta':list(map(str,(l,h))),'source':str(j)}
                if four:
                    lower=min(max(d[i][0] for i in s) for s in four)
                    upper,witness=min((max(d[i][1] for i in s),s) for s in four)
                    row.update(half_width_lower=str(lower),half_width_upper=str(upper),upper_witness=witness)
                rows.append(row)
        result={'positive_events':sorted(material),'order_relations':len(ORDER),
                'antichain_counts':{str(k):sum(len(s)==k for s in families) for k in range(width+1)},
                'max_width':width,'four_vertex_sets':[list(s) for s in four],
                'relabel_transpositions':len(list(combinations(nodes,2))),'cells':rows,
                'return_probe':{'send':16,'reflection_candidate':18,'future_of_18':future,
                                'first_possible_node':7,'first_possible_x':'1',
                                'same_material_worldline_certified':False},
                'time_definition':'x=(Y_i-Y_3)/(Y_7-Y_3) using each solution'}
        if four:
            result['global_lower']=str(min(F(row['half_width_lower']) for row in rows))
            result['global_upper']=str(max(F(row['half_width_upper']) for row in rows))
        return result
