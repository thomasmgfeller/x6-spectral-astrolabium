"""Reproduce the input study, all field screens and the fixed-source root enclosure."""
from collections import Counter
from fractions import Fraction as F
from hashlib import sha256
import json
import subprocess
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from kegel import ROOT,cones,projected
import leer
import positiv
import paar


def compare(name, v, compact=False):
    args={'separators':(',',':')} if compact else {'indent':2}
    assert (json.dumps(v,sort_keys=True,**args)+'\n').encode()==(ROOT/name).read_bytes(),name


def verify():
    for manifest in ('Pruefplan.sha256','Leerplan.sha256','SHA256SUMS'):
        for line in (ROOT/manifest).read_text().splitlines():
            digest,name=line.split('  ',1)
            assert sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    arc=ROOT/'Vorstudie.zip'
    assert sha256(arc.read_bytes()).hexdigest()=='3b8f7cfd75d457a0e8ccf6f1912279b0caefd25063a3697b07d192013a05f6c0'
    with ZipFile(arc) as z,TemporaryDirectory() as tmp:
        for n in ('basis/zweig.json','basis/intervall.py','basis/vorversuch.json','LICENSE','NOTICE'):
            assert (ROOT/n).read_bytes()==z.read(n)
        reference=json.loads(z.read('Empfang.json'))
        z.extractall(tmp)
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=tmp,check=True,stdout=subprocess.DEVNULL)
    # Recompute the twenty N18 cones with the new residual evaluator.
    from kegel import OLD,NODES,Z,R,ideals,coefficients
    e,s,t=leer.coordinates(False)
    legacy={tuple(v['past']):v['branches'][0] for v in reference['cases']}
    for p in ideals(NODES,OLD):
        if Z not in p:continue
        prev=legacy.pop(tuple(sorted(p)))
        y=leer.prior(e.lo,e.hi,s.lo,s.hi,'pairwise')
        if any(y[j].lo>=t.hi for j in p):
            assert 'excluded_by_order' in prev
        else:
            _,terms=coefficients(OLD|{(j,R) for j in p},NODES|{R},'pairwise')
            v=positiv.density(terms[R],y,t,'pairwise')
            assert v.hi<0 or v.lo>0
            assert v.intersection(positiv.Box.hull(*map(F,prev['D_r']))) is not None
    assert not legacy
    cases=cones()
    assert len(cases)==len(set(cases))==3816 and set(cases)==projected()
    p=positiv.scan();compare('Positiv.json',p,True)
    assert not any(v['status']=='OPEN' or any(v['singular']) for v in p)
    assert Counter(r['status'] for r in p)=={'residual_excluded':113,'no_receiver_branch':3703}
    print('PASS — N17 and N18 baseline, 3816 positive-ancestor cones, both counts and clock screens.')
    v=leer.scan_fixed();compare('Leerer_Vorlaeufer.json',v,True)
    audit=Counter()
    # Rerun all 8165 cases using the alternative discriminant and receiver formula.
    for case in leer.enumerate_orders():
        audit[leer.fixed(case,e,s,t,'pairwise')]+=1
    allowed={'receiver_order','precursor_order','no_strict_receiver_root','density_domain','vacuum_h','vacuum_u'}
    assert set(audit)<=allowed and set(v['counts'])<=allowed
    assert len(v['rows'])==len({tuple(r[:4]) for r in v['rows']})==sum(audit.values())==8165
    print('PASS — 8165 vacuum-ancestor orders exclude the archived rounded source.')
    witness=paar.run();compare('Paar.json',witness)
    fixed=witness['fixed_rounded']
    assert F(fixed['proof']['lipschitz_upper'])<F(12,1000)
    assert F(fixed['proof']['error_upper'])<F(7,10**7)
    assert all(F(interval[0])>0 for k,interval in fixed['w'].items() if int(k) in paar.FREE)
    assert witness['clock_record']['link']
    print('PASS — N19 inverse fields, unique local fixed-source solution, 11 free clocks and 9 positive densities.')
    print('PASS — separate registered windows, 171 relabellings and missing/ambiguous readout controls.')
    print('Physical P3: 60 NOT_RUN.')


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O')
    verify()
