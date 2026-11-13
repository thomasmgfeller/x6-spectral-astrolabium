#!/usr/bin/env python3
"""Certify analytic truncation decimals with rational exponential majorants.

This does not enclose floating-point quadrature evaluation or elementary functions.
The full-weight program is imported only for a few-point implementation comparison;
all interval coefficients and exact bounds are reconstructed independently here.
"""
from pathlib import Path
from fractions import Fraction as F
import importlib.util
import itertools
import json
import math
import mpmath as mp

OUT=Path(__file__).resolve().parent
PARENT=OUT.parent/'full_weight'
spec=importlib.util.spec_from_file_location('fullweight_under_audit',PARENT/'check.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
stored=json.loads((PARENT/'results.json').read_text())
INNER=(4,5,6);BOUNDARY=(0,1,2,3,7,8,9,10)
BS=(1,-9,16,-8)
R=F(7,4);aa=(R+1/R)/2;bb=(R-1/R)/2

def exp_upper(x,n=512):
    assert 0<=x<n+2
    term=F(1);partial=term
    for k in range(1,n+1):term=term*x/k;partial+=term
    next_term=term*x/(n+1)
    # Every later Taylor term ratio is at most x/(n+2).
    return partial+next_term/(1-x/(n+2))

mp.mp.dps=60
beta=4/mp.sqrt(6);Delta=mp.sqrt(2/(19*beta))
points=[(-mp.mpf('1.5'),-mp.mpf('.37'),mp.mpf('1.5')),
        (mp.mpf('0'),mp.mpf('0'),mp.mpf('0')),
        (-Delta,mp.mpf('0'),Delta)]
rows=[]
for name,removed in [('chain',set()),('two_cover_deleted',{(4,5),(5,6)})]:
    relations={(i,j) for i in range(11) for j in range(i+1,11)}-removed
    coefficients={}
    for i,j in relations:
        interval=sum((i,k) in relations and (k,j) in relations for k in range(11))
        coefficients[i,j]=BS[interval] if interval<4 else 0
    F4=11-sum(coefficients.values())
    incident=[sum(abs(v)*(F(1) if j in INNER else F(1,4))
                 for (i,j),v in coefficients.items() if k in (i,j)) for k in INNER]
    logs=[F(15,8)*bb*(aa+1)*v for v in incident]
    outer_abs=sum(abs(v) for (i,j),v in coefficients.items() if j in BOUNDARY)
    insertion=F(len(BOUNDARY),2)+F(5,12)*F(9,4)*(aa+bb+1)**2*outer_abs
    exponent_bounds=[exp_upper(x) for x in logs]
    certified=[]
    for run in stored['quadrature'][name]:
        n=run['nodes_per_axis'];analytic=run['analytic_truncation']
        assert [F(v) for v in analytic['incident_weight_sums']]==incident
        assert [F(v) for v in analytic['log_M_upper_rational']]==logs
        assert F(analytic['derivative_insertion_complex_bound'])==insertion
        bound=sum(4*e*R**(-2*n)/(1-1/R) for e in exponent_bounds)
        claimed=F(analytic['absolute_W_truncation_bound_upward'])
        claimed_derivative=F(analytic['absolute_dW_truncation_bound_upward'])
        assert bound<claimed
        assert bound*insertion<claimed_derivative
        certified.append({'nodes_per_axis':n,'rational_exponential_majorant_terms':513,
          'reported_W_decimal_bound_certified':True,
          'reported_dW_decimal_bound_certified':True,
          'W_bound':analytic['absolute_W_truncation_bound_upward'],
          'dW_bound':analytic['absolute_dW_truncation_bound_upward']})
    discrepancies=[]
    for point in points:
        T=[(j-5)*Delta for j in range(11)]
        for j,v in zip(INNER,point):T[j]=v
        Cs=[1+beta*sum(v*(T[j]-T[i])**2 for (i,jj),v in coefficients.items() if jj==j)/2
            for j in range(11)]
        Tfloat=list(map(float,T))
        module_coeff,moduleF=module.geometry(removed)
        assert module_coeff==coefficients and moduleF==F4
        numericCs=[module.cvalue(j,Tfloat,module_coeff) for j in range(11)]
        discrepancy=max(abs(float(v)-w) for v,w in zip(Cs,numericCs))
        assert discrepancy<2e-13
        for rho in (mp.mpf(1)/8,mp.mpf(1)/4):
            E=[]
            for j in INNER:
                c=Cs[j]
                E.append(mp.mpf(1) if abs(c)<mp.mpf('1e-50') else
                         2*(1-mp.exp(-mp.j*c/2))/(mp.j*c))
            direct=mp.exp(mp.j*F4-mp.j*rho*sum(Cs[j] for j in BOUNDARY)/2)
            product=direct*mp.fprod((1+e)/2 for e in E)
            strata=direct*sum(mp.fprod(E[i] for i,m in enumerate(mask) if m)/8
                              for mask in itertools.product([0,1],repeat=3))
            assert abs(product-strata)<mp.mpf('1e-50')
        discrepancies.append(discrepancy)
    last=stored['quadrature'][name][-1]
    for r,source in last['sources'].items():
        z=complex(source['W']['real'],source['W']['imag'])
        assert abs(z)<1+1e-13
        for term in source['stratum_W']:
            assert abs(complex(term['real'],term['imag']))<1/8+1e-13
    rows.append({'history':name,'exact_incident_weight_sums':[str(v) for v in incident],
                 'analytic_truncation_certificates':certified,
                 'few_point_float_constraint_discrepancies':discrepancies,
                 'few_point_eight_stratum_vs_product_check':True,
                 'stored_W_and_strata_obey_rigorous_norm_bounds_numerically':True})

result={'id':'FULLWEIGHT-QUADRATURE-INDEPENDENT-AUDIT-0.1','all_checks_pass':True,
 'source_range_for_analytic_truncation':'0<=rho<=1/4 only',
 'method':'exact Fraction Taylor exponential upper bound with geometric remainder, independently reconstructed ellipse constants',
 'histories':rows,'new_full_quadratures':0,
 'floating_point_evaluation_error_certified':False,
 'physical_probabilities_certified':False}
(OUT/'quadrature_results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS analytic truncation decimals certified by rational arithmetic; float evaluation remains uncertified')
