"""Generate rigorous single-kernel and memory-preserving sewing certificates."""
import json
from pathlib import Path
import sympy as s
from flint import arb,acb,ctx
import bounds as b

ROOT=Path(__file__).resolve().parent

def parse_rows():return json.loads((ROOT/'results/geometry_constants.json').read_text())

def scan_abel(tolerance='1/100'):
    tol=arb(tolerance);beta=b.pc.beta();hist=[];frozen=acb(0)
    for l in b.pc.histories():
        for r in b.pc.histories():
            h,F=b.joint_data(l,r);zero=b.scalar_pair(h,'0')
            hist.append((l,r,h,zero));frozen+=acb(0,F).exp()*zero[0]/(128*1089)
    prior=json.loads((ROOT/'inputs/prior_sewing_verification.json').read_text())['full_1089_sum_all_atom']['0']['arb_enclosure']
    if not frozen.overlaps(acb(arb(prior['real']),arb(prior['imag']))):raise ArithmeticError('frozen 1089-history Abel control differs')
    c=b.constants(parse_rows());factor=(1+c['zeta_abs']**2).sqrt()/4
    scans=[]
    for k in range(1,12):
        eps='1/'+str(7**k);delta=[arb(0),arb(0)]
        for l,r,h,zero in hist:
            value=b.scalar_pair(h,eps)
            for n in (0,1):delta[n]+=abs(value[n]-zero[n])/1089
        error=factor*max(x.upper() for x in delta)
        scans.append({'epsilon':eps,'scalar_difference_means':[b.pack(x) for x in delta],
                      'four_state_class_Abel_error_bound':b.pack(error)})
        print(json.dumps(scans[-1]),flush=True)
        if error<tol/4:break
    else:raise ArithmeticError('Abel scan failed declared finite search budget')
    return {'method':'exact enclosed Gaussian difference to the analytic Abel value, followed by an analytic absolute dust bound',
            'histories':1089,'parity_off_blocks_exactly_zero':True,
            'frozen_all_atom_sum_reproduced':True,'scans':scans,'chosen_epsilon':scans[-1]['epsilon'],
            'chosen_error':scans[-1]['four_state_class_Abel_error_bound']}

def ceil_certified(x):
    return int(x.upper().ceil().unique_fmpz())

def polynomial_cutoff(required,minimum=0):
    lo=minimum;hi=max(1,lo)
    while not arb((hi+1)*(hi+2))>=required:hi=2*hi+1
    while lo<hi:
        mid=(lo+hi)//2
        if arb((mid+1)*(mid+2))>=required:hi=mid
        else:lo=mid+1
    return lo

def single_budget(c,tolerance):
    # Six squared contributions: three sectors in each pairing direction.
    h=arb(tolerance)/(arb(261).sqrt()*arb(6).sqrt())
    f=max(c[d]['field'].upper() for d in ('forward','backward'))
    rho=max(sum(x*x for x in c[d]['density']).sqrt().upper() for d in ('forward','backward'))
    clock=max(sum(x*x for x in c[d]['clock']).sqrt().upper() for d in ('forward','backward'))
    N=max(6,ceil_certified(arb(f)/(2*h)-2));D=polynomial_cutoff(arb(rho)/h);T=polynomial_cutoff(arb(clock)/h,2)
    result=b.single_bounds(c,N,D,T)
    if not arb(result['forward_class_bound'])<arb(tolerance) or not arb(result['backward_class_bound'])<arb(tolerance):raise ArithmeticError('single-step budget not certified')
    if not arb(result['full_C_M_class_error'])<arb(tolerance):raise ArithmeticError('infinite state-class budget not certified')
    result['tolerance']=tolerance;result['decision']='ANALYTIC_TOLERANCE_PASS_NOT_MATRIX_COMPUTED'
    return result

def sewing_budget(rows,c,abel,tolerance):
    eps=abel['chosen_epsilon'];epsilon=arb(eps)
    # Half the budget is reserved for the cut tail; Abel uses at most one quarter.
    cut_budget=arb(tolerance)/2
    h=(cut_budget*epsilon**2/(96*arb.pi()**2)).sqrt()
    maxima={'field_energy':arb(0),'density_energy':arb(0),'clock_energy':arb(0)}
    for row in rows:
        for side in ('left','right'):
            for n in (0,1):
                for density in ('0','+'):
                    _,energies=b.sewing_sector(row,side,n,density,eps,6,0,2)
                    for key,value in energies.items():maxima[key]=arb(max(maxima[key].upper(),value.upper()))
    N=max(6,ceil_certified(maxima['field_energy'].sqrt()/(2*h)-2))
    D=polynomial_cutoff(maxima['density_energy'].sqrt()/h)
    T=polynomial_cutoff(maxima['clock_energy'].sqrt()/h,2)
    envelope,cut=b.sewing_cut_bound(rows,c,eps,N,D,T)
    total=cut+arb(abel['chosen_error'])
    if not total<arb(tolerance):raise ArithmeticError('composition budget not certified')
    return {'epsilon':eps,'cutoffs':[N,D,T],'labelled_cut_dimension':b.dimension(N,D,T,False),
            'matrix_entry_cut_bounds':[[b.pack(x) for x in row] for row in envelope],
            'cut_class_bound':b.pack(cut),'Abel_class_bound':abel['chosen_error'],
            'total_class_bound_before_numerics':b.pack(total),'tolerance':tolerance,
            'numerical_budget_remaining':b.pack(arb(tolerance)-total),
            'conditional_energy_maxima':{k:b.pack(v) for k,v in maxima.items()},
            'decision':'ANALYTIC_TOLERANCE_PASS_NOT_MATRIX_COMPUTED'}

def run():
    ctx.prec=192
    rows=b.geometry_records();b.write('results/geometry_constants.json',rows);c=b.constants(rows)
    operator={side:{'field':b.pack(c[side]['field']),'density':[b.pack(x) for x in c[side]['density']],
                   'clock':[b.pack(x) for x in c[side]['clock']]} for side in ('forward','backward')}
    operator['kernel_norm']=b.pack(c['kernel_norm']);operator['zeta']={'real':b.pack(c['zeta'].real),'imag':b.pack(c['zeta'].imag),'absolute':b.pack(c['zeta_abs'])}
    b.write('results/operator_constants.json',operator)
    stages=[b.single_bounds(c,*cut) for cut in [(6,0,2),(12,1,4),(24,3,8),(48,7,16),(96,15,32),(192,31,64)]]
    b.write('results/basis_progression.json',stages)
    tolerance='1/100'
    single=single_budget(c,tolerance);print('single certificate',json.dumps(single),flush=True)
    abel=scan_abel(tolerance);b.write('results/Abel_certificate.json',abel)
    sewn=sewing_budget(rows,c,abel,tolerance)
    resource_cap=1000000
    result={'status':'ANALYTIC_UPPER_BOUNDS_PROVED',
            'state_class':'Single step: C_M={f in V: ||f||_H<=1, ||f||_V<=sqrt(261)}, including all coherent H-unit combinations of the four original states, tested against the entire V unit ball in both directions. Composition: both outer states in the H-unit ball of the original four-state span.',
            'error_metric':'V-prime response norm in either single-step direction; absolute sesquilinear-amplitude error for memory-preserving composition',
            'all_four_inputs_covered':True,'forward_positive_input_factor':operator['zeta'],
            'original_V_Gram_diagonal':[65,261,65,261],
            'single_step':single,'composition':sewn,
            'resource_cap_basis_modes':resource_cap,
            'single_step_resource_decision':'HOLD' if single['invariant_dimension']>resource_cap else 'WITHIN_CAP',
            'composition_resource_decision':'HOLD' if sewn['labelled_cut_dimension']>resource_cap else 'WITHIN_CAP',
            'large_projection_matrices_computed':False,
            'physical_CST_evolution':'NOT_CONSTRUCTED'}
    b.write('results/reduction_certificate.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':run()
