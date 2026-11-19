"""Only two anchor cross-rows and the diagonal are needed for a full-support bound."""
from unittest.mock import patch
from model import ROOT, CACHE, layout, geometry, write
import json
import mpmath as mp

def overlap(left,right):
    h=left[0].conjugate()+right[0]
    root=geometry.continued_sqrt(h)
    z=mp.conj(left[1])*right[1]*(2*mp.pi)**mp.mpf('1.5')/root
    c=z*mp.erf(1/mp.sqrt(2*(1+(h**-1)[0,0])))
    return [complex((z-c)/2),complex(c),complex((z-c)/2)]

def run():
    data=json.loads((ROOT/'catalog.json').read_text())
    keys=sorted({int(k) for row in data['roots'].values() for k in row['ends']})
    mp.mp.dps=70;out={}
    with patch.object(geometry,'order',layout):
        anchors=[geometry.kernel((3,i))[1] for i in (7,1)]
        for m in keys:
            row,state=geometry.kernel((7,m))
            assert row['status']=='ADMISSIBLE',m
            overlaps=[overlap(a,state) for a in anchors+[state]]
            out[str(m)]=[[[z.real,z.imag] for z in bins] for bins in overlaps]
    write('anchor_rows.json',out)
if __name__=='__main__':run()
