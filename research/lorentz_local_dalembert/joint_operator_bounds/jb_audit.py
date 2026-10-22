"""Independent extremizer and attribution audit. SPDX-License-Identifier: Apache-2.0"""
from jb_run import *
def audit():
    cases=0
    # Exhaustive rational-grid feasibility checks exercise capped and unclamped
    # positive/negative branches. Numerical objective comparison is only sanity;
    # the derivative proof and directed arithmetic carry the bound.
    for lx,ux in [(F(0),F(8)),(F(5),F(8)),(F(1),F(3))]:
      for ly,uy in [(F(0),F(8)),(F(1),F(2)),(F(4),F(6))]:
       for d in [F(-4),F(-2),F(0),F(2),F(4)]:
        if max(lx,ly-d)>ux:continue
        x,y=maximizing_pair(lx,ux,ly,uy,d);opt=float(y)**(2/3)-float(x)**(2/3)
        for k in range(41):
         xx=lx+(ux-lx)*F(k,40)
         for h in range(41):
          yy=ly+(uy-ly)*F(h,40)
          if yy-xx<=d:assert float(yy)**(2/3)-float(xx)**(2/3)<=opt+1e-12
        cases+=1
    records=[read(HERE/f'results/cloud-{i:02d}.json.gz') for i in read(HERE/'contract.json')['indices']]
    valid=[r for r in records if r['status']=='COMPLETE']
    ratios=[F(r['contraction_ratio_vs_box_transport'][1]) for r in valid]
    old=[F(r['contraction_ratio_vs_old_symmetric'][1]) for r in valid]
    gammas=[F(r['combined']['contraction_upper']) for r in valid]
    assert all(v<=1 for v in ratios+old)
    return dict(status='PASS',extremizer_grid_cases=cases,record_count=len(records),computable_cases=len(valid),
      joint_improvement_cases=sum(v<1 for v in ratios),
      ratio_vs_box_transport_range=[min(r['contraction_ratio_vs_box_transport'][0] for r in valid),outward(max(ratios))[1]],
      ratio_vs_old_symmetric_range=[min(r['contraction_ratio_vs_old_symmetric'][0] for r in valid),outward(max(old))[1]],
      contraction_upper_range=[outward(min(gammas))[0],outward(max(gammas))[1]],
      ten_percent_certificates=sum(r['combined'].get('ten_percent_certified',False) for r in valid))
if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
