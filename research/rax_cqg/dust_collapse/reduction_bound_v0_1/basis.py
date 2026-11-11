"""Nested invariant test modes, with the original four states embedded exactly."""
from itertools import product
from math import factorial
from pathlib import Path
import argparse,json
import sympy as s
from bounds import dimension

X,Y=s.symbols('qs qa',real=True)

def gaussian_moment(poly):
    total=s.Rational(0)
    for (a,b),c in s.Poly(s.expand(poly),X,Y).terms():
        if a%2 or b%2:continue
        total+=c*s.Rational(factorial(a),4**(a//2)*factorial(a//2))*s.Rational(factorial(b),4**(b//2)*factorial(b//2))
    return s.simplify(total)

def hermite_polynomial(ns,na):
    return s.hermite(ns,X)*s.hermite(na,Y)/s.sqrt(2**(ns+na)*factorial(ns)*factorial(na))

def original_field_embedding(n):
    target=(1+X*X+Y*Y)**2*(s.sqrt(2)*X if n else 1)
    coefficients=[];reconstruction=0
    for ns in range(n+5):
        for na in range(n+5-ns):
            basis=hermite_polynomial(ns,na);value=gaussian_moment(target*basis)
            if value:
                coefficients.append({'ns':ns,'na':na,'coefficient':str(value)})
                reconstruction+=value*basis
    if s.expand(reconstruction-target)!=0:raise ArithmeticError('original field embedding incomplete')
    norm=s.simplify(sum(s.sympify(x['coefficient'])**2 for x in coefficients))
    if norm!=(261 if n else 65):raise ArithmeticError('weighted norm differs')
    return {'field_parity':n,'U_field_polynomial':str(s.expand(target)),
            'coefficients':coefficients,'V_norm_squared':int(norm)}

def labels(N,D,T,cap=1000000):
    count=dimension(N,D,T)
    if count>cap:raise ValueError('HOLD: requested basis exceeds the declared mode cap')
    local=list(product(range(-1,D+1),range(T+1))) # -1 is the isolated atom.
    result=[]
    for ns in range(N+1):
        for na in range(N+1-ns):
            for a in local:
                for b in local:
                    if a>b or (a==b and na%2):continue
                    result.append({'field':[ns,na],'point_1_density_clock':list(a),
                                   'point_2_density_clock':list(b),
                                   'swapped_partner':a!=b,'swap_relative_sign':(-1)**na,
                                   'orbit_normalization':'1/sqrt(2)' if a!=b else '1'})
    if len(result)!=count:raise ArithmeticError('invariant dimension formula differs')
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--field',type=int,default=6);p.add_argument('--density',type=int,default=0)
    p.add_argument('--clock',type=int,default=2);p.add_argument('--output',required=True)
    a=p.parse_args()
    data={'cutoffs':[a.field,a.density,a.clock],
          'one_point_density_basis':'atom: sqrt(2)*1_atom; positive k: sqrt(2*(2*k+1))*P_k(2*r-1)*1_positive',
          'one_point_clock_basis':'sqrt(2*k+1)*P_k(t)',
          'quotient_normalization':'sqrt(2)',
          'test_weight':'(1+qs^2+qa^2)^-2',
          'response_dual_weight':'(1+qs^2+qa^2)^2 relative to the unweighted Hermite product',
          'modes':labels(a.field,a.density,a.clock),
          'original_fields':[original_field_embedding(n) for n in (0,1)],
          'original_density_embeddings':{'0':'atom,atom','+':'sqrt(2/3)*sym(atom,positive_0) + 1/sqrt(3)*(positive_0,positive_0)'},
          'original_clock_modes':[0,0],
          'previous_15_states_included':a.field>=6 and a.density>=0 and a.clock>=2}
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','modes':len(data['modes']),'original_V_norms_squared':[65,261,65,261]}))

if __name__=='__main__':main()
