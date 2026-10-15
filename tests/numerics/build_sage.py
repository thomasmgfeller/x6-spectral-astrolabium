#!/usr/bin/env python3
"""Make a standalone exact Sage check from the actual source-bound repaired output."""
from pathlib import Path
from fractions import Fraction
import argparse,hashlib,json

ap=argparse.ArgumentParser();ap.add_argument('output_json',type=Path);ap.add_argument('sage_file',type=Path);args=ap.parse_args()
data=json.loads(args.output_json.read_text())
if data['source']['source_dirty']:raise ValueError('Refusing uncommitted application source')
q=lambda x:str(Fraction(x))
cases=[]
for name in ['scaled_pair_0','scaled_pair_-50']:
    r=next(r for r in data['runs'] if r['id']==name)
    cases.append({'id':name,'weight':str(Fraction(r['input'].splitlines()[-1].split()[2])),
        'L':[[q(x) for x in row] for row in r['L']],
        'values':[q(e['value']) for e in r['eigenpairs']],
        'vectors':[[q(x) for x in e['vector']] for e in r['eigenpairs']],
        'converged':r['analysis']['numerical']['converged'],'rotations':r['analysis']['numerical']['sweeps'],
        'parity':r['observation_parity']})
payload={'commit':data['source']['commit'],'app_sha256':data['source']['app_sha256'],'kernel_sha256':data['source']['kernel_sha256'],'output_sha256':hashlib.sha256(args.output_json.read_bytes()).hexdigest(),'cases':cases}
blob=json.dumps(payload,separators=(',',':'))
header='import json, hashlib\nfrom sage.all import *\nfrom sage.env import SAGE_VERSION\n'
header+='DATA_TEXT = '+repr(blob)+'\n'
header+='assert hashlib.sha256(DATA_TEXT.encode()).hexdigest() == '+repr(hashlib.sha256(blob.encode()).hexdigest())+'\n'
body='''data=json.loads(DATA_TEXT)
assert [r['id'] for r in data['cases']]==['scaled_pair_0','scaled_pair_-50']
tol=QQ(1)/10**12
print('Sage-Version:',SAGE_VERSION)
print('X6-Reparatur-Commit:',data['commit'])
print('App-SHA256:',data['app_sha256'])
print('Exakte Rechnung mit rational transportierten binary64-Ausgaben.')
for r in data['cases']:
    w=QQ(r['weight'])
    L=matrix(QQ,[[w,-w],[-w,w]])
    assert matrix(QQ,r['L'])==L
    ref=sorted(L.eigenvalues())
    assert ref==[0,2*w]
    values=list(map(QQ,r['values']))
    V=matrix(QQ,[[QQ(x) for x in v] for v in r['vectors']]).transpose()
    assert V.dimensions()==(2,2) and len(values)==2
    s=2*w
    eigerr=max(abs(values[j]-ref[j])/s for j in range(2))
    res2=[]
    for j in range(2):
        v=V.column(j);res=L*v-values[j]*v
        assert v.dot_product(v)>0
        res2.append(res.dot_product(res)/(s*s*v.dot_product(v)))
    orth=V.transpose()*V-identity_matrix(QQ,2)
    orth2=sum(x*x for x in orth.list())
    assert eigerr<=tol and max(res2)<=tol*tol and orth2<=tol*tol
    assert r['converged'] is True and r['rotations']>0 and r['parity'] is True
    print(r['id']+': REPARATUR PASS')
    print('  Eigenwertfehler / Matrixnorm:',eigerr)
    print('  Residuenquadrate / Matrixnorm^2:',res2)
    print('  Rotationen:',r['rotations'])
    if r['id']=='scaled_pair_-50':
        assert w==QQ(1)/2**50
        old=[w,w]
        assert max(abs(old[j]-ref[j])/s for j in range(2))==QQ(1)/2
        print('  Historischer Fehler 1/2 bleibt dokumentiert; neue Ausgabe besteht.')
print('GESAMT: PASS - 2/2 exakte Sage-Reparaturpruefungen')
print('Geltung: diese zwei X6-Ausgaben; kein allgemeiner Beweis, kein X6-Browserlauf.')
'''
args.sage_file.write_text(header+body)
print(str(args.sage_file))
