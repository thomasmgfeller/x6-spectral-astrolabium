"""Descriptive post-freeze failure localization; never modifies gates or data.
SPDX-License-Identifier: Apache-2.0
"""
from collections import Counter
import json
import numpy as np
from eb_common import HERE,read,save

def main():
    failures=[]; mismatches=Counter(); changed=[]; maximum_pool=0; maximum_eligible=0; total=Counter()
    for path in sorted((HERE/'results').glob('cloud-*.json.gz')):
        r=read(path); s=r['selection']; new=s['arms']['candidate']; old=s['arms']['legacy']
        inventory=new.get('inventory',[]); total.update(v['status'] for v in inventory)
        sides={side:sum(v['side']==side and v['status']=='COUNT_ELIGIBLE' for v in inventory) for side in ['past','future']}
        maximum_eligible=max(maximum_eligible,*sides.values()); maximum_pool=max(maximum_pool,len(inventory))
        if new['status']!='SELECTED':
            failures.append(dict(index=r['index'],status=new['status'],funnel=new.get('funnel'),eligible_by_side=sides))
        if old['status']=='SELECTED' and new['packet']['landmarks']!=old['packet']['landmarks']:changed.append(r['index'])
        if r['replicates']:
            f=r['replicates'][0]['arms']['candidate']['measurement']['four']
            if f['status']=='WEIGHTS_VALID':
                z=np.array(f['coordinates']); d=z[None]-z[:,None]
                order=(d[:,:,0]>0)&(d[:,:,0]**2>d[:,:,1]**2+d[:,:,2]**2)
                observed=np.array(new['packet']['full_order'],bool)
                for i,j in zip(*np.nonzero(np.triu((order!=observed)|(order.T!=observed.T),1))):
                    def kind(k):return 'landmark' if k<4 else 'root' if k==4 else 'support'
                    mismatches['-'.join(sorted([kind(i),kind(j)]))]+=1
    out=dict(status='POSTHOC_DIAGNOSTIC',failed_selections=failures,inventory_status_counts=dict(total),
        maximum_count_eligible_per_side=maximum_eligible,geometry_cap_per_side=128,
        all_count_eligible_evaluated=maximum_eligible<=128,maximum_pool_size=maximum_pool,
        changed_landmarks_on_common_A=changed,primary_undirected_order_mismatches_by_endpoint=dict(mismatches),
        scope='Descriptive audit after frozen gates; no new thresholds, reclassification or reselection. Exhaustion is limited to the fixed root/support/first-three-landmark common cones.')
    if (HERE/'failure-diagnosis.json').exists():assert out==read(HERE/'failure-diagnosis.json')
    else:save(HERE/'failure-diagnosis.json',out)
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
