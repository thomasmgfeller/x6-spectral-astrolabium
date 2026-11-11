import json
from calculus import ROOT
from states import evidence
if __name__=='__main__':
 result=evidence();(ROOT/'results/states.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 print('Exact invariant state family, rank',result['rank'])
