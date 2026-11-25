"""Independent rational reconstruction of the future-phase polynomial."""
from fractions import Fraction as Q
from itertools import combinations
import json
from pathlib import Path
import hashlib
from zertifikat import ORIGIN, ETA, CROSS, ORDER, PAST, INNER, FUTURE, profile
ROOT=Path(__file__).resolve().parent

def full_action(y_in,z):
    y=dict(y_in)
    w={j:Q((j%3)+3,31) for j in ORDER}
    for j in FUTURE:
        y[j]=Q(j-5)+(ETA*z[j-8] if j>7 else 0)
        w[j]=Q(1,8)+ETA*z[j-4]
    s=-sum(w.values())/2
    for n,j in enumerate(ORDER):
        for lag,b in enumerate((1,-9,16,-8),1):
            if n<lag: break
            i=ORDER[n-lag]
            s-=Q(b,38)*w[j]*(y[i]-y[j])**2
    return s

def extensions():
    """Direct interval counting, including edges with a translated old density at their source."""
    from itertools import combinations
    edges0=set(combinations(ORDER,2))
    delta=Q(1,2**14)
    samples=0
    for arm in (-1,1):
        u={j:Q(k,8) for k,j in enumerate(INNER,1)}
        u[5]+=arm*Q(1,1000)
        y,_,direction=profile(u)
        y.update({15:Q(21,4),16:Q(11,2)})
        faces=[Q(0)]+[(u[i]+u[j])/2 for i,j in zip(INNER,INNER[1:])]+[Q(1)]
        base={j:faces[k+1]-faces[k] for k,j in enumerate(INNER)}
        base[11]=Q(255,2048)
        base.update({j:Q(1,8) for j in PAST+FUTURE})
        base.update({15:Q(5,16),16:Q(3,16)})
        for ancestry in [((10,15),), ((12,15),), ((12,15),(15,16),(8,16))]:
            edges=edges0|set(ancestry)
            nodes=set(ORDER)|{j for i,j in ancestry}
            while True:
                extended=edges|{(i,k) for i,j in edges for jj,k in edges if jj==j}
                if extended==edges: break
                edges=extended
            assert {(i,j) for i,j in edges if i in ORDER and j in ORDER}==edges0
            layer={}
            for i,j in edges:
                m=sum((i,k) in edges and (k,j) in edges for k in nodes)
                if m<4: layer[i,j]=(1,-9,16,-8)[m]
            for pulse in (Q(0),Q(-1,8),Q(1,8),Q(5,17)):
                totals=[]
                for sign in (-1,1):
                    weights={j:base[j]+sign*delta*direction.get(j,0) for j in nodes}
                    total=-sum(weights.values())/2
                    for (i,j),b in layer.items():
                        shift=pulse if i==6 and j in (12,13,14) else 0
                        total-=Q(b,38)*weights[j]*(y[j]-y[i]-shift)**2
                    totals.append(total)
                assert totals[0]==totals[1]
                samples+=1
    return samples

def main():
    manifest=json.loads((ROOT/'HERKUNFT.json').read_text())
    for name,record in manifest['files'].items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==record['sha256'],name
    reference={j:Q(j-5) for j in PAST}
    reference[3]=Q(-7,4)
    reference.update({j:ORIGIN[j] for j in INNER})
    count=0
    for trial in range(3):
        clocks=reference.copy()
        for n,j in enumerate(INNER):
            clocks[j]+=Q(((n+1)*(trial+1))%7-3,128)
        zero=[Q(0)]*7
        a=[Q(0)]*7; cross=[Q(0)]*3
        for i,j,b in CROSS:
            t=clocks[i]-reference[i]
            a[j-4]+=Q(b,38)*ETA*t*(2*(ORIGIN[j]-ORIGIN[i])-t)
            if j>7:
                a[j-8]+=Q(b,19)*ETA*t/8
                cross[j-8]+=Q(b,19)*ETA**2*t
        def difference(z):
            return ((full_action(clocks,z)-full_action(clocks,zero))
                    -(full_action(reference,z)-full_action(reference,zero)))
        samples=[zero]
        for axis in range(7):
            for sign in (-1,1):
                row=zero.copy();row[axis]=sign
                samples.append(row)
        for i,j in combinations(range(7),2):
            row=zero.copy();row[i]=row[j]=1
            samples.append(row)
        assert len(samples)==36
        for z in samples:
            assert difference(z)==sum(v*t for v,t in zip(a,z))+sum(cross[k]*z[k]*z[k+4] for k in range(3))
            count+=1
    p3=json.loads((ROOT/'basis/p3_status.json').read_text())
    assert p3['records']==60 and p3['no_physical_data_generated']
    return {'exact_all_monomial_checks':count,'exact_extension_pairs':extensions(),'pinned_inputs':len(manifest['files']),
            'p3_records':p3['records'],'future_axes':['Y8','Y9','Y10','w7','w8','w9','w10']}
if __name__=='__main__':
    print(json.dumps(main(),indent=2))
