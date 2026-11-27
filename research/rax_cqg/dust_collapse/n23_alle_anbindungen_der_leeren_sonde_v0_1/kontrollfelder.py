"""Contraction proof for the four illustrative solutions outside the target window.

Run via gegenprobe.py inside the verified PR 414 archive, using its rational arithmetic.
"""
import json
import sys
from fractions import Fraction as Q
from pathlib import Path
from intervall import I, inverse_seed
from modell import inputs, make, FREE, POS, ZERO, DEVICE, WINDOW, evaluate
from zeuge import put, product
from gegenprobe import direct

def certify(control,pair):
    side=control['side']
    rel,edges=make(pair,control['past'],control['future'])
    y,w=([I(*v) for v in pair[side][kind]]+[I()] for kind in ('clock_box','weight_box'))
    center=[I(v) for v in control['clock']+control['weight']]
    radius=[Q(1,10**9)]*len(FREE)+[Q(1,10**11 if side=='heavy' else 10**12)]*len(POS)
    full=[v+I(-r,r) for v,r in zip(center,radius)]
    residual,jac,_=evaluate(*put(y,w,center),edges,I())
    matrix=inverse_seed(jac)
    _,jac_box,_=evaluate(*put(y,w,full),edges,I())
    norms=[];images=[]
    for i,row in enumerate(matrix):
        n=sum((int(i==j)-product(row,col)).mag()*r for j,(col,r) in enumerate(zip(zip(*jac_box),radius)))/radius[i]
        norms.append(n);images.append(n+product(row,residual).mag()/radius[i])
    assert max(norms)<1 and max(images)<1
    Y,W=put(y,w,[v+I(-r*e,r*e) for v,r,e in zip(center,radius,images)])
    assert all(v.l<=0<=v.h for v in direct(Y,W,edges)[0])
    assert all(Y[i].h<Y[j].l for i,j in rel)
    assert all(0<W[j].l<=W[j].h<1 for j in range(23) if j not in ZERO)
    assert all(W[j].l==W[j].h==0 for j in ZERO)
    assert all((Y[j]-Y[i]).mag()<8 for i,j in DEVICE+((15,18),))
    x=(Y[22]-Y[3])/(Y[7]-Y[3])
    assert x.h<WINDOW[0]
    def upper(q):return str(Q(-(-q*10**9//1),10**9))
    return dict(future=control['future'],past=control['past'],side=side,x22=x.data(),contraction_upper=upper(max(norms)),image_upper=upper(max(images)))

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Ohne -O ausführen')
    data=json.loads(Path(sys.argv[1]).read_text())
    pair,_=inputs()
    print(json.dumps({key:certify(control,pair) for key,control in data.items()},sort_keys=True,indent=2))
