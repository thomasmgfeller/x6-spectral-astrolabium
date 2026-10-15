#!/usr/bin/env python3
"""Replay the frozen Wolfram evidence locally, without Wolfram or network."""
import argparse
import copy
import hashlib
import importlib.util
from itertools import permutations
import json
from pathlib import Path
import re
import sys

from core import (require, selected, features, grouping, degree_pairs, height_two_seven,
                  validate_order, polynomial, multiply, add, transpose)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CHECKS = {'strict_transitive_inputs', 'K_normalization',
          'all_primary_same_F0_nonisomorphic_separated_D_and_W_future',
          'n7_future_only_collision_separated_by_past',
          'n8_D_and_both_moments_fail_connected_duals', 'reverse_label_invariance'}


def encode(obj):
    return (json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()


def decode(data):
    def pairs(items):
        result = {}
        for k, v in items:
            require(k not in result, 'Duplicate JSON key: '+k)
            result[k] = v
        return result
    def bad(x):
        raise ValueError('Nonfinite JSON: '+x)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=bad)


def read(path):
    return decode(Path(path).read_bytes())


def same(a, b, label):
    require(encode(a) == encode(b), label)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def parse_receipt(raw):
    same(set(raw) <= {'content', 'isError'}, True, 'Unexpected receipt fields')
    require(raw.get('isError') is False and len(raw['content']) == 1, 'Incomplete or failed receipt')
    block = raw['content'][0]
    require(block['type'] == 'text', 'Text receipt required')
    match = re.fullmatch(r'Out\[\d+\]= (".*")', block['text'], re.DOTALL)
    require(match is not None, 'Unexpected Wolfram output or messages')
    return decode(decode(match.group(1)))


def check_wolfram(doc, inputs, expected=None):
    expected = selected(inputs) if expected is None else expected
    same(set(doc) == {'schema','wolfram_version','inputs_sha256','sha256_abc','records','pairs','checks'},
         True, 'Wolfram result fields')
    require(doc['schema'] == 'x6.lorentz-wolfram/1', 'Wolfram schema')
    require(isinstance(doc['wolfram_version'], str) and doc['wolfram_version'], 'Missing kernel version')
    require(doc['inputs_sha256'] == digest(HERE/'inputs.json'), 'Wolfram input hash')
    require(doc['sha256_abc'] == hashlib.sha256(b'abc').hexdigest(), 'Hash convention')
    same(doc['records'], expected['records'], 'Exact record replay differs')
    same(doc['pairs'], expected['pairs'], 'Exact pair replay differs')
    same(doc['checks'], dict.fromkeys(CHECKS, True), 'Missing or failed Wolfram check')


def reject(action, label):
    try:
        action()
    except (ValueError, KeyError, TypeError):
        return {'case': label, 'rejected': True}
    raise ValueError('Invalid case accepted: '+label)


def negative_controls(doc, inputs, expected):
    controls = []
    def mutated(label, change):
        bad = copy.deepcopy(doc); change(bad)
        controls.append(reject(lambda: check_wolfram(bad, inputs, expected), label))
    mutated('missing-record', lambda d: d['records'].pop('n6-0073'))
    mutated('missing-primary-pair', lambda d: d['pairs'].pop(0))
    mutated('changed-W-future', lambda d: d['records']['n6-0073'].__setitem__('W_future',2))
    mutated('changed-K-normalization', lambda d: d['records']['n6-0073']['polynomials_S_A_K'][2].__setitem__(2,-17))
    mutated('lost-degree-multiplicity', lambda d: d['records']['n6-0073']['degree_pairs'].pop())
    mutated('false-duality', lambda d: d['pairs'][0].__setitem__('dual_isomorphic',True))
    mutated('hidden-n8-counterexample', lambda d: d['pairs'][5].__setitem__('isomorphic',True))
    mutated('missing-boolean-check', lambda d: d['checks'].pop('K_normalization'))
    mutated('integer-instead-of-boolean', lambda d: d['checks'].__setitem__('K_normalization',1))
    mutated('wrong-input-hash', lambda d: d.__setitem__('inputs_sha256','0'*64))
    controls.append(reject(lambda: decode('{"x":1,"x":2}'), 'duplicate-json-key'))
    controls.append(reject(lambda: validate_order([[0,1,0],[0,0,1],[0,0,0]]), 'hasse-chain-without-transitive-edge'))
    duplicate = copy.deepcopy(inputs); duplicate['records'].append(duplicate['records'][0])
    controls.append(reject(lambda: selected(duplicate), 'duplicate-case-id'))
    # Even a replacement receipt and matching parsed result cannot bypass mathematical replay.
    bad = copy.deepcopy(doc); bad['records']['n6-0073']['W_future'] = 999
    receipt = {'isError':False, 'content':[{'type':'text', 'text':'Out[1]= '+json.dumps(json.dumps(bad))}]}
    controls.append(reject(lambda: check_wolfram(parse_receipt(receipt), inputs, expected),
                           'consistent-replacement-receipt-with-false-math'))
    # Height-two K spectra are +/- symmetric: a sign mistake would be invisible there.
    # This transitive height-three control has an asymmetric K polynomial.
    c = [[0,1,1,1],[0,0,1,1],[0,0,0,0],[0,0,0,0]]
    validate_order(c)
    s, a = add(c,transpose(c)), add(c,transpose(c),-1)
    k = add(multiply(s,a),multiply(a,s),-1)
    require(polynomial(k) != polynomial([[-x for x in row] for row in k]), 'K sign control ineffective')
    controls.append(reject(lambda: same(polynomial(k), polynomial([[-x for x in row] for row in k]),
                                       'K sign reversed'), 'K-sign-on-height-three-control'))
    return controls


def compute():
    freeze = read(HERE/'freeze.json')
    require(set(freeze['files']) == {'inputs.json','contract.json','wolfram_check.wl'}, 'Freeze coverage')
    for name, sha in freeze['files'].items():
        require(digest(HERE/name) == sha, 'Frozen source changed: '+name)
    amendment = read(HERE/'freeze-compact.json')
    require(amendment['original_freeze_sha256'] == digest(HERE/'freeze.json'), 'Original freeze changed')
    require(set(amendment['files']) == {'inputs.json','contract.json','wolfram_check_compact.wl',
                                 'evidence/wolfram-response-attempt1.json'}, 'Amendment coverage')
    for name, sha in amendment['files'].items():
        require(digest(HERE/name) == sha, 'Amended source changed: '+name)
    original = (HERE/'wolfram_check.wl').read_text()
    same((HERE/'wolfram_check_compact.wl').read_text(),
         original.replace('"RawJSON"]\n', '"RawJSON", "Compact" -> True]\n'), 'Amendment exceeds formatting')
    first = read(HERE/'evidence/wolfram-response-attempt1.json')
    first_control = reject(lambda: parse_receipt(first), 'truncated-original-receipt')
    monic = read(HERE/'freeze-monic.json')
    require(monic['previous_freeze_sha256'] == digest(HERE/'freeze-compact.json'), 'Compact freeze changed')
    require(set(monic['files']) == {'inputs.json','contract.json','wolfram_check_monic.wl',
                                  'evidence/wolfram-response-attempt2.json',
                                  'evidence/wolfram-result-attempt2.json'}, 'Monic amendment coverage')
    for name, sha in monic['files'].items():
        require(digest(HERE/name) == sha, 'Monic source changed: '+name)
    same((HERE/'wolfram_check_monic.wl').read_text(),
         (HERE/'wolfram_check_compact.wl').read_text().replace('CharacteristicPolynomial[#, t]',
          '(-1)^n CharacteristicPolynomial[#, t]'), 'Monic amendment exceeds sign convention')
    inputs = read(HERE/'inputs.json'); contract = read(HERE/'contract.json')
    require(inputs['schema'] == 'x6.lorentz-residual-inputs/1', 'Input schema')
    require(len(inputs['records']) == 12 and len(inputs['primary_pairs']) == 4 and len(inputs['scope_pairs']) == 2,
            'Input coverage')
    atlas_path = ROOT/contract['source_atlas']['path']
    require(digest(atlas_path) == contract['source_atlas']['sha256'], 'Atlas provenance')
    atlas = read(atlas_path)
    spec = importlib.util.spec_from_file_location('original_n6_verifier', atlas_path.with_name('verify.py'))
    verifier = importlib.util.module_from_spec(spec); spec.loader.exec_module(verifier)
    atlas_verification = verifier.verify(atlas)
    records = {r['id']: features(r['causal_matrix']) for r in atlas['records']}
    require(len(records) == 318, 'Atlas coverage')
    for row in atlas['records']:
        same(records[row['id']]['polynomials_S_A_K'], row['polynomials_S_A_K'], 'Independent atlas polynomial')
    groups = {mode: grouping(records, mode) for mode in ('F0','D_only','F0_D','F0_W_future','F0_W_both')}
    same(groups['F0']['collision_groups'], sorted(inputs['primary_pairs']), 'Primary pairs are not exactly the atlas residuals')
    same([groups[m]['classes'] for m in groups], [314,311,318,318,318], 'Unexpected atlas grouping')
    atlas_matrices = {r['id']: r['causal_matrix'] for r in atlas['records']}
    relabel_count = 0
    for row in inputs['records']:
        if row['role'] == 'PRIMARY_N6':
            c = row['causal_matrix']
            same(c, atlas_matrices[row['id']], 'Primary matrix differs from atlas')
            d = sorted(degree_pairs(c))
            for p in permutations(range(6)):
                relabeled = [[c[i][j] for j in p] for i in p]
                same(sorted(degree_pairs(relabeled)), d, 'Relabeling changed D')
                relabel_count += 1
    require(relabel_count == 5760, 'Primary relabeling coverage')
    expected = selected(inputs)
    second = read(HERE/'evidence/wolfram-result-attempt2.json')
    same(parse_receipt(read(HERE/'evidence/wolfram-response-attempt2.json')), second, 'Second receipt differs')
    second_control = reject(lambda: check_wolfram(second, inputs, expected), 'nonmonic-odd-dimension-attempt')
    corrected = copy.deepcopy(second)
    for record in corrected['records'].values():
        if record['n'] % 2:
            record['polynomials_S_A_K'] = [[-x for x in poly] for poly in record['polynomials_S_A_K']]
    check_wolfram(corrected, inputs, expected)
    raw = read(HERE/'evidence/wolfram-response-attempt3.json')
    wolfram = read(HERE/'evidence/wolfram-result.json')
    same(parse_receipt(raw), wolfram, 'Stored result differs from full receipt')
    check_wolfram(wolfram, inputs, expected)
    h2 = height_two_seven()
    require(h2['orders'] == 164, 'Height-two enumeration count')
    same([h2['groups'][m]['classes'] for m in h2['groups']], [158,163,164,164], 'Height-two grouping')
    controls = [first_control, second_control] + negative_controls(wolfram, inputs, expected)
    return {'schema':'x6.lorentz-residual-report/1','status':'PASS_WITH_SCOPE_LIMITS',
            'primary_pairs_resolved':4, 'primary_pairs_unresolved':0,
            'wolfram_polynomials_compared':36, 'wolfram_boolean_checks':6,
            'wolfram_reexecuted_by_this_script':False,
            'wolfram_version':wolfram['wolfram_version'],
            'first_attempt_status':'REJECTED_TRUNCATED_OUTPUT',
            'second_attempt_status':'REJECTED_NONMONIC_ODD_DIMENSION_POLYNOMIALS',
            'third_attempt_status':'COMPLETE_EXACT_AGREEMENT',
            'atlas_verification':atlas_verification, 'n6_groups':groups,
            'primary_degree_relabelings':relabel_count,
            'selected':expected, 'n7_height_at_most_two':h2,
            'hypothesis':contract['hypothesis'], 'negative_controls':controls,
            'negative_controls_passed':len(controls),
            'scope':'FINITE_EXACT_CHECKS; N7_HEIGHT_GE_3_OPEN; NO_PHYSICAL_VALIDATION; NO_EXTERNAL_REVIEW'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--verify-report', type=Path, help='Additionally reject any modified or incomplete supplied report')
    args = parser.parse_args()
    try:
        report = compute()
        same(report, read(HERE/'evidence/local-results.json'), 'Committed report differs from complete replay')
        if args.verify_report:
            same(report, read(args.verify_report), 'Supplied report differs from complete replay')
        if args.output:
            args.output.write_bytes(encode(report))
        print(encode(report).decode(), end='')
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('FAIL: '+str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
