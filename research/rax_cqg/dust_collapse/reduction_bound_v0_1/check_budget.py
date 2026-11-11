"""Stop only on an upper error bound; report HOLD when the mode cap is exceeded."""
from pathlib import Path
import argparse,json
from flint import arb,ctx
import bounds as b

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--field',type=int,required=True);p.add_argument('--density',type=int,required=True)
    p.add_argument('--clock',type=int,required=True);p.add_argument('--tolerance',default='1/100')
    p.add_argument('--numerical-error',default='0');p.add_argument('--mode-cap',type=int,default=1000000)
    p.add_argument('--composition',action='store_true');p.add_argument('--output')
    a=p.parse_args();ctx.prec=192
    if min(a.field,a.density,a.clock)<0 or a.field<6 or a.clock<2:p.error('this schedule retains the previous 15 states: field>=6, density>=0, clock>=2')
    tol=arb(a.tolerance);numerics=arb(a.numerical_error)
    if not tol>0 or not numerics>=0 or a.mode_cap<1:p.error('positive tolerance, positive mode cap and nonnegative certified numerical error required')
    root=Path(__file__).resolve().parent
    rows=json.loads((root/'results/geometry_constants.json').read_text());c=b.constants(rows)
    if a.composition:
        abel=json.loads((root/'results/Abel_certificate.json').read_text())
        _,cut=b.sewing_cut_bound(rows,c,abel['chosen_epsilon'],a.field,a.density,a.clock)
        error=cut+arb(abel['chosen_error'])+numerics
        count=b.dimension(a.field,a.density,a.clock,False)
        scope='memory-preserving composed amplitudes on the H-unit ball of the original four-state space'
    else:
        result=b.single_bounds(c,a.field,a.density,a.clock)
        error=arb(result['full_C_M_class_error'])+numerics;count=result['invariant_dimension']
        scope='single-kernel V-prime response error on C_M, M=sqrt(261)'
    decision='TOLERANCE_PASS' if error<tol else 'EXTEND_BASIS'
    if count>a.mode_cap:decision='HOLD_RESOURCE_CAP'
    data={'decision':decision,'scope':scope,'cutoffs':[a.field,a.density,a.clock],
          'basis_modes':count,'mode_cap':a.mode_cap,'upper_error_bound':b.pack(error),
          'tolerance':a.tolerance,'numerical_error_input':a.numerical_error,
          'large_matrix_computed':False,
          'numerical_error_requirement':'zero means the mathematical exact-projection bound; an implemented quadrature must supply its own certified error'}
    if a.output:Path(a.output).write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':main()
