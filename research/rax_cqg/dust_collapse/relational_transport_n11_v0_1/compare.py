"""Endpoint pairings on the archived N11 input, with two shifted intermediate cuts."""
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from exact import ROOT, INNER, MASKS, ward, ideal, interior_ideal


def read(name):
    return json.loads((ROOT/name).read_text())


CONTRACT = read("contract.json")
GRID = CONTRACT["grids"]
TOL = 5e-9
ORDERS = [ward.coeffs(x) for x in ward.ORDERS.values()]
ETA = np.asarray(read("sources/readout.json")["one_unknown_pulse"]["reference_charge_efficiencies_C0_C1"]["1"])
PACKET = read("sources/preparation.json")
RHO_F = 1/8


def axis(a,b,n):
    x,w = leggauss(n)
    return (a+b)/2+(b-a)*x/2, w*((b-a)/6)


def times_and_weights(t, axes):
    times = [(j-5)*ward.DELTA for j in range(11)]
    times[3] = t
    for j,value in zip(INNER,np.ix_(*(x for x,w in axes))):
        times[j] = value
    a,b,c = np.ix_(*(w for x,w in axes))
    return times, a*b*c


def kernel_mean(direct, coefficients, times, axes, weights, left):
    """Dust only. Mark average performed after assembling the full incoming action."""
    left_factor = 1.
    right_factor = 1.
    future = 0
    for j in (*INNER,*ward.FUTURE):
        incoming = [(i,v) for (i,k),v in coefficients.items() if k==j and v]
        if direct:
            kinetic = sum(v*(times[j]-times[i])**2 for i,v in incoming)
        else:
            local = [(i,v) for i,v in incoming if (i in left)==(j in left)]
            crossing = [(i,v) for i,v in incoming if (i in left)!=(j in left)]
            # Cross terms are evaluated at the join, including backward
            # C0-dust control edges possible on a C1 geometric cut.
            internal = sum(v*(times[j]-times[i])**2 for i,v in local)
            a = sum(v for i,v in crossing)
            b = sum(v*times[i] for i,v in crossing)
            c = sum(v*times[i]**2 for i,v in crossing)
            kinetic = internal + a*times[j]**2 - 2*b*times[j] + c
        local_action = 1+ward.BETA*kinetic/2
        if j in INNER:
            mark = (1+np.exp(-0.25j*local_action)*np.sinc(local_action/(4*np.pi)))/2
            if not direct and j in left and all(i in left for i,v in incoming):
                left_factor = left_factor*mark
            else:
                right_factor = right_factor*mark
        else:
            future = future + local_action
    right_factor = np.exp(-0.5j*RHO_F*future)*right_factor
    if direct:
        return np.sum(weights*right_factor)
    # Integrate the right subkernel first at fixed incoming separator data.
    # The left factor is then paired only on the remaining left coordinates.
    shape = tuple(len(x) for x,w in axes)
    right = np.broadcast_to(right_factor,shape)
    kept = [k for k,j in enumerate(INNER) if j in left]
    for k in reversed(range(len(INNER))):
        if k not in kept:
            right = np.tensordot(right,axes[k][1],axes=(k,0))
    left_shape = tuple(n if k in kept else 1 for k,n in enumerate(shape))
    left_array = np.broadcast_to(left_factor,left_shape).reshape(right.shape)
    paired = left_array*right
    for k in reversed(kept):
        paired = np.tensordot(paired,axes[k][1],axes=(-1,0))
    return complex(paired)


def past_set(mask,relation):
    return set(ward.PAST) | {j for j,inside in zip(INNER,interior_ideal(mask,relation)) if inside}


def assemble(t, cut):
    # Geometry and dust action indices, respectively. The control on C1 uses C0 dust.
    assignments = [(0,0),(1,1),(1,0)]
    full = np.zeros(3,complex)
    prefix = np.zeros(3,complex)
    if cut is None:
        axes = [axis(-ward.L,ward.L,GRID["direct_inner"])]*3
        times,weights = times_and_weights(t,axes)
        dust = [kernel_mean(True,c,times,axes,weights,set()) for c,g in ORDERS]
        for k,(geo,action) in enumerate(assignments):
            full[k] = np.exp(1j*ORDERS[geo][1])*dust[action]
        return {"direct":full}
    boxes = [axis(cut,ward.L,GRID["cell_inner"]),axis(-ward.L,cut,GRID["cell_inner"])]
    for mask in MASKS:
        axes = [boxes[int(b)] for b in mask]
        times,weights = times_and_weights(t,axes)
        for k,(geo,action) in enumerate(assignments):
            relation,gravity = ORDERS[geo]
            c = ORDERS[action][0]
            left = past_set(mask,relation)
            amplitude = np.exp(1j*gravity)*kernel_mean(False,c,times,axes,weights,left)
            full[k] += amplitude
            if ideal(mask,relation):
                prefix[k] += amplitude
    return {"history":full,"raw_prefix":prefix}


def outer_grid(prep):
    t0 = -2*ward.DELTA
    if prep == "sharp":
        return [(t0,1.)]
    nodes,weights = leggauss(GRID["outer_per_lobe"])
    offsets = [0.] if prep=="narrow" else PACKET["clock_offsets_from_affine_T3"]
    return [(t0+offset+PACKET["clock_lobe_half_width"]*x,w/(2*len(offsets)))
            for offset in offsets for x,w in zip(nodes,weights)]


def encode_gram(g):
    return {"diagonal":g.diagonal().real.tolist(),"off_diagonal_re_im":[g[0,1].real,g[0,1].imag]}


def endpoint(prep,cut):
    grams = {}
    for t,weight in outer_grid(prep):
        for route,amps in assemble(t,cut).items():
            for arm,indices in (("coupled",[0,1]),("common_C0_dust",[0,2])):
                values = amps[indices]/2
                key = (route,arm)
                grams[key] = grams.get(key,0) + weight*np.outer(values.conj(),values)
    data = {}
    for (route,arm), g in grams.items():
        assert np.linalg.eigvalsh(g)[0] >= -1e-13
        detected = g.diagonal().real*ETA
        three,one = detected
        data.setdefault(route,{})[arm] = {"gram":encode_gram(g),
            "P_three_one_other":[three,one,1-three-one]}
    return data


def vector(entry):
    return np.array([*entry["gram"]["diagonal"],complex(*entry["gram"]["off_diagonal_re_im"]),
                     *entry["P_three_one_other"]])


def compute():
    archive = read("sources/clock_reference.json")
    answer = {}
    max_gap = 0.
    archive_gap = 0.
    for prep in ("sharp","narrow","split"):
        base = endpoint(prep,None)["direct"]
        row = {"direct":base}
        if prep in archive:
            for arm in base:
                old = archive[prep][arm]
                gap = max(abs(np.array([old["three_pairs"],old["one_pair"]])-base[arm]["gram"]["diagonal"]))
                archive_gap = max(archive_gap,gap)
                assert gap<TOL
        for name,cut in (("0",0.),("1/4",.25)):
            glued = endpoint(prep,cut)
            for arm in base:
                gap = max(abs(vector(base[arm])-vector(glued["history"][arm])))
                max_gap = max(max_gap,gap)
                assert gap<TOL, (prep,name,arm,gap)
            gap = base["coupled"]["P_three_one_other"][1] - glued["raw_prefix"]["coupled"]["P_three_one_other"][1]
            assert gap > 0.029
            row[name] = {**glued,"direct_minus_raw_P_one":gap}
        answer[prep] = row
    return {"results":answer,"max_direct_history_abs_gap":max_gap,
            "max_direct_archived_raw_branch_gap":archive_gap,
            "physical_status":"HOLD; unmodified raw-clock causal-prefix candidate excluded"}


if __name__ == "__main__":
    print(json.dumps(compute(),indent=2,allow_nan=False))
