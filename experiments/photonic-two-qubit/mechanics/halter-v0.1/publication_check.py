"""Verify immutable mount artifacts and explicit design limits; no hardware qualification."""
from pathlib import Path
import hashlib,json,zipfile,math
P=Path(__file__).resolve().parent
entries={}
for line in (P/'SHA256SUMS.txt').read_text().splitlines():
 h,n=line.split('  ',1)
 assert n not in entries and Path(n).name==n
 entries[n]=h
 assert hashlib.sha256((P/n).read_bytes()).hexdigest()==h,n
expected=set(entries)|{'SHA256SUMS.txt'}
assert len(expected)==24
with zipfile.ZipFile(P/'X6_Halterzeichnungen_v0_1_CAD.zip') as z:
 assert len(z.namelist())==len(expected) and set(z.namelist())==expected
 assert z.testzip() is None
 for n in expected:assert z.read(n)==(P/n).read_bytes(),n
parts=json.loads((P/'Bauteile.json').read_text())
assert {x['id'] for x in parts}=={'H01','H02','H03A','H03B','H04','H05'}
assert all(x['status']=='DESIGN_HOLD' and x['volume_mm3']>0 for x in parts)
assert len(list(P.glob('*.step')))==6 and len(list(P.glob('*.dxf')))==9
v=json.loads((P/'Validierung.json').read_text())
assert v['manufacturing_release']=='HOLD' and v['hardware_status']=='NOT_RUN'
assert v['nominal_height_mm']==75 and v['pdf_page_count']==9
assert len(v['cad'])==6 and all(x['solid_valid'] and x['solids']==1 for x in v['cad'])
layout=json.loads((P/'Layout_Quelle.json').read_text())
coords={x['id']:x for x in layout['components']}
gap=coords['DM']['y_mm']-coords['O04']['y_mm']
c=json.loads((P/'Kollisionspruefung.json').read_text())
assert math.isclose(c['O04_DM_nominal_distance_mm'],gap,abs_tol=1e-10)
assert math.isclose(c['nominal_overlap_mm'],35-gap,abs_tol=1e-10)
assert math.isclose(c['worst_case_overlap_mm'],45-gap,abs_tol=1e-10)
assert c['status']=='FAIL_FOR_THIS_MOUNTING_SCENARIO'
assert c['global_collision_check']=='OPEN' and c['actual_hardware']=='NOT_RUN'
print('PASS: 23 original hashes, 24 ZIP members, 6 CAD parts, 9 DXFs; manufacturing HOLD; O04/DM collision retained')
