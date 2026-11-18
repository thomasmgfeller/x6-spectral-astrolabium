"""Replay of the extension contracts; local CPU only, with no network requests."""
import argparse
import itertools
import json
import hashlib
from pathlib import Path
import numpy as np
import geometry as g
from clocks import amplitudes, direct_lift, weights, STEP, RHO

ROOT=Path(__file__).resolve().parent
BASE=("chain","one")
MODES=("coherent","dephased_lobes","relative_pi_phase","phase_compensated","fixed_clock")
GRIDS=g.CONTRACT["quadrature"]["grids"]


def topology():
    triples=(4,5,6)
    labelled=set()
    counts={}
    for name,edges in g.CONTRACT["interior"].items():
        orbit=set()
        for perm in itertools.permutations(triples):
            rel=dict(zip(triples,perm))
            orbit.add(tuple(sorted((rel[i],rel[j]) for i,j in edges)))
        assert not (orbit & labelled)
        labelled.update(orbit)
        counts[name]=len(orbit)
    pairs=list(itertools.permutations(triples,2))
    all_posets=set()
    for mask in range(1<<len(pairs)):
        rel={ij for k,ij in enumerate(pairs) if mask & (1<<k)}
        if all((a,d) in rel for a,b in rel for c,d in rel if b==c):
            all_posets.add(tuple(sorted(rel)))
    assert labelled == all_posets and len(all_posets)==19
    for key,original in (("chain_lift","chain"),("one_lift","one")):
        a=set(g.order(key)[1]);b=set(g.order(original)[1])
        assert {e for e in a if 11 not in e}==b
    return counts


def four(vector,effects):
    accepted=np.einsum('i,kij,j->k',vector.conj(),effects,vector).real
    p=np.append(accepted,1-sum(accepted))
    assert min(p)>=-1e-14 and abs(sum(p)-1)<1e-14
    return p


def distribution(names,all_names,amplit,effects,coeff):
    indices=[all_names.index(x) for x in names]
    E=effects[:,indices][:,:,indices]
    norm=np.asarray(coeff)
    assert min(norm)>=0 and abs(sum(norm)-1)<1e-13
    out={mode:[] for mode in MODES}
    for j,r in enumerate(RHO):
        a,b=np.array([amplit[k][0][j] for k in names]).T*norm
        plus=four((a+b)/np.sqrt(2),E)
        minus=four((a-b)/np.sqrt(2),E)
        mix=(four(a,E)+four(b,E))/2
        np.testing.assert_allclose((plus+minus)/2,mix,atol=2e-15,rtol=0)
        comp=four(norm*np.array([amplit[k][1] for k in names]),E)
        fixed=four(norm*np.array([amplit[k][2][1]*np.exp(-0.5j*r*amplit[k][2][0]) for k in names]),E)
        for mode,p in zip(MODES,(plus,mix,minus,comp,fixed)): out[mode].append(p)
    arr={m:np.array(row) for m,row in out.items()}
    for mode in ("phase_compensated","fixed_clock"):
        np.testing.assert_allclose(arr[mode][0],arr[mode][1],atol=5e-15,rtol=0)
    return arr


def assess(arr,base):
    p=arr["coherent"];old=base["coherent"]
    tv=np.abs(p-old).sum(axis=1)/2
    refsuccess=old[:,:3].sum(axis=1)
    contrast=p[1]-p[0];oldcontrast=old[1]-old[0]
    distance=float(np.abs(contrast-oldcontrast).sum()/2)
    ref=float(np.abs(oldcontrast).sum()/2)
    dp=p[:,:3].sum(axis=1)
    delta=float(dp[1]-dp[0])
    checks=[bool(np.all(tv<=0.10*refsuccess)),bool(distance<=0.25*ref),bool(delta*(refsuccess[1]-refsuccess[0])>0)]
    return {"base_success":refsuccess.tolist(),"success":dp.tolist(),"success_delta":delta,
            "density_contrast":contrast.tolist(),"TV_each_density":tv.tolist(),
            "TV_over_base_success":(tv/refsuccess).tolist(),
            "contrast_half_L1_distance":distance,"contrast_change_relative":distance/ref,
            "gates_levels_contrast_sign":checks,"pass":all(checks)}


def first_loss(at,endpoint,base):
    # Every outcome is exactly quadratic in total new amplitude weight. Search all
    # polynomial intersections, including all signed branches of the L1 gates.
    p0=base["coherent"];pm=at(endpoint/2)["coherent"];p1=at(endpoint)["coherent"]
    qc=2*(p1+p0-2*pm); qb=p1-p0-qc
    model=lambda u:p0+qb*u+qc*u*u
    np.testing.assert_allclose(model(0.37),at(endpoint*0.37)["coherent"],atol=2e-15,rtol=0)
    roots={0.,1.}
    def cut(a,b,c):
        for root in np.roots([a,b,c]):
            if abs(root.imag)<1e-9 and 0<root.real<1: roots.add(float(root.real))
    ref=p0[:,:3].sum(axis=1)
    for sign in itertools.product((-1,1),repeat=4):
        s=np.array(sign)
        for j in (0,1):
            cut(s@qc[j],s@qb[j],-0.2*ref[j])
        cut(s@(qc[1]-qc[0]), s@(qb[1]-qb[0]),-0.25*np.abs(p0[1]-p0[0]).sum())
    cut((qc[1]-qc[0])[:3].sum(),(qb[1]-qb[0])[:3].sum(),ref[1]-ref[0])
    knots=sorted(roots)
    for lo,hi in zip(knots,knots[1:]):
        if hi-lo<1e-11: continue
        if not assess({"coherent":model((lo+hi)/2)},base)["pass"]:
            return lo*endpoint
    return None


def main():
    g.mp.mp.dps=55
    base_clock=json.loads((ROOT/"reference/clock_packet_results.json").read_text())["finest_grid"]
    gauss=json.loads((ROOT/"reference/gaussian_outputs.json").read_text())
    ref_contract=json.loads((ROOT/"reference/packet_contract.json").read_text())
    assert ref_contract["quadrature_inner_outer"]==GRIDS and ref_contract["density_centers"]==list(RHO)
    counts=topology()
    structural={}; states={}; supplementary={}
    for name in g.CONTRACT["stages"]["F7"]:
        structural[name],state=g.kernel(name)
        if state is None:
            supplementary[name],state=g.kernel(name,True)
        if state is not None: states[name]=state
    for name,ref in zip(BASE,gauss["branches"]):
        P,N=states[name]
        rv=lambda z:g.mp.mpc(z["re"],z["im"])
        assert abs(N-rv(ref["N"]))<g.mp.mpf('2e-48')
        for i,j in itertools.product(range(3),repeat=2):
            assert abs(P[i,j]-rv(ref["P_equals_beta_Omega"][i][j]))<g.mp.mpf('2e-48')
    effects=g.readout(states); names=list(states)
    separation_error=float(abs(weights("chain_lift",-2*STEP+1/16,12)[1]-direct_lift(-2*STEP+1/16,12)))
    assert separation_error<5e-13
    families={s:tuple(a) for s,a in g.CONTRACT["stages"].items()}
    families.update({"add_"+name:(*BASE,name) for name in structural if name not in BASE})
    families["add_both_lifts"]=(*BASE,"chain_lift","one_lift")
    results={}; previous={}
    for n,m in GRIDS:
        run={}; raw={name:amplitudes(name,n,m) for name in names}
        for fam,group in families.items():
            missing=[k for k in group if k not in names]
            if missing: continue
            probs=distribution(group,names,raw,effects,[1/len(group)]*len(group))
            run[fam]=probs
            if previous:
                diff=max(float(np.max(np.abs(arr-previous[fam][mode]))) for mode,arr in probs.items())
                assert diff<5e-12,(fam,diff)
                primary=all(structural[k]["status"]=="ADMISSIBLE" for k in group)
                row={"scope":"parent_rigging" if primary else "with_extra_bulk_volume_division",
                     "grid_max_probability_change":diff,
                     "outcomes":{m:v.tolist() for m,v in probs.items()},"comparison":assess(probs,run["F2"])}
                if len(group)>2:
                    endpoint=(len(group)-2)/len(group)
                    def at(lam):
                        coeff=[(1-lam)/2]*2+[lam/(len(group)-2)]*(len(group)-2)
                        return distribution(group,names,raw,effects,coeff)
                    added=distribution(group[2:],names,raw,effects,[1/(len(group)-2)]*(len(group)-2))
                    base_joint=run["F2"]["coherent"][:,:3]
                    new_joint=added["coherent"][:,:3]
                    attenuated=(1-endpoint)**2*base_joint
                    new_only=endpoint**2*new_joint
                    interference=probs["coherent"][:,:3]-attenuated-new_only
                    row["diagnostic_accepted_bins_by_density"]={
                        "old_diagonal_at_new_weight":attenuated.tolist(),
                        "new_diagonal_at_new_weight":new_only.tolist(),
                        "old_new_interference":interference.tolist(),
                        "delta_success_terms":[float(np.sum(v[1]-v[0])) for v in (attenuated,new_only,interference)]}
                    row["equal_weight_endpoint"]=endpoint
                    row["first_gate_loss_lambda"]=first_loss(at,endpoint,run["F2"])
                    row["mass_path"]=[{"lambda":l,"comparison":assess(at(l),run["F2"])}
                                      for l in (0,0.05,0.10,0.20,endpoint)]
                    np.testing.assert_allclose(at(0)["coherent"],run["F2"]["coherent"],rtol=0,atol=2e-15)
                results[fam]=row
        previous=run
    anchor_error=0.
    for j,high in enumerate(base_clock["clock_density_packets"]):
        for mode in MODES[:4]:
            anchor_error=max(anchor_error,float(np.max(np.abs(previous["F2"][mode][j]-high[mode]["joint_left_middle_right_failure"]))))
    assert anchor_error<5e-12
    primary_status={fam:("OBSTRUCTION: "+", ".join(k for k in members if structural[k]["status"]!="ADMISSIBLE")
                         if any(structural[k]["status"]!="ADMISSIBLE" for k in members)
                         else ("PASS" if results[fam]["comparison"]["pass"] else "FAIL_EXPLORATORY_TOLERANCE"))
                    for fam,members in families.items()}
    return {"base_commit":g.CONTRACT["base_commit"],"internal_orbit_sizes_among_19_labelled":counts,
            "contracts_sha256":{k:hashlib.sha256((ROOT/k).read_bytes()).hexdigest() for k in ("contract.json","supplement.json")},
            "rank_screen":structural,"screen_after_bulk_division":supplementary,"primary_status":primary_status,
            "designs":{k:list(v) for k,v in families.items()},"evaluated":results,
            "parent_max_probability_error":anchor_error,"direct_4d_factorization_error_n12":separation_error}


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=main()
    if args.output: args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+"\n")
    print(json.dumps({k:{"scope":v["scope"],"delta":v["comparison"]["success_delta"],
                         "TV/base":v["comparison"]["TV_over_base_success"],"contrast_change":v["comparison"]["contrast_change_relative"],
                         "first_loss":v.get("first_gate_loss_lambda"),"grid":v["grid_max_probability_change"]}
                      for k,v in result["evaluated"].items()},indent=2))
