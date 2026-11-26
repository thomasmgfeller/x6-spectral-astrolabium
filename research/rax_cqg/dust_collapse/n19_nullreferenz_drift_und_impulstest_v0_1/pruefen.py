"""Verify registered files, reproduce PR 392, and compare six new reports byte-for-byte."""
from fractions import Fraction as F
from hashlib import sha256
import json
import subprocess
import sys
from basisdaten import ROOT,inputs


def compare(name,data):
    encoded=(json.dumps(data,indent=2,sort_keys=True)+'\n').encode()
    if encoded!=(ROOT/name).read_bytes():raise ValueError('abweichendes Ergebnis: '+name)
    print('PASS',name,flush=True)


def main():
    if not __debug__:raise SystemExit('Python ohne -O starten.')
    for file in [ROOT/'SHA256SUMS',*sorted(ROOT.glob('*.sha256'))]:
        for line in file.read_text().splitlines():
            digest,path=line.split('  ',1)
            assert sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    with inputs() as (parent,_,previous,early):
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=parent,check=True)
        import nullreferenz,volltest,driftprobe,impulsprobe,drifteichung,impulstest
        from gemischt import ORDER
        assert all(edge in ORDER for edge in [(0,16),(0,18),(18,7)])
        data=nullreferenz.run(previous,early)
        compare('Nullreferenz.json',data)
        assert all(row['joint_pass']==144 for row in data['mesh'] if row['m']=='1')
        prior=json.loads((parent/'Streuungskontrollen.json').read_bytes())
        for row in prior['actual_n19_failure_witnesses']:
            cases=[v for v in data['false_pulse_replay'] if v['route']==row['route'] and v['k']==row['kappa']]
            assert [v['raw'] for v in cases]==row['two_sites_by_sign']
        all_atoms=volltest.run(previous,early)
        compare('Volltest.json',all_atoms)
        assert len(all_atoms['families'])==144
        for row in all_atoms['families']:
            assert F(row['referenced']['unresolved'])==0
            assert (F(row['referenced']['wrong'])==0)==(row['k']=='1')
            if row['original']:assert F(row['original']['wrong'])>F(row['referenced']['wrong'])
        compare('Driftkontrollen.json',driftprobe.run())
        compare('Synthetische_Eichreihe.json',driftprobe.fixture())
        compare('Impulskontrollen.json',impulsprobe.run())
        compare('Synthetische_Impulsproben.json',impulsprobe.fixture())
        empty=json.loads((ROOT/'Messstand.json').read_bytes())
        cal=drifteichung.evaluate(empty)
        assert cal['scale_status']=='NOT_MEASURED' and impulstest.evaluate(empty,cal)['status']=='NOT_MEASURED'
    print('PASS Referenz, Drift, Impulstest. Physische Messungen: 0; P3: 60 NOT_RUN.')


if __name__=='__main__':main()
