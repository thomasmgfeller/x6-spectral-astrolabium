"""Independent DESI DR2 BAO fit: python desi_gegenprobe.py MEAN.txt COV.txt"""

import argparse
import json
import math

import numpy as np
from scipy.integrate import quad
from scipy.linalg import cholesky, solve_triangular
from scipy.optimize import least_squares


def distance_ratios(omega_m, h_rd_mpc, redshifts, observables):
    # Late-time flat Lambda-CDM with matter and a cosmological constant.
    def inv_e(z):
        return 1.0 / math.sqrt(1.0 + omega_m * ((1.0 + z) ** 3 - 1.0))

    scale = 299792.458 / (100.0 * h_rd_mpc)
    predictions = []
    for z, observable in zip(redshifts, observables, strict=True):
        dm = scale * quad(inv_e, 0.0, z, epsabs=1e-12, epsrel=1e-12)[0]
        dh = scale * inv_e(z)
        dv = (z * dh * dm**2) ** (1.0 / 3.0)
        predictions.append({"DM_over_rs": dm, "DH_over_rs": dh, "DV_over_rs": dv}[observable])
    return np.array(predictions)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mean")
    parser.add_argument("covariance")
    args = parser.parse_args()
    z, observed, observable = np.loadtxt(
        args.mean, dtype=[("z", "f8"), ("obs", "f8"), ("tag", "U16")], unpack=True
    )
    covariance = np.loadtxt(args.covariance)
    if len(z) != 13 or covariance.shape != (13, 13):
        raise ValueError("Expected all 13 DESI DR2 BAO distances and their 13x13 covariance.")
    np.testing.assert_allclose(covariance, covariance.T, rtol=1e-12, atol=0.0)
    factor = cholesky(covariance, lower=True)

    def residual(parameters):
        model = distance_ratios(*parameters, z, observable)
        return solve_triangular(factor, observed - model, lower=True)

    result = least_squares(
        residual, (0.3, 100.0), bounds=((0.01, 20.0), (0.99, 200.0)),
        jac="3-point", x_scale="jac", ftol=1e-13, xtol=1e-13, gtol=1e-13,
    )
    if not result.success or np.any(result.active_mask):
        raise RuntimeError(result.message)
    # Published posterior summaries and correlation from DESI DR2 II, Eq. (17).
    offsets = (result.x - [0.2975, 101.54]) / [0.0086, 0.73]
    correlation = np.array([[1.0, -0.92], [-0.92, 1.0]])
    published_distance = np.linalg.norm(solve_triangular(cholesky(correlation, lower=True), offsets, lower=True))
    print(json.dumps({
        "omega_m": result.x[0], "h_rd_Mpc": result.x[1],
        "chi2_min": float(result.fun @ result.fun), "degrees_of_freedom": len(z) - len(result.x),
        "offset_in_reported_marginal_sigmas": offsets.tolist(),
        "mahalanobis_to_eq17": float(published_distance),
        "eq17_plausibility_threshold": 0.5,
        "eq17_plausibility_pass": bool(published_distance <= 0.5),
    }, indent=2))


if __name__ == "__main__":
    main()
