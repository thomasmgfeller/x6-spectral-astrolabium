"""Frozen no-optimization audit of confidence boxes and finite operator bounds.
SPDX-License-Identifier: Apache-2.0
"""
import platform,time
from fp_common import HERE,OLD,read,save,frozen,input_record,q_box,count_box,confidence_bound,F,outward
from fp_bound import Bound

def compute(index,pivots=None):
    c=read(HERE/'contract.json');p,obs,mask=input_record(index)
    counts=[obs['counts'][i] for i in mask];scale=F(str(p['scale']))
    box=q_box(counts,c['rho'],scale,c['chernoff_c'])
    previous=read(OLD/f'results/cloud-{index:02d}.json.gz')
    record=dict(index=index,intervals=len(mask),minimum_count=min(counts),
                mean_box=[[str(v) for v in count_box(n,c['chernoff_c'])] for n in counts],
                q_box=[[str(v) for v in pair] for pair in box],base_status=previous['base']['status'])
    if not previous['base'].get('qualified'):
        record['status']='BASE_HOLD';return record
    bound=Bound(p,mask,previous['base']['coordinates'],box,pivots=pivots)
    rows=[bound.evaluate(k) for k in c['dyadic_exponents']]
    record.update(status='COMPLETE',constants=bound.constants(),bounds=rows,
                  full_box_ten_percent=rows[0].get('ten_percent_certified',False),
                  first_local_ten_percent=next((r['k'] for r in rows if r.get('ten_percent_certified')),None))
    return record

def main():
    frozen();c=read(HERE/'contract.json');start=time.monotonic();records=[]
    for index in c['indices']:
        r=compute(index);save(HERE/f'results/cloud-{index:02d}.json.gz',r)
        row={k:r.get(k) for k in ['index','status','intervals','base_status','full_box_ten_percent','first_local_ten_percent']}
        if r['status']=='COMPLETE':row['full_box_contraction_upper']=r['bounds'][0]['contraction_upper']
        records.append(row);print(row,flush=True)
    total=sum(r['intervals'] for r in records);failure=confidence_bound(total,c['chernoff_c'])
    save(HERE/'summary.json',dict(status='COMPLETE',seconds=time.monotonic()-start,python=platform.python_version(),
        interval_total=total,family_failure_upper=outward(failure)[1],family_coverage_lower=outward(1-failure)[0],
        full_box_ten_percent=sum(bool(r.get('full_box_ten_percent')) for r in records),records=records,
        scope='Confidence coverage for fixed selected A intervals and independent ideal Poisson B, before B-dependent filtering. Local shrunk boxes have no coverage claim.'))

if __name__=='__main__':main()
