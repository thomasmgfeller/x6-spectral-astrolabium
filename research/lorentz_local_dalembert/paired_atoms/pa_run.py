"""Paired membership transfers and exact Poisson void certificate.
SPDX-License-Identifier: Apache-2.0
"""
import sys, hashlib, math
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'joint_atoms'))
from ja_run import F,read,save,outward,sqrt_bounds,inputs
from sc_run import constant

def void_bounds(x):
    """Rational enclosure of 1-exp(-x), restricted to 0<=x<=1."""
    assert 0<=x<=1
    even=sum(((-x)**k/F(math.factorial(k)) for k in range(81)),F(0))
    odd=even-x**81/F(math.factorial(81))
    return 1-even,1-odd

def paired_bound(background, transfers):
    """Exact finite paired-region intensities, not Monte Carlo estimates.

    background[b] is the diagonal region (same membership under both laws).
    transfers[(b,c)] is the region changing from b to c, b!=c.
    """
    assert all(x>=0 for x in background.values())
    assert all(b!=c and x>=0 for (b,c),x in transfers.items())
    labels=set(background)|{b for edge in transfers for b in edge}
    incoming={b:F(0) for b in labels};outgoing=incoming.copy()
    for (b,c),x in transfers.items():outgoing[b]+=x;incoming[c]+=x
    means0={b:background.get(b,F(0))+outgoing[b] for b in labels}
    means1={b:background.get(b,F(0))+incoming[b] for b in labels}
    J=F(0);used_linear=0
    for b in labels:
        delta=abs(incoming[b]-outgoing[b])
        m=background.get(b,F(0))
        # Exact identity: root difference squared = delta^2/(sqrt(lambda)+sqrt(mu))^2.
        # Both intensities >=m, so denominator >=4m; also root difference squared <=delta.
        J+=min(delta,delta*delta/(4*m)) if m else delta
        if delta and not m:used_linear+=1
    moved=sum(transfers.values(),F(0))
    balanced=sum(abs(incoming[b]-outgoing[b]) for b in labels)/2
    assert balanced<=moved and sum(means0.values())==sum(means1.values())
    # For equal total intensity a shared Poisson residual population of mean balanced
    # can be marked separately under the two laws. Disagreement <=1-exp(-balanced).
    tv_void=void_bounds(balanced)[1] if balanced<=1 else F(1)
    tv_hellinger=sqrt_bounds(J)[1]
    return dict(tv_upper=outward(min(F(1),tv_void,tv_hellinger))[1],
        squared_root_distance_upper=outward(J)[1],
        total_transfer_mean=str(moved),uncancelled_transfer_mean=str(balanced),
        zero_background_nonzero_difference_labels=used_linear)

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    w,_=inputs();old=read(HERE.parent/'shape_coupling'/'summary.json')
    selected=old['selected'];M=constant(w)*F(selected['step'])
    assert 0<M<=F(1,4)
    lo,hi=void_bounds(M)
    assert hi<F(selected['tv_upper'])
    atoms=read(HERE.parent/'joint_atoms'/'partitions.json.gz')[-1]
    keys=[set(g['atom_integer_volumes']) for g in atoms['geometries']]
    assert keys[0]==keys[1]
    result=dict(status='SHARPER_SAME_PAIR_COUPLING_CERTIFIED',
        unchanged_pair=dict(node=selected['node'],axis=selected['axis'],sign=selected['sign'],step=selected['step']),
        changed_region_mean_upper=str(M),previous_linear_tv_upper=selected['tv_upper'],
        poisson_void_at_mean_upper=outward(lo,hi),tv_upper=outward(hi)[1],
        relative_reduction_of_certified_upper_bound=outward(1-hi/M,1-lo/M),
        symmetric_operator_gap=selected['relative'],strong_pair_found=False,
        optimal_equal_prior_accuracy_upper=outward((1+hi)/2)[1],
        error_probability_at_half_gap_lower=outward((1-hi)/2)[0],
        paired_atom_status='HOLD_TRANSFER_LOCALIZATION',
        common_certified_positive_labels=len(keys[0]),
        scope='The numerical gain comes entirely from retaining the exponential already proved in PR95. No sharper geometry integration or measured TV. Positive atom lower volumes alone do not locate the transferred mass; no additional atom smoothing gain is claimed.')
    return result

if __name__=='__main__':
    result=run()
    if '--verify' in sys.argv:assert result==read(HERE/'summary.json')
    else:save(HERE/'summary.json',result)
    print(__import__('json').dumps(result))
