#!/usr/bin/env python3
"""Separate engineering evidence from inherited statistical qualification.

Default exit: nonzero for missing/failed engineering evidence; statistical
failures are retained in the JSON. --require-overall also exits 2 if V1b fails.
--native-only is an explicitly incomplete local diagnostic, never a browser PASS.
"""
import argparse
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import gzip
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import platform
import sys

import numpy as np
import scipy
from scipy.stats import binomtest, kstest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
q = json.loads((HERE/'protocol.json').read_text())
sha = lambda b: hashlib.sha256(b).hexdigest()
spec = importlib.util.spec_from_file_location('frozen_port', HERE.parent/'v1b_port_correction/port.py')
port = importlib.util.module_from_spec(spec)
spec.loader.exec_module(port)

def repaired_python_cloud(p):
    rng = port.RNG(p['seed'])
    points, flags = [], []
    rejected = dict(zeroTemporalUniform=0, invalidDirection=0, outsideSupport=0)
    attempts = 0
    for _ in range(p['m']):
        for attempt in range(128):
            attempts += 1
            u = rng()
            if u == 0:
                rejected['zeroTemporalUniform'] += 1
                continue
            a = .5*u**(1/p['d'])
            t = (-1 if rng() < .5 else 1)*(.5-a)
            v = [port.normal(rng) for _ in range(p['d']-1)]
            norm = math.hypot(*v)
            if not norm > 0 or not math.isfinite(norm):
                rejected['invalidDirection'] += 1
                continue
            r = a*rng()**(1/(p['d']-1))
            point = [t]+[x*r/norm for x in v]
            if not all(map(math.isfinite, point)) or not abs(t)+math.hypot(*point[1:]) < .5:
                rejected['outsideSupport'] += 1
                continue
            points.append(point)
            flags.append(abs(t)+math.hypot(*point[1:]) < p['theta']/2)
            break
        else:
            raise RuntimeError('128 rejected candidates')
    return dict(points=points,inside=flags,attempts=attempts,rejected=rejected)

def exact_inside(point, half=.5):
    # Independent high-precision predicate on the actual binary64 coordinates.
    with localcontext() as ctx:
        ctx.prec = 80
        t = abs(Decimal.from_float(point[0]))
        a = Decimal.from_float(half)-t
        return a > 0 and sum(Decimal.from_float(x)**2 for x in point[1:]) < a*a

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    ap.add_argument('--native-only',action='store_true')
    ap.add_argument('--require-overall',action='store_true')
    args = ap.parse_args()
    native_bytes = (args.output/'native_raw.json.gz').read_bytes()
    raw = json.loads(gzip.decompress(native_bytes))
    native = json.loads((args.output/'native_report.json').read_text())
    if native['raw_sha256'] != sha(native_bytes):
        raise ValueError('Native raw evidence hash mismatch')
    for name,digest in raw['provenance']['source_sha256'].items():
        if sha((ROOT/name).read_bytes()) != digest:
            raise ValueError('Tested source differs: '+name)
    support_violations = 0
    max_coordinate_error = 0.
    python_comparisons = []
    python_raw = []
    for c in raw['clouds']+[dict(parameters=dict(m=64,d=b['d'],theta=.5,seed=b['seed']),**b['result']) for b in raw['boundary']]:
        p = c['parameters']
        actual = repaired_python_cloud(p)
        delta = np.abs(np.array(actual['points'])-np.array(c['points']))
        tolerance = q['float_tolerance']['absolute']+q['float_tolerance']['relative']*np.abs(c['points'])
        max_coordinate_error = max(max_coordinate_error,float(delta.max()))
        comparison = dict(parameters=p,coordinate_tolerance_failures=int(np.sum(delta>tolerance)),
            flag_mismatches=sum(a!=b for a,b in zip(actual['inside'],c['inside'],strict=True)),
            attempts_equal=actual['attempts']==c['sampling']['attempts'],rejections_equal=actual['rejected']==c['sampling']['rejected'])
        python_comparisons.append(comparison)
        python_raw.append(dict(parameters=p,**actual))
        support_violations += sum(not exact_inside(pt) for pt in c['points'])
    for c in raw['injected_cases']:
        support_violations += not exact_inside(c['point'])
    py_bytes = gzip.compress(json.dumps(python_raw,separators=(',',':'),allow_nan=False).encode(),mtime=0)
    (args.output/'python_raw.json.gz').write_bytes(py_bytes)
    port_pass = all(c['coordinate_tolerance_failures']==0 and c['flag_mismatches']==0 and c['attempts_equal'] and c['rejections_equal'] for c in python_comparisons)
    ks_results, angular, counts = [],[],[]
    for d in q['dimensions']:
        rows = [c for c in raw['clouds'] if c['d']==d]
        pts = np.concatenate([np.array(c['points']) for c in rows])
        a = .5-np.abs(pts[:,0]); radius = np.linalg.norm(pts[:,1:],axis=1)
        for name,values in [('time',(2*a)**d),('radial',(radius/a)**(d-1))]:
            test = kstest(values,'uniform',method=q['statistics']['time_and_radial']['method'])
            ks_results.append(dict(d=d,kind=name,n=len(values),distance=float(test.statistic),pvalue=float(test.pvalue),
                alpha=q['statistics']['time_and_radial']['alpha_per_test'],passed=bool(test.pvalue>=q['statistics']['time_and_radial']['alpha_per_test'])))
        expected_second = d/(4*(d+1)*(d+2))
        for j in range(1,d):
            x=pts[:,j]
            for name,values,target in [('mean',x,0.),('second_moment',x*x,expected_second)]:
                se=float(np.std(values,ddof=1)/np.sqrt(len(values)))
                z=abs(float(np.mean(values))-target)/se
                angular.append(dict(d=d,axis=j,kind=name,observed=float(np.mean(values)),target=target,standard_errors=z,
                    passed=bool(z<=q['statistics']['angular_moments']['standard_error_limit'])))
        for c in rows:
            for t in c['theta_results']:
                p=t['theta']**d
                test=binomtest(t['k'],q['m'],p)
                alpha=q['statistics']['expanded_counts']['family_alpha']/q['statistics']['expanded_counts']['family_size']
                counts.append(dict(d=d,seed=c['parameters']['seed'],theta=t['theta'],k=t['k'],expected=q['m']*p,
                    z=(t['k']-q['m']*p)/math.sqrt(q['m']*p*(1-p)),pvalue=float(test.pvalue),alpha=alpha,passed=bool(test.pvalue>=alpha)))
    if len(counts)!=q['statistics']['expanded_counts']['family_size']:
        raise ValueError('Incomplete count matrix')
    browser=None
    if not args.native_only:
        browser=json.loads((args.output/'browser_report.json').read_text())
        if browser['native_raw_sha256']!=sha(native_bytes) or browser['provenance']['source_sha256']!=raw['provenance']['source_sha256']:
            raise ValueError('Browser/native provenance mismatch')
        for item in browser['frozen_exports']:
            if sha((args.output/item['file']).read_bytes())!=item['sha256']:
                raise ValueError('Frozen browser export mismatch')
    gates={
        'native_engineering':'PASS' if native['status']=='PASS_NATIVE_ENGINEERING' else 'FAIL',
        'repaired_python_port':'PASS' if port_pass else 'FAIL',
        'strict_support_independent_decimal':'PASS' if support_violations==0 else 'FAIL',
        'browser_and_export_freeze':'OPEN' if browser is None else ('PASS' if browser['status']=='PASS_BROWSER_EXPORT_FREEZE' and browser['matrix_cases']==192 and all(r['export_sha256']==r['replay_sha256'] for r in browser['records']) else 'FAIL'),
        'time_marginals_inherited':'PASS' if all(r['passed'] for r in ks_results if r['kind']=='time') else 'FAIL',
        'radial_marginals_inherited':'PASS' if all(r['passed'] for r in ks_results if r['kind']=='radial') else 'FAIL',
        'angular_moments_new_screen':'PASS' if all(r['passed'] for r in angular) else 'FAIL',
        'expanded_counts_new_screen':'PASS' if all(r['passed'] for r in counts) else 'FAIL'
    }
    engineering=all(gates[k]=='PASS' for k in ['native_engineering','repaired_python_port','strict_support_independent_decimal','browser_and_export_freeze'])
    overall='PASS' if all(x=='PASS' for x in gates.values()) else 'NOT_PASSED'
    report=dict(validation_id=q['validation_id'],schema=q['schema'],timestamp_utc=datetime.now(timezone.utc).isoformat(),
        mode='NATIVE_ONLY_INCOMPLETE' if args.native_only else 'NATIVE_BROWSER_EXPORT',
        provenance=raw['provenance'],analysis_runtime=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
        engineering_status='PASS' if engineering else ('OPEN' if args.native_only else 'FAIL'),overall_V1b=overall,gates=gates,
        support_violations=support_violations,python_port=dict(max_coordinate_error=max_coordinate_error,comparisons=python_comparisons,raw_sha256=sha(py_bytes)),
        ks=ks_results,angular_moments=angular,expanded_counts=counts,
        evidence_sha256={p.name:sha(p.read_bytes()) for p in sorted(args.output.iterdir()) if p.is_file() and p.name not in ['qualification.json','SHA256SUMS']},
        limitations=['Unblinded fixed regression; no proof of PRNG independence or uniformity.',
            'Inherited per-test alpha=0.05 retained; no post-hoc multiplicity adjustment rescues radial failure.',
            'Rejection conditions the finite candidate distribution; no exact continuous-law claim.',
            'Chromium version and OS in browser_report; other browser engines are not certified.',
            'Historical missing-XOR and original boundary evidence remain unmodified.'])
    (args.output/'qualification.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(engineering_status=report['engineering_status'],overall_V1b=overall,gates=gates,ks=ks_results,
        maximum_port_error=max_coordinate_error,count_failures=sum(not c['passed'] for c in counts)),indent=2))
    if not args.native_only and not engineering:
        raise SystemExit(1)
    if args.require_overall and overall!='PASS':
        raise SystemExit(2)

if __name__=='__main__':
    main()
