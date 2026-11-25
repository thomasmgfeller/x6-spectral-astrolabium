"""Rebuild hidden fixtures, verify blind predictions, and score after the frozen output."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from fractions import Fraction as F
import json
import shutil
import subprocess
import sys
from kontrollen import cases,frames,FACTORS,STRATA,corner,relation,crosscheck
from transfer import ltb,cst

ROOT=Path(__file__).resolve().parent
def packed(x):
    return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()

def check_manifest(name):
    for line in (ROOT/name).read_text().splitlines():
        target_hash,p=line.split('  ',1)
        assert sha256((ROOT/p).read_bytes()).hexdigest()==target_hash,p

def assess(truth,pred):
    assert {r['id'] for r in truth}==set(pred)
    counts={}; strata={}; by_curve={}
    grades=[]
    for factor in FACTORS:
        key=str(factor)
        counts[key]=dict(Counter(p[key] for p in pred.values()))
        strata[key]=[dict(Counter(pred[r['id']][key] for r in truth if r['stratum']==s)) for s in range(4)]
        by_curve[key]={str(k):dict(Counter(pred[r['id']][key] for r in truth if r['curvature_sign']==k))
                       for k in (-1,0,1)}
    for r in truth:
        p=pred[r['id']]
        nominal=crosscheck(r,*corner(0,True))
        assert nominal==relation(r,*corner(0,False)) and p['0']==nominal
        seen_open=False
        for factor in FACTORS:
            v=p[str(factor)]
            assert not (seen_open and v!='OFFEN')
            seen_open |= v=='OFFEN'
            if v!='OFFEN':assert v==nominal
        if r['stratum'] in (0,3):
            expected='JA' if r['radius_milli']<9200 else 'NEIN'
            grades.append(p['1']==expected)
    assert len(grades)==60 and all(grades)
    for s,(lo,hi) in enumerate(STRATA):
        group=[r for r in truth if r['stratum']==s]
        assert len(group)==30 and all(lo<=r['radius_milli']<=hi for r in group)
    return {'anzahl':len(truth),'eckpruefungen':len(truth)*2*len(FACTORS),
            'aeussere_strata_bestanden':sum(grades),'zaehlungen':counts,
            'je_stratum':strata,'je_kruemmung':by_curve}

def execute():
    for f in ('Plan_und_Leser.sha256','Generator.sha256','Schluessel.sha256','Blindurteile.sha256','Quellen.sha256'):
        check_manifest(f)
    truth=cases((ROOT/'Seed.txt').read_text().strip())
    assert packed(truth)==(ROOT/'Schluessel.json').read_bytes()
    exposures=frames(truth)
    assert packed(exposures)==(ROOT/'Aufnahmen.json').read_bytes()
    with TemporaryDirectory() as tmp:
        run=Path(tmp)
        shutil.copy(ROOT/'leser.py',run)
        (run/'Aufnahmen.json').write_bytes(packed(exposures))
        subprocess.run([sys.executable,'-I','-B','leser.py','Aufnahmen.json','Blindurteile.json'],
                       cwd=run,check=True)
        forecast=(run/'Blindurteile.json').read_bytes()
    assert forecast==(ROOT/'Blindurteile.json').read_bytes()
    return {'blind':assess(truth,json.loads(forecast)),'LTB':ltb(),'CST':cst()}

if __name__=='__main__':
    if not __debug__:raise SystemExit('Python ohne -O starten.')
    result=packed(execute())
    if sys.argv[1:]==['--erzeugen']:(ROOT/'Ergebnisse.json').write_bytes(result)
    else:assert result==(ROOT/'Ergebnisse.json').read_bytes()
    print('PASS: Blindurteile, beide Rechenwege, 120 Geometrien, LTB-Transfer und N15-Markerprüfung.')
