"""CI: immutable evidence, controls, published gates, algebra and two A/B replays.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib
import importlib.util
import math
import shutil
import tempfile
from pathlib import Path
from eb_common import HERE,read,encode,frozen

def compare_analysis(actual,expected,path='analysis'):
    """Exact structure/decisions; tolerate only last-bit float reductions.

    Archived bytes remain hash-verified above. This checks a fresh computation,
    whose reduction order can differ across CPUs/BLAS. No scientific gate or
    count may change, including when a float is close to a decision threshold.
    """
    assert type(actual) is type(expected),path
    if isinstance(expected,dict):
        assert actual.keys()==expected.keys(),path
        for key in expected:compare_analysis(actual[key],expected[key],path+'.'+key)
    elif isinstance(expected,list):
        assert len(actual)==len(expected),path
        for i,(a,b) in enumerate(zip(actual,expected)):compare_analysis(a,b,f'{path}[{i}]')
    elif isinstance(expected,float):
        assert math.isfinite(actual) and math.isfinite(expected),path
        assert math.isclose(actual,expected,rel_tol=1e-12,abs_tol=1e-12),(path,actual,expected)
    else:
        assert actual==expected,(path,actual,expected)

def comparison_controls():
    compare_analysis({'gate':False,'n':17,'metric':1.+1e-14},
                     {'gate':False,'n':17,'metric':1.})
    for actual,expected in [(True,False),(18,17),(17.,17),('PASS','HOLD'),
                            (1.+1e-8,1.),(float('nan'),1.),(float('inf'),1.),
                            ({'a':1},{'b':1}),([1],[1,2])]:
        try:compare_analysis(actual,expected)
        except AssertionError:continue
        raise AssertionError(('comparison accepted changed meaning',actual,expected))

def local_module(name):
    spec=importlib.util.spec_from_file_location('eligibility_audit_'+name,HERE/(name+'.py'))
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def main():
    comparison_controls()
    from replay_coordinates import controls as coordinate_controls
    coordinate_controls()
    frozen()
    for line in (HERE/'SHA256SUMS.txt').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
    controls=local_module('controls'); analyze=local_module('analyze'); verify=local_module('verify')
    reference={'status':'SELECTED','packet':{'scale':1.},'selection_counts':[17],
               'landmark_condition':20.,'design_condition':30.}
    verify.compare_legacy({**reference,'design_condition':30.+1e-13},reference)
    for change in [{'status':'HOLD'},{'selection_counts':[18]},
                   {'packet':{'scale':1.+1e-14}},
                   {'design_condition':30.+1e-8},
                   {'landmark_condition':float('nan')}]:
        try:verify.compare_legacy({**reference,**change},reference)
        except (AssertionError,ValueError):continue
        raise AssertionError(('legacy replay accepted changed meaning',change))
    with tempfile.TemporaryDirectory() as directory:
        temp=Path(directory); shutil.copy2(HERE/'contract.json',temp/'contract.json')
        controls.HERE=temp; controls.main()
        assert encode(read(temp/'controls.json'))==encode(read(HERE/'controls.json'))
        (temp/'results').symlink_to(HERE/'results',target_is_directory=True)
        analyze.HERE=temp; analyze.main()
        compare_analysis(read(temp/'analysis.json'),read(HERE/'analysis.json'))
    verify.main(write=False)
    print('CI PASS: technical reproducibility; scientific gate statuses unchanged.')

if __name__=='__main__':main()
