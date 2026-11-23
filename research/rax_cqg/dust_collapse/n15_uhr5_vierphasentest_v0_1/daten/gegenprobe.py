"""Independent distance integrator and simultaneous unprojected three-parameter fit."""
import argparse
import json

from datenpilot import ROOT, inputs
import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import solve_triangular
from scipy.optimize import least_squares
from pathlib import Path


def run(cache, reference):
    files = inputs(cache)
    with files['desi_gaussian_bao_ALL_GCcomb_mean.txt'].open() as stream:
        data = np.genfromtxt(stream, dtype=[('z','f8'),('value','f8'),('type','U12')])
    bao_cov = np.loadtxt(files['desi_gaussian_bao_ALL_GCcomb_cov.txt'])
    bao_chol = np.linalg.cholesky(bao_cov)
    sn = np.genfromtxt(files['Pantheon+SH0ES.dat'], names=True, dtype=None, encoding='utf8')
    selected = np.flatnonzero(sn['zHD'] > 0.01)
    full_cov = np.loadtxt(files['Pantheon+SH0ES_STAT+SYS.cov'])
    matrix = full_cov[1:].reshape(int(full_cov[0]), int(full_cov[0]))
    sn_chol = np.linalg.cholesky(matrix[np.ix_(selected,selected)])
    sn = sn[selected]
    z_max = max(data['z'].max(), sn['zHD'].max())

    def residuals(parameters):
        om, scale, offset = parameters

        def hubble(z):
            return np.sqrt(om * (1+z)**3 + (1-om))

        distance = solve_ivp(lambda z, y: [1/hubble(z)], (0,z_max), [0.], method='DOP853',
                             dense_output=True, rtol=1e-12, atol=1e-14)
        if not distance.success:
            raise ArithmeticError(distance.message)
        prediction = []
        for z, obs, tag in data:
            comoving = distance.sol(z).item()
            radial = 1/hubble(z)
            dimless = {'DV_over_rs':(z * comoving**2 * radial)**(1/3),
                       'DH_over_rs':radial, 'DM_over_rs':comoving}[tag]
            prediction.append(299792.458/(100*scale) * dimless)
        bao_residual = solve_triangular(bao_chol, data['value'] - prediction, lower=True)
        sn_prediction = offset + 5*np.log10((1+sn['zHEL']) * distance.sol(sn['zHD']).ravel())
        sn_residual = solve_triangular(sn_chol, sn['m_b_corr'] - sn_prediction, lower=True)
        return np.concatenate((bao_residual, sn_residual))

    fit = least_squares(residuals, [.30,100.,23.], bounds=([.01,10.,-np.inf],[.99,1000.,np.inf]),
                        jac='3-point', diff_step=1e-4, ftol=1e-13, xtol=1e-13, gtol=1e-13)
    if not fit.success:
        raise ArithmeticError(fit.message)
    best = reference['posteriors']['DESI_DR2_plus_PantheonPlus']['best_fit']
    delta = dict(omega_m=float(fit.x[0]-best['omega_m']),
                 h_rd_Mpc=float(fit.x[1]-best['h_rd_Mpc']),
                 chi2=float(2*fit.cost-best['chi2_min']))
    if abs(delta['omega_m']) > 1e-7 or abs(delta['h_rd_Mpc']) > 1e-5 or abs(delta['chi2']) > 1e-6:
        raise ArithmeticError(f'Independent fit differs: {delta}')
    return dict(omega_m=float(fit.x[0]), h_rd_Mpc=float(fit.x[1]),
                dimensionless_distance_magnitude_offset=float(fit.x[2]),
                chi2_min=float(2*fit.cost), difference_from_primary_fit=delta)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache', type=Path, default=ROOT/'cache')
    parser.add_argument('--reference', type=Path, default=ROOT/'ergebnis.json')
    parser.add_argument('--output', type=Path, default=ROOT/'gegenprobe.json')
    args = parser.parse_args()
    result = run(args.cache,json.loads(args.reference.read_text()))
    output = json.dumps(result,indent=2,allow_nan=False)+'\n'
    args.output.write_text(output,encoding='utf-8')
    print(output,end='')
