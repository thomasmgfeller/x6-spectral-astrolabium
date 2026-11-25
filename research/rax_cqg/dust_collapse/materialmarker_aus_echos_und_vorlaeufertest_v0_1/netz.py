"""Select a pair and its direction using only the complete echo graph on material probes."""
from itertools import combinations, permutations
from hashlib import sha256
from fractions import Fraction as F
from echos import IDS,MASS,TARGET,TICK,FACTORS,echo_bounds,measured_echo,decode,contained,late,material_profile,locate

def edge(i,j):return tuple(sorted((i,j)))
def topology(accepted,durations):
    if len(accepted)!=1:return ('KEIN_PAAR' if not accepted else 'MEHRERE_PAARE',)
    i,j=next(iter(accepted))
    weights={v:sum(n for pair,n in durations.items() if v in pair and pair!=(i,j)) for v in (i,j)}
    if weights[i]==weights[j]:return ('UNORIENTIERT',)
    return (i,j) if weights[i]>weights[j] else (j,i)

def select_graph(durations,ratio):
    accepted={p for p,n in durations.items() if contained(decode(n,ratio,F(0)))}
    return topology(accepted,durations)

def run():
    result={}; records={}
    codes=('D',*sorted(IDS,key=lambda x:sha256(('Kennung|'+x).encode()).digest()))
    factors=dict(zip(codes,(F(0),*FACTORS)))
    for m in MASS:
        j=locate(material_profile(m));a=F(13*j,640);ratio=a/10
        durations={};bounds={};certain=set();possible=set()
        for v,w in combinations(codes,2):
            p=edge(v,w)
            theta=abs(factors[v]-factors[w])*TARGET
            l,h=echo_bounds(a,theta)
            n=measured_echo(a,m,theta)
            assert l<=n<=h
            durations[p]=n;bounds[p]=(l,h)
            num=sum(contained(decode(k,ratio,0)) for k in range(l,h+1))
            if num:possible.add(p)
            if num==h-l+1:certain.add(p)
        assert possible==certain and len(certain)==1
        i,j=select_graph(durations,ratio)
        assert factors[i]==0 and factors[j]==1
        pair=edge(i,j)
        low_first=sum(l for p,(l,h) in bounds.items() if i in p and p!=pair)
        high_second=sum(h for p,(l,h) in bounds.items() if j in p and p!=pair)
        assert low_first>high_second
        # Edge predicates depend only on the echo values. Test every renaming
        # after this stage, including direction selection from the renamed graph.
        for names in permutations(codes):
            rename=dict(zip(codes,names))
            new={edge(rename[v],rename[w]):n for (v,w),n in durations.items()}
            good={edge(rename[v],rename[w]) for v,w in certain}
            assert topology(good,new)==(rename[i],rename[j])
        # Removing all calibrated edges, adding a second, or erasing direction.
        n=durations[pair]
        assert select_graph({('a','b'):n//3},ratio)==('KEIN_PAAR',)
        assert select_graph({('a','b'):n,('a','c'):n,('b','c'):n//3},ratio)==('MEHRERE_PAARE',)
        assert select_graph({('a','b'):n},ratio)==('UNORIENTIERT',)
        l,h=bounds[pair]; angle=(decode(l,ratio,0)[0],decode(h,ratio,0)[1])
        result[str(m)]={'mat_station':492,'unique_undirected_pair':list(pair),'orientation':[i,j],
                        'min_direction_score_gap_ticks':low_first-high_second,'permutations':5040,
                        'late_positive_station':late(m,a,angle),'late_support':late(m,F(10),angle)}
        records[str(m)]={'ticks':{'|'.join(p):v for p,v in sorted(durations.items())},
                         'bounds':{'|'.join(p):v for p,v in sorted(bounds.items())}}
    return result,records
if __name__=='__main__':print(run()[0])
