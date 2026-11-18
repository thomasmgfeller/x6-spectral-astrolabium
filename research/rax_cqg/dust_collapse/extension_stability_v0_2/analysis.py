"""Readout under fixed parent weights and controls over the entire conditional weight class."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import numpy as np
from families import ROOT,BASE,screen,scalar,name
from integrals import decode
from run import assess,first_loss
from abel_check import numerical_state
from certificates import check_weight_class

CONTRACT=json.loads((ROOT/"fibre_contract.json").read_text())


def matrices(names,effects,amp):
    # The real polarization of the normalized four-outcome distribution.
    # For weights summing to one the failure matrix is 11^T minus the sum of accepted effects.
    out={k:[] for k in ("coherent","dephased_lobes","relative_pi_phase","phase_compensated","fixed_clock")}
    def bilinear(vec):
        bins=(effects*vec.conj()[None,:,None]*vec[None,None,:]).real
        return np.concatenate([bins,(1-bins.sum(axis=0))[None]],axis=0)
    for j,r in enumerate((1/8,1/4)):
        a,b=np.array([amp[n][0][j] for n in names]).T
        plus=bilinear((a+b)/np.sqrt(2));minus=bilinear((a-b)/np.sqrt(2))
        mix=(bilinear(a)+bilinear(b))/2
        np.testing.assert_allclose(mix,(plus+minus)/2,atol=4e-15,rtol=0)
        comp=bilinear(np.array([amp[n][1] for n in names]))
        fixed=bilinear(np.array([amp[n][2][1]*np.exp(-0.5j*r*amp[n][2][0]) for n in names]))
        for key,v in zip(out,(plus,mix,minus,comp,fixed)):out[key].append(v)
    res={k:np.array(v) for k,v in out.items()}
    assert max(abs(res["fixed_clock"][0]-res["fixed_clock"][1]).ravel())<1e-14
    return res


def probs(matrices,w):
    assert abs(sum(w)-1)<1e-13 and min(w)>-1e-14
    vals={k:np.einsum('i,dkij,j->dk',w,m,w) for k,m in matrices.items()}
    for v in vals.values():
        assert min(v.ravel())>-5e-14 and max(abs(v.sum(axis=1)-1))<5e-14
    return vals


def serial(v): return {k:val.tolist() for k,val in v.items()}


def allocation(pops,names,scheme):
    # Keep parent ledgers distinct even when two parents share an unmarked child.
    ledger={}
    for parent in BASE:
        c={k:(v if scheme=="marked" else 1) for k,v in pops[parent].items() if k in names}
        ledger[parent]={k:v/(2*sum(c.values())) for k,v in c.items()}
        assert abs(sum(ledger[parent].values())-0.5)<1e-15
    return ledger,np.array([sum(row.get(n,0) for row in ledger.values()) for n in names])


def class_enclosure(m,base,corners):
    # Approximate coefficients of exact polarization identities. If E1,E2
    # bound the normalized signed-law displacement at the cross and child-pair
    # levels, 2*l*(1-l)*E1+l^2*E2 bounds every allowed endpoint mixture.
    def cross(x,y):return np.einsum('i,dkij,j->dk',x,m,y)
    p=cross(base,base)
    def metrics(law):
        diff=law-p
        levels=abs(diff).sum(axis=1)/2/(0.1*p[:,:3].sum(axis=1))
        old_c=p[1]-p[0]
        c=diff[1]-diff[0]
        return np.r_[levels,abs(c).sum()/(.25*abs(old_c).sum()),abs(c[:3].sum()/old_c[:3].sum())]
    a=np.max([metrics(cross(base,v)) for v in corners],axis=0)
    b=np.max([metrics(cross(v,w)) for v,w in itertools.combinations_with_replacement(corners,2)],axis=0)
    upper=lambda l:2*l*(1-l)*a+l*l*b
    # First crossing of any normalized gate on [0,1]. Include any interior
    # maximum, so a nonmonotone quadratic cannot escape detection.
    roots=[]
    for aa,bb in zip(a,b):
        for z in np.roots([bb-2*aa,2*aa,-1]):
            if abs(z.imag)<1e-11 and 0<z.real<=1: roots.append(float(z.real))
    radius=min(roots,default=1.)
    stated=max(0.,np.floor((radius-1e-8)*1000)/1000)
    max_bound=upper(stated)
    for i,(aa,bb) in enumerate(zip(a,b)):
        if bb<2*aa:
            peak=aa/(2*aa-bb)
            if 0<peak<stated: max_bound[i]=max(max_bound[i],upper(peak)[i])
    assert max(max_bound)<1
    signs=[float((cross(v,w)[1,:3]-cross(v,w)[0,:3]).sum()) for v,w in itertools.combinations_with_replacement(corners,2)]
    return {"cross_gate_coefficients":a.tolist(),"child_pair_gate_coefficients":b.tolist(),"sufficient_crossing":radius,
            "reported_radius_rounded_down":float(stated),"maximum_normalized_bounds_on_reported_interval":max_bound.tolist(),
            "all_child_allocation_delta_enclosure_from_polarization":[min(signs),max(signs)]}


def analyze(cache):
    families,audit,states=screen()
    assert json.loads(json.dumps(audit))==cache["rank_audit"] and families==cache["families"]
    # A direct damped Gaussian integral checks every new scalar phase and width.
    scalar.mp.mp.dps=80;abel={}
    for n,(precision,amp) in states.items():
        P,ph=numerical_state(n,scalar.mp.mpf("1e-28"))
        err=max(abs(v) for v in P-precision); perr=abs(ph-amp/abs(amp))
        assert max(err,perr)<1e-17
        abel[n]={"precision_error":float(err),"unit_phase_error":float(perr)}
    names=list(states); E=scalar.readout(states)
    pops={p:Counter(name(v["mask"]) for v in vals) for p,vals in families.items()}
    shape_counts={p:dict(c) for p,c in pops.items()}
    base=np.array([.5 if k in BASE else 0 for k in names])
    grid_matrices=[]
    for ix in (-2,-1):
        raw={k:decode(cache["grids"][k][ix]["amplitudes"]) for k in names}
        grid_matrices.append(matrices(names,E,raw))
    coarse,m=grid_matrices
    worst=max(np.max(abs(coarse[k]-m[k])) for k in m)
    # This controls the observed grid change for every normalized choice of
    # nonnegative weights, including those outside the two named laws.
    assert worst<5e-12,worst
    anchor=probs(m,base)
    parent=json.loads((ROOT/"reference/extension_results.json").read_text())["evaluated"]
    orig_error=max(np.max(abs(arr-np.array(parent["F2"]["outcomes"][k]))) for k,arr in anchor.items())
    assert orig_error<5e-12
    independent_mask=next(r["mask"] for r in families["chain"] if r["relations_to_new"]==[0,0,0])
    lift=name(independent_mask)
    e=np.eye(len(names));unit=dict(zip(names,e))
    old_global=(unit["chain"]+unit["one"]+unit[lift])/3
    old_error=max(np.max(abs(probs(m,old_global)[k]-parent["add_chain_lift"]["outcomes"][k])) for k in m)
    assert old_error<5e-12
    summary={}
    def campaign(end):
        at=lambda l:probs(m,(1-l)*base+l*end)
        return {"endpoint_weights":dict(zip(names,map(float,end))),
                "first_gate_loss_replaced_fraction":first_loss(at,1.,anchor),
                "samples":[{"replaced_fraction":v,"metrics":assess(at(v),anchor),"all_modes":serial(at(v))}
                           for v in CONTRACT["lambda"]]}
    for law in ("marked","shapes"):
        ledger,weights=allocation(pops,names,law)
        summary[law]=dict(campaign(weights),parent_ledgers=ledger)
    singled=[]
    for total in (0,.05,.1,.25,1/3,.5):
        w=base+total*(unit[lift]-unit['chain'])
        vals=probs(m,w)
        singled.append({"child_total":total,"weights":dict(zip(names,map(float,w))),"metrics":assess(vals,anchor),"all_modes":serial(vals)})
    first_lift=first_loss(lambda w:probs(m,base+w*(unit[lift]-unit["chain"])),.5,anchor)
    chosen=[[k for k in pops[p] if k in names] for p in BASE]
    corners=[]; tests=[]
    for a,b in itertools.product(*chosen):
        w=(unit[a]+unit[b])/2
        corners.append(w)
        scores=assess(probs(m,w),anchor)
        tests.append({"chain_child":a,"one_child":b,"metrics":scores})
    result={
        "parent_counts":shape_counts,"admissible_names":names,"gaussian_abel":abel,
        "matrix_grid_difference_max_all_modes_all_weights":float(worst),"base_error":float(orig_error),"previous_three_history_error":float(old_error),
        "base_outcomes":serial(anchor),"two_growth_laws":summary,"one_chain_child_balanced":singled,
        "one_chain_child_first_loss_total":first_lift,"one_chain_child_previous_global_equal":assess(probs(m,old_global),anchor),
        "deterministic_extension_pairs":tests,"uniform_sufficient_enclosure":class_enclosure(m["coherent"],base,corners),
        "supplementary_weight_checks":{tag:check_weight_class(matrix["coherent"],names,BASE)
                                       for tag,matrix in (("coarse",coarse),("fine",m))},
        "fine_coherent_readout_matrices":m["coherent"].tolist(),
        "fully_positive_unfiltered_marked_law":"UNDEFINED_UNDER_PR295_SCALAR_PAIRING",
        "scope":"One marked event; fixed outer collar and conditional admitted scalar subspace; quadrature changes empirical."}
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('grids',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args()
    args.output.write_text(json.dumps(analyze(json.loads(args.grids.read_text())),indent=2,allow_nan=False)+"\n")
