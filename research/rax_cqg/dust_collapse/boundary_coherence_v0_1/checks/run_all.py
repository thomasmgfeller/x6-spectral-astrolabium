#!/usr/bin/env python3
"""Replay only this small follow-up package; never rerun the old quadrature."""
from pathlib import Path
import json
import subprocess
import sys

BASE=Path(__file__).resolve().parents[1]
ORDER=['interference.py','root_exact_audit.py','r_records.py','extended_R.py',
       'root_R_audit.py','physical_gate.py','hilbert_audit.py']
results=[]
for name in ORDER:
    p=subprocess.run([sys.executable,str(BASE/'checks'/name)],cwd=BASE,
                     capture_output=True,text=True)
    results.append({'script':name,'exit_code':p.returncode})
    print(name+': '+('PASS' if p.returncode==0 else 'FAIL'),flush=True)
    if p.returncode:
        print(p.stdout)
        print(p.stderr,file=sys.stderr)
        raise SystemExit(p.returncode)
expected={'root_exact_audit.json':'all_checks_pass','root_R_audit.json':'all_checks_pass',
          'physical_gate.json':'checks_passed','hilbert_audit.json':'all_checks_pass'}
for name,key in expected.items():
    d=json.loads((BASE/'checks'/name).read_text())
    assert d[key] is True,(name,key)
for name,key in [('interference_results.json','new_integrals_evaluated'),
                 ('extended_R_results.json','new_clock_integrals_evaluated'),
                 ('r_records_results.json','new_clock_integrations')]:
    assert json.loads((BASE/'checks'/name).read_text())[key]==0,name
result={'id':'BOUNDARY-COHERENCE-REPLAY-0.1','all_scripts_passed':True,
        'runs':results,'new_clock_integrations':0,
        'physical_eligibility':'HOLD_NOT_DERIVED',
        'qualification':'Passing replay confirms the declared finite calculations. It does not make the physical gates pass or independently regenerate inherited amplitude enclosures.'}
(BASE/'checks/replay.json').write_text(json.dumps(result,indent=2)+'\n')
print('Completed: finite calculations PASS; physical geometry comparison HOLD.')
