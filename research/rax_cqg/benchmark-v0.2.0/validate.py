"""Re-run bounded release checks and write a scoped machine-readable report."""
import hashlib
import io
import json
import platform
import subprocess
import sys
import time
import unittest
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import t
from rax_cqg_twin import VERSION,diagnose,experiment,load_experiment

ROOT=Path(__file__).resolve().parent


def compare_metrics(expected,actual):
    if set(expected)!=set(actual):raise AssertionError('metric keys differ')
    for key,value in expected.items():
        if value is None:
            if actual[key] is not None:raise AssertionError(key)
        else:np.testing.assert_allclose(actual[key],value,atol=1e-9,rtol=1e-9,err_msg=key)


def main():
    started=time.monotonic();evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
    log=io.StringIO()
    suite=unittest.defaultTestLoader.discover(str(ROOT/'tests'),pattern='test_*.py')
    tests=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    (evidence/'unittest.txt').write_text(log.getvalue())
    if not tests.wasSuccessful():print(log.getvalue());return 1
    template=(ROOT/'web/lab_template.html').read_text()
    expected_html=template.replace('/*__CORE__*/',(ROOT/'web/rax_core.js').read_text()).replace('/*__UI__*/',(ROOT/'web/lab_ui.js').read_text())
    if expected_html!=(ROOT/'rax_cqg_lab.html').read_text():raise AssertionError('HTML is not the current build; run build_web.py')
    ui=json.loads(subprocess.check_output(['node',str(ROOT/'tests/ui_logic_test.js')],text=True))
    (evidence/'ui_logic_results.json').write_text(json.dumps(ui,indent=2,allow_nan=False)+'\n')
    exported=load_experiment(ui['export_fixture']);compare_metrics(diagnose(exported),ui['export_fixture']['metrics'])
    sweep=json.loads((ROOT/'rax_cqg_sweep_results.json').read_text())
    if sweep.get('schema')!='RAX-CQG-SWEEP-0.2':raise AssertionError('wrong sweep schema')
    for name,expected_hash in sweep['source_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=expected_hash:raise AssertionError('stale sweep source hash: '+name)
    for record in sweep['runs']:
        meta=record['generator'];regenerated=experiment(meta['model'],meta['size'],meta['seed'],meta['p'] if meta['p'] is not None else .25)
        checked=load_experiment(record)
        if checked.rows()!=regenerated['relation_rows']:raise AssertionError('seed replay mismatch')
        compare_metrics(regenerated['metrics'],record['metrics'])
    for group in sweep['groups']:
        runs=[r for r in sweep['runs'] if r['generator']['model']==group['model'] and r['generator']['size']==group['size'] and r['generator']['p']==group['p']]
        if len(runs)!=group['replicates']:raise AssertionError('replicate count mismatch')
        for metric,summary in group['summary'].items():
            vals=np.array([r['metrics'][metric] for r in runs if r['metrics'][metric] is not None]);n=len(vals)
            if summary['count']!=n or summary['undefined_count']!=len(runs)-n:raise AssertionError('summary missing-value mismatch')
            if n:
                np.testing.assert_allclose(summary['mean'],vals.mean(),atol=1e-12)
            if n>1:
                sd=float(vals.std(ddof=1));half=float(t.ppf(.975,n-1))*sd/n**.5
                np.testing.assert_allclose(summary['t95_interval'],[vals.mean()-half,vals.mean()+half],atol=1e-12)
    sources=['rax_cqg_twin.py','rax_cqg_matter_astrolab.py','rax_cqg_reference_models.py','run_sweep.py','build_web.py','validate.py',
             'web/rax_core.js','web/lab_ui.js','web/lab_template.html','tests/test_science.py','tests/js_bridge.js','tests/ui_logic_test.js','rax_cqg_lab.html']
    report={'schema':'RAX-CQG-RELEASE-CHECKS-0.2','software_version':VERSION,'date':'2026-10-16',
            'result':'PASS_WITH_EXPLICIT_SCOPE_LIMITS','unittest_cases':tests.testsRun,
            'exhaustive_small_order_check':{'upper_DAGs_on_5_labels':1024,'distinct_transitive_orders':357,'reference':'independent graph reachability, explicit interval sets and brute-force chain subsets'},
            'javascript_python_parity_cases':28,'numeric_comparison':{'atol':1e-9,'rtol':1e-9},
            'ui_logic_checks':ui['count'],'ui_export_python_roundtrip':'PASS',
            'sweep_runs_replayed':len(sweep['runs']),'sweep_groups_verified':len(sweep['groups']),
            'visual_browser_QA':'NOT_RUN: managed environment has no supported browser-control capability; Node VM DOM tests are not visual QA',
            'scientific_scope':['finite mathematical/implementation consistency only','4D BDG interval bracket, not continuum curvature validation',
                                'conditioned fixed-N sprinklings, not Poisson count sampling','classical stable graph-field reference',
                                'assumed two-qubit clock, not emergence of quantum mechanics','no QSG, KR suppression, Hauptvermutung or continuum-limit claim'],
            'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,
                           'node':subprocess.check_output(['node','--version'],text=True).strip(),'platform':platform.platform()},
            'duration_seconds':time.monotonic()-started,
            'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in sources}}
    (ROOT/'VALIDATION.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:report[k] for k in ['result','unittest_cases','javascript_python_parity_cases','ui_logic_checks','sweep_runs_replayed','sweep_groups_verified','duration_seconds']},indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
