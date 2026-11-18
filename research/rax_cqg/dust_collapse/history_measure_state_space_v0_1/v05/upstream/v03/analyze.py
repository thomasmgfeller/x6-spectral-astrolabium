"""Assemble the exact growth audit and coherent finite-size response."""
import argparse
from collections import Counter
from fractions import Fraction as Q
from itertools import product, combinations_with_replacement
import json
from pathlib import Path
import numpy as np
import sympy as sp
from orders import ROOT, ROOTS, label, orbit_table, paths, screen, daughter_counts, scalar_layouts, geometry
from compute import select
from clock_network import scheme, decode
from path_laws import summarize_paths
from abel_check import numerical_state
from run import assess
from endpoint_tests import endpoint_tests


def matrices(names, states, amps):
    effects = geometry.readout({k:states[k] for k in names})
    modes = {k:[] for k in ("coherent","relative_pi_phase","dephased_lobes","phase_compensated","fixed_clock")}
    def form(vec):
        accepted = (effects*vec.conj()[None,:,None]*vec[None,None,:]).real
        return np.concatenate((accepted,(1-accepted.sum(axis=0))[None]),axis=0)
    for i,r in enumerate((1/8,1/4)):
        x,y = np.array([amps[k][0][i] for k in names]).T
        plus,minus,mix = form((x+y)/np.sqrt(2)), form((x-y)/np.sqrt(2)), (form(x)+form(y))/2
        np.testing.assert_allclose((plus+minus)/2,mix,atol=4e-15,rtol=0)
        fixed = [amps[k][2][1]*np.exp(-.5j*r*amps[k][2][0]) for k in names]
        for key,v in zip(modes,(plus,minus,mix,form(np.array([amps[k][1] for k in names])),form(np.array(fixed)))):
            modes[key].append(v)
    result = {k:np.array(v) for k,v in modes.items()}
    for k in ("fixed_clock","phase_compensated"):
        np.testing.assert_allclose(result[k][0],result[k][1],atol=5e-15,rtol=0)
    return result


def probabilities(mats, w):
    assert abs(sum(w)-1)<1e-14 and min(w)>=0
    p = {k:w@v@w for k,v in mats.items()}
    for v in p.values():
        assert v.min() >= -5e-14 and np.max(abs(v.sum(axis=1)-1))<5e-14
    return p


def branch_splits(parent, allowed, law):
    n, mask = parent
    counts = daughter_counts(parent)
    children = {(n+1,g):(v if law=="marked" else 1) for g,v in counts.items() if (n+1,g) in allowed}
    return {k:Q(v,sum(children.values())) for k,v in children.items()}


def transfer(current, layer, fraction, allowed, law):
    weights = Counter()
    for key, mass in current.items():
        parts = branch_splits(key,allowed,law) if key[0]==layer else {}
        if not parts:
            weights[key] += mass
            continue
        weights[key] += mass * (1-fraction)
        for child, prop in parts.items():
            weights[child] += mass*fraction*prop
    assert sum(weights.values()) == 1
    return weights


def sign_certificate(m, names):
    # Apply exact rational algebra to the stored finite-grid values.
    get_q=np.vectorize(lambda x:Q.from_float(float(x)),otypes=[object])
    a=get_q(m)
    d=sum(a[1,:3]-a[0,:3])
    d=(d+d.T)/2
    upper=max(d[i,i]+sum(abs(d[i,j]) for j in range(len(d)) if j!=i) for i in range(len(d)))
    if upper < 0:
        return {"method":"Gershgorin","upper":float(upper),"negative_definite":True}
    # Exact LDL by symmetric elimination; negative pivots certify definiteness.
    h=sp.Matrix(d.tolist())
    pivots=[]
    for i in range(len(d)):
        pivot=h[0,0]
        pivots.append(float(pivot))
        if pivot>=0:
            break
        h=h[1:,1:]-h[1:,:1]*h[:1,1:]/pivot
    return {"method":"exact LDL","negative_definite":len(pivots)==len(d) and max(pivots)<0,
            "pivots":pivots,"upper_row_bound":float(upper)}


def uniform_bound(names, m, parents, mids, ends):
    # Every normalized descendant endpoint per root lies in this simplex,
    # regardless of the details of splitting and the intermediate transfer rate.
    eye=dict(zip(names,np.eye(len(names))))
    root=np.array([.5 if k in parents else 0 for k in names])
    options=[]
    for p in parents:
        first=set(branch_splits(p,mids,"marked"))
        reach=first|{g for h in first for g in branch_splits(h,ends,"marked")}
        options.append(sorted(reach))
    corners=[(eye[a]+eye[b])/2 for a,b in product(*options)]
    anchor=root@m@root
    def gauges(x):
        diff=x-anchor
        old=anchor[1]-anchor[0]
        delta=diff[1]-diff[0]
        return np.r_[np.abs(diff).sum(axis=1)/(.2*anchor[:,:3].sum(axis=1)),
                     np.abs(delta).sum()/(.25*np.abs(old).sum()),abs(delta[:3].sum()/old[:3].sum())]
    a=np.max([gauges(root@m@x) for x in corners],axis=0)
    b=np.max([gauges(x@m@y) for x,y in combinations_with_replacement(corners,2)],axis=0)
    # For every lambda <= L <= 1/2, upper bound both nonnegative
    # coefficients at L. Report a conservative radius in 0.1% steps.
    def cap(L):
        return 2*L*(1-L)*a+L**2*b
    radius=max(i/1000 for i in range(501) if max(cap(i/1000))<1)
    return {"corners":len(corners),"reported_radius":radius,"bounds_at_radius":cap(radius).tolist(),
            "bounds_at_five_percent":cap(.05).tolist(),"coefficients":[a.tolist(),b.tolist()]}


def main(grids):
    families=paths()
    audit,states=screen(families)
    children,small,extra=select(states)
    added=small|set(extra.values())
    all_mids=set(children)
    parent_keys=[(3,orbit_table(3)[old]) for old in ROOTS.values()]
    names=parent_keys+sorted(all_mids)+sorted(added)
    assert set(grids)=={label(k) for k in added}
    n12=json.loads((ROOT/'upstream/v02_grids.json').read_text())
    oldres=json.loads((ROOT/'upstream/v02_results.json').read_text())
    oldnames={**dict(zip(parent_keys,ROOTS)),**{k:f"poset{k[1]:02d}_lift" for k in all_mids}}
    for k,n in oldnames.items():
        inherited=n12['rank_audit'][n]
        for field in ('F4','status','legendre_rank','legendre_size','external_gauge_rank','free_directions'):
            assert inherited[field]==audit[k][field]
    geometry.mp.mp.dps=80
    independent={}
    with scalar_layouts():
        for k in sorted(added):
            P,phase=numerical_state(k,geometry.mp.mpf('1e-28'))
            current,amp=states[k]
            error=float(max(abs(v) for v in current-P));phase_error=float(abs(phase-amp/abs(amp)))
            assert max(error,phase_error)<1e-17
            independent[label(k)]=[error,phase_error]
    stored={}
    for i,tag in ((-2,'coarse'),(-1,'fine')):
        amp={k:decode(n12['grids'][n][i]['amplitudes']) for k,n in oldnames.items()}
        amp.update({k:decode(grids[label(k)]['grids'][i]['amplitudes']) for k in added})
        stored[tag]=matrices(names,states,amp)
    fine=stored['fine']
    err=max(float(np.max(abs(v-stored['coarse'][k]))) for k,v in fine.items())
    assert err<5e-12
    oldmatrix=np.array(oldres['fine_coherent_readout_matrices'])
    n=len(oldnames)
    anchored=float(np.max(abs(fine['coherent'][:,:,:n,:n]-oldmatrix)))
    assert anchored<5e-12
    base={key:Q(1,2) for key in parent_keys}
    def probs(w):
        return probabilities(fine,np.array([float(w.get(k,0)) for k in names]))
    anchor=probs(base)
    comparisons={}
    max_inherit=0.
    for category, support in (('width3',small),('width3_plus_controls',added)):
        rows=[]
        for law in ('marked','shapes'):
            for rate in (Q(0),Q(1,20),Q(1)):
                stage=transfer(base,3,rate,all_mids,law)
                local=probs(stage)
                original=next(s for s in oldres['two_growth_laws'][law]['samples'] if s['replaced_fraction']==float(rate))
                max_inherit=max(max_inherit,max(float(np.max(abs(v-np.array(original['all_modes'][k])))) for k,v in local.items()))
                for mu in (Q(0),Q(1,20),Q(1,2),Q(1)):
                    weights=transfer(stage,4,mu,support,law)
                    out=probs(weights)
                    rows.append({"law":law,"lambda":float(rate),"mu":float(mu),
                                 "mass_N13":float(sum(v for k,v in weights.items() if k[0]==5)),
                                 "weights":{label(k):str(v) for k,v in weights.items() if v},
                                 "vs_N11":assess(out,anchor),"vs_preceding":assess(out,local),
                                 "outcomes":{k:v.tolist() for k,v in out.items()}})
        comparisons[category]=rows
    assert max_inherit<5e-12
    all_paths={k:summarize_paths(k,v,states) for k,v in families.items()}
    end_types={g for ends in children.values() for g in ends}
    return {"domain":{label(k):v for k,v in audit.items()},"paths_by_root":all_paths,
            "counts":{"all_end_types":sum(k[0]==5 for k in audit),"admissible_end_types":sum(k[0]==5 for k in states),
                      "sequential_end_types":len(end_types),"not_sequential":[label(k) for k in states if k[0]==5 and k not in end_types]},
            "daughter_ledger":{label(k):{label((5,g)):v for g,v in sorted(daughter_counts(k).items())} for k in all_mids},
            "width3":sorted(label(k) for k in small),"width4_controls":{label(k):label(v) for k,v in extra.items()},
            "width_per_sequential_type":{label(k):scheme(k)[0] for k in sorted(end_types)},
            "branch_order":[label(k) for k in names],"max_matrix_grid_difference":err,"v02_matrix_replay_error":anchored,
            "v02_all_modes_replay_error":max_inherit,"independent_abel":independent,
            "weight_sign_diagnostic":{k:sign_certificate(v['coherent'],names) for k,v in stored.items()},
            "uniform_two_step_sufficient_bound":{k:uniform_bound(names,v['coherent'],parent_keys,all_mids,added) for k,v in stored.items()},
            "exploratory_endpoint_checks":{tag:endpoint_tests(m["coherent"],names,parent_keys,added,branch_splits,transfer) for tag,m in stored.items()},
            "outcome_matrices_fine_coherent":fine['coherent'].tolist(),"nested_comparisons":comparisons}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('grids',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    report=main(json.loads(args.grids.read_text()))
    args.output.write_text(json.dumps(report,indent=2,allow_nan=False,sort_keys=True)+'\n')
