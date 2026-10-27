"""Exploratory diagnostics on archived v0.3 data; not fresh validation."""
from pathlib import Path
import json,sys
import numpy as np
import refined

ROOT=Path(__file__).resolve().parent


def components(y):
    captured={}
    def profile(frame,event,arg):
        if event=='return' and frame.f_code is refined.previous.evaluate.__code__:
            captured.update({k:frame.f_locals[k] for k in ['first','H','eps','q'] if k in frame.f_locals})
    sys.setprofile(profile)
    try:result=refined.previous.evaluate(y)
    finally:sys.setprofile(None)
    return result,captured


def main():
    data=np.load(ROOT.parent/'joint_region_v0_3/fresh_counts.npz')
    gs=json.loads((ROOT.parent/'poisson_v0_2/geometries.json').read_text())
    records=[];retained=0;comparisons=0
    for gi,g in enumerate(gs):
        row=20+gi;count=0;oldcount=int(data['metrics'][row,:,5].sum())
        for rep,y in enumerate(data['cells'][row]):
            old=refined.previous.evaluate(y);new=refined.evaluate(y)
            count+=int(new['certified'])
            if 'error_bound' in old:
                assert new['error_bound']<=old['error_bound']*(1+1e-10)
                comparisons+=1
            if old['certified']:
                assert new['certified'];retained+=1
        old,c=components(data['cells'][row,0]);new=refined.evaluate(data['cells'][row,0])
        records.append({'geometry':g['id'],'family':g['family'],'old_validated_certificates':oldcount,
                        'new_float_candidates':count,'replicates':128,
                        'first_old_observation':{'old_first_relative_bound':c['first']/c['q'],
                          'old_nonlinear_relative_bound':c['H']**2/(1-c['eps'])/c['q'],
                          'old_epsilon':c['eps'],'new_relative_bound':new['error_bound']/new['qhat']}})
    result={'scope':'Exploratory v0.3 high-density development set; new float candidates are not validated certificates.',
            'old_certificates_retained_as_candidates':retained,'nonweakening_comparisons':comparisons,
            'new_float_candidates':sum(r['new_float_candidates'] for r in records),'records':records}
    (ROOT/'DEVELOPMENT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'}))


if __name__=='__main__':main()
