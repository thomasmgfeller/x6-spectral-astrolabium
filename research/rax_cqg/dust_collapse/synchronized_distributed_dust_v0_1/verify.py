"""Offline verification of input identities, rational certificates and controls."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from itertools import product

import census
import charge_control
import coherence
import saddle
import support
import tube

ROOT=support.HERE
sys.path.insert(0,str(ROOT/'inputs/variation'))
from variation import matter_action
from gluing import encode


def read(name):
    return json.loads((ROOT/name).read_text())


def action_check(signs):
    n=0
    for key,data in signs["by_type"].items():
        if not data["full_box"]:
            continue
        code=int(key)
        _,rel=support.geometry(code)
        bit_code=encode(rel,15)
        paths,center,_,_,_,_=tube.template(code)
        f=support.fractions_on_paths(paths,center)
        for side,e in enumerate((Q(-1,4),Q(1,4))):
            # y=T/Delta; in the exact response p/M the units give beta*Delta^2=2/19.
            T={v:Q(v-5) for v in support.PAST+support.FUTURE}
            T[3]+=e
            T.update((v,-2+e+(4-e)*center[v]) for v in support.I)
            t=[T[i] for i in range(15)]
            w=[Q(1,8)]*15
            for v,frac in zip(support.I,f):
                w[v]=(4-e)*frac
            tau=Q(1,8)
            plus=[y+(tau/2 if v in support.PAST else 0) for v,y in enumerate(t)]
            minus=[y-(tau/2 if v in support.PAST else 0) for v,y in enumerate(t)]
            val=Q(2,19)*(matter_action(bit_code,15,minus,w)-matter_action(bit_code,15,plus,w))/tau
            if code==2324:
                assert val==(Q(-391,912),Q(-69,304))[side]
            l,r=data['p_over_M_lobe_bounds_nanounits'][side]
            assert l<=val*10**9<=r
            n+=1
    return n


def verify():
    for record in read("sources.json")["files"].values():
        if "local" in record:
            raw=(ROOT/record["local"]).read_bytes()
            assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\x00"+raw).hexdigest()==record["sha"]
    assert hashlib.sha256((ROOT/"design.json").read_bytes()).hexdigest()=="2af687f759185b4aa294af89bb9d2f2038bc1349b9b6abb819f0861aa117bb6a"
    certs=read("certificates.json")
    capacity=support.summarize(certs)
    assert capacity==read("capacity.json")
    independent=read("independent_complete.json")
    for k,v in certs.items():
        opt=Q(v["primal"][-1])
        pattern="".join(str(int(support.open_at(Q(4),x,opt))) for interval in support.WINDOWS for x in interval)
        assert pattern==independent["heavy_by_type"][k]
    s=saddle.run()
    t=tube.run()
    c=coherence.run()
    q=charge_control.run()
    series=census.run()
    for name,value in (("saddle",s),("tube",t),("coherence",c),("charge_control",q),("census",series)):
        assert json.loads(json.dumps(value))==read(name+".json")
    assert all(v["conditional_modulus_lower_display"]>0 for v in c["rows"].values())
    assert all(Q(v["p_over_M_enclosure"][1])<0 for v in q["fine_source_only"].values())
    assert series["by_type"]["2324"]["signs"]=="--"
    rows=read("inputs/checkpoints.json")
    eligible=read("inputs/eligibility.json")
    assert len(rows)==60 and all(r["execution"]=="NOT_RUN" for r in rows)
    assert eligible["decision"]=="HOLD_NOT_ELIGIBLE"
    return {"capacity":capacity["packet_counts"],"local_saddle_exclusions":s["excluded_type_count"],
            "diagnostic_charge_tube":series["counts"],"lobe_signs":series["sign_patterns_left_right"],
            "independent_action_differences":action_check(series),
            "negative_source_selected_positive_band_on_type_2324_tube":"identically zero",
            "physical_sector_norm":None,"physical_mass_standard":None,"physical_gain":None,
            "physical_pilot":"NOT_RUN","physical_checkpoints_not_run":len(rows)}


if __name__=="__main__":
    if not __debug__:
        raise RuntimeError('Verification requires Python without -O')
    print(json.dumps(verify(),indent=2,sort_keys=True))
