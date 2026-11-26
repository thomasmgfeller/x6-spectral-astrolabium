"""Reproduce PR 393 and all eight new JSON files using the Python standard library."""
from fractions import Fraction as F
from hashlib import sha256
import json
import subprocess
import sys
from n19_archiv393 import ROOT,inputs


def compare(name,result):
    raw=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
    if (ROOT/(name+'.json')).read_bytes()!=raw:raise ValueError('abweichendes Ergebnis: '+name)
    print('PASS',name,flush=True)


def main():
    if not __debug__:raise SystemExit('Python ohne -O starten.')
    for file in [ROOT/'SHA256SUMS',*sorted(ROOT.glob('*.sha256'))]:
        for line in file.read_text().splitlines():
            value,name=line.split('  ',1)
            assert sha256((ROOT/name).read_bytes()).hexdigest()==value,name
    with inputs() as (prior,p,e):
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=prior,check=True)
        import empfangsbit,kanalprobe,kollision,kovarianzzeuge,referenzwechsel,zweigleser
        branches=zweigleser.run(p,e);compare('Zweigleser',branches)
        assert branches['count']==sum(x['correct_both'] for x in branches['all_atom_families'])==104976
        assert branches['wrong_or_unresolved_wrong_reference']>0
        assert all(r['joint_pass']==144 for r in branches['continuous_bands'] if F(r['r'])<=1)
        collisions=kollision.run(p,e);compare('Kollisionen',collisions)
        assert len(collisions)==48 and sum(F(x['max_abs_y'])<=64 for x in collisions)==2
        for c in collisions:
            if F(c['max_abs_y'])<=96:
                assert all(a['J']==a['one_bit_label'] for a in c['arms'])
        bits=empfangsbit.proof_rows(p,e);compare('Empfangsbit',bits)
        assert all(r['joint_one_bit']==144 for r in bits if r['m']<=96)
        cov=kovarianzzeuge.run(p,e);compare('Kovarianzzeuge',cov)
        assert cov['late_only']['minimum_error']=='1/4000000'
        test=referenzwechsel.run(p,e);compare('Nulluhrkontrolle',test)
        assert all(row['one_bit_correct_at_m96']==12 for row in test['holdout'])
        controls=kanalprobe.run(p,e,bits);compare('Kanalkontrolle',controls)
        compare('Beispiel_Empfang',controls['examples']['receiver'])
        compare('Beispiel_Speicher',controls['examples']['late'])
        assert controls['concrete_trials']==288
    print('PASS Modell, Referenzen und Empfangsbit. Physische Messungen: 0. P3: 60 NOT_RUN.')


if __name__=='__main__':main()
