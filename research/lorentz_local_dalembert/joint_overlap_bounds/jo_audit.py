"""Independent projection diagnostics; SPDX-License-Identifier: Apache-2.0"""
from jo_run import *
def audit():
    pairs=nest=known=0;ratios=[];rows=[]
    for i in read(HERE/'contract.json')['indices']:
        r=read(HERE/f'results/cloud-{i:02d}.json.gz');p,o,mask=input_record(i)
        raw=[count_box(o['counts'][j],12) for j in mask];D=r['difference_upper_microcounts'];n=0
        for a in range(len(mask)):
            for b in range(a+1,len(mask)):
                old=raw[a][1]-raw[a][0]+raw[b][1]-raw[b][0]
                new=F(D[a+1][b+1]+D[b+1][a+1],UNIT)
                assert new>=0
                if new<old:n+=1;ratios.append(new/old)
        pairs+=n;nest+=r['nesting_pairs'];known+=r['known_intersections']
        rows.append(dict(index=i,narrower_pair_difference_ranges=n))
    # Exact normalized quadratic-field identity: Box(1/2 u^T H u)=tr(eta H).
    H=[F(1,2),F(-1,3),F(1,4)]
    response=-H[0]+H[1]+H[2]
    assert response==F(-7,12) and max(map(abs,H))<=1
    return dict(status='PASS',narrower_pair_difference_ranges=pairs,
        smallest_width_ratio=outward(min(ratios)),nesting_pairs=nest,
        known_intersection_pairs=known,records=rows,
        normalized_quadratic_control=str(response),
        scope='Difference-range projections of a necessary relaxation; no full geometric realization or operator accuracy claim.')
if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
