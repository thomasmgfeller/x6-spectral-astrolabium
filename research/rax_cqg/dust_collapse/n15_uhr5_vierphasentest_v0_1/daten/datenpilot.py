"""Uncalibrated late-time flat-LambdaCDM reference fits, with pinned inputs."""
import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path
from urllib.request import urlopen

# Use a single BLAS thread by default to keep these small batches inexpensive.
os.environ['OPENBLAS_NUM_THREADS'] = os.environ.get('PILOT_THREADS', '1')
os.environ['MKL_NUM_THREADS'] = os.environ.get('PILOT_THREADS', '1')

import numpy as np
import scipy
from numpy.polynomial.legendre import leggauss
from scipy.linalg import solve_triangular
from scipy.optimize import minimize_scalar

ROOT = Path(__file__).resolve().parent
C_OVER_100 = 2997.92458  # Mpc, c / (100 km s^-1 Mpc^-1)
OMEGA_BINS = [0.01, .15, .225, .275, .325, .375, .43, .55, .75, .99]
SCALE_BINS = [10, 75, 87, 91, 94, 97, 100, 103, 106, 109, 112, 115, 120, 130, 170, 1000]
DISTANCE_NODES, DISTANCE_WEIGHTS = leggauss(32)


def inputs(cache):
    cache.mkdir(parents=True, exist_ok=True)
    files = {}
    for item in json.loads((ROOT / 'quelldaten.json').read_text()):
        name = item['file']
        path = cache / name
        if not path.exists():
            # Accept the filenames used by the project's earlier data audit.
            revision = item['url'].split('/')[5]
            audited = cache / f'{revision[:10]}_{name}'
            if audited.exists():
                path = audited
        if path.exists():
            with path.open('rb') as stream:
                digest = hashlib.file_digest(stream, 'sha256').hexdigest()
            if digest != item['sha256']:
                raise ValueError(f'SHA-256 mismatch in {path}')
        else:
            with tempfile.NamedTemporaryFile(dir=cache, delete=False) as temp:
                temporary_path = Path(temp.name)
            try:
                with urlopen(item['url'], timeout=120) as response, temporary_path.open('wb') as out:
                    while block := response.read(1024 * 1024):
                        out.write(block)
                with temporary_path.open('rb') as stream:
                    digest = hashlib.file_digest(stream, 'sha256').hexdigest()
                if digest != item['sha256']:
                    raise ValueError(f'SHA-256 mismatch for download {name}')
                temporary_path.replace(path)
            finally:
                temporary_path.unlink(missing_ok=True)
        files[name] = path
    return files


def inv_expansion(z, om, radiation):
    return (1 + om * ((1 + z)**3 - 1) + radiation * ((1 + z)**4 - 1))**-.5


class Distance:
    def __init__(self, z):
        self.z = z
        self.nodes = (DISTANCE_NODES + 1) * z[:, None] / 2

    def comoving(self, om, radiation):
        # Axes for inv_expansion: redshift, integration node, matter fraction.
        e_inv = inv_expansion(self.nodes[:, :, None], om, radiation)
        return self.z[:, None] / 2 * np.einsum('ijk,j->ik', e_inv, DISTANCE_WEIGHTS)


class BAO:
    def __init__(self, files):
        basename = 'desi_gaussian_bao_ALL_GCcomb_'
        with files[basename+'mean.txt'].open() as src:
            records = [line.split() for line in src if line.strip() and not line.startswith('#')]
        self.z = np.array([float(row[0]) for row in records])
        self.distance = Distance(self.z)
        self.tag = np.array([row[2] for row in records])
        if set(self.tag) != {'DM_over_rs','DH_over_rs','DV_over_rs'}:
            raise ValueError('Unexpected DESI observable labels')
        cov = np.loadtxt(files[basename+'cov.txt'])
        if cov.shape != (len(records),len(records)) or not np.array_equal(cov, cov.T):
            raise ValueError('Unexpected DESI covariance')
        self.chol = np.linalg.cholesky(cov)
        self.obs = solve_triangular(self.chol, [float(row[1]) for row in records], lower=True)

    def profile(self, om, radiation):
        dm = self.distance.comoving(om, radiation)
        dh = inv_expansion(self.z[:, None], om, radiation)
        dv = np.cbrt(self.z[:, None] * dm**2 * dh)
        distances = np.select([self.tag[:, None] == 'DM_over_rs',self.tag[:, None] == 'DH_over_rs'],[dm,dh],default=dv)
        model = solve_triangular(self.chol, C_OVER_100 * distances, lower=True)
        curvature = np.sum(model**2, axis=0)
        inv_scale = (self.obs @ model) / curvature
        residual = self.obs[:, None] - model * inv_scale
        return np.sum(residual**2, axis=0), inv_scale, curvature


class Pantheon:
    def __init__(self, files):
        row = np.genfromtxt(files['Pantheon+SH0ES.dat'], names=True, dtype=None, encoding='utf8')
        mask = row['zHD'] > .01
        self.n_total = len(row)
        self.n = int(mask.sum())
        self.n_flagged = int(row['IS_CALIBRATOR'][mask].sum())
        self.distance = Distance(row['zHD'][mask])
        self.zhel = row['zHEL'][mask]
        self.obs = row['m_b_corr'][mask]
        with files['Pantheon+SH0ES_STAT+SYS.cov'].open() as src:
            if int(src.readline()) != len(row):
                raise ValueError('Pantheon+ covariance and data dimensions disagree')
            cov = np.loadtxt(src).reshape(len(row),len(row))[np.ix_(mask,mask)]
        self.max_asymmetry = float(np.max(abs(cov - cov.T)))
        if self.max_asymmetry > 4e-8:
            raise ValueError('Unexpected Pantheon+ covariance asymmetry')
        self.chol = np.linalg.cholesky((cov + cov.T)/2)
        self.ones = solve_triangular(self.chol,np.ones(self.n),lower=True)
        self.ones_norm2 = self.ones @ self.ones

    def profile(self, om, radiation):
        # Magnitude offset absorbs both M and the absolute distance scale.
        luminosity = (1 + self.zhel[:, None]) * self.distance.comoving(om,radiation)
        residual = self.obs[:, None] - 5 * np.log10(luminosity)
        white = solve_triangular(self.chol,residual,lower=True)
        offset = (self.ones @ white) / self.ones_norm2
        projected = white - self.ones[:, None] * offset
        return np.sum(projected**2,axis=0)


def quadrature(bins, n):
    node, weight = leggauss(n)
    low, high = np.array(bins[:-1])[:,None], np.array(bins[1:])[:,None]
    return ((low+high + (high-low)*node)/2).ravel(), ((high-low)*weight/2).ravel()


def summary(om, wo, scale, ws, chi):
    mass = np.exp(-.5 * (chi - np.min(chi))) * wo[:,None] * ws
    mass /= mass.sum()
    om_mean = np.sum(mass * om[:,None])
    scale_mean = np.sum(mass * scale)
    do, ds = om[:,None] - om_mean, scale - scale_mean
    om_sd = np.sqrt(np.sum(mass * do**2))
    scale_sd = np.sqrt(np.sum(mass * ds**2))
    return dict(omega_m_mean=om_mean, omega_m_sd=om_sd, h_rd_mean_Mpc=scale_mean,
                h_rd_sd_Mpc=scale_sd, correlation=np.sum(mass*do*ds)/(om_sd*scale_sd))


def posteriors(bao, sn, n, radiation, only_bao=False):
    om, wo = quadrature(OMEGA_BINS,n)
    scale, ws = quadrature(SCALE_BINS,n)
    profile, inv_scale, curvature = bao.profile(om,radiation)
    chi = profile[:,None] + curvature[:,None] * (1/scale - inv_scale[:,None])**2
    result = {'DESI_DR2': summary(om,wo,scale,ws,chi)}
    if not only_bao:
        sn_chi = np.concatenate([sn.profile(om[i:i+16],radiation) for i in range(0,len(om),16)])
        mass = np.exp(-.5 * (sn_chi - sn_chi.min())) * wo
        mass /= mass.sum()
        mean = mass @ om
        result['PantheonPlus'] = dict(omega_m_mean=mean, omega_m_sd=np.sqrt(mass @ (om-mean)**2))
        result['DESI_DR2_plus_PantheonPlus'] = summary(om,wo,scale,ws,chi + sn_chi[:,None])
    return result


def best_fit(bao, sn, use_bao, use_sn):
    def parameters(x):
        om = np.atleast_1d(x)
        chi = 0.
        out = {'omega_m': float(x)}
        if use_bao:
            base, inv_scale, _ = bao.profile(om,0.)
            chi += base.item()
            out.update(h_rd_Mpc=1/inv_scale.item(), chi2_bao=base.item())
        if use_sn:
            value = sn.profile(om,0.).item()
            chi += value
            out.update(chi2_sn=value)
        return dict(**out, chi2_min=chi)
    opt = minimize_scalar(lambda x: parameters(x)['chi2_min'], bounds=(.01,.99), method='bounded', options={'xatol':1e-11})
    if not opt.success:
        raise RuntimeError(opt.message)
    out = parameters(opt.x)
    out['nominal_dof'] = (len(bao.z)-1 if use_bao else 0) + (sn.n-1 if use_sn else 0) - 1
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cache',type=Path,default=ROOT/'cache')
    parser.add_argument('--output',type=Path,default=ROOT/'ergebnis.json')
    args = parser.parse_args()
    files = inputs(args.cache)
    bao = BAO(files)
    sn = Pantheon(files)
    fine = posteriors(bao,sn,40,0.)
    coarse = posteriors(bao,sn,24,0.)
    difference = {name: {key: abs(val-coarse[name][key]) for key,val in values.items()} for name, values in fine.items()}
    if max(value for group in difference.values() for value in group.values()) > 1e-6:
        raise ArithmeticError(f'Quadrature has not converged: {difference}')
    reference = {'omega_m_mean':.2975,'omega_m_sd':.0086,'h_rd_mean_Mpc':101.54,'h_rd_sd_Mpc':.73,'correlation':-.92}
    radiation = posteriors(bao,sn,40,9e-5,only_bao=True)['DESI_DR2']
    for name,use_bao,use_sn in [('DESI_DR2',True,False),('PantheonPlus',False,True),('DESI_DR2_plus_PantheonPlus',True,True)]:
        fine[name]['best_fit'] = best_fit(bao,sn,use_bao,use_sn)
    result = dict(software={'numpy':np.__version__,'scipy':scipy.__version__},
                  parameters={'omega_r':0,'prior_omega_m':[.01,.99], 'prior_h_rd_Mpc':[10,1000], 'prior_measure':'uniform in Omega_m and h*r_d'},
                  inputs={'bao_data_points':len(bao.z),'pantheon_rows':sn.n_total,'pantheon_after_zHD_gt_0.01':sn.n,'flagged_in_selection_without_Cepheid_anchor':sn.n_flagged,'max_cov_asymmetry_selected_mag2':sn.max_asymmetry},
                  posteriors=fine, abs_change_quadrature_24_to_40=difference,
                  reference_DESI_eq17=reference,
                  DESI_minus_eq17={k:fine['DESI_DR2'][k]-v for k,v in reference.items()},
                  DESI_with_fixed_omega_r_0_00009=radiation)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(fine,indent=2))


if __name__ == '__main__':
    main()
