# X6 Check 3: exact confirmation of the minimal scaling counterexample.
import json, hashlib
from fractions import Fraction
from sage.all import *
from sage.env import SAGE_VERSION
DATA_TEXT = '{"commit":"7257e51a8df93ff1722d1116103143cc6c827ef4","kernel_sha256":"a5adaeb576e6e0417023cc61ac4e431b782362843c2110f121c82d1f8227b46e","cases":[{"id":"scaled_pair_0","input":"v0\\nv1\\nv0 v1 1","L":[["1","-1"],["-1","1"]],"eigenvalues":["0","4503599627370495/2251799813685248"],"vectors":[["1592262918131443/2251799813685248","1592262918131443/2251799813685248"],["1592262918131443/2251799813685248","-1592262918131443/2251799813685248"]],"converged":true,"rotations":1,"observation_parity":true},{"id":"scaled_pair_-50","input":"v0\\nv1\\nv0 v1 0.00000000000000088817841970012523233890533447265625","L":[["1/1125899906842624","-1/1125899906842624"],["-1/1125899906842624","1/1125899906842624"]],"eigenvalues":["1/1125899906842624","1/1125899906842624"],"vectors":[["1","0"],["0","1"]],"converged":true,"rotations":0,"observation_parity":true}]}'
assert hashlib.sha256(DATA_TEXT.encode()).hexdigest() == '7381dabf0959ac92b2cb3896f92e396362d4085ea98773491a418318a0725fff'
data=json.loads(DATA_TEXT)
assert data['commit']=='7257e51a8df93ff1722d1116103143cc6c827ef4'
assert data['kernel_sha256']=='a5adaeb576e6e0417023cc61ac4e431b782362843c2110f121c82d1f8227b46e'
assert [r['id'] for r in data['cases']]==['scaled_pair_0','scaled_pair_-50']
tol=QQ(1)/10**12
print('Sage-Version:',SAGE_VERSION)
print('X6-Commit:',data['commit'])
print('Quelle: echte Node.js-Ausgaben; Eigenvektoren nur beobachtend exportiert.')
statuses=[]
for r in data['cases']:
    w=QQ(str(Fraction(r['input'].splitlines()[-1].split()[2])))
    L=matrix(QQ,[[w,-w],[-w,w]])
    assert matrix(QQ,r['L'])==L
    lam=list(map(QQ,r['eigenvalues']))
    V=matrix(QQ,[[QQ(x) for x in v] for v in r['vectors']]).transpose()
    ref=sorted(L.eigenvalues())
    assert ref==[0,2*w]
    s=2*w
    rel_error=max(abs(lam[j]-ref[j])/s for j in range(2))
    residuals_squared=[]
    for j in range(2):
        v=V.column(j)
        rv=L*v-lam[j]*v
        residuals_squared.append(rv.dot_product(rv)/(s*s*v.dot_product(v)))
    orth=V.transpose()*V-identity_matrix(QQ,2)
    orth_squared=sum(x*x for x in orth.list())
    good=(rel_error<=tol and max(residuals_squared)<=tol*tol and orth_squared<=tol*tol)
    status='PASS' if good else 'FAIL'
    statuses.append(status)
    print(r['id']+': X6 '+status)
    print('  Soll-Eigenwerte:',ref)
    print('  X6-Eigenwerte:',lam)
    print('  Skalierter Eigenwertfehler:',rel_error)
    print('  Skalierte Residuenquadrate:',residuals_squared)
    print('  X6 converged:',r['converged'],'; Rotationen:',r['rotations'])
    assert r['observation_parity'] is True
    if r['id']=='scaled_pair_-50':
        assert w==QQ(1)/2**50
        assert lam==[w,w]
        assert V==identity_matrix(QQ,2)
        assert rel_error==QQ(1)/2
        assert residuals_squared==[QQ(1)/4,QQ(1)/4]
        assert r['converged'] is True and r['rotations']==0
assert statuses==['PASS','FAIL']
print('GEGENBEISPIEL: EXAKT BESTAETIGT')
print('X6-ROBUSTHEIT: FAIL fuer kleine Gewichtsskalen; kein allgemeines PASS.')
print('Geltung: zwei eingebettete X6-Ausgaben; kein X6-Browserlauf.')
