"""Reproduce all archived and new finite checks from a clean offline directory."""
import sys
sys.dont_write_bytecode=True
from hashlib import sha256
import json
import subprocess
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from basisdaten import ROOT,read
import antwort
import rand
import gegenrechnung
import anfangsvergleich


def compare(file,data):
    assert (ROOT/file).read_bytes()==(json.dumps(data,indent=2,sort_keys=True)+'\n').encode(),file


def main():
    for file in ('SHA256SUMS','Pruefplan.sha256','Randkontrolle.sha256'):
        for row in (ROOT/file).read_text().splitlines():
            digest,name=row.split('  ',1)
            assert sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    archive=ROOT/'basis/Zeigerstudie.zip'
    refs=json.loads((ROOT/'Quellen.json').read_bytes())
    for name,item in refs.items():
        assert sha256((ROOT/name).read_bytes()).hexdigest()==item['sha256'],name
    assert refs['basis/Zeigerstudie.zip']['sha256']=='a537def35e23fca60b5eefeb91d48b16e063e6fb41028bb93298d7874069cd7e'
    with TemporaryDirectory() as tmp,ZipFile(archive) as z:
        z.extractall(tmp)
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=tmp,check=True)
        code=("import json; from vorstudie import inputs\n"
              "with inputs() as (bg,select,matrices,_):\n"
              " print(json.dumps([sorted(bg.relation),select(bg),matrices[0]]))")
        rel,marked,b=json.loads(subprocess.check_output([sys.executable,'-B','-c',code],cwd=tmp))
        _,_,ours,weights,_,_=read()
        assert set(map(tuple,rel))==ours and marked==[16,18]
        assert all(b[j][i]==weights[i,j] for i,j in ours)
    compare('Dirichlet.json',antwort.run())
    compare('Anfangsdaten.json',rand.run())
    compare('Gegenrechnung.json',gegenrechnung.audit())
    compare('Ein_weiterer_Anfangsimpuls.json',anfangsvergleich.reduced_gate())
    print('PASS: native Dirichlet Hessian, reciprocal susceptibility and finite two-window exclusion.')
    print('PASS: released future, matched boundary momenta, collective counterexamples and reduced input check.')
    print('PASS: four exact quadratic-field controls with all 20 native equations and two homogeneous continuations.')
    print('Physical P3 checkpoints: 60 NOT_RUN.')


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    main()
