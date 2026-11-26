"""Paired native source runs with a fixed far boundary or a fixed causal prefix."""
from fractions import Fraction as F
import json


def run(early):
    from algebra import box, hull, mid
    from gemischt import Action, N, CLOCK, WEIGHT, COEFF, ORDER, WINDOWS, certify, propose, validate_state
    from quelle import SCALE
    import rand                             # Pinned unforced-receiver construction.
    from basisdaten import box as old_box, hull as old_hull

    z,r,u = 16,18,15
    fixed = Action(False)
    centre = json.loads((early/'Randpraeparation.json').read_bytes())['reference']
    nominal = list(map(F,centre['solution_centres']))
    radius = F(centre['radius'])
    start = list(map(mid,nominal))
    ref_domain = [hull(v-radius,v+radius) for v in nominal]
    y,w = fixed.fields(ref_domain)
    old_y = {i:old_hull(*v.data()) for i,v in y.items()}
    old_w = {i:old_hull(*v.data()) for i,v in w.items()}
    axis = len(CLOCK)+WEIGHT.index(z)

    class Source:
        def __init__(self,strength):
            self.strength = strength
            self.fields = fixed.fields

        def evaluate(self,x,targets):
            gradient,H = fixed.evaluate(x)
            val = box(self.strength) if hasattr(x[0],'lo') else mid(self.strength)
            gradient[axis] -= val
            return gradient,H

    def residuals(yy,ww,strength):
        G = {i:box(0) for i in y}
        D = {i:box(19) for i in y}
        for (i,j),c in COEFF.items():
            gap = yy[j]-yy[i]
            flow = c*ww[j]*gap
            G[i] += flow
            G[j] -= flow
            D[j] += c*gap*gap
        residuals = [G[i] for i in CLOCK]+[D[i]-(strength if i==z else 0) for i in WEIGHT]
        assert all(v.contains_zero() for v in residuals)
        return G,D

    def predicted(uu,strength):
        return (uu*uu-6-strength)/(2*(uu+3))

    assert (predicted(y[u],0)-y[z]).contains_zero()
    assert (y[u]+3).lo>0
    result = []
    for strength in (F(0),F(-1,10**6),F(1,10**6)):
        expected_delta = -box(strength)/(2*(y[u]+3))
        model = Source(strength)
        proposal = propose(model,start)
        domain,proof = certify(model,proposal,(0,0),F(1,10**21))
        validate_state(model,domain)
        yy,ww = model.fields(domain)
        residuals(yy,ww,strength)
        at_fixed = {i:yy[i]-y[i] for i in (0,1,2,u,z,r)}
        assert (predicted(yy[u],strength)-yy[z]).contains_zero()
        if strength:
            assert not at_fixed[u].contains_zero()
            assert not (at_fixed[z]-expected_delta).contains_zero()

        fields = {}
        yy2,ww2 = y.copy(),w.copy()
        if strength:
            control = rand.finite(old_y,old_w,COEFF,old_box(F(1,6)),WINDOWS,strength,False)
            for key,values in control['future_and_endpoints'].items():
                i = int(key)
                fields[i] = {name:hull(*v) for name,v in values.items()}
                yy2[i] += fields[i]['dY']
                ww2[i] += fields[i]['dw']
        assert all(i==z or (z,i) in ORDER for i in fields)
        residuals(yy2,ww2,strength)
        for i in y:
            if w[i].hi:
                assert 0<ww2[i].lo<=ww2[i].hi<SCALE
            else:
                assert ww2[i].lo==ww2[i].hi==0
        assert all(yy2[j].lo>yy2[i].hi for i,j in ORDER)
        x = {i:(v+F(11,6))/F(23,6) for i,v in yy2.items()}
        for (lo,hi),mark in zip(WINDOWS,(z,r)):
            matches = [i for i,t in x.items() if ww2[i].hi>0 and t.hi>=lo*SCALE and t.lo<=hi*SCALE]
            assert matches == [mark] and lo*SCALE<x[mark].lo<=x[mark].hi<hi*SCALE
        d = {i:yy2[i]-y[i] for i in (u,z,r)}
        assert (d[z]-expected_delta).contains_zero()
        flux0 = w[z]*(y[z]-y[u])
        flux1 = ww2[z]*(yy2[z]-yy2[u])
        dflux = flux1-flux0
        exterior = sum((c*(ww2[j]*(yy2[j]-yy2[u])-w[j]*(y[j]-y[u]))
                        for (i,j),c in COEFF.items() if i==u and j!=z and c),box(0))
        assert (dflux+exterior).contains_zero()
        if strength:
            assert not dflux.contains_zero() and not d[r].contains_zero()
            assert any(not fields[j]['dw'].contains_zero() or not fields[j]['dY'].contains_zero()
                       for j in (7,8,9,10))
        result.append({'Jw':str(strength),'predicted_dY16_fixed_prefix':expected_delta.data(),
                       'fixed_collars':{'proof':proof,'dY':{str(i):v.data() for i,v in at_fixed.items()},
                                        'source_free_receiver':True},
                       'fixed_prefix':{'dY15_exact':'0','dY16':d[z].data(),'dY18':d[r].data(),
                                       'delta_internal_flux_at_15':dflux.data(),
                                       'delta_external_flux_at_15':exterior.data(),
                                       'changes':{str(i):{key:v.data() for key,v in vals.items()}
                                                  for i,vals in fields.items()}}})
    return {'e':'1/6','slope_at_frozen_prefix':(-box(1)/(2*(y[u]+3))).data(),
            'first_postsend_G15':(w[z]*(y[z]-y[u])).data(),'arms':result,'physical_P3':{'NOT_RUN':60}}
