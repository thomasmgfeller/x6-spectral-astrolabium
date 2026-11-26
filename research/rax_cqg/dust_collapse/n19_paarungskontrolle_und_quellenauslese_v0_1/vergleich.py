"""Lock off-target predictions, then compare against independently constructed arms."""
import json
from hashlib import sha256
from fractions import Fraction as F
from leser import PROBES,old_clocks,read
from proben import samples,causal_sites


def run(previous,early):
    from gemischt import COEFF,ORDER,WINDOWS
    from quelle import hull,SCALE
    from felder import pulses
    fixtures,construction=samples(previous,early)
    locks=[]
    memory={}
    for name,y,w in fixtures:
        old=old_clocks({i:y[i] for i in (0,1,2,3)},COEFF,ORDER)
        pred=read(old,{i:w[i] for i in PROBES},y[15],y[17],COEFF,ORDER,WINDOWS)
        memory[name]=pred
        locks.append({'case':name,'K0':pred['K0'].data(),'tag_T':pred['arms'][0]['delta'].data(),
                      'W':pred['W'].data(),'M':pred['M'].data(),'P':pred['P'].data(),
                      'signed_prediction':[a['delta'].data() for a in pred['arms']]})
    frozen=sha256(json.dumps(locks,sort_keys=True).encode()).hexdigest()
    observed={}
    local=[]
    for name,y,w in fixtures:
        pred=memory[name]
        for key,i in [('s',16),('t',18)]:
            assert (pred[key]-y[i]).contains_zero()
        assert (pred['K0']-w[16]*(y[16]-y[15])).contains_zero()
        arms=pulses(y,w)
        for (actual,yy,ww),guess in zip(arms,pred['arms']):
            assert (guess['delta']-actual).contains_zero()
            assert (guess['absolute']-ww[16]*(yy[16]-yy[15])).contains_zero()
            assert (guess['wz']-ww[16]).contains_zero() and (guess['wr']-ww[18]).contains_zero()
            assert all((yy[i]-y[i]).contains_zero() for i in (15,17))
        observed[name]=[a[0] for a in arms]
        if name.startswith('local_'):
            local.append((name,arms))
    oldQ=json.loads((previous/'Fenster.json').read_bytes())['positive_weight_reversal']['Q']
    low,high=map(F,oldQ)
    comparisons=[]
    for npos,pos in observed.items():
        for nneg,neg in observed.items():
            raw=-pos[1]/neg[0]
            corrected=raw*memory[nneg]['arms'][0]['delta']/memory[npos]['arms'][0]['delta']
            native=-pos[1]/pos[0]
            assert (corrected-native).contains_zero()
            assert low*SCALE<=corrected.lo<=corrected.hi<=high*SCALE
            comparisons.append({'positive':npos,'negative':nneg,'raw':raw.data(),'corrected':corrected.data(),
                                'raw_outside':raw.lo>high*SCALE or raw.hi<low*SCALE})
    (la,arms_a),(lb,arms_b)=local
    assert len(local)==2
    past=sorted({18}|{i for i,j in ORDER if j==18})
    assert past==[0,1,2,15,16,17,18]
    risk=[]
    for (a,ya,wa),(b,yb,wb) in zip(arms_a,arms_b):
        assert all((ya[i]-yb[i]).contains_zero() for i in past)
        assert all((wa[i]-wb[i]).contains_zero() for i in past if i!=16)
        assert not (wa[16]-wb[16]).contains_zero()
        a,b=(a,b) if a.lo>0 else (-a,-b)
        assert 0<a.lo<=a.hi<b.lo
        risk.append(str(F(b.lo-a.hi,b.lo+a.hi)))
    return {'off_target_predictions':locks,'prediction_hash':frozen,'sites':causal_sites(ORDER),
            'comparisons':comparisons,'raw_outside_count':sum(c['raw_outside'] for c in comparisons),
            'local_pair':{'construction':construction,'receiver_cone':past,'hidden_weight':16,
                          'relative_risk_lower_bound':risk}}


if __name__=='__main__':
    from vorgaenger import inputs
    with inputs() as args:
        print(json.dumps(run(*args),indent=2,sort_keys=True))
