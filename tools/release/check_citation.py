"""Build-time metadata check; the offline reproduction does not need these packages."""
import hashlib
import json
from pathlib import Path
import urllib.request
import yaml
import jsonschema
ROOT=Path(__file__).resolve().parents[2]
evidence=json.loads((ROOT/'docs/validation-v1/evidence/citation-validation.json').read_text())
raw=urllib.request.urlopen(evidence['schema_url'],timeout=30).read()
if hashlib.sha256(raw).hexdigest()!=evidence['schema_sha256']:raise ValueError('CFF schema drift')
citation=(ROOT/'CITATION.cff').read_bytes()
if hashlib.sha256(citation).hexdigest()!=evidence['citation_sha256']:raise ValueError('CFF validation evidence stale')
jsonschema.validate(yaml.safe_load(citation),json.loads(raw),format_checker=jsonschema.FormatChecker())
print('CFF_1_2_0_PASS')
