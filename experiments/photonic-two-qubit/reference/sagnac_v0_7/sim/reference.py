"""Independent batch specification: bin membership from integer division.

It does not simulate the RTL state machine, latency or backpressure.
"""
from collections import Counter, defaultdict

def reference(start, stop, width, events, cal=7, bits=64):
    flags=0; last=start; groups=defaultdict(list); final=False
    if stop<=start or (stop-start)%width:
        return [0]*24,1<<4
    for kind,t,cid,err in events:
        if final: break
        if err: flags |= 1<<2
        if kind>4: flags |= 1<<5; continue
        if cid!=cal: flags |= 1<<3; continue
        if t<last: flags |= 1<<1; continue
        last=t
        if kind==4:
            if t>=stop: final=True
            continue
        if not start<=t<stop:
            flags |= 1<<5; continue
        groups[(t-start)//width].append(kind)
    if not final: raise ValueError("incomplete")
    n=(stop-start)//width
    counts=[0]*24;counts[0]=n-len(groups);counts[16]=n
    for events_in_bin in groups.values():
        channels=Counter(events_in_bin)
        mask=sum(1<<ch for ch in channels)
        counts[mask]+=1
        counts[17]+=int(any(n>1 for n in channels.values()))
        for ch,n in channels.items():counts[18+ch]+=n
        counts[22]+=sum(n-1 for n in channels.values())
        counts[23]+=int((mask&3)==3 or ((mask>>2)&3)==3)
    limit=(1<<bits)-1
    if any(c>limit for c in counts): flags |= 1
    return [min(c,limit) for c in counts],flags
