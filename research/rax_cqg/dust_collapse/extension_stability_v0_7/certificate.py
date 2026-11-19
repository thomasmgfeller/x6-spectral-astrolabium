"""Apply the original two-grid inequalities to the 169+23 reachable study states."""
from fractions import Fraction as F
import json
from unittest.mock import patch
from matrices import ROOT, CACHE, names_and_reach, write
import exact
import positive

def calculate():
    new=json.loads((ROOT/'clocks.json').read_text())
    def inputs(name):
        d=json.loads((CACHE/'study'/name).read_text())
        return {**d,**new} if name=='direct.json' else d
    # The q vectors, thresholds, counterexample, clock radii and all inequalities
    # are unchanged. Only the Gram table, the reachable vertices and direct clocks grow.
    with patch.object(positive,'HERE',ROOT):
        residuals=positive.verify()
    with patch.object(exact,'jsonread',inputs),patch.object(exact,'setup',names_and_reach),patch.object(exact,'HERE',ROOT):
        out={}
        for tag in ('coarse','fine'):
            out[tag]={}
            for T in (F(1,20),F(5021,100000)):
                row=exact.verify(tag,T)
                # These two legacy counters predate N15; report scope explicitly.
                row.pop('evaluated_N14');row.pop('abs_bounded_N14')
                out[tag][str(T)]=row
    return {'grids':out,'positive_congruence_residuals':residuals,
            'N14_direct':34,'N14_bounded':105,'N15_direct':len(new)}
if __name__=='__main__':
    if not __debug__:raise RuntimeError('Run without -O')
    data=calculate();write('certificate.json',data)
