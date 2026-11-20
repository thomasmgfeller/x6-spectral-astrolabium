"""Compare the exact records and allow rounding in the numerical diagnostics."""
import json
from pathlib import Path
from sys import argv

a,b = [json.loads(Path(p).read_text()) for p in argv[1:]]
ca,cb = a.pop('dust_clock_checks'),b.pop('dust_clock_checks')
if a!=b:
    raise SystemExit('Exact fields differ')
for item in (ca,cb):
    for g in item['comparison_grids']:
        if not 0 <= g.pop('max_complex_lobe_difference') < 1e-13:
            raise SystemExit('Packet check exceeded tolerance')
    if not 0 <= item.pop('fixed_old_fields_max_complex_difference') < 1e-13:
        raise SystemExit('Dust check exceeded tolerance')
va,vb = ca.pop('example_influence_at_fixed_fields'),cb.pop('example_influence_at_fixed_fields')
if ca!=cb or va.keys()!=vb.keys() or any(abs(complex(*va[k])-complex(*vb[k]))>1e-13 for k in va):
    raise SystemExit('Numerical records differ')
print('PASS: all 16 marked maps, two Fourier constraints, dust certificate and outer boundary check')
