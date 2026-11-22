"""Compare both arms on the same admitted subset, separately for every setting."""
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import cmath,hashlib,json,math,sys
from instrument import cell,rule,settings
ROOT=Path(__file__).resolve().parent

def read(rho,sector,m,n,k,method):
    nodes,weights=rule(k,method);rows=settings();phases={};ratios={}
    for tag,(src,_) in rows.items():
        z=0j;ref=0j
        for mid in (-1/16,1/16):
            for x,w in zip(nodes,weights):
                args=(sector,m,rho,method)
                shifted,weight=cell(n,mid+x/32,src,'strict',*args)
                zero,weight0=cell(n,mid+x/32,(0,)*5,'strict',*args,gate_source=src)
                assert weight==weight0
                z+=w*shifted;ref+=w*zero
        ratio=z/ref;phases[tag]=cmath.phase(ratio);ratios[tag]=[ratio.real,ratio.imag]
    assert max(map(abs,phases.values()))<1
    return math.fsum(float(w)*phases[tag] for tag,(_,w) in rows.items()),ratios

def cal():
    levels={}
    for n,k in ((4,8),(5,10)):
        b=read(.125,'empty',0,n,k,'gauss')[0];p=read(.125,'positive',.25,n,k,'gauss')[0];levels[f'{n}x{k}']=[b,p]
    return {'levels':levels,'offset':format(b,'.12f'),'gain':format(.25/(p-b),'.12f') if p>b else None,
            'plan_sha256':hashlib.sha256((ROOT/'paarplan.txt').read_bytes()).hexdigest()}

def test(case):
    rho,sector,m=case;f=(ROOT/'paareichung.json').read_bytes();assert hashlib.sha256(f).hexdigest()==(ROOT/'paareichung.sha256').read_text().split()[0];c=json.loads(f)
    raw,ratios=read(rho,sector,m,5,10,'gauss');control=read(rho,sector,m,5,9,'cc')[0]
    return f'{rho}|{sector}|{m}',{'raw':raw,'cc_control':control,'ratios':ratios,'calibrated':float(c['gain'])*(raw-float(c['offset'])) if c['gain'] is not None else None}

def run():
    cases=[(r,s,m) for r in (.125,.25) for s,m in [('empty',0),('positive',.25),('positive',1)]]
    with ProcessPoolExecutor(max_workers=3) as pool:return dict(pool.map(test,cases))
if __name__=='__main__':print(json.dumps(cal() if '--eichen' in sys.argv else run(),indent=2,sort_keys=True))
