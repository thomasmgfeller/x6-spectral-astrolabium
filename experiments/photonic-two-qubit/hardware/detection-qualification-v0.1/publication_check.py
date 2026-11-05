"""Publication integrity checks, independent of the immutable delivered verifier."""
from pathlib import Path
import hashlib,json,zipfile
import analysis
ROOT=Path(__file__).resolve().parent
manifest=json.loads((ROOT/'SHA256.json').read_text())
expected=set(manifest['files'])|{'SHA256.json'}
assert len(expected)==20
with zipfile.ZipFile(ROOT/'X6_Detektionsqualifikation_v0_1_Pruefpaket.zip') as archive:
    prefix='X6_Detektionsqualifikation_v0_1/'
    assert len(archive.namelist())==len(expected)
    assert set(archive.namelist())=={prefix+n for n in expected}
    assert archive.testzip() is None
    for n in expected:assert archive.read(prefix+n)==(ROOT/n).read_bytes(),n
for n,h in manifest['files'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
contract=json.loads((ROOT/'Referenzvertrag.json').read_text())
record=json.loads((ROOT/'Referenzmessung.template.json').read_text())
assert contract['hardware_status']=='NOT_RUN' and contract['bom_freeze']=='HOLD'
assert len(contract['required_tests'])==15
front=json.loads((ROOT/'Eigenfrontend_Pruefmatrix.json').read_text())
assert len(front['electrical'])==10 and len(front['full_detector_only'])==7
assert all(r['status']=='NOT_RUN' for r in front['electrical']+front['full_detector_only'])
actual=analysis.reference_screen(record,contract,ROOT)
assert actual==json.loads((ROOT/'Referenzscreen_TEMPLATE.json').read_text())
assert actual['screen_status']=='HOLD' and actual['physical_qualification']=='NOT_RUN'
assert analysis.design_results()==json.loads((ROOT/'Rechenergebnisse.json').read_text())
validation=json.loads((ROOT/'Validierung.json').read_text())
assert validation['software_tests']['count']==47
assert validation['hardware_measurements']=='NOT_RUN' and validation['bom_freeze']=='HOLD'
print('PASS: original ZIP bytes, 19 hashes, 15/10/7 test scopes, empty template HOLD; hardware NOT_RUN')
