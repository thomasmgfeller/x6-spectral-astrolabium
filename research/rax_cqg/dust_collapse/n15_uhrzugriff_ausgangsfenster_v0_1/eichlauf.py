"""Freeze the strict-window calibration before applying the test at unit mass."""
from pathlib import Path
import hashlib,json
from instrument import spectrum
ROOT=Path(__file__).resolve().parent

def run():
    levels={}
    for n,k in [(3,4),(4,8),(5,10)]:
        b=spectrum('empty',0,1/8,'strict',n,k);p=spectrum('positive',1/4,1/8,'strict',n,k)
        levels[f'{n}x{k}']={k:{'raw':v['raw'],'max_relative_angle':v['max_relative_angle'],'min_modulus':v['min_modulus']} for k,v in [('empty',b),('quarter',p)]}
    fine=levels['5x10'];b=fine['empty']['raw'];diff=fine['quarter']['raw']-b
    valid=diff>0 and all(x['max_relative_angle']<1 and x['min_modulus']>0 for x in fine.values())
    return {'levels':levels,'plan_sha256':hashlib.sha256((ROOT/'pruefplan.txt').read_bytes()).hexdigest(),
            'positive_local_calibration':valid,'offset':format(b,'.12f'),'gain':format(.25/diff,'.12f') if valid else None}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
