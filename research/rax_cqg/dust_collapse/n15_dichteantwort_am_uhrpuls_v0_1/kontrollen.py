"""Independent conditional-density integration and separate preparation normalization."""
import json
from itertools import product
import numpy as np
from numpy.polynomial.legendre import leggauss
from randquelle import ROOT,INNER
from modell import dwell

DELTA=(3/722)**.25

def direct(n):
    x,w=leggauss(n);w=w/2
    e0,ew=leggauss(20)
    small,ws=leggauss(2);ws=ws/2
    # Q integrates the five unused uniforms. The product is degree <=2 in each.
    q=np.zeros((n,n));box_weights=w[:,None]*w[None,:]
    u6=3/8+x[:,None]/64;u12=5/8+x[None,:]/64
    for index in product((0,1),repeat=5):
        it=iter(index);weight=1.;u=[]
        for k,j in enumerate(INNER):
            if j==6:u.append(u6)
            elif j==12:u.append(u12)
            else:
                i=next(it)
                u.append((k+1)/8+small[i]/64);weight*=ws[i]
        f=dwell(u);cur=weight*box_weights
        for j in INNER:
            if j!=11:cur=cur*f[j]
        q+=cur
    sums={sg:[0.,0.] for sg in (1,-1)}
    base=0.
    for centre in (-1/16,1/16):
        for node,weight in zip(e0,ew):
            D=4*DELTA-(centre+node/32)
            dw=weight*D**14/4
            f=(u12-u6)/2
            base+=dw*np.sum(q*f)
            for sign in (1,-1):
                fp=f-sign*DELTA/(16*D**1.5)
                fraction=(.99*7/64/fp-.99)/.02 if sign==1 else (1.01-1.01*9/64/fp)/.02
                fraction=np.clip(fraction,0,1)
                sums[sign][0]+=dw*np.sum(q*fp*fraction)
                sums[sign][1]+=dw*np.sum(q*fp)
    return {tag:{'verbotener_anteil':sums[s][0]/sums[s][1],'armgewicht':sums[s][1]/base}
            for s,tag in ((1,'plus'),(-1,'minus'))}

def run(data):
    grids={str(n):direct(n) for n in (96,192)}
    arm=grids['192'];asym={}
    for k,row in data['1|gauss5x10'].items():
        alpha=k.split('|')[-1]
        v=[row['intensitaeten'][tag]/(arm[tag]['armgewicht'] if alpha=='1' else 1)**2 for tag in ('minus','plus')]
        asym[k]=(v[0]-v[1])/(v[0]+v[1])
    return {'direkt':grids,'asymmetrie_bei_separater_normierung_M1':asym}

if __name__=='__main__':
    print(json.dumps(run(json.loads((ROOT/'auslese.json').read_bytes())),indent=2,sort_keys=True))
