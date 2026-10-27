"""Exploratory screening on the published v0.4 observations."""
from pathlib import Path
import json
import numpy as np
import constrained as c

ROOT=Path(__file__).resolve().parent


def main():
    data=np.load(ROOT.parent/'refined_bound_v0_4/fresh_counts.npz')
    old=json.loads((ROOT.parent/'refined_bound_v0_4/RESULTS.json').read_text())
    rows=[]
    for row,record in enumerate(old['records']):
        candidates=selected=0
        for rep,y in enumerate(data['cells'][row]):
            r=c.evaluate(y)
            candidates+=r['certified'];selected+=r['certified'] or bool(data['metrics'][row,rep,5])
        rows.append({'level':record['level'],'geometry':record['geometry'],'replicates':64,
                     'geometric_float_candidates':int(candidates),'selected_float_candidates':int(selected),
                     'v04_validated_certificates':record['new_validated_certificates']})
    result={'scope':'Archived v0.4 development data; candidate counts are not validated new certificates or fresh validation.',
            'records':rows}
    (ROOT/'DEVELOPMENT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{ 'level':l,'geometric_candidates':sum(x['geometric_float_candidates'] for x in rows if x['level']==l),
                       'selected_candidates':sum(x['selected_float_candidates'] for x in rows if x['level']==l)} for l in range(3)]))


if __name__=='__main__':main()
