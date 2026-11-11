"""Run exact controls and export the 33 declared AA candidate Hessians."""
from pathlib import Path
import argparse
import io
import json
import unittest
import sympy as s
import test_model
from model import ROOT, carrier, bd_matrix, scalar_hessian, gaussian_order, g


def _ids(suite):
    for x in suite:
        if isinstance(x, unittest.TestSuite):
            yield from _ids(x)
        else:
            yield x.id()


def run(out):
    out.mkdir(parents=True, exist_ok=True)
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_model)
    ids = list(_ids(suite))
    log = io.StringIO()
    result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    if not result.wasSuccessful():
        raise RuntimeError(log.getvalue())
    checks = {'tests_run':result.testsRun, 'status':'PASS', 'test_ids':ids,
              'scope':'EXACT_FINITE_ALGEBRA_AND_CONTINUUM_TARGET_IDENTITIES',
              'physical_gates':'HOLD', 'CST_continuum_convergence_proved':False,
              'physical_matter_kernel_computed':False}
    (out/'checks.json').write_text(json.dumps(checks, indent=2, sort_keys=True)+'\n')
    records = []
    for code in carrier('A','A',True):
        B = bd_matrix(code,5)
        H = scalar_hessian(B,[1]*5)
        rel = set(g.pairs(code,5))
        p = sum((i,2) in rel for i in (0,1))
        q = sum((2,j) in rel for j in (3,4))
        records.append({'order_code':code,'F4':int(g.action(code,5)), 'p':p,'q':q,
                        'H0_over_va':[[str(x) for x in row] for row in H.tolist()],
                        'gaussian_order_H0_over_va':[[str(x) for x in row] for row in gaussian_order(H).tolist()],
                        'interior_diagonal_over_va_massless':str(H[2,2]),
                        'interior_diagonal_over_va':'-'+str(s.Rational(p+q,2))+'-u'})
    record = {'scope':'33_DECLARED_AA_CONTROL_HISTORIES_WITH_EXPLICIT_SCALAR_ACTION',
              'physical_history_measure_derived':False,
              'physical_kernel_entries':None,
              'units':{'a':'4/(sqrt(6)*ell^2)','v':'ell^4','u':'mu^2/a',
                       'full_H':'v*a*(H0_over_va-u*I5)','mu2_domain':'nonnegative'},
              'order':[0,1,2,3,4], 'gaussian_order':[0,1,3,4,2],
              'interior_gap_bound':'abs(H_II) >= v*(a+mu^2) > 0 for fixed ell>0',
              'bound_not_uniform_in_ell':'v*a tends to zero as ell tends to zero; no continuum bound claimed',
              'covered_AA_histogram':{'-1-u':20,'-3/2-u':12,'-2-u':1},
              'histories':records}
    (out/'aa_hessians.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    print(f'{result.testsRun} exact tests PASS; {len(records)} candidate AA Hessians; physical gates HOLD')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, default=ROOT/'results')
    run(p.parse_args().out)
