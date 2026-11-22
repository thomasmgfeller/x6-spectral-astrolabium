"""Interval propagation with only a causal time ordering, independent of inner windows."""
from basis import Q,PAST,INNER,EDGES
from stationaer import DELTA,box
from intervalle import I,S
from collections import Counter

def test(a,b):
    e=box(a,b)/DELTA;fields={j:I.of(j-5) for j in PAST};fields[3]+=e;last=fields[3]
    for pos,j in enumerate(INNER,1):
        inc={i:w for (i,k),w in EDGES.items() if j==k};B=sum((w*fields[i] for i,w in inc.items()),I.of(0));N=19+sum((w*fields[i]**2 for i,w in inc.items()),I.of(0));bounds=I(last.lo,2*S);res=N-2*B*bounds
        if res.lo>0 or res.hi<0:return pos
        if B.lo<=0<=B.hi:return 0
        y=N/(2*B);lo=max(y.lo,last.lo);hi=min(y.hi,2*S)
        if lo>hi:return pos
        last=fields[j]=I(lo,hi)
    return 0

def run():
    out={}
    for side,mid in [('left',Q(-1,16)),('right',Q(1,16))]:
        groups=Counter();lengths=Counter();deep=0;open_ranges=[]
        def check(a,b,depth):
            nonlocal deep
            deep=max(depth,deep);k=test(a,b)
            if k or depth==14:
                groups[k]+=1;lengths[k]+=b-a
                if not k:
                    if open_ranges and open_ranges[-1][1]==a:open_ranges[-1][1]=b
                    else:open_ranges.append([a,b])
            else:
                c=(a+b)/2;check(a,c,depth+1);check(c,b,depth+1)
        check(mid-Q(1,32),mid+Q(1,32),0);assert sum(lengths.values())==Q(1,16)
        out[side]={'tiles_by_first_certified_failure':dict(groups),'covered_offset_length_by_step':dict(lengths),'deepest_subdivision':deep,'open_offset_intervals':open_ranges}
    return out
if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2,sort_keys=True,default=str))
