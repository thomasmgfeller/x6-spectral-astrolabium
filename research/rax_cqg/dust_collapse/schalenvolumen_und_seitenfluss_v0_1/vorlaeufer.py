"""One positive predecessor and one later vacuum event at the middle cut."""
from erweiterung import *

def run():
    ext=[(p,f) for p,f,_ in extensions() if p and f]
    stats=Counter();samples=[];closest=None;unresolved=[]
    for p,f in ext:
        for pv,fv in ext:
            if not (p<=pv and fv<=f):continue
            r=R|{(u,16) for u in p}|{(16,v) for v in f}|{(u,Z) for u in pv}|{(Z,v) for v in fv}|{(16,Z)}
            succ=[0]*17
            for i,j in r:succ[i]|=1<<j
            assert all(not(succ[i] & (1<<i)) for i in range(17))
            assert all(succ[j] & ~succ[i]==0 for i,j in r)
            stats['orders']+=1
            rows,unknown=solve(r,box(F(1,6)),box(F(1,2)),False,True)
            if unknown:unresolved.append([sorted(p),sorted(f),sorted(pv),sorted(fv),unknown])
            if rows:
                stats['candidate_orders']+=1
                checked,other=solve(r,box(F(1,6)),box(F(1,2)),True,True)
                assert checked==rows and other==unknown
            for val in rows:
                lo,hi=map(F,val['flux'])
                sign='positive' if lo>0 else 'negative' if hi<0 else 'possibly_zero'
                stats[sign]+=1
                dist=max(lo,-hi,F(0))
                descriptor=[sorted(p),sorted(f),sorted(pv),sorted(fv)]
                if closest is None or dist<closest[0]:
                    closest=(dist,descriptor,val)
                if sign=='possibly_zero' or val['bounds_only']:samples.append([descriptor,val])
    # Full independent action difference at the least separated candidate.
    if closest is not None:
        dist,desc,_=closest
        p,f,pv,fv=desc
        r=R|{(u,16) for u in p}|{(16,v) for v in f}|{(u,Z) for u in pv}|{(Z,v) for v in fv}|{(16,Z)}
        repeat,_=solve(r,box(F(1,6)),box(F(1,2)),True,True)
        assert closest[2] in repeat
    return {'counts':dict(stats),'open':unresolved,'ambiguous':samples,
            'nearest':None if closest is None else [str(closest[0]),closest[1],closest[2]]}
