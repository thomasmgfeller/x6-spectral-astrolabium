"""Verify the delivered archive, its extracted bytes and scientific status."""
import hashlib
import json
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'SHA256.json').read_text())
assert manifest['algorithm'] == 'SHA-256'
with zipfile.ZipFile(root / 'X6_Polarisation_Filter_Spektral_v0_1_Pruefpaket.zip') as z:
    assert z.testzip() is None
    assert set(z.namelist()) == set(manifest['files']) | {'SHA256.json'}
    for name in z.namelist():
        assert Path(name).name == name, name
        assert z.read(name) == (root / name).read_bytes(), name
    for name, digest in manifest['files'].items():
        assert hashlib.sha256(z.read(name)).hexdigest() == digest, name
spec = json.loads((root / 'Spezifikation.json').read_text())
assert len(spec['polarization_transfer']) == 16
assert len(spec['spectral_matrix']) == 23
assert len(spec['filter_positions']) == 6
assert spec['bom_status'] == 'HOLD'
assert spec['spectral_hardware_status'] == 'NOT_RUN'
assert all(x['measurement_status'] == 'NOT_RUN' and x['result'] is None
           for x in spec['spectral_matrix'])
assert spec['laboratory_records'] == {
    'measured_pump': None, 'filter_curves': [], 'spectra': [], 'relative_phase': None}
from analysis import spectral_overlap
try:
    spectral_overlap(json.loads((root / 'Spektraldaten.template.json').read_text()))
except ValueError:
    pass
else:
    raise AssertionError('empty measurement template must be rejected')
print('PASS: 12 original ZIP members, SHA-256, extracted bytes, 16/23/6 records; hardware NOT_RUN, BOM HOLD')
