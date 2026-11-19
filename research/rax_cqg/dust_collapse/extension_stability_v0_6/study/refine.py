"""Additional integration on (64,10) for threshold-relevant and grid-sensitive types."""
from common import HERE, clocks, prior, archived, coherent
import json
import numpy as np
from tails import packet
from tempfile import TemporaryDirectory
from quadrature import build
from unittest.mock import patch

def run():
    recorded=json.loads((HERE/'direct.json').read_text())
    source=archived()
    selected={n for n,v in recorded.items() if max(abs(complex(*a)-complex(*b)) for a,b in
              zip(v['rows']['coarse'],v['rows']['fine']))>2e-12}
    selected.update(f'N14_{m}' for m in (734,760,8191))
    out={};path=HERE/'refined.json'
    with TemporaryDirectory() as tmp,patch.object(clocks.reference,'layout',prior.growth.layout):
        lib=build(tmp)
        for name in sorted(selected,key=lambda x:int(x.split('_')[1])):
            prev=(np.array([complex(*pair) for pair in recorded[name]['rows']['fine']])
                  if name in recorded else coherent(source[name][-1]))
            z=packet(prior.key(name),64,10,lib)
            change=float(np.max(abs(z-prev)))
            out[name]={'grid':[64,10],'amplitudes':[[v.real,v.imag] for v in z],
                       'change_from_48_8':change}
            path.write_text(json.dumps(out,indent=2)+'\n')
            print(name,change,flush=True)
if __name__=='__main__':run()
