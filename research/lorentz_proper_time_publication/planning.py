"""Finite-sample planning examples; no simulation and no minimum-budget claim."""
import json
import math
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING
from scipy.stats import binom, poisson


def planning():
    # Decimal arithmetic fixes strict integer endpoints without float rounding.
    d, relative_error, theta = 4, Decimal('0.1'), Decimal('0.1')
    rminus, rplus = (1-relative_error)**d, (1+relative_error)**d
    rows = []
    for scale, m in [('1', 300000), ('0.2', 480), ('1', 550000), ('0.2', 880)]:
        p = (theta/Decimal(scale))**d
        mean = m*p
        lower = int((mean*rminus).to_integral_value(rounding=ROUND_FLOOR))+1
        upper = int((mean*rplus).to_integral_value(rounding=ROUND_CEILING))-1
        # Complementary tails avoid subtracting two near-one CDFs.
        success = 1-binom.cdf(lower-1, m, float(p))-binom.sf(upper, m, float(p))
        h = lambda r: float(r)*math.log(float(r))-float(r)+1
        bound = min(1., math.exp(-float(mean)*h(rminus))+math.exp(-float(mean)*h(rplus)))
        rows.append(dict(scale_over_T=float(scale), m=m, p=float(p), expected_K=float(mean),
                         accepted_K=[lower, upper], binomial_success_probability=float(success),
                         chernoff_failure_upper_bound=bound))
    return dict(scope='Fixed known flat 4D diamond, iid sampling, tau/T=0.1; strict relative error <0.1',
                calculation='Exact binomial expressions evaluated numerically with SciPy, not interval arithmetic',
                minimum_budget_claim=False, rows=rows,
                poisson_mean_30_success=float(1-poisson.cdf(19, 30)-poisson.sf(43, 30)))


if __name__ == '__main__':
    print(json.dumps(planning(), indent=2, allow_nan=False))
