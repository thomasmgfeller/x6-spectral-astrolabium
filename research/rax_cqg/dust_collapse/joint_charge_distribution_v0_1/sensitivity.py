"""Keep the preparation fixed while changing only certified charge-blind chain weights."""
import json
from fractions import Fraction as F
import numpy as np
from model import BASE,gram,laws,combined_laws
from integrate import MASSES,RHOS
from evaluate import readout,mix_range
def run():
    z=json.loads((BASE/'chain.json').read_text())
    keys,base=combined_laws()
    _,one=laws()
    scal=np.load(BASE/'scalars.npz')
    idx=np.searchsorted(scal['keys'],keys)
    G=gram(list(zip(scal['precision'][idx],scal['factor'][idx])))
    raw=np.load(BASE/'combined_raw.npz')
    data=raw['amp'][:,-1]
    assert list(raw['keys'])==keys
    out={}
    for law in ['alternative_same_N13','alternative_same_new_N14']:
        delta=np.array([float((F(z[law]['law'].get(str(k),0))-F(z['law'].get(str(k),0)))/2) for k in keys])
        alt=base[0]+delta
        assert min(alt)>0 and abs(alt.sum()-1)<1e-12
        rows={}
        for im,m in enumerate(MASSES):
            for ir,r in enumerate(RHOS):
                arr=data[:,im,ir].mean(axis=0)
                res=readout(arr,G,alt)
                rows[f'{m:g}/{r:g}']={'bins':res['bin_probabilities'],'sign_positive':res['positive_sign_record'],
                    'sign_range_four_scrambles':[float(f([readout(a,G,alt)['positive_sign_record'] for a in data[:,im,ir]])) for f in (min,max)],
                    'interpolated_positive_sign':mix_range(arr,G,base[0],alt)}
        out[law]={'parent_weight_total_variation':float(abs(delta).sum()),'one_edge_AB':'1:1','rows':rows}
    return out
if __name__=='__main__': print(json.dumps(run(),indent=2))
