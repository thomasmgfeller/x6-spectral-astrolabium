"""Frozen summaries and decision rules; scientific non-passes are retained."""
from math import comb
import numpy as np
from scipy.stats import t as student_t
from core import coefficients, de_sitter_slope, flat_probability


def interval(samples, comparisons):
    x = np.asarray(samples)
    se = x.std(axis=0,ddof=1)/np.sqrt(len(x))
    radius = student_t.ppf(1-.01/(2*comparisons),len(x)-1)*se
    mean = x.mean(axis=0)
    return mean, se, mean-radius, mean+radius


def summarize(data, contract, geometry, quadrature):
    p = np.array([flat_probability(4,k) for k in [2,3,4]])
    b = np.array([float(de_sitter_slope(k)) for k in [2,3,4]])
    mean,se,lo,hi = interval(data['importance_slopes'],21)
    margin = contract['importance']['slope_relative_equivalence_margin']
    slope_pass = bool(np.all(lo[0] >= b*(1-margin)) and np.all(hi[0] <= b*(1+margin)))
    importance = []
    for i,h in enumerate([0.]+contract['importance']['h']):
        importance.append(dict(h=h,kind='analytic_h2_derivative' if i==0 else 'paired_finite_h_response',
                               mean=mean[i].tolist(),standard_error=se[i].tolist(),
                               interval99_family= np.column_stack((lo[i],hi[i])).tolist(),
                               relative_to_rss=(mean[i]/b).tolist()))
    matrix = np.array([[float(v) for v in coefficients(4,k)[2:]] for k in [2,3]])
    direct = []
    for ci,(n,h,geo) in enumerate(geometry):
        counts = data['direct_counts'][ci]
        f = counts/np.array([comb(n,k) for k in [2,3,4]])
        avg,err,lower,upper = interval(f,8)
        cov = np.cov(f,rowvar=False,ddof=1)
        corr = cov/np.sqrt(np.outer(np.diag(cov),np.diag(cov)))
        inverse = np.linalg.solve(matrix,(f[:,:2]/p[:2]-1).T).T
        truth = np.array([geo['R_tau_squared'],-geo['R_tau_squared']/4])
        q = next(row['probabilities'][-1] for row in quadrature if row['h']==h)
        direct.append(dict(N=n,h=h,replicates=len(f),mean=avg.tolist(),standard_error=err.tolist(),
                           covariance=cov.tolist(),correlation=corr.tolist(),
                           C2_quadrature=q,C2_mean_interval99_family=[float(lower[0]),float(upper[0])],
                           C2_reference_in_interval=bool(lower[0] <= q <= upper[0]),
                           inverse=dict(target=truth.tolist(),mean=inverse.mean(axis=0).tolist(),
                                        bias=(inverse.mean(axis=0)-truth).tolist(),
                                        single_order_RMSE=np.sqrt(np.mean((inverse-truth)**2,axis=0)).tolist(),
                                        single_order_SD=inverse.std(axis=0,ddof=1).tolist(),
                                        scope='Exploratory linear inverse; correlated samples within each order, independent orders; no clipping or coverage claim')))
    quad_out=[]
    for row in quadrature:
        h=row['h']; values=row['probabilities']; geo=row['geometry']
        gap=max(abs(values[j]-values[j-1]) for j in range(1,len(values)))
        converged=gap<=contract['quadrature']['convergence_absolute_tolerance']
        predicted=.1*(1+float(b[0])*geo['R_tau_squared'])
        signal=values[-1]-.1
        remainder=None if h==0 else abs(values[-1]-predicted)/abs(signal)
        quad_out.append(dict(h=h,R_tau_squared=geo['R_tau_squared'],probabilities=values,
                             max_successive_gap=gap,converged=converged,leading_RSS=predicted,
                             relative_remainder_of_curvature_signal=remainder,
                             within_5percent_signal=bool(converged and h>0 and remainder<=.05)))
    return dict(schema='x6.rss-fixed-n.results/1',
                primary_slope_status='FORWARD_SLOPE_RESOLVED_WITH_APPROXIMATE_INTERVALS' if slope_pass else 'FORWARD_SLOPE_NOT_RESOLVED',
                primary_slope_pass=slope_pass,
                conditional_coefficients=[dict(k=k,alpha=str(coefficients(4,k)[0]),beta=str(coefficients(4,k)[1]),
                     A=str(coefficients(4,k)[2]),B=str(coefficients(4,k)[3]),de_sitter=str(de_sitter_slope(k))) for k in [2,3,4]],
                flat_probabilities=p.tolist(),rss_de_sitter_slopes=b.tolist(),importance=importance,
                quadrature=quad_out,direct=direct,
                linear_inverse_matrix=matrix.tolist(),linear_inverse_condition_number_2=float(np.linalg.cond(matrix)),
                scientific_scope='Conditional forward model; approximate MC intervals; de Sitter tests only one Ricci combination; no general curvature qualification',
                density_identifiability='NOT_IDENTIFIABLE_WITH_UNRESTRICTED_SAMPLING_DENSITY',
                total_independent_clouds=len(data['importance_slopes'])+int(np.prod(data['direct_counts'].shape[:2])))
