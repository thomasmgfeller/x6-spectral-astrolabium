"""Single calibration at one inlet, prior to the unit and four-dose transfers."""
import hashlib,json
from modell import ROOT
from quadratur import amplitudes,readout

def run():
    levels={}
    for n,k in ((3,4),(4,8),(5,10)):
        row={}
        for name,m,medium in [('empty',0,'empty'),('quarter',.25,'positive')]:
            z=amplitudes(m,.125,medium,n,k,'gauss');row[name]=readout({a:t[0] for a,t in z.items()})
        levels[f'{n}x{k}']=row
    row=levels['5x10'];offset=row['empty']['raw'];gap=row['quarter']['raw']-offset
    return {'plan_sha256':hashlib.sha256((ROOT/'ergaenzung.txt').read_bytes()).hexdigest(),'levels':levels,'offset':format(offset,'.12f'),'gain':format(.25/gap,'.12f') if gap>0 else None}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
