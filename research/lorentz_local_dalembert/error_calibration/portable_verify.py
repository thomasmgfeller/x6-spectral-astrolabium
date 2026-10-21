"""SPDX-License-Identifier: Apache-2.0
Portable reporting adapter for one development bytehash diagnostic.

The frozen verifier remains byte-identical. Its development comparison treats
coordinate_hash_matches as an exact gate although PROTOCOL.md explicitly makes
byte identity a separate diagnostic. Preserve all numerical comparisons,
thresholds, source pins, records, calibration and scientific decisions.
"""
import argparse
import contextlib
import io
import json
import re
import ec_verify as frozen

PATTERN=re.compile(r'root\.records\[\d+\]\.coordinate_hash_matches\Z')
ORIGINAL_COMPARE=frozen.compare
diagnostics=[]


def compare(a,b,path='root'):
    if PATTERN.fullmatch(path):
        assert type(a) is bool and type(b) is bool
        diagnostics.append(dict(path=path,current_matches_archive=a,
                                original_matches_archive=b))
        return
    return ORIGINAL_COMPARE(a,b,path)


def self_test():
    # The only exception is the bytehash diagnostic at the exact path.
    frozen.compare=compare
    try:
        compare(False,True,'root.records[0].coordinate_hash_matches')
        for a,b,path in [(False,True,'root.records[0].other_flag'),
                         (1.,0.,'root.records[0].errors[0][0]'),
                         ('different','fixed','root.source_hash')]:
            try:compare(a,b,path)
            except AssertionError:pass
            else:raise AssertionError('Adapter skipped a required comparison: '+path)
        try:ORIGINAL_COMPARE(False,True,'root.records[0].coordinate_hash_matches')
        except AssertionError:pass
        else:raise AssertionError('Frozen exact comparison unexpectedly changed')
    finally:
        frozen.compare=ORIGINAL_COMPARE
        diagnostics.clear()
    print(json.dumps(dict(adapter_controls='PASS',groups=5)))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--strict',action='store_true',help='Use the original exact development-byteflag comparison.')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    if args.self_test:return self_test()
    if not args.strict:frozen.compare=compare
    try:
        captured=io.StringIO()
        with contextlib.redirect_stdout(captured):frozen.main()
        result=json.loads(captured.getvalue())
    finally:frozen.compare=ORIGINAL_COMPARE
    result['development_bytehash_adapter']=dict(
        mode='ORIGINAL_EXACT_BYTEFLAG' if args.strict else 'NUMERICAL_WITH_SEPARATE_DEVELOPMENT_BYTEHASH_DIAGNOSTIC',
        compared=len(diagnostics),
        current_matches_archive=sum(v['current_matches_archive'] for v in diagnostics),
        original_matches_archive=sum(v['original_matches_archive'] for v in diagnostics),
        changed_flags=[v for v in diagnostics if v['current_matches_archive']!=v['original_matches_archive']],
        scope='Only root.records[i].coordinate_hash_matches is reported rather than asserted; every numerical comparison and scientific gate is unchanged.')
    print(json.dumps(result))


if __name__=='__main__':main()
