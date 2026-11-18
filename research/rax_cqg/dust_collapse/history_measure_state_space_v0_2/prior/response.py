"""Two selected N14 branches: contracted clock packet and conditional q7 instrument."""
import argparse
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from unittest.mock import patch

if __name__ == "__main__":
    for name in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[name] = "1"

import numpy as np

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "v05"))
sys.path.insert(0, str(ROOT / "v05/upstream"))
import clock14
import quadrature
from growth import layout, geometry
from clock_network import BETA, STEP, RHO, density_factor, encode, decode
from clocks import quadrature as rule

MASKS = (1790, 5374)
GRIDS = ((32, 6), (48, 8), (64, 10), (80, 12))


def encode_complex(values):
    return np.stack((values.real, values.imag), axis=-1).tolist()


def decode_complex(values):
    pairs = np.array(values)
    return pairs[..., 0] + 1j * pairs[..., 1]


def samples(mask, n, times, lib):
    """Keep the first clock fixed. Contract three remaining clock axes at most."""
    inner, coeff, gravity = layout((6, mask))
    assert inner == (4, 5, 6, 11, 12, 13)
    past, future = geometry.P, geometry.F
    nodes, weight = rule(n)
    x = 1.5 * nodes
    fixed = {i: (i - 5)*STEP for i in (*past, *future)}
    fixed[3] = times
    def collar(j):
        return 1 + BETA/2 * sum(v*(fixed[j] - fixed[i])**2 for (i,k),v in coeff.items()
                              if k == j and i in fixed)
    past_phase = sum(collar(j) for j in past)
    overall = np.exp(1j*(gravity - sum(collar(j) for j in future)/16))
    dist = (x[:, None] - x[None, :])**2
    edge = {(i,j): BETA/2*v*dist for (i,j),v in coeff.items() if i in inner and j in inner and v}
    base = {}
    unary = {}
    parents = []
    for j in inner:
        base[j] = 1 + BETA/2*sum(coeff[i,j]*(x-(fixed[i][:, None] if i==3 else fixed[i]))**2
                                 for i in past)
        unary[j] = weight*np.exp(-1j*BETA/32*sum(coeff[j,i]*(fixed[i]-x)**2 for i in future))
        parents.append([i for i in inner if (i,j) in edge])
    if mask == 1790:
        assert parents == [[], [], [4,5], [4,5,6], [4,5,6], [4]]
        twin_left, twin_right = 11, 12
    else:
        assert mask == 5374 and parents == [[], [], [4,5], [4,5], [4,5,6,11], [4]]
        assert coeff[3,12] == 0 and np.all(base[12][0] == base[12])
        twin_left, twin_right = 6, 11
    assert np.array_equal(base[twin_left], base[twin_right])
    assert np.array_equal(unary[twin_left], unary[twin_right])
    assert all(np.array_equal(edge[i,twin_left],edge[i,twin_right])
               for i in parents[inner.index(twin_left)])

    def tail_arguments(child, remaining_parents):
        edges = np.ascontiguousarray([edge[i,child] for i in remaining_parents])
        return edges, np.exp(-0.5j*edges)
    def tail(c, u, edges, phases):
        count = len(edges)
        out = np.empty((n,)*count, dtype=complex)
        lib.tail(n,count,c,np.exp(-0.5j*c),u,edges,phases,out)
        return out

    max_child = 11 if mask == 1790 else 12
    remaining = [5,6] if mask == 1790 else [5,6,11]
    edges, phases = tail_arguments(max_child, remaining)
    # The independent leaf 13 is connected only to 4. The main sum over
    # leaves uses the actual collar coefficients of this labelled geometry.
    f4 = unary[4]*density_factor(base[4])
    f5 = unary[5]*density_factor(base[5])
    result = np.zeros(len(times), dtype=complex)
    for a in range(n):
        f13 = np.sum(unary[13]*density_factor(base[13] + edge[4,13][a]),axis=1)
        f6 = unary[6]*density_factor(base[6][:,None,:] + edge[4,6][a] + edge[5,6])
        if mask == 1790:
            # At fixed (4,5,6), the equal integrations over 11 and 12 multiply.
            middle = np.empty_like(f5)
            for t,c in enumerate(base[11]):
                leaf = tail(c+edge[4,11][a], unary[11], edges, phases)
                middle[t] = (f6[t]*leaf**2).sum(axis=1)
        else:
            # At fixed 4, integrate 12 conditional on (5,6,11) once for all
            # collar times. The two identical sibling factors are multiplied
            # bilinearly, before conjugation in the subsequent Born readout.
            joint = tail(base[12][0]+edge[4,12][a], unary[12], edges, phases)
            middle = np.empty_like(f5)
            for b in range(n):
                f = f6[:,b,:]
                middle[:,b] = ((f@joint[b])*f).sum(axis=1)
        result += f4[:,a]*f13*(f5*middle).sum(axis=1)
    return past_phase, overall*result


def packet(mask, n, m, lib):
    nodes, w = rule(m)
    mid = -2*STEP
    t = np.r_[mid-1/16+nodes/32, mid+1/16+nodes/32, mid]
    phases, amplitudes = samples(mask,n,t,lib)
    norm = 1/np.sqrt(48*32)
    lobes = np.empty((2,2),dtype=complex)
    compensated = 0j
    for side in range(2):
        sl = slice(side*m,(side+1)*m)
        p,z = phases[sl], amplitudes[sl]
        compensated += norm*(w@z)/np.sqrt(2)
        for j,r in enumerate(RHO):
            lobes[j,side] = norm*((w*np.sinc(p/(64*np.pi))*np.exp(-0.5j*r*p))@z)
    return lobes, compensated, (phases[-1], amplitudes[-1])


def grid_result(packets, scalar_bins):
    scalars = np.array([p[0].sum(axis=1)/np.sqrt(2) for p in packets]).T
    effects = (scalars.conj()[:,None,:,None]*scalar_bins[None]*scalars[:,None,None,:])
    delta = np.array([-1.,1.])
    def outcomes(weights):
        accepted = weights@effects@weights
        assert np.max(abs(accepted.imag))<1e-18 and np.min(accepted.real)>=0
        accepted = accepted.real
        return np.column_stack((accepted, 1-accepted.sum(axis=1)))
    mixtures = [[.75,.25],[.5,.5],[.25,.75]]
    results = np.array([outcomes(np.array(w)) for w in mixtures])
    differences = (delta@effects@delta).real
    centre_difference = results[0,:,:3]-2*results[1,:,:3]+results[2,:,:3]
    assert np.max(abs(centre_difference - 2*(1/4)**2*differences))<2e-18
    assert np.all(differences>0) and np.all(results>=0)
    # Zero off-diagonal response keeps the exact branch effects but removes
    # two-branch interference; the relative phase test changes its sign.
    diagonal = np.diagonal(effects,axis1=-2,axis2=-1).real
    off_diagonal = 0.5*effects[:,:,0,1].real
    incoherent = diagonal.sum(axis=-1)/4
    assert np.allclose(results[1,:,:3], incoherent+off_diagonal, rtol=0,atol=1e-18)
    return {"coherent_effects": encode_complex(effects), "delta_quadratic": differences.tolist(),
            "pair_preparations": results.tolist(), "at_equal_weights_incoherent_accepted":incoherent.tolist(),
            "at_equal_weights_interference_accepted":off_diagonal.tolist()}


def run(sector_path):
    if not __debug__:
        raise RuntimeError("Run with assertions active")
    sector = json.loads(sector_path.read_text())
    assert sector["order"] == list(MASKS)
    scalar_bins = decode_complex(sector['pointer_effects_scalar'])
    assert np.allclose(scalar_bins.sum(axis=0),decode_complex(sector['gram_scalar']),atol=1e-14,rtol=0)
    weights = json.loads((ROOT/'v05/exchange.json').read_text())['one']['witness_N14_end_weights']
    assert [weights[str(k)] for k in MASKS] == ['1/882','1/882']
    with TemporaryDirectory() as tmp:
        lib = quadrature.build(tmp)
        err = {}
        elimination_check = {}
        for mask in MASKS:
            small = packet(mask,4,3,lib)
            direct = clock14.direct_packet((6,mask),4,3)
            err[str(mask)] = float(max(abs(clock14.flat(small)-clock14.flat(direct))))
            assert err[str(mask)] < 2e-13 and abs(small[-1][0]-direct[-1][0]) < 2e-13
            # The published general eliminator uses different tensor groupings.
            # At ten nodes its widest intermediate (10**5) remains modest.
            with patch.object(clock14.reference, "layout", layout):
                reference = clock14.reference.packet((6,mask),10,5)
            contracted = packet(mask,10,5,lib)
            gap = float(max(abs(clock14.flat(contracted)-clock14.flat(reference))))
            assert gap < 2e-13 and abs(contracted[-1][0]-reference[-1][0]) < 2e-13
            elimination_check[str(mask)] = gap
        rows, old = [], None
        for n,m in GRIDS:
            packets = [packet(mask,n,m,lib) for mask in MASKS]
            current = np.array([clock14.flat(p) for p in packets])
            row = {"grid":[n,m], "packets":[encode(p) for p in packets],
                   **grid_result(packets,scalar_bins)}
            rows.append(row)
            if old is not None:
                change = float(np.max(abs(current-old)))
                row['max_packet_change'] = change
                if change < 2e-12:
                    break
            old = current
        else:
            raise ArithmeticError("No resolved production grid within local budget")
        # Separate last inner and outer refinements to guard against cancellation.
        (nc,mc),(nf,mf) = [r['grid'] for r in rows[-2:]]
        groups = [[decode(p) for p in r['packets']] for r in rows[-2:]]
        fc = [packet(mask,nf,mc,lib) for mask in MASKS]
        cf = [packet(mask,nc,mf,lib) for mask in MASKS]
        def distance(x,y):
            return float(max(max(abs(clock14.flat(a)-clock14.flat(b))) for a,b in zip(x,y)))
        crossed = [distance(groups[0],cf),distance(groups[0],fc),
                   distance(groups[1],cf),distance(groups[1],fc)]
        assert max(crossed)<2e-12
    return {"order":list(MASKS), "source":"v0.5 boundary contract, including exp(i F4) exactly once in each clock amplitude",
            "conditioning":"explicit coherent preparation restricted to the two endtypes of the one-edge root; amplitudes rescaled by their common total 1/441",
            "weight_vectors":[["3/4","1/4"],["1/2","1/2"],["1/4","3/4"]],
            "densities":["1/8","1/4"], "outcomes":["left","middle","right","failure"],
            "direct_small_cartesian_packet_errors":err,"independent_elimination_packet_errors_10_5":elimination_check,"crossed_grid_max_packet_changes":crossed,
            "crossed_grid_comparisons":["outer at coarse inner","inner at coarse outer","inner at fine outer","outer at fine inner"],
            "production_grids":rows}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output",type=Path)
    parser.add_argument("--sector",type=Path,default=ROOT/'sector.json')
    args = parser.parse_args()
    args.output.write_text(json.dumps(run(args.sector),indent=2,sort_keys=True,allow_nan=False)+'\n')
