"""Exact density transfer in the affine, strictly increasing stationary control."""
from basis import INNER,FUTURE,ORDER,Q,force,scalar_coefficients

def run():
    # Constant unit clock increments. The weighted sum of lags is -1.
    lags=[b*k for k,b in enumerate((1,-9,16,-8),1)]
    assert sum(lags)==-1
    rows={j:[int(i==j) for i in FUTURE] for j in FUTURE}
    for i in reversed(INNER):
        k=ORDER.index(i);rows[i]=[-sum(c*rows[ORDER[k+t]][j] for t,c in enumerate(lags,1)) for j in range(4)]
        assert sum(rows[i])==1
    y={v:Q(i-5) for i,v in enumerate(ORDER)}
    for col in range(4):
        w={v:Q(rows[v][col]) if v in rows else Q(1,8) for v in ORDER}
        assert all(force(y,w)[i]==0 for i in INNER)
    assert all(scalar_coefficients(y)[i]==0 for i in INNER)
    gain={i:sum(map(abs,rows[i])) for i in INNER};worst=max(INNER,key=lambda i:gain[i]);threshold=Q(1,gain[worst]);s=[-1 if a>0 else 1 if a<0 else 0 for a in rows[worst]]
    def solution(eps):
        future=[Q(1,8)*(1+eps*v) for v in s]
        return [sum(a*b for a,b in zip(rows[i],future)) for i in INNER]
    marginal=solution(threshold); doubled=solution(2*threshold)
    assert min(marginal)==0 and min(doubled)<0 and min(solution(threshold/2))>0
    return {'rows_by_inner':{str(i):rows[i] for i in INNER},'future_order':FUTURE,'relative_linf_gain':gain,'critical_site':worst,'strict_positivity_radius_supremum':threshold,'worst_sign_pattern':s,'inner_at_threshold':marginal,'inner_at_twice_threshold':doubled}
if __name__=='__main__':
    import json
    print(json.dumps(run(),default=str,indent=2,sort_keys=True))
