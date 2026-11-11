from pathlib import Path
import json
from boundary import evidence

ROOT=Path(__file__).resolve().parent
def render(): return json.dumps(evidence(),indent=2,ensure_ascii=False,sort_keys=True)+'\n'
if __name__=='__main__':
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/gram_matrices.json').write_text(render(),encoding='utf-8')
