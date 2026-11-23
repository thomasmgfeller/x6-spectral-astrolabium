"""Uniform bounds on both full clock packets; only the Python standard library."""
from fractions import Fraction as Q
from hashlib import sha256
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'quellen'))
from intervalle import I, S
from modell import EDGES, ORDER


def bound(lo, hi):
    return I(I.of(lo).lo, I.of(hi).hi)


def mag(a):
    return Q(a.absmax(), S)


def check_sources():
    meta = json.loads((ROOT / 'herkunft.json').read_text())
    for name, row in meta['files'].items():
        assert sha256((ROOT / 'quellen' / name).read_bytes()).hexdigest() == row['sha256']
    p3 = json.loads((ROOT / 'quellen/p3.json').read_text())
    assert len(p3) == 60 and all(row['checkpoint_id'] == 'P3' and row['execution'] == 'NOT_RUN' for row in p3)
    assert EDGES[5,11] == -9 and EDGES[5,12] == 16 and EDGES[5,13] == -8
    assert ORDER[ORDER.index(11)-3:ORDER.index(11)+1] == (4,5,6,11)


def certify():
    k, h = I.of(Q(15,4)), Q(1,16384)
    duration = k * I.of(Q(3,722)).sqrt().sqrt()
    displacement = 1/(72*duration*k*k) + h
    rho = Q(displacement.hi,S)
    u = bound(Q(1,4)-rho,Q(1,4)+rho)
    z = bound(Q(1,8)-Q(1,64),Q(1,8)+Q(1,64))
    v = bound(Q(1,2)-Q(1,64),Q(1,2)+Q(1,64))
    x = bound(Q(255,2048)-h,Q(257,2048)+h)
    y = {j:I.of(j-5) for j in (0,1,2,3)}
    y[3] += Q(1,4)
    y.update({j:y[3]+k*a for j,a in ((4,z),(5,u),(6,Q(3,8)),(11,v))})
    # f4,f5,f6 are the three already closed cells.
    f = {4:(z+u)/2, 5:(I.of(Q(3,8))-z)/2, 6:(v-u)/2}
    df = {4:Q(1,2), 5:Q(0), 6:Q(-1,2)}
    c = {j:I.of(Q(-1,2)) for j in (4,5,6,11)}
    dc = {j:I.of(0) for j in c}
    for (i,j),b in EDGES.items():
        if j in c:
            gap = y[j]-y[i]
            c[j] -= gap**2 * Q(b,38)
            dc[j] -= gap*k*Q(b,19)*(int(j==5)-int(i==5))
    log_vol_derivative = I.of(0)
    phase_derivative = duration*x*dc[11]
    sinc_bound = Q(0)
    max_arg = Q(0)
    for j in (4,5,6):
        assert f[j].lo>0
        log_vol_derivative += I.of(df[j])/f[j]
        phase_derivative += duration*(df[j]*c[j]+f[j]*dc[j])
        arg = duration*f[j]*c[j]/100
        da = duration*(df[j]*c[j]+f[j]*dc[j])/100
        max_arg = max(max_arg,mag(arg))
        assert mag(arg)<1
        sinc_bound += mag(arg)*mag(da)/(3*(1-mag(arg)**2/6))
    derivative_bound = mag(log_vol_derivative)+sinc_bound+mag(phase_derivative)
    # |L/L0 - 1| <= exp(rho*bound)-1 <= q/(1-q).
    q = derivative_bound*rho
    assert q<1
    eta = q/(1-q)
    pointwise_real_lower = 1-2*eta-eta**2
    assert pointwise_real_lower>0
    corr_squared_lower = 1-(2*eta/(1-eta))**2
    corr_lower = Q(I.of(corr_squared_lower).sqrt().lo,S)
    # Round only outward to human-readable rational limits.
    def up(value, decimals):
        n=10**decimals
        return str(Q(-(-value*n).__floor__(),n))
    def down(value, decimals):
        n=10**decimals
        return str(Q((value*n).__floor__(),n))
    # Follow-up on a single admissible continuation with u11=1/2, u12=5/8.
    d = 1/(36*duration*k*k)
    a12 = Q(16,38)*duration*k*k/8
    phase_spread = mag(a12)*(Q(3,4)*rho+rho**2)
    min_gap = (1-2*h/Q(d.lo,S))/912
    max_gap = (1+2*h/Q(d.lo,S))/912
    assert min_gap>0 and max_gap<1
    half = min_gap/2
    determinant_lower = 2*(half-half**3/6)*(1-2*eta-eta**2-phase_spread)
    assert determinant_lower>Q(1,1000)
    return dict(continuation_center_phase_gap='1/912',
                continuation_relative_determinant_lower=down(determinant_lower,9),
                packet_radius_upper=up(rho,12),sinc_argument_abs_upper=up(max_arg,7),
                log_derivative_abs_upper=up(derivative_bound,7),
                amplitude_disk_radius_upper=up(eta,9),
                shared_real_cross_over_reference_lower=down(pointwise_real_lower,8),
                normalized_overlap_lower=down(corr_lower,9),
                best_scalar_isometry_defect_lower=down(corr_lower,9),
                max_kept_fraction_equiprobable_arms_upper=up(1/(1+corr_lower),9),
                early_memory=[4,5,6,11],future_pairs_of_clock5=[[12,16],[13,-8]],
                physical_P3_NOT_RUN=60)


if __name__ == '__main__':
    check_sources()
    print(json.dumps(certify(),indent=2))
