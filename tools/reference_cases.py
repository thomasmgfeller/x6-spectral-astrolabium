"""Fixed offline cases and deliberate invalid inputs; Apache-2.0."""
import copy
import importlib.util
import shutil

from tools.reference_suite import ROOT, decode, encode, execute, extract, python, read, rejected, require

ARCHIVES = {
    'rax-w1': ('docs/research/rax/wolfram-check-v0.1/RAX_W1_Exakte_Gegenpruefung_v0_1_Paket.zip',
               'RAX_W1_Exakte_Gegenpruefung_v0_1'),
    'wolfram-polarity': ('docs/signal-lab/wolfram-polarity-v0.1/X6_Wolfram_Fall2_v0_1.zip',
                        'X6_Wolfram_Fall2_v0_1'),
    'wolfram-dependence': ('docs/signal-lab/wolfram-zero-failures-v0.1/X6_Wolfram_Fall4_v0_1.zip',
                          'X6_Wolfram_Fall4_v0_1'),
    'wolfram-causal3': ('docs/research/causal-order/wolfram-countercheck-v0.1/X6_Wolfram_Fall5_v0_1.zip',
                       'X6_Wolfram_Fall5_v0_1'),
}


def module(name, path):
    spec = importlib.util.spec_from_file_location('reference_' + name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def fields(doc, expected):
    for key, value in expected.items():
        require(key in doc and encode(doc[key]) == encode(value), 'Expected result: ' + key)


def run_cases(work):
    reports, controls, packages = {}, [], {}
    for name, (archive, root) in ARCHIVES.items():
        extract(archive, work / name)
        packages[name] = work / name / root

    graph_dir = work / 'graphs'; graph_dir.mkdir()
    shutil.copyfile(ROOT / 'tests/python/independent_audit.py', graph_dir / 'audit.py')
    graph = python('audit.py', graph_dir)
    fields(graph, {'schema': 'x6-community-audit-1', 'passed': 5, 'total': 5})
    expected = [('path4', '1/2', '3/5', True), ('triangle', '2', '3', True),
                ('weighted2', '1/8', '1/4', True),
                ('rounded_signal_path', '367879/6000000', '1/2', True),
                ('disconnected', '1/10', '1/2', False)]
    require(len(graph['results']) == 5, 'Graph result coverage')
    for row, (name, bound, invalid, accepted) in zip(graph['results'], expected):
        fields(row, {'name': name, 'valid_bound': bound, 'invalid_bound': invalid,
                     'valid_accepted': accepted, 'expected_valid': accepted,
                     'invalid_rejected': True, 'pass_': True})
    reports['rational-graphs'] = graph
    audit = module('graphs', graph_dir / 'audit.py')
    for name, edges in [('graph-self-loop', [(0, 0, '1')]),
                        ('graph-negative-weight', [(0, 1, '-1')]),
                        ('graph-zero-weight', [(0, 1, '0')])]:
        controls.append(rejected(lambda: audit.laplacian(2, edges), name))

    n6 = ROOT / 'references/causal-order-n6'
    report = python(n6 / 'verify.py', work, n6 / 'atlas_n6.json', '--output', work / 'n6.json')
    fields(report, {'status': 'PASS', 'representatives_checked': 318,
                    'natural_orders_checked': 4824, 'exact_polynomials_checked': 4208})
    atlas = decode(read(n6 / 'atlas_n6.json'))
    reports['causal-n6'] = dict(report, collision_summary=atlas['summary'])
    verifier = module('n6', n6 / 'verify.py')
    for name in ('causal-missing-order', 'causal-self-loop', 'causal-wrong-polynomial',
                 'causal-missing-quill', 'causal-false-collision-list'):
        bad = copy.deepcopy(atlas)
        if name == 'causal-missing-order':
            bad['records'].pop()
        elif name == 'causal-self-loop':
            bad['records'][0]['causal_matrix'][0][0] = 1
        elif name == 'causal-wrong-polynomial':
            bad['records'][0]['polynomials_S_A_K'][0][0] += 1
        elif name == 'causal-missing-quill':
            bad['records'][0]['quills'].pop()
        else:
            bad['summary']['three_spectra']['collision_groups'] = []
        controls.append(rejected(lambda: verifier.verify(bad), name))

    rax = packages['rax-w1']
    inventory = python('verify_package.py', rax)
    fields(inventory, {'status': 'PASS', 'errors': []})
    python('verify.py', rax, '--output', work / 'rax-full.json')
    report = decode(read(work / 'rax-full.json'))
    report.pop('local_python')
    fields(report, {'status': 'PASS_WITH_SCOPE_LIMITS', 'selected_matrices': 44,
                    'matrix_digest_matches': 44, 'lumpable': 10, 'not_lumpable': 34,
                    'relabeling_checks': 44, 'power_checks': 20, 'shift_controls': 10,
                    'invalid_matrix_controls': 2, 'symbolic_boolean_checks': 7,
                    'constant_minimax': '1/20', 'constant_optimizer': '2/5',
                    'external_review': False, 'physical_validation': False})
    require(len(report['case_results']) == 44 and len(report['shift_results']) == 10,
            'RAX full detail coverage')
    reports['rax-w1'] = {'inventory': inventory, 'verification': report}
    rv = module('rax', rax / 'verify.py')
    symbolic, parts = rv.load_wolfram()
    for name in ('rax-missing-wolfram-row', 'rax-wrong-prediction-loss'):
        bad = copy.deepcopy(parts)
        if name == 'rax-missing-wolfram-row':
            bad[0]['cases'].pop()
        else:
            bad[0]['cases'][0]['prediction_loss'] = '999'
        controls.append(rejected(lambda: rv.verify(symbolic, bad), name))

    polarity = packages['wolfram-polarity']
    report = python('verify.py', polarity, '--rerun')
    report.pop('fresh_node')
    fields(report, {'status': 'PASS_WITH_SCOPE_LIMITS', 'symbolic_checks': 4,
                    'wolfram_metric_checks': 12, 'wolfram_reexecuted': False,
                    'first_attempt_failure_retained': True})
    reports['wolfram-polarity'] = report
    pv = module('polarity', polarity / 'verify.py')
    wolfram = pv.read('wolfram_result.json'); contract = pv.read('contract.json')
    current = execute(['node', ROOT / 'tools/reference_current.cjs', ROOT / 'app/signal-lab-core.js'], work)
    comparison = pv.check_local(current, wolfram, contract)
    fields(comparison, {'metric_comparisons': 12,
                        'x6_case_statuses': {'inverted': 'FAIL', 'identity': 'PASS', 'zero': 'FAIL'}})
    reports['current-polarity'] = {'status': 'PASS_WITH_SCOPE_LIMITS',
                                  'comparison': comparison, 'full_result': current}
    for name in ('polarity-false-acceptance', 'polarity-lost-undefined', 'polarity-missing-bin'):
        bad = copy.deepcopy(current)
        cases = {c['label']: c['result'] for c in bad['cases']}
        if name == 'polarity-false-acceptance':
            cases['inverted']['status'] = 'PASS'
        elif name == 'polarity-lost-undefined':
            cases['zero']['metrics']['coherence_mean'] = {'status': 'OK', 'value': 1}
        else:
            cases['inverted']['spectrum']['referencePSD'].pop()
        controls.append(rejected(lambda: pv.check_local(bad, wolfram, contract), name))

    dependence = python('verify.py', packages['wolfram-dependence'])
    dependence.pop('python_version')
    fields(dependence, {'status': 'PASS_WITH_SCOPE_LIMITS', 'wolfram_checks_passed': 12,
                        'cross_engine_quantities_passed': 7, 'original_attempt_status': 'INCONCLUSIVE',
                        'amended_wolfram_attempt_status': 'PASS_NO_MESSAGES',
                        'package_manifest_verified': True, 'freeze_hashes_verified': True,
                        'wolfram_reexecuted_by_this_script': False})
    reports['wolfram-dependence'] = dependence
    causal = python('verify_release.py', packages['wolfram-causal3'])
    causal.pop('python_version')
    fields(causal, {'status': 'PASS_WITH_SCOPE_LIMITS', 'wolfram_checks_passed': 16,
                    'python_checks_passed': 16, 'characteristic_polynomials_compared': 6,
                    'permutation_rows_compared': 6, 'initial_kernel_status': 'FAIL_SIGN_CONVENTION',
                    'amended_kernel_status': 'PASS_NO_MESSAGES', 'package_manifest_verified': True,
                    'freeze_hashes_verified': True, 'preserved_sign_convention_failure_verified': True,
                    'wolfram_reexecuted_by_this_script': False})
    reports['wolfram-causal3'] = causal
    residuals = python(ROOT / 'research/lorentz_n6_residuals/verify.py', work)
    fields(residuals, {'status': 'PASS_WITH_SCOPE_LIMITS', 'primary_pairs_resolved': 4,
                       'primary_pairs_unresolved': 0, 'wolfram_polynomials_compared': 36,
                       'negative_controls_passed': 17, 'wolfram_reexecuted_by_this_script': False})
    reports['lorentz-residuals'] = residuals
    return reports, controls
