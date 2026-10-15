"""Portable audit of the unchanged frozen pilot, including threshold roundoff.

Scores retain the originally specified replay tolerance. Decisions are checked
exactly against canonical saved scores and frozen thresholds. Only non-evaluation
roundoff at a boundary can be reconciled; ambiguous evaluation decisions fail.
The frozen calculation source, fit and observed results are never rewritten.
"""
import argparse
import json
import math
from pathlib import Path
import sys

import pilot

ROOT = Path(__file__).resolve().parent


def reconcile_decisions(saved, computed, thresholds):
    pilot.require(len(saved) == len(computed), 'OUTPUT_RECORD_COUNT')
    reconciled = []
    for canonical, actual in zip(saved, computed):
        for name in ['bearing_id','record_id','split','label']:
            pilot.same(canonical[name], actual[name], name)
        pilot.same(canonical['scores'], actual['scores'], 'scores')
        pilot.require(canonical['decisions'].keys() == thresholds.keys(), 'DECISION_METHODS')
        for method, threshold in thresholds.items():
            exact = canonical['scores'][method] >= threshold
            pilot.require(canonical['decisions'][method] is exact, 'CANONICAL_DECISION_MISMATCH')
            near = math.isclose(actual['scores'][method], threshold, rel_tol=1e-10, abs_tol=1e-12)
            if actual['split'] == 'evaluation':
                pilot.require(not near and actual['decisions'][method] is exact,
                              'UNSTABLE_EVALUATION_DECISION')
            elif actual['decisions'][method] is not exact:
                pilot.require(near and math.isclose(canonical['scores'][method], threshold,
                              rel_tol=1e-10, abs_tol=1e-12), 'NONNUMERICAL_DECISION_MISMATCH')
                actual['decisions'][method] = exact
                reconciled.append(actual['bearing_id']+':'+method)
    return reconciled


def verify(data, fit_path, report_path):
    saved, fitted = pilot.read(report_path), pilot.read(fit_path)
    computed = pilot.run(data, fit_path, saved['started_utc'])
    # Check the stored numerical calibration exactly, without changing its values.
    validation = [r for r in saved['records'] if r['split']=='validation' and r['label']=='healthy']
    pilot.require([r['bearing_id'] for r in validation] == ['K003','K004'], 'CANONICAL_VALIDATION_UNITS')
    for method, threshold in fitted['thresholds'].items():
        expected = math.nextafter(max(r['scores'][method] for r in validation), math.inf)
        pilot.require(threshold == expected, 'CANONICAL_FIT_RULE')
    reconciled = reconcile_decisions(saved['records'], computed['records'], fitted['thresholds'])
    pilot.same(saved, computed)
    return dict(status='REPLAY_PASS', units=computed['units_total'],
        industrial_claim_supported=False, evaluation_decisions_numerically_stable=True,
        non_evaluation_roundoff_reconciliations=reconciled,
        frozen_report_sha256=pilot.sha(report_path), verifier_sha256=pilot.sha(Path(__file__)))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data',type=Path,default=ROOT/'data')
    p.add_argument('--fit',type=Path,default=ROOT/'evidence/fit.json')
    p.add_argument('--report',type=Path,default=ROOT/'evidence/pilot-report.json')
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    try:
        value=verify(a.data,a.fit,a.report)
        if a.output:pilot.write_new(a.output,value)
        print(json.dumps(value))
        return 0
    except (ValueError,KeyError,TypeError,OSError,IndexError) as exc:
        print(json.dumps({'status':'INVALID','reason':str(exc),'industrial_claim_supported':False}),file=sys.stderr)
        return 2


if __name__=='__main__':raise SystemExit(main())
