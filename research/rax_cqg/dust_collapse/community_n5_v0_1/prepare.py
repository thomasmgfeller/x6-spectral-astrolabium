"""Exact mathematical preparation only: never evaluates an n=5 field integral."""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, prod
from functools import lru_cache
from pathlib import Path
import hashlib, json, sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'inputs'))
import geometry as g
import memory as m
import intervals as v
import gauss
import bounds

BASE = '3177458a7f8545f845054e235cd3dcd7e829eff3'
CHUNK = 65536

def require(ok, message):
    if not ok: raise RuntimeError(message)

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()

def digest(obj): return hashlib.sha256(canonical(obj)).hexdigest()

@lru_cache(None)
def bernstein_vector(items, degrees):
    """Degree-elevate each polynomial to the shared clock multidegree."""
    values = []
    for index in product(*(range(d+1) for d in degrees)):
        total = F(0)
        for key, c in items:
            if any(a > b for a, b in zip(key, index)): continue
            factor = c
            for a, b, d in zip(key, index, degrees):
                factor *= F(comb(b, a), comb(d, a))
            total += factor
        values.append(total)
    return tuple(values)

def linear_density_range(polys, n):
    # The phase is linear in each w_j. At each clock Bernstein index,
    # all density-corner extrema are sums of negative/positive coefficients.
    degrees = tuple(max((key[j] for p in polys for key in p), default=0) for j in range(n))
    vectors = [bernstein_vector(tuple(sorted(p.items())), degrees) for p in polys]
    low = min(sum((min(F(0), x) for x in row), F(0)) for row in zip(*vectors))
    high = max(sum((max(F(0), x) for x in row), F(0)) for row in zip(*vectors))
    return low, high

def fast_bounds(order, h):
    n = len(order)
    polys, _ = g.action_polynomials(order, h)
    result = []
    for j in range(n):
        first = [g.scale(g.derivative(p, j), -1) for p in polys]
        second = [g.scale(g.derivative(g.derivative(p, j), j), F(-1, 2)) for p in polys]
        r1, r2 = linear_density_range(first, n), linear_density_range(second, n)
        result.append({'D': max(map(abs, r1)), 'A': max(map(abs, r2)),
                       'first_range': r1, 'quadratic_range': r2})
    return result

def select(all_bounds, mu, n):
    # Conservative coordinatewise maxima preserve the existing proof.
    maxima = [(max(b[j]['D'] for b in all_bounds)*abs(mu),
               max(b[j]['A'] for b in all_bounds)*abs(mu)) for j in range(n)]
    qs, errors = [], []
    for j, (D, A) in enumerate(maxima):
        for q in range(8, 129, 2):
            e = gauss.error_bound(q, D, A, j, n)
            if e <= F(1, 10**9):
                qs.append(q); errors.append(e); break
        else: raise RuntimeError('No order <=128 meets the fixed quadrature budget')
    return qs, errors, maxima

def build():
    orders = list(m.natural_orders(5))
    require(len(orders) == 357 and set(orders) == set(v.brute_orders(5)), 'Independent n=5 enumeration')
    b0 = [fast_bounds(p, F(1, 2)) for p in orders]
    configs = []
    for h in [F(1, 4), F(1, 2)]:
        scale = (2*h)**2
        bs = [[{k: x*scale if k in ('D','A') else tuple(y*scale for y in x)
                for k, x in row.items()} for row in b] for b in b0]
        for mu in [F(1, 4), F(1)]:
            qs, errors, maxima = select(bs, mu, 5)
            count = prod(qs)
            polys = {tuple(sorted(p.items())) for order in orders for p in g.action_polynomials(order, h)[0]}
            configs.append({'id': f'h{h.numerator}d{h.denominator}_mu{mu.numerator}d{mu.denominator}',
                'h': str(h), 'mu': str(mu), 'q': qs, 'nodes': count,
                'shards': (count+CHUNK-1)//CHUNK,
                'unique_polynomials': len(polys), 'characteristic_calls': count*len(polys),
                'quadrature_radius': str(sum(errors, F(0))),
                'coordinate_errors': list(map(str, errors)),
                'derivative_maxima': [[str(D),str(A)] for D,A in maxima]})
    tails=[]
    for h in [F(1,4), F(1,2)]:
        for alpha in [1,2]:
            c5 = bounds.coefficient(357,h,alpha,5)
            c6 = bounds.coefficient(4824,h,alpha,6)
            delta = bounds.anchored_tail(4824,h,alpha,6)
            z6 = sum((bounds.coefficient(N,h,alpha,n) for n,N in enumerate([1,1,2,7,40,357,4824])),F(0))
            tails.append({'h':str(h),'alpha':alpha,'c5':str(c5),'c6':str(c6),
                'delta6':str(delta),'Zmax':str(z6+delta),
                'old_phase_tail_fraction':str((c5+c6+delta)/(z6+delta)),
                'after_n5_phase_tail_fraction':str((c6+delta)/(z6+delta)),
                'n5_share_of_old_tail':str(c5/(c5+c6+delta))})
    return {'schema':'cst-dust-n5-community-plan-v1','source_main':BASE,
        'status':'PREPARED_NOT_PRODUCTION_RUN','project_budget_chf':0,
        'n':5,'natural_orders':[list(p) for p in orders],
        'chunk_nodes':CHUNK,'kernel_timeout_seconds':120,
        'amplitude_tolerance':'1/100000000','arithmetic_budget':'1/250000000',
        'configs':configs,'analytic_mu_zero':'A_p=1 exactly for every geometry',
        'postprocess_g_over_pi':['0','1/18','1/9'],'postprocess_alpha':[1,2],
        'tail_budget':tails,'all_eight_physical_gates':'HOLD'}

if __name__ == '__main__':
    plan=build()
    (ROOT/'plan.json').write_text(json.dumps(plan,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'plan_sha256':digest(plan),'configs':[{k:c[k] for k in ('id','q','nodes','shards','unique_polynomials')} for c in plan['configs']]},indent=2))
