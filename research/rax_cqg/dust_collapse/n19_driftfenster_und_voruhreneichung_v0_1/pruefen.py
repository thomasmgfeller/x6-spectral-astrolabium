"""Offline replay of the drift-family certificate, quantizer inversion and fault controls."""
import argparse
from hashlib import sha256
import json
import subprocess
import sys
from quellenpaket import ROOT,model
from driftfamilie import certify
from freigabefenster import analyze
from gegenproben import geometry_contract,scan,stale
from offsetgrenze import stable_limits


def raw(doc):
    return (json.dumps(doc,indent=2,sort_keys=True,ensure_ascii=False)+'\n').encode()


def results(history=False):
    with model() as (pkg,par,prev,early):
        from modell import setup,setting,read
        from empfangsbit import STEP
        from voruhren import protected_read
        if history:
            subprocess.run([sys.executable,'-B','pruefen.py','--mit-vorgaenger'],cwd=pkg,check=True)
        ref=read(pkg/'daten','A_Referenz')['reference']
        geo=read(par,'Geometrische_Nulluhr')
        y,w=setup(prev,early)
        domain=geometry_contract(y,w,geo)
        cert=certify(y,w)
        windows=analyze(y,w,ref,geo,cert)
        offsets=stable_limits(setting(y,w,6*STEP)[0],ref,geo,cert)
        samples=scan(y,w,ref,geo,cert,windows)
        stale_test,examples=stale(pkg,y,w,ref,geo,cert)
        for name,expected in (('Stabil','CONDITIONAL_MODEL_CLASSIFICATION'),('Sprung','DISJOINT_REFERENCES')):
            group=[read(pkg/'daten',name+'_'+key) for key in ('Voruhren','receiver','memory','received')]
            assert protected_read(par,ref,*group)['status']==expected
        return {'Dynamik':cert,'Freigabefenster':windows,'Offsetgrenzen':offsets,
                'Kontrollen':{'domain':domain,'direct':samples,'held_clocks':stale_test,
                              'physical_observations':0,'physical_P3':'60 NOT_RUN'},
                **{'beispiel/'+key:value for key,value in examples.items()}}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mit-vorgaenger',action='store_true')
    args=p.parse_args()
    if not __debug__:
        raise SystemExit('Python ohne -O starten.')
    for filename in ('SHA256SUMS','Pruefplan.sha256','Offsetgrenze.sha256'):
        for line in (ROOT/filename).read_text().splitlines():
            value,name=line.split('  ',1)
            assert sha256((ROOT/name).read_bytes()).hexdigest()==value,name
    for name,result in results(args.mit_vorgaenger).items():
        assert (ROOT/(name+'.json')).read_bytes()==raw(result),name
    print('PASS — Driftfamilie, Freigabefenster, Offsetgrenzen und festgehaltene Voruhren.')
    print('Physische Messungen: 0. P3: 60 NOT_RUN.')


if __name__=='__main__':
    main()
