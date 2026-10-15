import json, hashlib
from sage.all import *
from sage.env import SAGE_VERSION
DATA_TEXT = '{"commit":"7715b7d07ec333c838ca6a4f1da503253b75ea8b","app_sha256":"56df754a1c5c3d26022e54b000f0d9e52ab4067d39e6a664556de12bfd7dc071","kernel_sha256":"02345490b0aee9a4c1bfc53ba4ce724e396d227ec842dc7d3e24309af89fd5cb","output_sha256":"384c3e806560edea1874861829d64bd06f6f857507fed0cd2b5f70d986ff28f6","cases":[{"id":"scaled_pair_0","weight":"1","L":[["1","-1"],["-1","1"]],"values":["0","4503599627370495/2251799813685248"],"vectors":[["1592262918131443/2251799813685248","1592262918131443/2251799813685248"],["1592262918131443/2251799813685248","-1592262918131443/2251799813685248"]],"converged":true,"rotations":1,"parity":true},{"id":"scaled_pair_-50","weight":"1/1125899906842624","L":[["1/1125899906842624","-1/1125899906842624"],["-1/1125899906842624","1/1125899906842624"]],"values":["0","4503599627370495/2535301200456458802993406410752"],"vectors":[["1592262918131443/2251799813685248","1592262918131443/2251799813685248"],["1592262918131443/2251799813685248","-1592262918131443/2251799813685248"]],"converged":true,"rotations":1,"parity":true}]}'
assert hashlib.sha256(DATA_TEXT.encode()).hexdigest() == '1598aa23a8b69afe5ab69b7647b8bde5a4c88aa093ca7f71eb15781be25f2519'
data=json.loads(DATA_TEXT)
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
