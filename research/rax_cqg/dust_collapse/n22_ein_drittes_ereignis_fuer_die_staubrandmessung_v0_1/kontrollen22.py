"""Independent combinatorial and rational variation checks."""
from collections import Counter
from fractions import Fraction as F
from ordnung22 import structure
from seriendaten import MATERIAL


def reconstruct(d,rows):
    old=set(d['order']);past=[sum(1<<i for i,jj in old if jj==j) for j in range(19)]
    ideals=[m for m in range(1,1<<19) if all(not(past[j]&~m) for j in range(19) if m&(1<<j))]
    single=[]
    for p in ideals:
        for middle in ideals:
            if p&~middle:continue
            f=((1<<19)-1)^middle
            if f and all(p&~past[j]==0 for j in range(19) if f&(1<<j)):single.append((p,f))
    alternate={(p,f,q,g) for p,f in single for q,g in single if p&q&MATERIAL and f&g&MATERIAL
               and not(p&g or q&f)}
    assert alternate==set(rows)
    return len(alternate)


def variations(d,samples):
    old=set(d['order']);k=F(1,79);mu=-k;source=F(1,43);step=F(1,2048)
    probes=((15,16),(16,18),(17,18),(18,7))
    velocities=(F(-2,11),F(3,13),F(5,17));checks=0
    for key,row in samples:
        rel,c=structure(old,row,key[0]);n=22
        positive=[j for j in (4,5,6,11,12,13,14,16,18,19,21) if j!=21 or key[1]=='+']
        free=sorted(positive+[15,17,20]+([21] if key[1]=='0' else []))
        y=[F(5*j-31,37) for j in range(n)]
        w=[F(j+3,31) if j in positive or j not in free else F(0) for j in range(n)]
        tracks=[];mom=[];dw=[F(0) for j in range(n)];dg=dw.copy();dw[16]=-source
        for track,v in zip(d['routes'],velocities):
            for j,inertia,edge in track:
                gap=y[edge[1]]-y[edge[0]] if edge else 0
                tracks.append((j,inertia,edge,gap+v/w[inertia]))
                dw[inertia]+=k*(v/w[inertia])**2
                if edge:
                    a,b=edge;mom.append((a,b));dw[j]+=mu*gap**2
                    x=mu*w[j]*gap-k*v;dg[a]+=x;dg[b]-=x
        assert tuple(mom)==probes
        def action(Y,W):
            s=19*sum(W)-source*W[16]+sum(v*W[j]*(Y[j]-Y[i])**2 for (i,j),v in c.items())
            for j,inertia,edge,increment in tracks:
                gap=Y[edge[1]]-Y[edge[0]] if edge else 0
                s+=k*W[inertia]*(increment-gap)**2
                if edge:s+=mu*W[j]*gap**2
            return s
        for i in free:
            l=y.copy();h=y.copy();l[i]-=step;h[i]+=step
            expr=sum(v*w[b]*(y[b]-y[i]) for (a,b),v in c.items() if a==i)
            expr-=w[i]*sum(v*(y[i]-y[a]) for (a,b),v in c.items() if b==i)
            assert -(action(h,w)-action(l,w))/(4*step)==expr+dg[i];checks+=1
        for j in positive:
            l=w.copy();h=w.copy();l[j]-=step;h[j]+=step
            expr=19+sum(v*(y[j]-y[i])**2 for (i,b),v in c.items() if b==j)
            assert (action(y,h)-action(y,l))/(2*step)==expr+dw[j];checks+=1
        # Direct parent/new layer counting by old endpoints and insertion masks.
        for i,j in old:
            direct=sum((i,t) in old and (t,j) in old for t in range(19))
            p,f,q,g=row
            def between(p,f):return int(bool(p&1<<i and f&1<<j))
            extra=between(p,f)+between(q,g)+between(*(row[:2] if key[0]=='A' else row[2:]))
            assert c.get((i,j),0)==((1,-9,16,-8,0)[min(4,direct+extra)])
    return {'orders_and_sectors':len(samples),'exact_variations':checks}


def example(d,rows):
    mask=(1<<17)|1
    n=Counter()
    for row in rows:
        if row[0]!=mask:continue
        n['anchored']+=1
        from seriendaten import prefilter
        if not prefilter(row,'A'):n['after_A_prefilters']+=1
    r=next(row for row in rows if row[0]==mask)
    _,c=structure(set(d['order']),r,'A')
    assert {i:v for (i,j),v in c.items() if j==19}=={0:16,17:-9,21:1}
    lo=F(d['window'][0],10**9)
    return {'orders':dict(n),'D19_strict_lower_bound':str(19+7*(lo+5)**2)}


def binary_control(d,samples,proposals,certificates,tmp):
    from pathlib import Path
    import subprocess
    here=Path(__file__).resolve().parent;binary=tmp/'gegencheck'
    subprocess.run(['g++','-std=c++17','-O2','-DN22_JOINT','-DN22_BOUNDED_LOAD','-Wall','-Wextra',
                    '-Werror','-fsanitize=undefined','-fno-sanitize-recover=undefined',
                    str(here/'gegencheck.cpp'),'-o',binary],check=True)
    lines=[str(len(d['order'])),*['%d %d'%e for e in d['order']]];expected=[]
    for case,row in samples:
        lines.append(' '.join(map(str,['C',*case,*row])))
        _,c=structure(set(d['order']),row,case[0])
        expected.append([str(c.get((i,j),0)) for i in range(22) for j in range(22)])
    for name,p in proposals.items():
        lines.append(' '.join(map(str,['W',*p['case'],*p['row']])))
        collar=certificates[name]['collar']
        for j in range(22):
            if str(j) in collar:
                y,w=collar[str(j)]
            else:
                y0=F(p['y'][j]);w0=F(p['w'][j]);yr=F(1,10**7);wr=F(1,10**8) if w0 else 0
                y=[y0-yr,y0+yr];w=[w0-wr,w0+wr]
            yl,yh,wl,wh=[F(v)*10**9 for v in (*y,*w)]
            lines.append(' '.join(map(str,[yl.__floor__(),yh.__ceil__(),wl.__floor__(),wh.__ceil__()])))
        expected.append(['PASS'])
    inp='\n'.join(lines)+'\n'
    out=subprocess.run([binary],input=inp,capture_output=True,text=True,check=True)
    assert [line.split() for line in out.stdout.splitlines()]==expected
    return {'coefficient_matrices':len(samples),'witness_sweeps':2*len(proposals)}
