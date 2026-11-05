"""Produce early-data forecasts before any late propagation is performed."""
from pathlib import Path
import hashlib
import json
from states import early_moments

ROOT=Path(__file__).resolve().parent


def seal():
    plan=ROOT/'plan.json'
    if hashlib.sha256(plan.read_bytes()).hexdigest()!=(ROOT/'PLAN_SHA256').read_text().split()[0]:
        raise ValueError('Plan changed')
    return json.loads(plan.read_text())


if __name__=='__main__':
    plan=seal();path=ROOT/'forecast.json'
    if path.exists():raise SystemExit('Existing forecast is immutable; use verify.py for replay')
    data={'plan_sha256':hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest(),
          'uses_late_evolution':False,'cases':{c['id']:early_moments(c) for c in plan['cases']}}
    path.write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    (ROOT/'FORECAST_SHA256').write_text(hashlib.sha256(path.read_bytes()).hexdigest()+'  forecast.json\n')
    print(json.dumps({k:{f:v[f] for f in ('T_b','V_b')} for k,v in data['cases'].items()},indent=2))
