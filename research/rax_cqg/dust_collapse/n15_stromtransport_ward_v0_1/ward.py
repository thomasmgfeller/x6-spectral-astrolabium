"""Finite-source volume insertion, moving density faces, and pointer controls."""
import json
import sys

import numpy as np

from strom import B, K, PATHS, ROOT, ideals
sys.path.insert(0, str(ROOT/'basis_340'))
import gegenrechnung as model
from nachweis import phase_enclosure

I, P, F = model.I, model.P, model.F
M, DELTA, R = float(model.MASS), model.DELTA, model.RADIUS
IDS = [(5, 12, 13), (12, 13, 5), (13, 5, 12)]


def edge_rows(y, cut):
    coefficients = np.zeros_like(y)
    for (i, j), b in B.items():
        if b and i in cut and j not in cut:
            coefficients[:, j] += b*(y[:, i]-y[:, j])/(19*DELTA)
    return coefficients


def shift_rows(y, mask, matrix):
    # Recover dC_v/dtau from the unmodified global action polynomial.
    # Half of this derivative is the coefficient of -dS/dtau for a density w_v.
    step = 1/64
    shift = np.zeros(15)
    shift[list(mask)] = step/(2*DELTA)
    return (model.global_rows(y+shift, matrix)-model.global_rows(y-shift, matrix))/step


def fixed_packet_integrand(row, duration, x, fw):
    # Full normalized integral density at fixed e,u,z after analytic integration
    # over the collective old density and the seven independent xi coordinates.
    inner_row = row[:, I]*(M*duration[:, None])
    past = row[:, P].sum(axis=1)
    phase = past/8+row[:, F]@fw+np.sum(inner_row*x, axis=1)
    prefactor = (duration/(4.25*DELTA))**14*np.sinc(past/(32*np.pi))
    carrier = prefactor*np.exp(1j*phase)
    filters = np.sinc(inner_row*R/np.pi)
    return carrier, inner_row, filters


def face_integrand(y, c, duration, centre, fw):
    # For V = sum_v in I d/dT_v, the earlier-to-inner differences contribute
    # to V C_v. The other inner-to-inner differences are unchanged.
    vc = np.zeros_like(y)
    for v in K:
        for i in P:
            vc[:, v] += 2*B[i, v]*(y[:, v]-y[:, i])/(19*DELTA)
    carrier, inner_row, filters = fixed_packet_integrand(-c/2, duration, centre, fw)
    face = np.zeros(len(y), dtype=complex)
    for v, a, b in IDS:
        j = I.index(v)
        velocity_jump = 2*float(model.ref.COFACTOR_SCALE)*(vc[:, a]-vc[:, b])
        # Difference of upper/lower density-face phases divided by 2R*i.
        # sin(kR)/R is stable even for a very narrow box. Only the remaining
        # six xi integrals carry their volume filters on this face.
        face_pair = np.sin(inner_row[:, j]*R)/R
        other_faces = np.prod(np.delete(filters, j, axis=1), axis=1)
        face += velocity_jump*carrier*other_faces*face_pair
    return face


def run_level(inputs, futures, matrix):
    y, duration, dwell = model.clocks_and_dwell(inputs, PATHS)
    centres = model.packet_centres(model.global_rows(y, matrix), dwell)
    masks = {'anfang':set(P), 'zwischen':set(P+[4, 5, 6, 11]), 'ausgang':set(P+I)}
    sums = np.zeros(2, complex)
    worst = 0.
    arms = {key:[] for key in masks}
    for z in futures:
        y[:, F[1:]] = [3, 4, 5]+float(model.FUTURE_WIDTH)*z[:3]
        fw = 1/8+float(model.FUTURE_WIDTH)*z[3:]
        c = model.global_rows(y, matrix)
        carrier, _, filters = fixed_packet_integrand(-c/2, duration, centres[0], fw)
        # Difference of the two inner Euler insertions at the same fields in
        # integration coordinates. The unperturbed phase agrees pointwise.
        derivative = shift_rows(y, I, matrix)
        density_diff = M*duration[:, None]*(centres[0]-centres[1])
        volume = -0.5*np.sum(derivative[:, I]*density_diff, axis=1)*carrier*filters.prod(axis=1)
        face = face_integrand(y, c, duration, centres[0], fw)
        sums += [np.mean(volume), np.mean(face)]
        worst = max(worst, float(np.max(abs(volume-face))))
        for key, cut in masks.items():
            p = edge_rows(y, cut)
            channels = [model.density_integrals(-c/2+lam*p, duration, centres, fw)
                        for lam in (0,1)]
            arms[key].append(np.array(channels).T)
    sums /= len(futures)
    return {'euler_volumen_re_im':[float(sums[0].real), float(sums[0].imag)],
            'paketrand_re_im':[float(sums[1].real), float(sums[1].imag)],
            'differenz_abs':float(abs(sums[0]-sums[1])),
            'max_abs_bei_festen_uhren_und_z':worst,
            'zeiger_Yplus':{k:model.matrices(np.array(v))[1].tolist() for k,v in arms.items()}}


def audit():
    config = json.loads((ROOT/'pruefvertrag.json').read_text())['numerik']
    matrix = np.zeros((15,15), int)
    for edge,b in B.items():
        matrix[edge] = b
    # Read the phase certificate directly from the original action verifier.
    # Together with the separately certified initial charge gap >1/320, this
    # implies Re(E+ - E-)/packet volume > 1/400 pointwise on the future box.
    from fractions import Fraction as Q
    phase = phase_enclosure(PATHS, B)
    assert -Q(5, 8) < phase[0] < phase[1] < 0 and 1-Q(5,8)**2/2 > Q(4,5)

    # All cuts checked separately on the original global polynomial with
    # independent rational-coefficient edge sums, including future sources.
    probes = model.sobol(8,64,9127)
    y, _, _ = model.clocks_and_dwell(probes, PATHS)
    zs = model.sobol(7,64,12341)
    y[:, F[1:]] += float(model.FUTURE_WIDTH)*zs[:, :3]
    max_row_difference = 0.
    for cut in ideals():
        discrepancy = np.max(np.abs(shift_rows(y, cut, matrix)/2-edge_rows(y, cut)))
        max_row_difference = max(max_row_difference, float(discrepancy))
    assert max_row_difference < 1e-10
    stages = []
    for si, sz in config['sobol_seeds']:
        n,m = config['stufen'][-1]
        points, future = model.sobol(8,n,si), model.sobol(7,m,sz)
        for n,m in config['stufen']:
            result = run_level(points[:n], future[:m], matrix)
            assert result['max_abs_bei_festen_uhren_und_z'] < 1e-10
            probabilities = result['zeiger_Yplus']
            assert abs(probabilities['ausgang'][0]-probabilities['ausgang'][1]) < 1e-12
            assert abs(probabilities['anfang'][0]-0.500940513261159) < 1e-9
            assert abs(probabilities['anfang'][1]-0.4993390916398255) < 1e-9
            stages.append(dict(saat=[si,sz], innen=n, aussen=m, **result))
    return {'max_differenz_native_wirkungsableitung_alle_20_schnitte':max_row_difference,
            'ward_kontrast_re_durch_paketmass_strikt_groesser':'1/400',
            'gemeinsame_normierung':'Volumenreferenz von PR 340, gemeinsamer Skalarfaktor und F4 ausgeklammert, normiertes flaches Zukunftsmass.',
            'stufen':stages}


if __name__ == '__main__':
    if not __debug__:
        sys.exit('Bitte Python ohne -O verwenden.')
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
