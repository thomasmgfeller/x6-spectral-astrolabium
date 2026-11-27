"""Independent reconstruction of layer coefficients and exact differences of the action."""
from collections import Counter
from klassen import DUST, S


def audit(rows,collar,exe,inputs,invoke):
    from wirkung import check
    first={}; methods=Counter(); comparisons=0
    # Give dust nonzero clocks and weights so that new mixed derivatives are exercised.
    fixed=dict(collar)
    for k,j in enumerate(DUST,1):
        y=(k-4)*(S//8); w=k*(S//16)
        fixed[j]=(y,y,w,w)
    for row in rows:
        span=row['span']
        bounds=dict(row['bounds'])
        if span is not None:
            bounds[21]=span
        for j in (16,18):
            lower=19*S*S
            for (i,k),c in row['coeff'].items():
                if k==j and c<0:
                    gap=max(0,bounds[j][1]-bounds[i][0])
                    lower+=c*gap*gap
            assert lower>=-100000*S*S
        if row['weight']=='0':
            fields=inputs(row,collar)
            fields[21][:2]=[0,0]
            raw=invoke(exe,row,fields,0,1,'order')
            got=[tuple(map(int,line.split())) for line in raw.splitlines()]
            assert len(got)==len(row['coeff']) and {(a,b):c for a,b,c in got}==row['coeff']
        # All one-relation cases, plus at least one case from each type of clock bound.
        key=(row['family'],row['weight'],row['method'])
        first.setdefault(key,row['id'])
        if row['distance']!=1 and first[key]!=row['id']:
            continue
        def call(dots,centers):
            fields=[[0,0,0,0] for j in range(22)]
            for j,v in dots.items():fields[j]=v.copy()
            for j,ab in zip(range(15,22),centers[:7]):fields[j][:2]=ab
            for j,ab in zip((16,18,19,21),centers[7:]):fields[j][2:]=ab
            return invoke(exe,row,fields,sector,1,'algebra')
        for sector in range(4):
            # The archived action checker calls its two occupation flags A0 and A+.
            # Actual order and coefficients are supplied explicitly for both families.
            comparisons+=check(call,row['coeff'],fixed,'A'+row['weight'],sector)
            methods[row['method']]+=1
    return dict(orders=sum(r['weight']=='0' for r in rows),action_entries=comparisons,
                action_sectors_by_method=dict(methods))
