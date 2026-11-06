"""Finite-family interval decisions and metadata guards, not proof verification."""
from fractions import Fraction as F
from intervals import I


def interval_decision(error_interval,tolerance):
    tol=I.coerce(tolerance)
    if tol.lo!=tol.hi or tol.lo<=0:raise ValueError('exact positive tolerance required')
    e=I.coerce(error_interval);bound=tol.lo
    if e.lo>=-bound and e.hi<=bound:return 'PASS'
    if e.hi<-bound or e.lo>bound:return 'FAIL'
    return 'HOLD'


def complete_comparison(nominal_error,components,tolerance,fractions):
    if set(components)!=set(fractions) or any(v is None for v in components.values()):
        return {'decision':'HOLD','reason':'unknown or omitted uncertainty component'}
    total=I.coerce(nominal_error)
    for name,width in components.items():
        w=I.coerce(width)
        if w.lo<0:raise ValueError('negative uncertainty budget')
        if w.hi>(I.coerce(tolerance)*I.coerce(fractions[name])).lo:
            return {'decision':'HOLD','reason':'component exceeds predeclared cap: '+name}
        total=total.inflate(w)
    return {'decision':interval_decision(total,tolerance),'error_interval':total.bounds()}


def matching_guard(manifests,invariant_keys):
    issues=[]
    if len(manifests)!=4:return {'decision':'HOLD','issues':['four levels required']}
    ratios=[1,2,4,8];base=manifests[0]
    for i,m in enumerate(manifests):
        for key in invariant_keys:
            if key not in m or m[key] is None or m[key]=='':issues.append(f'level {i}: missing '+key)
            elif m[key]!=base.get(key):issues.append(f'level {i}: changed '+key)
        if m.get('refinement_mode')!='regulated_physical_matching':issues.append(f'level {i}: wrong refinement mode')
        try:
            lam,lam0=F(m['lambda']),F(base['lambda'])
            if lam<=0 or lam0<=0:raise ValueError('nonpositive density')
        except (KeyError,ValueError,TypeError,ZeroDivisionError):
            issues.append(f'level {i}: invalid counting density');continue
        if lam!=lam0*ratios[i]:issues.append(f'level {i}: wrong counting-density ratio')
        # Store ell^4 exactly; avoids accepting an erroneous ell ~ lambda^-1/2.
        if 'ell_power4' not in m or m['ell_power4']!=1/lam:
            issues.append(f'level {i}: wrong discreteness length')
    return {'decision':'HOLD' if issues else 'PASS_METADATA_ONLY','issues':issues,
            'physical_equivalence_proved':False}


def cst_eligibility(closure,run,origin):
    reasons=[key+' unresolved' for key,status in closure.items() if status!='CLOSED_WITH_REVIEWED_EVIDENCE']
    for key in ['lambda0','Lk','Lcg','ensemble_size','seed_manifest','matched_couplings','physical_observable_adapters','total_uncertainty_method']:
        if run.get(key) is None:reasons.append(key+' not frozen')
    if origin!='COUPLED_CST_KERNEL':reasons.append('reference or synthetic data cannot qualify CST dynamics')
    return {'decision':'HOLD_NOT_ELIGIBLE' if reasons else 'ELIGIBILITY_RECORD_COMPLETE_REQUIRES_SCIENTIFIC_REVIEW',
            'reasons':reasons,'physical_pass':False}
