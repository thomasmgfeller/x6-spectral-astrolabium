"""Finite N15 variables and early prefix bounds from the finite N15 reference."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha1, sha256
from pathlib import Path
import argparse
import json
import sys

ROOT=Path(__file__).resolve().parent
SRC=ROOT/'quellen'
sys.path.insert(0,str(SRC))
from intervalle import I, S
from ordnung import ORDER,INNER,PAST,pairs_from_intervals
from modell import clocks,dwell,INNER_MEANS

E=F(1,4)
K=4-E
DELTA=I.of(F(3,722)).sqrt().sqrt()
D=K*DELTA
STEP=1/(72*D*K**2)
H=F(1,16384)
X0=F(1,8)
DX=F(1,2048)
EDGES=pairs_from_intervals()


def require(test,message):
    if not test:
        raise ValueError(message)


def provenance():
    m=json.loads((SRC/'herkunft.json').read_text())
    for name,r in m['files'].items():
        data=(SRC/name).read_bytes()
        gid=sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(gid==r['git_blob'] and sha256(data).hexdigest()==r['sha256'],name)
    digest=sha256((SRC/'uhr5_ausgang.json').read_bytes()).hexdigest()
    require(digest=='c545145520796dfd4e6244f05a09dc6331752cee7604f91bb00c7d7299b25127','Vorstudie')
    for p in ROOT.glob('*plan.txt'):
        require(sha256(p.read_bytes()).hexdigest()==p.with_suffix('.sha256').read_text().split()[0],p.name)
    p3=json.loads((SRC/'p3.json').read_text())
    counts=Counter(v['execution'] for v in p3 if v['checkpoint_id']=='P3')
    require(len(p3)==60 and counts=={'NOT_RUN':60},'P3')
    return m['commit'],dict(counts)


def run():
    commit,p3=provenance()
    # At the audited e,u6,u11 the entire u4 window and both finite paired u5 arms are covered.
    s=F(3,2500)
    require(STEP.hi<I.of(s).lo and D.hi<S,'Dauer und Schritt')
    fmin=F(7,64)
    fmax=F(13,64)
    for u4 in (F(7,64),F(9,64)):
        for u5 in (F(1,4)-s-H,F(1,4)+s+H):
            u=INNER_MEANS.copy();u[:2]=[u4,u5]
            fs=dwell(u);y=clocks(E,u)
            require(all(fmin<=fs[j]<=fmax for j in (4,5,6)),'Dichteband')
            require(all(abs(y[j]-y[i])<5 for i,j in EDGES if j in (4,5,6)),'Paare vor 11')
    cmax=F(1,2)+F(34*25,38)
    zmax=fmax*cmax/100
    require(zmax<F(1,20),'sinc positiv')
    sinc_min=1-zmax**2/6
    # f4,f6 change by s; f5 is identical. Common collar factors cancel.
    ratio=(1+s/fmin)**2/sinc_min**3
    vmin=2*ratio/(1+ratio**2)
    kmin,kmax=(1-4*H)/304,(1+4*H)/304
    lo,hi=kmin*(DX-H),kmax*(DX+H)
    margin=vmin*(lo-lo**3/6)/2
    maxmargin=hi/2
    require(margin>F(7,10**7) and maxmargin<F(91,10**8),'Separation vom Zufallsbit')
    # Independent full-action column: the slope arises solely from (5,11).
    for r in (F(-1,2048),F(7,8192)):
        for offset in (-H,0,H):
            values=[]
            for arm in (-1,1):
                u=INNER_MEANS.copy();u[1]+=arm*r+offset
                y=clocks(E,u)
                values.append(-F(1,2)-sum(F(b,38)*(y[11]-y[i])**2 for (i,j),b in EDGES.items() if j==11))
            require(values[1]-values[0]==-F(36,38)*K**2*r*(F(1,4)-offset),'Lokale Steigung')
    # Both new u12 continuations also have common x support for both finite tags.
    for u12 in (F(5,8)-F(1,1024),F(5,8)+F(1,1024)):
        f=(u12-F(3,8))/2
        require(F(99,100)*f < X0-DX-H and X0+DX+H < F(101,100)*f,'Zulässige Fortsetzung')
    return {'commit':commit,'visibility_lower':I.of(vmin).rounded(11)[0],
            'plus_margin_for_strength_one':[I.of(margin).rounded(13)[0],I.of(maxmargin).rounded(13)[1]],
            'p_plus_low':[I.of(F(1,2)+margin).rounded(13)[0],I.of(F(1,2)+maxmargin).rounded(13)[1]],
            'p_plus_high':[I.of(F(1,2)-maxmargin).rounded(13)[0],I.of(F(1,2)-margin).rounded(13)[1]],
            'P3':p3}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true')
    args=p.parse_args();out=json.dumps(run(),indent=2)+'\n'
    if args.json: print(out,end='')
    else:
        require(out==(ROOT/'praefix.json').read_text(),'Archiv');
        print('PASS · Präfix, gemeinsame Banddaten, Sichtbarkeit, Bitabstand und P3')
