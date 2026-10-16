"""Complete archived-result comparison with exact decisions and bounded floats."""
import json
from pathlib import Path
import sys
from check import near
from proper_common import readz
from proper_core import require


def compare(a,b):
    for directory in [a,b]:
        require(not (directory/'INCONCLUSIVE.json').exists(),'no inconclusive archive')
        result=json.loads((directory/'RESULTS.json').read_text())
        require(result['status']=='PASS_COMPLETE_STUDY','successful complete archive')
    require(readz(a/'selection.json.gz')==readz(b/'selection.json.gz'),'exact matching reproduction')
    near(readz(a/'records.json.gz'),readz(b/'records.json.gz'),'all raw records features targets predictions')
    for name in ['models.json','summary.json','verification.json']:
        near(json.loads((a/name).read_text()),json.loads((b/name).read_text()),name)
    print('PASS: exact decisions and matching; all records and numerical outputs agree within atol=1e-10 rtol=1e-9')


if __name__=='__main__':
    compare(Path(sys.argv[1]),Path(sys.argv[2]))
