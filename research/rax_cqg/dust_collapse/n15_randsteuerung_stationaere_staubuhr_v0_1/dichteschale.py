"""Test the density-stationarity equations chronologically on the full clock support."""
from basis import PAST,INNER,EDGES,Q
from stationaer import DELTA,box
from intervalle import I,S

def certify(tile):
    e=tile/DELTA;length=4-e;y={j:I.of(j-5) for j in PAST};y[3]+=e
    for pos,node in enumerate(INNER[:2],1):
        inc={i:b for (i,j),b in EDGES.items() if j==node};assert len(inc)==4 and sum(inc.values())==0
        # N - 2 B Y_j = 0, no Y_j^2. Test the whole clock window before inversion.
        B=sum((b*y[i] for i,b in inc.items()),I.of(0));N=19+sum((b*y[i]**2 for i,b in inc.items()),I.of(0));window=y[3]+length*box(Q(pos,8)-Q(1,64),Q(pos,8)+Q(1,64));res=N-2*B*window
        if res.lo>0 or res.hi<0:return pos,res
        if B.lo<=0<=B.hi:return 0,None
        forced=N/(2*B);lo=max(forced.lo,window.lo);hi=min(forced.hi,window.hi)
        if lo>hi:
            gap=I(lo-hi,lo-hi);return -pos,gap
        y[node]=I(lo,hi)
    return 0,None

def run():
    result={}
    for name,mid in [('left',Q(-1,16)),('right',Q(1,16))]:
        n=256; counts={}; minima={};records=[]
        for i in range(n):
            a=mid-Q(1,32)+Q(i,16*n);b=a+Q(1,16*n);stage,val=certify(box(a,b));counts[stage]=counts.get(stage,0)+1
            if val is not None:
                m=min(abs(val.lo),abs(val.hi));minima[stage]=min(minima.get(stage,m),m)
            if not records or records[-1]['step']!=stage:records.append({'step':stage,'start':str(a),'end':str(b)})
            else:records[-1]['end']=str(b)
        result[name]={'tiles':n,'counts':counts,'ranges':records,'certificate_min_abs':{j:I(v,v).rounded(8)[0] for j,v in minima.items()}}
    return result
if __name__=='__main__':
    import json
    print(json.dumps(run(),indent=2,sort_keys=True))
