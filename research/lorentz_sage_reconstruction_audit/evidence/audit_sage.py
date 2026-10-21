"""Independent SageMath audit. Run inside a Sage environment: python audit_sage.py

No project solver, generator, inference function or stored design matrix is
imported. Archived coordinates are fixed IEEE-754 inputs, not exact continuum
coordinates. Input records remain retrospective. SPDX-License-Identifier: Apache-2.0
"""
import argparse
import hashlib
import json
import platform
import time
from pathlib import Path
from sage.all import (QQ, PolynomialRing, RealField, block_matrix, identity_matrix,
                      matrix, ones_matrix, vector, zero_matrix)
from sage.env import SAGE_VERSION

HERE = Path(__file__).resolve().parent
CHECKS = []

def check(name, passed, detail=None):
    CHECKS.append(dict(name=name, passed=bool(passed), detail=detail))
    if not passed:
        raise AssertionError(name)

def exact_float(x):
    if isinstance(x, int):
        return QQ(x)
    n, d = float(x).as_integer_ratio()
    return QQ(n) / QQ(d)

def monomials(p):
    t, x, y = p
    # Mixed rows omit sqrt(2); this invertible row rescaling leaves their
    # homogeneous constraints and the unique solution unchanged.
    return [t, x, y, t*t, x*x, y*y, t*x, t*y, x*y]

def design(points, ring):
    return matrix(ring, [monomials(p) for p in points]).transpose()

def weights(points, scale, ring):
    d = design(points, ring)
    n = d.ncols()
    h = identity_matrix(ring, n) + ones_matrix(ring, n, n)
    target = vector(ring, [0, 0, 0, -2, 2, 2, 0, 0, 0])
    # Direct saddle-point KKT solve, unlike X6's normal-equation route.
    kkt = block_matrix(ring, [[h, d.transpose()],
                             [d, zero_matrix(ring, 9, 9)]])
    rhs = vector(ring, [0]*n + list(target))
    sol = kkt.solve_right(rhs)
    a, dual = sol[:n], sol[n:]
    full = vector(ring, [-sum(a)] + list(a)) / ring(scale)**2
    residual = max([abs(v) for v in d*a-target] +
                   [abs(v) for v in h*a+d.transpose()*dual])
    return full, residual

def exact_controls():
    p = matrix(QQ, [[0,0,0],[-1,0,0],[-2,0,0],[-2,1,0],[-2,-1,0],
                    [-2,0,1],[-2,0,-1],[-3,1,1],[-3,1,0],[-3,0,1]])
    q = matrix(QQ, p.rows()); q[3,1] = QQ(11)/10
    target = vector(QQ, [0,0,0,-2,2,2,0,0,0])
    a, _ = weights(p.rows()[1:], 1, QQ)
    b, _ = weights(q.rows()[1:], 1, QQ)
    check('rational_full_rank', design(p.rows()[1:], QQ).rank() == 9)
    check('true_geometry_polynomial_exactness',
          design(p.rows()[1:], QQ)*a[1:] == target and sum(a) == 0)
    check('reconstructed_internal_polynomial_exactness',
          design(q.rows()[1:], QQ)*b[1:] == target and sum(b) == 0)
    defect = design(p.rows()[1:], QQ)*b[1:]-target
    check('wolfram_exact_defect_agreement', defect == vector(QQ,
          [0,-QQ(20)/231,0,0,-QQ(2)/11,0,QQ(40)/231,0,0]),
          [str(v) for v in defect])
    check('first_moment_identity', p.transpose()*b ==
          q.transpose()*b-(q-p).transpose()*b)
    eta = matrix(QQ, [[-1,0,0],[0,1,0],[0,0,1]])
    lor = matrix(QQ, [[QQ(5)/4,-QQ(3)/4,0],[-QQ(3)/4,QQ(5)/4,0],[0,0,1]])
    check('lorentz_metric_exact', lor.transpose()*eta*lor == eta)
    boosted = p*lor.transpose()
    boost_w, _ = weights(boosted.rows()[1:], 1, QQ)
    check('lorentz_weights_invariant', boost_w == a)
    scaled_w, _ = weights([v/7 for v in p.rows()[1:]], 7, QQ)
    check('normalization_scale_invariant', scaled_w == a)
    perm = [3,0,8,1,7,2,6,4,5]
    wp, _ = weights([p.rows()[1:][j] for j in perm], 1, QQ)
    check('support_permutation_equivariant',
          wp[0] == a[0] and all(wp[j+1] == a[perm[j]+1] for j in range(9)))
    check('past_timelike_support', all(v[0] < 0 and v[0]**2 > v[1]**2+v[2]**2
                                     for v in p.rows()[1:]))
    # Overdetermined fixture: root covariance affects the minimizer.
    extended = p.rows()[1:]+[vector(QQ,[-4,1,2]),vector(QQ,[-4,-2,1])]
    u, residual = weights(extended, 1, QQ)
    h = identity_matrix(QQ,len(extended))+ones_matrix(QQ,len(extended),len(extended))
    check('unique_minimum_variance_kkt', residual == 0)
    check('shared_root_covariance_identity', u*u == u[1:]*(h*u[1:]))
    d = design(extended, QQ)
    wrong = d.transpose()*(d*d.transpose()).solve_right(target)
    check('omitted_root_covariance_negative_control', wrong != u[1:])
    singular = [vector(QQ,[-j,0,0]) for j in range(1,12)]
    rejected = False
    try:
        weights(singular, 1, QQ)
    except (ValueError, ZeroDivisionError, ArithmeticError):
        rejected = True
    check('rank_deficient_support_rejected', rejected)
    check('wrong_signature_negative_control', design(p.rows()[1:], QQ)*(-a[1:]) != target)
    poly = PolynomialRing(QQ, names=('d','r'))
    dd, rr = poly.gens()
    check('mse_cross_term_identity', (dd+rr)**2-dd**2-rr**2-2*dd*rr == 0)
    return dict(status='PASS', checks=len(CHECKS), physical_x_response=str(defect[1]),
                true_weights=[str(v) for v in a], reconstructed_weights=[str(v) for v in b])

def max_scaled(a, b, atol, rtol):
    return max(float(abs(x-y)/(atol+rtol*abs(y))) for x,y in zip(a,b))

def audit_record(row, fields):
    result = {k:row[k] for k in ('phase','index','seed','status','input_sha256')}
    if row['status'] != 'COMPLETE':
        result['audit_status'] = 'PRESERVED_UNAVAILABLE'
        return result
    scale = exact_float(row['scale'])
    true = [vector(QQ,[exact_float(v) for v in p]) for p in row['true_points']]
    features = {
        'original':[vector(QQ,[exact_float(v) for v in p]) for p in row['reconstructed_features']],
        'projected':[vector(QQ,[exact_float(v) for v in p]) for p in row['projected_features']],
        'oracle':[p/scale for p in true[1:]]}
    calc = {}; convergence = {}; agreement = {}; moment_residuals = {}
    for arm, coords in features.items():
        check('%s/%s/%s/rank'%(row['phase'],row['index'],arm), design(coords,QQ).rank()==9)
        low, lowres = weights(coords,scale,RealField(128))
        high, highres = weights(coords,scale,RealField(256))
        convergence[arm] = max_scaled(high,vector(RealField(256),low),
                                     RealField(256)('1e-22'),RealField(256)('1e-22'))
        saved = vector(RealField(256),[exact_float(v) for v in row['saved_'+arm]])
        agreement[arm] = max_scaled(high,saved,RealField(256)('1e-8'),RealField(256)('1e-7'))
        check('%s/%s/%s/precision'%(row['phase'],row['index'],arm), convergence[arm]<=1)
        check('%s/%s/%s/archive_weights'%(row['phase'],row['index'],arm),agreement[arm]<=1)
        check('%s/%s/%s/kkt'%(row['phase'],row['index'],arm), highres<RealField(256)('1e-50'))
        calc[arm]=high
        moment_residuals[arm]=[float(v) for v in design(true[1:],RealField(256))*high[1:]-
                               vector(RealField(256),[0,0,0,-2,2,2,0,0,0])]
    R=RealField(256); field_results=[]
    for spec,saved in zip(fields,row['saved_fields']):
        k=vector(R,[exact_float(v) for v in spec['k']]); phase=R(exact_float(spec['phase']))
        root=phase.cos() if spec['kind']=='cos' else phase.sin()
        derivative=-phase.sin() if spec['kind']=='cos' else phase.cos()
        truth=(k[0]**2-k[1]**2-k[2]**2)*root
        uu=vector(R,[k*vector(R,p) for p in true[1:]])
        contrast=vector(R,[(v+phase).cos()-root if spec['kind']=='cos' else
                           (v+phase).sin()-root for v in uu])
        linear=derivative*uu; quadratic=-root*vector(R,[v*v for v in uu])/2
        remainder=contrast-linear-quadratic
        errors={arm:val[1:]*contrast-truth for arm,val in calc.items()}
        parts={arm:[val[1:]*linear,val[1:]*quadratic-truth,val[1:]*remainder]
               for arm,val in calc.items()}
        ratios={arm:max_scaled([errors[arm]],[R(exact_float(saved['errors'][j]))],
                              R('1e-8'),R('1e-7'))
                for arm,j in [('original',0),('projected',2),('oracle',4)]}
        check('%s/%s/%s/archive_errors'%(row['phase'],row['index'],spec['name']),max(ratios.values())<=1)
        for arm in calc:
            check('%s/%s/%s/%s/taylor'%(row['phase'],row['index'],spec['name'],arm),
                  abs(sum(parts[arm])-errors[arm])<R('1e-50'))
        disc=errors['oracle']; recon=errors['original']-disc
        identity=errors['original']**2-disc**2-recon**2-2*disc*recon
        check('%s/%s/%s/mse'%(row['phase'],row['index'],spec['name']),abs(identity)<R('1e-50'))
        check('%s/%s/%s/oracle_low_degree'%(row['phase'],row['index'],spec['name']),
              max(abs(v) for v in parts['oracle'][:2])<R('1e-50'))
        field_results.append(dict(name=spec['name'],truth=float(truth),
            errors={k:float(v) for k,v in errors.items()},
            taylor={k:[float(v) for v in vs] for k,vs in parts.items()},
            decomposition=dict(discretization_square=float(disc**2),reconstruction_square=float(recon**2),
                               cross_term=float(2*disc*recon)),archive_error_ratios=ratios))
    result.update(audit_status='PASS',weight_tolerance_ratios=agreement,precision_tolerance_ratios=convergence,
                  physical_moment_residuals=moment_residuals,fields=field_results)
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--exact-only',action='store_true')
    args=ap.parse_args();start=time.time()
    summary=dict(schema='x6.sage-independent-audit/1',sage_version=SAGE_VERSION,
                 python=platform.python_version(),mode='EXACT_ONLY' if args.exact_only else 'ARCHIVED_AUDIT',
                 new_cloud_confirmation='NOT_RUN',status='RUNNING')
    rows=[]
    try:
        summary['exact']=exact_controls()
        print('Exact Sage controls: PASS (%d checks)'%summary['exact']['checks'],flush=True)
        if not args.exact_only:
            raw=(HERE/'inputs.json').read_bytes();data=json.loads(raw)
            summary.update(input_sha256=hashlib.sha256(raw).hexdigest(),source_commit=data['source_commit'])
            for row in data['records']:
                audited=audit_record(row,data['fields']);rows.append(audited)
                print('%s %02d %s'%(row['phase'],row['index'],audited['audit_status']),flush=True)
                (HERE/'records.partial.json').write_text(json.dumps(rows,indent=2)+'\n')
            import math
            summary['phases']={}
            for phase in ['calibration','test']:
                available=[r for r in rows if r['phase']==phase and r['audit_status']=='PASS']
                fs=[f for r in available for f in r['fields']]
                means={k:sum(f['decomposition'][k] for f in fs)/len(fs)
                       for k in ['discretization_square','reconstruction_square','cross_term']}
                rms={a:math.sqrt(sum(f['errors'][a]**2 for f in fs)/len(fs))
                     for a in ['original','projected','oracle']}
                summary['phases'][phase]=dict(scheduled=32,complete=len(available),rmse=rms,
                    mse_original=sum(f['errors']['original']**2 for f in fs)/len(fs),decomposition=means,
                    rmse_ratio_oracle_original=rms['oracle']/rms['original'])
            (HERE/'records.json').write_text(json.dumps(rows,indent=2)+'\n')
        summary['status']='PASS'
    except Exception as exc:
        summary.update(status='FAIL',error=repr(exc))
        raise
    finally:
        summary.update(elapsed_seconds=time.time()-start,checks_total=len(CHECKS),
                       checks_passed=sum(c['passed'] for c in CHECKS))
        stem='exact' if args.exact_only else 'audit'
        (HERE/(stem+'_summary.json')).write_text(json.dumps(summary,indent=2)+'\n')
        (HERE/(stem+'_checks.json')).write_text(json.dumps(CHECKS,indent=2)+'\n')
        print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':
    main()
