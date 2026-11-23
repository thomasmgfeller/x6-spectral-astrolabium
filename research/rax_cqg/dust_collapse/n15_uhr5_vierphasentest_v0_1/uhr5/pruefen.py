"""Exact action and four-phase controls. Run with Python 3.10+ and NumPy."""
import json
import sys
from fractions import Fraction as Q
from itertools import product
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "quellen"))
from modell import EDGES, INNER_MEANS, ORDER, clocks, coefficients, dwell

K = Q(15, 4)
H = Q(1, 16384)
DX = Q(1, 1024)
PHASES = np.array([1, 1j, -1, -1j])


def action_check():
    assert EDGES[5, 11] == -9
    early = ORDER[:ORDER.index(11) + 1]
    tests = 0
    for offset, u_a, u_b in product((Q(-1,100), Q(0), Q(1,100)),
                                   (Q(249,1000), Q(250,1000)),
                                   (Q(251,1000), Q(252,1000))):
        vals = []
        for u in (u_a, u_b):
            inner = INNER_MEANS.copy()
            inner[0] += offset
            inner[1] = u
            y = clocks(Q(1,4), inner)
            f = dwell(inner)
            # Compute S/D from all early pairs and all earlier densities in their cells.
            both = []
            for sign in (-1, 1):
                x = {j: f.get(j, Q(1,8)) for j in early}
                x[11] = Q(1,8) + sign * DX / 2
                assert abs(x[11] / f[11] - 1) < Q(1,100)
                both.append(-sum(x.values())/2 - sum(
                    b*x[j]*(y[j]-y[i])**2/38 for (i,j), b in EDGES.items()
                    if j in early
                ))
            vals.append(both[1] - both[0])
            assert vals[-1] == DX * coefficients(y)[11]
        expected = Q(9,38)*K**2*DX*((Q(1,2)-u_a)**2-(Q(1,2)-u_b)**2)
        assert vals[0]-vals[1] == expected
        tests += 1
    # d^4 = 1 / (36^4 K^12 Delta^4), so this bracket is exact.
    d_fourth = Q(722,3) / (36**4 * K**12)
    d_lo, d_hi = Q(2074711344,10**12), Q(2074711345,10**12)
    assert 0 < 2*H < d_lo and d_lo**4 < d_fourth < d_hi**4
    center = Q(9,38) * DX * Q(1,36) / 2
    assert center == Q(1,311296)
    lo = center * (1-2*H/d_lo)
    hi = center * (1+2*H/d_lo)
    outer = Q(3023369,10**12), Q(3401385,10**12)
    assert outer[0] < lo < center < hi < outer[1]
    return dict(action_mixed_difference_exact_checks=tests, pair_weight=EDGES[5,11],
                x_centers=['255/2048','257/2048'], center_gap_rad=str(center),
                cross_packet_angle_bounds_rad=[str(x) for x in outer])


def four_phase(gram, effect):
    for operator in (gram, effect, gram-effect):
        assert np.allclose(operator,operator.conj().T)
        assert np.linalg.eigvalsh(operator)[0] >= -1e-14
    states = np.stack([np.ones(4), PHASES], axis=1)/np.sqrt(2)
    def weights(form):
        return np.einsum('ij,jk,ik->i',states.conj(),form,states).real
    norms, raw = weights(gram), weights(effect)
    assert np.all(norms > 0)
    p = raw/norms
    def extract(xs):
        return ((xs[0]-xs[2])-1j*(xs[1]-xs[3]))/2
    for xs, expected in [(norms,gram[0,1]),(p*norms,effect[0,1])]:
        np.testing.assert_allclose(extract(xs),expected,atol=1e-14)
    corrected = extract(p*norms)
    return {'norms':norms.tolist(),'probabilities':p.tolist(),
            'uncorrected_abs':float(abs(extract(p))),
            'corrected_real_imag':[float(corrected.real),float(corrected.imag)]}


def control_checks():
    identity = np.eye(2)
    g = np.array([[1.,.5],[.5,1.]])
    diagonal = np.diag([.5,0.])
    # Real and imaginary quadratures, independent of the action.
    probe = np.array([[.5,(1+1j)/8],[(1-1j)/8,.5]])
    controls = {'orthogonal_support_readout':four_phase(identity,np.diag([1.,0.])),
                'positive_test_instrument':four_phase(identity,probe),
                'normalization_artifact':four_phase(g,diagonal),
                'constant_probability_half':four_phase(g,g/2)}
    np.testing.assert_allclose(controls['normalization_artifact']['probabilities'],[1/6,1/4,1/2,1/4])
    np.testing.assert_allclose(controls['positive_test_instrument']['probabilities'],[5/8,3/8,3/8,5/8])
    # The two actual center phases, up to a common phase. Allow the outgoing
    # metric to depend on the density: the same positive incoming cross term survives.
    k = float(K); d_k2 = k**3*(3/722)**.25
    d = 1/(36*d_k2)
    u = np.array([.25-d/2,.25+d/2])
    outgoing = []
    for x in (255/2048,257/2048):
        unitary = np.diag(np.exp(1j*9/38*d_k2*x*(.5-u)**2))
        native_cut = unitary.conj().T @ np.diag([1.,0.]) @ unitary
        np.testing.assert_allclose(four_phase(identity,native_cut)['probabilities'],
                                   [.5,.5,.5,.5],atol=1e-14,rtol=0)
        choice = unitary @ g @ unitary.conj().T
        np.testing.assert_allclose(unitary.conj().T@choice@unitary,g,atol=1e-14,rtol=0)
        outgoing.append(choice)
    delta = abs(outgoing[0][0,1]-outgoing[1][0,1])
    np.testing.assert_allclose(delta,np.sin(1/(2*311296)),rtol=1e-9)
    # Same two conditional scalars on each arm give a complete instrument for any G.
    # A sharp support readout fails completeness precisely by G's two off-diagonals.
    for coefficients in ([np.array([.6,.8j]), np.array([.6,.8j])],
                         [np.array([1.,0.]), np.array([0.,1.])]):
        a,b = coefficients
        kraus = [np.diag(column) for column in zip(a,b)]
        total = sum(op.conj().T@g@op for op in kraus)
        np.testing.assert_allclose(1 - (total[0,1]/g[0,1]).real,
                                   np.linalg.norm(a-b)**2/2, atol=1e-14)
        if np.array_equal(a,b):
            np.testing.assert_allclose(total,g,atol=1e-14)
        else:
            np.testing.assert_allclose(total,identity,atol=1e-14)
    return controls, float(delta)


def main():
    records = json.loads((HERE/'quellen/p3.json').read_text())
    assert len(records)==60 and all(r['checkpoint_id']=='P3' and r['execution']=='NOT_RUN' for r in records)
    controls, delta = control_checks()
    result = {'action':action_check(),'four_phase_controls':controls,
              'density_dependent_outgoing_gram_center_difference_abs':delta,
              'two_center_residual_gain':float(1/(2*np.sin(1/(2*311296)))),
              'two_center_residual_sum_for_one_percent':float(.02*np.sin(1/(2*311296))),
              'physical_early_effect':'HOLD', 'physical_four_phase_probabilities':'NOT_RUN',
              'physical_positive_mass_calibration':'HOLD','P3_NOT_RUN':len(records)}
    print(json.dumps(result,indent=2,allow_nan=False))


if __name__ == '__main__':
    main()
